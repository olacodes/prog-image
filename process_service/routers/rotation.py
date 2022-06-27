from celery import group
from pydantic import BaseModel
from typing import Union, List, Optional
from fastapi import FastAPI, File, UploadFile, Form, APIRouter

from process_service.utils import fetch_url
from process_service.response import Response
from process_service.rotation.rotate import rotate
from process_service.tasks import handle_rotate

router = APIRouter(
    prefix="/api/v1/rotate",
    tags=["rotation"],
    responses={404: {"description": "Not found"}},
)


class ImageURLs(BaseModel):
    urls: list[str] = []


@router.post("/urls/")
async def rotate_url(
    urls: Union[ImageURLs, None] = [],
    angle: int = 90, expand: bool = True
):
    if len(urls.urls) == 0:
        return Response(error=dict(urls="Enter an image url"))
    handler = group(handle_rotate.s(url, angle, expand) for url in urls.urls)()
    response = handler.get()
    return Response(data=dict(rotated_files=response, total=len(response)))


@router.post("/files/")
async def rotate_files(
    files: list[UploadFile] = File(None),
    angle: int = 90, expand: bool = True
):
    response = []
    for file in files:
        filename, ext = file.filename.split(".")
        file = file.file
        file_path = rotate(file, filename, ext, angle=90,
                           expand=True, is_file=True)
        response.append(file_path)
    return Response(data=dict(rotated_files=response, total=len(response)))
