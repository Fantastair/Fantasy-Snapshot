from __future__ import annotations
from dataclasses import dataclass
from collections import deque

import fantas

__all__ = (
    "Renderer",
    "RenderCommand",
    "SurfaceRenderCommand",
    "ColorFillCommand",
    "ColorTextLineRenderCommand",
)

class Renderer:
    """
    渲染器类，管理渲染命令队列并执行渲染操作。
    """
    def __init__(self):
        self.queue = deque()    # 渲染命令队列，左端入右端出

    def pre_render(self, root_ui: fantas.UI):
        """
        预处理渲染命令，从根 UI 元素生成渲染命令并添加到渲染队列中。
        Args:
            root_ui (fantas.UI): 根 UI 元素。
        """
        self.queue.clear()
        for command in root_ui.create_render_commands():
            self.queue.append(command)

    def render(self, target_surface: fantas.Surface):
        """
        执行渲染队列中的所有渲染命令。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象，渲染结果将绘制到该对象上。
        """
        for command in self.queue:
            command.render(target_surface)

    def add_command(self, command: fantas.RenderCommand):
        """
        向渲染队列中添加一个渲染命令。
        Args:
            command (fantas.RenderCommand): 渲染命令对象，必须实现 render(target_surface) 方法。
        """
        self.queue.appendleft(command)

    def clear_commands(self):
        """
        清空渲染命令队列。
        """
        self.queue.clear()

@dataclass(slots=True)
class RenderCommand:
    """
    渲染命令基类，所有具体渲染命令类应继承自此类并实现 render 方法。
    """
    creator: fantas.UI    # 创建此渲染命令的 UI 元素

    def render(self, target_surface: fantas.Surface):
        """
        执行渲染操作，将渲染结果绘制到目标 Surface 上。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象，渲染结果将绘制到该对象上。
        """
        raise NotImplementedError("子类未实现 render 方法。")

@dataclass(slots=True)
class SurfaceRenderCommand(RenderCommand):
    """
    Surface 渲染命令类，表示将一个 Surface 渲染到目标矩形区域。
    """
    surface: fantas.Surface       # 要渲染的 Surface 对象
    dest_rect: fantas.RectLike    # 目标矩形区域，指定渲染的位置

    def render(self, target_surface: fantas.Surface):
        """
        执行渲染操作，将 Surface 渲染到目标 Surface 上的指定矩形区域。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象，渲染结果将绘制到该对象上。
        """
        target_surface.blit(self.surface, self.dest_rect)

@dataclass(slots=True)
class ColorFillCommand(RenderCommand):
    """
    颜色填充命令类，表示在目标矩形区域内填充指定颜色。
    """
    color: fantas.ColorLike                     # 填充颜色
    dest_rect: fantas.RectLike | None = None    # 目标矩形区域，指定填充的位置和大小

    def render(self, target_surface: fantas.Surface):
        """
        执行填充操作，在目标 Surface 上的指定矩形区域内填充颜色。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象，填充结果将绘制到该对象上。
        """
        target_surface.fill(self.color, self.dest_rect)

@dataclass(slots=True)
class ColorTextLineRenderCommand(RenderCommand):
    """
    文字渲染命令类，表示将文本渲染到目标矩形区域。
    """
    text: str                           # 要渲染的文本内容
    font: fantas.Font                   # 字体对象
    size: float                         # 字体大小
    fgcolor: fantas.ColorLike | None    # 文字颜色
    dest_rect: fantas.RectLike          # 目标矩形区域，指定文本的渲染位置和大小

    def render(self, target_surface: fantas.Surface):
        """
        执行文本渲染操作，将文本渲染到目标 Surface 上的指定矩形区域。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象，渲染结果将绘制到该对象上。
        """
        self.font.render_to(target_surface, self.dest_rect, self.text, self.fgcolor, size=self.size)
