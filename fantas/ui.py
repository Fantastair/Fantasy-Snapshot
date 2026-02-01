from __future__ import annotations
from dataclasses import dataclass, field

import fantas

__all__ = (
    "UI",
    "ColorBackground",
    "Label",
    "SurfaceLabel",
    "TextLine",
    "Text",
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
class ColorBackground(UI):
    """ 纯色背景 UI 类 """
    bgcolor : fantas.ColorLike = 'black'                                           # 背景颜色
    command : fantas.ColorBackgroundFillCommand = field(init=False, repr=False)    # 颜色填充命令

    def __post_init__(self):
        """ 初始化 ColorBackground 实例 """
        self.command = fantas.ColorBackgroundFillCommand(creator = self)

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

# 简化引用
ColorFillCommand = fantas.ColorFillCommand
QuarterCircleRenderCommand = fantas.QuarterCircleRenderCommand

@dataclass(slots=True)
class LabelRenderCommands:
    """ Label 渲染命令容器。 """
    top               : ColorFillCommand              # 上填充命令
    bottom            : ColorFillCommand              # 下填充命令
    center            : ColorFillCommand              # 中填充命令

    top_border        : ColorFillCommand              # 上边框命令
    left_border       : ColorFillCommand              # 左边框命令
    right_border      : ColorFillCommand              # 右边框命令
    bottom_border     : ColorFillCommand              # 下边框命令

    topleft           : QuarterCircleRenderCommand    # 左上角圆角命令
    topright          : QuarterCircleRenderCommand    # 右上角圆角命令
    bottomleft        : QuarterCircleRenderCommand    # 左下角圆角命令
    bottomright       : QuarterCircleRenderCommand    # 右下角圆角命令

    topleft_border    : QuarterCircleRenderCommand    # 左上角圆角边框命令
    topright_border   : QuarterCircleRenderCommand    # 右上角圆角边框命令
    bottomleft_border : QuarterCircleRenderCommand    # 左下角圆角边框命令
    bottomright_border: QuarterCircleRenderCommand    # 右下角圆角边框命令

@dataclass(slots=True)
class Label(UI):
    """ 纯色矩形 UI 类 """
    bgcolor: fantas.ColorLike | None   = 'black'                                                      # 背景颜色
    fgcolor: fantas.ColorLike          = 'white'                                                      # 前景颜色
    rect   : fantas.RectLike           = field(default_factory=lambda: fantas.Rect(0, 0, 100, 50))    # 矩形区域
    border_radius: int | float         = 0.0                                                          # 边框圆角半径
    border_width : int                 = 0                                                            # 边框宽度
    quadrant     : fantas.QuadrantMask = 0b111111                                                     # 圆角象限掩码
    box_mode     : fantas.BoxMode      = fantas.BoxMode.INSIDE                                        # 盒子模式

    render_commands: LabelRenderCommands = field(init=False, repr=False)                    # 渲染命令容器

    def __post_init__(self):
        """ 初始化 Label 实例 """
        self.render_commands = LabelRenderCommands(
            top                = ColorFillCommand(creator=self),
            bottom             = ColorFillCommand(creator=self),
            center             = ColorFillCommand(creator=self),
            top_border         = ColorFillCommand(creator=self),
            left_border        = ColorFillCommand(creator=self),
            right_border       = ColorFillCommand(creator=self),
            bottom_border      = ColorFillCommand(creator=self),
            topleft            = QuarterCircleRenderCommand(creator=self, quadrant=fantas.Quadrant.TOPLEFT),
            topright           = QuarterCircleRenderCommand(creator=self, quadrant=fantas.Quadrant.TOPRIGHT),
            bottomleft         = QuarterCircleRenderCommand(creator=self, quadrant=fantas.Quadrant.BOTTOMLEFT),
            bottomright        = QuarterCircleRenderCommand(creator=self, quadrant=fantas.Quadrant.BOTTOMRIGHT),
            topleft_border     = QuarterCircleRenderCommand(creator=self, quadrant=fantas.Quadrant.TOPLEFT),
            topright_border    = QuarterCircleRenderCommand(creator=self, quadrant=fantas.Quadrant.TOPRIGHT),
            bottomleft_border  = QuarterCircleRenderCommand(creator=self, quadrant=fantas.Quadrant.BOTTOMLEFT),
            bottomright_border = QuarterCircleRenderCommand(creator=self, quadrant=fantas.Quadrant.BOTTOMRIGHT),
        )

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
        bw = self.border_width
        bw_2x = bw * 2
        bm = self.box_mode
        if isinstance(rect, fantas.Rect):
            rect = fantas.IntRect(rect)
        if bm == fantas.BoxMode.OUTSIDE:
            rect.inflate_ip(bw_2x, bw_2x)
        elif bm == fantas.BoxMode.INOUTSIDE:
            rect.inflate_ip(bw, bw)
        # 限制圆角半径和边框宽度
        border_radius = self.border_radius
        border_width  = bw
        min_half_size = min(rect.width, rect.height) / 2
        self.border_radius = round(border_radius) if border_radius < min_half_size else round(min_half_size)
        self.border_width  = border_width  if border_width  < min_half_size else round(min_half_size)
        # 计算渲染样式键
        render_style_key = ((self.bgcolor is not None) << 2) | ((self.border_width >= 1) << 1) | (self.border_radius >= 1)
        # 生成对应的渲染命令。
        if render_style_key >> 1:    # 背景色和边框至少有一个存在
            yield from Label_crc_bwr_map[render_style_key](self, rect)
        # 生成子元素的渲染命令
        yield from UI.create_render_commands(self, offset)
        # 恢复圆角半径和边框宽度
        self.border_radius = border_radius
        self.border_width  = border_width

    def crc_bwr_010(self, rect: fantas.RectLike):
        """
        无背景色，有边框，无圆角渲染命令生成器。
        Args:
            rect (fantas.RectLike): 矩形区域（绝对位置）。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        # 简化引用
        rcs = self.render_commands
        tb = rcs.top_border
        bb = rcs.bottom_border
        lb = rcs.left_border
        rb = rcs.right_border
        top = rect.top
        left = rect.left
        width = rect.width
        bw = self.border_width
        in_top = top + bw
        in_height = rect.height - 2 * bw
        # 更新样式
        tb.color = bb.color = lb.color = rb.color = self.fgcolor
        tb.dest_rect.update(left, top, width, bw)
        lb.dest_rect.update(left, in_top, bw, in_height)
        bb.dest_rect.update(left, rect.bottom - bw, width, bw)
        rb.dest_rect.update(rect.right - bw, in_top, bw, in_height)
        # 生成渲染命令
        yield tb
        yield bb
        yield lb
        yield rb

    def crc_bwr_011(self, rect: fantas.RectLike):
        """
        无背景色，有边框，有圆角渲染命令生成器。
        Args:
            rect (fantas.RectLike): 矩形区域（绝对位置）。
        Yields:
            RenderCommand: 渲染命令对象.
        """
        # 简化引用
        rcs = self.render_commands
        tb = rcs.top_border
        lb = rcs.left_border
        rb = rcs.right_border
        bb = rcs.bottom_border
        tlb = rcs.topleft_border
        trb = rcs.topright_border
        blb = rcs.bottomleft_border
        brb = rcs.bottomright_border
        quadrant = self.quadrant >> 2
        tr_on =  quadrant & 0b0001
        tl_on = (quadrant & 0b0010) >> 1
        bl_on = (quadrant & 0b0100) >> 2
        br_on = (quadrant & 0b1000) >> 3
        top = rect.top
        left = rect.left
        width = rect.width
        right = rect.right
        bottom = rect.bottom
        height = rect.height
        bw = self.border_width
        fgcolor = self.fgcolor
        radius = self.border_radius
        radius_tl = radius if tl_on else 0
        radius_tr = radius if tr_on else 0
        radius_bl = radius if bl_on else 0
        radius_br = radius if br_on else 0
        top_radius = top + radius
        left_radius = left + radius
        right_radius = right - radius - 1
        bottom_radius = bottom - radius - 1
        # 更新样式并生成渲染命令
        tb.color = bb.color = lb.color = rb.color = fgcolor
        tb.dest_rect.update(left + radius_tl, top            , width - radius_tl - radius_tr,  bw)
        bb.dest_rect.update(left + radius_bl, bottom - bw    , width - radius_bl - radius_br,  bw)
        lb.dest_rect.update(left            , top + radius_tl, bw, height - radius_tl - radius_bl)
        rb.dest_rect.update(right - bw      , top + radius_tr, bw, height - radius_tr - radius_br)
        yield tb
        yield bb
        yield lb
        yield rb
        if bw > 1:
            bw -= 1
        if tl_on:
            tlb.color, tlb.center, tlb.radius, tlb.width = fgcolor, (left_radius, top_radius), radius, bw
            yield tlb
        if tr_on:
            trb.color, trb.center, trb.radius, trb.width = fgcolor, (right_radius, top_radius), radius, bw
            yield trb
        if bl_on:
            blb.color, blb.center, blb.radius, blb.width = fgcolor, (left_radius, bottom_radius), radius, bw
            yield blb
        if br_on:
            brb.color, brb.center, brb.radius, brb.width = fgcolor, (right_radius, bottom_radius), radius, bw
            yield brb

    def crc_bwr_100(self, rect: fantas.RectLike):
        """
        有背景色，无边框，无圆角渲染命令生成器。
        Args:
            rect (fantas.RectLike): 矩形区域（绝对位置）。
        Yields:
            RenderCommand: 渲染命令对象.
        """
        # 简化引用
        c = self.render_commands.center
        # 更新样式
        c.color = self.bgcolor
        c.dest_rect.update(rect)
        # 生成渲染命令
        yield c

    def crc_bwr_101(self, rect: fantas.RectLike):
        """
        有背景色，无边框，有圆角渲染命令生成器。
        Args:
            rect (fantas.RectLike): 矩形区域（绝对位置）。
        Yields:
            RenderCommand: 渲染命令对象.
        """
        # 简化引用
        rcs = self.render_commands
        t = rcs.top
        b = rcs.bottom
        c = rcs.center
        tl = rcs.topleft
        tr = rcs.topright
        bl = rcs.bottomleft
        br = rcs.bottomright
        quadrant = self.quadrant >> 2
        tr_on =  quadrant & 0b0001
        tl_on = (quadrant & 0b0010) >> 1
        bl_on = (quadrant & 0b0100) >> 2
        br_on = (quadrant & 0b1000) >> 3
        top = rect.top
        left = rect.left
        width = rect.width
        bottom = rect.bottom
        radius = self.border_radius
        radius_tl = radius if tl_on else 0
        radius_bl = radius if bl_on else 0
        top_radius = top + radius
        left_radius = left + radius
        right_radius = rect.right - radius - 1
        bottom_radius = bottom - radius - 1
        bgcolor = self.bgcolor
        # 更新样式并生成渲染命令
        t.color = b.color = c.color = bgcolor
        c.dest_rect.update(left            , top_radius, width, rect.height - 2 * radius)
        t.dest_rect.update(left + radius_tl, top                , width - radius_tl - (radius if tr_on else 0), radius)
        b.dest_rect.update(left + radius_bl, bottom - radius    , width - radius_bl - (radius if br_on else 0), radius)
        yield c
        yield t
        yield b
        if tl_on:
            tl.color, tl.center, tl.radius, tl.width = bgcolor, (left_radius, top_radius), radius, 0
            yield tl
        if tr_on:
            tr.color, tr.center, tr.radius, tr.width = bgcolor, (right_radius, top_radius), radius, 0
            yield tr
        if bl_on:
            bl.color, bl.center, bl.radius, bl.width = bgcolor, (left_radius, bottom_radius), radius, 0
            yield bl
        if br_on:
            br.color, br.center, br.radius, br.width = bgcolor, (right_radius, bottom_radius), radius, 0
            yield br

    def crc_bwr_110(self, rect: fantas.RectLike):
        """
        有背景色，有边框，无圆角渲染命令生成器。
        Args:
            rect (fantas.RectLike): 矩形区域（绝对位置）。
        Yields:
            RenderCommand: 渲染命令对象.
        """
        # 简化引用
        rcs = self.render_commands
        c  = rcs.center
        tb = rcs.top_border
        lb = rcs.left_border
        rb = rcs.right_border
        bb = rcs.bottom_border
        top = rect.top
        left = rect.left
        width = rect.width
        bw = self.border_width
        in_top = top + bw
        in_height = rect.height - 2 * bw
        # 更新样式
        c.color = self.bgcolor
        tb.color = bb.color = lb.color = rb.color = self.fgcolor
        c.dest_rect.update(rect.inflate(-bw, -bw))
        tb.dest_rect.update(left, top, width, bw)
        lb.dest_rect.update(left, in_top, bw, in_height)
        bb.dest_rect.update(left, rect.bottom - bw, width, bw)
        rb.dest_rect.update(rect.right - bw, in_top, bw, in_height)
        # 生成渲染命令
        yield c
        yield tb
        yield bb
        yield lb
        yield rb

    def crc_bwr_111(self, rect: fantas.RectLike):
        """
        有背景色，有边框，有圆角渲染命令生成器。
        Args:
            rect (fantas.RectLike): 矩形区域（绝对位置）。
        Yields:
            RenderCommand: 渲染命令对象.
        """
        # 简化引用
        rcs = self.render_commands
        t = rcs.top
        b = rcs.bottom
        c = rcs.center
        tl = rcs.topleft
        tr = rcs.topright
        bl = rcs.bottomleft
        br = rcs.bottomright
        tb = rcs.top_border
        lb = rcs.left_border
        rb = rcs.right_border
        bb = rcs.bottom_border
        tlb = rcs.topleft_border
        trb = rcs.topright_border
        blb = rcs.bottomleft_border
        brb = rcs.bottomright_border
        quadrant = self.quadrant >> 2
        tr_on =  quadrant & 0b0001
        tl_on = (quadrant & 0b0010) >> 1
        bl_on = (quadrant & 0b0100) >> 2
        br_on = (quadrant & 0b1000) >> 3
        bgcolor = self.bgcolor
        fgcolor = self.fgcolor
        left = rect.left
        top = rect.top
        width = rect.width
        height = rect.height
        right = rect.right
        bottom = rect.bottom
        bw = self.border_width
        radius = self.border_radius
        top_radius = top + radius
        left_radius = left + radius
        right_radius = right - radius - 1
        bottom_radius = bottom - radius - 1
        radius_tl = radius if tl_on else 0
        radius_tr = radius if tr_on else 0
        radius_bl = radius if bl_on else 0
        radius_br = radius if br_on else 0
        width_radius_tl_radius_tr = width - radius_tl - radius_tr
        width_radius_bl_radius_br = width - radius_bl - radius_br
        radius_bw = radius - bw
        left_radius_tl = left + radius_tl
        left_radius_bl = left + radius_bl
        # 更新样式并生成渲染命令
        c.color = t.color = b.color = bgcolor
        tb.color = bb.color = lb.color = rb.color = fgcolor
        c.dest_rect.update(left + bw, top_radius, width - 2 * bw, height - 2 * radius)
        t.dest_rect.update(left_radius_tl, top + bw, width_radius_tl_radius_tr, radius_bw)
        b.dest_rect.update(left_radius_bl, bottom_radius + 1, width_radius_bl_radius_br, radius_bw)
        tb.dest_rect.update(left_radius_tl, top, width_radius_tl_radius_tr, bw)
        bb.dest_rect.update(left_radius_bl, bottom - bw, width_radius_bl_radius_br, bw)
        lb.dest_rect.update(left, top + radius_tl, bw, height - radius_tl - radius_bl)
        rb.dest_rect.update(right - bw, top + radius_tr, bw, height - radius_tr - radius_br)
        yield c
        yield t
        yield b
        yield tb
        yield bb
        yield lb
        yield rb
        if bw > 1:
            bw -= 1
        if tl_on:
            tl_center = (left_radius, top_radius)
            tl.color, tl.center, tl.radius, tl.width = bgcolor, tl_center, radius_bw, 0
            tlb.color, tlb.center, tlb.radius, tlb.width = fgcolor, tl_center, radius, bw
            yield tl
            yield tlb
        if tr_on:
            tr_center = (right_radius, top_radius)
            tr.color, tr.center, tr.radius, tr.width = bgcolor, tr_center, radius_bw, 0
            trb.color, trb.center, trb.radius, trb.width = fgcolor, tr_center, radius, bw
            yield tr
            yield trb
        if bl_on:
            bl_center = (left_radius, bottom_radius)
            bl.color, bl.center, bl.radius, bl.width = bgcolor, bl_center, radius_bw, 0
            blb.color, blb.center, blb.radius, blb.width = fgcolor, bl_center, radius, bw
            yield bl
            yield blb
        if br_on:
            br_center = (right_radius, bottom_radius)
            br.color, br.center, br.radius, br.width = bgcolor, br_center, radius_bw, 0
            brb.color, brb.center, brb.radius, brb.width = fgcolor, br_center, radius, bw
            yield br
            yield brb

Label_crc_bwr_map = {
    0b010: Label.crc_bwr_010,
    0b011: Label.crc_bwr_011,
    0b100: Label.crc_bwr_100,
    0b101: Label.crc_bwr_101,
    0b110: Label.crc_bwr_110,
    0b111: Label.crc_bwr_111,
}

@dataclass(slots=True)
class SurfaceLabel(UI):
    """ 用于显示 Surface 对象的标签类 """
    father  : UI | None = field(default=None, init=False, repr=False)                     # 指向父显示元素
    children: list[UI]  = field(default_factory=list, init=False, repr=False)             # 子显示元素列表
    ui_id   : fantas.UIID      = field(default_factory=fantas.generate_unique_id, init=False)    # 唯一标识 ID

    surface  : fantas.Surface                                                                 # 显示的 Surface 对象
    rect     : fantas.RectLike = field(default_factory=fantas.DEFAULTRECT.copy)               # 矩形区域
    fill_mode: fantas.FillMode = fantas.FillMode.IGNORE                                       # 填充模式

    command  : fantas.SurfaceRenderCommand = field(init=False, repr=False)                    # 渲染命令对象

    def __post_init__(self):
        """ 初始化 SurfaceLabel 实例 """
        self.command = fantas.SurfaceRenderCommand(creator=self, surface=self.surface)

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
        c.dest_rect.update(rect)
        yield c
        # 生成子元素的渲染命令
        yield from UI.create_render_commands(self, offset)

@dataclass(slots=True)
class TextLine(UI):
    """ 纯色单行文本 UI 类 """
    children: None               = field(default=None, init=False, repr=False)    # 纯色文本不包含子元素

    text    : str                = 'text'                                     # 显示的文本内容
    style   : fantas.TextStyle   = field(default_factory=fantas.TextStyle)    # 文本样式
    origin  : fantas.Point       = (0, 0)                                     # 定位原点
    command : fantas.TextLineRenderCommand = field(init=False, repr=False)    # 文字渲染命令对象

    def __post_init__(self):
        """ 初始化 ColorTextLine 实例 """
        self.command = fantas.TextLineRenderCommand(creator=self)

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表。
        Args:
            offset (fantas.Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        # 简化引用
        rc = self.command
        # 设置文本内容
        rc.text = self.text
        # 设置文本样式
        rc.style = self.style
        # 设置文本原点
        rc.origin = (self.origin[0] + offset[0], self.origin[1] + offset[1])
        # 生成渲染命令
        yield rc

@dataclass(slots=True)
class Text(UI):
    """ 纯色多行文本 UI 类 """
    children: None               = field(default=None, init=False, repr=False)                 # 纯色文本不包含子元素

    text    : str                = 'text'                                                      # 显示的文本内容
    style   : fantas.TextStyle   = field(default_factory=fantas.TextStyle)                     # 文本样式
    line_spacing: float          = 4.0                                                         # 行间距
    rect    : fantas.RectLike    = field(default_factory=lambda: fantas.Rect(0, 0, 100, 0))    # 文本显示区域
    align_mode: fantas.AlignMode = fantas.AlignMode.LEFT                                       # 对齐模式
    reverse : bool               = False                                                       # 是否反向渲染文本

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
        # 设置文本样式
        rc.style = self.style
        # 设置行间距
        rc.line_spacing = self.line_spacing
        # 设置文本显示区域
        if isinstance(self.rect, fantas.Rect):
            rc.rect = fantas.IntRect(self.rect).move(offset)
        else:
            rc.rect = self.rect.move(offset)
        # 设置对齐模式
        rc.align_mode = self.align_mode
        # 设置反向渲染标志
        rc.reverse = self.reverse
        # 生成渲染命令
        yield rc

    def get_lineheight(self) -> float:
        """ 获取文本行高（包含行间距） """
        return self.style.font.get_sized_height(self.style.size) + self.line_spacing
    def set_lineheight(self, lineheight: float) -> None:
        """ 设置文本行高（包含行间距） """
        self.line_spacing = lineheight - self.style.font.get_sized_height(self.style.size)
    line_height = property(get_lineheight, set_lineheight)
