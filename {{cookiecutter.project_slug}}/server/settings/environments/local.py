# 本地模式
from server.settings import config, ZQ_EXCEPTION
from server.settings.components.configs import CacheConfig, DatabaseConfig

DEBUG = True

ALLOWED_HOSTS = ["*"]

SERVER_URL = "http://127.0.0.1:8000"


ZQ_EXCEPTION["EXCEPTION_UNKNOWN_HANDLE"] = False


QUERYCOUNT = {
    "THRESHOLDS": {
        "MEDIUM": 50,
        "HIGH": 200,
        "MIN_TIME_TO_LOG": 0,
        "MIN_QUERY_COUNT_TO_LOG": 0,
    },
    "IGNORE_REQUEST_PATTERNS": [],
    "IGNORE_SQL_PATTERNS": [],
    "DISPLAY_DUPLICATES": 10,
    "RESPONSE_HEADER": "X-DjangoQueryCount-Count",
}


CACHEOPS = {}
