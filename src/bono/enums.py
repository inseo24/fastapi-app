from enum import Enum


class AppEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)