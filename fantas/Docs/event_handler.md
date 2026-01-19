# fantas.event_handler

> fantas 事件处理模块。

## fantas.EventHandler

事件处理器是跟随窗口的，负责预处理并分发事件。

`EventHandler(window: fantas.Window) -> fantas.EventHandler`

### 属性

- **window (fantas.Window)**: 关联的窗口对象。
- **active_ui (fantas.UI)**: 当前激活的 UI 元素。
- **hover_ui (fantas.UI)**: 当前鼠标悬停的 UI 元素。
- **last_mouse_pos (fantas.IntPoint)**: 上一帧的鼠标位置。
- **listeners (dict[fantas.ListenerKey, list[fantas.ListenerFunc]])**: 事件监听注册表。
  一个字典，键为监听器键（`fantas.ListenerKey`），值为监听器函数列表（`list[fantas.ListenerFunc]`）。可以用一个事件类型、UI 元素唯一标识和是否为捕获阶段的布尔值来唯一确定一个监听函数列表。

### 方法

- **EventHandler.handle_mousemotion_event()**

  处理鼠标移动事件，更新悬停的 UI 元素。

  `handle_mousemotion_event(event: fantas.Event)`

  - **event (fantas.Event)**: 鼠标移动事件对象。

- **EventHandler.handle_event()**

  处理单个事件。

  `handle_event(event: fantas.Event)`
  
  - **event (fantas.Event)**: 要处理的事件对象。

- **EventHandler.add_event_listener()**

    注册事件监听器。
    
    `add_event_listener(event_type: fantas.EventType, ui_element: fantas.UI, use_capture: bool, callback: fantas.ListenerFunc)`

    - **event_type (fantas.EventType)**: 事件类型。
    - **ui_element (fantas.UI)**: 关联的 UI 元素
    - **use_capture (bool)**: 是否在捕获阶段调用回调
    - **callback (fantas.ListenerFunc)**: 事件回调函数，接收一个 `fantas.Event` 对象作为参数。

- **EventHandler.remove_event_listener()**

    移除事件监听器。

    `remove_event_listener(event_type: fantas.EventType, ui_element: fantas.UI, use_capture: bool, callback: fantas.ListenerFunc)`

    - **event_type (fantas.EventType)**: 事件类型。
    - **ui_element (fantas.UI)**: 关联的 UI 元素
    - **callback (fantas.ListenerFunc)**: 事件回调函数，接收一个 `fantas.Event` 对象作为参数。
    - **use_capture (bool)**: 是否在捕获阶段调用回调

## 其他函数

- **custom_event()**

    生成一个自定义事件类型 id.

    `custom_event() -> fantas.EventType`

- **get_event_category()**

    获取事件分类。

    `get_event_category(event_type: fantas.EventType) -> fantas.EventCategory`
