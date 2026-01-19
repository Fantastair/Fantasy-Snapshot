from __future__ import annotations
from enum import Enum, auto

import pygame
import pygame.freetype
from pygame.locals import *

import fantas

__all__ = [
    "DEFAULTRECT",
    "DEFAULTFONT",
    "EventCategory",
    "event_category_dict",

    "WINDOWPOS_UNDEFINED",
    "WINDOWPOS_CENTERED",

    "MOUSEBUTTONDOWN",
    "MOUSEBUTTONUP",
    "MOUSEMOTION",
    "MOUSEWHEEL",
    "KEYDOWN",
    "KEYUP",
    "TEXTEDITING",
    "TEXTINPUT",
    "WINDOWSHOWN",
    "WINDOWHIDDEN",
    "WINDOWEXPOSED",
    "WINDOWMOVED",
    "WINDOWRESIZED",
    "WINDOWSIZECHANGED",
    "WINDOWMINIMIZED",
    "WINDOWMAXIMIZED",
    "WINDOWRESTORED",
    "WINDOWENTER",
    "WINDOWLEAVE",
    "WINDOWFOCUSGAINED",
    "WINDOWFOCUSLOST",
    "WINDOWCLOSE",
    "WINDOWTAKEFOCUS",
    "WINDOWHITTEST",
    "WINDOWICCPROFCHANGED",
    "WINDOWDISPLAYCHANGED",
]

DEFAULTRECT = pygame.Rect(0, 0, 0, 0)       # 默认矩形

DEFAULTFONT = pygame.freetype.Font(None)    # 默认字体
DEFAULTFONT.origin = True

# 自定义事件
# MOUSEBUTTONCLICKED = fantas.custom_event()    # 鼠标按钮点击事件
# MOUSEENTERED       = fantas.custom_event()    # 鼠标进入事件
# MOUSELEAVED        = fantas.custom_event()    # 鼠标离开事件

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
    WINDOWEXPOSED       : EventCategory.WINDOW,
    WINDOWMOVED         : EventCategory.WINDOW,
    WINDOWRESIZED       : EventCategory.WINDOW,
    WINDOWSIZECHANGED   : EventCategory.WINDOW,
    WINDOWMINIMIZED     : EventCategory.WINDOW,
    WINDOWMAXIMIZED     : EventCategory.WINDOW,
    WINDOWRESTORED      : EventCategory.WINDOW,
    WINDOWENTER         : EventCategory.WINDOW,
    WINDOWLEAVE         : EventCategory.WINDOW,
    WINDOWFOCUSGAINED   : EventCategory.WINDOW,
    WINDOWFOCUSLOST     : EventCategory.WINDOW,
    WINDOWCLOSE         : EventCategory.WINDOW,
    WINDOWTAKEFOCUS     : EventCategory.WINDOW,
    WINDOWHITTEST       : EventCategory.WINDOW,
    WINDOWICCPROFCHANGED: EventCategory.WINDOW,
    WINDOWDISPLAYCHANGED: EventCategory.WINDOW,
}
