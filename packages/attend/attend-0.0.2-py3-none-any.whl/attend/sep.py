import torch

def ConvND(dim, *args, **kwargs):
    conv_cls = [torch.nn.Conv1d, torch.nn.Conv2d, torch.nn.Conv3d][dim - 1]
    return conv_cls(*args, **kwargs)

class SpatiotemporallySeparableConvND(torch.nn.Module):
    def __init__(self, dim, ch, kernel_size, groups=1, bias=True):
        super().__init__()
        if isinstance(ch, int):
            channel_list = [ch]
            current = ch
            for _ in range(dim):
                current *= kernel_size
                channel_list.append(current)
        else:
            channel_list = list(ch)
        
        convs = []
        current_channels = channel_list[0]
        
        for axis in range(dim):
            ks_tuple = tuple(kernel_size if i == axis else 1 for i in range(dim))
            
            groups_this = groups if axis == 0 else current_channels
            next_channels = channel_list[axis + 1]
            
            conv = ConvND(
                dim,
                in_channels=current_channels,
                out_channels=next_channels,
                kernel_size=ks_tuple,
                stride=ks_tuple,
                groups=groups_this,
                bias=bias,
                padding=0,
            )
            convs.append(conv)
            current_channels = next_channels
        
        self.seq = torch.nn.Sequential(*convs)
    
    def forward(self, x):
        return self.seq(x)