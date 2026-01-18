from __future__ import annotations
from dataclasses import dataclass, field
from itertools import count

import fantas

__all__ = (
    "UI",
)

ui_id_counter = count()

@dataclass(slots=True)
class UI(fantas.NodeBase):
    """ 显示元素基类。 """
    father: UI | None = None    # 指向父显示元素
    children: list[UI] = field(default_factory=list)    # 子显示元素列表
    ui_id: int = field(default_factory=lambda: next(ui_id_counter))    # 唯一标识 ID

    def create_render_commands(self, offset: fantas.Point = (0, 0)):
        """
        创建渲染命令列表，由子类实现，本方法会遍历子节点并生成渲染命令
        Args:
            offset (Point): 当前元素的偏移位置，用于计算子元素的绝对位置。
        Yields:
            RenderCommand: 渲染命令对象。
        """
        for child in self.children:
            yield from child.create_render_commands(offset)
    