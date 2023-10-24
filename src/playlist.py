import datetime
import os
import isodate
from googleapiclient.discovery import build


class PlayList:

    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.__total_duration = datetime.timedelta()
        self.__best_video_url = ''
        playlist_videos = PlayList.youtube.playlists().list(id=self.__playlist_id,
                                                            part='snippet',
                                                            maxResults=50,
                                                            ).execute()
        self.title = playlist_videos['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'
        self.popular_video()

    @property
    def total_duration(self):
        """
        Длительность плейлиста
        """
        return self.__total_duration

    def show_best_video(self):
        """
        Самое популярное видео
        """
        return self.__best_video_url

    def popular_video(self):
        """
        Инфа по видео в плейлисте
        """
        like_count = 0
        most_likes = 0
        url = ''
        playlist_videos = PlayList.youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                                part='contentDetails',
                                                                maxResults=50,
                                                                ).execute()
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = PlayList.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=video_ids
                                                        ).execute()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            self.__total_duration += isodate.parse_duration(iso_8601_duration)
            like_count = int(video['statistics']['likeCount'])
            if like_count > most_likes:
                videoid = video['id']
                url = f'https://youtu.be/{videoid}'
                most_likes = like_count
            self.__best_video_url = url
