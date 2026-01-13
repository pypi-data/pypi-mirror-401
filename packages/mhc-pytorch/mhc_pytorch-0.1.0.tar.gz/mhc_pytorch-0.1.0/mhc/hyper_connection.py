"""
Module for implementing Manifold-Constrained Hyper-Connections (mHC).

This module provides the ManifoldHyperConnections class, which implements
a multi-stream residual connection mechanism. The mixing of streams is
dynamically determined by the input and constrained to mathematical
manifolds, such as Sigmoid for scalars and Sinkhorn for matrices.
"""

import torch
import torch.nn.functional as F
from torch import nn

from mhc.sinkhorn_knopp import apply_sinkhorn_knopp


class ManifoldHyperConnections(nn.Module):
    """Manifold-Constrained Hyper-Connections (mHC).

    This module implements a multi-stream residual connection where the mixing
    of streams is dynamically determined by the input state and constrained to
    mathematical manifolds (Sigmoid for scalars, Sinkhorn for matrices).

    References:
        - mHC: Manifold-Constrained Hyper-Connections Paper: https://arxiv.org/pdf/2512.24880
        - Hyper-Connections Paper: https://arxiv.org/pdf/2409.19606

    Args:
        dim (int): The hidden dim of the model.
        num_streams (int): Number of parallel residual streams.
        block (nn.Module): The transformation function F (ex: Attention, MLP, etc).
    """

    def __init__(self, dim: int, num_streams: int, block: nn.Module):
        super().__init__()
        self.num_streams = num_streams
        self.block = block
        self.dim = dim

        # x_l is flattened, so the input dim is num_streams * dim
        input_vec_dim = num_streams * dim

        # Linear projections for dynamic mappings (phi)
        self.phi_pre = nn.Linear(input_vec_dim, self.num_streams)
        self.phi_post = nn.Linear(input_vec_dim, self.num_streams)
        self.phi_res = nn.Linear(input_vec_dim, self.num_streams * self.num_streams)

        # Scalars (alpha)
        self.alpha_pre = nn.Parameter(torch.ones(1))
        self.alpha_post = nn.Parameter(torch.ones(1))
        self.alpha_res = nn.Parameter(torch.ones(1))

        # Biases (b)
        self.b_pre = nn.Parameter(torch.zeros(self.num_streams))
        self.b_post = nn.Parameter(torch.zeros(self.num_streams))
        self.b_res = nn.Parameter(torch.zeros(self.num_streams, self.num_streams))

        self.norm = nn.RMSNorm(dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass of the mHC module.

        Args:
            x (torch.Tensor): Input tensor.

        Returns:
            torch.Tensor: Output tensor.
        """
        bs, seq_len, dim = x.shape

        assert dim == self.dim, "Hidden dim of input does not match model dim."

        # Expand the stream and then flatten it.
        x_l = x.unsqueeze(dim=2).expand(bs, seq_len, self.num_streams, dim)  # [bs, seq_len, num_streams, dim]
        x_vec = x_l.reshape(bs, seq_len, self.num_streams * dim)  # [bs, seq_len, num_streams * dim]

        # RMSNorm the vectorized input (x_vec)
        x_vec_norm = F.rms_norm(x_vec, (self.num_streams * dim,))  # [bs, seq_len, num_streams * dim]

        # Calculate unconstrained mappings
        h_pre_tilde = self.alpha_pre * self.phi_pre(x_vec_norm) + self.b_pre  # [bs, seq_len, num_streams]
        h_post_tilde = self.alpha_post * self.phi_post(x_vec_norm) + self.b_post  # [bs, seq_len, num_streams]
        h_res_tilde = (
            self.alpha_res * self.phi_res(x_vec_norm).view(bs, seq_len, self.num_streams, self.num_streams) + self.b_res
        )  # [bs, seq_len, num_streams, num_streams]

        # Constrained mappings
        h_pre = torch.sigmoid(h_pre_tilde)  # [bs, seq_len, num_streams]
        h_post = 2 * torch.sigmoid(h_post_tilde)  # [bs, seq_len, num_streams]
        h_res = apply_sinkhorn_knopp(h_res_tilde)  # [bs, seq_len, num_streams, num_streams]

        # Weighted sum of normalized streams (width connection)
        block_input = torch.sum(x_l * h_pre.unsqueeze(-1), dim=2)  # [bs, seq_len, dim]

        # Block execution
        block_out = self.block(block_input)  # [bs, seq_len, dim]

        # Scale transformation output and broadcast to streams
        post_block_out = h_post.unsqueeze(-1) * block_out.unsqueeze(2)  # [bs, seq_len, num_streams, dim]

        # Depth connection (mixing streams)
        mixed_streams = torch.matmul(h_res, x_l)  # [bs, seq_len, num_streams, dim]

        # Final output
        out_streams = mixed_streams + post_block_out  # [bs, seq_len, num_streams, dim]

        # Collapse streams
        out = out_streams.sum(dim=2)  # [bs, seq_len, dim]
        return out
