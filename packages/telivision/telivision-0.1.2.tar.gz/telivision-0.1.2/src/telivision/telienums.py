from enum import Enum, auto, StrEnum
from functools import total_ordering


@total_ordering
class VerbosityLevel(Enum):
    NONE = 0
    LOW = 1
    FULL = 2

    def __lt__(self, other):
        if not isinstance(other, VerbosityLevel):
            return NotImplemented
        return self.value < other.value


class CaptureMode(StrEnum):
    CONTINUOUS = auto()
    MANUAL = auto()
    END = auto()
