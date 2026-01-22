import atexit
import threading
import subprocess
from queue import Queue

import fantas

__all__ = (
    "Debug",
)

class Debug:
    process: subprocess.Popen | None = None    # 调试窗口子进程对象
    queue: Queue = Queue()                     # 调试子进程返回队列

    @staticmethod
    def open_debug_window(window: fantas.Window, left: int = 0, top: int = 0, width: int = 1280, height: int = 720, close_with_main: bool = True):
        """
        启动调试窗口子进程。
        Args:
            window (fantas.Window): 主窗口对象。
            left            (int) : 窗口左上角的 X 坐标位置。
            top             (int) : 窗口左上角的 Y 坐标位置。
            width           (int) : 窗口宽度（像素）。
            height          (int) : 窗口高度（像素）。
            close_with_main (bool): 主进程关闭时是否关闭调试窗口子进程。
        """
        # 先关闭已有的调试窗口
        Debug.close_debug_window()
        if close_with_main:
            atexit.register(Debug.close_debug_window)
        else:
            atexit.unregister(Debug.close_debug_window)
        # 设置子进程的环境变量，确保可以找到 fantas 包
        import os
        env = os.environ.copy()
        env['PYTHONPATH'] = os.pathsep.join([
            str(fantas.package_path().parent),
            *env.get('PYTHONPATH', '').split(os.pathsep)
        ])
        # 使用同一个 Python 解释器，构建命令行参数
        import sys
        cmd = [sys.executable, str(fantas.package_path() / "debug_window.py"), window.title, str(left), str(top), str(width), str(height)]

        try:
            Debug.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,     # 发送信息通信管道
                stdout=subprocess.PIPE,    # 接收信息通信管道
                text=True,                 # 文本模式，自动编码/解码
                bufsize=1,                 # 行缓冲
                env=env,                   # 子进程环境变量
            )
            # 启动后台线程读取子进程输出
            threading.Thread(target=Debug.read_debug_output, daemon=True).start()
        except FileNotFoundError as e:
            raise RuntimeError(f"命令{cmd}出错，无法启动调试窗口:") from e

    @staticmethod
    def close_debug_window():
        """ 关闭调试窗口子进程。 """
        if Debug.is_debug_window_open() and Debug.process.stdin is not None:
            Debug.process.stdin.close()
        if Debug.is_debug_window_open():
            Debug.process.kill()
            Debug.process.wait()

    @staticmethod
    def send_debug_command(msg: str, prompt: str = "Debug"):
        """
        发送调试命令到调试窗口子进程。
        Args:
            msg (str): 要发送的调试命令字符串。
            prompt (str): 调试命令的提示符。
        Raises:
            RuntimeError: 如果调试窗口未启动则抛出此异常。
        """
        if not Debug.is_debug_window_open() or Debug.process.stdin is None:
            # raise RuntimeError("调试窗口未启动，无法发送调试命令。")
            return
        Debug.process.stdin.write(f"[{prompt}] {msg}\n")
        Debug.process.stdin.flush()
    
    @staticmethod
    def read_debug_output():
        """
        从调试窗口子进程读取输出信息并放入队列。
        """
        for line in iter(Debug.process.stdout.readline, ''):
            Debug.queue.put(line.rstrip('\n'))
    
    @staticmethod
    def is_debug_window_open() -> bool:
        """
        检查调试窗口子进程是否正在运行。
        Returns:
            is_open (bool): 如果调试窗口正在运行则返回 True，否则返回 False。
        """
        return Debug.process is not None and Debug.process.poll() is None
