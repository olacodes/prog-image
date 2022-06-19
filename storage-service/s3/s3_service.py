# import aiobotocore
from app.tasks import upload_file_celery
import logging
import glob
# from aiobotocore.session import get_session
import boto3
logger = logging.getLogger(__name__)

'''
For Asynchronous Events
'''


class S3Service:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region, *args, **kwargs):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region

    def upload_files(self, file_paths, bucket):
        # session = get_session()
        # async with session.create_client('s3', region_name=self.region,
        #                                  aws_secret_access_key=self.aws_secret_access_key,
        #                                  aws_access_key_id=self.aws_access_key_id) as client:
        # await client.list_objects
        # s3 = boto3.resource('s3')
        upload_file_celery.delay(file_paths, bucket)
        # for file_path in file_paths:
        #     print('================== something ================ blocking')
        #     file_upload_response =  s3.meta.client.upload_file(file_path, bucket, Key=file_path)

        # if file_upload_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        #     logger.info(
        #         f"File uploaded path : https://{bucket}.s3.{self.region}.amazonaws.com/{key}")
        #     return True
        # return False
