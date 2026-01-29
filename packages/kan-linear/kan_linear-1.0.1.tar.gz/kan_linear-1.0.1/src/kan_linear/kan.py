import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class KANLinear(nn.Module):
    def __init__(self, in_features, out_features, grid_size=5, spline_order=3, scale_noise=0.1, scale_base=1.0, scale_spline=1.0, base_activation=torch.nn.SiLU, grid_eps=0.02, grid_range=[-1, 1], bias=True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.grid_size = grid_size
        self.spline_order = spline_order

        h = (grid_range[1] - grid_range[0]) / grid_size
        grid = ((torch.arange(-spline_order, grid_size + spline_order + 1) * h + grid_range[0]).expand(in_features, -1).contiguous())
        self.register_buffer("grid", grid)

        self.base_weight = nn.Parameter(torch.Tensor(out_features, in_features))
        self.weight = self.base_weight
        self.spline_weight = nn.Parameter(torch.Tensor(out_features, in_features, grid_size + spline_order))
        
        if bias:
            self.bias = nn.Parameter(torch.Tensor(out_features))
        else:
            self.register_parameter('bias', None)
            
        self.scale_noise = scale_noise
        self.scale_base = scale_base
        self.scale_spline = scale_spline
        self.base_activation = base_activation()
        self.grid_eps = grid_eps

        self.reset_parameters()

    def reset_parameters(self):
        nn.init.kaiming_uniform_(self.base_weight, a=math.sqrt(5) * self.scale_base)
        if self.bias is not None:
            fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.base_weight)
            bound = 1 / math.sqrt(fan_in) if fan_in > 0 else 0
            nn.init.uniform_(self.bias, -bound, bound)
            
        with torch.no_grad():
            noise = (torch.rand(self.grid_size + self.spline_order, self.in_features, self.out_features) - 1 / 2) * self.scale_noise / self.grid_size
            self.spline_weight.data.copy_((self.scale_spline * noise).permute(2, 1, 0))

    def b_splines(self, x):
        assert x.dim() == 2 and x.size(1) == self.in_features

        grid = self.grid
        x = x.unsqueeze(-1)
        bases = ((x >= grid[:, :-1]) & (x < grid[:, 1:])).to(x.dtype)
        for k in range(1, self.spline_order + 1):
            t_k = grid[:, k:-1]
            t_0 = grid[:, :-(k+1)]
            term1 = (x - t_0) / (t_k - t_0)
            
            t_k1 = grid[:, k+1:]
            t_1 = grid[:, 1:-k]
            term2 = (t_k1 - x) / (t_k1 - t_1)
            
            bases = term1 * bases[:, :, :-1] + term2 * bases[:, :, 1:]
            
        return bases

    def forward(self, x):
        original_shape = x.shape
        x = x.reshape(-1, self.in_features)
        
        base_output = F.linear(self.base_activation(x), self.base_weight)
        
        spline_basis = self.b_splines(x)
        spline_output = F.linear(spline_basis.reshape(x.size(0), -1), self.spline_weight.view(self.out_features, -1))
        
        output = base_output + spline_output
        if self.bias is not None:
            output = output + self.bias
        return output.reshape(*original_shape[:-1], self.out_features)