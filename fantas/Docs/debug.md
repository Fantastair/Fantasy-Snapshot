# fantas.debug

> fantas 调试模块

此模块用于提供 fantas 的调试支持，可以方便的获取并设置一些窗口的状态。该模块会在子进程中打开一个调试窗口用于调试，值得一提的是，这个调试窗口也是用 fantas 开发的。

## fantas.Debug

这是一个静态类，封装一些调试函数。

- **fantas.Debug.open_debug_window()**
  在子进程中打开调试窗口。
  `open_debug_window(left: int = 0, top: int = 0, width: int = 1280, height: int = 720, close_with_main: bool = True, opacity: float = 1.0)`
  参数：
  - left (int): 窗口左上角的 X 坐标位置。
  - top (int): 窗口左上角的 Y 坐标位置。
  - width (int): 窗口宽度（像素）。
  - height (int): 窗口高度（像素）。
  - close_with_main (bool): 主进程关闭时是否关闭调试窗口子进程。
  - opacity (float): 窗口透明度，范围 0.0 - 1.0。
  注意，除非主窗口使用 `mainloop_debug()`，否则调试窗口是受不到任何调试信息的。同一个程序只能有一个调试窗口，多次打开会先关闭原来的窗口。
  如果你希望主程序结束后调试窗口还能保留，那么将 `close_with_main` 参数设置为 `False`，这样你可以在关闭主窗口后继续观察调试窗口的信息（当然这之后信息不会更新了）
