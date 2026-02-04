from __future__ import annotations
from dataclasses import dataclass
from copy import copy

import fantas

__all__ = (
    "TextStyle",
    "LabelStyle",

    "set_default_text_style",
    "set_default_label_style",
)

@dataclass(slots=True)
class TextStyle:
    """
    文本样式类。
    Args:
        font        : 字体
        size        : 字体大小
        fgcolor     : 文本颜色
        style_flag  : 文本风格标志
        line_spacing: 行间距
    """
    font : fantas.Font                = fantas.DEFAULTFONT
    size : float                      = 16.0
    fgcolor : fantas.ColorLike        = 'black'
    style_flag : fantas.TextStyleFlag = fantas.TEXTSTYLEFLAG_DEFAULT
    line_spacing: float               = 4.0

    def copy(self) -> TextStyle:
        """ 创建并返回当前 TextStyle 实例的副本 """
        return copy(self)

fantas.DEFAULTTEXTSTYLE = TextStyle()    # 初始化默认文本样式

def set_default_text_style(font: fantas.Font = None, size: float = None, fgcolor: fantas.ColorLike = None, style_flag: fantas.TextStyleFlag = None) -> None:
    """
    设置默认文本样式。
    Args:
        font       (fantas.Font)         : 字体。
        size       (float)               : 字体大小。
        fgcolor    (fantas.ColorLike)    : 文本颜色。
        style_flag (fantas.TextStyleFlag): 文本风格标志。
    """
    if font is not None:
        fantas.DEFAULTTEXTSTYLE.font = font
    if size is not None:
        fantas.DEFAULTTEXTSTYLE.size = size
    if fgcolor is not None:
        fantas.DEFAULTTEXTSTYLE.fgcolor = fgcolor
    if style_flag is not None:
        fantas.DEFAULTTEXTSTYLE.style_flag = style_flag

@dataclass(slots=True)
class LabelStyle:
    """ 
    Label 样式类。
    Attributes:
        bgcolor      : 背景颜色（填充，None 表示无背景填充）
        fgcolor      : 前景颜色（边框）
        border_radius: 边框圆角半径，0 表示直角
        border_width : 边框宽度
        quadrant     : 圆角象限掩码
    """
    bgcolor: fantas.ColorLike | None = 'black'
    fgcolor: fantas.ColorLike        = 'white'
    border_radius: int | float       = 0
    border_width : int | float       = 0
    quadrant: fantas.QuadrantMask    = fantas.Quadrant.ALL

    def copy(self) -> LabelStyle:
        """ 创建并返回当前 LabelStyle 实例的副本 """
        return copy(self)

fantas.DEFAULTLABELSTYLE = LabelStyle()    # 初始化默认 Label 样式

def set_default_label_style(bgcolor: fantas.ColorLike | None = None, fgcolor: fantas.ColorLike = None, border_radius: int | float = None, border_width: int = None, quadrant: fantas.QuadrantMask = None) -> None:
    """
    设置默认 Label 样式。
    Args:
        bgcolor      (fantas.ColorLike | None): 背景颜色（填充，None 表示无背景填充）。
        fgcolor      (fantas.ColorLike)       : 前景颜色（边框）。
        border_radius(int | float)            : 边框圆角半径，0 表示直角。
        border_width (int)                    : 边框宽度。
        quadrant     (fantas.QuadrantMask)    : 圆角象限掩码。
    """
    if bgcolor is not None:
        fantas.DEFAULTLABELSTYLE.bgcolor = bgcolor
    if fgcolor is not None:
        fantas.DEFAULTLABELSTYLE.fgcolor = fgcolor
    if border_radius is not None:
        fantas.DEFAULTLABELSTYLE.border_radius = border_radius
    if border_width is not None:
        fantas.DEFAULTLABELSTYLE.border_width = border_width
    if quadrant is not None:
        fantas.DEFAULTLABELSTYLE.quadrant = quadrant
