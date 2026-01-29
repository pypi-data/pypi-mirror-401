import torch
import torch.nn as nn


class SpectralDerivative(nn.Module):
    def __init__(self, context):
        super().__init__()
        self.register_buffer("Md0", context.Md0_t.clone())
        self.register_buffer("Mdelta1", context.Mdelta1_t.clone())
        self.register_buffer("Md1", context.Md1_t.clone())
        self.register_buffer("Mdelta2", context.Mdelta2_t.clone())
        
        self.k0 = context.k0
        self.k1 = context.k1
        self.k2 = context.k2
    
    def gradient(self, c0):
        return torch.matmul(c0, self.Md0.t())
    
    def divergence(self, c1):
        return torch.matmul(c1, self.Mdelta1.t())
    
    def curl(self, c1):
        return torch.matmul(c1, self.Md1.t())
    
    def codifferential(self, c2):
        return torch.matmul(c2, self.Mdelta2.t())
    
    def compute_enhanced_features(self, c0, c1, c2):
        d0_c0 = self.gradient(c0)
        delta1_c1 = self.divergence(c1)
        d1_c1 = self.curl(c1)
        delta2_c2 = self.codifferential(c2)
        
        feat_c0 = torch.cat([c0, delta1_c1], dim=-1)
        feat_c1 = torch.cat([c1, d0_c0, delta2_c2], dim=-1)
        feat_c2 = torch.cat([c2, d1_c1], dim=-1)
        
        return feat_c0, feat_c1, feat_c2
    
    def forward(self, c0, c1, c2):
        return self.compute_enhanced_features(c0, c1, c2)


class FluxMapper(nn.Module):
    def __init__(self, context):
        super().__init__()
        
        B1_abs_coo = abs(context.B1).tocoo()
        indices = torch.from_numpy(np.stack([B1_abs_coo.row, B1_abs_coo.col])).long()
        values = torch.from_numpy(B1_abs_coo.data).float()
        
        self.register_buffer('abs_B1_indices', indices)
        self.register_buffer('abs_B1_values', values)
        self.abs_B1_shape = context.B1.shape
        
        pts_tensor = context.points_t
        B1_signed = context.B1.tocoo()
        ind_s = torch.from_numpy(np.stack([B1_signed.row, B1_signed.col])).long()
        val_s = torch.from_numpy(B1_signed.data).float()
        B1_sparse = torch.sparse_coo_tensor(ind_s, val_s, context.B1.shape)
        
        edge_vectors = torch.sparse.mm(B1_sparse, pts_tensor)
        self.register_buffer('edge_vectors', edge_vectors)
        
        self.n_edges = self.abs_B1_shape[0]
        self.n_nodes = self.abs_B1_shape[1]

    def forward(self, node_vectors):
        B, N, D = node_vectors.shape
        device = node_vectors.device
        
        x_flat = node_vectors.permute(1, 0, 2).reshape(N, -1)
        
        abs_B1 = torch.sparse_coo_tensor(
            self.abs_B1_indices, self.abs_B1_values, self.abs_B1_shape, device=device
        )
        
        u_sum = torch.sparse.mm(abs_B1, x_flat)
        u_mid = u_sum.reshape(self.n_edges, B, D).permute(1, 0, 2) / 2.0
        
        flux = torch.sum(u_mid * self.edge_vectors.unsqueeze(0), dim=-1)
        return flux


import numpy as np