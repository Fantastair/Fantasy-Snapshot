import atexit
import threading
import subprocess
from queue import Queue
from enum import Flag

import fantas

__all__ = (
    "Debug",
    "DebugFlag",
)

class DebugFlag(Flag):
    """ 调试选项标志枚举。 """
    EVENTLOG     = 1    # 事件日志
    TIMERECORD   = 2    # 时间记录
    MOUSEMAGNIFY = 4    # 鼠标放大镜

    ALL  = EVENTLOG | TIMERECORD | MOUSEMAGNIFY
    NONE = 0

class Debug:
    process: subprocess.Popen | None = None    # 调试窗口子进程对象
    queue: Queue = Queue()                     # 调试子进程返回队列
    debug_flag: DebugFlag = DebugFlag.NONE     # 当前调试选项标志

    @staticmethod
    def start_debug(flag: DebugFlag = DebugFlag.ALL, windows_title: str = "fantas 调试窗口"):
        """
        启动调试窗口子进程。
        Args:
            flag   (DebugFlag)    : 调试选项标志。
            windows_title (str)   : 调试窗口标题。
        """
        # 先关闭已有的调试窗口
        Debug.close_debug()
        # 设置子进程的环境变量，确保可以找到 fantas 包
        import os
        env = os.environ.copy()
        env['PYTHONPATH'] = os.pathsep.join([
            str(fantas.package_path().parent),
            *env.get('PYTHONPATH', '').split(os.pathsep)
        ])
        # 使用同一个 Python 解释器，构建命令行参数
        import sys
        cmd = [sys.executable, str(fantas.package_path() / "debug_window.py"), str(flag.value), windows_title]

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
            # 记录当前调试选项标志
            Debug.debug_flag = flag
        except FileNotFoundError as e:
            raise RuntimeError(f"命令{cmd}出错，无法启动调试窗口:") from e

    @staticmethod
    def close_debug():
        """ 关闭调试窗口子进程。 """
        if Debug.is_debuging():
            if Debug.process.stdin is not None:
                Debug.process.stdin.close()
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
        if not Debug.is_debuging() or Debug.process.stdin is None:
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
    def is_debuging() -> bool:
        """
        检查调试窗口子进程是否正在运行。
        Returns:
            is_open (bool): 如果调试窗口正在运行则返回 True，否则返回 False。
        """
        return Debug.process is not None and Debug.process.poll() is None
atexit.register(Debug.close_debug)
