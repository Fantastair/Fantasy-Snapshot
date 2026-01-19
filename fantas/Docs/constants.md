# fantas.constants

> fantas 常量

该模块包含 fantas 使用或定义的多种常量，这些常量会自动放入 fantas 的命名空间里。

- fantas 的各种事件类型代号，这是一系列 int 类型的数据，代表了各种可能产生的事件。
- **DEFAULTRECT**
  默认矩形对象，参数为（0, 0, 0, 0）。

- **DEFAULTFONT**
  默认字体，这是一个自动加载的英文字体。

- **fantas.EventCategory**
  fantas 的事件分类枚举。
  包含如下类别：
  - EventCategory.MOUSE 鼠标事件
  - EventCategory.KETBOARD 键盘事件
  - EventCategory.INPUT 文本输入事件
  - EventCategory.WINDOW 窗口事件
  - EventCategory.USER 用户自定义事件
  - EventCategory.NONE 未分类事件

除此之外，还在这里定义了 2 个函数：

- **fantas.custom_event()**
  生成一个自定义事件类型 id。

  `custom_event(event_category: fantas.EventCategory = fantas.EventCategory.USER) -> fantas.EventType`
  
  每个类型的事件都有一个独特的 id，为了避免与 fantas 内置的事件类型 id 冲突，从该函数获取事件类型 id。

  - `event_category (fantas.EventCategory):` 事件分类，默认为 USER。

- **fantas.get_event_category()**
  获取事件分类。

  `get_event_category(event_type: fantas.EventType) -> fantas.EventCategory`
  
  根据传入的事件类型 id，返回对应的事件分类枚举值。

  - `event_type (fantas.EventType):` 事件类型 id。
