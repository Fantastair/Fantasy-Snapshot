# fantas.font

> fantas 的字体支持模块。

- **fantas.Font**
  字体对象类型。
  用于表示和操作字体的对象，支持加载系统字体和自定义字体文件。
  `fantas.Font(file: fantas.FileLike | None, size: float = 0, font_index: int = 0, resolution: int = 0, ucs4: int = False) -> fantas.Font`**

  ## 属性

  - `FANTASID: int`
    字体的唯一标识符。

  ## 方法

  - get_widthes()
    获取制定样式文本的字符宽度度量信息。
    `fantas.Font.get_widthes(self, style_flag: fantas.TextStyleFlag, size: float, text: str) -> tuple[int]`
    该方法会缓存计算结果以提升性能。

- **fantas.TextStyle**
  文本样式类。

```python
TextStyle(
    font: fantas.Font = fantas.DEFAULTFONT,
    size: float = 16.0,
    fgcolor: fantas.ColorLike = 'black',
    style_flag: fantas.TextStyleFlag = fantas.TEXTSTYLEFLAG_DEFAULT
) -> fantas.TextStyle
```

## 函数

- **fantas.SysFont**
  加载系统字体并返回字体对象。
  `fantas.SysFont(name: str, size: float = 16) -> fantas.Font`

- **fantas.get_font_by_id**
  通过字体 ID 获取字体对象。
  `fantas.get_font_by_id(font_id: int) -> fantas.Font | None`
