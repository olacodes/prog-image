from celery import group
from pydantic import BaseModel
from fastapi import APIRouter
from typing import Union, List, Optional
from fastapi import FastAPI, File, UploadFile, Form

from process_service.utils import fetch_url
from process_service.compression.compress import compress
from process_service.response import Response
from process_service.tasks import handle_compress


router = APIRouter(
    prefix="/api/v1/compress",
    tags=["compress"],
    responses={404: {"description": "Not found"}},
)


class ImageURLs(BaseModel):
    urls: list[str] = []


@router.post("/urls/")
async def compress_url(
    urls: Union[ImageURLs, None] = [],
    size_ratio=0.9, quality=10, width=200, height=200
):
    if len(urls.urls) == 0:
        return Response(error=dict(urls="Enter an image url"))
    handler = group(handle_compress.s(url, size_ratio, quality, width, height)
                    for url in urls.urls)()
    response = handler.get()
    return Response(data=dict(compressed_files=response, total=len(response)))


@router.post("/files/")
async def compress_file(
    files: list[UploadFile] = File(None),
    size_ratio=0.9,
    quality=90, width=200, height=200,
):
    response = []
    for file in files:
        filename, ext = file.filename.split(".")
        file = file.file
        file_path = compress(file, filename, ext, size_ratio=size_ratio,
                             quality=quality, width=width, height=height, is_file=True)
        response.append(file_path)
    return Response(data=dict(compressed_files=response, total=len(response)))
