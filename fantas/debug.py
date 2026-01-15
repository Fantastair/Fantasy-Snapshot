"""
此模块不会被自动导入。
"""
import atexit
import subprocess
from pathlib import Path
from importlib import resources

import fantas

__all__ = (
    "package_path",
    "Debug",
)

def package_path() -> Path:
    """
    获取 fantas 包的目录路径。
    Returns:
        path (Path): 模块所在的文件系统路径。
    """
    return Path(resources.files(__name__))

class Debug:
    process: subprocess.Popen | None = None

    @staticmethod
    def open_debug_window():
        """
        启动调试窗口子进程。
        """
        # 设置子进程的环境变量，确保可以找到 fantas 包
        import os
        env = os.environ.copy()
        env['PYTHONPATH'] = os.pathsep.join([
            str(fantas.package_path().parent),
            *env.get('PYTHONPATH', '').split(os.pathsep)
        ])
        # 使用同一个 Python 解释器，构建命令行参数
        import sys
        cmd = [sys.executable, str(fantas.package_path() / "debug_window.py")]

        try:
            Debug.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,    # 通信管道
                text=True,                # 文本模式，自动编码/解码
                bufsize=1,                # 行缓冲
                env=env,                  # 子进程环境变量
            )
        except FileNotFoundError as e:
            raise RuntimeError(f"命令{cmd}出错，无法启动调试窗口:") from e

    @staticmethod
    def close_debug_window():
        """
        关闭调试窗口子进程。
        """
        if Debug.process is not None and Debug.process.stdin is not None:
            Debug.process.stdin.close()
        if Debug.process is not None and Debug.process.poll() is None:
            Debug.process.kill()
            Debug.process.wait()

    @staticmethod
    def send_debug_command(msg: str):
        """
        发送调试命令到调试窗口子进程。
        """
        if Debug.process is None or Debug.process.stdin is None:
            raise RuntimeError("调试窗口未启动，无法发送调试命令。")
        Debug.process.stdin.write(msg + "\n")
        Debug.process.stdin.flush()

atexit.register(Debug.close_debug_window)
