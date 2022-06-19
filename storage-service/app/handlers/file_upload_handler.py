from typing import List
from fastapi import FastAPI, File, UploadFile
from app.tasks import format_converter
import json
import pickle
import shutil


class FileUploadHandler:
    # Pass the data object into this class
    def __init__(self, files: List[File]):
        self.files = files

    # I/O bound operation: writing to tmp file
    async def file_writer(self):
        counter = 0
        for file in self.files:
            file_location = f"tmp/files/{file.filename}"
            with open(file_location, "wb") as fd:
                shutil.copyfileobj(file.file, fd)
                counter += 1
        return {"result": f"write {counter} file in temp/files"}

    def send_s3(self):
        format_converter.delay()
