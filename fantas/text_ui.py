from __future__ import annotations
from dataclasses import dataclass, field

import fantas

__all__ = (
    "ColorTextLine",
)

@dataclass(slots=True)
class ColorTextLine(fantas.UI):
    """ 纯色单行文本 UI 类 """
    father  : fantas.UI | None = None                                                 # 指向父显示元素
    children: None             = None                                                 # 纯色文本不包含子元素
    ui_id   : fantas.UIID      = field(default_factory=fantas.generate_unique_id)     # 唯一标识 ID
    text    : str              = 'text'                                               # 显示的文本内容
    font    : fantas.Font      = fantas.DEFAULTFONT                                   # 使用的字体
    fgcolor   : fantas.ColorLike = 'black'                                            # 文本颜色
    size    : float            = 16.0                                                 # 字体大小
    rect    : fantas.RectLike  = field(default_factory=lambda: fantas.DEFAULTRECT)    # 定位矩形
    color_text_line_render_command: fantas.ColorTextLineRenderCommand = field(init=False)    # 文字渲染命令对象

    def __post_init__(self):
        """ 初始化 ColorTextLine 实例 """
        self.color_text_line_render_command = fantas.ColorTextLineRenderCommand(
            creator   = self,
            text      = self.text,
            font      = self.font,
            size      = self.size,
            fgcolor   = self.fgcolor,
            dest_rect = self.rect,
        )
    
    def set_text(self, text: str):
        """
        设置文本内容
        Args:
            text (str): 新的文本内容。
        """
        self.text = text
        self.color_text_line_render_command.text = text
    
    def set_font(self, font: fantas.Font):
        """
        设置字体
        Args:
            font (fantas.Font): 新的字体对象。
        """
        self.font = font
        self.color_text_line_render_command.font = font
    
    def set_fgcolor(self, fgcolor: fantas.ColorLike):
        """
        设置文本颜色
        Args:
            fgcolor (fantas.ColorLike): 新的文本颜色。
        """
        self.fgcolor = fgcolor
        self.color_text_line_render_command.fgcolor = fgcolor
    
    def set_size(self, size: float):
        """
        设置字体大小
        Args:
            size (float): 新的字体大小。
        """
        self.size = size
        self.color_text_line_render_command.size = size
    
    def set_rect(self, rect: fantas.RectLike):
        """
        设置定位矩形
        Args:
            rect (fantas.RectLike): 新的定位矩形。
        """
        self.rect = fantas.Rect(rect)

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        self.color_text_line_render_command.dest_rect = self.rect.move((offset[0], offset[1] + self.font.get_sized_ascender(self.size)))
        yield self.color_text_line_render_command
