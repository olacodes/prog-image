
from pydantic import BaseModel
from typing import Union, List, Optional
from fastapi import FastAPI, File, UploadFile, Form

from process_service.utils import fetch_url

from process_service.rotation.rotate import rotate
from process_service.filtering.filter import filter
from process_service.thumbnail.thumbnail import thumbnail
from process_service.masking.mask import mask

from process_service.routers import compress, filters, rotation, thumbnail


app = FastAPI()

app.include_router(compress.router)
app.include_router(rotation.router)
app.include_router(filters.router)
app.include_router(thumbnail.router)


class ImageURLs(BaseModel):
    urls: list[str] = []


@app.post("/mask/urls")
async def mask_url(
    urls: Union[ImageURLs, None] = [],
):
    res = []
    for url in urls.urls:
        file, filename, ext = fetch_url(url)
        if file:
            file_path = mask(file, filename, ext)
        res.append(file_path)

    return {'message': 'Success', 'data': res}
