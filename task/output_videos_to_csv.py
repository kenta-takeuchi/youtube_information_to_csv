import configparser
import csv
import datetime
import os
from pathlib import Path

from .utils import (
    iso_to_jstdt,
    get_search_date_range
)
from youtube import YoutubeService

BASE_DIR = Path(__file__).resolve().parent.parent

config_ini = configparser.ConfigParser()
config_ini_path = os.path.join(BASE_DIR, 'config.ini')
config_ini.read(config_ini_path, encoding='utf-8')

input_csv_path = os.path.join(BASE_DIR, config_ini.get('CSV', 'INPUT'))
output_csv_path = os.path.join(BASE_DIR, config_ini.get('CSV', 'OUTPUT'))

published_after, published_before = get_search_date_range()


def task():
    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    youtube_service = YoutubeService(config_ini.get('YOUTUBE', 'API_KEY'))
    with open(input_csv_path) as input_f:
        reader = csv.DictReader(input_f)
        for row in reader:
            print(row)
            create_csv_channel_videos(youtube_service, row, now)


def create_csv_channel_videos(youtube_service, row, now):
    with open(output_csv_path.format(row['チャンネル名'], now), 'w') as output_f:
        writer = csv.DictWriter(output_f, ['タイトル', '公開日時', '動画時間', '長尺', 'URL'])
        writer.writeheader()

        videos = youtube_service.search_videos(row['チャンネルID'], published_after, published_before)

        sorted_videos = sorted(videos, key=lambda x: x['snippet']['publishedAt'])

        for video in sorted_videos:
            video_detail = youtube_service.get_videos_detail(video['id']['videoId'])

            video_information = VideoInformation(
                video['id']['videoId'],
                video_detail['snippet']['title'],
                video_detail['snippet']['publishedAt'],
                video_detail['contentDetails']['duration']
            )
            writer.writerow(video_information.output_row())


class VideoInformation:
    def __init__(self, video_id, title, published_at, duration):
        self.video_id = video_id
        self.title = title
        self.published_at = published_at
        self.duration = duration

    @property
    def title(self):
        return f'{self._title} {self.duration}'

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def published_at(self):
        published_at = iso_to_jstdt(self._published_at)
        return f'{published_at.month}/{published_at.day}'

    @published_at.setter
    def published_at(self, value):
        self._published_at = value

    @property
    def duration(self):
        sub_duration = self._duration.translate(str.maketrans({'P': '', 'T': '', 'H': ':', 'M': ':', 'S': ''}))
        return ':'.join([s.zfill(2) for s in sub_duration.split(':')])

    @duration.setter
    def duration(self, duration):
        self._duration = duration

    def _duration_to_seconds(self):
        duration_list = list(map(int, self.duration.split(':')))
        print(f'{self.title} {duration_list}')
        if len(duration_list) == 1:
            dt_duration = datetime.timedelta(seconds=duration_list[-1])
        else:
            dt_duration = datetime.timedelta(minutes=duration_list[-2], seconds=duration_list[-1])
            if len(duration_list) == 3:
                dt_duration += datetime.timedelta(hours=duration_list[-3])
        return dt_duration.total_seconds()

    def _is_long(self):
        duration_seconds = self._duration_to_seconds()
        if duration_seconds < 60:
            return 'shorts'
        elif duration_seconds < 450:
            return '通常'
        elif duration_seconds < 900:
            return '長尺'
        elif duration_seconds < 1200:
            return '長尺2'
        return '長尺'

    def _url(self):
        return f'https://www.youtube.com/watch?v={self.video_id}'

    def output_row(self):
        return {
            'タイトル': self.title,
            '公開日時': self.published_at,
            '動画時間': self.duration,
            '長尺': self._is_long(),
            'URL': self._url()
        }


if __name__ == '__main__':
    task()
