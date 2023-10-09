import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб - канала"""
    __api_key = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=Channel.__api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.print_info()['items'][0]['snippet']['title']

    @property
    def description(self):
        return self.print_info()['items'][0]['snippet']['description']

    @property
    def url(self):
        id_channel = self.print_info()['items'][0]['id']
        url = f'https://www.youtube.com/channel/{id_channel}'
        return url

    @property
    def subscriber_count(self):
        subscribers = self.print_info()['items'][0]['statistics']['subscriberCount']
        return subscribers

    @property
    def video_count(self):
        video_count = self.print_info()['items'][0]['statistics']['videoCount']
        return video_count

    @property
    def view_count(self):
        view_count = self.print_info()['items'][0]['statistics']['viewCount']
        return view_count

    @classmethod
    def get_service(cls):
        get_service = build('youtube', 'v3', developerKey=cls.__api_key)
        return get_service

    def to_json(self, path):
        channel = self.print_info()
        channel_string = json.dumps(channel)
        with open(path, "w", encoding='UTF=8') as file:
            file.write(channel_string)
