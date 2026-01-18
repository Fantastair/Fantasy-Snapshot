from __future__ import annotations
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
    # 窗口是否在创建时获得输入焦点
    input_focus: bool = True
    # 是否允许高DPI显示
    allow_high_dpi: bool = True
del dataclass

class Window(pygame.Window):
    """
    窗口类，每一个实例就是一个窗口。
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
            input_focus=window_config.input_focus,
            allow_high_dpi=window_config.allow_high_dpi,
        )

        self.clock = pygame.time.Clock()     # 用于控制帧率的时钟对象
        self.fps = window_config.fps         # 窗口帧率

        self.screen = self.get_surface()                         # 窗口的主 Surface 对象
        self.renderer = fantas.Renderer()                        # 窗口的渲染器对象
        self.event_handler = fantas.EventHandler(window=self)    # 窗口的事件处理器对象

        self.root_ui: fantas.UI = fantas.ColorBackground()    # 窗口的根 UI 元素，默认为纯色背景

        self.event_handler.add_event_listener(fantas.WINDOWCLOSE, self.root_ui, self.close, False)    # 注册窗口关闭事件监听器
        self.event_handler.set_focus(fantas.EventCategory.WINDOW, self.root_ui)    # 设置窗口事件焦点为根 UI 元素

        self.running = True    # 窗口运行状态标志

    def mainloop(self):
        """
        进入窗口的主事件循环，直到窗口关闭。
        """
        fantas.event.clear()
        while self.running:
            self.clock.tick(self.fps)    # 限制帧率
            # 处理事件
            for event in pygame.event.get():
                self.event_handler.handle_event(event)
            # 生成渲染命令
            self.renderer.pre_render(self.root_ui)
            # 渲染窗口
            self.renderer.render(self.screen)
            # 更新窗口显示
            self.flip()
    
    def close(self, event: fantas.Event):
        """
        关闭窗口并释放资源。
        Args:
            event (fantas.Event): 关闭事件对象。
        """
        if event.window == self:
            self.running = False
    
    def get_root_ui(self) -> fantas.UI:
        """
        获取窗口的根 UI 元素。
        Returns:
            root_ui (fantas.UI): 窗口的根 UI 元素。
        """
        return self.root_ui
    
    def set_root_ui(self, root_ui: fantas.UI):
        """
        设置窗口的根 UI 元素。
        Args:
            root_ui (fantas.UI): 要设置的根 UI 元素。
        """
        # 移除旧根节点的窗口关闭事件监听器
        self.event_handler.remove_event_listener(fantas.WINDOWCLOSE, self.root_ui, self.close, False)
        self.root_ui = root_ui
        # 添加新根节点的窗口关闭事件监听器
        self.event_handler.add_event_listener(fantas.WINDOWCLOSE, self.root_ui, self.close, False)
        self.event_handler.set_focus(fantas.EventCategory.WINDOW, self.root_ui)    # 设置窗口事件焦点为根 UI 元素

    def mainloop_debug(self):
        """
        以调试模式进入窗口的主事件循环，直到窗口关闭。
        """
        if not fantas.Debug.is_debug_window_open():
            raise RuntimeError("调试窗口未打开，无法进入调试主循环。")
        while True:
            self.clock.tick(self.fps)    # 限制帧率
            # 处理事件
            for event in pygame.event.get():
                if fantas.Debug.is_debug_window_open():    # 发送事件信息到调试窗口
                    fantas.Debug.send_debug_command(str(event))
                if event.type == fantas.WINDOWCLOSE:
                    self.destroy()
                    return
            # 处理调试输出
            while not fantas.Debug.queue.empty():
                output = fantas.Debug.queue.get()
                self.handle_debug_output(output)
            # 生成渲染命令
            self.renderer.pre_render(self.root_ui)
            # 渲染窗口
            self.renderer.render(self.screen)
            # 更新窗口显示
            self.flip()
    
    def handle_debug_output(self, output: str):
        """
        处理从调试窗口接收到的输出信息。
        Args:
            output (str): 从调试窗口接收到的输出信息字符串。
        """
        # if output == "started":
            # self.focus()
        print(f"[Debug Output] {output}")
