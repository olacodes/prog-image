from json import JSONEncoder
import json
from typing import Union, List, Optional, Set
import pickle
import os
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form, Request
from pydantic import BaseModel

from app.handlers import file_upload_handler, repo_img_handler, img_url_handler
from app.tasks import create_task, format_converter, list_files
from s3.s3_service import S3Service
import environ

env = environ.Env()
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', None)
AWS_REGION = env('AWS_REGION', None)
AWS_S3_BUCKET = env('AWS_S3_BUCKET', None)

app = FastAPI()
s3_service = S3Service(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)


class ImageURLs(BaseModel):
    urls: list[str] = []


def get_content_type(request):
    types = {'multipart/form-data;': 'form_data', 'application/json;': 'json'}
    content_type = request.headers['content-type']
    return types[content_type.split(" ")[0]]


@app.post("/image/")
async def upload_file(
        request: Request,
        img_urls: Union[ImageURLs, None] = [],
        files: Optional[List[UploadFile]] = File(None)
):
    mapper = {
        'form_data': {
            'klass': file_upload_handler.FileUploadHandler,
            'data': files
        },
        'json': {
            'klass': img_url_handler.URLImageHandler,
            'data': img_urls
        }
    }
    content_type = mapper[get_content_type(request)]
    handler = content_type['klass'](content_type['data'])
    res = await handler.file_writer()

    # format_converter()
    handler.send_s3()
    # print(Path.cwd())
    files = list_files('tmp/img')
    print(files)

    s3_service.upload_files(files, 'sodiqcodesbucket')
    # return res
    return "hello"
