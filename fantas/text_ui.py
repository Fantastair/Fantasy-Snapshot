from __future__ import annotations
from dataclasses import dataclass, field

import fantas

__all__ = (
    "ColorTextLine",
)

@dataclass(slots=True)
class ColorTextLine(fantas.UI):
    """ 纯色单行文本 UI 类 """
    children: None = None                     # 纯色文本不包含子元素
    text: str = 'text'                        # 显示的文本内容
    font: fantas.Font = fantas.DEFAULTFONT    # 使用的字体
    color: fantas.ColorLike = 'black'         # 文本颜色
    size: float = 16.0                        # 字体大小
    rect: fantas.RectLike = field(default_factory=lambda: fantas.DEFAULTRECT)    # 定位矩形

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        yield fantas.ColorTextLineRenderCommand(
            creator=self,
            text=self.text,
            font=self.font,
            size=self.size,
            fgcolor=self.color,
            dest_rect=self.rect.move((offset[0], offset[1] + self.font.get_sized_ascender(self.size))),
        )
