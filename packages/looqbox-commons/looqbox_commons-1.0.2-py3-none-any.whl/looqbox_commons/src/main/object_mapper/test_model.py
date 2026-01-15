from dataclasses import dataclass
from typing import Any


@dataclass
class TestModel:
    input: Any
    expected: Any
