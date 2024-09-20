from dataclasses import dataclass


@dataclass
class Association:
    id: int
    name: str
    isCommon: bool