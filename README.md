# moiré pattern generator

This script generates moiré patterns from custom user-defined kernel functions.

All of the pattern generation logic is located in a single function, `moire_pattern()`.

### parameters

- **`n`** *int*: Size of the image width and height in pixels (n x n).
- **`k`** *float*: Scaling factor affecting pattern frequency and density.
- **`kernel`** *{'elliptical', 'hexagonal', 'radial', 'spiral', 'square', 'star', 'wave'} | Callable[[ndarray, ndarray], ndarray]*: Determines pattern shape. Can be the name of a preset kernel or a callable object which accepts two arrays and returns an array.
- **`colorize`** *bool*: `False` for greyscale (default), `True` for RGB.

### preset kernels

The preset kernels are in the global variable `KERNELS`, a dict mapping of names to lambda functions.

- `'elliptical'`
- `'hexagonal'`
- `'radial'`
- `'spiral'`
- `'square'`
- `'star'`
- `'wave'`

The presets offer quite a bit when it comes to experimentation.

This is especially true if one were to chain them together using higher-order lambdas, such as in the following code:

```python
from moire import moire_pattern, KERNELS
from PIL import Image

# using the product of two other patterns as the pattern
kernel_chain = lambda x, y: KERNELS['hexagonal'](x, y) * KERNELS['star'](x, y)

output = moire_pattern(m=999, k=777, kernel=kernel_chain, colorize=True)

Image.fromarray(output).show()
```

... which creates this output image:

![moire_rainbow](https://github.com/user-attachments/assets/05161402-77a4-462b-8e9b-827cf5cac8f2)


## more code examples

### preset kernel ('spiral')

```python
from moire import moire_pattern
from PIL import Image

output = moire_pattern(n=500, k=100.0, kernel='spiral', colorize=False)

Image.fromarray(output).show()
```

### user-defined kernel

```python
import numpy as np
from moire import moire_pattern
from PIL import Image

# custom kernel function
def custom_kernel(x, y):
    return np.sin(x) * np.cos(y)

# rgb image
output = moire_pattern(n=500, k=100.0, kernel=custom_kernel, colorize=True)

Image.fromarray(output).show()
```

## requirements
* Python>=3.12
```
numpy~=2.1.3
pillow~=10.4.0
matplotlib~=3.10.0rc1
```


## additional resources
* [Circle Squares fractal](https://paulbourke.net/fractals/circlesquares/) - the base implementation is pretty much directly from this. also very cool site, shoutout Paul Bourke fr
* [黎曼ζ函數](https://zh.wikipedia.org/wiki/%E9%BB%8E%E6%9B%BC%CE%B6%E5%87%BD%E6%95%B8) - mathematics wikipedia
