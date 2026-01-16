import torch

def ConvND(dim, *args, **kwargs):
    conv_cls = [torch.nn.Conv1d, torch.nn.Conv2d, torch.nn.Conv3d][dim-1]
    return conv_cls(*args, **kwargs)

def ConvTransposeND(dim, *args, **kwargs):
    conv_cls = [torch.nn.ConvTranspose1d, torch.nn.ConvTranspose2d, torch.nn.ConvTranspose3d][dim-1]
    return conv_cls(*args, **kwargs)

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
        return x

class NormCodecND(torch.nn.Module):
    def __init__(self, dim, ch):
        super().__init__()
        self.layers = torch.nn.Sequential(
            OrderedDict(
                [
                    ("analysis_transform", ConvND(dim=dim, in_channels=ch, out_channels=ch, kernel_size=2, stride=2, padding=0)),
                    ("sphere_norm", SphereNorm()),
                    ("quantize", Quantize()),
                    ("synthesis_transform", ConvTransposeND(dim=dim, in_channels=ch, out_channels=ch, kernel_size=2, stride=2, padding=0)),
                ]
            )
        )
    
    def forward(self, x):
        return self.layers(x)