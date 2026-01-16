import torch
import einops
from .asym import GELUTanh, ConvND, AsymptoticSphereNorm

class FactorizedConvND(torch.nn.Module):
    def __init__(self, dim, in_chs, out_chs, kernel_size=1, bias=False):
        super().__init__()
        self.dim = dim
        self.in_chs, self.out_chs = in_chs, out_chs
        g1, g2 = self._pick_groups(in_chs, out_chs)
        self.g1, self.g2 = g1, g2
        self.conv1 = ConvND(dim, in_chs, in_chs, kernel_size, groups=g1, bias=bias, padding=(kernel_size - 1)//2)
        self.conv2 = ConvND(dim, in_chs, out_chs, kernel_size, groups=g2, bias=bias, padding=(kernel_size - 1)//2)

    def _pick_groups(self, in_chs, out_chs):
        def _divisors(n):
            divs = []
            i = 1
            while i * i <= n:
                if n % i == 0:
                    divs.append(i)
                    if i != n // i:
                        divs.append(n // i)
                i += 1
            return sorted(divs)
        divs = _divisors(in_chs)
        best_g1, best_g2, best_cost = 1, in_chs, float('inf')
        for d in divs:
            g1, g2 = d, in_chs // d
            cost = (in_chs * in_chs / g1) + (in_chs * out_chs / g2)
            if cost < best_cost:
                best_cost, best_g1, best_g2 = cost, g1, g2
        return best_g1, best_g2

    def forward(self, x):
        x = self.conv1(x)
        x = einops.rearrange(x, 'b (g1 g2) ... -> b (g2 g1) ...', g1=self.g1, g2=self.g2)
        x = self.conv2(x)
        return x

class FactorizedSqueezeExciteND(torch.nn.Module):
    def __init__(self, dim, channels, se_ratio=0.25):
        super().__init__()
        AdaptivePool = [torch.nn.AdaptiveAvgPool1d, torch.nn.AdaptiveAvgPool2d, torch.nn.AdaptiveAvgPool3d][dim-1]
        self.pool = AdaptivePool(1)
        mid_chs = int(channels * se_ratio)
        self.conv_reduce = FactorizedConvND(dim, channels, mid_chs, kernel_size=1, bias=True)
        self.act = GELUTanh()
        self.conv_expand = FactorizedConvND(dim, mid_chs, channels, kernel_size=1, bias=True)
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x):
        s = self.pool(x)
        s = self.conv_reduce(s)
        s = self.act(s)
        s = self.conv_expand(s)
        s = self.sigmoid(s)
        return x * s

class FactorizedResBlockND(torch.nn.Module):
    def __init__(self, dim, channels, se_ratio=0.25, kernel_size=3):
        super().__init__()
        self.conv1 = FactorizedConvND(dim, channels, channels, kernel_size=kernel_size)
        self.norm1 = AsymptoticSphereNorm()
        self.act1 = GELUTanh()
        self.conv2 = FactorizedConvND(dim, channels, channels, kernel_size=kernel_size)
        self.norm2 = AsymptoticSphereNorm()
        self.se = FactorizedSqueezeExciteND(dim, channels, se_ratio=se_ratio)

    def forward(self, x):
        skip = x
        out = self.conv1(x)
        out = self.norm1(out)
        out = self.act1(out)
        out = self.conv2(out)
        out = self.norm2(out)
        out = self.se(out)
        out = out + skip
        return out