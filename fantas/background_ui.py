from __future__ import annotations
from dataclasses import dataclass, field

import fantas

__all__ = (
    "ColorBackground",
)

@dataclass(slots=True)
class ColorBackground(fantas.UI):
    """ 纯色背景 UI 类 """
    father  : fantas.UI | None = None                                                # 指向父显示元素
    children: list[fantas.UI]  = field(default_factory=list)                         # 子显示元素列表
    ui_id   : fantas.UIID      = field(default_factory=fantas.generate_unique_id)    # 唯一标识 ID
    bgcolor : fantas.ColorLike = 'black'                                             # 背景颜色

    def __post_init__(self):
        """ 初始化 ColorBackground 实例 """
        self.color_fill_command = fantas.ColorFillCommand(
            creator = self,
            color   = self.bgcolor,
        )

    def set_bgcolor(self, color: fantas.ColorLike):
        """
        设置背景颜色
        Args:
            color (fantas.ColorLike): 新的背景颜色。
        """
        self.bgcolor = color
        self.color_fill_command.color = color

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        yield self.color_fill_command
        yield from fantas.UI.create_render_commands(self, offset)
