"""
数据变换模块

提供线序调整和矩阵变换功能，将原始传感器数据转换为物理排列。
"""

import numpy as np
from typing import Optional


def adjust_wire_order(
    img_data: np.ndarray,
    row_map: Optional[np.ndarray] = None,
    col_map: Optional[np.ndarray] = None
) -> np.ndarray:
    """
    通用的正向行列索引变换函数

    用于将传感器的硬件布线顺序转换为物理排列顺序。

    参数:
        img_data: 输入数据矩阵，通常为 32x32
        row_map: 行索引映射数组，None 则使用默认映射
        col_map: 列索引映射数组，None 则使用默认映射

    返回:
        img_return: 变换后的矩阵，通常为 16x16

    默认映射:
        - row_map: 0-15 (对应 MATLAB 的 1:16)
        - col_map: [0-7, 15-8反向] (对应 MATLAB 的 [1:8, 16:-1:9])

    示例:
        >>> import numpy as np
        >>> data = np.random.rand(32, 32)
        >>> adjusted = adjust_wire_order(data)
        >>> adjusted.shape
        (16, 16)
    """
    # 使用默认映射
    if row_map is None:
        row_map = np.arange(16)

    if col_map is None:
        # [0-7, 15-8反向]
        col_map = np.concatenate([np.arange(8), np.arange(15, 7, -1)])

    # 应用行列索引变换
    img_return = img_data[np.ix_(row_map, col_map)]

    return img_return


def create_default_mapping() -> tuple:
    """
    创建默认的行列映射

    返回:
        (row_map, col_map): 默认的行列映射数组

    示例:
        >>> row_map, col_map = create_default_mapping()
        >>> row_map.shape
        (16,)
        >>> col_map.shape
        (16,)
    """
    row_map = np.arange(16)
    col_map = np.concatenate([np.arange(8), np.arange(15, 7, -1)])
    return row_map, col_map
