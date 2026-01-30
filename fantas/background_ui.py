from __future__ import annotations
from dataclasses import dataclass, field

import fantas

__all__ = (
    "ColorBackground",
)

@dataclass(slots=True)
class ColorBackground(fantas.UI):
    """ 纯色背景 UI 类 """
    bgcolor : fantas.ColorLike = 'black'                                                         # 背景颜色
    command : fantas.ColorBackgroundFillCommand = field(init=False, repr=False)                  # 颜色填充命令

    def __post_init__(self):
        """ 初始化 ColorBackground 实例 """
        self.command = fantas.ColorBackgroundFillCommand(creator = self)

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        # 设置背景颜色
        self.command.color = self.bgcolor
        # 生成自己的渲染命令
        yield self.command
        # 生成子元素的渲染命令
        yield from fantas.UI.create_render_commands(self)
