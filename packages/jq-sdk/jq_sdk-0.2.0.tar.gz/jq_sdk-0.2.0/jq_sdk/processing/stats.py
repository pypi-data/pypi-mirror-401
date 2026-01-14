"""
统计计算模块

提供矩阵统计信息计算功能。
"""

import numpy as np
from typing import Dict


class MatrixStats:
    """
    矩阵统计信息数据类

    属性:
        median: 有效点(>0)的中位数
        mean: 全局平均值
        mean_valid: 有效点的平均值
        max: 最大值
        min: 最小值
        count_255: 饱和点个数（值为255）
        count_valid: 有效点个数（值>0）
    """

    def __init__(self, stats_dict: Dict[str, float]):
        self.median = stats_dict['median']
        self.mean = stats_dict['mean']
        self.mean_valid = stats_dict['mean_valid']
        self.max = stats_dict['max']
        self.min = stats_dict['min']
        self.count_255 = stats_dict['count_255']
        self.count_valid = stats_dict['count_valid']

    def __repr__(self) -> str:
        return (
            f"MatrixStats(median={self.median:.1f}, "
            f"mean={self.mean:.1f}, "
            f"mean_valid={self.mean_valid:.1f}, "
            f"max={self.max:.1f}, "
            f"min={self.min:.1f}, "
            f"count_255={int(self.count_255)}, "
            f"count_valid={int(self.count_valid)})"
        )

    def to_dict(self) -> Dict[str, float]:
        """转换为字典"""
        return {
            'median': self.median,
            'mean': self.mean,
            'mean_valid': self.mean_valid,
            'max': self.max,
            'min': self.min,
            'count_255': self.count_255,
            'count_valid': self.count_valid,
        }


def calculate_stats(matrix: np.ndarray) -> Dict[str, float]:
    """
    计算矩阵的统计信息

    参数:
        matrix: 输入矩阵

    返回:
        stats: 包含统计信息的字典，包含以下键：
            - median: 有效点(>0)的中位数
            - mean: 全局平均值
            - mean_valid: 有效点的平均值
            - max: 最大值
            - min: 最小值
            - count_255: 饱和点个数（值为255）
            - count_valid: 有效点个数（值>0）

    示例:
        >>> import numpy as np
        >>> data = np.array([[0, 100, 200], [50, 255, 150]])
        >>> stats = calculate_stats(data)
        >>> stats['median']
        150.0
        >>> stats['count_valid']
        5
        >>> stats['count_255']
        1

    注意:
        0值通常表示无压力，在统计时会被排除
    """
    # 提取有效点（排除0值，因为0通常表示无压力）
    valid_points = matrix[matrix > 0]

    # 如果有有效点，计算中位数和均值，否则返回0
    if len(valid_points) > 0:
        median_value = float(np.median(valid_points))
        mean_valid = float(np.mean(valid_points))
    else:
        median_value = 0.0
        mean_valid = 0.0

    return {
        'median': median_value,               # 有效点的中位数
        'mean': float(np.mean(matrix)),       # 全部点的平均值
        'mean_valid': mean_valid,             # 有效点的平均值
        'max': float(np.max(matrix)),         # 最大值
        'min': float(np.min(matrix)),         # 最小值
        'count_255': int(np.sum(matrix == 255)),  # 饱和点个数
        'count_valid': int(len(valid_points)), # 有效点个数
    }


def create_stats_object(matrix: np.ndarray) -> MatrixStats:
    """
    创建 MatrixStats 对象

    参数:
        matrix: 输入矩阵

    返回:
        MatrixStats 对象

    示例:
        >>> import numpy as np
        >>> data = np.random.randint(0, 256, (32, 32))
        >>> stats = create_stats_object(data)
        >>> print(stats)
    """
    stats_dict = calculate_stats(matrix)
    return MatrixStats(stats_dict)
