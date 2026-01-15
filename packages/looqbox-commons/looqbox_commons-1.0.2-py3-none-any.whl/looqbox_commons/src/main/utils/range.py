from dataclasses import dataclass


@dataclass
class Range:
    """
    It's basically the native range but with some cool builtins!!!
    """
    start: float
    end: float

    def is_value_within(self, value: float) -> bool:
        answer = False
        if self.start <= value < self.end:
            answer = True
        return answer

    def intersects(self, other: "Range") -> bool:
        return self.is_value_within(other.start) or self.is_value_within(other.end)
