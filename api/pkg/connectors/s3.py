from dependency_injector.resources import Resource
import aioboto3


class S3Connector(Resource):
    def init(self, aws_access_key_id: str, aws_secret_access_key: str):
        return aioboto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
