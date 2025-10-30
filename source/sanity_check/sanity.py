from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List


class SanityFailLevel(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class Sanity(ABC):
    DEPENDENCY: List[Sanity] = []

    def __init__(self, nice_name: str, fail_level: SanityFailLevel, default_check: bool):
        self.nice_name = nice_name
        self.fail_level = fail_level
        self.default_check = default_check

    @abstractmethod
    def check(self) -> List[str]:
        """Method to check the integrity of an element."""

    def fix(self) -> None:
        """Method to resolve a wrong check."""

    @property
    def has_fix(self) -> bool:
        return self.__class__.fix != Sanity.fix
