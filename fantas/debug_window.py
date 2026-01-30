"""
这个模块不需要导入。
它定义了用于调试的窗口类，在子进程中运行。
"""
from __future__ import annotations
import re
import sys
import select
import threading
from queue import Queue
from base64 import b64decode
from collections import deque

import fantas

debug_flags = fantas.DebugFlag(int(sys.argv[1]))

# 如果没有启用任何调试标志，则退出子进程
if not debug_flags in fantas.DebugFlag.ALL:
    sys.exit(0)

# 预加载资源
fantas.colors.load("white")
fantas.colors.load("#e3e3e3", "debug_fg")
fantas.colors.load("#303030", "debug_bg")

fantas.set_default_text_style(
    font=fantas.fonts.DEFAULTSYSFONT,
    size=20,
    fgcolor=fantas.colors.get("debug_fg")
)

class Lpf:
    """
    滑动平均 + 一阶低通滤波器类。
    """
    _lpf_map: dict[str, callable] = {}

    @staticmethod
    def flit(name: str, x: float, alpha: float = 0.1, ma_win: int = 3) -> float:
        """
        调用滤波器进行滤波。
        Args:
            name (str): 滤波器名称。
            x (float): 新的数据点。
            alpha (float): 一阶低通滤波系数，范围 0.0 - 1.0，默认值为 0.1。
            ma_win (int): 滑动平均窗口大小，默认值为 3。
        Returns:
            float: 滤波后的结果。
        """
        if name not in Lpf._lpf_map:
            flit = Lpf._lpf_map[name] = [deque([0]*ma_win, maxlen=ma_win), 0, alpha, ma_win]
        else:
            flit = Lpf._lpf_map[name]
        flit[0].append(x)
        flit[1] = flit[2]*sum(flit[0])/flit[3] + (1-flit[2])*flit[1]
        return flit[1]

    @staticmethod
    def delete_lpf(name: str):
        """
        删除指定名称的滤波器。
        Args:
            name (str): 滤波器名称。
        """
        if name in Lpf._lpf_map:
            del Lpf._lpf_map[name]

class EventLogWindow(fantas.Window):
    """ 事件日志窗口类。 """

    min_size = (512, 288)

    def __init__(self):
        super().__init__(
            fantas.WindowConfig(
                title=f"{windows_title} | 事件日志",
                window_size=(600, 400),
                window_position=(left_offset, top_offset),
                resizable=True,
                mouse_focus=False,
                input_focus=False,
                allow_high_dpi=True,
            )
        )
        self.background = fantas.ColorBackground(fantas.colors.get("debug_bg"))
        self.root_ui.append(self.background)

        self.text = fantas.Text(style=fantas.DEFAULTTEXTSTYLE, rect=fantas.Rect(10, 0, self.size[0] - 20, self.size[1]), reverse=True)
        self.background.append(self.text)

        self.lines: deque[str] = deque(maxlen=10)
        self.add_event_listener(fantas.WINDOWRESIZED, self.root_ui, True, self.handle_WINDOWRESIZED_event)

    def log_event(self, event_str: str):
        """
        记录事件日志。
        Args:
            event_str (str): 事件信息字符串。
        """
        self.lines.append(event_str)
        self.text.text = '\n---\n'.join(self.lines)

    def handle_WINDOWRESIZED_event(self, event: fantas.Event):
        """
        处理窗口大小改变事件。
        Args:
            event (fantas.Event): 窗口大小改变事件对象。
        """
        if event.x < EventLogWindow.min_size[0]:
            event.x = EventLogWindow.min_size[0]
        if event.y < EventLogWindow.min_size[1]:
            event.y = EventLogWindow.min_size[1]
        if self.size != (event.x, event.y):
            self.size = (event.x, event.y)
        self.text.rect.width = event.x - 20
        self.text.rect.height = event.y

