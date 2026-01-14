import functools
from typing import Protocol, Any, runtime_checkable, Literal, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from . import SMU

def smu_script(name: str):
    def _decorator(func):
        @functools.wraps(func)
        def wrapper(smu, *args, **kwargs):
            return func(smu, *args, **kwargs)

        wrapper._is_smu_script = True
        wrapper._smu_script_name = name

        return wrapper

    return _decorator

@runtime_checkable
class SMUScriptCallable(Protocol):
    def __call__(self, smu: SMU, *args, **kwargs) -> Any | list | dict:
        ...

@dataclass
class SMUScriptParameter:
    name: str
    value_type: Any
    default: Any

@dataclass
class SMUScript:
    name: str
    parameters: list[SMUScriptParameter]
    callable: SMUScriptCallable