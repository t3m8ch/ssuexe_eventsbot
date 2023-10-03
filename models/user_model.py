from dataclasses import dataclass

from common.types import UserRole


@dataclass
class UserModel:
    id: int
    full_name: str
    user_name: str | None
    role: UserRole
