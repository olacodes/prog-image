import os
import environ

from pydantic import BaseModel
from typing import Union, List, Optional, Set
from fastapi import FastAPI, File, UploadFile, Form, Request

from app.handlers import file_upload_handler, repo_img_handler, img_url_handler
from app.tasks import format_converter, url_format_converter, delete_tmp_dir
from s3.s3_service import S3Service
from app.utils import get_content_type, list_files

env = environ.Env()
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', None)
AWS_REGION = env('AWS_REGION', None)
AWS_S3_BUCKET = env('AWS_S3_BUCKET', None)

app = FastAPI()
s3_service = S3Service(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)


class ImageURLs(BaseModel):
    urls: list[str] = []


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
    handler.chain_convert_s3_del()
    return res
