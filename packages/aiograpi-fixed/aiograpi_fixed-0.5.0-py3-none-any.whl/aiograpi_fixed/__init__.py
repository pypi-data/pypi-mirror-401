import logging
from urllib.parse import urlparse

from aiograpi_fixed.mixins.account import AccountMixin
from aiograpi_fixed.mixins.album import DownloadAlbumMixin, UploadAlbumMixin
from aiograpi_fixed.mixins.auth import LoginMixin
from aiograpi_fixed.mixins.bloks import BloksMixin
from aiograpi_fixed.mixins.challenge import ChallengeResolveMixin
from aiograpi_fixed.mixins.clip import DownloadClipMixin, UploadClipMixin
from aiograpi_fixed.mixins.collection import CollectionMixin
from aiograpi_fixed.mixins.comment import CommentMixin
from aiograpi_fixed.mixins.direct import DirectMixin
from aiograpi_fixed.mixins.fbsearch import FbSearchMixin
from aiograpi_fixed.mixins.graphql import GraphQLRequestMixin
from aiograpi_fixed.mixins.hashtag import HashtagMixin
from aiograpi_fixed.mixins.highlight import HighlightMixin
from aiograpi_fixed.mixins.igtv import DownloadIGTVMixin, UploadIGTVMixin
from aiograpi_fixed.mixins.insights import InsightsMixin
from aiograpi_fixed.mixins.location import LocationMixin
from aiograpi_fixed.mixins.media import MediaMixin
from aiograpi_fixed.mixins.multiple_accounts import MultipleAccountsMixin
from aiograpi_fixed.mixins.note import NoteMixin
from aiograpi_fixed.mixins.notification import NotificationMixin
from aiograpi_fixed.mixins.password import PasswordMixin
from aiograpi_fixed.mixins.photo import DownloadPhotoMixin, UploadPhotoMixin
from aiograpi_fixed.mixins.private import PrivateRequestMixin
from aiograpi_fixed.mixins.public import (
    ProfilePublicMixin,
    PublicRequestMixin,
    TopSearchesPublicMixin,
)
from aiograpi_fixed.mixins.share import ShareMixin
from aiograpi_fixed.mixins.signup import SignUpMixin
from aiograpi_fixed.mixins.story import StoryMixin
from aiograpi_fixed.mixins.timeline import ReelsMixin
from aiograpi_fixed.mixins.totp import TOTPMixin
from aiograpi_fixed.mixins.track import TrackMixin
from aiograpi_fixed.mixins.user import UserMixin
from aiograpi_fixed.mixins.video import DownloadVideoMixin, UploadVideoMixin


class Client(
    MultipleAccountsMixin,
    NoteMixin,
    GraphQLRequestMixin,
    PublicRequestMixin,
    ChallengeResolveMixin,
    PrivateRequestMixin,
    TopSearchesPublicMixin,
    ProfilePublicMixin,
    LoginMixin,
    ShareMixin,
    TrackMixin,
    FbSearchMixin,
    HighlightMixin,
    DownloadPhotoMixin,
    UploadPhotoMixin,
    DownloadVideoMixin,
    UploadVideoMixin,
    DownloadAlbumMixin,
    NotificationMixin,
    UploadAlbumMixin,
    DownloadIGTVMixin,
    UploadIGTVMixin,
    MediaMixin,
    UserMixin,
    InsightsMixin,
    CollectionMixin,
    AccountMixin,
    DirectMixin,
    LocationMixin,
    HashtagMixin,
    CommentMixin,
    StoryMixin,
    PasswordMixin,
    DownloadClipMixin,
    UploadClipMixin,
    ReelsMixin,
    BloksMixin,
    TOTPMixin,
    SignUpMixin,
):
    proxy = None
    logger = logging.getLogger("aiograpi_fixed")

    def __init__(
        self, settings: dict = {}, proxy: str = None, delay_range: list = None, **kwargs
    ):
        super().__init__(**kwargs)
        self.settings = settings
        self.delay_range = delay_range
        self.set_proxy(proxy)
        self.init()

    def set_proxy(self, dsn: str):
        if not dsn:
            self.public.proxy = self.private.proxy = None
            return False
        assert isinstance(
            dsn, str
        ), f'Proxy must been string (URL), but now "{dsn}" ({type(dsn)})'
        self.proxy = dsn
        proxy_href = "{scheme}{href}".format(
            scheme="http://" if not urlparse(self.proxy).scheme else "",
            href=self.proxy,
        )
        self.public.proxy = self.private.proxy = self.graphql.proxy = proxy_href
        return True
