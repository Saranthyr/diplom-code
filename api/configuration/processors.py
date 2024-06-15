from sqlalchemy_file import File
from sqlalchemy_file.processors import Processor


class UrlProcessor(Processor):
    def __init__(self) -> None:
        super().__init__()

    def process(self, file: "File", upload_storage: str | None = None) -> None:
        file.update({"url": f'localhost:8333/{file["path"]}'})
