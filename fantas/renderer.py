from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque

import fantas

__all__ = (
    "Renderer",
    "RenderCommand",
    "SurfaceRenderCommand",
    "ColorFillCommand",
    "ColorBackgroundFillCommand",
    "ColorTextLineRenderCommand",
    "QuarterCircleRenderCommand",
)

class Renderer:
    """
    渲染器类，管理渲染命令队列并执行渲染操作。
    """
    def __init__(self, window: fantas.Window):
        self.window = window    # 关联的窗口对象
        self.queue = deque()    # 渲染命令队列，左端入右端出

    def pre_render(self, root_ui: fantas.UI):
        """
        预处理渲染命令，即更新渲染命令队列。
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
            target_surface (fantas.Surface): 目标 Surface 对象。
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

    def coordinate_hit_test(self, point: fantas.IntPoint) -> fantas.UI:
        """
        根据给定的坐标点进行命中测试，返回位于该点的最上层 UI 元素。
        Args:
            point (fantas.IntPoint): 坐标点（x, y）。
        Returns:
            fantas.UI: 位于该点的最上层 UI 元素，如果没有命中任何元素则返回根 UI 元素。
        """
        for rc in reversed(self.queue):
            if rc.hit_test(point):
                return rc.creator
        return self.window.root_ui

@dataclass(slots=True)
class RenderCommand:
    """
    渲染命令基类。
    """
    creator: fantas.UI    # 创建此渲染命令的 UI 元素

    def render(self, target_surface: fantas.Surface):
        """
        执行渲染操作，将渲染结果绘制到目标 Surface 上。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        raise NotImplementedError("子类未实现 render 方法。")

    def hit_test(self, point: fantas.IntPoint) -> bool:
        """
        命中测试，判断给定的坐标点是否在此渲染命令的区域内。
        Args:
            point (fantas.IntPoint): 坐标点（x, y）。
        Returns:
            bool: 如果点在区域内则返回 True，否则返回 False。
        """
        raise NotImplementedError("子类未实现 hit_test 方法。")

