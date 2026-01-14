"""
串口通信核心功能

提供串口读取器和多进程串口读取器。
"""

import serial
import numpy as np
import multiprocessing as mp
import logging
import time
from typing import Optional, Dict
from .protocol import FrameBuffer, FRAME_DATA_SIZE
from ..processing import adjust_wire_order, interpolate_bilinear, calculate_stats


class SerialReader:
    """
    串口读取器类（单线程版本）

    用于读取串口数据并解析为数据帧。

    属性:
        port: 串口设备名
        baudrate: 波特率
        timeout: 超时时间（秒）
        ser: serial.Serial 对象
        frame_buffer: 帧缓冲区
    """

    def __init__(
        self,
        port: str,
        baudrate: int = 1000000,
        timeout: float = 1.0
    ):
        """
        初始化串口读取器

        参数:
            port: 串口设备名（如 'COM3', '/dev/ttyUSB0'）
            baudrate: 波特率，默认 1000000
            timeout: 超时时间（秒），默认 1.0

        抛出:
            serial.SerialException: 串口打开失败
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.frame_buffer = FrameBuffer()

        # 打开串口
        self._open()

    def _open(self):
        """打开串口连接"""
        try:
            self.ser = serial.Serial(
                self.port,
                self.baudrate,
                timeout=self.timeout
            )
            logging.info(f'串口已连接: {self.port} @ {self.baudrate} bps')
        except serial.SerialException as e:
            logging.error(f'串口连接失败: {e}')
            raise

    def read_raw(self) -> Optional[np.ndarray]:
        """
        读取原始字节数据

        返回:
            字节数据数组，无数据时返回 None
        """
        if not self.is_open:
            return None

        if self.ser.in_waiting > 0:
            data = self.ser.read(self.ser.in_waiting)
            return np.frombuffer(data, dtype=np.uint8)

        return None

    def read_frame(self) -> Optional[np.ndarray]:
        """
        读取一个完整的数据帧

        返回:
            帧数据 (1024字节)，未读取到完整帧时返回 None

        说明:
            此方法会自动管理缓冲区，处理粘包和半包问题
        """
        if not self.is_open:
            return None

        # 读取新数据
        raw_data = self.read_raw()
        if raw_data is not None:
            self.frame_buffer.append(raw_data)

        # 清理过大的缓冲区
        self.frame_buffer.clear_excess()

        # 尝试提取帧
        frame_data, success = self.frame_buffer.extract_frame()

        if success:
            return frame_data
        return None

    @property
    def is_open(self) -> bool:
        """串口是否打开"""
        return self.ser is not None and self.ser.is_open

    def close(self):
        """关闭串口"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            logging.info(f'串口已关闭: {self.port}')


class SerialReaderProcess:
    """
    串口读取进程类（多进程版本）

    在独立进程中运行，持续读取串口数据、处理并通过队列传递给其他进程。
    """

    def __init__(
        self,
        port: str,
        baudrate: int = 1000000,
        timeout: float = 1.0
    ):
        """
        初始化串口读取进程

        参数:
            port: 串口设备名
            baudrate: 波特率，默认 1000000
            timeout: 超时时间（秒），默认 1.0
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

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

        说明:
            此方法在独立进程中运行，持续读取串口数据并处理
        """
        # 在进程中打开串口
        try:
            ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            logging.info(f'串口接收进程已连接到: {self.port}')
        except Exception as e:
            logging.error(f"串口连接失败: {e}")
            return

        frame_buffer = FrameBuffer()
        valid_frame_count = 0
        invalid_frame_count = 0
        last_time = time.time()

        logging.info("串口数据接收进程已启动")

        try:
            while not stop_event.is_set():
                # 读取新数据
                if ser.in_waiting > 0:
                    receive = ser.read(ser.in_waiting)
                    frame_buffer.append(np.frombuffer(receive, dtype=np.uint8))

                    # 尝试提取帧
                    frame_data, success = frame_buffer.extract_frame()

                    if success:
                        # 步骤1: reshape成32x32
                        matrix_32x32_raw = frame_data.reshape(32, 32)

                        # 步骤2: 线序调整，转换成16x16
                        frame_data_16x16 = adjust_wire_order(matrix_32x32_raw)

                        # 步骤3: 插值回32x32
                        matrix_32x32_interpolated = interpolate_bilinear(
                            frame_data_16x16
                        )

                        # 步骤4: 计算统计信息
                        matrix_stats = calculate_stats(matrix_32x32_interpolated)

                        # 清空队列，只保留最新数据（丢弃旧数据策略）
                        self._clear_queue(data_queue)

                        # 将最新矩阵和统计信息放入队列
                        try:
                            data_queue.put_nowait({
                                'matrix': matrix_32x32_interpolated,
                                'stats': matrix_stats
                            })
                            valid_frame_count += 1
                        except:
                            pass  # 队列满时忽略
                    elif frame_data is not None:
                        # 帧长度不对
                        invalid_frame_count += 1

                    # 清理缓冲区
                    frame_buffer.clear_excess()

                    # 计算帧率并发送统计信息
                    current_time = time.time()
                    elapsed = current_time - last_time
                    if elapsed >= 0.5:  # 每0.5秒更新一次
                        valid_fps = valid_frame_count / elapsed
                        total_frames = valid_frame_count + invalid_frame_count

                        # 清空旧统计信息，只保留最新的
                        self._clear_queue(stats_queue)

                        # 发送最新统计信息
                        try:
                            stats_queue.put_nowait({
                                'valid_fps': valid_fps,
                                'valid_frames': valid_frame_count,
                                'invalid_frames': invalid_frame_count,
                                'total_frames': total_frames
                            })
                        except:
                            pass

                        valid_frame_count = 0
                        invalid_frame_count = 0
                        last_time = current_time
                else:
                    # 没有数据时短暂休眠，避免CPU空转
                    time.sleep(0.001)

        except KeyboardInterrupt:
            logging.info("串口进程被中断")
        finally:
            if ser and ser.is_open:
                ser.close()
                logging.info("串口已关闭")

    @staticmethod
    def _clear_queue(queue: mp.Queue):
        """清空队列（丢弃旧数据）"""
        while not queue.empty():
            try:
                queue.get_nowait()
            except:
                break


def start_serial_reader_process(
    port: str,
    data_queue: mp.Queue,
    stats_queue: mp.Queue,
    stop_event: mp.Event,
    baudrate: int = 1000000
) -> mp.Process:
    """
    启动串口读取进程

    参数:
        port: 串口设备名
        data_queue: 矩阵数据队列
        stats_queue: 统计信息队列
        stop_event: 停止事件
        baudrate: 波特率，默认 1000000

    返回:
        进程对象

    示例:
        >>> import multiprocessing as mp
        >>> data_queue = mp.Queue(maxsize=10)
        >>> stats_queue = mp.Queue(maxsize=5)
        >>> stop_event = mp.Event()
        >>> proc = start_serial_reader_process('COM3', data_queue, stats_queue, stop_event)
        >>> proc.start()
    """
    reader = SerialReaderProcess(port, baudrate)
    proc = mp.Process(
        target=reader.run,
        args=(data_queue, stats_queue, stop_event),
        name="SerialReader"
    )
    return proc
