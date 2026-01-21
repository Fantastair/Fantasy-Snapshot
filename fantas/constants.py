from __future__ import annotations
from enum import Enum, IntEnum, auto

import pygame
import pygame.freetype
from pygame.locals import *

import fantas

__all__ = [
    "DEFAULTRECT",
    "DEFAULTFONT",

    "Quadrant",
    "BoxMode",

    "WINDOWPOS_UNDEFINED",
    "WINDOWPOS_CENTERED",

    "EventCategory",
    "event_category_dict",
    "custom_event",
    "get_event_category",

    "MOUSEBUTTONDOWN",
    "MOUSEBUTTONUP",
    "MOUSEMOTION",
    "MOUSEWHEEL",
    "MOUSEENTERED",
    "MOUSELEAVED",
    "MOUSECLICKED",
    "KEYDOWN",
    "KEYUP",
    "TEXTEDITING",
    "TEXTINPUT",
    "WINDOWSHOWN",
    "WINDOWHIDDEN",
    "WINDOWMOVED",
    "WINDOWRESIZED",
    "WINDOWMINIMIZED",
    "WINDOWMAXIMIZED",
    "WINDOWRESTORED",
    "WINDOWLEAVE",
    "WINDOWFOCUSGAINED",
    "WINDOWFOCUSLOST",
    "WINDOWCLOSE",
    "WINDOWDISPLAYCHANGED",
]

DEFAULTRECT = pygame.Rect(0, 0, 0, 0)       # 默认矩形

DEFAULTFONT = pygame.freetype.Font(None)    # 默认字体
DEFAULTFONT.origin = True

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
    注意，fantas 默认禁用不需要的事件，创建自定义事件后需要手动启用该事件类型才能接收此事件。
    Args:
        event_category (fantas.EventCategory): 事件分类，默认为 USER。
    Returns:
        fantas.EventType: 自定义事件类型 id。
    """
    t = fantas.event.custom_type()
    event_category_dict[t] = event_category
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
MOUSEENTERED = custom_event(EventCategory.MOUSE)    # 鼠标进入事件
MOUSELEAVED  = custom_event(EventCategory.MOUSE)    # 鼠标离开事件
MOUSECLICKED = custom_event(EventCategory.MOUSE)    # 有效单击事件
