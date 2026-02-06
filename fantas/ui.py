from __future__ import annotations
from dataclasses import dataclass, field

import fantas

__all__ = (
    "UI",
    "WindowRoot",
    "ColorBackground",
    "Label",
    "Image",
    "Text",
    "TextLabel",
    "LinearGradientLabel",
)

@dataclass(slots=True)
class UI(fantas.NodeBase):
    """ 显示元素基类。 """
    father  : UI | None   = field(default=None, init=False, repr=False)                     # 指向父显示元素
    children: list[UI]    = field(default_factory=list, init=False, repr=False)             # 子显示元素列表
    ui_id   : fantas.UIID = field(default_factory=fantas.generate_unique_id, init=False)    # 唯一标识 ID

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表，由子类实现，本方法会遍历子节点并生成渲染命令
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        for child in self.children:
            yield from child.create_render_commands(offset)

@dataclass(slots=True)
class WindowRoot(UI):
    """
    窗口根元素类。
    Args:
        window: 指向所属窗口。
    """
    window: fantas.Window
    rect  : fantas.RectLike = field(init=False)    # 窗口矩形区域

    def __post_init__(self):
        self.rect = fantas.IntRect((0, 0), self.window.size)

    def update_rect(self):
        """ 更新窗口矩形区域。 """
        self.rect.size = self.window.size

@dataclass(slots=True)
class ColorBackground(UI):
    """
    纯色背景类。
    Args:
        bgcolor: 背景颜色。
    """
    bgcolor : fantas.ColorLike = 'black'

    command : fantas.ColorBackgroundFillCommand = field(init=False, repr=False)    # 颜色填充命令

    def __post_init__(self):
        """ 初始化 ColorBackground 实例 """
        self.command = fantas.ColorBackgroundFillCommand(creator=self)

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        # 设置背景颜色
        self.command.color = self.bgcolor
        # 生成自己的渲染命令
        yield self.command
        # 生成子元素的渲染命令
        yield from UI.create_render_commands(self)

@dataclass(slots=True)
class Label(UI):
    """
    纯色矩形标签类。
    Args:
        rect    : 矩形区域。
        style   : 标签样式。
        box_mode: 盒子模式。
    """
    rect    : fantas.RectLike
    style   : fantas.LabelStyle = field(default_factory=fantas.DEFAULTLABELSTYLE.copy)
    box_mode: fantas.BoxMode    = fantas.BoxMode.INSIDE

    command: fantas.LabelRenderCommand = field(init=False, repr=False)

    def __post_init__(self):
        """ 初始化 Label 实例 """
        self.command = fantas.LabelRenderCommand(creator=self)

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        # 计算渲染命令矩形
        if isinstance(self.rect, fantas.Rect):
            rect = fantas.IntRect(self.rect).move(offset)
        else:
            rect = self.rect.move(offset)
        if self.style.border_width > 0:
            if self.box_mode is fantas.BoxMode.OUTSIDE:
                rect.inflate_ip(2 * self.style.border_width, 2 * self.style.border_width)
            elif self.box_mode is fantas.BoxMode.INOUTSIDE:
                rect.inflate_ip(self.style.border_width, self.style.border_width)
        self.command.rect = rect
        # 设置渲染命令样式
        self.command.style = self.style
        # 生成渲染命令
        yield self.command
        # 生成子元素的渲染命令
        yield from UI.create_render_commands(self, offset)

@dataclass(slots=True)
class Image(UI):
    """
    图像显示类。
    Args:
        surface  : 显示的 Surface 对象。
        rect     : 矩形区域。
        fill_mode: 填充模式。
    """
    surface  : fantas.Surface
    rect     : fantas.RectLike = None
    fill_mode: fantas.FillMode = fantas.FillMode.IGNORE

    command  : fantas.SurfaceRenderCommand = field(init=False, repr=False)                    # 渲染命令对象

    def __post_init__(self):
        """ 初始化 Image 实例 """
        self.command = fantas.SurfaceRenderCommand(creator=self)
        if self.rect is None:
            self.rect = fantas.Rect((0, 0), self.surface.get_size())

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        # 调整矩形区域
        rect = self.rect.move(offset)
        offset = rect.topleft
        # 生成 Surface 渲染命令
        c = self.command
        c.surface = self.surface
        c.fill_mode = self.fill_mode
        c.dest_rect = rect
        yield c
        # 生成子元素的渲染命令
        yield from UI.create_render_commands(self, offset)

