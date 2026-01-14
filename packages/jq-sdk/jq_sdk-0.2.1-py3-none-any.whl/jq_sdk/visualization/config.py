"""
可视化配置模块

提供可视化相关的配置和常量。
"""

from dataclasses import dataclass
from typing import Tuple
import matplotlib.pyplot as plt


@dataclass
class VisualizationConfig:
    """
    可视化配置类

    属性:
        colormap: 颜色映射名称
        figsize: 图形大小 (宽, 高) 单位：英寸
        update_interval: 更新间隔（毫秒）
        vmin: 颜色映射最小值
        vmax: 颜色映射最大值
        show_colorbar: 是否显示颜色条
        interpolation: matplotlib 插值方法
        aspect: 图像纵横比
    """
    colormap: str = 'hot'
    figsize: Tuple[float, float] = (8, 8)
    update_interval: int = 10  # 毫秒
    vmin: float = 0
    vmax: float = 255
    show_colorbar: bool = True
    interpolation: str = 'nearest'
    aspect: str = 'equal'

    def to_dict(self):
        """转换为字典"""
        return {
            'colormap': self.colormap,
            'figsize': self.figsize,
            'update_interval': self.update_interval,
            'vmin': self.vmin,
            'vmax': self.vmax,
            'show_colorbar': self.show_colorbar,
            'interpolation': self.interpolation,
            'aspect': self.aspect,
        }


# 默认配置
DEFAULT_CONFIG = VisualizationConfig()


def setup_chinese_font():
    """
    设置中文字体支持

    尝试配置 matplotlib 支持中文显示，
    如果失败则使用默认字体。
    """
    try:
        # 尝试使用 SimHei 字体（黑体）
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    except Exception:
        # 如果设置失败，使用默认字体
        pass


# 自动设置中文字体
setup_chinese_font()


# 常用颜色映射
COLORMAPS = {
    'hot': 'Hot',
    'viridis': 'Viridis',
    'plasma': 'Plasma',
    'inferno': 'Inferno',
    'magma': 'Magma',
    'jet': 'Jet',
    'turbo': 'Turbo',
    'coolwarm': 'CoolWarm',
    'seismic': 'Seismic',
}


def get_available_colormaps():
    """
    获取可用的颜色映射列表

    返回:
        颜色映射名称列表
    """
    return list(COLORMAPS.keys())
