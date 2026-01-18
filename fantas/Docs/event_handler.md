# fantas.event_handler

> fantas 事件处理模块。

## fantas.EventHandler

事件处理器是跟随窗口的，负责预处理并分发事件。

`EventHandler(window: fantas.Window) -> fantas.EventHandler`

### 属性

- **window (fantas.Window)**: 关联的窗口对象。
- **focus (dict[fantas.EventCategory, fantas.UI | None])**: 事件焦点映射表，每一分类的事件只会发送给对应焦点所在的传递路径上的 UI 元素进行处理。
- **listeners (dict[int, dict[tuple[int, bool], list[callable]]])**: 事件监听注册表。
  本身是一个字典，每一个事件类型都有一个子字典，子字典的键是（UI，是否捕获）元组，值是回调函数列表

### 方法

- **EventHandler.handle_event()**

  处理单个事件。

  `handle_event(event: fantas.Event)`
  
  - **event (fantas.Event)**: 要处理的事件对象。

- **EventHandler.add_event_listener()**

    注册事件监听器。
    
    `add_event_listener(event_type: int, ui_element: fantas.UI, callback: callable, use_capture: bool = False)`

    - **event_type (int)**: 事件类型。
    - **ui_element (fantas.UI)**: 关联的 UI 元素
    - **callback (callable)**: 事件回调函数，接收一个 `fantas.Event` 对象作为参数。
    - **use_capture (bool, optional)**: 是否在捕获阶段调用回调

- **EventHandler.remove_event_listener()**

    移除事件监听器。

    `remove_event_listener(event_type: int, ui_element: fantas.UI, callback: callable, use_capture: bool = False)`

    - **event_type (int)**: 事件类型。
    - **ui_element (fantas.UI)**: 关联的 UI 元素
    - **callback (callable)**: 事件回调函数，接收一个 `fantas.Event` 对象作为参数。
    - **use_capture (bool, optional)**: 是否在捕获阶段调用回调

- **EventHandler.set_focus()**

    设置指定分类事件的焦点 UI 元素。

    `set_focus(category: fantas.EventCategory, ui_element: fantas.UI | None)`

    - **category (fantas.EventCategory)**: 事件分类。
    - **ui_element (fantas.UI | None)**: 要设置为焦点的 UI 元素，或 `None` 清除焦点。
