import glob
import logging
import boto3
import botocore
import environ

env = environ.Env()

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', None)
AWS_REGION = env('AWS_REGION', None)
AWS_S3_BUCKET = env('AWS_S3_BUCKET', None)


class S3Service:
    S3 = boto3.resource('s3')

    def __init__(self, aws_access_key_id, aws_secret_access_key, region, *args, **kwargs):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region

    @classmethod
    async def get_file(cls, filename):
        try:
            fdir = filename.split(".")[0]
            KEY = f"{fdir}/{filename}"
            cls.S3.Bucket(env('AWS_S3_BUCKET')).download_file(KEY, filename)
            return f'https://{env("AWS_S3_BUCKET")}.s3.amazonaws.com/{KEY}'
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                # Todo: Log to file
                raise

    @classmethod
    async def get_files(cls, prefix):
        try:
            res = cls.S3.Bucket(f"{AWS_S3_BUCKET}")
            return [f'https://{file.bucket_name}.s3.amazonaws.com/{file.key}'
                    for file in res.objects.filter(Prefix=prefix)]

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return "The object does not exist."
            else:
                # Todo: Log to file
                raise

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
                # Todo: Log to file
                raise
