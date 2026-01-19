from __future__ import annotations
from dataclasses import dataclass, field

import fantas

__all__ = (
    "ColorLabel",
)

@dataclass(slots=True)
class ColorLabel(fantas.UI):
    """ 纯色矩形 UI 类 """
    father  : fantas.UI | None = None                                                         # 指向父显示元素
    children: list[fantas.UI]  = field(default_factory=list)                                  # 子显示元素列表
    ui_id   : fantas.UIID      = field(default_factory=fantas.generate_unique_id)             # 唯一标识 ID
    bgcolor : fantas.ColorLike = 'black'                                                      # 矩形颜色
    rect    : fantas.RectLike  = field(default_factory=lambda: fantas.Rect(0, 0, 100, 50))    # 矩形区域

    def __post_init__(self):
        """ 初始化 ColorLabel 实例 """
        self.color_fill_command = fantas.ColorFillCommand(
            creator = self,
            color   = self.bgcolor,
        )
    
    def set_bgcolor(self, color: fantas.ColorLike):
        """
        设置矩形颜色
        Args:
            color (fantas.ColorLike): 新的矩形颜色。
        """
        self.bgcolor = color
        self.color_fill_command.color = color
    
    def set_rect(self, rect: fantas.RectLike):
        """
        设置矩形区域
        Args:
            rect (fantas.RectLike): 新的矩形区域。
        """
        self.rect.update(rect)

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        rect = self.rect.move(offset)
        self.color_fill_command.dest_rect = rect
        yield self.color_fill_command
        yield from fantas.UI.create_render_commands(self, rect.topleft)
