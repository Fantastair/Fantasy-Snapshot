import fantas

# 创建主窗口
window_config = fantas.WindowConfig(
    title = "Fantas3 Demo",
    window_size = (1920, 1080),
)
window = fantas.Window(window_config)

# 创建背景
background = fantas.ColorBackground(bgcolor=fantas.Color("#e3e3e3"))
window.append(background)

# 创建测试标签
test_label = fantas.ColorLabel(
    bgcolor=fantas.Color("#3498db"),
    fgcolor=fantas.Color("#303030"),
    rect=fantas.Rect(100, 100, 400, 200),
    border_radius=40,
    border_width=8,
    box_mode=fantas.BoxMode.OUTSIDE,
    quadrant=fantas.Quadrant.TOPLEFT | fantas.Quadrant.BOTTOMRIGHT,
)
background.append(test_label)
test_label.rect.center = (window.size[0] // 2, window.size[1] // 2)

# 创建测试文字行
test_text = fantas.ColorTextLine(
    rect=fantas.Rect(0, 0, 0, 0),
    text="Hello Fantas3!",
    size=48.0,
)
test_label.append(test_text)

def enter_test_label(event: fantas.Event) -> bool:
    """ 鼠标移入测试标签时的回调函数。 """
    if event.ui is test_label:
        test_label.bgcolor = fantas.Color("#29b952")    # 设置背景色为绿色

def leave_test_label(event: fantas.Event) -> bool:
    """ 鼠标移出测试标签时的回调函数。 """
    if event.ui is test_label:
        test_label.bgcolor = fantas.Color("#3498db")    # 恢复背景色为蓝色

count = 0
def click_test_label(event: fantas.Event) -> bool:
    """ 鼠标点击测试标签时的回调函数。 """
    global count
    if event.ui is test_label:
        count += 1
        print(f"测试标签被点击了{count}次！")

window.add_event_listener(fantas.MOUSEENTERED, test_label, False, enter_test_label)    
window.add_event_listener(fantas.MOUSELEAVED,  test_label, False, leave_test_label)
window.add_event_listener(fantas.MOUSECLICKED, test_label, False, click_test_label)

# 运行主循环
window.mainloop()

# 调试模式
# fantas.Debug.open_debug_window(window, 0, 0, 2557, (1600 - window.size[1]) // 2 - 50)
# window.mainloop_debug()
