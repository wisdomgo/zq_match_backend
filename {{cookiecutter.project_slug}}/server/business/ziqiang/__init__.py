from django.conf import settings
from django.core.cache import caches
from zq_auth_sdk import ZqAuthClient
from zq_auth_sdk.storage import SessionStorage


class ZqAuthCache(SessionStorage):
    def __init__(self, cache):
        self.cache = cache

    def get(self, key, default=None):
        return self.cache.get(key, default)

    def set(self, key, value, ttl=None):
        self.cache.set(key, value, timeout=ttl)

    def delete(self, key):
        self.cache.delete(key)


if settings._ENV == "test":
    from unittest import mock

    zq_client = mock.MagicMock()
else:
    zq_client = ZqAuthClient(
        settings.ZQAUTH_APPID,
        settings.ZQAUTH_SECRET,
        storage=ZqAuthCache(caches["third_session"]),
    )
