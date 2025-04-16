from uuid import UUID
from fastapi import Depends, UploadFile

from app.db.tables import TaskItem
from app.repositories.external import ExternalRepository
from app.repositories.storage import StorageRepository
from app.repositories.task import TaskRepository
from app.schemas.exception import APIException
from app.schemas.external import ExternalTaskSchema
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskShortSchema


class TaskService:
    def __init__(
            self,
            task_repository: TaskRepository = Depends(TaskRepository.depend),
            external_repository: ExternalRepository = Depends(),
            storage_repository: StorageRepository = Depends()
    ):
        self.task_repository = task_repository
        self.external_repository = external_repository
        self.storage_repository = storage_repository

    async def create(self, schema: TaskCreateSchema) -> TaskShortSchema:
        model = await self.task_repository.create(app_bundle=schema.app_bundle, user_id=schema.user_id)
        return TaskShortSchema.model_validate(model)

    async def send(self, task_id: UUID, file: bytes, schema: TaskCreateSchema):
        try:
            converted_file_body = await self.external_repository.convert(file, schema.convert_to.value)
        except APIException as e:
            return await self.task_repository.update(task_id, error=str(e))

        self.storage_repository.store(str(task_id), converted_file_body)

        return await self.task_repository.create_items(TaskItem(task_id=task_id, filename=str(task_id)))

    async def get(self, task_id: UUID) -> TaskSchema:
        model = await self.task_repository.get(task_id)
        return TaskSchema.model_validate(model)

    def get_file(self, filename: str) -> bytes | None:
        return self.storage_repository.get(filename)
