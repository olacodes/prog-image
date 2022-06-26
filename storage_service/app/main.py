import os
import environ

from pydantic import BaseModel
from typing import Union, List, Optional, Set
from fastapi import FastAPI, File, UploadFile, Form, Request, Body

from storage_service.app.handlers import file_upload_handler, repo_img_handler, img_url_handler
from storage_service.app.tasks import format_converter, url_format_converter, delete_tmp_dir
from storage_service.s3.s3_service import S3Service
from storage_service.app.utils import get_content_type, list_files

env = environ.Env()
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default=None)
AWS_REGION = env('AWS_REGION', default=None)
AWS_S3_BUCKET = env('AWS_S3_BUCKET', default=None)

app = FastAPI()
s3_service = S3Service(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)


# The upload file [multipart/form] and urls [application/json] can not be together
# If their is frontend we could implement a web socket that talk wait until all files are processed

class ImageURLs(BaseModel):
    urls: list[str] = []


@app.post("/api/v1/images/")
def upload_image(files: List[UploadFile] = File(None)):
    print("This is called")
    print(files)
    handler = file_upload_handler.FileUploadHandler(files)
    writer_response = handler.file_writer()
    handler.chain_convert_s3_del()
    return writer_response


@app.post("/api/v1/images/urls/")
async def upload_url(
    img_urls: Union[ImageURLs, None] = [],
):
    handler = img_url_handler.URLImageHandler(img_urls.urls)
    handler.chain_convert_s3_del()
    return img_urls


@app.get("/api/v1/images/{image_name}/")
async def get_image(image_name):
    res = await s3_service.get_file(image_name)
    return {"image_name": image_name}


@app.get("/api/v1/images/file/{prefix}")
async def get_image(prefix):
    res = await s3_service.get_files(prefix)
    return {"image_name": res}


@app.get("/api/v1/images/")
async def get_image():
    res = await s3_service.get_all()
    return {"image_name": res}
