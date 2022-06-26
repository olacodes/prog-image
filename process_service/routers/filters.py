from pydantic import BaseModel
from typing import Union, List, Optional
from fastapi import FastAPI, File, UploadFile, Form, APIRouter

from process_service.utils import fetch_url
from process_service.filtering.filter import filter

router = APIRouter(
    prefix="/api/v1/filters",
    tags=["filters"],
    responses={404: {"description": "Not found"}},
)


class ImageURLs(BaseModel):
    urls: list[str] = []


@router.post("/urls/", tags=["filters"])
async def filter_urls(urls: Union[ImageURLs, None] = [], method: str = 'blur'):
    res = []
    for url in urls.urls:
        file, filename, ext = fetch_url(url)
        if file:
            file_path = filter(file, filename, ext, method)
        res.append(file_path)

    return {'message': 'Success', 'data': res}


@router.post("/files/")
async def filter_files(
    files: list[UploadFile] = File(None), method: str = 'blur'
):
    res = []
    for file in files:
        filename, ext = file.filename.split(".")
        file = file.file
        file_path = filter(file, filename, ext, method=method, is_file=True)
        res.append(file_path)
    return {'message': 'Success', 'data': res}
