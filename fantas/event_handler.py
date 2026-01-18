from __future__ import annotations

import fantas

__all__ = (
    "EventHandler",
)

class EventHandler:
    """ 事件处理器，负责预处理并分发事件。 """
    def __init__(self, window: fantas.Window):
        self.window: fantas.Window = window    # 关联的窗口对象

        # 事件焦点映射字典
        self.focus: dict[fantas.EventCategory, fantas.UI | None] = {
            fantas.EventCategory.MOUSE   : None,    # 鼠标焦点 UI 元素
            fantas.EventCategory.KEYBOARD: None,    # 键盘焦点 UI 元素
            fantas.EventCategory.INPUT   : None,    # 输入焦点 UI 元素
            fantas.EventCategory.WINDOW  : None,    # 窗口焦点 UI 元素
            fantas.EventCategory.USER    : None,    # 用户自定义事件焦点 UI 元素
        }

        """
        事件监听注册表，是一个字典
        字典内的键值对为 事件类型: 另一个字典
        二级字典的键值对为 (UI 元素, 是否使用捕获阶段): 回调函数列表
        {
            event_type (int): {
                (ui_id (int), use_capture (bool)): [callback1, callback2, ...]
            }
        }
        """
        self.listeners: dict[int, dict[tuple[int, bool], list[callable]]] = {}
        for event_type in fantas.event_category_dict.keys():
            self.listeners[event_type] = {}

    def handle_event(self, event: fantas.Event):
        """
        处理单个事件。
        Args:
            event (fantas.Event): 要处理的事件对象。
        """
        # 获取事件分类
        event_category = fantas.get_event_category(event.type)
        # 如果事件有分类
        if event_category != fantas.EventCategory.NONE:
            # 获取该分类的焦点 UI 元素
            focused_ui = self.focus[event_category]
            # 如果焦点 UI 元素不为空
            if focused_ui is not None:
                # 构建传递路径
                event_pass_path = [focused_ui]
                focused_ui = focused_ui.father
                while focused_ui is not None:
                    event_pass_path.append(focused_ui)
                    focused_ui = focused_ui.father
                # 获取该事件类型的监听器字典
                event_listeners = self.listeners[event.type]
                # 如果有监听器注册
                if event_listeners:
                    # 事件传递 [根节点 -> ... -> 焦点节点（捕获阶段）, 焦点节点 -> ... -> 根节点（冒泡阶段）]
                    for ui in reversed(event_pass_path):
                        # 捕获阶段
                        # 依次调用回调函数
                        for callback in event_listeners.get((ui.ui_id, True), []):
                            # 如果回调函数返回 True，停止事件传递
                            if callback(event):
                                return
                    for ui in event_pass_path:
                        # 冒泡阶段
                        # 依次调用回调函数
                        for callback in event_listeners.get((ui.ui_id, False), []):
                            # 如果回调函数返回 True，停止事件传递
                            if callback(event):
                                return
    
    def add_event_listener(self, event_type: int, ui_element: fantas.UI, callback: callable, use_capture: bool = False):
        """
        为指定事件类型和 UI 元素添加事件监听器。
        Args:
            event_type (int): 事件类型。
            ui_element (fantas.UI): 关联的 UI 元素。
            callback (callable): 事件回调函数，接受一个 fantas.Event 参数，返回 bool。
            use_capture (bool): 是否在捕获阶段调用回调函数，默认为 False（冒泡阶段）。
        """
        # 构建监听器键
        listener_key = (ui_element.ui_id, use_capture)
        # 获取该事件类型的监听器字典
        event_listeners = self.listeners.get(event_type, None)
        # 如果有监听器字典
        if event_listeners is not None:
            # 获取注册的回调函数列表
            callback_list = event_listeners.get(listener_key, None)
            # 如果没有回调函数列表，创建一个新的列表
            if callback_list is None:
                event_listeners[listener_key] = [callback]
            # 否则，添加回调函数到列表中
            else:
                callback_list.append(callback)
        else:
            # 如果没有该事件类型的监听器字典，创建一个新的字典并添加回调函数列表
            self.listeners[event_type] = {listener_key: [callback]}
    
    def remove_event_listener(self, event_type: int, ui_element: fantas.UI, callback: callable, use_capture: bool = False):
        """
        移除指定事件类型和 UI 元素的事件监听器。
        Args:
            event_type (int): 事件类型。
            ui_element (fantas.UI): 关联的 UI 元素。
            callback (callable): 要移除的事件回调函数。
            use_capture (bool): 是否在捕获阶段调用回调函数，默认为 False（冒泡阶段）。
        """
        # 构建监听器键
        listener_key = (ui_element.ui_id, use_capture)
        # 获取该事件类型的监听器字典
        event_listeners = self.listeners.get(event_type, None)
        # 如果有监听器字典
        if event_listeners is not None:
            # 获取注册的回调函数列表
            callback_list = event_listeners.get(listener_key, None)
            # 如果有回调函数列表
            if callback_list is not None:
                # 尝试移除回调函数
                try:
                    callback_list.remove(callback)
                except ValueError:
                    pass
                # 如果回调函数列表为空，移除监听器键
                if not callback_list:
                    event_listeners.pop(listener_key)
    
    def set_focus(self, event_category: fantas.EventCategory, ui_element: fantas.UI | None):
        """
        设置指定事件类别的焦点 UI 元素。
        Args:
            event_category (fantas.EventCategory): 事件类别。
            ui_element (fantas.UI | None): 要设置为焦点的 UI 元素，或 None 清除焦点。
        """
        self.focus[event_category] = ui_element
