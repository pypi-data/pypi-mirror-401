"""User-related DTOs and protocols."""

from pydantic import BaseModel


class UserDTO(BaseModel):
    """User DTO used across API/service/persistence layers."""

    user_name: str
    password: str | None = None
    roles: list[str]
    real_name: str
    division: str
    description: str
    policy_epoch: int
    created_at: str | None = None
    updated_at: str | None = None

    def __str__(self) -> str:
        return f"#<User {self.user_name}: roles={self.roles}>"

    def __repr__(self) -> str:
        return self.__str__()


class UserDTOForCreate(BaseModel):
    """Input DTO for creating a user."""

    user_name: str
    password: str
    roles: list[str]
    real_name: str = ""
    division: str = ""
    description: str = ""
    policy_epoch: int = 1

    def __str__(self) -> str:
        return f"#<UserCreate {self.user_name}: roles={self.roles}>"

    def __repr__(self) -> str:
        return self.__str__()


class UserDTOForUpdate(BaseModel):
    """Input DTO for updating a user (partial fields)."""

    user_name: str
    password: str | None = None
    roles: list[str] | None = None
    real_name: str | None = None
    division: str | None = None
    description: str | None = None

    def __str__(self) -> str:
        return f"#<UserUpdate {self.user_name}: roles={self.roles}>"

    def __repr__(self) -> str:
        return self.__str__()
