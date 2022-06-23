
from pydantic import BaseModel
from typing import Union, List, Optional
from fastapi import FastAPI, File, UploadFile, Form

from process_service.compression.utils import fetch_url, resize

app = FastAPI()


class ImageURLs(BaseModel):
    urls: list[str] = []


@app.post("/compress/files/")
async def compress_file(
    size_ratio=0.9,
    quality=90, width=200, height=200,
    files: Optional[List[UploadFile]] = File(None),
):
    res = []
    for file in files:
        filename, ext = file.filename.split(".")
        file = file.file
        file_path = resize(file, filename, ext, size_ratio=size_ratio,
                           quality=quality, width=width, height=height)
        res.append(file_path)
    return {'message': 'Success', 'data': res}


@ app.post("/compress/urls/")
async def compress_url(
    urls: Union[ImageURLs, None] = [],
    size_ratio=0.9, quality=10, width=200, height=200
):
    res = []
    for url in urls.urls:
        file, filename, ext = fetch_url(url)
        if file:
            file_path = resize(file, filename, ext, file_type="urls",
                               size_ratio=size_ratio, quality=quality,
                               width=width, height=height)
            res.append(file_path)
    return {'message': 'Success', 'data': res}
