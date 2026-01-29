from __future__ import annotations
from dataclasses import dataclass, field

import fantas

__all__ = (
    "TextLine",
    "Text",
)

@dataclass(slots=True)
class TextLine(fantas.UI):
    """ 纯色单行文本 UI 类 """
    father  : fantas.UI | None   = field(default=None, init=False, repr=False)                     # 指向父显示元素
    children: None               = field(default=None, init=False, repr=False)                     # 纯色文本不包含子元素
    ui_id   : fantas.UIID        = field(default_factory=fantas.generate_unique_id, init=False)    # 唯一标识 ID

    text    : str                = 'text'                                     # 显示的文本内容
    style   : fantas.TextStyle   = field(default_factory=fantas.TextStyle)    # 文本样式
    origin  : fantas.Point       = (0, 0)                                     # 定位原点
    command : fantas.TextLineRenderCommand = field(init=False, repr=False)    # 文字渲染命令对象

    def __post_init__(self):
        """ 初始化 ColorTextLine 实例 """
        self.command = fantas.TextLineRenderCommand(creator=self)

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表。
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        # 简化引用
        rc = self.command
        # 设置文本内容
        rc.text = self.text
        # 设置文本样式
        rc.style = self.style
        # 设置文本原点
        rc.origin = (self.origin[0] + offset[0], self.origin[1] + offset[1])
        # 生成渲染命令
        yield rc

@dataclass(slots=True)
class Text(fantas.UI):
    """ 纯色多行文本 UI 类 """
    father  : fantas.UI | None   = field(default=None, init=False, repr=False)                     # 指向父显示元素
    children: None               = field(default=None, init=False, repr=False)                     # 纯色文本不包含子元素
    ui_id   : fantas.UIID        = field(default_factory=fantas.generate_unique_id, init=False)    # 唯一标识 ID

    text    : str                = 'text'                                                      # 显示的文本内容
    style   : fantas.TextStyle   = field(default_factory=fantas.TextStyle)                     # 文本样式
    line_spacing: float          = 4.0                                                         # 行间距
    rect    : fantas.RectLike    = field(default_factory=lambda: fantas.Rect(0, 0, 100, 0))    # 文本显示区域
    align_mode: fantas.AlignMode = fantas.AlignMode.LEFT                                       # 对齐模式

    command : fantas.TextRenderCommand = field(init=False, repr=False)    # 渲染命令

    def __post_init__(self):
        """ 初始化 ColorText 实例 """
        self.command = fantas.TextRenderCommand(creator=self)
    
    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表。
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象.
        """
        # 仅当文本非空时才生成渲染命令
        if not self.text:
            return
        # 简化引用
        rc = self.command
        # 设置文本内容
        rc.text = self.text
        # 设置文本样式
        rc.style = self.style
        # 设置行间距
        rc.line_spacing = self.line_spacing
        # 设置文本显示区域
        if isinstance(self.rect, fantas.Rect):
            rc.rect = fantas.IntRect(self.rect).move(offset)
        else:
            rc.rect = self.rect.move(offset)
        # 设置对齐模式
        rc.align_mode = self.align_mode
        # 生成渲染命令
        yield rc
