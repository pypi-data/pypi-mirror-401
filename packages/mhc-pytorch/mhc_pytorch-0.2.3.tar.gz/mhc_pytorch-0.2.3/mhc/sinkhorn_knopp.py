"""
Implementation  of Sinkhorn-Knopp algorithm.
"""

import torch


def apply_sinkhorn_knopp(logits: torch.Tensor, iters: int = 20) -> torch.Tensor:
    """Normalizes a projection matrix into a doubly stochastic matrix.

    This implementation uses the Sinkhorn-Knopp algorithm to iteratively
    normalize rows and columns.

    Args:
        logits: The input tensor of for raw logits.
        iters: The number of normalization iterations to perform. Defaults to 20.

    Returns:
        A torch.Tensor of the same shape as logits normalized into a doubly stochastic
        matrix where rows and columns sum to 1.
    """
    # Using exponment to make all raw logits into non-negatives (sec 4.2)
    probs = torch.exp(logits)

    # Row and column normalization
    for _ in range(iters):
        probs = probs / probs.sum(dim=-1, keepdim=True)
        probs = probs / probs.sum(dim=-2, keepdim=True)

    return probs
