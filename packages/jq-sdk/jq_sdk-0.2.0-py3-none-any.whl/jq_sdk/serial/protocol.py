"""
串口协议定义和数据帧解析

协议格式:
- 帧尾标识: 0xAA 0x55 0x03 0x99 (十进制: 170, 85, 3, 153)
- 数据长度: 1024 字节 (32x32 原始数据)
- 帧结构: [数据 1024B] [帧尾 4B] [数据 1024B] [帧尾 4B] ...
"""

import numpy as np
from typing import List, Optional, Tuple


# 帧尾标识符常量
FRAME_TAIL = np.array([170, 85, 3, 153], dtype=np.uint8)
FRAME_TAIL_SIZE = 4
FRAME_DATA_SIZE = 1024


def find_frame_tail(data: np.ndarray) -> List[int]:
    """
    查找帧尾标识符 0xAA 0x55 0x03 0x99 的位置

    参数:
        data: 字节数据数组 (numpy uint8)

    返回:
        positions: 帧尾位置列表（每个位置指向帧尾的起始字节）

    示例:
        >>> import numpy as np
        >>> data = np.array([1, 2, 170, 85, 3, 153, 5, 6], dtype=np.uint8)
        >>> positions = find_frame_tail(data)
        >>> positions
        [2]
    """
    positions = []
    data_len = len(data)

    # 需要至少 4 个字节才能匹配帧尾
    if data_len < 4:
        return positions

    # 查找所有匹配的位置
    for i in range(data_len - 3):
        if (data[i] == 170 and data[i+1] == 85 and
            data[i+2] == 3 and data[i+3] == 153):
            positions.append(i)

    return positions


class FrameBuffer:
    """
    帧缓冲区管理类

    用于管理串口接收的字节流，处理粘包和半包问题。

    属性:
        buffer: 缓冲区数据
        max_buffer_size: 最大缓冲区大小（字节）
    """

    def __init__(self, max_buffer_size: int = 10000):
        """
        初始化帧缓冲区

        参数:
            max_buffer_size: 最大缓冲区大小（字节），超过此大小会自动清理
        """
        self.buffer = np.array([], dtype=np.uint8)
        self.max_buffer_size = max_buffer_size

    def append(self, data: np.ndarray):
        """
        向缓冲区追加数据

        参数:
            data: 新接收的字节数据
        """
        self.buffer = np.concatenate([self.buffer, data])

    def extract_frame(self) -> Tuple[Optional[np.ndarray], bool]:
        """
        从缓冲区提取一个完整的数据帧

        返回:
            (frame_data, success):
                - frame_data: 提取的帧数据 (1024字节)，失败时返回 None
                - success: 是否成功提取

        提取逻辑:
            1. 查找至少两个帧尾标识
            2. 提取两个帧尾之间的数据
            3. 验证数据长度是否为 1024 字节
            4. 移除已处理的数据，保留第二个帧尾作为下一帧的起始
        """
        # 查找帧尾标识符
        tail_positions = find_frame_tail(self.buffer)

        # 需要至少2个帧尾才能提取一帧数据
        if len(tail_positions) < 2:
            return None, False

        # 第一个帧尾位置
        first_tail = tail_positions[0]
        # 第二个帧尾位置
        second_tail = tail_positions[1]

        # 提取两个帧尾之间的数据（不包括第一个帧尾，不包括第二个帧尾）
        frame_start = first_tail + FRAME_TAIL_SIZE  # 跳过第一个帧尾（4字节）
        frame_end = second_tail                      # 到第二个帧尾之前
        frame_data = self.buffer[frame_start:frame_end]

        # 检查数据长度
        if len(frame_data) != FRAME_DATA_SIZE:
            # 无效帧，移除第一个帧尾，继续查找
            self.buffer = self.buffer[first_tail + FRAME_TAIL_SIZE:]
            return None, False

        # 移除已处理的数据（到第二个帧尾之前，保留第二个帧尾作为下一帧的第一个帧尾）
        self.buffer = self.buffer[second_tail:]

        return frame_data, True

    def clear_excess(self):
        """
        清理过大的缓冲区

        如果缓冲区超过最大大小，保留最后一部分数据
        """
        if len(self.buffer) > self.max_buffer_size:
            # 保留最后一半数据
            keep_size = self.max_buffer_size // 2
            self.buffer = self.buffer[-keep_size:]

    def size(self) -> int:
        """返回当前缓冲区大小"""
        return len(self.buffer)

    def clear(self):
        """清空缓冲区"""
        self.buffer = np.array([], dtype=np.uint8)


def validate_frame(frame_data: np.ndarray) -> bool:
    """
    验证帧数据的有效性

    参数:
        frame_data: 帧数据

    返回:
        是否有效
    """
    return len(frame_data) == FRAME_DATA_SIZE
