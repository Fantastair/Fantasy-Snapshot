import fantas

# 创建主窗口
window_config = fantas.WindowConfig(
    title = "幻想快照",
    window_size = (1920, 1080),
)
window = fantas.Window(window_config)

# 运行主循环
window.mainloop()

# 调试模式
# fantas.Debug.start_debug(flag=fantas.DebugFlag.TIMERECORD, windows_title=window.title)
# window.mainloop_debug()
