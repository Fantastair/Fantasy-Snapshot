# 设置 Pygame 环境变量以优化性能和兼容性
import os
os.environ['PYGAME_BLEND_ALPHA_SDL2'] = '1'                 # 启用 SDL2 Alpha 混合支持
os.environ['PYGAME_FREETYPE'] = '1'                         # 启用 Pygame FreeType 字体支持
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'              # 隐藏 Pygame 支持提示
os.environ['SDL_VIDEO_ALLOW_SCREENSAVER'] = '1'             # 允许屏幕保护程序
os.environ['SDL_IME_SHOW_UI'] = '1'                         # 显示输入法编辑器 (IME) 界面
os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'    # 启用每个监视器（V2）的 DPI 感知
os.environ['SDL_TIMER_RESOLUTION'] = '1'                    # 提高定时器分辨率
os.environ['SDL_RENDER_VSYNC'] = '0'                        # 禁用渲染垂直同步
os.environ['SDL_KMSDRM_ATOMIC'] = '1'                       # 启用 KMSDRM 原子模式
os.environ['SDL_JOYSTICK_HIDAPI'] = '1'                     # 启用 HIDAPI 支持的操纵杆
os.environ['SDL_JOYSTICK_RAWINPUT'] = '1'                   # 启用 RawInput 支持的操纵杆
os.environ['SDL_WINDOWS_RAW_KEYBOARD'] = '1'                # 启用 Windows 原始键盘输入
os.environ['SDL_AUDIO_ALSA_DEFAULT_DEVICE'] = 'hw:0,0'      # 设置 ALSA 默认音频设备
os.environ['SDL_VIDEO_WAYLAND_SCALE_TO_DISPLAY'] = '0'      # 禁用 Wayland 显示缩放
os.environ['SDL_VIDEO_X11_SCALING_FACTOR'] = '0'            # 禁用 X11 显示缩放
os.environ['SDL_MOUSE_DPI_SCALE_CURSORS'] = '1'             # 启用鼠标 DPI 缩放光标
os.environ['SDL_VIDEO_METAL_AUTO_RESIZE_DRAWABLE'] = '1'    # 启用 Metal 自动调整可绘制区域大小
os.environ['SDL_RENDER_LINE_METHOD'] = '1'                  # 使用更高质量的线条渲染方法
os.environ['SDL_VIDEO_WAYLAND_ALLOW_LIBDECOR'] = '0'        # 禁用 Wayland Libdecor 支持
os.environ['SDL_WINDOWS_ENABLE_MESSAGELOOP'] = '1'          # 启用 Windows 消息循环
os.environ['SDL_QUIT_ON_LAST_WINDOW_CLOSE'] = '1'           # 在最后一个窗口关闭时退出应用程序

# 提供 fantas 包的路径获取函数
from pathlib   import Path
from importlib import resources
def package_path() -> Path:
    """
    获取 fantas 包的目录路径。
    Returns:
        path (Path): 模块所在的文件系统路径。
    """
    return Path(resources.files(__name__))

# 初始化 Pygame
import pygame
import pygame.freetype
pygame.init()
pygame.freetype.init()

# 导入 Pygame 的子模块以简化引用
import pygame.time as time
import pygame.event as event

# 导入 fantas 包的各个子模块
from fantas.constants     import *    # 常量定义
from fantas.nodebase      import *    # 节点基类
from fantas.window        import *    # 窗口管理
from fantas.debug         import *    # 调试功能
from fantas.renderer      import *    # 渲染器和渲染命令
from fantas.event_handler import *    # 事件处理
from fantas.ui            import *    # UI 基类
from fantas.background_ui import *    # 背景 UI
from fantas.label_ui      import *    # 标签 UI
from fantas.text_ui       import *    # 文字 UI

# 类型支持
from typing import TypeAlias, Union

RectLike:  TypeAlias = pygame.typing.RectLike     # 矩形类型
from pygame import FRect as Rect                  # 矩形类

ColorLike: TypeAlias = pygame.typing.ColorLike    # 颜色类型
from pygame import Color                          # 颜色类

Point:     TypeAlias = pygame.typing.Point        # 点类
# IntPoint:  TypeAlias = pygame.typing.IntPoint     # 整数点类
# from pygame.math import Vector2                   # 二维向量类
# from pygame.math import Vector3                   # 三维向量类

from pygame import Surface          # 表面类
from pygame.event import Event      # 事件类
from pygame.freetype import Font    # 字体类

del Union, TypeAlias, pygame, os
