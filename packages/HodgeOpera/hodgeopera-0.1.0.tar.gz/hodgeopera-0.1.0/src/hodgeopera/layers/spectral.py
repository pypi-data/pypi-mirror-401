import torch
import torch.nn as nn
import torch.nn.functional as F


class SpectralAmp(nn.Module):
    def __init__(self, n_modes, power=1.0):
        super().__init__()
        ramp = torch.arange(1, n_modes + 1).float().pow(power)
        self.gain = nn.Parameter(ramp)

    def forward(self, x):
        k = min(x.shape[-1], self.gain.shape[0])
        return x[..., :k] * self.gain[:k].unsqueeze(0)


class PhysicsEncoder(nn.Module):
    def __init__(self, Md0, Md1):
        super().__init__()
        self.register_buffer("Md0", Md0.clone())
        self.register_buffer("Mdelta1", Md0.t().clone())
        self.register_buffer("Md1", Md1.clone())
        self.register_buffer("Mdelta2", Md1.t().clone())

    def forward(self, c0, c1, c2):
        c0_from_c1 = torch.matmul(c1, self.Mdelta1.t())
        c1_from_c0 = torch.matmul(c0, self.Md0.t())
        c1_from_c2 = torch.matmul(c2, self.Mdelta2.t())
        c2_from_c1 = torch.matmul(c1, self.Md1.t())
        
        feat_c0 = torch.cat([c0, c0_from_c1], dim=-1)
        feat_c1 = torch.cat([c1, c1_from_c0, c1_from_c2], dim=-1)
        feat_c2 = torch.cat([c2, c2_from_c1], dim=-1)
        
        return feat_c0, feat_c1, feat_c2


class PhysicsGMLPLayer(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.norm = nn.LayerNorm(in_features)
        self.W1 = nn.Linear(in_features, out_features)
        self.W2 = nn.Linear(in_features, out_features)
        self.W_out = nn.Linear(out_features, out_features)

    def forward(self, x):
        x_norm = self.norm(x)
        content = self.W1(x_norm)
        gate = self.W2(x_norm)
        gate_act = F.silu(gate)
        mixed = content * gate_act
        out = self.W_out(mixed)
        
        if x.shape[-1] == out.shape[-1]:
            return x + out
        return out


class SpectralMLP(nn.Module):
    def __init__(self, in_dim, hidden_dims, out_dim):
        super().__init__()
        layers = []
        last_dim = in_dim
        
        for h in hidden_dims:
            layers.append(PhysicsGMLPLayer(last_dim, h))
            last_dim = h
        
        self.body = nn.Sequential(*layers)
        self.head = nn.Linear(last_dim, out_dim)
        nn.init.orthogonal_(self.head.weight, gain=0.1)
        nn.init.zeros_(self.head.bias)
    
    def forward(self, x):
        h = self.body(x)
        return self.head(h)