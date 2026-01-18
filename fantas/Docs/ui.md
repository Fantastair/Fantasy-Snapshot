# fantas.UI

> fantas 显示元素模块

在 fantas 中，所有内容的显示都是通过 UI 类来实现的。各个显示元素之间以树形结构组织，树形结构的操作由 `fantas.Nodebase` 类提供支持。UI 类在 `fantas.Nodebase` 的基础上增加了显示相关的属性和方法。

## fantas.UI

显示元素基类。

`UI() -> fantas.UI`

### 属性

一个空的显示元素初始化时不需要提供任何参数。

- **father (UI | None)**: 指向父显示元素。
- **children (List[UI\])**: 子显示元素列表。
- **ui_id (int)**: 显示元素唯一标识符，自动生成。
  在一整个程序中，所有显示元素的 `ui_id` 都是唯一的，即使显示元素被删除后，其 `ui_id` 也不会被回收。

### 方法

- **UI.create_render_commands()**:
  创建渲染命令列表（包括子元素的）。
  `create_render_commands(offset: fantas.Point = (0, 0)`
  返回一个生成器。
  `UI` 类自己不会生成任何渲染命令，但是会递归调用子元素的 `create_render_commands` 方法，并将偏移量传递给子元素。
  子类可以重写此方法以生成自己的渲染命令。

## fantas.ColorBackground

纯色背景 UI 类。

### 属性

- **color (fantas.Color)**: 背景颜色。

### 方法

- **ColorBackground.create_render_commands()**:
  创建渲染命令列表（包括子元素的）。
  `create_render_commands(offset: fantas.Point = (0, 0)`
  返回一个生成器。
  该方法会生成一个填充矩形的渲染命令，然后递归调用子元素的 `create_render_commands` 方法，并将偏移量传递给子元素。

## fantas.ColorLabel

纯色矩形 UI 类。

### 属性

- **color (fantas.Color)**: 矩形颜色。
- **rect (fantas.Rect)**: 矩形区域。

### 方法

- **ColorLabel.create_render_commands()**:
  创建渲染命令列表（包括子元素的）。
  `create_render_commands(offset: fantas.Point = (0, 0)`
  返回一个生成器。
  该方法会生成一个填充矩形的渲染命令，然后递归调用子元素的 `create_render_commands` 方法，并将偏移量传递给子元素。

## fantas.ColorTextLine

纯色单行文本 UI 类。

### 属性

- **children (None)**: 该类不允许有子元素。
- **text (str)**: 显示的文本内容。
- **font (fantas.Font)**: 字体。
- **color (fantas.Color)**: 文本颜色。
- **size (float)**: 字体大小。
- **rect (fantas.Rect)**: 定位矩形。

### 方法

- **ColorTextLine.create_render_commands()**:
  创建渲染命令列表（包括子元素的）。
  `create_render_commands(offset: fantas.Point = (0, 0)`
  返回一个生成器。
  该方法会生成一个绘制文本的渲染命令，然后递归调用子元素的 `create_render_commands` 方法，并将偏移量传递给子元素。
