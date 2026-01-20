from __future__ import annotations
from dataclasses import dataclass

import fantas
from pygame.window import Window as PygameWindow

__all__ = (
    "WindowConfig",
    "Window",
)

@dataclass(slots=True)
class WindowConfig:
    """
    窗口配置数据类，包含创建窗口所需的各种参数。
    Args:
        title (str): 窗口标题。
        window_size (fantas.IntPoint): 窗口尺寸（宽, 高）（像素）。
        window_position (fantas.IntPoint | int): 窗口位置（x, y）或预设常量 fantas.WINDOWPOS_CENTERED / fantas.WINDOWPOS_UNDEFINED。
        borderless (bool): 窗口是否无边框。
        resizable (bool): 是否可以调整窗口大小。
        fps (int): 窗口帧率。
        mouse_focus (bool): 窗口是否在创建时获得鼠标焦点。
        input_focus (bool): 窗口是否在创建时获得输入焦点。
        allow_high_dpi (bool): 是否允许高 DPI 显示。
    """
    title          : str                   = "Fantas Window"
    window_size    : fantas.IntPoint       = (1280, 720)
    window_position: fantas.IntPoint | int = fantas.WINDOWPOS_UNDEFINED
    borderless     : bool                  = False
    resizable      : bool                  = False
    fps            : int                   = 60
    mouse_focus    : bool                  = True
    input_focus    : bool                  = True
    allow_high_dpi : bool                  = True

class Window(PygameWindow):
    """
    窗口类，每一个实例就是一个窗口。
    """
    def __init__(self, window_config: WindowConfig):
        """
        初始化 Window 实例。
        Args:
            window_config (WindowConfig): 窗口配置数据类实例，包含窗口的各种参数。
        """
        # 初始化父类
        super().__init__(
            title          = window_config.title,
            size           = window_config.window_size,
            position       = window_config.window_position,
            borderless     = window_config.borderless,
            resizable      = window_config.resizable,
            mouse_focus    = window_config.mouse_focus,
            input_focus    = window_config.input_focus,
            allow_high_dpi = window_config.allow_high_dpi,
        )

        self.running      : bool                = True                     # 窗口运行状态标志
        self.fps          : int                 = window_config.fps        # 窗口帧率设置
        self.clock        : fantas.time.Clock   = fantas.time.Clock()      # 用于控制帧率的时钟对象
        self.screen       : fantas.Surface      = self.get_surface()       # 窗口的主 Surface 对象
        self.renderer     : fantas.Renderer     = fantas.Renderer(self)    # 窗口的渲染器对象
        self.root_ui      : fantas.UI           = fantas.UI()              # 窗口的根 UI 元素是一个空的根节点
        self.event_handler: fantas.EventHandler = fantas.EventHandler(window=self)    # 窗口的事件处理器对象

        # 方便访问根 UI 元素的方法
        self.append: callable = self.root_ui.append
        self.insert: callable = self.root_ui.insert
        self.remove: callable = self.root_ui.remove
        self.pop   : callable = self.root_ui.pop
        self.clear : callable = self.root_ui.clear
        # 方便访问事件处理器的管理监听器方法
        self.add_event_listener   : callable = self.event_handler.add_event_listener
        self.remove_event_listener: callable = self.event_handler.remove_event_listener

    def mainloop(self):
        """
        进入窗口的主事件循环，直到窗口关闭。
        """
        # 清空事件队列
        fantas.event.clear()
        # 预生成传递路径缓存
        self.root_ui.build_pass_path_cache()
        # 主循环
        while self.running:
            # 限制帧率
            self.clock.tick(self.fps)
            # 处理事件
            for event in fantas.event.get():
                self.event_handler.handle_event(event)
            # 生成渲染命令
            self.renderer.pre_render(self.root_ui)
            # 渲染窗口
            self.renderer.render(self.screen)
            # 更新窗口显示
            self.flip()
        # 退出主循环后销毁窗口
        self.destroy()
    
    def mainloop_debug(self):
        """
        以调试模式进入窗口的主事件循环，直到窗口关闭。
        """
        # === 调试 ===
        if not fantas.Debug.is_debug_window_open():
            raise RuntimeError("调试窗口未打开，无法进入调试主循环。")
        # === 调试 ===
        # 清空事件队列
        fantas.event.clear()
        # 预生成传递路径缓存
        self.root_ui.build_pass_path_cache()
        # 主循环
        while self.running:
            # 限制帧率
            self.clock.tick(self.fps)
            # 处理事件
            for event in fantas.event.get():
                # === 调试 ===
                # 发送事件信息到调试窗口
                if fantas.Debug.is_debug_window_open():
                    fantas.Debug.send_debug_command(str(event))
                # === 调试 ===
                self.event_handler.handle_event(event)
            # === 调试 ===
            # 处理调试输出
            while not fantas.Debug.queue.empty():
                output = fantas.Debug.queue.get()
                self.handle_debug_output(output)
            # === 调试 ===
            # 生成渲染命令
            self.renderer.pre_render(self.root_ui)
            # 渲染窗口
            self.renderer.render(self.screen)
            # 更新窗口显示
            self.flip()
        # 退出主循环后销毁窗口
        self.destroy()
    
    def handle_debug_output(self, output: str):
        """
        处理从调试窗口接收到的输出信息。
        Args:
            output (str): 从调试窗口接收到的输出信息字符串。
        """
        # if output == "started":
            # self.focus()
        print(f"[Debug Output] {output}")
