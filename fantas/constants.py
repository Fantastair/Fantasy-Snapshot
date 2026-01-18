from enum import Enum, auto

import pygame
import pygame.freetype
from pygame.locals import *

DEFAULTRECT = pygame.Rect(0, 0, 0, 0)       # 默认矩形

DEFAULTFONT = pygame.freetype.Font(None)    # 默认字体
DEFAULTFONT.origin = True

# 先禁用所有事件，然后再根据需要启用特定事件
pygame.event.set_blocked(None)

def custom_event() -> int:
    """
    生成一个自定义事件类型 id。
    Returns:
        int: 自定义事件类型的整数值。
    """
    t = pygame.event.custom_type()
    event_category_dict[t] = EventCategory.USER
    pygame.event.set_allowed(t)
    return t
# 自定义事件
# MOUSEBUTTONCLICKED = custom_event()    # 鼠标按钮点击事件

class EventCategory(Enum):
    """ 事件分类枚举。 """
    MOUSE    = auto()    # 鼠标事件
    KEYBOARD = auto()    # 键盘事件
    INPUT    = auto()    # 输入事件
    WINDOW   = auto()    # 窗口事件
    USER     = auto()    # 用户自定义事件
    NONE     = auto()    # 未分类事件
# 事件类别映射字典
event_category_dict: dict[int, EventCategory] = {
    MOUSEBUTTONDOWN: EventCategory.MOUSE,
    MOUSEBUTTONUP:   EventCategory.MOUSE,
    MOUSEMOTION:     EventCategory.MOUSE,
    MOUSEWHEEL:      EventCategory.MOUSE,

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
# 启用所有已分类事件
pygame.event.set_allowed(list(event_category_dict.keys()))

def get_event_category(event_type: int) -> EventCategory:
    """ 获取事件类别。 """
    return event_category_dict.get(event_type, EventCategory.NONE)

del auto, Enum, pygame