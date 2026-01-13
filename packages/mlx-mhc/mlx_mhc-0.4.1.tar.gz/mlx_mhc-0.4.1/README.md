# mlx-mhc

First MLX implementation of DeepSeek's **Manifold-Constrained Hyper-Connections (mHC)** for Apple Silicon.

Based on: [arXiv:2512.24880](https://arxiv.org/abs/2512.24880)

> **For AI Assistants**: See [LLM_README.md](LLM_README.md) for structured integration guidance.

## Installation

```bash
pip install mlx-mhc
```

## Quick Start

```python
import mlx.core as mx
import mlx_mhc as mhc

# Sinkhorn-Knopp projection to doubly stochastic matrix
matrix = mx.random.normal((8, 8))
doubly_stochastic = mhc.sinkhorn_knopp(matrix)

# Manifold Hyper-Connection module
connection = mhc.ManifoldHyperConnection(dims=512, expansion=2)
output = connection(x, layer_output)
```

## What is mHC?

mHC (Manifold-Constrained Hyper-Connections) improves training stability for large language models by constraining residual connection mixing matrices to the Birkhoff polytope (doubly stochastic matrices).

Key benefits:
- Prevents gradient explosion in deep networks
- Maintains identity mapping property
- 2.1% improvement on benchmarks with only 6.7% overhead

## Step-by-Step Integration

### Step 1: Identify Your Residual Connections

In a standard transformer, residual connections look like:
```python
# Attention residual
h = x + self.attn(self.norm1(x))

# MLP residual
output = h + self.mlp(self.norm2(h))
```

### Step 2: Create mHC Connections

Add one `ManifoldHyperConnection` for each residual:
```python
import mlx_mhc as mhc

# In __init__
self.mhc_attn = mhc.ManifoldHyperConnection(dims=hidden_size)
self.mhc_mlp = mhc.ManifoldHyperConnection(dims=hidden_size)
```

### Step 3: Replace Residual Additions

Change `x + layer_output` to `self.mhc(x, layer_output)`:
```python
# Before: h = x + self.attn(self.norm1(x))
# After:
h = self.mhc_attn(x, self.attn(self.norm1(x)))

# Before: output = h + self.mlp(self.norm2(h))
# After:
output = self.mhc_mlp(h, self.mlp(self.norm2(h)))
```

### Complete Example

```python
import mlx.nn as nn
import mlx_mhc as mhc

class TransformerBlock(nn.Module):
    def __init__(self, dims, num_heads):
        super().__init__()
        self.norm1 = nn.RMSNorm(dims)
        self.norm2 = nn.RMSNorm(dims)
        self.attn = nn.MultiHeadAttention(dims, num_heads)
        self.mlp = nn.Sequential(
            nn.Linear(dims, dims * 4),
            nn.GELU(),
            nn.Linear(dims * 4, dims),
        )
        # mHC replaces standard residual connections
        self.mhc_attn = mhc.ManifoldHyperConnection(dims)
        self.mhc_mlp = mhc.ManifoldHyperConnection(dims)

    def __call__(self, x):
        h = self.mhc_attn(x, self.attn(self.norm1(x), self.norm1(x), self.norm1(x)))
        return self.mhc_mlp(h, self.mlp(self.norm2(h)))
```

## API Reference

### `sinkhorn_knopp(matrix, max_iterations=100, epsilon=1e-6, log_space=True)`

Project a matrix onto the Birkhoff polytope (set of doubly stochastic matrices).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `matrix` | mx.array | required | Input matrix to project |
| `max_iterations` | int | 100 | Maximum Sinkhorn iterations |
| `epsilon` | float | 1e-6 | Convergence threshold |
| `log_space` | bool | True | Use log-space for numerical stability |

### `ManifoldHyperConnection(dims, expansion=2, sinkhorn_iterations=10)`

MLX module implementing mHC for transformer residual connections.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dims` | int | required | Hidden dimension (must match your model) |
| `expansion` | int | 2 | Expansion factor for H_res matrix |
| `sinkhorn_iterations` | int | 10 | Sinkhorn iterations per forward pass |

## Author

Created by **Mario Iturrino** ([@machiabeli](https://github.com/machiabeli))

## License

MIT
