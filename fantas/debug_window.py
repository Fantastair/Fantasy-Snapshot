"""
这个模块不需要导入。
它定义了用于调试的窗口类，在子进程中运行。
"""
from __future__ import annotations
import re
import sys
import threading
from queue import Queue
from collections import deque

import fantas

def make_lpf(alpha, ma_win=3):
    """
    滑动平均 + 一阶低通滤波器生成函数。
    Args:
        alpha (float): 一阶低通滤波器的平滑系数，取值范围为0到1。
        ma_win (int): 滑动平均窗口大小，默认值为3。
    Returns:
        function: 返回一个滤波函数，调用该函数并传入新的数据点即可获得滤波后的结果。
    """
    buf = deque([0]*ma_win, maxlen=ma_win)
    y = 0
    def filt(x):
        nonlocal y
        buf.append(x)
        z = sum(buf)/ma_win          # 滑动平均
        y = alpha*z + (1-alpha)*y    # 一阶低通
        return y
    return filt

RECEIVEDDEBUGCOMMAND = fantas.custom_event()    # 用于接收调试命令的自定义事件类型
fantas.event.set_allowed(RECEIVEDDEBUGCOMMAND)

# 调试命令拆分正则表达式
split_prompt_command_re = re.compile(r"^\[(.*?)\]\s+(.*)$")

lpf_map = {
    "Event":         make_lpf(0.05, 5),
    "PreRender":     make_lpf(0.05, 5),
    "Render":        make_lpf(0.05, 5),
    "Idle":          make_lpf(0.05, 5),
    "EventTime":     make_lpf(0.05, 5),
    "PreRenderTime": make_lpf(0.05, 5),
    "RenderTime":    make_lpf(0.05, 5),
    "IdleTime":      make_lpf(0.05, 5),
}

# 中文字体支持
chinese_font = fantas.freetype.SysFont(("SimHei", "Microsoft YaHei", "notoserifcjksc"), 16)

class RatioBar:
    """
    比例条类，用于显示时间占比。
    """
    def __init__(self, width: int, height: int, parent_ui: fantas.UI, legend_box: LegendBox):
        self.legend_box = legend_box
        self.box = fantas.ColorLabel(
            bgcolor=None,
            rect=fantas.Rect(0, 0, width, height),
        )
        parent_ui.append(self.box)
        self.sub_bar = {
            "Event": fantas.ColorLabel(
                bgcolor=fantas.Color("#e74c3c"),
                rect=fantas.Rect(0, 0, 0, height),
                border_radius=6,
                quadrant=fantas.Quadrant.TOPLEFT | fantas.Quadrant.BOTTOMLEFT,
            ),
            "PreRender": fantas.ColorLabel(
                bgcolor=fantas.Color("#9b59b6"),
                rect=fantas.Rect(0, 0, 0, height),
            ),
            "Render": fantas.ColorLabel(
                bgcolor=fantas.Color("#f1c40f"),
                rect=fantas.Rect(0, 0, 0, height),
            ),
            "Idle": fantas.ColorLabel(
                bgcolor=fantas.Color("#2ecc71"),
                rect=fantas.Rect(0, 0, 0, height),
                border_radius=6,
                quadrant=fantas.Quadrant.TOPRIGHT | fantas.Quadrant.BOTTOMRIGHT,
            ),
        }
        for bar in self.sub_bar.values():
            self.box.append(bar)
    
    def set_time(self, time_list: list[int]):
        """
        设置各阶段时间并更新比例条显示。
        Args:
            time_list (list[int]): 包含各阶段时间的列表，单位ns。
        """
        total_time = time_list[-1] - time_list[0]
        idle_time = time_list[1] - time_list[0]
        event_time = time_list[2] - time_list[1]
        prerender_time = time_list[3] - time_list[2]
        render_time = time_list[4] - time_list[3]
        times = {
            "Idle": idle_time,
            "Event": event_time,
            "PreRender": prerender_time,
            "Render": render_time,
        }
        x = 0
        for key, bar in self.sub_bar.items():
            width = round(lpf_map[key](self.box.rect.width * times[key] / total_time))
            bar.rect.left = x
            bar.rect.width = width
            x += width
            time = lpf_map[f"{key}Time"](times[key] / 1e6)
            self.legend_box.time_texts[key].text = f"{time:.2f} ms"
        if x < self.box.rect.width:
            self.sub_bar["Idle"].rect.width += self.box.rect.width - x

