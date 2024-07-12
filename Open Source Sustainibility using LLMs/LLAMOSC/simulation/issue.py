from dataclasses import dataclass


@dataclass
class Issue:
    id: int
    difficulty: int
    filepath: str
