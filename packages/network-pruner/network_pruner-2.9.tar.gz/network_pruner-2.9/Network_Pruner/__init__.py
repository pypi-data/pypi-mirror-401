# Network_Pruner/__init__.py

from .FAIR_Pruner import get_metrics, get_ratios, get_skeleton, prune

# 对外导出（包级别）
__all__ = ["FAIR_Pruner", "get_metrics", "get_ratios", "get_skeleton", "prune"]


class _FAIRPrunerAPI:
    __slots__ = ()
    _public = ["get_metrics", "get_ratios", "get_skeleton", "prune"]

    def __dir__(self):
        # 让 dir(fp) / IDE 补全只显示公共 API
        return list(self._public)

    def __getattr__(self, name: str):
        # 只允许访问公共 API
        if name in self._public:
            return globals()[name]
        raise AttributeError(
            f"'{__name__}.FAIR_Pruner' exposes only public APIs: {', '.join(self._public)}. "
            f"Do not rely on internal helpers."
        )


# 关键：用同名对象“遮住”子模块，让 `from Network_Pruner import FAIR_Pruner as fp` 拿到这个门面
FAIR_Pruner = _FAIRPrunerAPI()


def __dir__():
    # 让 `dir(Network_Pruner)` 也只显示公共 API
    return sorted(__all__)


def __getattr__(name: str):
    # 访问未导出的符号时给出明确提示
    raise AttributeError(
        f"'{__name__}' exposes only public APIs: {', '.join(__all__)}. "
        f"Do not rely on internal helpers."
    )
