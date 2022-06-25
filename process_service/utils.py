import re
import requests


def fetch_url(url):
    print('This function is called')
    try:
        fname = url.split("/")[-1]
        fname, ext = fname.split(".")[0], fname.split(".")[-1]
        filename = re.sub('[^A-Za-z0-9]+', '', fname)
        res = requests.get(url, stream=True)
        file = res.content
        return file, filename, ext
    except Exception as e:
        filename, file, ext = None
        return file, filename, ext
