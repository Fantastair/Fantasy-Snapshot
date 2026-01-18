# fantas.renderer

> fantas 渲染模块
这是 fantas 的高级模块（或者说底层模块），只有在你需要自定义显示元素时才需要了解，如果你只使用 fantas 提供的 UI 类，那么你不会接触到这里的内容，不过也可以了解一下 fantas 的底层逻辑。

在 fantas 中，所有对窗口内容的绘制都是通过渲染命令实现的，发送渲染命令并不会立即开始渲染，而是会在下一次执行渲染操作时一起绘制并刷新显示。这样做的好处是渲染命令的顺序代表了实际渲染元素的层叠顺序，将原本树形的非线性元素关系转化为顺序的线性关系，有利于事件处理等操作，并且可以集中优化渲染流程以提升性能。

所有的渲染命令都有一个基类：

## fantas.RenderCommand

基类的实现不完整，无法直接使用，其他渲染命令都应该继承自这个基类，补全相应的功能。
每个渲染命令至少包括 2 个要素：

- **creator**
  渲染命令的创建者。
  `creator -> fantas.UI`
  这个属性对于渲染来说是不必要的，但是对于前面讲的层叠信息判断很有帮助。

- **render()**
  具体的渲染函数，基类未定义，由子类实现。
  `render(target_surface: fantas.Surface)`
  子类在这个函数里需要将渲染的内容绘制到目标 Surface 上。
  这个方法不会被直接调用，所以一定要按照规则定义。

## fantas.SurfaceRenderCommand

Surface 渲染命令，直接将一个 Surface 对象绘制在目标 Surface 上。

``` python
SurfaceRenderCommand(
    creator:   fantas.UI,
    surface:   fantas.Surface,
    dest_rect: fantas.RectLike,
) -> SurfaceRenderCommand
```

参数：

- surface (fantas.Surface): 要绘制的 Surface 对象。
- dest_rect (fantas.Rect): 绘制的矩形区域（相对于目标 Surface）。

## fantas.ColorFillCommand

纯色填充命令，在特定区域填充颜色。

``` python
ColorFillCommand(
    creator: fantas.UI,
    color: fantas.ColorLike,
    dest_rect: fantas.RectLike | None = None,
) -> ColorFillCommand
```

参数：

- color (fantas.ColorLike): 用于填充的颜色。
- dest_rect (fantas.RectLike | None): 目标矩形区域，指定填充的位置和大小，如果设为 None，则会填满整个目标 Surface（这通常用于覆盖内容，比如纯色背景）。

## fantas.ColorTextLineRenderCommand

纯色单行文本绘制命令。

``` python
ColorTextLineRenderCommand(
    creator: fantas.UI,
    text: str,
    font: fantas.Font,
    size: float,
    fgcolor: fantas.ColorLike | None,
    dest_rect: fantas.RectLike,
) -> ColorTextLineRenderCommand
```

参数：

- text (str): 要渲染的文本内容
- font (fantas.Font): 字体对象
- size (float): 字体大小
- fgcolor (fantas.ColorLike | None): 文字颜色
- dest_rect (fantas.RectLike): 目标矩形区域，指定文本的渲染位置和大小
