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

    "KeyFrameBase",
    "AttrKeyFrame",
    "ColorKeyframe",
)

@dataclass(slots=True)
class FrameFunc:
    """
    帧函数类，用于在每一帧调用指定的函数。
    Args:
        func  : 帧函数。
        args  : 位置参数。
        kwargs: 关键字参数。
    """
    ID    : int = field(default_factory=fantas.generate_unique_id, init=False)    # 唯一标识 ID

    func  : Callable = field(default=None, compare=False)
    args  : tuple    = field(default=tuple(), compare=False)
    kwargs: dict     = field(default_factory=dict, compare=False)

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
class FrameTrigger:
    """
    帧触发器类，用于在指定的帧数后触发一个函数。
    Args:
        func        : 触发函数。
        total_frames: 总帧数。
    """

    func        : Callable = field(compare=False)
    total_frames: int      = field(default=0, compare=False)

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
            self.func()
            return True
        return False

get_time_ns = fantas.get_time_ns    # 提高访问速度

@dataclass(slots=True)
class TimeTrigger:
    """
    时间触发器类，用于在指定的时间后触发一个函数。
    Args:
        func       : 触发函数。
        target_time: 目标时间（纳秒）。
    """

    func       : Callable    = field(compare=False)
    target_time: int | float = field(compare=False)

    start_time  : int         = field(init=False, compare=False)    # 开始时间（纳秒）

    def start(self, restart: bool = True):
        """
        启动时间触发器。
        Args:
            restart (bool): 是否重新计时。如果为 True，则从当前时间开始计时；如果为 False，则继续之前的计时。
        """
        if restart or not self.is_started():
            self.start_time = get_time_ns()
        add_framefunc(self.tick)

    def stop(self):
        """
        停止时间触发器。
        """
        del_framefunc(self.tick)
    
    def is_started(self) -> bool:
        """
        检查时间触发器是否已启动。

        Returns:
            bool: 如果时间触发器已启动则返回 True，否则返回 False。
        """
        return self.tick in framefunc_set

    def tick(self) -> bool:
        """
        时间触发器的帧函数。

        Returns:
            bool: 如果触发器已完成则返回 True，否则返回 False。
        """
        if get_time_ns() - self.start_time >= self.target_time:
            self.func()
            return True
        return False

    def set_target_time_ns(self, target_time: int | float):
        """
        设置目标时间。

        Args:
            target_time (int | float): 目标时间（纳秒）。
        """
        self.target_time = target_time

    def set_target_time_us(self, target_time: int | float):
        """
        设置目标时间。

        Args:
            target_time (int | float): 目标时间（微秒）。
        """
        self.target_time = target_time * 1000

    def set_target_time_ms(self, target_time: int | float):
        """
        设置目标时间。

        Args:
            target_time (int | float): 目标时间（毫秒）。
        """
        self.target_time = target_time * 1_000_000

    def set_target_time_s(self, target_time: int | float):
        """
        设置目标时间。

        Args:
            target_time (int | float): 目标时间（秒）。
        """
        self.target_time = target_time * 1_000_000_000

@dataclass(slots=True)
class KeyFrameBase(TimeTrigger):
    """
    关键帧基类，用于在指定的时间内按比例调用一个函数。
    """

    def tick(self) -> bool:
        t = get_time_ns() - self.start_time
        ratio = t / self.target_time
        self(ratio)
        if t >= self.target_time:
            return True
        return False

lerp = fantas.math.lerp    # 提高访问速度

@dataclass(slots=True)
class AttrKeyFrame(KeyFrameBase):
    """
    属性关键帧类，用于修改对象的属性。
    Args:
        obj       : 目标对象。
        attr      : 目标属性名。
        end_value : 结束值。
        map_curve : 映射曲线。
    """

    func       : None  = field(default=None, init=False, compare=False)    # 覆盖父类的 func 属性，不使用它
    args       : None  = field(default=None, init=False, compare=False)    # 覆盖父类的 args 属性，不使用它
    kwargs     : None  = field(default=None, init=False, compare=False)    # 覆盖父类的 kwargs 属性，不使用它
    start_value: float = field(init=False, compare=False)                  # 起始值

    obj        : object           = field(compare=False)
    attr       : str              = field(compare=False)
    end_value  : float            = field(compare=False)
    map_curve  : fantas.CurveBase = field(compare=False, default=fantas.CURVE_LINEAR)

    def start(self, start_value: float = None, restart: bool = True):
        """
        启动属性关键帧。

        Args:
            start_value (float, optional): 起始值。如果为 None，则使用当前属性值作为起始值。
            restart (bool): 是否重新计时。如果为 True，则从当前时间开始计时；如果为 False，则继续之前的计时。
        """
        if start_value is None:
            self.start_value = getattr(self.obj, self.attr)
        else:
            self.start_value = start_value
        KeyFrameBase.start(self, restart)

    def __call__(self, ratio: float):
        """
        在指定的时间点修改对象的属性。

        Args:
            ratio (float): 当前时间点与总时间的比例。
        """
        setattr(self.obj, self.attr, lerp(self.start_value, self.end_value, self.map_curve(ratio), False))

@dataclass(slots=True)
class ColorKeyframe(AttrKeyFrame):
    """
    颜色关键帧类，用于修改对象的颜色属性。
    """

    def start(self, start_value = None):
        AttrKeyFrame.start(self, start_value)
        if not isinstance(self.start_value, fantas.Color):
            self.start_value = fantas.Color(self.start_value)

    def __call__(self, ratio: float):
        """
        在指定的时间点修改对象的颜色属性。

        Args:
            ratio (float): 当前时间点与总时间的比例。
        """
        setattr(self.obj, self.attr, self.start_value.lerp(self.end_value, self.map_curve(ratio)))
