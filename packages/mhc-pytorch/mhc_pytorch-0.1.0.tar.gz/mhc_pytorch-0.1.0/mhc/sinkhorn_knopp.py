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
        A torch.Tensor of the same shape as logits, where rows and
        columns approximately sum to 1/N and 1/M respectively (or 1
        depending on the specific normalization target).
    """
    # Using exponment to make all raw logits into non-negatives (sec 4.2)
    probs = torch.exp(logits)

    for _ in range(iters):
        probs = probs / probs.sum(dim=-1, keepdim=True)  # Row normalization
        probs = probs / probs.sum(dim=-2, keepdim=True)  # Column normalization

    return probs
