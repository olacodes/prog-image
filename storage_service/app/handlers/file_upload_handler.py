import shutil
import environ

from typing import List
from fastapi import File

from storage_service.app.utils import list_files
from storage_service.app.tasks import format_converter, delete_tmp_dir, upload_file_s3

env = environ.Env()


class FileUploadHandler:
    def __init__(self, files: List[File]):
        self.files = files

    # I/O bound operation: writing to tmp file
    def file_writer(self):
        file_written = []
        for file in self.files:
            file_location = f"tmp/files/{file.filename}"
            with open(file_location, "wb") as fd:
                shutil.copyfileobj(file.file, fd)
                file_written.append(file.filename)
        return {"response": f"Saved and uploaded {file_written} file(s)"}

    def chain_convert_s3_del(self):
        celery_chain = format_converter.apply_async(
            (), link=upload_file_s3.s(env('AWS_S3_BUCKET')))
        # delete_tmp_dir.delay([env('TMP_FILES'), env('TMP_IMG')])

    # def convert(self):
    #     format_converter.delay()

    # def s3_upload(self):
    #     upload_file_s3.delay(
    #         list_files(env('TMP_IMG')),
    #         env('AWS_S3_BUCKET')
    #     )

    # def delete_tmp(self):
    #     delete_tmp_dir.delay([env('TMP_FILES'), env('TMP_IMG')])
