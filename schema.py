from enum import Enum, StrEnum
from dataclasses import dataclass


class Swing(StrEnum):
    TRUE = "swung/shuffled"
    FALSE = "played straight"


class Tempo(Enum):
    EIGHTYISH = range(76, 85)
    NINETYISH = range(85, 98)
    HUNDREDISH = range(98, 106)
    HUNDREDTENISH = range(107, 115)
    HUNDREDTWENTYISH = range(115, 125)
    HUNDREDTHIRTYISH = range(125, 133)
    HUNDREDFOURTYISH = range(133, 146)
    HUNDREDFIFTYISH = range(146, 156)
    HUNDREDSIXTYISH = range(156, 166)
    HUNDREDSEVENTYISH = range(166, 175)


@dataclass
class SongSeed:
    swing: str
    tempo: str
    attitude: str
    sensation: str
    lyric_prompt: str
