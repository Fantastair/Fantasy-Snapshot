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

### 属性

- **father (UI | None)**: 指向父显示元素。
- **children (List[UI\])**: 子显示元素列表。
- **ui_id (fantas.UIID)**: 唯一标识 ID。
- **bgcolor (fantas.ColorLike)**: 背景颜色。
- **color_fill_command (fantas.ColorFillCommand)**: 用于填充背景颜色的渲染命令。

初始化 `ColorBackground` 时，你应该只提供 `bgcolor` 参数。

### 方法

- **ColorBackground.set_bgcolor()**:
  设置背景颜色。
  `set_bgcolor(color: fantas.ColorLike)`
  该方法会更新 `bgcolor` 属性和 `color_fill_command` 属性。

- **ColorBackground.create_render_commands()**:
  创建渲染命令列表（包括子元素的）。
  `create_render_commands(offset: fantas.Point = (0, 0)`
  返回一个生成器。
  该方法会生成一个填充矩形的渲染命令，然后递归调用子元素的 `create_render_commands` 方法，并将偏移量传递给子元素。

## fantas.ColorLabel

纯色矩形 UI 类。

### 属性

- **father (UI | None)**: 指向父显示元素。
- **children (List[UI\])**: 子显示元素列表。
- **ui_id (fantas.UIID)**: 唯一标识 ID。
- **bgcolor (fantas.ColorLike)**: 矩形颜色。
- **rect (fantas.RectLike)**: 矩形区域。
- **color_fill_command (fantas.ColorFillCommand)**: 用于填充矩形颜色的渲染命令。

### 方法

- **ColorLabel.set_bgcolor()**:
  设置矩形颜色。
  `set_bgcolor(color: fantas.ColorLike)`
  该方法会更新 `bgcolor` 属性和 `color_fill_command` 属性。
- **ColorLabel.set_rect()**:
  设置矩形区域。
  `set_rect(rect: fantas.RectLike)`
  该方法会更新 `rect` 属性。
- **ColorLabel.create_render_commands()**:
  创建渲染命令列表（包括子元素的）。
  `create_render_commands(offset: fantas.Point = (0, 0)`
  返回一个生成器。
  该方法会生成一个填充矩形的渲染命令，然后递归调用子元素的 `create_render_commands` 方法，并将偏移量传递给子元素。

## fantas.ColorTextLine

纯色单行文本 UI 类。

### 属性

- **father (UI | None)**: 指向父显示元素。
- **children (None)**: 该类不允许有子元素。
- **ui_id (fantas.UIID)**: 唯一标识 ID。
- **text (str)**: 显示的文本内容。
- **font (fantas.Font)**: 字体。
- **fgcolor (fantas.ColorLike)**: 文本颜色。
- **size (float)**: 字体大小。
- **rect (fantas.RectLike)**: 定位矩形。
- **color_text_line_render_command (fantas.ColorTextLineRenderCommand)**: 用于绘制文本的渲染命令。

### 方法

- **ColorTextLine.set_text()**:
  设置显示的文本内容。
  `set_text(text: str)`
  该方法会更新 `text` 属性和 `color_text_line_render_command` 属性。
- **ColorTextLine.set_font()**:
  设置字体。
  `set_font(font: fantas.Font)`
  该方法会更新 `font` 属性和 `color_text_line_render_command` 属性。
- **ColorTextLine.set_fgcolor()**:
  设置文本颜色。
  `set_fgcolor(color: fantas.ColorLike)`
  该方法会更新 `fgcolor` 属性和 `color_text_line_render_command` 属性。
- **ColorTextLine.set_size()**:
  设置字体大小。
  `set_size(size: float)`
  该方法会更新 `size` 属性和 `color_text_line_render_command` 属性。
- **ColorTextLine.set_rect()**:
  设置定位矩形。
  `set_rect(rect: fantas.RectLike)`
  该方法会更新 `rect` 属性。
- **ColorTextLine.create_render_commands()**:
  创建渲染命令列表（包括子元素的）。
  `create_render_commands(offset: fantas.Point = (0, 0)`
  返回一个生成器。
  该方法会生成一个绘制文本的渲染命令，然后递归调用子元素的 `create_render_commands` 方法，并将偏移量传递给子元素。
