import boto3
import botocore
import environ
from botocore.exceptions import ClientError

from storage_service.logger import Logger

env = environ.Env()
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default=None)
AWS_REGION = env('AWS_REGION', default=None)
AWS_S3_BUCKET = env('AWS_S3_BUCKET', default=None)
AWS_S3_STORAGE_KEY = env('AWS_S3_STORAGE_KEY', default='storage_service')
AWS_S3_BASE_URL = env(
    'AWS_S3_BASE_URL', default='https://sodiqcodesbucket.s3.amazonaws.com')
logger = Logger(__name__)


class S3Service:
    S3 = boto3.resource('s3')
    log = logger.log()

    @classmethod
    async def get_file(cls, filename):
        try:
            KEY = f"{AWS_S3_STORAGE_KEY}/{filename}"
            cls.S3.Bucket(env('AWS_S3_BUCKET')).download_file(KEY, filename)
            return {'url': f'https://{env("AWS_S3_BUCKET")}.s3.amazonaws.com/{KEY}'}
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                cls.log.error(e)
                return {"error": "The object does not exist."}
            else:
                cls.log.error(e)

    @classmethod
    async def get_files(cls, prefix):
        try:
            res = cls.S3.Bucket(f"{AWS_S3_BUCKET}")
            print(prefix)
            urls = [f'https://{file.bucket_name}.s3.amazonaws.com/{file.key}'
                    for file in res.objects.filter(Prefix=f"{AWS_S3_STORAGE_KEY}/{prefix}")]
            return {'urls': urls}

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                cls.log.error(e)
                return {"error": "The object does not exist."}
            else:
                cls.log.error(e)
                return {"error": str(e)}

    @classmethod
    async def get_all(cls):
        try:
            res = cls.S3.Bucket(f"{AWS_S3_BUCKET}")
            urls = [f'https://{file.bucket_name}.s3.amazonaws.com/{file.key}'
                    for file in res.objects.all()]
            return {'urls': urls}
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                cls.log.error(e)
                return{"error": "The object does not exist."}
            else:
                cls.log.error(e)
                return{"error": str(e)}

    @classmethod
    def upload_file_s3(cls, filepath):
        try:
            filename = filepath.split('/')[-1]
            key = f'{AWS_S3_STORAGE_KEY}/{filename}'
            cls.S3.meta.client.upload_file(
                filepath, AWS_S3_BUCKET, Key=key)
            return f"{AWS_S3_BASE_URL}/{key}"
        except ClientError as e:
            cls.log.error(e)
