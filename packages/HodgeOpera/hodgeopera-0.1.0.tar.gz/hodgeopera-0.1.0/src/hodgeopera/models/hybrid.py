import torch
import torch.nn as nn
import torch.nn.functional as F

from hodgeopera.layers.spectral import SpectralAmp, PhysicsEncoder, SpectralMLP
from hodgeopera.layers.spatial import FNO3d, CouplingMLP, DataManager
from hodgeopera.layers.physics import SpectralDerivative


class SpectralCore(nn.Module):
    def __init__(self, context, hidden_dims=(64, 64)):
        super().__init__()
        
        self.k0 = context.k0
        self.k1 = context.k1
        self.k2 = context.k2
        
        self.amp_c0 = SpectralAmp(self.k0, power=1.0)
        self.amp_c1 = SpectralAmp(self.k1, power=1.0)
        self.amp_c2 = SpectralAmp(self.k2, power=1.0)
        
        self.physics_encoder = PhysicsEncoder(context.Md0_t, context.Md1_t)
        
        self.register_buffer("Md0", context.Md0_t.clone())
        self.register_buffer("Mdelta1", context.Mdelta1_t.clone())
        self.register_buffer("Md1", context.Md1_t.clone())
        self.register_buffer("Mdelta2", context.Mdelta2_t.clone())
        
        in_dim = (2 * self.k0) + (3 * self.k1) + (2 * self.k2)
        
        self.mlp_c0 = SpectralMLP(in_dim, hidden_dims, self.k0)
        self.mlp_c1 = SpectralMLP(in_dim, hidden_dims, self.k1)
        self.mlp_c2 = SpectralMLP(in_dim, hidden_dims, self.k2)
    
    def forward(self, c0, c1, c2):
        c0_amp = self.amp_c0(c0)
        c1_amp = self.amp_c1(c1)
        c2_amp = self.amp_c2(c2)
        
        feat_c0, feat_c1, feat_c2 = self.physics_encoder(c0_amp, c1_amp, c2_amp)
        feat = torch.cat([feat_c0, feat_c1, feat_c2], dim=-1)
        
        out_c0 = self.mlp_c0(feat)
        out_c1 = self.mlp_c1(feat)
        out_c2 = self.mlp_c2(feat)
        
        return out_c0, out_c1, out_c2