@dataclass(slots=True)
class Text(UI):
    """
    文本显示类。
    Args:
        text      : 显示的文本内容。
        style     : 文本样式。
        rect      : 文本显示区域。
        align_mode: 对齐模式。
    """
    children: None               = field(default=None, init=False, repr=False)    # 纯色文本不包含子元素

    rect      : fantas.RectLike
    text      : str                  = 'text'
    style     : fantas.TextStyle     = field(default_factory=fantas.DEFAULTTEXTSTYLE.copy)
    align_mode: fantas.TextAlignMode = fantas.TextAlignMode.LEFT

    command : fantas.TextRenderCommand = field(init=False, repr=False)    # 渲染命令

    def __post_init__(self):
        """ 初始化 ColorText 实例 """
        self.command = fantas.TextRenderCommand(creator=self)

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表。
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象.
        """
        # 仅当文本非空时才生成渲染命令
        if not self.text:
            return
        # 简化引用
        rc = self.command
        # 设置文本内容
        rc.text = self.text
        # 设置对齐模式
        rc.align_mode = self.align_mode
        # 设置文本样式
        rc.style = self.style
        # 设置文本显示区域
        if isinstance(self.rect, fantas.Rect):
            rc.rect = fantas.IntRect(self.rect).move(offset)
        else:
            rc.rect = self.rect.move(offset)
        # 生成渲染命令
        yield rc

    def _get_lineheight(self) -> float:
        """ 获取文本行高（包含行间距） """
        return self.style.font.get_sized_height(self.style.size) + self.style.line_spacing
    def _set_lineheight(self, lineheight: float) -> None:
        """ 设置文本行高（包含行间距） """
        self.style.line_spacing = lineheight - self.style.font.get_sized_height(self.style.size)
    line_height = property(_get_lineheight, _set_lineheight)

@dataclass(slots=True)
class TextLabel(UI):
    """
    纯色矩形文本标签类。
    Args:
        rect       : 矩形区域。
        text       : 显示的文本内容。
        text_style : 文本样式。
        label_style: 标签样式。
        align_mode : 对齐模式。
        box_mode   : 盒子模式。
    """
    rect    : fantas.RectLike

    text       : str                  = 'text'
    text_style : fantas.TextStyle     = field(default_factory=fantas.DEFAULTTEXTSTYLE.copy)
    label_style: fantas.LabelStyle    = field(default_factory=fantas.DEFAULTLABELSTYLE.copy)
    align_mode : fantas.TextAlignMode = fantas.TextAlignMode.LEFT
    box_mode   : fantas.BoxMode       = fantas.BoxMode.INSIDE

    label_command: fantas.LabelRenderCommand = field(init=False, repr=False)    # 标签渲染命令
    text_command : fantas.TextRenderCommand = field(init=False, repr=False)     # 文本渲染命令

    def __post_init__(self):
        """ 初始化 TextLabel 实例 """
        self.text_command = fantas.TextRenderCommand(creator=self)
        self.label_command = fantas.LabelRenderCommand(creator=self)

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        # 简化引用
        lrc = self.label_command
        trc = self.text_command
        bw = self.label_style.border_width
        # 计算渲染命令矩形
        if isinstance(self.rect, fantas.Rect):
            rect = fantas.IntRect(self.rect).move(offset)
        else:
            rect = self.rect.move(offset)
        if bw > 0:
            if self.box_mode is fantas.BoxMode.OUTSIDE:
                lrc.rect = rect.inflate(2 * bw, 2 * bw)
                trc.rect = rect
            elif self.box_mode is fantas.BoxMode.INOUTSIDE:
                lrc.rect = rect.inflate(bw, bw)
                trc.rect = rect.inflate(-bw, -bw)
            else:
                lrc.rect = rect
                trc.rect = rect.inflate(-2 * bw, -2 * bw)
        else:
            lrc.rect = trc.rect = rect
        # 设置标签样式
        lrc.style = self.label_style
        # 生成标签渲染命令
        yield lrc
        # 仅当文本非空时才生成文本渲染命令
        if self.text:
            # 设置文本内容
            trc.text = self.text
            # 设置对齐模式
            trc.align_mode = self.align_mode
            # 设置文本样式
            trc.style = self.text_style
            # 生成渲染命令
            yield trc
        # 生成子元素的渲染命令
        yield from UI.create_render_commands(self, offset)

    def get_lineheight(self) -> float:
        """ 获取文本行高（包含行间距） """
        return self.text_style.font.get_sized_height(self.text_style.size) + self.text_style.line_spacing
    def set_lineheight(self, lineheight: float) -> None:
        """ 设置文本行高（包含行间距） """
        self.text_style.line_spacing = lineheight - self.text_style.font.get_sized_height(self.text_style.size)
    line_height = property(get_lineheight, set_lineheight)

@dataclass(slots=True)
class LinearGradientLabel(UI):
    """
    线性渐变标签类。
    Args:
        rect       : 矩形区域。
        start_color: 起始颜色。
        end_color  : 结束颜色。
        start_pos  : 起始位置。
        end_pos    : 结束位置。
    """
    rect       : fantas.RectLike
    start_color: fantas.ColorLike
    end_color  : fantas.ColorLike
    start_pos  : fantas.Point
    end_pos    : fantas.Point

    command: fantas.LinearGradientRenderCommand = field(init=False, repr=False)           # 渲染命令对象

    def __post_init__(self):
        """ 初始化 LinearGradientLabel 实例 """
        self.command = fantas.LinearGradientRenderCommand(creator=self)

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        # 计算渲染命令矩形
        if isinstance(self.rect, fantas.Rect):
            rect = fantas.IntRect(self.rect).move(offset)
        else:
            rect = self.rect.move(offset)
        # 简化引用
        c = self.command
        # 设置渲染命令属性
        c.rect = rect
        c.start_color = self.start_color
        c.end_color = self.end_color
        c.start_pos = (self.start_pos[0] + offset[0], self.start_pos[1] + offset[1])
        c.end_pos = (self.end_pos[0] + offset[0], self.end_pos[1] + offset[1])
        # 生成渲染命令
        yield c
        # 生成子元素的渲染命令
        yield from UI.create_render_commands(self, offset)
    
    def mark_cache_dirty(self):
        """ 标记渲染命令缓存为脏，需重新生成缓存 """
        self.command.cache_dirty = True
