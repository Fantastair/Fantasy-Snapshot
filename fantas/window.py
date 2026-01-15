from dataclasses import dataclass

import fantas
import pygame

__all__ = (
    "WindowConfig",
    "Window",
)

@dataclass(slots=True)
class WindowConfig:
    """
    窗口配置数据类，包含创建窗口所需的各种参数。
    """
    # 窗口标题
    title: str = "Fantas Window"
    # 窗口尺寸（宽, 高）（像素）
    window_size: tuple[int, int] = (1280, 720)
    # 窗口位置（x, y）或预设常量 fantas.WINDOWPOS_CENTERED / fantas.WINDOWPOS_UNDEFINED
    window_position: tuple[int, int] | int = fantas.WINDOWPOS_UNDEFINED
    # 窗口是否无边框
    borderless: bool = False
    # 是否可以调整窗口大小（无边框模式下无效，需要自己实现边框拖动等功能）
    resizable: bool = False
    # 窗口帧率
    fps: int = 60
    # 窗口是否在创建时获得鼠标焦点
    mouse_focus: bool = True
del dataclass

class Window(pygame.Window):
    """
    窗口类，每一个实例就是一个窗口
    Window 类是对 pygame.Window 的封装，提供了更简洁的初始化接口和默认参数设置。
    """
    def __init__(self, window_config: WindowConfig):
        """
        初始化 Window 实例。
        Args:
            window_config (WindowConfig): 窗口配置数据类实例，包含窗口的各种参数。
        """
        super().__init__(
            title=window_config.title,
            size=window_config.window_size,
            position=window_config.window_position,
            borderless=window_config.borderless,
            resizable=window_config.resizable,
            mouse_focus=window_config.mouse_focus,
        )

        self.clock = pygame.time.Clock()     # 用于控制帧率的时钟对象
        self.fps = window_config.fps         # 窗口帧率

        self.screen = self.get_surface()     # 窗口的主 Surface 对象
        self.renderer = fantas.Renderer()    # 窗口的渲染器对象
        self.root_ui: fantas.UI = fantas.ColorBackground()    # 窗口的根 UI 元素

    def mainloop(self):
        """
        进入窗口的主事件循环，处理事件直到窗口关闭。
        """
        while True:
            self.clock.tick(self.fps)    # 限制帧率
            # 处理事件
            for event in pygame.event.get():
                if fantas.Debug.is_debug_window_open():
                    fantas.Debug.send_debug_command(str(event))
                if event.type == fantas.WINDOWCLOSE:
                    self.destroy()
                    return
            # 生成渲染命令
            self.renderer.pre_render(self.root_ui)
            # 渲染窗口
            self.renderer.render(self.screen)
            # 更新窗口显示
            self.flip()


