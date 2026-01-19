# fantas.nodebase

> fantas 树形节点模块

## fantas.Nodebase

树形节点基类，包含指针域的相关实现。
`Nodebase() -> Nodebase`
如果想要得到一个可用的树形节点，需要通过子类继承，然后由子类实现数据域的部分。

### 属性

一般情况下，建议把它们当作只读属性，因为修改树形结构时父节点和子节点的信息是需要同步变化的，如果你只修改了其中一个，会引发意想不到的错误。你应该用节点的方法来改变树形结构。

- **father**
  父节点指针。（你应该明白，在 python 里说指针意味着什么，这不过是一个变量名罢了）
  `father -> Nodebase | None`
  读取或设置父节点。
  默认为 None，表示没有父节点。

- **children**
  子节点列表。
  `children -> list[Nodebase]`
  存储子节点的列表，顺序为从左到右。
  默认为空列表，表示没有子节点。

### 方法

节点操作的很多方法和列表非常相似，实际上，你可以把它理解为一个保存子节点的列表，附加一个父节点属性。

- **Nodebase.append()**
  添加子节点至最后。
  `append(node: Nodebase)`

  - node (Nodebase): 要添加的子节点。

  如果子节点已经有父节点，会先自动脱离。

- **Nodebase.insert()**
  插入子节点至指定位置。
  `insert(index: int, node: Nodebase)`

  - index (int): 插入后的索引，如果索引越界，会插入在边界上。
  - node (Nodebase): 要插入的子节点

  如果子节点已有父节点，会先自动脱离。

- **Nodebase.remove()**
  移除指定的子节点。
  `remove(node: Nodebase)`

  - node (Nodebase): 要移除的子节点。

  如果子节点列表中没有 node，则抛出 `ValueError`。

- **Nodebase.pop()**
  移除并返回指定位置的子节点。
  `pop(index: int) -> Nodebase`
  - index (int): 要移除的子节点的索引。
  如果索引越界，则抛出 `IndexError`。

- **Nodebase.leave()**
  从父节点中脱离。
  `leave()`
  `node.leave()` 等价于 `node.father.remove(node)`，可以看到这种写法更加简洁。事实上该方法还会判断 `father` 是否为 `None`，所以如果父节点不存在，`leave()` 方法不会执行任何操作，也不会报错。

- **Nodebase.clear()**
  清空子节点。
  `clear()`
  这个方法会比逐个子节点调用 `leave()` 略快。

- **Nodebase.is_root()**
  判断节点是否为根节点。
  `is_root() -> bool`

- **Nodebase.is_leaf()**
  判断节点是否为叶子节点。
  `is_leaf() -> bool`

- **Nodebase.get_index()**
  查询自己在父节点的子节点列表中的索引。
  `get_index() -> int`

- **Nodebase.get_pass_path()**
  获取从自己到根节点的传递路径。
  `get_pass_path() -> list[Nodebase]`
  返回一个列表，包含从自己到根节点的所有节点。
