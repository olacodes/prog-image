
from pydantic import BaseModel
from typing import Union, List, Optional
from fastapi import FastAPI, File, UploadFile, Form, APIRouter

from process_service.utils import fetch_url
from process_service.thumbnail.thumbnail import thumbnail


router = APIRouter(
    prefix="/thumbnail",
    tags=["thumbnail"],
    responses={404: {"description": "Not found"}},
)


class ImageURLs(BaseModel):
    urls: list[str] = []


@router.post("/urls/")
async def thumbnail_url(
    urls: Union[ImageURLs, None] = [],
    width: int = 200, height: int = 200
):
    res = []
    for url in urls.urls:
        file, filename, ext = fetch_url(url)
        if file:
            file_path = thumbnail(file, filename, ext, width, height)
        res.append(file_path)

    return {'message': 'Success', 'data': res}
