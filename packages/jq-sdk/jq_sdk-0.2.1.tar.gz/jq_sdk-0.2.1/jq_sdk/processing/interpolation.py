"""
插值算法模块

提供多种插值方法，用于提升矩阵分辨率。
"""

import numpy as np
from scipy.interpolate import RectBivariateSpline
from typing import Literal


InterpolationMethod = Literal['bilinear', 'bicubic', 'nearest']


def interpolate_bilinear(frame_data_16x16: np.ndarray) -> np.ndarray:
    """
    将 16x16 矩阵插值为 32x32（使用双线性插值）

    使用 scipy 的 RectBivariateSpline 进行快速双线性插值，
    适合实时处理场景。

    参数:
        frame_data_16x16: 16x16 输入矩阵

    返回:
        frame_data_32x32: 32x32 插值后的矩阵

    示例:
        >>> import numpy as np
        >>> data_16 = np.random.rand(16, 16)
        >>> data_32 = interpolate_bilinear(data_16)
        >>> data_32.shape
        (32, 32)

    注意:
        输出矩阵的数值会被裁剪到 [0, 255] 范围内
    """
    # 验证输入形状
    if frame_data_16x16.shape != (16, 16):
        raise ValueError(
            f"Input must be 16x16, got {frame_data_16x16.shape}"
        )

    # 创建原始网格
    x_orig = np.arange(16)
    y_orig = np.arange(16)

    # 创建新网格（32x32）
    x_new = np.linspace(0, 15, 32)
    y_new = np.linspace(0, 15, 32)

    # 使用双线性插值（Bilinear Interpolation）
    # kx=1, ky=1 表示使用1阶样条（线性），计算快速，适合实时显示
    interp_func = RectBivariateSpline(
        y_orig, x_orig, frame_data_16x16, kx=1, ky=1
    )
    frame_data_32x32 = interp_func(y_new, x_new)

    # 裁剪到有效范围[0, 255]，确保数据在有效范围内
    frame_data_32x32 = np.clip(frame_data_32x32, 0, 255)

    return frame_data_32x32


def interpolate_to_target_size(
    matrix: np.ndarray,
    target_shape: tuple,
    method: InterpolationMethod = 'bilinear'
) -> np.ndarray:
    """
    将矩阵插值到目标大小

    参数:
        matrix: 输入矩阵
        target_shape: 目标形状，如 (32, 32)
        method: 插值方法，可选 'bilinear', 'bicubic', 'nearest'

    返回:
        插值后的矩阵

    示例:
        >>> import numpy as np
        >>> data = np.random.rand(16, 16)
        >>> result = interpolate_to_target_size(data, (32, 32))
        >>> result.shape
        (32, 32)
    """
    if matrix.shape == target_shape:
        return matrix

    rows_orig, cols_orig = matrix.shape
    rows_new, cols_new = target_shape

    # 创建原始网格
    x_orig = np.arange(cols_orig)
    y_orig = np.arange(rows_orig)

    # 创建新网格
    x_new = np.linspace(0, cols_orig - 1, cols_new)
    y_new = np.linspace(0, rows_orig - 1, rows_new)

    # 根据方法选择插值阶数
    if method == 'bilinear':
        kx, ky = 1, 1
    elif method == 'bicubic':
        kx, ky = 3, 3
    elif method == 'nearest':
        kx, ky = 0, 0
    else:
        raise ValueError(f"Unknown interpolation method: {method}")

    # 执行插值
    interp_func = RectBivariateSpline(y_orig, x_orig, matrix, kx=kx, ky=ky)
    result = interp_func(y_new, x_new)

    # 裁剪到有效范围
    result = np.clip(result, 0, 255)

    return result
