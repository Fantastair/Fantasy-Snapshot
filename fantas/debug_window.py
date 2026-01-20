"""
这个模块不需要导入。
它定义了用于调试的窗口类，在子进程中运行。
"""
import sys
import threading
from queue import Queue

import fantas

RECEIVEDDEBUGCOMMAND = fantas.custom_event()    # 用于接收调试命令的自定义事件类型

class DebugWindow(fantas.Window):
    """
    调试窗口类，用于显示调试信息。
    """
    def __init__(self, window_config):
        super().__init__(window_config)
        self.command_queue = Queue()    # 用于接收调试命令的队列
        # 启动后台线程读取标准输入
        threading.Thread(target=self.read_debug_command, daemon=True).start()

        # 初始化事件显示
        self.top_pos = 0
        self.line_height = 24
        self.total_lines = window_config.window_size[1] // self.line_height
        self.space = 4
        self.background = fantas.ColorBackground(bgcolor=fantas.Color(30, 30, 30))
        self.append(self.background)
        for i in range(self.total_lines):
            c = 255 * (i + 1) / self.total_lines
            text_line = fantas.ColorTextLine(
                text='',
                fgcolor=fantas.Color(c, c, c),
                size=self.line_height - self.space,
                rect=fantas.Rect(10, self.space / 2 + i * self.line_height, 0, 0),
            )
            self.background.append(text_line)
        self.text_index = 0

        # 注册接收调试命令事件的处理器
        self.add_event_listener(RECEIVEDDEBUGCOMMAND, self.root_ui, True, self.handle_received_debug_command_event)

        # 进入主循环
        self.mainloop()

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
        if self.text_index == self.total_lines - 1:
            # 滚动文本
            for i in range(self.total_lines - 1):
                line_ui: fantas.ColorTextLine = self.background.children[i]
                next_line_ui: fantas.ColorTextLine = self.background.children[i + 1]
                line_ui.text = next_line_ui.text
            self.background.children[self.total_lines - 1].text = cmd
        else:
            self.background.children[self.text_index].text = cmd
            self.text_index += 1

debugwindow_config = fantas.WindowConfig()
debugwindow_config.title = "调试窗口"
debugwindow_config.window_size = (int(sys.argv[3]), int(sys.argv[4]))
debugwindow_config.window_position = (int(sys.argv[1]), int(sys.argv[2]))
debugwindow_config.mouse_focus = False
debugwindow_config.input_focus = False
debug_window = DebugWindow(debugwindow_config)
