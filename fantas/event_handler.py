from __future__ import annotations

import fantas

__all__ = (
    "EventHandler",
    "custom_event",
    "get_event_category",
)

class EventHandler:
    """ 事件处理器，负责预处理并分发事件。 """
    def __init__(self, window: fantas.Window):
        self.window        : fantas.Window   = window            # 关联的窗口对象
        self.active_ui     : fantas.UI       = window.root_ui    # 当前激活的 UI 元素
        self.hover_ui      : fantas.UI       = window.root_ui    # 当前鼠标悬停的 UI 元素
        self.last_mouse_pos: fantas.IntPoint = (0, 0)            # 上一帧的鼠标位置
        self.listeners     : dict[fantas.ListenerKey, list[fantas.ListenerFunc]] = {}    # 事件监听注册表

        # 注册鼠标移动事件的默认处理器，用于更新悬停的 UI 元素
        self.add_event_listener(fantas.MOUSEMOTION, self.window.root_ui, True, self.handle_mousemotion_event)

    def handle_mousemotion_event(self, event: fantas.Event):
        """
        处理鼠标移动事件，更新悬停的 UI 元素。
        Args:
            event (fantas.Event): 鼠标移动事件对象。
        """
        # 更新悬停的 UI 元素
        if event.pos != self.last_mouse_pos:    # 惰性更新
            self.last_mouse_pos = event.pos
            self.hover_ui = self.window.renderer.coordinate_hit_test(event.pos)

    def handle_event(self, event: fantas.Event, focused_ui: fantas.UI | None = None):
        """
        处理单个事件。
        Args:
            event      (fantas.Event)    : 要处理的事件对象。
            focused_ui (fantas.UI | None): 事件传递的焦点 UI 元素，为 None 会自动确认焦点。
        """
        # 获取焦点 UI 元素
        if focused_ui is None:
            # 鼠标事件的焦点为当前悬停的 UI 元素，其他事件的焦点为当前激活的 UI 元素
            focused_ui = self.hover_ui if get_event_category(event.type) == fantas.EventCategory.MOUSE else self.active_ui
        # 构建传递路径
        event_pass_path = focused_ui.get_pass_path()
        # 事件传递 [根节点 -> ... -> 焦点节点（捕获阶段）, 焦点节点 -> ... -> 根节点（冒泡阶段）]
        for ui in reversed(event_pass_path):
            # 捕获阶段
            # 依次调用回调函数
            for callback in self.listeners.get((event.type, ui.ui_id, True), []):
                # 如果回调函数返回 True，停止事件传递
                if callback(event):
                    return
        for ui in event_pass_path:
            # 冒泡阶段
            # 依次调用回调函数
            for callback in self.listeners.get((event.type, ui.ui_id, False), []):
                # 如果回调函数返回 True，停止事件传递
                if callback(event):
                    return
    
    def add_event_listener(self, event_type: fantas.EventType, ui_element: fantas.UI, use_capture: bool, listener: fantas.ListenerFunc):
        """
        为指定事件类型和 UI 元素添加事件监听器。
        Args:
            event_type  (fantas.EventType)   : 事件类型。
            ui_element  (fantas.UI)          : 关联的 UI 元素。
            use_capture (bool)               : 是否在捕获阶段调用回调函数。
            listener    (fantas.ListenerFunc): 要添加的事件监听函数。
        """
        # 获取或创建该监听器键的监听函数列表
        listener_list = self.listeners.setdefault((event_type, ui_element.ui_id, use_capture), [])
        # 添加回调函数到列表
        listener_list.append(listener)

    def remove_event_listener(self, event_type: fantas.EventType, ui_element: fantas.UI, use_capture: bool, listener: fantas.ListenerFunc):
        """
        移除指定事件类型和 UI 元素的事件监听器。
        Args:
            event_type  (fantas.EventType)   : 事件类型。
            ui_element  (fantas.UI)          : 关联的 UI 元素。
            use_capture (bool)               : 是否在捕获阶段调用回调函数。
            listener    (fantas.ListenerFunc): 要移除的事件监听函数。
        Raises:
            ValueError: 如果指定的监听器不存在则引发此异常。
        """
        # 获取该监听器键的回调函数列表
        listener_list = self.listeners.get((event_type, ui_element.ui_id, use_capture), [])
        # 尝试移除回调函数
        try:
            listener_list.remove(listener)
        except ValueError:
            raise ValueError("监听器不存在。") from None

def custom_event() -> fantas.EventType:
    """
    生成一个自定义事件类型 id。
    Returns:
        fantas.EventType: 自定义事件类型 id。
    """
    t = fantas.event.custom_type()
    fantas.event_category_dict[t] = fantas.EventCategory.USER
    fantas.event.set_allowed(t)
    return t

def get_event_category(event_type: fantas.EventType) -> fantas.EventCategory:
    """
    获取事件分类。
    Args:
        event_type (fantas.EventType): 事件类型。
    Returns:
        fantas.EventCategory: 事件分类枚举值。
    """
    return fantas.event_category_dict.get(event_type, fantas.EventCategory.NONE)
