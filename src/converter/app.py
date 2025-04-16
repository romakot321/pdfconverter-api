from fastapi import FastAPI, File, HTTPException, UploadFile, Query
from fastapi.responses import Response
from converter.convert import run_server, convert_file


def lifespan(app: FastAPI):
    # run_server()
    yield


fastapi_app = FastAPI()


@fastapi_app.post("/convert")
def convert(file: UploadFile = File(), convert_to: str = Query()):
    result = convert_file(file.file.read(), convert_to)
    if result is None:
        raise HTTPException(500, detail="Error occured on file converting")
    return Response(content=result, media_type="application/octet-stream")
