"""
这个模块不需要导入。
它定义了用于调试的窗口类，在子进程中运行。
"""
import sys
import threading
from queue import Queue

import fantas

class DebugWindow(fantas.Window):
    """
    调试窗口类，用于显示调试信息。
    """
    def __init__(self, window_config):
        super().__init__(window_config)
        self.command_queue = Queue()    # 用于接收调试命令的队列
        # 启动后台线程读取标准输入
        threading.Thread(target=self._read_stdin, daemon=True).start()

        self.top_pos = 0
        self.line_height = 24
        self.total_lines = window_config.window_size[1] // self.line_height
        self.space = 4

        for i in range(self.total_lines):
            c = 255 * (i + 1) / self.total_lines
            text_line = fantas.ColorTextLine(
                text='',
                color=fantas.Color(c, c, c),
                size=self.line_height - self.space,
                rect=fantas.Rect(10, self.space / 2 + i * self.line_height, 0, 0),
            )
            self.root_ui.append(text_line)
        self.text_index = 0
        
        # 进入主循环
        self.mainloop()

    def _read_stdin(self):
        """
        从标准输入读取调试命令并放入队列。
        """
        for line in iter(sys.stdin.readline, ''):
            self.command_queue.put(line.rstrip('\n'))


    def mainloop(self):
        """
        进入窗口的主事件循环，处理事件直到窗口关闭。
        """
        while True:
            self.clock.tick(self.fps)    # 限制帧率
            # 处理事件
            for event in fantas.event.get():
                if event.type == fantas.WINDOWCLOSE:
                    self.destroy()
                    return
            # 处理调试命令
            while not self.command_queue.empty():
                cmd = self.command_queue.get()
                if self.text_index == self.total_lines - 1:
                    # 滚动文本
                    for i in range(self.total_lines - 1):
                        line_ui = self.root_ui.children[i]
                        next_line_ui = self.root_ui.children[i + 1]
                        line_ui.text = next_line_ui.text
                    self.root_ui.children[self.total_lines - 1].text = cmd
                else:
                    self.root_ui.children[self.text_index].text = cmd
                    self.text_index += 1
                    
            # 生成渲染命令
            self.renderer.pre_render(self.root_ui)
            # 渲染窗口
            self.renderer.render(self.screen)
            # 更新窗口显示
            self.flip()


debugwindow_config = fantas.WindowConfig()
debugwindow_config.title = "调试窗口"
debugwindow_config.window_size = (int(sys.argv[3]), int(sys.argv[4]))
debugwindow_config.window_position = (int(sys.argv[1]), int(sys.argv[2]))
debugwindow_config.mouse_focus = False
debug_window = DebugWindow(debugwindow_config)
