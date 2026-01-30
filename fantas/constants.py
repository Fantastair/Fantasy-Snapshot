from __future__ import annotations
from enum import Enum, IntEnum, auto

import pygame
import pygame.freetype
from pygame.freetype import\
    STYLE_DEFAULT   as TEXTSTYLEFLAG_DEFAULT,\
    STYLE_NORMAL    as TEXTSTYLEFLAG_NORMAL,\
    STYLE_STRONG    as TEXTSTYLEFLAG_STRONG,\
    STYLE_OBLIQUE   as TEXTSTYLEFLAG_OBLIQUE,\
    STYLE_UNDERLINE as TEXTSTYLEFLAG_UNDERLINE,\
    STYLE_WIDE      as TEXTSTYLEFLAG_WIDE
from pygame.locals import *

import fantas

__all__ = [
    "DEFAULTRECT",
    "DEFAULTFONT",
    "DEFAULTTEXTSTYLE",

    "Quadrant",
    "BoxMode",
    "FillMode",
    "AlignMode",

    "WINDOWPOS_UNDEFINED",
    "WINDOWPOS_CENTERED",

    "EventCategory",
    "event_category_dict",
    "custom_event",
    "get_event_category",

    "MOUSEWHEEL",
    "MOUSEMOTION",
    "MOUSEBUTTONUP",
    "MOUSEBUTTONDOWN",
    "MOUSELEAVED",
    "MOUSEENTERED",
    "MOUSECLICKED",
    "KEYUP",
    "KEYDOWN",
    "TEXTINPUT",
    "WINDOWCLOSE",
    "TEXTEDITING",
    "WINDOWLEAVE",
    "WINDOWSHOWN",
    "WINDOWMOVED",
    "WINDOWHIDDEN",
    "WINDOWRESIZED",
    "WINDOWRESTORED",
    "WINDOWMINIMIZED",
    "WINDOWMAXIMIZED",
    "WINDOWFOCUSLOST",
    "WINDOWFOCUSGAINED",
    "WINDOWDISPLAYCHANGED",
    "DEBUGRECEIVED",

    "BUTTON_X1",
    "BUTTON_X2",
    "BUTTON_LEFT",
    "BUTTON_RIGHT",
    "BUTTON_MIDDLE",
    "BUTTON_WHEELUP",
    "BUTTON_WHEELDOWN",

    "TEXTSTYLEFLAG_DEFAULT",
    "TEXTSTYLEFLAG_NORMAL",
    "TEXTSTYLEFLAG_STRONG",
    "TEXTSTYLEFLAG_OBLIQUE",
    "TEXTSTYLEFLAG_UNDERLINE",
    "TEXTSTYLEFLAG_WIDE",
]

DEFAULTRECT = pygame.Rect(0, 0, 0, 0)       # 默认矩形

DEFAULTFONT = pygame.freetype.Font(None)    # 默认字体
DEFAULTFONT.origin = True
DEFAULTFONT.kerning = True

DEFAULTTEXTSTYLE: fantas.TextStyle = None    # 默认文本样式，占位符，在 fantas.font 模块中初始化

class Quadrant(IntEnum):
    """
    象限枚举。
    低 2 位用于快速符号计算，高 4 位作为单比特掩码。
    """
    TOPRIGHT    = 0b000101    # 第一象限
    TOPLEFT     = 0b001000    # 第二象限
    BOTTOMLEFT  = 0b010010    # 第三象限
    BOTTOMRIGHT = 0b100011    # 第四象限

class BoxMode(Enum):
    """ 盒子模式枚举，用来控制边框的扩展方向。 """
    INSIDE     = auto()    # 内部盒子，表示边框只会向内部扩展
    OUTSIDE    = auto()    # 外部盒子，表示边框只会向外部扩展
    INOUTSIDE  = auto()    # 中间盒子，表示边框会向内部和外部同时扩展

