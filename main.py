import fantas

# 创建主窗口
window_config = fantas.WindowConfig(
    title = "幻想快照",
    window_size = (1920, 1080),
)
window = fantas.Window(window_config)

linear_gradient = fantas.LinearGradientLabel(
    rect = fantas.Rect((0, 0), (1920, 1080)),
    start_color = fantas.Color(255, 0, 0),
    end_color   = fantas.Color(0, 0, 255),
    start_pos   = (0, 0),
    end_pos     = (1920, 0),
)
window.append(linear_gradient)

# 运行主循环
# window.mainloop()

# 调试模式
fantas.Debug.start_debug(flag=fantas.DebugFlag.ALL, windows_title=window.title)
window.mainloop_debug()
