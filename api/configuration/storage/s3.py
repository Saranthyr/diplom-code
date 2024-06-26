from dependency_injector.resources import Resource
from sqlalchemy_file.storage import StorageManager
from libcloud.storage.types import Provider
from libcloud.storage.drivers.s3 import S3StorageDriver
from libcloud.storage.base import Container


class S3Storage(Resource):
    def init(self, aws_access_key: str, aws_secret_key: str, host: str, port: int):
        self.access_key = aws_access_key
        self.secret_key = aws_secret_key
        self.host = host
        self.port = port
        self.stor = S3StorageDriver(
            self.access_key, self.secret_key, False, self.host, self.port
        )
        try:
            self.stor.create_container("default")
        except Exception:
            pass
        StorageManager.add_storage("default", self.stor.get_container("default"))
        return None
