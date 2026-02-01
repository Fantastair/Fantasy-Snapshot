from __future__ import annotations
from dataclasses import dataclass, field
from collections.abc import Callable

import fantas

__all__ = (
    "FrameFunc",
    "run_framefuncs",
    "add_framefunc",
    "del_framefunc",

    "FrameTrigger",
    "TimeTrigger",
)

@dataclass(slots=True)
class FrameFunc:
    """
    帧函数类，用于在每一帧调用指定的函数。
    """
    ID    : int = field(default_factory=fantas.generate_unique_id, init=False)    # 唯一标识 ID

    func  : Callable = field(init=False, compare=False)                          # 帧函数
    args  : tuple    = field(init=False, default=tuple(), compare=False)         # 位置参数
    kwargs: dict     = field(init=False, default_factory=dict, compare=False)    # 关键字参数

    def __call__(self):
        return self.func(*self.args, **self.kwargs)

    def bind(self, func: Callable, /, *args, **kwargs):
        """
        绑定新的帧函数及其参数。

        Args:
            func (Callable): 新的帧函数。
            args: 位置参数。
            kwargs: 关键字参数。
        """
        self.func   = func
        self.args   = args
        self.kwargs = kwargs

# 全局帧函数集合
framefunc_set: set[Callable] = set()

def run_framefuncs():
    """
    运行所有已启动的帧函数。
    """
    for framefunc in tuple(framefunc_set):
        if framefunc():    # 如果帧函数返回 True，会自动停止该帧函数
            framefunc_set.discard(framefunc)

def add_framefunc(framefunc: Callable):
    """
    添加一个新的帧函数并启动它。

    Args:
        framefunc (Callable): 要添加的帧函数.
    """
    framefunc_set.add(framefunc)

def del_framefunc(framefunc: Callable):
    """
    停止并删除一个帧函数。

    Args:
        framefunc (Callable): 要删除的帧函数。
    """
    framefunc_set.discard(framefunc)

@dataclass(slots=True)
class FrameTrigger(FrameFunc):
    """
    帧触发器类，用于在指定的帧数后触发一个函数。
    """

    total_frames : int = field(default=0, compare=False)     # 总帧数
    current_frame: int = field(init=False, compare=False)    # 当前帧数

    def start(self):
        """
        启动帧触发器。
        """
        self.current_frame = 0
        add_framefunc(self.tick)

    def stop(self):
        """
        停止帧触发器。
        """
        del_framefunc(self.tick)

    def set_total_frames(self, total_frames: int):
        """
        设置总帧数。

        Args:
            total_frames (int): 总帧数。
        """
        self.total_frames = total_frames

    def tick(self) -> bool:
        """
        帧触发器的帧函数。

        Returns:
            bool: 如果触发器已完成则返回 True，否则返回 False。
        """
        self.current_frame += 1
        if self.current_frame >= self.total_frames:
            self()
            return True
        return False

class TimeTrigger(FrameFunc):
    """
    时间触发器类，用于在指定的时间后触发一个函数。
    """

    target_time : int = field(default=0, compare=False)     # 目标时间（纳秒）
    start_time  : int = field(init=False, compare=False)    # 开始时间（纳秒）

    def start(self):
        """
        启动时间触发器。
        """
        self.start_time = fantas.get_time_ns()
        add_framefunc(self.tick)

    def stop(self):
        """
        停止时间触发器。
        """
        del_framefunc(self.tick)

    def tick(self) -> bool:
        """
        时间触发器的帧函数。

        Returns:
            bool: 如果触发器已完成则返回 True，否则返回 False。
        """
        if fantas.get_time_ns() - self.start_time >= self.target_time:
            self()
            return True
        return False

    def set_target_time_ns(self, target_time: int):
        """
        设置目标时间。

        Args:
            target_time (int): 目标时间（纳秒）。
        """
        self.target_time = target_time

    def set_target_time_us(self, target_time: int):
        """
        设置目标时间。

        Args:
            target_time (int): 目标时间（微秒）。
        """
        self.target_time = target_time * 1000

    def set_target_time_ms(self, target_time: int):
        """
        设置目标时间。

        Args:
            target_time (int): 目标时间（毫秒）。
        """
        self.target_time = target_time * 1_000_000

    def set_target_time_s(self, target_time: int):
        """
        设置目标时间。

        Args:
            target_time (int): 目标时间（秒）。
        """
        self.target_time = target_time * 1_000_000_000
