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
    # bgcolor=None,
    bgcolor=fantas.Color("#3498db"),
    fgcolor=fantas.Color("#303030"),
    rect=fantas.Rect(100, 100, 400, 200),
    border_radius=40,
    border_width=8,
    # quadrant=fantas.Quadrant.TOPLEFT | fantas.Quadrant.BOTTOMRIGHT,
)
background.append(test_label)
test_label.rect.center = (window.size[0] // 2, window.size[1] // 2)

# 创建测试文字行
test_text = fantas.ColorTextLine(
    rect=fantas.Rect(0, 0, 0, 0),
    text="Hello Fantas3!",
    size=48.0,
)
# test_label.append(test_text)

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

# window.add_event_listener(fantas.MOUSEENTERED, test_label, False, enter_test_label)    
# window.add_event_listener(fantas.MOUSELEAVED,  test_label, False, leave_test_label)
# window.add_event_listener(fantas.MOUSECLICKED, test_label, False, click_test_label)

class TestSlider:
    """
    测试滑块组件。
    """
    def __init__(self, name: str, topleft: tuple[int, int], start: float, end: float, init_value: float, set_func):
        self.start = start
        self.end = end
        self.value = init_value
        self.set_func = set_func
        self.name_text = fantas.ColorTextLine(
            text=name,
            size=32,
            rect=fantas.Rect(topleft, (0, 0)),
        )
        background.append(self.name_text)
        self.slider_bar = fantas.ColorLabel(
            bgcolor=fantas.Color("#888888"),
            fgcolor=fantas.Color("#303030"),
            rect=fantas.Rect(topleft[0] + 120, topleft[1] + 4, 400, 24),
            border_radius=12,
            border_width=4,
        )
        background.append(self.slider_bar)
        self.active_bar = fantas.ColorLabel(
            bgcolor=fantas.Color("#6EDE3A"),
            rect=fantas.Rect(4, 4, 0, 16),
            border_radius=8,
        )
        self.slider_bar.append(self.active_bar)
        self.slider = fantas.ColorLabel(
            bgcolor=fantas.Color("#888888"),
            fgcolor=fantas.Color("#303030"),
            rect=fantas.Rect(0, 0, 24, 24),
            border_radius=12,
            border_width=4,
        )
        self.slider_activated = False
        self.slider_bar.append(self.slider)
        self.value_text = fantas.ColorTextLine(
            text="",
            size=24,
            rect=fantas.Rect(topleft[0] + 560, topleft[1] + 4, 0, 0),
        )
        background.append(self.value_text)
        window.add_event_listener(fantas.MOUSEENTERED, self.slider, False, self.mouse_enter_slider)
        window.add_event_listener(fantas.MOUSELEAVED, self.slider, False, self.mouse_leave_slider)
        window.add_event_listener(fantas.MOUSEBUTTONDOWN, background, False, self.activate_slider)
        window.add_event_listener(fantas.MOUSEBUTTONUP, background, False, self.deactivate_slider)
        window.add_event_listener(fantas.MOUSEMOTION, background, False, self.move_slider)
        self.set_value(init_value)

    def set_value(self, value: float):
        """ 设置滑块的值。 """
        self.value = max(self.start, min(self.end, value))
        ratio = (self.value - self.start) / (self.end - self.start)
        self.slider.rect.left = ratio * (self.slider_bar.rect.width - self.slider.rect.width)
        self.active_bar.rect.width = self.slider.rect.centerx - self.active_bar.rect.left
        if self.name_text.text == "bw":
            self.value_text.text = f"{int(self.value)}"
        else:
            self.value_text.text = f"{self.value:.2f}"

    def mouse_enter_slider(self, event: fantas.Event) -> bool:
        if event.ui is self.slider:
            self.slider.bgcolor = fantas.Color("#6EDE3A")
        return False

    def mouse_leave_slider(self, event: fantas.Event) -> bool:
        if not self.slider_activated and event.ui is self.slider:
            self.slider.bgcolor = fantas.Color("#888888")
        return False

    def activate_slider(self, event: fantas.Event) -> bool:
        if not self.slider_activated and event.button == fantas.BUTTON_LEFT and window.event_handler.hover_ui is self.slider:
            self.slider_activated = True
        return False

    def deactivate_slider(self, event: fantas.Event) -> bool:
        if self.slider_activated and event.button == fantas.BUTTON_LEFT:
            self.slider_activated = False
            if self.slider.bgcolor == fantas.Color("#6EDE3A"):
                self.slider.bgcolor = fantas.Color("#888888")
        return False

    def move_slider(self, event: fantas.Event) -> bool:
        if self.slider_activated:
            mouse_x = event.pos[0] - self.slider_bar.rect.left
            ratio = (mouse_x - self.slider.rect.width / 2) / (self.slider_bar.rect.width - self.slider.rect.width)
            value = self.start + ratio * (self.end - self.start)
            self.set_value(value)
            self.set_func(self.value)
        return False

top_slider    = TestSlider("top",    (10, 10 + 40 * 1), 0.0, window.size[1], test_label.rect.top,      lambda v: setattr(test_label.rect, 'top', v))
left_slider   = TestSlider("left",   (10, 10 + 40 * 0), 0.0, window.size[0], test_label.rect.left,     lambda v: setattr(test_label.rect, 'left', v))
width_slider  = TestSlider("width",  (10, 10 + 40 * 2), 0.0, window.size[0], test_label.rect.width,    lambda v: setattr(test_label.rect, 'width', v))
height_slider = TestSlider("height", (10, 10 + 40 * 3), 0.0, window.size[1], test_label.rect.height,   lambda v: setattr(test_label.rect, 'height', v))
radius_slider = TestSlider("radius", (10, 10 + 40 * 4), 0.0, 400.0,          test_label.border_radius, lambda v: setattr(test_label, 'border_radius', v))
bw_slider     = TestSlider("bw",     (10, 10 + 40 * 5), 0.0, 10.0,           test_label.border_width,  lambda v: setattr(test_label, 'border_width', int(v)))

# 运行主循环
window.mainloop()

# 调试模式
# fantas.Debug.open_debug_window(window, 0, 0, 2557, (1600 - window.size[1]) // 2 - 50)
# window.mainloop_debug()
