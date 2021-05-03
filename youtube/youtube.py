from apiclient.discovery import build

from youtube.errors import (
    NoChannelError,
    NoMovieError,
    NoMovieDetailError,
)


class YoutubeService:
    """
    YoutubeAPIドキュメント
    https://developers.google.com/youtube/v3/docs?hl=ja
    """

    def __init__(self, youtube_api_key):
        self.__youtube = build('youtube', 'v3', developerKey=youtube_api_key)

    def search_channel(self, channel_id: str) -> str:
        """
        チャンネル情報を取得する
        :param channel_id: チャンネルID
        :return: チェンネル
        """
        channels_response = self.__youtube.channels().list(
            part='snippet',
            id=channel_id
        ).execute()

        if channels_response['items'] is None:
            raise NoChannelError(f"Channel Not found. channel_id: {channel_id}")
        return channels_response['items'][0]

    def search_videos(self, channel_id: str, published_after, published_before) -> list:
        """
        チャンネルに投稿されている動画を検索し一覧で返す
        :param published_before: この日時より後に作成された日付に絞り込む
        :param published_after:この日時より前に作成された日付に絞り込む
        :param channel_id: チャンネルID
        :return: 動画情報一覧
        """
        videos_response = self.__youtube.search().list(
            part='snippet',
            channelId=channel_id,
            type='video',
            maxResults=50,
            order='date',
            publishedAfter=published_after,
            publishedBefore=published_before
        ).execute()

        if videos_response['items'] is None:
            raise NoMovieError(f"Video not found. channel_id: {channel_id}")
        return videos_response['items']

    def get_videos_detail(self, video_id: str):
        """
        動画情報を取得する
        :param video_id: 動画ID
        :return: 動画詳細情報
        """
        video_detail_response = self.__youtube.videos().list(
            part=['statistics', 'snippet', 'contentDetails'],
            id=video_id,
        ).execute()
        if video_detail_response['items'] is None:
            raise NoMovieDetailError(f'Video detail not found. video_id: {video_id}')
        return video_detail_response['items'][0]
