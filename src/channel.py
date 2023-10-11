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
        """Возвращает id канала"""
        return self.__channel_id

    @property
    def title(self):
        """Возвращает название канала"""
        title = self.print_info()['items'][0]['snippet']['title']
        return title

    @property
    def description(self):
        """Возвращает описание канала"""
        description = self.print_info()['items'][0]['snippet']['description']
        return description

    @property
    def url(self):
        """Возвращает ссылку на канал"""
        id_channel = self.print_info()['items'][0]['id']
        url = f'https://www.youtube.com/channel/{id_channel}'
        return url

    @property
    def subscriber_count(self):
        """Возвращает количество подписчиков"""
        subscribers = self.print_info()['items'][0]['statistics']['subscriberCount']
        return subscribers

    @property
    def video_count(self):
        """Возвращает количество видео"""
        video_count = self.print_info()['items'][0]['statistics']['videoCount']
        return video_count

    @property
    def view_count(self):
        """Возвращает общее количество просмотров"""
        view_count = self.print_info()['items'][0]['statistics']['viewCount']
        return view_count

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        get_service = build('youtube', 'v3', developerKey=cls.__api_key)
        return get_service

    def to_json(self, path):
        """Сохраняет в файл значения атрибутов экземпляра"""
        channel = self.print_info()
        channel_string = json.dumps(channel)
        with open(path, "w", encoding='UTF=8') as file:
            file.write(channel_string)

    def __str__(self):
        """
        Отображает информацию об объекте класса
        """
        return f'{self.title} ({self.url}'

    def __add__(self, other):
        """
        Прибавляет к экземпляру класса объект произвольного типа данных
        """
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """
        Метод для операции вычитания
        """
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        """
        Метод для операции сравнения «меньше»
        """
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __le__(self, other):
        """
        Метод для операции сравнения «меньше или равно»
        """
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __gt__(self, other):
        """
        Метод для операции сравнения «больше»
        """
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __ge__(self, other):
        """
        Метод для операции сравнения «больше или равно»
        """
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        """
        Метод для операции сравнения «равно»
        """
        return int(self.subscriber_count) == int(other.subscriber_count)