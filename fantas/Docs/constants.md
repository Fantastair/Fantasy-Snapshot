# fantas.constants

> fantas 常量

该模块包含 fantas 使用或定义的多种常量，这些常量会自动放入 fantas 的命名空间里。

- fantas 的各种事件类型代号，这是一系列 int 类型的数据，代表了各种可能产生的事件。
- **DEFAULTRECT**
  默认矩形对象，参数为（0, 0, 0, 0）。

- **DEFAULTFONT**
  默认字体，这是一个自动加载的英文字体。

- **Quadrant**
  象限枚举。
  低 2 位用于快速符号计算，高 4 位作为单比特掩码。
  
  ``` python
  fantas.Quadrant.TOPRIGHT    = 0b000101
  fantas.Quadrant.TOPLEFT     = 0b001000
  fantas.Quadrant.BOTTOMLEFT  = 0b010010
  fantas.Quadrant.BOTTOMRIGHT = 0b100011
  ```

- **BoxMode**
  盒子模式枚举，用于控制边框的扩展方向。

  - `fantas.BoxMode.INSIDE`: 边框向内扩展。
  - `fantas.BoxMode.OUTSIDE`: 边框向外扩展。
  - `fantas.BoxMode.INOUTSIDE`: 边框向内外各扩展一半。

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

  - `event_category (fantas.EventCategory):` 事件分类，默认为 USER。

  每个类型的事件都有一个独特的 id，为了避免与 fantas 内置的事件类型 id 冲突，从该函数获取事件类型 id。
  注意，fantas 默认禁用不需要的事件，创建自定义事件后需要手动启用该事件类型才能接收此事件。

- **fantas.get_event_category()**
  获取事件分类。

  `get_event_category(event_type: fantas.EventType) -> fantas.EventCategory`
  
  根据传入的事件类型 id，返回对应的事件分类枚举值。

  - `event_type (fantas.EventType):` 事件类型 id。
