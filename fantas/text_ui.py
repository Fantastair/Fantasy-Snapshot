from __future__ import annotations
from dataclasses import dataclass, field

import fantas

__all__ = (
    "TextLine",
)

@dataclass(slots=True)
class TextLine(fantas.UI):
    """ 纯色单行文本 UI 类 """
    father  : fantas.UI | None   = field(default=None, init=False, repr=False)                     # 指向父显示元素
    children: None               = field(default=None, init=False, repr=False)                     # 纯色文本不包含子元素
    ui_id   : fantas.UIID        = field(default_factory=fantas.generate_unique_id, init=False)    # 唯一标识 ID
    text    : str                = 'text'                                                          # 显示的文本内容
    font    : fantas.Font        = fantas.DEFAULTFONT                                              # 使用的字体
    fgcolor : fantas.ColorLike   = 'black'                                                         # 文本颜色
    size    : float              = 16.0                                                            # 字体大小
    origin  : fantas.Point       = (0, 0)                                                          # 定位原点
    command : fantas.ColorTextLineRenderCommand = field(init=False, repr=False)                    # 文字渲染命令对象

    def __post_init__(self):
        """ 初始化 ColorTextLine 实例 """
        self.command = fantas.ColorTextLineRenderCommand(creator=self)

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        # 简化引用
        rc = self.command
        # 设置文本内容
        rc.text = self.text
        # 设置字体
        rc.font = self.font
        # 设置字体大小
        rc.size = self.size
        # 设置文本颜色
        rc.fgcolor = self.fgcolor
        # 设置文本原点
        rc.origin = (self.origin[0] + offset[0], self.origin[1] + offset[1])
        # 生成渲染命令
        yield rc