# fantas.fantas_typing

> fantas 的类型注解支持模块。

- **fantas.RectLike**
  表示矩形的对象，如数字序列或点数，或具有 `rect` 属性的对象，或返回矩形矩形的方法。这些类型由每个接受 rect 作为参数的函数支持。

  - `(left, top, width, height)`
  - `((left, top), (width, height))`
  - `fantas.Rect(RectLike)`
  - 任何含有 `rect` 属性并且这个属性是 `RectLike` 类型的对象。
  - 任何返回 `RectLike` 类型的对象的函数。

  需要声明两点：
  1. fantas 里的所有 `Rect` 对象都是浮点矩形。
  2. 虽然说 `RectLike` 支持多种类型，但是在传递参数时，建议使用 `fantas.Rect` 对象，因为它是最通用且功能最完整的矩形类型。使用其他类型可能会导致一些意想不到的问题。

- **fantas.ColorLike**
  表示颜色的对象，如映射整数、字符串或范围为0-255的三至四个整数序列，类型由每个接受颜色参数的函数支持。

  - `fantas.Color(ColorLike)`
  - `(r, g, b)` 或 `(r, g, b, a)` 或 `[r, g, b]` 或 `[r, g, b, a]`，其中 r、g、b、a 的取值范围为 0-255 的整数。
  - `"green"`，一些常用颜色的名称字符串，具体可以参考 [Named Colors](https://pyga.me/docs/ref/color_list.html)。
  - `#rrgdbb` 或 `#rrggbbaa`，十六进制颜色字符串表示法。

同样，使用 `fantas.Color` 对象是最通用且功能最完整的颜色类型，建议优先使用它。

- **fantas.Point**
  两个数字（float 或 int）组成的序列。

  - `(x, y)` 或 `[x, y]`

- **fantas.IntPoint**
  两个严格整数（int）组成的序列。

  - `(x, y)` 或 `[x, y]`

- **fantas.EventType**
  事件类型。
  实际上是一个 `int` 对象，表示事件的类型代码，为了便于观察，可以使用 fantas 定义的常量，比如 `fantas.QUIT`。

- **fantas.UIID**
  UI 元素唯一标识类型。
  实际上是一个 `int` 对象，表示 UI 元素的唯一标识符。

- **fantas.ListenerKey**
  监听器键类型。
  一个三元组，包含事件类型（`fantas.EventType`）、UI 元素唯一标识（`fantas.UIID`）和是否为捕获阶段（`bool`）。

- **fantas.ListenerFunc**
  监听器函数类型。
  一个可调用对象，接受一个 `pygame.event.Event` 对象作为参数，并返回一个布尔值。
