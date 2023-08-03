from enum import Enum


class TypoSerializer:
    removed_dup = 0


class DifferenceEnum(Enum):
    wrong = 'Wrong Letter'
    extra = 'Extra Letter'


class DifferenceSerializer:
    def __init__(self, wrong_index: int, wrong_letter: str, cause: DifferenceEnum, current: str, previous:str):
        self.wrong_index = wrong_index
        self.wrong_letter = wrong_letter
        self.cause = cause
        self.current = current
        self.previous = previous
