"""
实时数据采集管道模块

提供端到端的实时串口数据采集和可视化功能。
"""

import multiprocessing as mp
import logging
from typing import Optional
from .process_manager import ProcessManager
from ..serial import start_serial_reader_process, select_port_interactive
from ..visualization import start_heatmap_process, VisualizationConfig


class RealtimePipeline:
    """
    实时数据采集管道

    协调串口读取、数据处理和实时可视化的完整流程。
    """

    def __init__(
        self,
        port: Optional[str] = None,
        baudrate: int = 1000000,
        colormap: str = 'hot',
        figsize: tuple = (8, 8),
        interactive_port_selection: bool = True
    ):
        """
        初始化实时采集管道

        参数:
            port: 串口设备名，None 则自动选择
            baudrate: 波特率，默认 1000000
            colormap: 颜色映射，默认 'hot'
            figsize: 图形大小，默认 (8, 8)
            interactive_port_selection: 是否交互式选择串口
        """
        self.port = port
        self.baudrate = baudrate
        self.colormap = colormap
        self.figsize = figsize
        self.interactive_port_selection = interactive_port_selection

        # IPC 原语
        self.data_queue = mp.Queue(maxsize=10)
        self.stats_queue = mp.Queue(maxsize=5)
        self.stop_event = mp.Event()

        # 进程管理器
        self.process_manager = ProcessManager()
        self.process_manager.stop_event = self.stop_event

        # 配置
        self.vis_config = VisualizationConfig(
            colormap=colormap,
            figsize=figsize
        )

    def _select_port(self) -> Optional[str]:
        """选择串口"""
        if self.port:
            return self.port

        if self.interactive_port_selection:
            return select_port_interactive()

        return None

    def start(self):
        """
        启动管道

        启动串口读取进程和渲染进程，然后等待渲染窗口关闭。
        """
        # 显示启动信息
        self._print_banner()

        # 选择串口
        selected_port = self._select_port()
        if not selected_port:
            logging.error("未选择串口，退出")
            return

        logging.info(f"使用串口: {selected_port}")

        # 创建串口读取进程
        serial_proc = start_serial_reader_process(
            selected_port,
            self.data_queue,
            self.stats_queue,
            self.stop_event,
            self.baudrate
        )
        self.process_manager.add_process(serial_proc)

        # 创建渲染进程
        render_proc = start_heatmap_process(
            self.data_queue,
            self.stats_queue,
            self.stop_event,
            size=(32, 32),
            config=self.vis_config
        )
        self.process_manager.add_process(render_proc)

        # 启动所有进程
        try:
            self.process_manager.start_all(delay_between_starts=1.0)

            # 等待渲染进程结束（用户关闭窗口）
            render_proc.join()

            logging.info("渲染窗口已关闭")

        except KeyboardInterrupt:
            logging.info("收到中断信号 (Ctrl+C)")
        finally:
            self.stop()

    def stop(self):
        """停止管道"""
        logging.info("正在停止管道...")
        self.stop_event.set()
        self.process_manager.stop_all(timeout=2.0, force=True)
        logging.info("管道已停止")

    def get_stats(self) -> dict:
        """
        获取运行统计

        返回:
            统计信息字典
        """
        return self.process_manager.get_status()

    @staticmethod
    def _print_banner():
        """打印启动横幅"""
        print("\n" + "="*60)
        print("JQ-SDK 实时数据采集系统")
        print("32x32 传感器热力图实时显示")
        print("多进程架构：串口接收进程 + GPU加速渲染进程")
        print("数据流: 1024字节 -> 32x32原始 -> 16x16线序调整 -> 32x32插值")
        print("="*60 + "\n")
