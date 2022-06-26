from pydantic import BaseModel
from typing import Union, List, Optional
from fastapi import FastAPI, File, UploadFile, Form, APIRouter

from process_service.utils import fetch_url
from process_service.rotation.rotate import rotate


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
    res = []
    for url in urls.urls:
        file, filename, ext = fetch_url(url)
        if file:
            file_path = rotate(file, filename, ext, angle, expand)
        res.append(file_path)

    return {'message': 'Success', 'data': res}


@router.post("/files/")
async def rotate_files(
    files: list[UploadFile] = File(None),
    angle: int = 90, expand: bool = True
):
    res = []
    for file in files:
        filename, ext = file.filename.split(".")
        file = file.file
        file_path = rotate(file, filename, ext, angle=90, expand=True, is_file=True)
        res.append(file_path)
    return {'message': 'Success', 'data': res}
