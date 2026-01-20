from __future__ import annotations
from dataclasses import dataclass, field

import fantas

__all__ = (
    "ColorBackground",
)

@dataclass(slots=True)
class ColorBackground(fantas.UI):
    """ 纯色背景 UI 类 """
    father  : fantas.UI | None = field(default=None, init=False, repr=False)                     # 指向父显示元素
    children: list[fantas.UI]  = field(default_factory=list, init=False, repr=False)             # 子显示元素列表
    ui_id   : fantas.UIID      = field(default_factory=fantas.generate_unique_id, init=False)    # 唯一标识 ID
    bgcolor : fantas.ColorLike = 'black'                                                         # 背景颜色
    color_fill_command: fantas.ColorFillCommand = field(init=False, repr=False)                  # 颜色填充命令

    def __post_init__(self):
        """ 初始化 ColorBackground 实例 """
        self.color_fill_command = fantas.ColorFillCommand(creator = self)

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        # 设置背景颜色
        self.color_fill_command.color = self.bgcolor
        # 生成自己的渲染命令
        yield self.color_fill_command
        # 生成子元素的渲染命令
        yield from fantas.UI.create_render_commands(self, offset)
