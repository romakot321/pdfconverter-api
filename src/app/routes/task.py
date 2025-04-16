from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response

from app.schemas.task import TaskCreateSchema, TaskFileConvertTo, TaskSchema, TaskShortSchema
from app.services.task import TaskService

from . import validate_api_token

router = APIRouter(prefix="/api/task", tags=["Task"])


@router.post("", response_model=TaskShortSchema, dependencies=[Depends(validate_api_token)])
async def create_task(
    file: list[UploadFile],
    background_tasks: BackgroundTasks,
    schema: TaskCreateSchema = Depends(),
    service: TaskService = Depends(),
):
    files = [await f.read() for f in file]
    if len(files) > 1 and schema.convert_to != TaskFileConvertTo.pdf:
        raise HTTPException(422, detail="More than 1 file is supported only for convert_to='pdf'")
    if schema.password and schema.convert_to != TaskFileConvertTo.pdf:
        raise HTTPException(422, detail="Password is supported only for convert_to='pdf'")

    task = await service.create(schema)
    background_tasks.add_task(service.send, task.id, files, schema)
    return task


@router.get("/{task_id}", response_model=TaskSchema, dependencies=[Depends(validate_api_token)])
async def get_task(task_id: UUID, service: TaskService = Depends()):
    return await service.get(task_id)


@router.get("/{task_id}/file", response_class=Response)
def get_task_file(task_id: UUID, service: TaskService = Depends()):
    body = service.get_file(str(task_id))
    return Response(content=body, media_type="application/octet-stream")
