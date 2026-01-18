# fantas.window

> fantas 窗口模块

这个模块提供窗口类,负责驱动窗口。

## fantas.WindowConfig

窗口配置类。

``` python
WindowConfig(
    title          : str                   = "Fantas Window"
    window_size    : fantas.IntPoint       = (1280, 720)
    window_position: fantas.IntPoint | int = fantas.WINDOWPOS_UNDEFINED
    borderless     : bool                  = False
    resizable      : bool                  = False
    fps            : int                   = 60
    mouse_focus    : bool                  = True
    input_focus    : bool                  = True
    allow_high_dpi : bool                  = True
) -> WindowConfig
```

- **title (str)**: 窗口标题。
- **window_size (fantas.IntPoint)**: 窗口尺寸（宽，高）（像素）
- **window_position (fantas.IntPoint | int)**: 窗口初始位置。
  可以使用自定义坐标，也可以使用预设常量：
  
  - `fantas.WINDOWPOS_CENTERED`：窗口居中显示。
  - `fantas.WINDOWPOS_UNDEFINED`：由系统决定窗口初始位置。
- **borderless (bool)**: 窗口是否无边框。
  需要说明的是，窗口的边框不仅仅是装饰作用，还承担着窗口控制的作用，比如拖动、调整大小、最小化、最大化、关闭等功能。如果将窗口设置为无边框，这些功能也会一并被移除，在你得到全平台一致的无边框窗口体验的同时，也需要自己实现这些功能。并且，很多桌面都会为窗口添加阴影效果，而无边框窗口通常无法显示阴影。
- **resizable (bool)**: 是否可以调整窗口大小。
  这里的调整大小是指用户通过拖动窗口边框来调整窗口尺寸。无论否允许调整大小，程序都可以通过代码来直接改变窗口尺寸（在    `Window` 类中有介绍）。
- **fps (int)**: 窗口帧率。
  窗口在每一轮主循环里会刷新一帧画面，所以这个参数控制的实质上是主循环的频率，它不仅仅影响画面刷新的频率，还会影响事件处理等主循环内操作的频率。
- **mouse_focus (bool)**: 窗口是否在创建时获得鼠标焦点。
- **input_focus (bool)**: 窗口是否在创建时获得输入焦点。
- **allow_high_dpi (bool)**: 是否允许高 DPI 显示。
  这个参数只针对 macOS 和 Linux 平台生效，在 Windows 平台上，fantas 默认设置高 DPI 感知为 Per Monitor V2 模式（也就是开启高 DPI 支持）。
  对于 macOS 平台，需要说明的是，如果你的显示器是 Retina（视网膜）屏幕，并且开启了 hidpi，那么系统一般会以 2 倍逻辑分辨率渲染窗口内容，一旦你同时启用高 DPI 支持，就会得到一个 2 倍大小的窗口，然而鼠标等坐标事件仍然是基于逻辑分辨率的，这就会导致鼠标位置和窗口内容位置不匹配的问题。如果你不希望出现这种情况，可以关闭高 DPI 支持。
  如果你想知道是否开启高 DPI 支持有什么区别，简单来说，系统在高分辨率的屏幕上为了使得显示的内容物理尺寸合适观看，会施加一个缩放因子，如果你的程序没有开启高 DPI 支持，那么系统会在渲染后对画面进行缩放处理，这样会导致画面模糊；开启高 DPI 支持后，系统不会缩放你的程序窗口，这样你就可以直接以高分辨率渲染画面，从而获得更清晰的显示效果。不过这也意味着你需要处理好不同 DPI 下的界面布局问题。

这个类唯一的作用就是整合信息，没有任何方法，你可以当成C语言的结构体。不过所有的参数都有默认值，所以你可以只提供你想修改的参数。

## fantas.Window

窗口类，每一个实例就是一个窗口。
`Window(window_config: WindowConfig) -> Window`