class TimeRecordWindow(fantas.Window):
    """ 时间记录窗口类。 """

    time_category = {
        "Event": "事件处理",
        "PreRender": "预渲染",
        "Render": "渲染",
        "Debug": "调试",
        "Idle": "空闲",
    }
    for key in time_category.keys():
        Lpf.flit(f"{key}Time", 0, 0.05, 5)
        Lpf.flit(f"{key}Ratio", 0, 0.05, 5)
    Lpf.flit("FPS", 0, 0.05, 5)
    fantas.colors.load("#e74c3c", "Event_legend_color")
    fantas.colors.load("#9b59b6", "PreRender_legend_color")
    fantas.colors.load("#f1c40f", "Render_legend_color")
    fantas.colors.load("#7d7d7d", "Debug_legend_color")
    fantas.colors.load("#2ecc71", "Idle_legend_color")

    min_width  = 400
    fix_height = 200

    def __init__(self):
        super().__init__(
            fantas.WindowConfig(
                title=f"{windows_title} | 时间记录",
                window_size=(TimeRecordWindow.min_width, TimeRecordWindow.fix_height),
                window_position=(left_offset, top_offset),
                resizable=True,
                mouse_focus=False,
                input_focus=False,
                allow_high_dpi=True
            )
        )

        self.background = fantas.ColorBackground(fantas.colors.get("debug_bg"))
        self.root_ui.append(self.background)

        self.fps_text = fantas.TextLine(
            text="FPS: 0.0",
            style=fantas.DEFAULTTEXTSTYLE,
            origin=(8, 29),
        )
        self.background.append(self.fps_text)

        self.legend_text = fantas.Text(
            style=fantas.DEFAULTTEXTSTYLE,
            line_spacing=1,
            rect=fantas.Rect(50, 44, 100, 150),
            align_mode=fantas.AlignMode.LEFTRIGHT
        )
        text = ""
        for i, (key, desc) in enumerate(TimeRecordWindow.time_category.items()):
            legend_color = fantas.colors.get(f"{key}_legend_color")
            legend = fantas.Label(
                bgcolor=legend_color,
                fgcolor=fantas.colors.get("debug_fg"),
                rect=fantas.Rect(10, 50 + i*30, 20, 20),
                border_width=2,
            )
            self.background.append(legend)
            text += f"{desc}\n"
        self.legend_text.text = text.strip()
        self.background.append(self.legend_text)
        self.times = {key: 0.0 for key in TimeRecordWindow.time_category.keys()}
        self.time_text = fantas.Text(
            text='',
            style=fantas.DEFAULTTEXTSTYLE,
            line_spacing=1,
            rect=fantas.Rect(170, 44, 100, 150),
        )
        self.background.append(self.time_text)
        self.ratios = {key: 0.0 for key in TimeRecordWindow.time_category.keys()}
        self.time_ratio_bars = {}
        for i, key in enumerate(TimeRecordWindow.time_category.keys()):
            bar1 = fantas.Label(
                bgcolor=fantas.colors.get(f"{key}_legend_color"),
                rect=fantas.Rect(100, 10, 100, 20),
            )
            self.background.append(bar1)
            bar2 = fantas.Label(
                bgcolor=fantas.colors.get(f"{key}_legend_color"),
                rect=fantas.Rect(260, 50 + i*30,  self.size[0] - 270, 20),
            )
            self.background.append(bar2)
            self.time_ratio_bars[key] = (bar1, bar2)
        self.add_event_listener(fantas.WINDOWRESIZED, self.root_ui, True, self.handle_WINDOWRESIZED_event)
    
    def update_fps(self, fps: float):
        """
        更新帧率显示。
        Args:
            fps (float): 当前帧率值。
        """
        self.fps_text.text = f"FPS: {Lpf.flit("FPS", fps):.2f}"
    
    def update_time_records(self, time_dict: dict[str, int]):
        """
        更新时间记录显示。
        Args:
            time_dict (dict[str, int]): 包含时间记录的字典，单位ns。
        """
        total_time = sum(time_dict.values())
        self.update_fps(1e9 / total_time if total_time > 0 else 0.0)
        for key, time in time_dict.items():
            self.times[key] = Lpf.flit(f"{key}Time", time / 1e6)    # 转换为毫秒
            self.ratios[key] = Lpf.flit(f"{key}Ratio", time / total_time if total_time > 0 else 0.0)
        self.time_text.text = '\n'.join([f"{time:.2f} ms" for time in self.times.values()])
        x = 120
        width = self.size[0] - x - 10
        for key, bars in self.time_ratio_bars.items():
            bars[0].rect.left = x
            bars[0].rect.width = round(width * self.ratios[key])
            bars[1].rect.width = self.ratios[key] * (self.size[0] - 270)
            x += bars[0].rect.width
        self.time_ratio_bars["Idle"][0].rect.width += self.size[0] - 10 - x    # 修正舍入误差

    def handle_WINDOWRESIZED_event(self, event: fantas.Event):
        """
        处理窗口大小改变事件。
        Args:
            event (fantas.Event): 窗口大小改变事件对象。
        """
        if event.x < TimeRecordWindow.min_width:
            event.x = TimeRecordWindow.min_width
        if self.size != (event.x, TimeRecordWindow.fix_height):
            self.size = (event.x, TimeRecordWindow.fix_height)

