from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    PasswordLoginView,
    ZqAuthLoginView,
    SmsMsgView,
{%- if cookiecutter.use_wechat == 'y' %}
    OpenIdLoginView,
    WechatLoginView,
{%- endif %}
)


router = routers.SimpleRouter()

router.register("sms", SmsMsgView, basename="sms")

urlpatterns = [
{%- if cookiecutter.use_wechat == 'y' %}
    path(
        "login/wechat/",
        WechatLoginView.as_view(),
        name="wechat_login"
    ),  # 微信登录
    path(
        "login/wechat/openid/",
        OpenIdLoginView.as_view(),
        name="openid_pair"
    ),  # openid登录
{%- endif %}
    path(
        "login/zq/",
        ZqAuthLoginView.as_view(),
        name="zq_auth_login",
    ),  # ZqAuth登录
    path(
        "login/password/",
        PasswordLoginView.as_view(),
        name="password_login"
    ),  # 密码登录
    path(
        "login/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),  # 刷新token
]

urlpatterns += router.urls
