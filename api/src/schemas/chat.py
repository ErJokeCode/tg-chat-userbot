from pydantic import BaseModel


class AddChatDTO(BaseModel):
    name: str
    users: list[str | int] | None = None
