from typing import TypeAlias, Callable
import pygame

__all__ = (
    "RectLike", "Rect",
    "ColorLike", "Color",
    "Point", "IntPoint",
    "Event", "EventType", "IsCapture",
    "UIID", "ListenerKey", "ListenerFunc",
    "Surface",
    "Font",
)

RectLike:  TypeAlias = pygame.typing.RectLike     # 矩形类型
from pygame import FRect as Rect                  # 矩形类

ColorLike: TypeAlias = pygame.typing.ColorLike    # 颜色类型
from pygame import Color                          # 颜色类

Point:     TypeAlias = pygame.typing.Point       # 点类
IntPoint:  TypeAlias = pygame.typing.IntPoint    # 整数点类

from pygame.event import Event    # 事件类
EventType: TypeAlias = int        # 事件类型

UIID: TypeAlias = int    # UI 元素唯一标识类型
ListenerKey : TypeAlias = tuple[EventType, UIID, bool]    # 监听器键类型
ListenerFunc: TypeAlias = Callable[[Event], bool]         # 监听器函数类型

from pygame import Surface          # 表面类
from pygame.freetype import Font    # 字体类
