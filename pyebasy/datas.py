from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class StorageElement:
    path: Path
    date_of_creation: datetime

@dataclass(frozen=True)
class File(StorageElement):
    size: int
    date_of_last_modification: datetime

@dataclass(frozen=True)
class Directory(StorageElement):
    pass
