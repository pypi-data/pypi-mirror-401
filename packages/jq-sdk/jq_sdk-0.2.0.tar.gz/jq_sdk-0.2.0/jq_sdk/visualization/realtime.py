"""
实时热力图渲染模块

使用 matplotlib 提供实时热力图渲染功能。
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import multiprocessing as mp
import logging
import time
from typing import Dict, Callable, Optional
from .config import VisualizationConfig, DEFAULT_CONFIG


class RealtimeHeatmap:
    """
    实时热力图类（单进程版本）

    使用 matplotlib 的 blitting 技术实现高性能实时渲染。
    """

    def __init__(
        self,
        size: tuple = (32, 32),
        config: Optional[VisualizationConfig] = None
    ):
        """
        初始化实时热力图

        参数:
            size: 矩阵大小，默认 (32, 32)
            config: 可视化配置，None 则使用默认配置
        """
        self.size = size
        self.config = config or DEFAULT_CONFIG

        self.fig = None
        self.ax = None
        self.im = None
        self.cbar = None
        self.anim = None

        # 帧统计
        self.frame_count = 0
        self.render_frame_count = 0
        self.render_last_time = time.time()
        self.render_fps = 0.0

    def setup_figure(self):
        """初始化 matplotlib 图形"""
        self.fig, self.ax = plt.subplots(figsize=self.config.figsize)

        # 初始化热力图
        initial_data = np.zeros(self.size)
        self.im = self.ax.imshow(
            initial_data,
            cmap=self.config.colormap,
            interpolation=self.config.interpolation,
            vmin=self.config.vmin,
            vmax=self.config.vmax,
            animated=True,
            aspect=self.config.aspect
        )

        # 添加颜色条
        if self.config.show_colorbar:
            self.cbar = self.fig.colorbar(self.im, ax=self.ax, label='数值')

        # 设置标题和标签
        self.ax.set_title("实时热力图 | FPS: 0.00", fontsize=14)
        self.ax.set_xlabel(f"列 (0-{self.size[1]-1})")
        self.ax.set_ylabel(f"行 (0-{self.size[0]-1})")

        # 设置坐标轴刻度
        step = max(self.size[0] // 8, 1)
        self.ax.set_xticks(range(0, self.size[1], step))
        self.ax.set_yticks(range(0, self.size[0], step))

    def update(self, matrix: np.ndarray, stats: Optional[Dict] = None):
        """
        更新热力图数据

        参数:
            matrix: 新的矩阵数据
            stats: 可选的统计信息字典
        """
        if self.im is None:
            return

        self.im.set_data(matrix)
        self.frame_count += 1

        # 更新标题
        if stats:
            self._update_title_with_stats(stats)

    def _update_title_with_stats(self, stats: Dict):
        """根据统计信息更新标题"""
        title = (
            f"实时热力图 | "
            f"渲染FPS: {self.render_fps:.2f} | "
            f"帧数: {self.frame_count}\n"
            f"统计: 中位数={stats.get('median', 0):.1f}, "
            f"均值={stats.get('mean_valid', 0):.1f}, "
            f"最大={stats.get('max', 0):.1f}"
        )
        self.ax.set_title(title, fontsize=9)


class HeatmapProcess:
    """
    热力图渲染进程（多进程版本）

    在独立进程中运行，从队列获取数据并实时渲染。
    """

    def __init__(
        self,
        size: tuple = (32, 32),
        config: Optional[VisualizationConfig] = None
    ):
        """
        初始化热力图进程

        参数:
            size: 矩阵大小，默认 (32, 32)
            config: 可视化配置，None 则使用默认配置
        """
        self.size = size
        self.config = config or DEFAULT_CONFIG

    def run(
        self,
        data_queue: mp.Queue,
        stats_queue: mp.Queue,
        stop_event: mp.Event
    ):
        """
        进程主循环

        参数:
            data_queue: 矩阵数据队列
            stats_queue: 统计信息队列
            stop_event: 停止事件
        """
        logging.info("渲染进程已启动")

        # 初始化图形
        fig, ax = plt.subplots(figsize=self.config.figsize)

        # 初始化热力图
        initial_data = np.zeros(self.size)
        im = ax.imshow(
            initial_data,
            cmap=self.config.colormap,
            interpolation=self.config.interpolation,
            vmin=self.config.vmin,
            vmax=self.config.vmax,
            animated=True,
            aspect=self.config.aspect
        )

        if self.config.show_colorbar:
            fig.colorbar(im, ax=ax, label='数值')

        ax.set_title("实时热力图 | FPS: 0.00", fontsize=14)
        ax.set_xlabel(f"列 (0-{self.size[1]-1})")
        ax.set_ylabel(f"行 (0-{self.size[0]-1})")

        # 设置坐标轴刻度
        step = max(self.size[0] // 8, 1)
        ax.set_xticks(range(0, self.size[1], step))
        ax.set_yticks(range(0, self.size[0], step))

        # 存储统计信息
        stats_info = {
            'valid_fps': 0,
            'valid_frames': 0,
            'invalid_frames': 0,
            'total_frames': 0
        }

        # 渲染帧计数器
        render_frame_count = [0]
        render_last_time = [time.time()]
        render_fps = [0.0]

        # 累计统计
        total_valid_frames = [0]
        total_invalid_frames = [0]

        # 矩阵统计信息
        matrix_stats_current = {
            'median': 0,
            'mean': 0,
            'mean_valid': 0,
            'max': 0,
            'count_255': 0,
            'count_valid': 0,
            'min': 0
        }

        def update_frame(frame):
            """动画更新函数"""
            nonlocal render_frame_count, render_last_time, render_fps

            # 尝试获取最新的矩阵数据（非阻塞）
            updated = False
            while not data_queue.empty():
                try:
                    data_dict = data_queue.get_nowait()
                    matrix = data_dict['matrix']
                    matrix_stats_current.update(data_dict['stats'])

                    im.set_data(matrix)

                    # 动态调整颜色范围（可选）
                    vmin = self.config.vmin
                    vmax = self.config.vmax
                    if vmax > vmin:
                        im.set_clim(vmin=vmin, vmax=vmax)

                    updated = True
                    total_valid_frames[0] += 1
                except:
                    break

            # 尝试获取统计信息（非阻塞）
            while not stats_queue.empty():
                try:
                    new_stats = stats_queue.get_nowait()
                    stats_info.update(new_stats)
                    total_invalid_frames[0] += new_stats.get('invalid_frames', 0)
                except:
                    break

            # 计算渲染帧率
            if updated:
                render_frame_count[0] += 1
                current_time = time.time()
                elapsed = current_time - render_last_time[0]

                if elapsed >= 1.0:  # 每秒更新一次渲染帧率
                    render_fps[0] = render_frame_count[0] / elapsed
                    render_frame_count[0] = 0
                    render_last_time[0] = current_time

            # 更新标题（每帧都更新）
            ax.set_title(
                f"实时热力图 (32x32) | "
                f"接收FPS: {stats_info['valid_fps']:.2f} | "
                f"渲染FPS: {render_fps[0]:.2f}\n"
                f"有效帧: {total_valid_frames[0]} | "
                f"无效帧: {total_invalid_frames[0]} | "
                f"统计(有效点): 中位数={matrix_stats_current['median']:.1f}, "
                f"均值={matrix_stats_current['mean_valid']:.1f}, "
                f"有效点数={int(matrix_stats_current['count_valid'])}\n"
                f"全局: 最大={matrix_stats_current['max']:.1f}, "
                f"最小={matrix_stats_current['min']:.1f}, "
                f"255值个数={int(matrix_stats_current['count_255'])}",
                fontsize=9
            )

            return [im] if updated else []

        # 使用 FuncAnimation，blit=True 开启 blitting 加速
        anim = FuncAnimation(
            fig,
            update_frame,
            interval=self.config.update_interval,
            blit=True,
            cache_frame_data=False
        )

        plt.tight_layout()

        try:
            plt.show()
        except KeyboardInterrupt:
            logging.info("渲染进程被中断")
        finally:
            stop_event.set()
            logging.info("渲染进程已退出")


def start_heatmap_process(
    data_queue: mp.Queue,
    stats_queue: mp.Queue,
    stop_event: mp.Event,
    size: tuple = (32, 32),
    config: Optional[VisualizationConfig] = None
) -> mp.Process:
    """
    启动热力图渲染进程

    参数:
        data_queue: 矩阵数据队列
        stats_queue: 统计信息队列
        stop_event: 停止事件
        size: 矩阵大小，默认 (32, 32)
        config: 可视化配置，None 则使用默认配置

    返回:
        进程对象
    """
    renderer = HeatmapProcess(size, config)
    proc = mp.Process(
        target=renderer.run,
        args=(data_queue, stats_queue, stop_event),
        name="Renderer"
    )
    return proc
