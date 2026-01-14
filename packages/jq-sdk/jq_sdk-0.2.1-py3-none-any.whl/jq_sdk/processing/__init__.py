"""
数据处理模块

提供数据变换、插值和统计计算功能。
"""

from .transform import adjust_wire_order, create_default_mapping
from .interpolation import (
    interpolate_bilinear,
    interpolate_to_target_size,
    InterpolationMethod,
)
from .stats import calculate_stats, create_stats_object, MatrixStats

__all__ = [
    # 变换函数
    'adjust_wire_order',
    'create_default_mapping',
    # 插值函数
    'interpolate_bilinear',
    'interpolate_to_target_size',
    'InterpolationMethod',
    # 统计函数
    'calculate_stats',
    'create_stats_object',
    'MatrixStats',
]
