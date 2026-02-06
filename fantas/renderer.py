from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field

import fantas

__all__ = (
    "Renderer",
    "RenderCommand",
    "SurfaceRenderCommand",
    "ColorFillCommand",
    "ColorBackgroundFillCommand",
    "LabelRenderCommand",
    "TextRenderCommand",
    "QuarterCircleRenderCommand",
)

@dataclass(slots=True)
class Renderer:
    """
    渲染器类，管理渲染命令队列并执行渲染操作。
    Args:
        window: 关联的窗口对象。
    """
    window: fantas.Window    # 关联的窗口对象

    queue: deque = field(default_factory=deque, init=False, repr=False)    # 渲染命令队列，左端入右端出

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
class RenderCommand(ABC):
    """
    渲染命令基类。
    Args:
        creator: 创建此渲染命令的 UI 元素。
    """
    creator: fantas.UI

    @abstractmethod
    def render(self, target_surface: fantas.Surface):
        """
        执行渲染操作，将渲染结果绘制到目标 Surface 上。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        pass


    @abstractmethod
    def hit_test(self, point: fantas.IntPoint) -> bool:
        """
        命中测试，判断给定的坐标点是否在此渲染命令的区域内。
        Args:
            point (fantas.IntPoint): 坐标点（x, y）。
        Returns:
            bool: 如果点在区域内则返回 True，否则返回 False。
        """
        pass

@dataclass(slots=True)
class SurfaceRenderCommand(RenderCommand):
    """
    Surface 渲染命令类。
    Args:
        surface  : 要渲染的 Surface 对象。
        fill_mode: 填充模式。
        dest_rect: 目标矩形区域。
    """
    surface  : fantas.Surface
    dest_rect: fantas.RectLike
    fill_mode: fantas.FillMode = fantas.FillMode.IGNORE

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
    Args:
        dest_rect: 目标矩形区域。
        color    : 填充颜色。
    """
    dest_rect: fantas.RectLike
    color    : fantas.ColorLike = 'black'

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
    Args:
        color: 填充颜色。
    """
    color    : fantas.ColorLike = 'black'

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
class LabelRenderCommand(RenderCommand):
    """
    矩形标签渲染命令类。
    Args:
        style: 标签样式。
        rect : 渲染区域。
    """
    style: fantas.LabelStyle = field(init=False)
    rect : fantas.RectLike   = field(init=False)

    def render(self, target_surface: fantas.Surface):
        """
        执行渲染操作。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        s = self.style
        rect = self.rect
        bw = s.border_width
        if bw > 0:
            fantas.draw.aarect(target_surface, s.fgcolor, rect, bw, s.border_radius, s.border_radius_top_left, s.border_radius_top_right, s.border_radius_bottom_left, s.border_radius_bottom_right)
            rect = rect.inflate(-2 * bw, -2 * bw)
        if s.bgcolor is not None:
            if s.border_radius_top_left >= 0 or s.border_radius_top_right >= 0 or s.border_radius_bottom_left >= 0 or s.border_radius_bottom_right >= 0:
                fantas.draw.aarect(target_surface, s.bgcolor, rect, 0, s.border_radius - bw, max(0, s.border_radius_top_left - bw), max(0, s.border_radius_top_right - bw), max(0, s.border_radius_bottom_left - bw), max(0, s.border_radius_bottom_right - bw))
            else:
                fantas.draw.aarect(target_surface, s.bgcolor, rect, 0, s.border_radius - bw, s.border_radius_top_left - bw)

    def hit_test(self, point: fantas.IntPoint) -> bool:
        """
        命中测试。
        Args:
            point (fantas.IntPoint): 坐标点（x, y）。
        Returns:
            bool: 如果点在区域内则返回 True，否则返回 False。
        """
        return self.rect.collidepoint(point)

