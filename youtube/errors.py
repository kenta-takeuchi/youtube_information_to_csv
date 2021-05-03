class YoutubeError(Exception):
    """youtube apiに関するエラー基底クラス"""


class NoChannelError(YoutubeError):
    """チャンネル情報を取得できなかった時のエラークラス"""


class NoMovieError(YoutubeError):
    """動画情報を取得できなかった時のエラークラス"""


class NoMovieDetailError(YoutubeError):
    """動画の詳細情報を取得できなかった時のエラークラス"""


class NetworkAccessError(YoutubeError):
    """ネットワークエラー時のエラークラス"""
