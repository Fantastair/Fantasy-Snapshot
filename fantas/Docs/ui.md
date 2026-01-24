# fantas.UI

> fantas 显示元素模块

在 fantas 中，所有内容的显示都是通过 UI 类来实现的。各个显示元素之间以树形结构组织，树形结构的操作由 `fantas.Nodebase` 类提供支持。UI 类在 `fantas.Nodebase` 的基础上增加了显示相关的属性和方法。

## fantas.UI

显示元素基类。

`UI() -> fantas.UI`

### 属性

- **father (UI | None)**: 指向父显示元素。
- **children (List[UI\])**: 子显示元素列表。
- **ui_id (fantas.UIID)**: 显示元素唯一标识符，自动生成。
  在一整个程序中，所有显示元素的 `ui_id` 都是唯一的，即使显示元素被删除后，其 `ui_id` 也不会被回收。

如果你有特殊需求，可以创建一个空的 `UI` 对象，它不会进行任何渲染，但是可以传递子元素的渲染命令。窗口的根元素就是一个空的 `UI` 对象，用来执行某些预设的事件处理。

### 方法

- **UI.create_render_commands()**:
  创建渲染命令列表（包括子元素的）。
  `create_render_commands(offset: fantas.Point = (0, 0)`
  返回一个生成器。
  `UI` 类自己不会生成任何渲染命令，但是会递归调用子元素的 `create_render_commands` 方法，并将偏移量传递给子元素。
  子类可以重写此方法以生成自己的渲染命令。

## fantas.ColorBackground

纯色背景 UI 类。

``` python
ColorBackground(
    bgcolor : fantas.ColorLike = 'black'
) -> fantas.ColorBackground
```

### 属性

- **father (UI | None)**: 指向父显示元素。
- **children (List[UI\])**: 子显示元素列表。
- **ui_id (fantas.UIID)**: 唯一标识 ID。
- **bgcolor (fantas.ColorLike)**: 背景颜色。
- **command (fantas.ColorBackgroundFillCommand)**: 用于填充背景颜色的渲染命令。

## fantas.Label

纯色矩形 UI 类。

``` python
Label(
    bgcolor: fantas.ColorLike | None   = 'black'
    fgcolor: fantas.ColorLike          = 'white'
    rect   : fantas.RectLike           = fantas.Rect(0, 0, 100, 50)
    border_radius: int | float         = 0.0
    border_width : int | float         = 0.0
    quadrant     : fantas.QuadrantMask = 0b111111
    box_mode     : fantas.BoxMode      = fantas.BoxMode.INSIDE
) -> fantas.Label
```

### 属性

- **father (UI | None)**: 指向父显示元素。
- **children (List[UI\])**: 子显示元素列表。
- **ui_id (fantas.UIID)**: 唯一标识 ID。
- **bgcolor (fantas.ColorLike)**: 矩形颜色。
- **fgcolor (fantas.ColorLike)**: 边框颜色。
- **rect (fantas.RectLike)**: 矩形区域。
- **border_radius (int | float)**: 边框圆角半径。
- **border_width (int | float)**: 边框宽度。
- **quadrant (fantas.QuadrantMask)**: 指定哪些角是圆角。
- **box_mode (fantas.BoxMode)**: 边框绘制模式。
- **render_commands (LabelRenderCommands)**: 渲染命令容器。

## fantas.SurfaceLabel

显示图像的矩形 UI 类。

``` python
SurfaceLabel(
    surface : fantas.SurfaceLike
    rect    : fantas.RectLike        = fantas.DEFAULTRECT
    fill_mode: fantas.FillMode      = fantas.FillMode.IGNORE
) -> fantas.SurfaceLabel
```

### 属性

- **father (UI | None)**: 指向父显示元素。
- **children (List[UI\])**: 子显示元素列表。
- **ui_id (fantas.UIID)**: 唯一标识 ID。
- **surface (fantas.SurfaceLike)**: 显示的 `Surface` 对象。
- **rect (fantas.RectLike)**: 矩形区域。
- **fill_mode (fantas.FillMode)**: 填充模式。
- **command (fantas.SurfaceRenderCommand)**: 用于绘制图像的渲染命令。

## fantas.TextLine

纯色单行文本 UI 类。

``` python
TextLine(
    text    : str                = 'text'
    font    : fantas.Font        = fantas.DEFAULTFONT
    fgcolor : fantas.ColorLike   = 'black'
    size    : float              = 16.0
    origin  : fantas.Point       = (0, 0)
) -> fantas.TextLine
```

### 属性

- **father (UI | None)**: 指向父显示元素。
- **children (None)**: 该类不允许有子元素。
- **ui_id (fantas.UIID)**: 唯一标识 ID。
- **text (str)**: 显示的文本内容。
- **font (fantas.Font)**: 字体。
- **fgcolor (fantas.ColorLike)**: 文本颜色。
- **size (float)**: 字体大小。
- **origin (fantas.Point)**: 定位原点。
- **command (fantas.TextLineRenderCommand)**: 用于绘制文本的渲染命令。
