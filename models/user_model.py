from dataclasses import dataclass
from typing import Literal


@dataclass
class UserModel:
    id: int
    full_name: str
    user_name: str | None
    role: Literal['USER', 'ADMIN']
