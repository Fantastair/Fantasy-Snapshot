# fantas.constants

> fantas 常量

该模块包含 fantas 使用或定义的多种常量，这些常量会自动放入 fantas 的命名空间里。
以下是一些说明（部分从 pygame.locals 导入的常量 fantas 并不会使用，虽然他们存在）:

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

- **fantas.custom_event()**
  生成一个自定义事件类型 id。
  `custom_event() -> int`
  返回一个可用的自定义事件 id。可以多次调用，得到多个自定义事件 id。这些 id 不会和已有的事件冲突。

- **fantas.get_event_category()**
  获取一个事件的分类。
  `get_event_category(event_type: int) -> EventCategory`
  返回指定类型事件的分类。
