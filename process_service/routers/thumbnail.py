from celery import group
from pydantic import BaseModel
from typing import Union, List, Optional
from fastapi import FastAPI, File, UploadFile, Form, APIRouter

from process_service.utils import fetch_url
from process_service.response import Response
from process_service.tasks import handle_thumbnail
from process_service.thumbnail.thumbnail import thumbnail


router = APIRouter(
    prefix="/api/v1/thumbnail",
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
    if len(urls.urls) == 0:
        return Response(error=dict(urls="Enter an image url"))
    handler = group(handle_thumbnail.s(url, width, height)
                    for url in urls.urls)()
    response = handler.get()
    return Response(data=dict(thumbnail_files=response, total=len(response)))


@router.post("/files/")
async def thumbnail_files(
    files: list[UploadFile] = File(None),
    width: int = 200, height: int = 200
):
    response = []
    for file in files:
        filename, ext = file.filename.split(".")
        file = file.file
        file_path = thumbnail(file, filename, ext, width=width,
                              height=height, is_file=True)
        response.append(file_path)
    return Response(data=dict(thumbnail_files=response, total=len(response)))
