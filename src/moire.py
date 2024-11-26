from typing import Callable, Literal, Union, overload

import numpy as np
from PIL import Image

type ShapedArray[_Shape: tuple[int, ...], _SCT: np.generic] = np.ndarray[_Shape, np.dtype[_SCT]]
type Matrix[_SCT: np.generic] = ShapedArray[tuple[int, int], _SCT]
type UInt8Matrix = Matrix[np.uint8]
type BinaryArrayFunc = Callable[[np.ndarray, np.ndarray], np.ndarray]

_KernelNames = Literal[
    'elliptical',
    'hexagonal',
    'radial',
    'spiral',
    'square',
    'star',
    'wave',
]


def _make_kernel_dict():
    def _default_func(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return np.sqrt(x ** 2 + y ** 2)

    names: list[Union[_KernelNames, str]] = getattr(_KernelNames, '__args__', [])
    d = {
        **dict.fromkeys(names, _default_func),
        'elliptical': lambda x, y: (x * 1.5) ** 2 + (y * 0.8) ** 2,
        'hexagonal': lambda x, y: np.cos(x) + np.cos(y - x * np.sqrt(3) / 2) + np.cos(
            y + x * np.sqrt(3) / 2),
        'spiral': lambda x, y: _default_func(x, y) + np.arctan2(y, x),
        'wave': lambda x, y: np.sin(_default_func(x, y)),
        'star': lambda x, y: np.sin(x) ** 2 + np.cos(y) ** 2,
        'square': lambda x, y: np.abs(x) + np.abs(y)
    }
    return d


KERNELS = _make_kernel_dict()


@overload
def moire_pattern(
    n: int,
    k=100.0,
    *,
    kernel: Union[_KernelNames, BinaryArrayFunc] = None,
    colorize: Literal[False] = False
) -> UInt8Matrix:
    ...


@overload
def moire_pattern(
    n: int,
    k=100.0,
    *,
    kernel: Union[_KernelNames, BinaryArrayFunc] = None,
    colorize: Literal[True]
) -> ShapedArray[tuple[int, int, Literal[3]], np.uint8]:
    ...


def moire_pattern(
    n: int,
    k: float = 100.0,
    *,
    kernel: Union[_KernelNames, BinaryArrayFunc] = None,
    colorize: bool = False
) -> UInt8Matrix:
    x = np.linspace(-n / 2., n / 2., n) * 10. / n
    X, Y = np.meshgrid(x, x)
    if kernel is None:
        kernel = lambda *_: X ** 2 + Y ** 2
    elif isinstance(kernel, str):
        kernel = KERNELS[kernel]
    lens = np.exp(k * (0 - 1j) * kernel(X, Y))
    angle_mat = np.angle(lens)
    angle_norm = (angle_mat - angle_mat.min()) / (angle_mat.max() - angle_mat.min())
    if colorize is True:
        from matplotlib.colors import hsv_to_rgb as m_hsv2rgb

        magnitude_mat = np.abs(lens)
        magnitude_norm = magnitude_mat / magnitude_mat.max()
        hsv = np.zeros((n, n, 3), dtype=np.float32)
        hsv[..., 0] = angle_norm
        hsv[..., 1] = 1.0
        hsv[..., 2] = magnitude_norm
        out = m_hsv2rgb(hsv)
    else:
        out = angle_norm
    return (255 * out).astype(np.uint8)


if __name__ == '__main__':
    m = 333 * 3
    K = 100.

    kernel_func = lambda x, y: -KERNELS['spiral'](x, y) - KERNELS['star'](x, y)
    output = moire_pattern(m, k=777, kernel=kernel_func, colorize=True)

    Image.fromarray(output).convert('RGB').show()
