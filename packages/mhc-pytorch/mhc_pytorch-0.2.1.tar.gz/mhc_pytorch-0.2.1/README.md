# mHC: Manifold-Constrained Hyper-Connections

A PyTorch implementation of [*Manifold-Constrained Hyper-Connections (mHC)*](https://arxiv.org/pdf/2512.24880), an advanced multi-stream residual connection mechanism for deep learning models. This module dynamically determines stream mixing based on input while constraining the parameters to mathematical manifolds such as Sinkhorn.

<div align="center"><img src="https://raw.githubusercontent.com/KennyStryker/manifold-constrained-hyper-connections/refs/heads/main/assets/mhc.png" alt="MHC Architecture"/></div>

## 🔍 Features

- **Manifold-Constrained Mixing**: Ensures mixing parameters with mathematical manifolds
- **Multi-Stream Architecture**: Supports parallel residual streams for enhanced model capacity
- **PyTorch Native**: Seamless integration with existing PyTorch models and training pipelines

## 📦 Installation

Make sure you have Python 3.12+ and [Poetry](https://python-poetry.org/) installed.

### From the source
```bash
git clone https://github.com/KennyStryker/manifold-constrained-hyper-connections.git
cd manifold-constrained-hyper-connections
poetry install
```

## 🚀 Usage

```python
import torch
import torch.nn as nn
from mhc import ManifoldHyperConnections

# Define your base block
class MLPBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.block = nn.Sequential(
            nn.Linear(dim, 4 * dim),
            nn.GELU(),
            nn.Linear(4 * dim, dim)
        )

    def forward(self, x):
        return self.block(x)

# Create mHC module
dim = 512
num_streams = 4
block = MLPBlock(dim)

mhc_layer = ManifoldHyperConnections(dim=dim, num_streams=num_streams, block=block)

# Use in forward pass
x = torch.randn(32, 128, dim)  # [batch_size, seq_len, dim]
output = mhc_layer(x)  # [batch_size, seq_len, dim]
```

## Citations

```bibtex
@article{arXiv,
    title   = {mHC: Manifold-Constrained Hyper-Connections},
    author  = {Zhenda Xie, Yixuan Wei, Huanqi Cao, Chenggang Zhao, Chengqi Deng, Jiashi Li, Damai Dai, Huazuo Gao, Jiang Chang, Kuai Yu, Liang Zhao, Shangyan Zhou, Zhean Xu, Zhengyan Zhang, Wangding Zeng, Shengding Hu, Yuqing Wang, Jingyang Yuan, Lean Wang, Wenfeng Liang},
    url     = {https://www.arxiv.org/abs/2512.24880}
}

@article{arXiv,
    title   = {Hyper-Connections},
    author  = {Defa Zhu, Hongzhi Huang, Zihao Huang, Yutao Zeng, Yunyao Mao, Banggu Wu, Qiyang Min, Xun Zhou},
    url     = {https://arxiv.org/abs/2409.19606}
}
```
