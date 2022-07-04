from typing import List, Union

import environ
from fastapi import FastAPI, File, UploadFile, status
from pydantic import BaseModel

from storage_service.app.handlers import file_upload_handler, img_url_handler
from storage_service.response import Response
from storage_service.s3.s3_service import S3Service

env = environ.Env()
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default=None)
AWS_REGION = env('AWS_REGION', default=None)
AWS_S3_BUCKET = env('AWS_S3_BUCKET', default=None)

app = FastAPI()
s3_service = S3Service()


# The upload file [multipart/form] and urls [application/json]
# can not be together
env = environ.Env()


class ImageURLs(BaseModel):
    urls: list[str] = []


@app.post("/api/v1/images/")
async def upload_image(files: List[UploadFile] = File(None)):
    handler = file_upload_handler.FileUploadHandler(files)
    response = await handler.handle()
    if not response:
        return Response(errors=dict(errors=response),
                        status_code=status.HTTP_400_BAD_REQUEST)

    if error := response.get('error', None):
        return Response(errors=dict(errors=error),
                        status_code=status.HTTP_400_BAD_REQUEST)

    return Response(data=response)


@app.post("/api/v1/images/urls/")
async def upload_url(
    img_urls: Union[ImageURLs, None] = [],
):
    handler = img_url_handler.URLImageHandler(img_urls.urls)
    response = await handler.handle()
    if not response:
        return Response(errors=dict(errors=response),
                        status_code=status.HTTP_400_BAD_REQUEST)
    if error := response.get('error', None):
        return Response(errors=dict(errors=error),
                        status_code=status.HTTP_400_BAD_REQUEST)
    return Response(data=response)


@app.get("/api/v1/images/{id}/")
async def get_image(id):
    response = await s3_service.get_file(id)
    if not response:
        return Response(errors=dict(errors=response),
                        status_code=status.HTTP_404_NOT_FOUND)
    if error := response.get('error', None):
        return Response(errors=dict(errors=error),
                        status_code=status.HTTP_400_BAD_REQUEST)
    return Response(dict(url=response.get('url')))


@app.get("/api/v1/images/file/{id}/")
async def get_multiple_image_format(id):
    response = await s3_service.get_files(id)
    if not response:
        return Response(errors=dict(errors=response),
                        status_code=status.HTTP_404_NOT_FOUND)
    if error := response.get('error', None):
        return Response(errors=dict(errors=error),
                        status_code=status.HTTP_400_BAD_REQUEST)
    urls = response.get('urls', None)
    return Response(data=dict(urls=urls, total=len(urls)))


@app.get("/api/v1/images/")
async def get_all_image():
    response = await s3_service.get_all()
    if not response:
        return Response(errors=dict(errors=response),
                        status_code=status.HTTP_404_NOT_FOUND)
    if error := response.get('error', None):
        return Response(errors=dict(errors=error),
                        status_code=status.HTTP_400_BAD_REQUEST)
    urls = response.get('urls', None)
    return Response(data=dict(urls=urls, total=len(urls)))