class MouseMagnifyWindow(fantas.Window):
    """ 鼠标放大镜窗口类。 """
    def __init__(self):
        super().__init__(
            fantas.WindowConfig(
                title=f"{windows_title} | 鼠标放大镜",
                window_size=(256, 320),
                window_position=(left_offset, top_offset),
                mouse_focus=False,
                input_focus=False,
                allow_high_dpi=True
            )
        )

        self.background = fantas.ColorBackground(fantas.colors.get("debug_bg"))
        self.root_ui.append(self.background)

        self.ratio = 8
        self.ratio_text = fantas.TextLine(
            text=f"放大倍数: {self.ratio}x",
            style=fantas.DEFAULTTEXTSTYLE,
            origin=(40, 40),
        )
        self.background.append(self.ratio_text)

        self.mouse_shot_label = fantas.SurfaceLabel(
            surface=fantas.Surface((32, 32)),
            rect=fantas.Rect(0, 0, 256, 256),
            fill_mode=fantas.FillMode.SCALE,
        )
        self.mouse_shot_label.rect.bottom = self.size[1]
        self.background.append(self.mouse_shot_label)

        self.cursor = fantas.Label(
            bgcolor=None,
            rect=fantas.Rect(0, 0, self.ratio, self.ratio),
            border_width=1
        )
        self.mouse_shot_label.append(self.cursor)
        self.cursor.rect.center = self.mouse_shot_label.rect.width / 2, self.mouse_shot_label.rect.height / 2
        self.cursor_color_label = fantas.Label(
            fgcolor=fantas.colors.get("debug_fg"),
            rect=fantas.Rect(0, 0, 48, 48),
            border_width=2,
        )
        self.cursor_color_label.rect.midright = (self.size[0] - 10, 32)
        self.background.append(self.cursor_color_label)

    def update_ratio(self, ratio: int):
        """
        更新放大倍数显示。
        Args:
            ratio (int): 当前放大倍数值。
        """
        self.ratio = ratio
        self.ratio_text.text = f"放大倍数: {self.ratio}x"
    
    def update_mouse_shot(self, surface_bytes: str):
        """
        更新鼠标截图 Surface。
        Args:
            surface_bytes (str): 编码后的 Surface 字节数据字符串。
        """
        self.mouse_shot_label.surface.get_buffer().write(b64decode(surface_bytes[4:]))
        x = int(surface_bytes[0:2])
        y = int(surface_bytes[2:4])
        self.cursor.rect.left = x * self.ratio
        self.cursor.rect.top  = y * self.ratio
        cursor_color = self.mouse_shot_label.surface.get_at((x, y))
        self.cursor.fgcolor = fantas.get_distinct_blackorwhite(cursor_color)
        self.cursor_color_label.bgcolor = cursor_color

def read_debug_command():
    """
    从标准输入读取调试命令并放入队列。
    """
    fantas.time.delay(100)
    stdin_fd = sys.stdin.fileno()

    while debug_windows.running:
        try:
            readable, _, _ = select.select([stdin_fd], [], [], 0.1)

            if stdin_fd in readable:
                # 有输入数据时，才执行 readline 读取（不会阻塞）
                line = sys.stdin.readline()
                if not line:    # 检测到 stdin 关闭（主程序退出时）
                    break
                # 放入命令队列
                if command_queue.empty():
                    command_queue.put(line.rstrip('\n'))
                    fantas.event.post(fantas.Event(fantas.DEBUGRECEIVED))
                else:
                    command_queue.put(line.rstrip('\n'))
        except Exception as e:
            if debug_windows.running:
                print(f"读取调试命令异常: {e}", flush=True)
            break

