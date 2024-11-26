# moiré pattern generator

This script generates moiré patterns from custom user-defined kernel functions.

All of the pattern generation logic is located in a single function, `moire_pattern()`.

### parameters

- **`n`** *int*: Size of the image width and height in pixels (n x n).
- **`k`** *float*: Scaling factor affecting pattern frequency and density.
- **`kernel`** *{'elliptical', 'hexagonal', 'radial', 'spiral', 'square', 'star', 'wave'} | Callable[[ndarray, ndarray], ndarray]*: Determines pattern shape. Can be the name of a preset kernel or a callable object which accepts two arrays and returns an array.
- **`colorize`** *bool*: `False` for greyscale (default), `True` for RGB.

### preset kernels

The preset kernels are a dictionary of lambda functions that gets created at runtime.

- `'elliptical'`
- `'hexagonal'`
- `'radial'`
- `'spiral'`
- `'square'`
- `'star'`
- `'wave'`

## usage

### example with preset kernel

```python
from moire import moire_pattern
from PIL import Image

# generate a spiral pattern
output = moire_pattern(n=500, k=100.0, kernel='spiral', colorize=False)

# display the image
Image.fromarray(output).show()
```

### example with user-defined kernel

```python
import numpy as np
from moire import moire_pattern
from PIL import Image

# define a custom kernel function
def custom_kernel(x, y):
    return np.sin(x) * np.cos(y)

# make an rgb image with the kernel function
output = moire_pattern(n=500, k=100.0, kernel=custom_kernel, colorize=True)

# display the image
Image.fromarray(output).show()
```

## requirements
* Python>=3.12
```
numpy~=2.1.3
pillow~=10.4.0
matplotlib~=3.10.0rc1
```
