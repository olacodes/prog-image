from config.celery_app import app

from process_service.utils import fetch_url
from process_service.rotation.rotate import rotate
from process_service.filtering.filter import filter
from process_service.compression.compress import compress
from process_service.thumbnail.thumbnail import thumbnail


@app.task(name='handle_compress')
def handle_compress(url, size_ratio, quality, width, height):
    file, filename, ext = fetch_url(url)
    if file:
        return compress(
            file, filename, ext, size_ratio=size_ratio,
            quality=quality, width=width, height=height)
    return "Error"


@app.task(name='handle_filter')
def handle_filter(url, method):
    file, filename, ext = fetch_url(url)
    if file:
        return filter(file, filename, ext, method)
    return "Error"


@app.task(name='handle_rotate')
def handle_rotate(url, angle, expand):
    file, filename, ext = fetch_url(url)
    if file:
        return rotate(file, filename, ext, angle, expand)
    return "Error"


@app.task(name='handle_thumbnail')
def handle_thumbnail(url, width, height):
    file, filename, ext = fetch_url(url)
    if file:
        return thumbnail(file, filename, ext, width, height)
    return "Error"
