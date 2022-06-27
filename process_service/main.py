
from pydantic import BaseModel
from typing import Union, List, Optional
from fastapi import FastAPI, File, UploadFile, Form

from process_service.routers import compress, filters, rotation, thumbnail


app = FastAPI()

app.include_router(compress.router)
app.include_router(rotation.router)
app.include_router(filters.router)
app.include_router(thumbnail.router)
