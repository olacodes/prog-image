import environ
from storage_service.app.tasks import url_format_converter, delete_tmp_dir, upload_file_s3

env = environ.Env()


class URLImageHandler:
    # Download the image
    def __init__(self, urls: list):
        self.urls = urls
    

    def chain_convert_s3_del(self):
        celery_chain = url_format_converter.apply_async(
            (self.urls,), link=upload_file_s3.s(env('AWS_S3_BUCKET')))
        delete_tmp_dir.delay([env('TMP_FILES'), env('TMP_IMG')])
