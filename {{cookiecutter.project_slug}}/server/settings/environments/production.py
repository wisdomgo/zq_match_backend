from server.settings.components import config
from server.settings.components.configs import CacheConfig

# debug 模式
DEBUG = config("DJANGO_DEBUG", False, cast=bool)

ALLOWED_HOSTS = [
    "localhost",
    "{{cookiecutter.project_name}}.ziqiang.net.cn",
    "api.{{cookiecutter.project_name}}.ziqiang.net.cn",
    "test.{{cookiecutter.project_name}}.ziqiang.net.cn",
    "api.test.{{cookiecutter.project_name}}.ziqiang.net.cn",
]

SERVER_URL = config("SERVER_URL", "https://api.{{cookiecutter.project_name}}.ziqiang.net.cn")

# region Cache
# Redis
CacheConfig.url = "redis://redis"
CACHES = CacheConfig.get()

{%- if cookiecutter.use_celery == 'y' %}
CELERY_BROKER_URL = "redis://redis/0"
{%- endif %}
# endregion
