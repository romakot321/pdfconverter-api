from io import BytesIO
import os
from aiohttp import ClientSession

from app.schemas.exception import APIException


class ExternalRepository:
    EXTERNAL_API_URL = "http://pdfconverterapi_converter"
    EXTERNAL_API_TOKEN = os.getenv("EXTERNAL_API_TOKEN")

    async def convert(self, file: bytes, convert_to: str) -> bytes:
        async with ClientSession(
            base_url=self.EXTERNAL_API_URL,
        ) as session:
            resp = await session.post("/convert?convert_to=" + convert_to, data={"file": BytesIO(file)})
            if resp.status != 200:
                raise APIException(await resp.text())
            return await resp.read()
