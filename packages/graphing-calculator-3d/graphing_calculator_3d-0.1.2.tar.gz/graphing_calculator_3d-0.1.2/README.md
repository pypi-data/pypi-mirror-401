# 3D Graphing Calculator

A Python library for rendering 3D and 4D mathematical expressions using VisPy.

## Installation

```bash
pip install graphing_calculator_3d
```

## Usage

```python
import sympy as sp
from graphing_lib import api_contract

x, y, z, t = sp.symbols('x y z t')

# Define a 4D function (animated over t)
function = x**2 + y**2 + z - 25 + sp.sin(t)

# Plot it
api_contract.plot(function)
```