@dataclass(slots=True)
class SurfaceRenderCommand(RenderCommand):
    """
    Surface 渲染命令类。
    """
    creator  : fantas.UI                                                           # 创建此渲染命令的 UI 元素
    surface  : fantas.Surface                                                      # 要渲染的 Surface 对象
    fill_mode: fantas.FillMode = fantas.FillMode.IGNORE                            # 填充模式
    dest_rect: fantas.RectLike = field(default_factory=fantas.DEFAULTRECT.copy)    # 目标矩形区域

    affected_area: fantas.RectLike = field(init=False, repr=False)                 # 受影响的矩形区域

    def render(self, target_surface: fantas.Surface):
        """
        执行渲染操作。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        SurfaceRenderCommand_render_map[self.fill_mode](self, target_surface)

    def hit_test(self, point: fantas.IntPoint) -> bool:
        """
        命中测试。
        Args:
            point (fantas.IntPoint): 坐标点（x, y）。
        Returns:
            bool: 如果点在区域内则返回 True，否则返回 False。
        """
        return self.affected_area.collidepoint(point)

    def render_IGNORE(self, target_surface: fantas.Surface):
        """
        执行 IGNORE 填充模式的渲染操作。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        self.affected_area = target_surface.blit(self.surface, self.dest_rect)

    def render_SCALE(self, target_surface: fantas.Surface):
        """
        执行 SCALE 填充模式的渲染操作。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        rect = self.affected_area = self.dest_rect
        target_surface.blit(fantas.transform.scale(self.surface, rect.size), rect)
    
    def render_SMOOTHSCALE(self, target_surface: fantas.Surface):
        """
        执行 SMOOTHSCALE 填充模式的渲染操作。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        rect = self.affected_area = self.dest_rect
        target_surface.blit(fantas.transform.smoothscale(self.surface, rect.size), rect)

    def render_REPEAT(self, target_surface: fantas.Surface):
        """
        执行 REPEAT 填充模式的渲染操作。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        # 简化引用
        rect = self.affected_area = self.dest_rect
        surface = self.surface
        if isinstance(rect, fantas.Rect):
            rect = fantas.IntRect(rect)
        left, top, width, height = rect
        w, h = surface.get_size()
        # 计算重复次数并绘制
        row_count, height_remain = divmod(height, h)
        col_count, width_remain  = divmod(width,  w)
        for row in range(row_count):
            for col in range(col_count):
                target_surface.blit(surface, (left + col * w, top + row * h))
        top_row = top + row_count * h
        left_col = left + col_count * w
        # 绘制剩余部分
        if height_remain > 0:
            for col in range(left, left_col, w):
                target_surface.blit(surface, (col, top_row), (0, 0, w, height_remain))
        if width_remain > 0:
            for row in range(top, top_row, h):
                target_surface.blit(surface, (left_col, row), (0, 0, width_remain, h))
        if height_remain > 0 and width_remain > 0:
            target_surface.blit(surface, (left_col, top_row), (0, 0, width_remain, height_remain))

    def render_FITMIN(self, target_surface: fantas.Surface):
        """
        执行 FITMIN 填充模式的渲染操作。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        # 简化引用
        w, h = self.surface.get_size()
        left, top, width, height = self.dest_rect
        scale = min(width / w, height / h)
        # 计算缩放后尺寸并居中绘制
        w = round(w * scale)
        h = round(h * scale)
        self.affected_area = target_surface.blit(fantas.transform.smoothscale(self.surface, (w, h)), (left + (width - w) // 2, top + (height - h) // 2))

    def render_FITMAX(self, target_surface: fantas.Surface):
        """
        执行 FITMAX 填充模式的渲染操作。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        # 简化引用
        w, h = self.surface.get_size()
        left, top, width, height = self.affected_area = self.dest_rect
        scale = max(width / w, height / h)
        # 计算缩放后尺寸并居中绘制
        w = round(w * scale)
        h = round(h * scale)
        scaled_surface = fantas.transform.smoothscale(self.surface, (w, h))
        target_surface.blit(scaled_surface, (left, top), ((w - width) // 2, (h - height) // 2, width, height))

# SurfaceRenderCommand 渲染映射表
SurfaceRenderCommand_render_map = {
    fantas.FillMode.IGNORE     : SurfaceRenderCommand.render_IGNORE,
    fantas.FillMode.SCALE      : SurfaceRenderCommand.render_SCALE,
    fantas.FillMode.SMOOTHSCALE: SurfaceRenderCommand.render_SMOOTHSCALE,
    fantas.FillMode.REPEAT     : SurfaceRenderCommand.render_REPEAT,
    fantas.FillMode.FITMIN     : SurfaceRenderCommand.render_FITMIN,
    fantas.FillMode.FITMAX     : SurfaceRenderCommand.render_FITMAX,
}

@dataclass(slots=True)
class ColorFillCommand(RenderCommand):
    """
    颜色填充命令类。
    """
    creator  : fantas.UI                     # 创建此渲染命令的 UI 元素
    color    : fantas.ColorLike = 'black'    # 填充颜色
    dest_rect: fantas.RectLike  = field(default_factory=fantas.DEFAULTRECT.copy)    # 目标矩形区域，指定填充的位置和大小

    def render(self, target_surface: fantas.Surface):
        """
        执行填充操作。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        target_surface.fill(self.color, self.dest_rect)

    def hit_test(self, point: fantas.IntPoint) -> bool:
        """
        命中测试。
        Args:
            point (fantas.IntPoint): 坐标点（x, y）。
        Returns:
            bool: 如果点在区域内则返回 True，否则返回 False。
        """
        return self.dest_rect.collidepoint(point)

class ColorBackgroundFillCommand(RenderCommand):
    """
    颜色背景填充命令类。
    """
    creator  : fantas.UI                     # 创建此渲染命令的 UI 元素
    color    : fantas.ColorLike = 'black'    # 填充颜色

    def render(self, target_surface: fantas.Surface):
        """
        执行填充操作。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        target_surface.fill(self.color)

    def hit_test(self, point: fantas.IntPoint) -> bool:
        """
        命中测试。
        Args:
            point (fantas.IntPoint): 坐标点（x, y）。
        Returns:
            bool: 如果点在区域内则返回 True，否则返回 False。
        """
        return True

@dataclass(slots=True)
class ColorTextLineRenderCommand(RenderCommand):
    """
    文字渲染命令类。
    """
    creator  : fantas.UI                                       # 创建此渲染命令的 UI 元素
    text     : str                     = 'text'                # 文本内容
    font     : fantas.Font             = fantas.DEFAULTFONT    # 字体对象
    size     : float                   = 16.0                  # 字体大小
    fgcolor  : fantas.ColorLike | None = 'black'               # 文字颜色
    origin   : fantas.Point            = (0, 0)                # 渲染原点
    affected_rect: fantas.RectLike     = field(init=False)     # 受影响的矩形区域

    def render(self, target_surface: fantas.Surface):
        """
        执行文本渲染操作。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        self.affected_rect = self.font.render_to(target_surface, self.origin, self.text, self.fgcolor, size=self.size)

    def hit_test(self, point: fantas.IntPoint) -> bool:
        """
        命中测试。
        Args:
            point (fantas.IntPoint): 坐标点（x, y）。
        Returns:
            bool: 如果点在区域内则返回 True，否则返回 False。
        """
        return self.affected_rect.collidepoint(point)

# 象限映射表
quadrant_map = {
    fantas.Quadrant.TOPRIGHT   : {'draw_top_right': True},
    fantas.Quadrant.TOPLEFT    : {'draw_top_left' : True},
    fantas.Quadrant.BOTTOMLEFT : {'draw_bottom_left': True},
    fantas.Quadrant.BOTTOMRIGHT: {'draw_bottom_right': True},
}

@dataclass(slots=True)
class QuarterCircleRenderCommand(RenderCommand):
    """
    四分之一圆渲染命令类。
    """
    creator  : fantas.UI                     # 创建此渲染命令的 UI 元素
    color    : fantas.ColorLike = 'black'    # 圆的颜色
    center   : fantas.Point     = (0, 0)     # 圆心位置
    radius   : int | float      = 8          # 圆的半径，≥ 1
    width    : int | float      = 0          # 圆边框宽度，≥ 0，0 表示填充
    quadrant : fantas.Quadrant  = fantas.Quadrant.TOPRIGHT    # 象限

    def render(self, target_surface: fantas.Surface):
        """
        执行四分之一圆渲染操作。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        fantas.draw.aacircle(target_surface, self.color, self.center, self.radius, width=self.width, **quadrant_map[self.quadrant])

    def hit_test(self, point: fantas.Point) -> bool:
        """
        命中测试。
        Args:
            point (fantas.IntPoint): 坐标点（x, y）。
        Returns:
            bool: 如果点在区域内则返回 True，否则返回 False。
        """
        # 计算相对坐标
        cx, cy = self.center
        dx = point[0] - cx
        dy = point[1] - cy
        # 符号测试
        if (self.quadrant & 0b11) ^ ((dx >= 0) | ((dy >= 0) << 1)):
            return False
        # 距离测试
        return self.radius * self.radius >= dx * dx + dy * dy >= self.width * self.width
