"""
串口通信模块

提供串口设备发现、协议解析和数据读取功能。
"""

from .device import (
    list_serial_ports,
    select_port_interactive,
    find_port_by_description,
    is_port_available,
    PortInfo,
)
from .protocol import (
    find_frame_tail,
    validate_frame,
    FrameBuffer,
    FRAME_TAIL,
    FRAME_TAIL_SIZE,
    FRAME_DATA_SIZE,
)
from .comm import (
    SerialReader,
    SerialReaderProcess,
    start_serial_reader_process,
)

__all__ = [
    # 设备发现
    'list_serial_ports',
    'select_port_interactive',
    'find_port_by_description',
    'is_port_available',
    'PortInfo',
    # 协议
    'find_frame_tail',
    'validate_frame',
    'FrameBuffer',
    'FRAME_TAIL',
    'FRAME_TAIL_SIZE',
    'FRAME_DATA_SIZE',
    # 通信
    'SerialReader',
    'SerialReaderProcess',
    'start_serial_reader_process',
]
