import torch


def lift_to_spectral(context, data, form):
    return context.lift(data, form)


def reconstruct_from_spectral(context, coeffs, form):
    return context.reconstruct(coeffs, form)


def compute_spectral_gradient(c0, Md0):
    return torch.matmul(c0, Md0.t())


def compute_spectral_divergence(c1, Mdelta1):
    return torch.matmul(c1, Mdelta1.t())


def compute_spectral_curl(c1, Md1):
    return torch.matmul(c1, Md1.t())


def compute_spectral_codifferential(c2, Mdelta2):
    return torch.matmul(c2, Mdelta2.t())


def orthogonal_projection(flux, Phi):
    proj_coeffs = torch.matmul(flux, Phi)
    flux_base = torch.matmul(proj_coeffs, Phi.t())
    return flux - flux_base