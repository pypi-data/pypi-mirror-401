import torch
import torch.nn as nn
import torch.nn.functional as F


class SpectralConv3d(nn.Module):
    def __init__(self, in_channels, out_channels, modes1, modes2, modes3):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.modes1 = modes1
        self.modes2 = modes2
        self.modes3 = modes3
        
        scale = 1 / (in_channels * out_channels)
        self.weights1 = nn.Parameter(scale * torch.rand(in_channels, out_channels, modes1, modes2, modes3, dtype=torch.cfloat))
        self.weights2 = nn.Parameter(scale * torch.rand(in_channels, out_channels, modes1, modes2, modes3, dtype=torch.cfloat))
        self.weights3 = nn.Parameter(scale * torch.rand(in_channels, out_channels, modes1, modes2, modes3, dtype=torch.cfloat))
        self.weights4 = nn.Parameter(scale * torch.rand(in_channels, out_channels, modes1, modes2, modes3, dtype=torch.cfloat))

    def compl_mul3d(self, input, weights):
        return torch.einsum("bixyz,ioxyz->boxyz", input, weights)

    def forward(self, x):
        batchsize = x.shape[0]
        x_ft = torch.fft.rfftn(x, dim=[-3, -2, -1])
        
        out_ft = torch.zeros(batchsize, self.out_channels, x.size(-3), x.size(-2), x.size(-1)//2 + 1, dtype=torch.cfloat, device=x.device)
        
        out_ft[:, :, :self.modes1, :self.modes2, :self.modes3] = self.compl_mul3d(x_ft[:, :, :self.modes1, :self.modes2, :self.modes3], self.weights1)
        out_ft[:, :, -self.modes1:, :self.modes2, :self.modes3] = self.compl_mul3d(x_ft[:, :, -self.modes1:, :self.modes2, :self.modes3], self.weights2)
        out_ft[:, :, :self.modes1, -self.modes2:, :self.modes3] = self.compl_mul3d(x_ft[:, :, :self.modes1, -self.modes2:, :self.modes3], self.weights3)
        out_ft[:, :, -self.modes1:, -self.modes2:, :self.modes3] = self.compl_mul3d(x_ft[:, :, -self.modes1:, -self.modes2:, :self.modes3], self.weights4)
        
        return torch.fft.irfftn(out_ft, s=(x.size(-3), x.size(-2), x.size(-1)))


class FNO3d(nn.Module):
    def __init__(self, in_channels, out_channels, hidden_channels=16, n_modes=(4, 4, 4), n_layers=3):
        super().__init__()
        self.hidden_channels = hidden_channels
        self.n_layers = n_layers
        
        self.lifting = nn.Conv3d(in_channels, hidden_channels, 1)
        
        self.spectral_layers = nn.ModuleList([
            SpectralConv3d(hidden_channels, hidden_channels, *n_modes)
            for _ in range(n_layers)
        ])
        
        self.local_layers = nn.ModuleList([
            nn.Conv3d(hidden_channels, hidden_channels, 1)
            for _ in range(n_layers)
        ])
        
        self.norms = nn.ModuleList([
            nn.BatchNorm3d(hidden_channels)
            for _ in range(n_layers)
        ])
        
        self.projection = nn.Sequential(
            nn.Conv3d(hidden_channels, hidden_channels, 1),
            nn.GELU(),
            nn.Conv3d(hidden_channels, out_channels, 1)
        )

    def forward(self, x):
        h = self.lifting(x)
        
        for i, (spectral, local, norm) in enumerate(zip(self.spectral_layers, self.local_layers, self.norms)):
            h1 = spectral(h)
            h2 = local(h)
            h = norm(h1 + h2)
            if i < self.n_layers - 1:
                h = F.gelu(h)
        
        return self.projection(h)


class CouplingMLP(nn.Module):
    def __init__(self, k_total, n_nodes, hidden_dim=64, out_dim=1):
        super().__init__()
        self.n_nodes = n_nodes
        self.out_dim = out_dim
        
        self.global_proj = nn.Linear(k_total, hidden_dim // 2)
        self.local_proj = nn.Linear(1, hidden_dim // 2)
        
        self.body = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, out_dim)
        )
        
        nn.init.zeros_(self.body[-1].weight)
        nn.init.zeros_(self.body[-1].bias)

    def forward(self, x_spatial, c_enhanced):
        if x_spatial.dim() == 2:
            x_spatial = x_spatial.unsqueeze(-1)
        
        B, N, _ = x_spatial.shape
        
        local_feat = self.local_proj(x_spatial)
        global_feat = self.global_proj(c_enhanced)
        global_feat = global_feat.unsqueeze(1).expand(-1, N, -1)
        
        in_feat = torch.cat([local_feat, global_feat], dim=-1)
        return self.body(in_feat)


class DataManager:
    def __init__(self, n_nodes, points, device, grid_res=16):
        self.n_nodes = n_nodes
        self.pts = torch.from_numpy(points).float().to(device)
        self.device = device
        self.grid_res = grid_res
        
        self.pts_min = self.pts.min(dim=0)[0]
        self.pts_max = self.pts.max(dim=0)[0]
        self.pts_norm = (self.pts - self.pts_min) / (self.pts_max - self.pts_min + 1e-6)
        self.grid_sample_coords = (self.pts_norm * 2.0 - 1.0).view(1, 1, 1, n_nodes, 3)
    
    def prepare_fno_input(self, x_batch, out_channels=1):
        B = x_batch.shape[0]
        Res = self.grid_res
        
        n_in = 1 if x_batch.dim() == 2 else x_batch.shape[-1]
        grid_x = torch.zeros(B, n_in + 1, Res, Res, Res, device=self.device)
        
        indices = (self.pts_norm * (Res - 1)).long().clamp(0, Res - 1)
        idx_x, idx_y, idx_z = indices[:, 0], indices[:, 1], indices[:, 2]
        
        for b in range(B):
            if x_batch.dim() == 2:
                grid_x[b, 0, idx_x, idx_y, idx_z] = x_batch[b]
            else:
                for c in range(n_in):
                    grid_x[b, c, idx_x, idx_y, idx_z] = x_batch[b, :, c]
            grid_x[b, -1, idx_x, idx_y, idx_z] = 1.0
        
        return grid_x
    
    def decode_fno_output(self, grid_out):
        B = grid_out.shape[0]
        sample_coords = self.grid_sample_coords.expand(B, -1, -1, -1, -1)
        
        sampled = F.grid_sample(
            grid_out, sample_coords,
            mode='bilinear', padding_mode='zeros', align_corners=True
        )
        
        out_mesh = sampled.view(B, grid_out.shape[1], -1).permute(0, 2, 1)
        return out_mesh