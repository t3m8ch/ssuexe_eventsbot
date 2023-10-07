from dataclasses import dataclass
from typing import Literal


@dataclass
class MediaItemModel:
    file_id: str
    media_type: Literal['video', 'photo']
