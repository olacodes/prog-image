from celery import group
from pydantic import BaseModel
from typing import Union, List, Optional
from fastapi import FastAPI, File, UploadFile, Form, APIRouter

from process_service.response import Response
from process_service.tasks import handle_filter
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
    if len(urls.urls) == 0:
        return Response(error=dict(urls="Enter an image url"))
    handler = group(handle_filter.s(url, method) for url in urls.urls)()
    response = handler.get()
    return Response(data=dict(filtered_files=response, total=len(response)))


@router.post("/files/")
async def filter_files(
    files: list[UploadFile] = File(None), method: str = 'blur'
):
    response = []
    for file in files:
        filename, ext = file.filename.split(".")
        file = file.file
        file_path = filter(file, filename, ext, method=method, is_file=True)
        response.append(file_path)
    return Response(data=dict(filtered_files=response, total=len(response)))

