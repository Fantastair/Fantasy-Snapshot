from __future__ import annotations
from dataclasses import dataclass, field
from typing import Generic, TypeVar
from pathlib import Path

import fantas

__all__ = (
    "images",
    "fonts",
    "colors",
)

T = TypeVar('T')

@dataclass(slots=True)
class ResourceLoader(Generic[T]):
    """ 资源加载器抽象基类。 """
    _resources: dict[str, T] = field(default_factory=dict, init=False)

    def get(self, name: str) -> T:
        """ 根据名称获取已加载的资源。 """
        if name not in self._resources:
            raise KeyError(f"资源 '{name}' 未加载。")
        return self._resources[name]

def image_convert_hook(surface: fantas.Surface) -> fantas.Surface:
    """ 图像转换钩子函数，将图像转换为与显示器兼容的格式。 """
    return surface.convert()

def image_convert_alpha_hook(surface: fantas.Surface) -> fantas.Surface:
    """ 图像转换钩子函数，将图像转换为与显示器兼容的格式。 """
    return surface.convert_alpha()

@dataclass(slots=True)
class ImageLoader(ResourceLoader[fantas.Surface]):
    """ 图像资源加载器。 """

    def load_bitmap(self, path: Path, alias: str = None, hook: callable = image_convert_hook):
        """
        加载位图图像资源。
        Args:
            path (Path): 图像文件路径。
            alias (str, optional): 资源别名，默认为 None，使用文件名作为资源名称。
            hook (callable, optional): 图像转换钩子函数，默认为 image_convert_hook。
        """
        if not isinstance(path, Path):
            path = Path(path)
        self._resources[alias if alias else path.stem] = hook(fantas.image.load(path))

    def load_svg(self, path: Path, alias: str = None, size: int = 64, hook: callable = image_convert_alpha_hook):
        """
        加载 SVG 图像资源。
        Args:
            path (Path): SVG 文件路径。
            alias (str, optional): 资源别名，默认为 None，使用文件名作为资源名称。
            size (int, optional): 图像最长边大小，默认为 64 像素。
            hook (callable, optional): 图像转换钩子函数，默认为 image_convert_alpha_hook。
        """
        if not isinstance(path, Path):
            path = Path(path)
        self._resources[alias if alias else path.stem] = hook(fantas.image.load_sized_svg(path, size))
images = ImageLoader()

class FontLoader(ResourceLoader[fantas.Font]):
    """ 字体资源加载器。 """

    def load(self, path: Path, alias: str = None):
        """
        加载字体资源。
        Args:
            path (Path): 字体文件路径。
            alias (str, optional): 资源别名，默认为 None，使用文件名作为资源名称。
        """
        if not isinstance(path, Path):
            path = Path(path)
        font = fantas.Font(path)
        font.origin = True
        font.kerning = True
        self._resources[alias if alias else path.stem] = font

    _default_sysfont = None
    def get_default_sysfont(self) -> fantas.Font:
        """ 获取默认系统字体。 """
        if self._default_sysfont is None:
            self._default_sysfont = fantas.SysFont(("Noto Sans CJK SC", "PingFang SC", "Simhei", "Microsoft YaHei"), 16)
            self._default_sysfont.origin = True
            self._default_sysfont.kerning = True
        return self._default_sysfont
    def set_default_sysfont(self, font: fantas.Font):
        """ 设置默认系统字体。 """
        self._default_sysfont = font
    DEFAULTSYSFONT = property(get_default_sysfont, set_default_sysfont)
fonts = FontLoader()

class ColorLoader(ResourceLoader[fantas.Color]):
    """ 颜色资源加载器。 """

    def load(self, color: str, name: str = None):
        """
        加载颜色资源。
        Args:
            color (str): 颜色字符串（如 "#RRGGBBAA" 或 "red"）。
            name (str, optional): 资源名称，默认为 None，使用颜色字符串作为资源名称。
        """
        self._resources[name if name else color] = fantas.Color(color)
colors = ColorLoader()
