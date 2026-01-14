"""
管道模块

提供端到端的实时数据采集和可视化管道。
"""

from typing import Optional

from .process_manager import ProcessManager
from .realtime_pipeline import RealtimePipeline


def start_realtime_acquisition(
    port: Optional[str] = None,
    baudrate: int = 1000000,
    colormap: str = 'hot',
    figsize: tuple = (8, 8),
    interactive_port_selection: bool = True,
    processing_mode: str = 'standard'
) -> RealtimePipeline:
    """
    启动实时数据采集和可视化

    这是高级API，提供最简单的使用方式。

    参数:
        port: 串口设备名（如 'COM3'），None 则自动选择
        baudrate: 波特率，默认 1000000
        colormap: 颜色映射，默认 'hot'
        figsize: 图形大小 (宽, 高)，默认 (8, 8)
        interactive_port_selection: 是否交互式选择串口，默认 True
        processing_mode: 数据处理模式，默认 'standard'
            - 'standard': 标准处理（1024字节 → 32x32 → 线序调整 → 16x16 → 插值 → 32x32）
            - 'raw': 原始数据（1024字节 → 直接 reshape 32x32，无线序调整和插值）
            - 'no_interpolation': 仅线序调整（1024字节 → 32x32 → 线序调整 → 16x16，无插值）

    返回:
        RealtimePipeline 对象

    示例:
        >>> import jq_sdk
        >>> # 最简单的方式（自动选择串口，标准处理）
        >>> jq_sdk.start_realtime_acquisition()

        >>> # 指定串口
        >>> jq_sdk.start_realtime_acquisition(port='COM3')

        >>> # 原始数据模式（无线序调整）
        >>> jq_sdk.start_realtime_acquisition(
        ...     port='COM3',
        ...     processing_mode='raw'
        ... )

        >>> # 自定义配置
        >>> jq_sdk.start_realtime_acquisition(
        ...     port='COM3',
        ...     colormap='plasma',
        ...     figsize=(10, 10),
        ...     processing_mode='standard'
        ... )

    注意:
        - 需要安装串口功能：pip install jq-sdk[serial]
        - Windows 需要在 if __name__ == '__main__': 中调用
        - 关闭显示窗口即可停止采集
        - 可以使用 Ctrl+C 强制终止
    """
    pipeline = RealtimePipeline(
        port=port,
        baudrate=baudrate,
        colormap=colormap,
        figsize=figsize,
        interactive_port_selection=interactive_port_selection,
        processing_mode=processing_mode
    )

    pipeline.start()
    return pipeline


__all__ = [
    'ProcessManager',
    'RealtimePipeline',
    'start_realtime_acquisition',
]
