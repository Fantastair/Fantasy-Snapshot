# fantas

> fantas 顶级包

fantas 包代表了供他人使用的顶级包。和大部分 python 包一样，fantas 包含了许多子模块，不过一般情况下只导入顶级包就可以了。

fantas 中定义了许多有意义的常量，如果你实在不想在访问这些常量时都加上 `fantas.` 这个前缀，可以先 `from fantas.constants import *`，虽然大部分 python 教程里都不会建议你导入一个模块的所有变量，因为这会污染全局命名空间，尤其是在你不清楚对方模块里到底有哪些变量时。

在你导入 fantas 时，所有的子模块都会被自动导入并初始化，大部分子模块的接口都直接放在 fantas 的命名空间里，使用时不需要加上子模块名称前缀（注意，是大部分，有些接口是直接从 pygame 那里获取的，为了避免未知的命名冲突，这些接口保存在子模块的命名空间里，比如 fantas.time、fantas.event等，其实都是 pygame 的子模块，被我越级提升了）

- fantas.package_path()
  返回 fantas 包的安装路径。
  `package_path() -> Path`
  返回 fantas 包的安装路径字符串。

- fantas.generate_unique_id()
    生成一个全局唯一的整数 ID。
    `generate_unique_id() -> int`
    返回一个全局唯一的整数 ID，每次调用都会返回一个新的 ID。
    id 没有任何特殊的格式，纯粹是一个递增的整数。

- fantas.get_time_ns()
    获取当前的高精度时间戳，单位为纳秒。
    `get_time_ns() -> int`
    返回一个纳秒级整数时间戳。
    具体时间取决于操作系统，应该通过计算时间差来得到经过的相对时间。
