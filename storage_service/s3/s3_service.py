import boto3
import botocore
import environ

from storage_service.logger import Logger

env = environ.Env()
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default=None)
AWS_REGION = env('AWS_REGION', default=None)
AWS_S3_BUCKET = env('AWS_S3_BUCKET', default=None)
AWS_S3_STORAGE_KEY = env('AWS_S3_STORAGE_KEY', default='storage_service/')

logger = Logger(__name__)


class S3Service:
    S3 = boto3.resource('s3')
    log = logger.log()

    def __init__(self, aws_access_key_id, aws_secret_access_key, region, *args, **kwargs):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region

    @classmethod
    async def get_file(cls, filename):
        try:
            KEY = f"{AWS_S3_STORAGE_KEY}/{filename}"
            cls.S3.Bucket(env('AWS_S3_BUCKET')).download_file(KEY, filename)
            return f'https://{env("AWS_S3_BUCKET")}.s3.amazonaws.com/{KEY}'
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
            return [f'https://{file.bucket_name}.s3.amazonaws.com/{file.key}'
                    for file in res.objects.filter(Prefix=f"{AWS_S3_STORAGE_KEY}/{prefix}")]

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                cls.log.error(e)
                return {"error": "The object does not exist."}
            else:
                cls.log.error(e)

    @classmethod
    async def get_all(cls):
        try:
            res = cls.S3.Bucket(f"{AWS_S3_BUCKET}")
            return [f'https://{file.bucket_name}.s3.amazonaws.com/{file.key}'
                    for file in res.objects.all()]
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return "The object does not exist."
            else:
                cls.log.error(e)
