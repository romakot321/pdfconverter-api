from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.schemas import BaseSearchSchema


class TaskFileConvertTo(Enum):
    pdf = 'pdf'
    docx = 'docx'
    doc = 'doc'


class TaskSchema(BaseModel):
    class TaskItem(BaseModel):
        id: int
        filename: str

        model_config = ConfigDict(from_attributes=True)

    id: UUID
    error: str | None = None
    items: list[TaskItem]

    model_config = ConfigDict(from_attributes=True)


class TaskShortSchema(BaseModel):
    id: UUID
    error: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TaskCreateSchema(BaseModel):
    convert_to: TaskFileConvertTo
    password: str | None = None
    app_bundle: str
    user_id: str
