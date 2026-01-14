"""
多进程管理器模块

提供进程生命周期管理功能。
"""

import multiprocessing as mp
import logging
from typing import List, Optional
import time


class ProcessManager:
    """
    进程管理器

    管理多个进程的启动、停止和监控。
    """

    def __init__(self):
        """初始化进程管理器"""
        self.processes: List[mp.Process] = []
        self.stop_event: Optional[mp.Event] = None

    def add_process(self, process: mp.Process):
        """
        添加进程到管理器

        参数:
            process: 进程对象
        """
        self.processes.append(process)

    def start_all(self, delay_between_starts: float = 1.0):
        """
        启动所有进程

        参数:
            delay_between_starts: 进程启动间隔（秒），默认 1.0
        """
        logging.info(f"启动 {len(self.processes)} 个进程...")

        for i, proc in enumerate(self.processes):
            proc.start()
            logging.info(f"进程 [{i}] {proc.name} 已启动 (PID: {proc.pid})")

            # 在启动进程之间添加延迟
            if i < len(self.processes) - 1:
                time.sleep(delay_between_starts)

        logging.info("所有进程已启动")

    def stop_all(self, timeout: float = 2.0, force: bool = True):
        """
        停止所有进程

        参数:
            timeout: 等待进程结束的超时时间（秒）
            force: 超时后是否强制终止进程
        """
        logging.info("正在停止所有进程...")

        # 设置停止事件
        if self.stop_event:
            self.stop_event.set()

        # 等待进程结束
        for proc in self.processes:
            proc.join(timeout=timeout)

        # 强制终止仍在运行的进程
        if force:
            for proc in self.processes:
                if proc.is_alive():
                    logging.warning(f"进程 {proc.name} 未响应，强制终止")
                    proc.terminate()
                    proc.join(timeout=1.0)

                    # 如果仍未终止，使用 kill
                    if proc.is_alive():
                        logging.error(f"进程 {proc.name} 无法终止，使用 kill")
                        proc.kill()

        logging.info("所有进程已停止")

    def wait_for_any(self):
        """
        等待任意一个进程结束

        返回:
            结束的进程对象
        """
        while True:
            for proc in self.processes:
                if not proc.is_alive():
                    return proc
            time.sleep(0.1)

    def are_all_alive(self) -> bool:
        """检查所有进程是否都在运行"""
        return all(proc.is_alive() for proc in self.processes)

    def get_status(self) -> dict:
        """
        获取所有进程的状态

        返回:
            状态字典
        """
        status = {}
        for i, proc in enumerate(self.processes):
            status[proc.name] = {
                'pid': proc.pid,
                'is_alive': proc.is_alive(),
                'exitcode': proc.exitcode,
            }
        return status

    def cleanup(self):
        """清理资源"""
        self.stop_all()
        self.processes.clear()