# 时间记录拆分正则表达式
split_time_records = re.compile(rf'([^:{re.escape("\x1f")}]+):(-?\d+)')

def handle_debug_command(prompt: str, command: str):
    """
    处理调试命令。
    Args:
        prompt (str): 命令提示符。
        command (str): 调试命令字符串。
    """
    if fantas.DebugFlag.EVENTLOG in debug_flags and prompt == "EventLog":
        event_log_window.log_event(command)
    elif fantas.DebugFlag.TIMERECORD in debug_flags and prompt == "TimeRecord":
        time_record_window.update_time_records({key.strip(): int(value) for key, value in re.findall(split_time_records, command)})
    elif fantas.DebugFlag.MOUSEMAGNIFY in debug_flags and prompt == "MouseMagnify":
        mouse_magnify_window.update_mouse_shot(command)

# 调试命令拆分正则表达式
split_prompt_command_re = re.compile(r"^\[(.*?)\]\s+(.*)$")

def handle_received_debug_command_event(event: fantas.Event):
    """
    处理接收到的调试命令事件。
    Args:
        event (fantas.Event): 接收到的调试命令事件对象。
    """
    while not command_queue.empty():
        cmd = command_queue.get()
        match = split_prompt_command_re.match(cmd)
        if match:
            prompt = match.group(1)
            command = match.group(2)
            handle_debug_command(prompt, command)
    return True

# 创建调试命令队列
command_queue = Queue(maxsize=1024)

# 存储所有调试窗口的列表
windows = []

windows_title = sys.argv[2]    # 调试窗口标题
left_offset = 0    # 窗口左侧偏移位置
top_offset  = 0    # 窗口顶部偏移位置
max_bottom = 0     # 窗口最大底部位置
screen_size = fantas.display.get_desktop_sizes()[0]

# 如果启用了事件日志调试标志，则创建事件日志窗口
if fantas.DebugFlag.EVENTLOG in debug_flags:
    event_log_window = EventLogWindow()
    windows.append(event_log_window)
    if screen_size[0] - left_offset < event_log_window.size[0]:
        left_offset = 0
        top_offset = max_bottom
    left_offset += event_log_window.size[0]
    max_bottom = max(max_bottom, top_offset + event_log_window.size[1])

# 如果启用了时间记录调试标志，则创建时间记录窗口
if fantas.DebugFlag.TIMERECORD in debug_flags:
    time_record_window = TimeRecordWindow()
    windows.append(time_record_window)
    if screen_size[0] - left_offset < time_record_window.size[0]:
        left_offset = 0
        top_offset = max_bottom
    left_offset += time_record_window.size[0]
    max_bottom = max(max_bottom, top_offset + time_record_window.size[1])

# 如果启用了鼠标放大调试标志，则创建鼠标放大窗口
if fantas.DebugFlag.MOUSEMAGNIFY in debug_flags:
    mouse_magnify_window = MouseMagnifyWindow()
    windows.append(mouse_magnify_window)
    if screen_size[0] - left_offset < mouse_magnify_window.size[0]:
        left_offset = 0
        top_offset = max_bottom
    left_offset += mouse_magnify_window.size[0]
    max_bottom = max(max_bottom, top_offset + mouse_magnify_window.size[1])

# 注册接收调试命令事件的处理器
for window in windows:
    window.add_event_listener(fantas.DEBUGRECEIVED, window.root_ui, True, handle_received_debug_command_event)

# 创建调试窗口
debug_windows = fantas.MultiWindow(*windows)

# 启动后台线程读取标准输入
debug_thread = threading.Thread(target=read_debug_command)
debug_thread.start()

# 运行调试窗口主循环
debug_windows.mainloops()

# 等待调试线程结束
debug_thread.join()
