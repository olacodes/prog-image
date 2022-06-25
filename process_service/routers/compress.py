from pydantic import BaseModel
from fastapi import APIRouter
from typing import Union, List, Optional
from fastapi import FastAPI, File, UploadFile, Form

from process_service.utils import fetch_url
from process_service.compression.compress import compress

router = APIRouter(
    prefix="/compress",
    tags=["compress"],
    responses={404: {"description": "Not found"}},
)


class ImageURLs(BaseModel):
    urls: list[str] = []


@router.post("/files/")
async def compress_file(
    files: list[UploadFile] = File(None),
    size_ratio=0.9,
    quality=90, width=200, height=200,
):
    res = []
    for file in files:
        filename, ext = file.filename.split(".")
        file = file.file
        file_path = compress(file, filename, ext, size_ratio=size_ratio,
                             quality=quality, width=width, height=height, is_file=True)
        res.append(file_path)
    return {'message': 'Success', 'data': res}


@router.post("/urls/")
async def compress_url(
    urls: Union[ImageURLs, None] = [],
    size_ratio=0.9, quality=10, width=200, height=200
):
    res = []
    for url in urls.urls:
        file, filename, ext = fetch_url(url)
        if file:
            file_path = compress(file, filename, ext, size_ratio=size_ratio,
                                 quality=quality, width=width, height=height)
            res.append(file_path)
    return {'message': 'Success', 'data': res}
