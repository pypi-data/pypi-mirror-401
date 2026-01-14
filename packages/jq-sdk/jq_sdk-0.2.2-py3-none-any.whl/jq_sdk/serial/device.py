"""
串口设备发现和管理
"""

import serial.tools.list_ports
from typing import List, Optional, NamedTuple
import logging


class PortInfo(NamedTuple):
    """
    串口信息数据类

    属性:
        device: 串口设备名（如 'COM3', '/dev/ttyUSB0'）
        description: 设备描述
        hwid: 硬件ID
    """
    device: str
    description: str
    hwid: str


def list_serial_ports() -> List[PortInfo]:
    """
    列出所有可用的串口设备

    返回:
        串口信息列表

    示例:
        >>> ports = list_serial_ports()
        >>> for port in ports:
        ...     print(f"{port.device}: {port.description}")
    """
    available_ports = list(serial.tools.list_ports.comports())

    port_list = []
    for port in available_ports:
        port_list.append(PortInfo(
            device=port.device,
            description=port.description,
            hwid=port.hwid
        ))

    return port_list


def select_port_interactive() -> Optional[str]:
    """
    交互式选择串口

    在终端显示可用串口列表，让用户选择

    返回:
        选中的串口设备名，如果没有可用串口或选择无效则返回 None

    示例:
        >>> port = select_port_interactive()
        可用的串口设备:
        [0] COM3 - USB Serial Port (COM3)
        [1] COM5 - Arduino Uno (COM5)
        请选择串口编号: 0
        >>> print(port)
        COM3
    """
    available_ports = list(serial.tools.list_ports.comports())

    if not available_ports:
        logging.error('未找到可用的串口设备')
        return None

    print("可用的串口设备:")
    for i, port in enumerate(available_ports):
        print(f"[{i}] {port.device} - {port.description}")

    try:
        choice = int(input("请选择串口编号: "))
        if 0 <= choice < len(available_ports):
            selected_port = available_ports[choice].device
            logging.info(f'已选择串口: {selected_port}')
            return selected_port
        else:
            logging.error("无效的选择")
            return None
    except ValueError:
        logging.error("请输入有效的数字")
        return None
    except (KeyboardInterrupt, EOFError):
        logging.info("用户取消选择")
        return None


def find_port_by_description(keyword: str) -> Optional[str]:
    """
    根据描述关键字查找串口

    参数:
        keyword: 描述关键字（不区分大小写）

    返回:
        匹配的串口设备名，未找到返回 None

    示例:
        >>> port = find_port_by_description('Arduino')
        >>> print(port)
        COM5
    """
    ports = list_serial_ports()

    for port in ports:
        if keyword.lower() in port.description.lower():
            logging.info(f'找到匹配的串口: {port.device} - {port.description}')
            return port.device

    logging.warning(f'未找到包含关键字 "{keyword}" 的串口')
    return None


def is_port_available(port_name: str) -> bool:
    """
    检查指定串口是否可用

    参数:
        port_name: 串口设备名

    返回:
        是否可用

    示例:
        >>> is_port_available('COM3')
        True
        >>> is_port_available('COM99')
        False
    """
    ports = list_serial_ports()
    return any(port.device == port_name for port in ports)
