import torch, math
from typing import Optional
from timm.layers import use_fused_attn

def ConvND(dim, *args, **kwargs):
    conv_cls = [torch.nn.Conv1d, torch.nn.Conv2d, torch.nn.Conv3d][dim-1]
    return conv_cls(*args, **kwargs)

def ConvTransposeND(dim, *args, **kwargs):
    conv_cls = [torch.nn.ConvTranspose1d, torch.nn.ConvTranspose2d, torch.nn.ConvTranspose3d][dim-1]
    return conv_cls(*args, **kwargs)

class GELUTanh(torch.nn.Module):
    def __init__(self):
        super().__init__()
    def forward(self, x):
        return torch.nn.functional.gelu(x, approximate='tanh')

class SphereNorm(torch.nn.Module):
    def __init__(self, r=127.0, eps=1e-12, p=2.0, dim=1):
        super().__init__()
        self.r=r; self.eps=eps; self.p=p; self.dim=dim;
    def forward(self, x):
        return self.r * torch.nn.functional.normalize(x, p=self.p, dim=self.dim, eps=self.eps)
        
class Quantize(torch.nn.Module):
    def __init__(self):
        super().__init__()
    def forward(self, x):
        if self.training:
            x += torch.rand_like(x) - 0.5
        else:
            x = x.round()
        return x

class Residual(torch.nn.Module):
    def __init__(self, main, d):
        super().__init__()
        self.main = main
        self.drop_path = d

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if self.training and self.drop_path > 0.0:
            if torch.rand(1, device=x.device).item() < self.drop_path:
                return x
        return x + self.main(x)

class ConvNormActQuantND(torch.nn.Module):
    def __init__(self, dim, in_channels, out_channels, norm_layer, act_layer, quant_layer,
                 kernel_size=3, stride=1, groups=1, bias=False, padding=None):
        super().__init__()
        Conv = [torch.nn.Conv1d, torch.nn.Conv2d, torch.nn.Conv3d][dim-1]
        if padding is None:
            padding = kernel_size//2
        self.conv = Conv(in_channels, out_channels, kernel_size, stride,
                         padding=padding, groups=groups, bias=bias)
        self.norm = norm_layer()
        self.act = act_layer()
        self.quant = quant_layer()
    def forward(self, x):
        return self.quant(self.act(self.norm(self.conv(x))))

class MBConvND(torch.nn.Module):
    def __init__(self, dim, in_channels, norm_layer, act_layer, quant_layer, expand_ratio=4):
        super().__init__()
        mid_channels = in_channels * expand_ratio
        self.inverted_conv = ConvNormActQuantND(
            dim, in_channels, mid_channels, kernel_size=1, bias=True,
            norm_layer=torch.nn.Identity, act_layer=act_layer, quant_layer=torch.nn.Identity)
        self.depth_conv = ConvNormActQuantND(
            dim, mid_channels, mid_channels, kernel_size=3, groups=mid_channels, bias=True,
            norm_layer=torch.nn.Identity, act_layer=act_layer, quant_layer=torch.nn.Identity)
        self.point_conv = ConvNormActQuantND(
            dim, mid_channels, in_channels, kernel_size=1, bias=False,
            norm_layer=norm_layer, act_layer=torch.nn.Identity, quant_layer=quant_layer)
    def forward(self, x):
        x = self.inverted_conv(x)
        x = self.depth_conv(x)
        x = self.point_conv(x)
        return x

class AttentionND(torch.nn.Module):
    def __init__(
        self,
        dim: int,
        embed_dim: int,
        dim_out: Optional[int] = None,
        dim_head: int = 32,
        attn_drop: float = 0.0,
        proj_drop: float = 0.0,
        norm_layer=torch.nn.Identity,
        quant_layer=torch.nn.Identity,
    ):
        super().__init__()
        assert dim in (1, 2, 3), "`dim` must be 1, 2 or 3"
        assert use_fused_attn(), "no support for fused attention"
        Conv = [torch.nn.Conv1d, torch.nn.Conv2d, torch.nn.Conv3d][dim - 1]
        dim_out = dim_out or embed_dim
        dim_attn = dim_out
        self.num_heads = dim_attn // dim_head
        self.dim_head = dim_head
        self.scale = dim_head**-0.5
        self.qkv = Conv(embed_dim, dim_attn * 3, 1, bias=True)
        self.attn_drop = torch.nn.Dropout(attn_drop)
        self.proj = ConvNormActQuantND(dim=dim, in_channels=dim_attn, out_channels=dim_out,
                                  norm_layer=norm_layer, act_layer=torch.nn.Identity, quant_layer=quant_layer,
                                  kernel_size=1, bias=True)
        self.proj_drop = torch.nn.Dropout(proj_drop)

    def forward(self, x):
        B, C, *spatial_shape = x.shape
        N = math.prod(spatial_shape)  
        q, k, v = (
            self.qkv(x)
              .view(B, self.num_heads, -1, self.dim_head)
              .reshape(B, self.num_heads, -1, 3, self.dim_head)
              .unbind(3)
        )
        x = torch.nn.functional.scaled_dot_product_attention(
            q.transpose(-1, -2),
            k.transpose(-1, -2),
            v.transpose(-1, -2),
            attn_mask=None,
            dropout_p=self.attn_drop.p if self.training else 0.0,
            enable_gqa=True,
        )
        x = (
            x.transpose(-1, -2)
            .reshape(B, -1, *spatial_shape)
        )
        x = self.proj(x)
        x = self.proj_drop(x)
        return x

class VitBlockND(torch.nn.Module):
    def __init__(self, dim, in_channels, norm_layer, act_layer, quant_layer, head_dim, expand_ratio, drop_path):
        super().__init__()
        self.context_module = Residual(AttentionND(
            dim, in_channels, in_channels, dim_head=head_dim,
            norm_layer=norm_layer, quant_layer=quant_layer
        ), d=drop_path)
        self.local_module = Residual(MBConvND(
            dim, in_channels, expand_ratio=expand_ratio,
            norm_layer=norm_layer, act_layer=act_layer, quant_layer=quant_layer
        ), d=drop_path)
    def forward(self, x):
        x = self.context_module(x)
        x = self.local_module(x)
        return x