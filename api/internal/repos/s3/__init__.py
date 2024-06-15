from typing import Union
from io import BytesIO

from botocore.exceptions import ClientError


class S3:
    def __init__(self, s3_session, s3_uri: str):
        self.s3_session = s3_session
        self.s3_uri = s3_uri

    async def get_file(self, filename: str, bucket: str) -> Union[BytesIO, int]:
        async with self.s3_session.client("s3", endpoint_url=self.s3_uri) as cl:
            contents = BytesIO()
            try:
                await cl.download_fileobj(bucket, filename, contents)
                return contents
            except ClientError:
                return -1

    async def upload_file(self, file: bytes, key: str, bucket: str) -> str | int:
        async with self.s3_session.client("s3", endpoint_url=self.s3_uri) as cl:
            await cl.put_object(Bucket=bucket, Key=key, Body=file)
            try:
                res = await cl.head_object(Bucket=bucket, Key=key)
                res = res["ETag"][1:-1]
                return res
            except ClientError:
                return -1

    async def delete_file(self, key: str, bucket: str) -> int:
        async with self.s3_session.client("s3", endpoint_url=self.s3_uri) as cl:
            await cl.delete_object(Bucket=bucket, Key=key)
            try:
                await cl.head_object(Bucket=bucket, Key=key)
                return -1
            except ClientError:
                return 0

    async def get_file_md5(self, key: str, bucket: str) -> str | int:
        async with self.s3_session.client("s3", endpoint_url=self.s3_uri) as cl:
            try:
                res = await cl.head_object(Bucket=bucket, Key=key)
                res = res["ETag"][1:-1]
                return res
            except Exception:
                return -1