class LegendBox:
    """
    图例框类，用于显示时间占比图例。
    """
    def __init__(self, parent_ui: fantas.UI):
        self.legend_box = fantas.ColorLabel(
            bgcolor=fantas.Color("#303030"),
            fgcolor=fantas.Color("#e3e3e3"),
            rect=fantas.Rect(0, 0, 260, 136),
            border_radius=12,
            border_width=3,
            box_mode=fantas.BoxMode.OUTSIDE,
        )
        parent_ui.append(self.legend_box)
        legend_items = (
            ("Event",     "#e74c3c", "事件处理"),
            ("PreRender", "#9b59b6", "预渲染"),
            ("Render",    "#f1c40f", "渲染"),
            ("Idle",      "#2ecc71", "空闲"),
        )
        self.time_texts = {}
        for i, (name, color, desc) in enumerate(legend_items):
            color_box = fantas.ColorLabel(
                bgcolor=fantas.Color(color),
                fgcolor=fantas.Color("#e3e3e3"),
                rect=fantas.Rect(10, 10 + i*32, 24, 24),
                border_width=3,
                box_mode=fantas.BoxMode.INSIDE,
            )
            self.legend_box.append(color_box)
            desc_text = fantas.ColorTextLine(
                text=desc,
                size=24.0,
                fgcolor=fantas.Color("#e3e3e3"),
                rect=fantas.Rect(42, 13 + (i-1)*32, 0, 0),
                font=chinese_font,
            )
            self.legend_box.append(desc_text)
            time_text = fantas.ColorTextLine(
                text="0 ms",
                size=24.0,
                fgcolor=fantas.Color("#e3e3e3"),
                rect=fantas.Rect(150, 16 + (i-1)*32, 0, 0),
                font=chinese_font,
            )
            self.legend_box.append(time_text)
            self.time_texts[name] = time_text

class FrameTimer:
    """
    帧计时器类，用于显示帧率及时间占比。
    """
    def __init__(self, width: int, height: int, parent_ui: fantas.UI):
        # 显示框
        self.box = fantas.ColorLabel(
            bgcolor=fantas.Color("#303030"),
            fgcolor=fantas.Color("#e3e3e3"),
            rect=fantas.Rect(0, 0, width, height),
            border_radius=12,
            border_width=3,
            box_mode=fantas.BoxMode.OUTSIDE,
        )
        parent_ui.append(self.box)
        # 帧率文本
        self.fps_text = fantas.ColorTextLine(
            text="FPS: 0.0",
            size=24.0,
            fgcolor=fantas.Color("#e3e3e3"),
            rect=fantas.Rect(8, 8, 0, 0),
        )
        self.box.append(self.fps_text)
        self.fps_lpf = make_lpf(0.05, 5)
        # 比例条宽度
        self.fps_text_width = 160
        self.bar_width = width - self.fps_text_width - 30
        # 图例
        self.legend_box = LegendBox(parent_ui)
        # 比例条
        self.ratio_bar = RatioBar(self.bar_width, 24, self.box, self.legend_box)
        self.ratio_bar.box.rect.topleft = (self.fps_text_width + 20, 8)
        
    def show_frame_time(self, time_list: list[int]):
        """
        显示帧时间信息。
        Args:
            time_list (list[int]): 包含各阶段时间的列表，单位ns。
        """
        fps = self.fps_lpf(1e9 / (time_list[-1] - time_list[0]))
        self.fps_text.text = f"FPS: {fps:.2f}"
        # 设置比例条时间
        self.ratio_bar.set_time(time_list)

