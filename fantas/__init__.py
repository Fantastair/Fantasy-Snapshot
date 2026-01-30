# 设置 Pygame 环境变量以优化性能和兼容性
import os
os.environ.update({
    'PYGAME_BLEND_ALPHA_SDL2'             : '1',               # 启用 SDL2 Alpha 混合支持
    'PYGAME_FREETYPE'                     : '1',               # 启用 Pygame FreeType 字体支持
    'PYGAME_HIDE_SUPPORT_PROMPT'          : '1',               # 隐藏 Pygame 支持提示
    'SDL_VIDEO_ALLOW_SCREENSAVER'         : '1',               # 允许屏幕保护程序
    'SDL_IME_SHOW_UI'                     : '1',               # 显示输入法编辑器 (IME) 界面
    'SDL_WINDOWS_DPI_AWARENESS'           : 'permonitorv2',    # 启用每个监视器（V2）的 DPI 感知
    'SDL_TIMER_RESOLUTION'                : '1',               # 提高定时器分辨率
    'SDL_RENDER_VSYNC'                    : '0',               # 禁用渲染垂直同步
    'SDL_KMSDRM_ATOMIC'                   : '1',               # 启用 KMSDRM 原子模式
    'SDL_JOYSTICK_HIDAPI'                 : '1',               # 启用 HIDAPI 支持的操纵杆
    'SDL_JOYSTICK_RAWINPUT'               : '1',               # 启用 RawInput 支持的操纵杆
    'SDL_WINDOWS_RAW_KEYBOARD'            : '1',               # 启用 Windows 原始键盘输入
    'SDL_AUDIO_ALSA_DEFAULT_DEVICE'       : 'hw:0,0',          # 设置 ALSA 默认音频设备
    'SDL_VIDEO_WAYLAND_SCALE_TO_DISPLAY'  : '0',               # 禁用 Wayland 显示缩放
    'SDL_VIDEO_X11_SCALING_FACTOR'        : '0',               # 禁用 X11 显示缩放
    'SDL_MOUSE_DPI_SCALE_CURSORS'         : '1',               # 启用鼠标 DPI 缩放光标
    'SDL_VIDEO_METAL_AUTO_RESIZE_DRAWABLE': '1',               # 启用 Metal 自动调整可绘制区域大小
    'SDL_RENDER_LINE_METHOD'              : '1',               # 使用更高质量的线条渲染方法
    'SDL_VIDEO_WAYLAND_ALLOW_LIBDECOR'    : '0',               # 禁用 Wayland Libdecor 支持
    'SDL_WINDOWS_ENABLE_MESSAGELOOP'      : '1',               # 启用 Windows 消息循环
    'SDL_QUIT_ON_LAST_WINDOW_CLOSE'       : '1',               # 在最后一个窗口关闭时退出应用程序
})

# 提供 fantas 包的路径获取函数
def package_path():
    """
    获取 fantas 包的目录路径。
    Returns:
        path (Path): 模块所在的文件系统路径。
    """
    from pathlib   import Path
    from importlib import resources
    return Path(resources.files(__name__))

# 全局唯一 ID 生成器
from itertools import count
id_counter = count()
def generate_unique_id() -> int:
    """
    生成一个全局唯一的整数 ID。
    Returns:
        int: 唯一整数 ID。
    """
    return next(id_counter)

# 高精度时间获取函数
from time import perf_counter_ns as get_time_ns

# 类型装饰器以支持类型注解的 lru_cache
from functools import lru_cache, wraps
def lru_cache_typed(maxsize=128, typed=False):
    def decorator(func):
        @wraps(func)  # 用typing.wraps保留类型签名
        @lru_cache(maxsize=maxsize, typed=typed)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 初始化 Pygame
import pygame as pygame
import pygame.freetype
pygame.init()
pygame.freetype.init(cache_size=1024)

# 导入 Pygame 的子模块以简化调用链
import pygame.time      as time
import pygame.draw      as draw
import pygame.event     as event
import pygame.mouse     as mouse
import pygame.image     as image
import pygame.display   as display
import pygame.transform as transform

# 导入 fantas 包的各个子模块
from fantas.constants     import *    # 常量定义
from fantas.window        import *    # 窗口管理
from fantas.font          import *    # 字体支持
from fantas.renderer      import *    # 渲染支持
from fantas.event_handler import *    # 事件处理
from fantas.color         import *    # 颜色支持
from fantas.nodebase      import *    # 节点基类
from fantas.ui            import *    # UI 基类
from fantas.background_ui import *    # 背景 UI
from fantas.label_ui      import *    # 标签 UI
from fantas.text_ui       import *    # 文字 UI
from fantas.fantas_typing import *    # 类型定义
from fantas.resource      import *    # 资源管理

# 如果在调试模式下，导入调试和网络支持模块
if os.environ.get('FANTAS_DEBUG_OFF', '0') != '1':
    from fantas.udp   import *    # 网络支持
    from fantas.debug import *    # 调试功能

# 先禁用所有事件，然后再根据需要启用特定事件
event.set_blocked(None)
# 启用所有已分类事件
event.set_allowed(list(event_category_dict.keys()))

del pygame, count, os
