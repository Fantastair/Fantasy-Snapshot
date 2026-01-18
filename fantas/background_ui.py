from __future__ import annotations
from dataclasses import dataclass

import fantas

__all__ = (
    "ColorBackground",
)

@dataclass(slots=True)
class ColorBackground(fantas.UI):
    """ 纯色背景 UI 类 """
    color: fantas.ColorLike = 'black'    # 背景颜色

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        yield fantas.ColorFillCommand(
            creator=self,
            color=self.color,
        )
        yield from fantas.UI.create_render_commands(self, offset)
