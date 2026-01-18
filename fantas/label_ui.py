from __future__ import annotations
from dataclasses import dataclass, field

import fantas

__all__ = (
    "ColorLabel",
)

@dataclass(slots=True)
class ColorLabel(fantas.UI):
    """ 纯色矩形 UI 类 """
    color: fantas.ColorLike = 'black'    # 矩形颜色
    rect: fantas.RectLike = field(default_factory=lambda: fantas.Rect(0, 0, 100, 50))    # 矩形区域

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        rect = self.rect.move(offset)
        yield fantas.ColorFillCommand(
            creator=self,
            color=self.color,
            dest_rect=rect,
        )
        yield from fantas.UI.create_render_commands(self, rect.topleft)
