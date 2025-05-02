import typing
import os
from webdav3.client import Client


class WebdavMailRu:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.url = "https://webdav.cloud.mail.ru"
        self.client: typing.Optional[Client] = None

    def connect(self):
        data = {
            'webdav_hostname': self.url,
            'webdav_login': self.username,
            'webdav_password': self.password
        }
        self.client = Client(data)
        self.client.list()

    def upload_file(self, remote_file: str, local_path: str):
        self.client.upload_file(remote_file, local_path)