@dataclass(slots=True)
class TextRenderCommand(RenderCommand):
    """
    文本渲染命令类。
    Args:
        text      : 文本内容。
        align_mode: 对齐模式。
        style     : 文本样式。
        rect      : 渲染区域。
    """
    text      : str                  = 'text'
    align_mode: fantas.TextAlignMode = fantas.TextAlignMode.LEFT
    style     : fantas.TextStyle     = field(default_factory=lambda: fantas.DEFAULTTEXTSTYLE)
    rect      : fantas.RectLike      = field(default_factory=lambda: fantas.Rect(0, 0, 100, 0))

    affected_rects: list[fantas.RectLike] = field(default_factory=list, init=False, repr=False)    # 受影响的矩形区域列表

    def render(self, target_surface: fantas.Surface):
        """
        执行多行文本渲染操作。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        # 简化引用
        s = self.style
        # 执行渲染
        TextRenderCommand_render_map[self.align_mode](self, target_surface)

    def hit_test(self, point: fantas.IntPoint) -> bool:
        """
        命中测试。
        Args:
            point (fantas.IntPoint): 坐标点（x, y）。
        Returns:
            bool: 如果点在区域内则返回 True，否则返回 False。
        """
        for rect in self.affected_rects:
            if rect.collidepoint(point):
                return True
        return False

    def render_LEFT(self, target_surface: fantas.Surface):
        """
        左对齐渲染。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        # 简化引用
        s = self.style
        size = s.size
        font = s.font
        ar = self.affected_rects
        ar_append = ar.append
        rect = self.rect
        font_ascender = font.get_sized_ascender(size)
        line_height = font.get_sized_height(size) + s.line_spacing
        # 清空受影响矩形列表
        ar.clear()
        # 计算换行结果
        wraps = s.font.auto_wrap(s.style_flag, s.size, self.text, self.rect.width)
        # 计算渲染原点及范围
        origin_x = rect.left
        origin_y = rect.centery - (len(wraps) * line_height - s.line_spacing) // 2 + font_ascender
        min_y = rect.top + font_ascender
        max_y = rect.bottom + font.get_sized_descender(size)
        # 执行渲染
        for text, _ in wraps:
            if origin_y >= min_y:
                ar_append(font.render_to(target_surface, (origin_x, origin_y), text, s.fgcolor, style=s.style_flag, size=size))
            origin_y += line_height
            if origin_y > max_y:
                break

    def render_CENTER(self, target_surface: fantas.Surface):
        """
        居中对齐渲染。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        # 简化引用
        s = self.style
        size = s.size
        font = s.font
        ar = self.affected_rects
        ar_append = ar.append
        rect = self.rect
        centerx = rect.centerx
        font_ascender = font.get_sized_ascender(size)
        line_height = font.get_sized_height(size) + s.line_spacing
        # 清空受影响矩形列表
        ar.clear()
        # 计算换行结果
        wraps = s.font.auto_wrap(s.style_flag, s.size, self.text, self.rect.width)
        # 计算渲染原点及范围
        origin_y = rect.centery - (len(wraps) * line_height - s.line_spacing) // 2 + font_ascender
        min_y = rect.top + font_ascender
        max_y = rect.bottom + font.get_sized_descender(size)
        # 执行渲染
        for text, width in wraps:
            if origin_y >= min_y:
                ar_append(font.render_to(target_surface, (centerx - width // 2, origin_y), text, s.fgcolor, style=s.style_flag, size=size))
            origin_y += line_height
            if origin_y > max_y:
                break

    def render_RIGHT(self, target_surface: fantas.Surface, wraps: tuple[tuple[str, int]]):
        """
        右对齐渲染。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        # 简化引用
        s = self.style
        size = s.size
        font = s.font
        ar = self.affected_rects
        ar_append = ar.append
        rect = self.rect
        right = rect.right
        font_ascender = font.get_sized_ascender(size)
        line_height = font.get_sized_height(size) + s.line_spacing
        # 清空受影响矩形列表
        ar.clear()
        # 计算换行结果
        wraps = s.font.auto_wrap(s.style_flag, s.size, self.text, self.rect.width)
        # 计算渲染原点及范围
        origin_y = rect.centery - (len(wraps) * line_height - s.line_spacing) // 2 + font_ascender
        min_y = rect.top + font_ascender
        max_y = rect.bottom + font.get_sized_descender(size)
        # 执行渲染
        for text, width in wraps:
            if origin_y >= min_y:
                ar_append(font.render_to(target_surface, (right - width, origin_y), text, s.fgcolor, style=s.style_flag, size=size))
            origin_y += line_height
            if origin_y > max_y:
                break
    
    def render_TOP(self, target_surface: fantas.Surface):
        """
        顶部对齐渲染。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        # 简化引用
        s = self.style
        size = s.size
        font = s.font
        ar = self.affected_rects
        ar_append = ar.append
        rect = self.rect
        centerx = rect.centerx
        line_height = font.get_sized_height(size) + s.line_spacing
        # 清空受影响矩形列表
        ar.clear()
        # 计算换行结果
        wraps = s.font.auto_wrap(s.style_flag, s.size, self.text, self.rect.width)
        # 计算渲染原点及范围
        origin_y = rect.top + font.get_sized_ascender(size)
        max_y = rect.bottom + font.get_sized_descender(size)
        # 执行渲染
        for text, width in wraps:
            ar_append(font.render_to(target_surface, (centerx - width // 2, origin_y), text, s.fgcolor, style=s.style_flag, size=size))
            origin_y += line_height
            if origin_y > max_y:
                break
    
    def render_BOTTOM(self, target_surface: fantas.Surface):
        """
        底部对齐渲染。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        # 简化引用
        s = self.style
        size = s.size
        font = s.font
        ar = self.affected_rects
        ar_append = ar.append
        rect = self.rect
        centerx = rect.centerx
        font_ascender = font.get_sized_ascender(size)
        line_height = font.get_sized_height(size) + s.line_spacing
        # 清空受影响矩形列表
        ar.clear()
        # 计算换行结果
        wraps = s.font.auto_wrap(s.style_flag, s.size, self.text, self.rect.width)
        # 计算渲染原点及范围
        min_y = rect.top + font_ascender
        max_y = rect.bottom + font.get_sized_descender(size)
        origin_y = rect.bottom - len(wraps) * line_height + s.line_spacing + font_ascender
        # 执行渲染
        for text, width in wraps:
            if origin_y >= min_y:
                ar_append(font.render_to(target_surface, (centerx - width // 2, origin_y), text, s.fgcolor, style=s.style_flag, size=size))
            origin_y += line_height
    
    def render_TOPLEFT(self, target_surface: fantas.Surface):
        """
        左上对齐渲染。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        # 简化引用
        s = self.style
        size = s.size
        font = s.font
        ar = self.affected_rects
        ar_append = ar.append
        rect = self.rect
        line_height = font.get_sized_height(size) + s.line_spacing
        # 清空受影响矩形列表
        ar.clear()
        # 计算换行结果
        wraps = s.font.auto_wrap(s.style_flag, s.size, self.text, self.rect.width)
        # 计算渲染原点及范围
        origin_x = rect.left
        origin_y = rect.top + font.get_sized_ascender(size)
        max_y = rect.bottom + font.get_sized_descender(size)
        # 执行渲染
        for text, _ in wraps:
            ar_append(font.render_to(target_surface, (origin_x, origin_y), text, s.fgcolor, style=s.style_flag, size=size))
            origin_y += line_height
            if origin_y > max_y:
                break
    
    def render_TOPRIGHT(self, target_surface: fantas.Surface):
        """
        右上对齐渲染。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        # 简化引用
        s = self.style
        size = s.size
        font = s.font
        ar = self.affected_rects
        ar_append = ar.append
        rect = self.rect
        right = rect.right
        line_height = font.get_sized_height(size) + s.line_spacing
        # 清空受影响矩形列表
        ar.clear()
        # 计算换行结果
        wraps = s.font.auto_wrap(s.style_flag, s.size, self.text, self.rect.width)
        # 计算渲染原点及范围
        origin_y = rect.top + font.get_sized_ascender(size)
        max_y = rect.bottom + font.get_sized_descender(size)
        # 执行渲染
        for text, width in wraps:
            ar_append(font.render_to(target_surface, (right - width, origin_y), text, s.fgcolor, style=s.style_flag, size=size))
            origin_y += line_height
            if origin_y > max_y:
                break
    
    def render_BOTTOMLEFT(self, target_surface: fantas.Surface):
        """
        左下对齐渲染。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        # 简化引用
        s = self.style
        size = s.size
        font = s.font
        ar = self.affected_rects
        ar_append = ar.append
        rect = self.rect
        font_ascender = font.get_sized_ascender(size)
        line_height = font.get_sized_height(size) + s.line_spacing
        # 清空受影响矩形列表
        ar.clear()
        # 计算换行结果
        wraps = s.font.auto_wrap(s.style_flag, s.size, self.text, self.rect.width)
        # 计算渲染原点及范围
        origin_x = rect.left
        min_y = rect.top + font_ascender
        max_y = rect.bottom + font.get_sized_descender(size)
        origin_y = rect.bottom - len(wraps) * line_height + s.line_spacing + font_ascender
        # 执行渲染
        for text, _ in wraps:
            if origin_y >= min_y:
                ar_append(font.render_to(target_surface, (origin_x, origin_y), text, s.fgcolor, style=s.style_flag, size=size))
            origin_y += line_height
    
    def render_BOTTOMRIGHT(self, target_surface: fantas.Surface):
        """
        右下对齐渲染。
        Args:
            target_surface (fantas.Surface): 目标 Surface 对象。
        """
        # 简化引用
        s = self.style
        size = s.size
        font = s.font
        ar = self.affected_rects
        ar_append = ar.append
        rect = self.rect
        right = rect.right
        font_ascender = font.get_sized_ascender(size)
        line_height = font.get_sized_height(size) + s.line_spacing
        # 清空受影响矩形列表
        ar.clear()
        # 计算换行结果
        wraps = s.font.auto_wrap(s.style_flag, s.size, self.text, self.rect.width)
        # 计算渲染原点及范围
        min_y = rect.top + font_ascender
        max_y = rect.bottom + font.get_sized_descender(size)
        origin_y = rect.bottom - len(wraps) * line_height + s.line_spacing + font_ascender
        # 执行渲染
        for text, width in wraps:
            if origin_y >= min_y:
                ar_append(font.render_to(target_surface, (right - width, origin_y), text, s.fgcolor, style=s.style_flag, size=size))
            origin_y += line_height

# TextRenderCommand 渲染映射表
TextRenderCommand_render_map = {
    fantas.TextAlignMode.TOP        : TextRenderCommand.render_TOP,
    fantas.TextAlignMode.LEFT       : TextRenderCommand.render_LEFT,
    fantas.TextAlignMode.RIGHT      : TextRenderCommand.render_RIGHT,
    fantas.TextAlignMode.BOTTOM     : TextRenderCommand.render_BOTTOM,
    fantas.TextAlignMode.CENTER     : TextRenderCommand.render_CENTER,
    fantas.TextAlignMode.TOPLEFT    : TextRenderCommand.render_TOPLEFT,
    fantas.TextAlignMode.TOPRIGHT   : TextRenderCommand.render_TOPRIGHT,
    fantas.TextAlignMode.BOTTOMLEFT : TextRenderCommand.render_BOTTOMLEFT,
    fantas.TextAlignMode.BOTTOMRIGHT: TextRenderCommand.render_BOTTOMRIGHT,
}

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
    Args:
        color    : 圆的颜色。
        center   : 圆心位置。
        radius   : 圆的半径，≥ 1。
        width    : 圆边框宽度，≥ 0，0 表示填充。
        quadrant : 象限。
    """
    color    : fantas.ColorLike = 'black'
    center   : fantas.Point     = (0, 0)
    radius   : int | float      = 8
    width    : int              = 0
    quadrant : fantas.Quadrant  = fantas.Quadrant.TOPRIGHT

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
            point (fantas.Point): 坐标点（x, y）。
        Returns:
            bool: 如果点在区域内则返回 True，否则返回 False。
        """
        # 计算相对坐标
        cx, cy = self.center
        dx = point[0] - cx
        dy = point[1] - cy
        # 符号测试
        if not fantas.Quadrant.has_point(self.quadrant, (dx, dy)):
            return False
        # 距离测试
        return self.radius * self.radius >= dx * dx + dy * dy >= self.width * self.width