class HodgeOperator(nn.Module):
    def __init__(
        self,
        context,
        in_form=0,
        out_form=0,
        hidden_dim=64,
        n_layers=3,
        use_residual=True,
        fno_modes=(4, 4, 4),
        fno_hidden=16,
        fno_layers=2,
        grid_res=16
    ):
        super().__init__()
        
        self.context = context
        self.in_form = in_form
        self.out_form = out_form
        self.use_residual = use_residual
        
        self.k0 = context.k0
        self.k1 = context.k1
        self.k2 = context.k2
        
        hidden_dims = tuple([hidden_dim] * n_layers)
        self.spectral_core = SpectralCore(context, hidden_dims)
        
        self.register_buffer("Phi0", context.Phi0_t.clone())
        self.register_buffer("Phi1", context.Phi1_t.clone())
        self.register_buffer("Phi2", context.Phi2_t.clone())
        
        self.spectral_derivative = SpectralDerivative(context)
        
        if use_residual:
            self._setup_residual_branch(context, fno_modes, fno_hidden, fno_layers, grid_res)
        
        self.res_scale = nn.Parameter(torch.tensor(0.1))
    
    def _setup_residual_branch(self, context, fno_modes, fno_hidden, fno_layers, grid_res):
        out_dim = self._get_spatial_dim()
        
        self.fno = FNO3d(
            in_channels=2,
            out_channels=out_dim,
            hidden_channels=fno_hidden,
            n_modes=fno_modes,
            n_layers=fno_layers
        )
        
        k_enhanced = (2 * self.k0) + (3 * self.k1) + (2 * self.k2)
        
        self.coupling_mlp = CouplingMLP(
            k_total=k_enhanced,
            n_nodes=context.n_nodes,
            hidden_dim=64,
            out_dim=out_dim
        )
        
        self.data_manager = DataManager(
            context.n_nodes,
            context.points,
            context.device,
            grid_res=grid_res
        )
    
    def _get_spatial_dim(self):
        if self.out_form == 0:
            return 1
        elif self.out_form == 1:
            return self.context.n_edges
        elif self.out_form == 2:
            return self.context.n_faces
        return 1
    
    def _get_output_phi(self):
        if self.out_form == 0:
            return self.Phi0
        elif self.out_form == 1:
            return self.Phi1
        elif self.out_form == 2:
            return self.Phi2
    
    def _get_output_coeffs(self, c0, c1, c2):
        if self.out_form == 0:
            return c0
        elif self.out_form == 1:
            return c1
        elif self.out_form == 2:
            return c2
    
    def forward(self, x):
        if x.dim() == 2:
            x_spatial = x
        else:
            x_spatial = x.squeeze(-1) if x.shape[-1] == 1 else x
        
        c0, c1, c2 = self.context.lift(x_spatial, self.in_form)
        
        out_c0, out_c1, out_c2 = self.spectral_core(c0, c1, c2)
        
        out_coeffs = self._get_output_coeffs(out_c0, out_c1, out_c2)
        Phi = self._get_output_phi()
        
        y_spectral = torch.matmul(out_coeffs, Phi.t())
        
        if not self.use_residual:
            return y_spectral
        
        feat_c0, feat_c1, feat_c2 = self.spectral_derivative(c0, c1, c2)
        c_enhanced = torch.cat([feat_c0, feat_c1, feat_c2], dim=-1)
        
        fno_in = self.data_manager.prepare_fno_input(x_spatial)
        fno_out = self.fno(fno_in)
        y_fno = self.data_manager.decode_fno_output(fno_out)
        
        if self.out_form == 0:
            y_fno = y_fno.squeeze(-1)
        
        y_mlp = self.coupling_mlp(x_spatial, c_enhanced)
        if self.out_form == 0:
            y_mlp = y_mlp.squeeze(-1)
        
        y_residual = y_fno + y_mlp
        
        proj_coeffs = torch.matmul(y_residual, Phi)
        y_base = torch.matmul(proj_coeffs, Phi.t())
        y_orthogonal = y_residual - y_base
        
        y_total = y_spectral + self.res_scale * y_orthogonal
        
        return y_total
    
    def forward_with_components(self, x):
        if x.dim() == 2:
            x_spatial = x
        else:
            x_spatial = x.squeeze(-1) if x.shape[-1] == 1 else x
        
        c0, c1, c2 = self.context.lift(x_spatial, self.in_form)
        out_c0, out_c1, out_c2 = self.spectral_core(c0, c1, c2)
        out_coeffs = self._get_output_coeffs(out_c0, out_c1, out_c2)
        Phi = self._get_output_phi()
        y_spectral = torch.matmul(out_coeffs, Phi.t())
        
        if not self.use_residual:
            return y_spectral, y_spectral, torch.zeros_like(y_spectral)
        
        feat_c0, feat_c1, feat_c2 = self.spectral_derivative(c0, c1, c2)
        c_enhanced = torch.cat([feat_c0, feat_c1, feat_c2], dim=-1)
        
        fno_in = self.data_manager.prepare_fno_input(x_spatial)
        fno_out = self.fno(fno_in)
        y_fno = self.data_manager.decode_fno_output(fno_out)
        
        if self.out_form == 0:
            y_fno = y_fno.squeeze(-1)
        
        y_mlp = self.coupling_mlp(x_spatial, c_enhanced)
        if self.out_form == 0:
            y_mlp = y_mlp.squeeze(-1)
        
        y_residual = y_fno + y_mlp
        
        proj_coeffs = torch.matmul(y_residual, Phi)
        y_base = torch.matmul(proj_coeffs, Phi.t())
        y_orthogonal = y_residual - y_base
        
        y_total = y_spectral + self.res_scale * y_orthogonal
        
        return y_total, y_spectral, y_orthogonal