# KANLinear

A PyTorch implementation of the KANLinear layer.

## Installation

```bash
pip install git+https://github.com/dillfrescott/kan_linear
```

## Usage

```python
from kan_linear import KANLinear
import torch

model = KANLinear(in_features=10, out_features=5)
x = torch.randn(1, 10)
output = model(x)
print(output.shape)
```
