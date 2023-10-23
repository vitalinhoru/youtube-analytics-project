import os
from googleapiclient.discovery import build


class Video:
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        """
        Создает объект по id видео
        """
        self.video_id = video_id
        video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                     id=video_id
                                                     ).execute()
        self.title = video_response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v={video_id}'
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        """
        Получает id плейлиста и создает из него объект по id видео
        """
        playlist_videos = Video.youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        for video in playlist_videos['items']:
            if video['contentDetails']['videoId'] == video_id:
                super().__init__(video_id)
