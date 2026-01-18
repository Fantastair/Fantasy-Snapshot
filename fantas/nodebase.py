from __future__ import annotations
from dataclasses import dataclass, field

__all__ = (
    "NodeBase",
)

@dataclass(slots=True)
class NodeBase:
    """ 树形节点基类，数据域由子类实现 """
    father: NodeBase | None = None                            # 指向父节点 
    children: list[NodeBase] = field(default_factory=list)    # 存储孩子节点，有序

    # === 结构操作方法 ===

    def append(self, node: NodeBase):
        """
        添加 node 节点至最后子节点，node 的子节点会跟随 node
        如果 node 已有父节点，则会先将 node 从其父节点中移除
        Args:
            node (NodeBase): 要添加的节点
        """
        if not node.is_root():
            node.leave()
        node.father = self
        self.children.append(node)

    def insert(self, index: int, node: NodeBase):
        """
        插入 node 至 index 位置
        如果 node 已有父节点，则会先将 node 从其父节点中移除
        Args:
            node (NodeBase): 要插入的节点
            index (int): 插入位置索引
        """
        if not node.is_root():
            node.leave()
        node.father = self
        self.children.insert(index, node)

    def remove(self, node: NodeBase):
        """
        从自己的子节点中移除 node
        试图移除不存在的节点是安全的
        Args:
            node (NodeBase): 要移除的节点
        """
        if node in self.children:
            self.children.remove(node)
            node.father = None

    def pop(self, index: int) -> NodeBase:
        """
        移除index位置的node
        Args:
            index (int): 要移除节点的位置索引
        Returns:
            node (NodeBase): 被移除的节点
        """
        node = self.children.pop(index)
        node.father = None
        return node

    def leave(self):
        """ 从父节点中移除 """
        if self.father is not None:
            self.father.remove(self)
        
    def clear(self):
        """ 移除所有子节点 """
        for child in self.children:
            child.father = None
        self.children.clear()

    # === 信息查询方法 ===

    def is_root(self) -> bool:
        """ 是否为根节点 """
        return self.father is None

    def is_leaf(self) -> bool:
        """ 是否为叶子节点 """
        return not self.children

    def get_index(self) -> int:
        """ 查询自己在父节点中的位置 """
        return self.father.children.index(self)
