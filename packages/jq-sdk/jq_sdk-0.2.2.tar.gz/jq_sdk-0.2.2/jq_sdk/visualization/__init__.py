"""
可视化模块

提供实时热力图渲染功能。
"""

from .config import (
    VisualizationConfig,
    DEFAULT_CONFIG,
    setup_chinese_font,
    get_available_colormaps,
    COLORMAPS,
)
from .realtime import (
    RealtimeHeatmap,
    HeatmapProcess,
    start_heatmap_process,
)

__all__ = [
    # 配置
    'VisualizationConfig',
    'DEFAULT_CONFIG',
    'setup_chinese_font',
    'get_available_colormaps',
    'COLORMAPS',
    # 实时渲染
    'RealtimeHeatmap',
    'HeatmapProcess',
    'start_heatmap_process',
]
