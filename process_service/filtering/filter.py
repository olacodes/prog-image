import environ
from io import BytesIO
from PIL import Image,  ImageFilter

env = environ.Env()
FILTERED_FILES = env('FILTERED_FILES')

def filter(file, filename, ext, method='blur', is_file=False):
    filt = filt_obj.get(method, None)
    Filter = getattr(ImageFilter, filt)

    try:
        img = Image.open(file) if is_file else Image.open(BytesIO(file))
        img = img.filter(Filter)
        filename = f'{filename}_filtered.{ext}'
        img.save(f'{FILTERED_FILES}/{filename}')
        return filename
    except OSError as e:
        print("Cannot filter this file", filename)
        print(e)


filt_obj = {
    "blur": "BLUR",
    "contour": "CONTOUR",
    "detail": "DETAIL",
    "edge_enhance": "EDGE_ENHANCE",
    "emboss": "EMBOSS",
    "find_edges": "FIND_EDGES",
    "sharpen": "SHARPEN",
    "smooth": "SMOOTH",
}