允许同时创建多个实例来管理多个窗口，不过在单线程模式下，同时只能运行一个窗口的主循环，因此一般会用一个窗口作为主窗口，其他窗口作为子窗口临时弹出（比如对话框）。
创建实例时，需要提供一个 WindowConfig 类型的参数，同一个 WindowConfig 对象可以多次使用。注意：WindowConfig 对象只在初始化 Window 实例时生效，后续的变化不会影响到窗口本身。

属性：

- **running**
  读取或设置窗口的运行状态。
  `running -> bool`
  初始值为 `True`，表示窗口处于运行状态，当设置为 `False` 后，会在运行完当前循环后退出主循环并关闭窗口。

- **fps**
  读取或设置帧率，默认 60 帧/秒。
  `fps -> int`
  窗口在每一轮主循环里会刷新一帧画面，所以这个属性控制的实质上是主循环的频率，它不仅仅影响画面刷新的频率，还会影响事件处理等主循环内操作的频率。
  这个参数可以在运行时修改，会在下一轮主循环生效。它影响的是主循环的最大频率，也就是说如果主循环内的操作耗时过长，实际帧率会低于这个值。

- **clock**
  窗口的时钟对象。
  `clock -> fantas.time.Clock`
  通过这个对象可以获取时间相关的信息，比如当前的实际帧率等。

- **screen**
  窗口的绘图表面对象。
  `screen -> fantas.Surface`
  这个对象是一个 `fantas.Surface` 实例，和窗口的内容绘制直接相关，在这个表面上的绘制可以刷新到窗口上。

- **renderer**
  窗口的渲染器对象。
  `renderer -> fantas.Renderer`
  通过这个对象可以对窗口内容进行渲染操作，一般情况下不需要直接使用它，因为窗口会在主循环内自动调用渲染器来渲染。

- **event_handler**
  窗口的事件处理器对象。
  `event_handler -> fantas.EventHandler`
  通过这个对象可以管理窗口的事件处理，比如添加或移除事件监听器等。
  `fantas.EventHandler` 有 `append_listener()` 和 `remove_listener()` 方法，可以用来添加或移除事件监听，但是调用比较麻烦：`window.event_handler.add_event_listener(...)`，所以窗口类直接将这两个方法放到了自己的命名空间下，方便调用：`window.add_event_listener（...）`。

- **root_ui**
  窗口的根 UI 元素。
  `root_ui -> fantas.UI`
  这是窗口保留的一个空的根节点 UI 元素，它不会渲染任何内容，但是你不应该删除或更改这个节点，向窗口上添加元素的方式就是将它们添加到这个根节点下。
  窗口类也将根 UI 元素的 `append()` `insert()` `remove()` `pop()` `clear()` 方法放到了自己的命名空间下，方便调用：`window.append(...)`。

方法：

- **mainloop()**
  进入窗口的主事件循环，直到窗口关闭。
  `mainloop()`
  进入主循环会阻塞，直到退出循环，一般作为整个程序的最后一行代码，当然，你也可以在退出窗口后做一些收尾工作，或者这个窗口并不是主窗口。
  主循环内会执行以下操作：
  - 获取并处理事件
  - 渲染并更新窗口
  每两轮循环之间的所有事件都会存放在一个队列里，等到下一轮循环一次性取出并处理。如果主循环卡住，或者你调整了 `fps` 属性使得事件处理的频率太低，都有可能导致事件队列塞满，这时新的事件无法进入队列，并且系统可能认定你的程序未响应。

- **handle_windowclose_event()**
  处理窗口关闭事件。
  `handle_windowclose_event(event: fantas.Event)`
  这个方法会在监听到 `WINDOWCLOSE` 事件时调用。

- **mainloop_debug()**
  以调试模式进入窗口的主事件循环，直到窗口关闭。
  `mainloop_debug()`
  和普通主循环的区别在于会发送调试信息给调试窗口，只有在调试窗口打开时才会生效，如果你没有使用调试窗口的需要，不要使用这个函数，通信是会消耗性能的。

- **handle_debug_output()**
  处理从调试窗口接收到的输出信息。
  `handle_debug_output(output: str)`
  在这里可以处理从调试窗口接收到的输出信息，比如执行一些调试命令等。
