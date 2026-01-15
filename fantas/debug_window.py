"""
这个模块不需要导入。
它定义了用于调试的窗口类，在子进程中运行。
"""
import sys
import threading
from queue import Queue

from fantas import Window, WindowConfig

class DebugWindow(Window):
    """
    调试窗口类，用于显示调试信息。
    """
    def __init__(self, window_config):
        super().__init__(window_config)
        self.command_queue = Queue()    # 用于接收调试命令的队列
        # 启动后台线程读取标准输入
        threading.Thread(target=self._read_stdin, daemon=True).start()
        # 进入主循环
        self.mainloop()

    def _read_stdin(self):
        """
        从标准输入读取调试命令并放入队列。
        """
        for line in iter(sys.stdin.readline, ''):
            self.command_queue.put(line.rstrip('\n'))

debugwindow_config = WindowConfig()
debugwindow_config.title = "调试窗口"
debugwindow_config.window_size = (800, 600)
debug_window = DebugWindow(debugwindow_config)
