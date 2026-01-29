import numpy as np
from scipy.sparse.linalg import eigsh
import toponetx as tnx
import torch


class HodgeContext:
    def __init__(self, points, faces, k_modes=64):
        self.points = np.asarray(points, dtype=np.float32)
        self.faces = np.asarray(faces, dtype=np.int32)
        self.n_nodes = len(self.points)
        self.k_modes = k_modes
        self.device = torch.device('cpu')
        
        self._build_complex()
        self._build_boundary_matrices()
        self._build_laplacians()
        self._compute_eigenbases()
        self._build_spectral_operators()
        self._convert_to_torch()
        
    def _build_complex(self):
        self.sc = tnx.SimplicialComplex(self.faces.tolist())
        for i in range(self.n_nodes):
            if i not in self.sc.nodes:
                self.sc.add_node(i)
    
    def _build_boundary_matrices(self):
        _B1 = self.sc.incidence_matrix(rank=1, signed=True)
        _B2 = self.sc.incidence_matrix(rank=2, signed=True)
        
        if _B1.shape[1] != self.n_nodes:
            self.B1 = _B1.T
        else:
            self.B1 = _B1
            
        n_edges = self.B1.shape[0]
        if _B2.shape[1] != n_edges:
            self.B2 = _B2.T
        else:
            self.B2 = _B2
            
        self.n_edges = self.B1.shape[0]
        self.n_faces = self.B2.shape[0]
    
    def _build_laplacians(self):
        self.L0 = self.sc.hodge_laplacian_matrix(rank=0, signed=True)
        self.L1 = self.sc.hodge_laplacian_matrix(rank=1, signed=True)
        self.L2 = self.sc.hodge_laplacian_matrix(rank=2, signed=True)
    
    def _compute_eigenbasis(self, L, k):
        n = L.shape[0]
        if n == 0 or k <= 0:
            return np.zeros((n, 0), dtype=np.float32)
        k = min(k, n)
        L_float = L.astype(float)
        
        if n < 500:
            vals, vecs = np.linalg.eigh(L_float.toarray())
            return vecs[:, :k].astype(np.float32)
        
        try:
            vals, vecs = eigsh(L_float, k=k, sigma=-0.01, which='LM', tol=1e-3)
            return vecs.astype(np.float32)
        except:
            try:
                vals, vecs = eigsh(L_float, k=k, which='SA', tol=1e-3)
                return vecs.astype(np.float32)
            except:
                vals, vecs = np.linalg.eigh(L_float.toarray())
                return vecs[:, :k].astype(np.float32)
    
    def _compute_eigenbases(self):
        self.Phi0 = self._compute_eigenbasis(self.L0, self.k_modes)
        self.Phi1 = self._compute_eigenbasis(self.L1, self.k_modes)
        self.Phi2 = self._compute_eigenbasis(self.L2, self.k_modes)
        
        self.k0 = self.Phi0.shape[1]
        self.k1 = self.Phi1.shape[1]
        self.k2 = self.Phi2.shape[1]
    
    def _build_spectral_operators(self):
        if self.k0 == 0 or self.k1 == 0:
            self.Md0 = np.zeros((self.k1, self.k0), dtype=np.float32)
        else:
            B1 = self.B1.tocsr().astype(float)
            B1_Phi0 = B1.dot(self.Phi0)
            self.Md0 = (self.Phi1.T @ B1_Phi0).astype(np.float32)
        
        self.Mdelta1 = self.Md0.T
        
        if self.k1 == 0 or self.k2 == 0:
            self.Md1 = np.zeros((self.k2, self.k1), dtype=np.float32)
        else:
            B2 = self.B2.tocsr().astype(float)
            B2_Phi1 = B2.dot(self.Phi1)
            self.Md1 = (self.Phi2.T @ B2_Phi1).astype(np.float32)
        
        self.Mdelta2 = self.Md1.T
    
    def _convert_to_torch(self):
        self.Phi0_t = torch.from_numpy(self.Phi0)
        self.Phi1_t = torch.from_numpy(self.Phi1)
        self.Phi2_t = torch.from_numpy(self.Phi2)
        self.Md0_t = torch.from_numpy(self.Md0)
        self.Md1_t = torch.from_numpy(self.Md1)
        self.Mdelta1_t = torch.from_numpy(self.Mdelta1)
        self.Mdelta2_t = torch.from_numpy(self.Mdelta2)
        self.points_t = torch.from_numpy(self.points)
        
        B1_coo = self.B1.tocoo()
        self.B1_indices = torch.from_numpy(np.vstack((B1_coo.row, B1_coo.col))).long()
        self.B1_values = torch.from_numpy(B1_coo.data).float()
        self.B1_shape = self.B1.shape
    
    def to(self, device):
        self.device = torch.device(device)
        self.Phi0_t = self.Phi0_t.to(self.device)
        self.Phi1_t = self.Phi1_t.to(self.device)
        self.Phi2_t = self.Phi2_t.to(self.device)
        self.Md0_t = self.Md0_t.to(self.device)
        self.Md1_t = self.Md1_t.to(self.device)
        self.Mdelta1_t = self.Mdelta1_t.to(self.device)
        self.Mdelta2_t = self.Mdelta2_t.to(self.device)
        self.points_t = self.points_t.to(self.device)
        self.B1_indices = self.B1_indices.to(self.device)
        self.B1_values = self.B1_values.to(self.device)
        return self
    
    def lift_0form(self, u):
        if u.dim() == 1:
            u = u.unsqueeze(0)
        c0 = torch.matmul(u, self.Phi0_t)
        g = torch.sparse_coo_tensor(
            self.B1_indices, self.B1_values, self.B1_shape, device=self.device
        )
        g_spatial = torch.sparse.mm(g, u.t()).t()
        c1 = torch.matmul(g_spatial, self.Phi1_t)
        c2 = torch.zeros(u.shape[0], self.k2, device=self.device)
        return c0, c1, c2
    
    def lift_1form(self, flux):
        if flux.dim() == 1:
            flux = flux.unsqueeze(0)
        c1 = torch.matmul(flux, self.Phi1_t)
        c0 = torch.matmul(c1, self.Mdelta1_t.t())
        c2 = torch.matmul(c1, self.Md1_t.t())
        return c0, c1, c2
    
    def lift_2form(self, h):
        if h.dim() == 1:
            h = h.unsqueeze(0)
        c2 = torch.matmul(h, self.Phi2_t)
        c1 = torch.matmul(c2, self.Mdelta2_t.t())
        c0 = torch.zeros(h.shape[0], self.k0, device=self.device)
        return c0, c1, c2
    
    def lift(self, data, form):
        if form == 0:
            return self.lift_0form(data)
        elif form == 1:
            return self.lift_1form(data)
        elif form == 2:
            return self.lift_2form(data)
        else:
            raise ValueError(f"Invalid form: {form}")
    
    def reconstruct_0form(self, c0):
        return torch.matmul(c0, self.Phi0_t.t())
    
    def reconstruct_1form(self, c1):
        return torch.matmul(c1, self.Phi1_t.t())
    
    def reconstruct_2form(self, c2):
        return torch.matmul(c2, self.Phi2_t.t())
    
    def reconstruct(self, coeffs, form):
        if form == 0:
            return self.reconstruct_0form(coeffs)
        elif form == 1:
            return self.reconstruct_1form(coeffs)
        elif form == 2:
            return self.reconstruct_2form(coeffs)
        else:
            raise ValueError(f"Invalid form: {form}")
    
    def project_to_spectral(self, data, form):
        if form == 0:
            return torch.matmul(data, self.Phi0_t)
        elif form == 1:
            return torch.matmul(data, self.Phi1_t)
        elif form == 2:
            return torch.matmul(data, self.Phi2_t)
        else:
            raise ValueError(f"Invalid form: {form}")