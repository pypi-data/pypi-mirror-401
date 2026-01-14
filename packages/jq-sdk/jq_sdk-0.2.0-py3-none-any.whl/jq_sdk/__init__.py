"""
JQ-SDK: A comprehensive package for sensor data acquisition and visualization.

This package provides:
- Static heatmap visualization with Plotly (1024 elements -> 32x32 heatmaps)
- Realtime serial data acquisition and visualization (32x32 sensor arrays)

For serial acquisition features, install with:
    pip install jq-sdk[serial]
"""

__version__ = "0.2.0"
__author__ = "Hirkond"
__email__ = "thd20x@gmail.com"

# 静态热力图可视化（基础功能）
from .heatmap import plot_heatmap, get_available_colorschemes, COLORSCHEMES

__all__ = [
    # 静态可视化
    "plot_heatmap",
    "get_available_colorschemes",
    "COLORSCHEMES",
]

# 尝试导入串口功能（可选依赖）
try:
    from .pipeline import start_realtime_acquisition
    _SERIAL_AVAILABLE = True
    __all__.append("start_realtime_acquisition")
except ImportError as e:
    _SERIAL_AVAILABLE = False

    # 提供友好的错误提示
    def start_realtime_acquisition(*args, **kwargs):
        raise ImportError(
            "Serial acquisition features require additional dependencies.\n"
            "Install with: pip install jq-sdk[serial]\n\n"
            f"Missing dependency: {str(e)}"
        )

    __all__.append("start_realtime_acquisition")
