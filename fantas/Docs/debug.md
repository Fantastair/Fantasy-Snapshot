# fantas.debug

> fantas 调试模块

此模块用于提供 fantas 的调试支持，可以方便的获取并设置一些窗口的状态。该模块会在子进程中打开一个调试窗口用于调试，值得一提的是，这个调试窗口也是用 fantas 开发的。

## fantas.Debug

这是一个静态类，封装一些调试函数。

- **fantas.Debug.start_debug()**
  启动调试窗口子进程。
  `start_debug(flag: fantas.DebugFlag = fantas.DebugFlag.ALL, windows_title: str = "Fantas 调试窗口")`
  参数：
  - `flag`: 调试选项标志，指定启用哪些调试选项，默认为 `fantas.DebugFlag.ALL`，即启用所有调试选项。
  - `windows_title`: 调试窗口的标题，默认为 `"Fantas 调试窗口"`。

  注意，除非主窗口使用 `mainloop_debug()`，否则调试窗口是受不到任何调试信息的。同一个程序只能有一套调试窗口，多次打开会先关闭原来的窗口。

## fantas.DebugFlag
  调试选项标志枚举。

  - EVENTLOG = 1
    事件日志选项标志，启用后会记录 fantas 事件日志。
  - TIMERECORD = 2
    时间记录选项标志，启用后会记录 fantas 各个操作的时间消耗。
  - MOUSEMAGNIFY = 4
    鼠标放大选项标志，启用后会在调试窗口中显示鼠标位置的放大截图。
  - ALL
    全部选项标志，启用所有调试选项。
  - NONE
    无选项标志，禁用所有调试选项。