class EventLogBox:
    """
    事件日志框类，用于显示事件日志信息。
    """
    def __init__(self, width: int, height: int, parent_ui: fantas.UI):
        self.box = fantas.ColorLabel(
            bgcolor=fantas.Color("#303030"),
            fgcolor=fantas.Color("#e3e3e3"),
            rect=fantas.Rect(0, 0, width, height),
            border_radius=12,
            border_width=3,
            box_mode=fantas.BoxMode.OUTSIDE,
        )
        parent_ui.append(self.box)
        self.line_height = 24
        self.max_lines = round(height / self.line_height - 1)
        self.lines: deque[str] = deque(['']*self.max_lines, maxlen=self.max_lines)
        self.text_lines: list[fantas.ColorTextLine] = []
        for i in range(self.max_lines):
            text_line = fantas.ColorTextLine(
                text="",
                size=self.line_height - 4,
                fgcolor=fantas.Color("#e3e3e3"),
                rect=fantas.Rect(8, (i-0.5)*self.line_height, 0, 0),
                font=chinese_font,
            )
            self.box.append(text_line)
            self.text_lines.append(text_line)
        text_line.fgcolor = fantas.Color("#c5e73c")
        self.log_event("事件日志：")

    def log_event(self, event_str: str):
        """
        记录事件日志。
        Args:
            event_str (str): 事件信息字符串。
        """
        self.lines.append(event_str)
        for i, line in enumerate(self.lines):
            self.text_lines[i].text = line

class DebugWindow(fantas.Window):
    """
    调试窗口类，用于显示调试信息。
    """
    def __init__(self, window_config):
        super().__init__(window_config)
        self.command_queue = Queue()    # 用于接收调试命令的队列
        # 启动后台线程读取标准输入
        threading.Thread(target=self.read_debug_command, daemon=True).start()
        # 注册接收调试命令事件的处理器
        self.add_event_listener(RECEIVEDDEBUGCOMMAND, self.root_ui, True, self.handle_received_debug_command_event)
        # 背景颜色
        self.background = fantas.ColorBackground(fantas.Color("#000000"))
        self.append(self.background)
        # 帧计时器
        self.frame_timer = FrameTimer(window_config.window_size[0] - 20, 40, self.background)
        self.frame_timer.box.rect.topleft = (10, 10)
        self.frame_timer.legend_box.legend_box.rect.topleft = (10, self.frame_timer.box.rect.bottom + 13)
        # 事件日志框
        self.event_log_box = EventLogBox(window_config.window_size[0] - self.frame_timer.legend_box.legend_box.rect.right - 23, self.frame_timer.legend_box.legend_box.rect.height, self.background)
        self.event_log_box.box.rect.topleft = (self.frame_timer.legend_box.legend_box.rect.right + 13, self.frame_timer.box.rect.bottom + 13)

    def read_debug_command(self):
        """
        从标准输入读取调试命令并放入队列。
        """
        for line in iter(sys.stdin.readline, ''):
            self.command_queue.put(line.rstrip('\n'))
            fantas.event.post(fantas.Event(RECEIVEDDEBUGCOMMAND))

    def write_debug_output(self, msg: str):
        """
        写入调试输出信息到标准输出。
        Args:
            msg (str): 要写入的调试信息字符串。
        """
        print(msg, flush=True)

    def handle_received_debug_command_event(self, event: fantas.Event):
        """
        处理接收到的调试命令事件。
        Args:
            event (fantas.Event): 接收到的调试命令事件对象。
        """
        cmd = self.command_queue.get()
        match = split_prompt_command_re.match(cmd)
        if match:
            prompt = match.group(1)
            command = match.group(2)
            self.handle_debug_command(prompt, command)
    
    def handle_debug_command(self, prompt: str, command: str):
        """
        处理调试命令。
        Args:
            prompt (str): 命令提示符。
            command (str): 调试命令字符串。
        """
        if prompt == "Debug":
            pass
        elif prompt == "EventLog":
            self.event_log_box.log_event(command)
        elif prompt == "FrameTime":
            self.frame_timer.show_frame_time(list(map(float, command[1:-1].split(', '))))

debugwindow_config = fantas.WindowConfig(
    title=f"{sys.argv[1]} | 调试窗口",
    window_size=(int(sys.argv[4]), int(sys.argv[5])),
    window_position=(int(sys.argv[2]), int(sys.argv[3])),
    mouse_focus=False,
    input_focus=False,
)
debug_window = DebugWindow(debugwindow_config)

debug_window.mainloop()
