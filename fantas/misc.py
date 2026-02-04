from pathlib   import Path
from itertools import count
from importlib import resources
from functools import lru_cache, wraps
from time import perf_counter_ns as get_time_ns

__all__ = (
    "get_time_ns",
    "package_path",
    "generate_unique_id",
    "lru_cache_typed",
)

# 提供 fantas 包的路径获取函数
def package_path():
    """
    获取 fantas 包的目录路径。
    Returns:
        path (Path): 模块所在的文件系统路径。
    """
    return Path(resources.files(__name__))

# 全局唯一 ID 生成器
id_counter = count()
def generate_unique_id() -> int:
    """
    生成一个全局唯一的整数 ID。
    Returns:
        int: 唯一整数 ID。
    """
    return next(id_counter)


# 类型装饰器以支持类型注解的 lru_cache
def lru_cache_typed(maxsize=128, typed=False):
    """
    生成一个保留原函数类型签名的 LRU 缓存装饰器。
    Args:
        maxsize (int): 缓存的最大数目。
        typed (bool) : 是否区分不同类型的参数。
    Returns:
        Callable: 装饰器函数。
    """
    def decorator(func):
        @wraps(func)  # 用typing.wraps保留类型签名
        @lru_cache(maxsize=maxsize, typed=typed)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
