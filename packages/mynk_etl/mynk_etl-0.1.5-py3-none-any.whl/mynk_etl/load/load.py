from abc import ABC, abstractmethod
from typing import Any

class Load(ABC):

    @abstractmethod
    def streamWriter(self, param_dct: dict[str, Any]) -> None:
        ...

    @abstractmethod
    def nonStreamWriter(self, param_dct: dict[str, Any]) -> None:
        ...

    # @abstractmethod
    # def multiSinkWriter(self, param_dct: dict[str, Any]) -> None:
    #     ...