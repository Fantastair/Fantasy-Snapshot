from __future__ import annotations
from dataclasses import dataclass, field

import fantas

__all__ = (
    "FrameFunc",
    "run_framefuncs",
    "add_framefunc",
    "del_framefunc",
)

@dataclass(slots=True)
class FrameFunc:
    """
    帧函数类，用于在每一帧调用指定的函数。
    """
    ID    : int = field(default_factory=fantas.generate_unique_id, init=False)    # 唯一标识 ID

    func  : callable = field(compare=False)                          # 帧函数
    args  : tuple    = field(default=tuple(), compare=False)         # 位置参数
    kwargs: dict     = field(default_factory=dict, compare=False)    # 关键字参数

    def __call__(self):
        return self.func(*self.args, **self.kwargs)

    def bind(self, func: callable, /, *args, **kwargs):
        """
        绑定新的帧函数及其参数。

        Args:
            func (callable): 新的帧函数。
            args: 位置参数。
            kwargs: 关键字参数。
        """
        self.func   = func
        self.args   = args
        self.kwargs = kwargs

# 全局帧函数集合
framefunc_set = set()

def run_framefuncs():
    """
    运行所有已启动的帧函数。
    """
    for framefunc in tuple(framefunc_set):
        if framefunc():    # 如果帧函数返回 True，会自动停止该帧函数
            framefunc_set.discard(framefunc)

def add_framefunc(framefunc: callable):
    """
    添加一个新的帧函数并启动它。

    Args:
        framefunc (callable): 要添加的帧函数。
    """
    framefunc_set.add(framefunc)

def del_framefunc(framefunc: callable):
    """
    停止并删除一个帧函数。

    Args:
        framefunc (callable): 要删除的帧函数。
    """
    framefunc_set.discard(framefunc)
