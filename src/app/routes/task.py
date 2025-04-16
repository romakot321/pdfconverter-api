from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile, HTTPException
from fastapi.responses import Response

from app.schemas.task import TaskCreateSchema, TaskSchema, TaskShortSchema
from app.services.task import TaskService

from . import validate_api_token

router = APIRouter(prefix="/api/task", tags=["Task"])


@router.post("", response_model=TaskShortSchema, dependencies=[Depends(validate_api_token)])
async def create_task(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(),
    schema: TaskCreateSchema = Depends(),
    service: TaskService = Depends(),
):
    task = await service.create(schema)
    background_tasks.add_task(service.send, task.id, await file.read(), schema)
    return task


@router.get("/{task_id}", response_model=TaskSchema, dependencies=[Depends(validate_api_token)])
async def get_task(task_id: UUID, service: TaskService = Depends()):
    return await service.get(task_id)


@router.get("/{task_id}/file", response_class=Response)
def get_task_file(task_id: UUID, service: TaskService = Depends()):
    body = service.get_file(str(task_id))
    if body is None:
        raise HTTPException(404)
    return Response(content=body, media_type="application/octet-stream")