class FillMode(Enum):
    """ Surface 填充模式枚举。 """
    IGNORE = auto()          # 忽略填充模式，只对齐 topleft，不关心 size
    SCALE  = auto()          # 缩放填充模式，对齐 topleft 并缩放图片至目标 size
    SMOOTHSCALE  = auto()    # 平滑缩放填充模式，对齐 topleft 并平滑缩放图片至目标 size
    REPEAT = auto()          # 重复填充模式，对齐 topleft 并重复平铺图片至目标 size
    FITMIN = auto()          # 最小适应填充模式，等比缩放图片，确保图片完整显示在目标 rect 内（可能留有空白）
    FITMAX = auto()          # 最大适应填充模式，等比缩放图片，确保图片覆盖整个目标 rect（超出部分将被裁剪）

class AlignMode(Enum):
    """ 文本对齐模式枚举。 """
    LEFT      = auto()    # 左对齐
    CENTER    = auto()    # 居中对齐
    RIGHT     = auto()    # 右对齐
    LEFTRIGHT = auto()    # 左右对齐（两端对齐）

class EventCategory(Enum):
    """ 事件分类枚举。 """
    MOUSE    = auto()    # 鼠标事件
    KEYBOARD = auto()    # 键盘事件
    INPUT    = auto()    # 输入事件
    WINDOW   = auto()    # 窗口事件
    USER     = auto()    # 用户自定义事件
    NONE     = auto()    # 未分类事件

# 事件分类表
event_category_dict: dict[fantas.EventType, EventCategory] = {
    MOUSEBUTTONDOWN: EventCategory.MOUSE,
    MOUSEBUTTONUP  : EventCategory.MOUSE,
    MOUSEMOTION    : EventCategory.MOUSE,
    MOUSEWHEEL     : EventCategory.MOUSE,

    KEYDOWN: EventCategory.KEYBOARD,
    KEYUP  : EventCategory.KEYBOARD,

    TEXTEDITING: EventCategory.INPUT,
    TEXTINPUT  : EventCategory.INPUT,

    WINDOWSHOWN         : EventCategory.WINDOW,
    WINDOWHIDDEN        : EventCategory.WINDOW,
    WINDOWMOVED         : EventCategory.WINDOW,
    WINDOWRESIZED       : EventCategory.WINDOW,
    WINDOWMINIMIZED     : EventCategory.WINDOW,
    WINDOWMAXIMIZED     : EventCategory.WINDOW,
    WINDOWRESTORED      : EventCategory.WINDOW,
    WINDOWLEAVE         : EventCategory.WINDOW,
    WINDOWFOCUSGAINED   : EventCategory.WINDOW,
    WINDOWFOCUSLOST     : EventCategory.WINDOW,
    WINDOWCLOSE         : EventCategory.WINDOW,
    WINDOWDISPLAYCHANGED: EventCategory.WINDOW,
}

def custom_event(event_category: EventCategory = EventCategory.USER) -> fantas.EventType:
    """
    生成一个自定义事件类型 id。
    Args:
        event_category (fantas.EventCategory): 事件分类，默认为 USER。
    Returns:
        fantas.EventType: 自定义事件类型 id。
    """
    t = fantas.event.custom_type()
    event_category_dict[t] = event_category
    fantas.event.set_allowed(t)
    return t

def get_event_category(event_type: fantas.EventType) -> EventCategory:
    """
    获取事件分类。
    Args:
        event_type (fantas.EventType): 事件类型。
    Returns:
        fantas.EventCategory: 事件分类枚举值。
    """
    return event_category_dict.get(event_type, EventCategory.NONE)

# 自定义事件
MOUSEENTERED  = custom_event(EventCategory.MOUSE)    # 鼠标进入事件
MOUSELEAVED   = custom_event(EventCategory.MOUSE)    # 鼠标离开事件
MOUSECLICKED  = custom_event(EventCategory.MOUSE)    # 有效单击事件
DEBUGRECEIVED = custom_event()                       # 接收到调试信息事件
CALLREQUEST   = custom_event()                       # 调用请求事件
