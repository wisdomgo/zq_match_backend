import re
from datetime import datetime
from typing import Dict, Any
from uuid import UUID

from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField
from zq_django_util.exceptions import ApiException
from zq_django_util.utils.auth.backends import OpenIdBackend
{%- if cookiecutter.use_wechat == 'y' %}
from zq_django_util.utils.auth.serializers import (
    OpenIdLoginSerializer as DefaultOpenIdLoginSerializer,
)
{%- endif %}

from users.models import User
from oauth.utils import VerifyCodeUtil
from oauth.backends import UnionIdBackend
from server.business.ziqiang.auth import get_union_id
{%- if cookiecutter.use_wechat == 'y' %}
from server.business.wechat.wxa import get_openid
{%- endif %}
{%- if cookiecutter.use_wechat == 'y' %}


class OpenIdLoginSerializer(DefaultOpenIdLoginSerializer):
    """
    OpenID Token 获取序列化器 (直接用 openid 获取登录 token，用于测试)
    """

    backend = OpenIdBackend(User)  # 自定义验证后端，用于指定不同类型的用户模型

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_token(cls, user: User):
        """
        自定义 jwt payload
        """
        token = super().get_token(user)
        token["is_staff"] = user.is_staff
        return token

    def generate_token_result(
        self,
        user: User,
        user_id_field: str,
        expire_time: datetime,
        access: str,
        refresh: str,
    ) -> dict:
        """
        生成登录接口返回结果

        :param user: 用户对象
        :param user_id_field: 用户主键字段
        :param expire_time: 过期时间
        :param access: access token
        :param refresh: refresh token
        :return:
        """
        return dict(
            id=getattr(user, user_id_field),
            username=user.username,
            is_active=user.is_active,
            expire_time=expire_time,
            access=access,
            refresh=refresh,
        )

    def handle_new_openid(self, openid: str) -> User:
        """
        重写处理新 openid 方法
        """
        super().handle_new_openid(openid)


class WechatLoginSerializer(OpenIdLoginSerializer):
    """
    微信登录序列化器
    """

    code = PasswordField(label="前端获取code")  # 前端传入 code

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields.pop("openid")  # 删除 openid 字段

    def get_open_id(self, attrs: Dict[str, Any]) -> str:
        """
        重写获取 open_id 方法
        """
        return get_openid(attrs["code"])
{%- endif %}


class ZqAuthLoginSerializer(DefaultOpenIdLoginSerializer):
    """
    自强Auth登录序列化器
    """

    backend = UnionIdBackend(User)
    openid = None
    openid_field = "union_id"
    code = PasswordField(label="前端获取code")  # 前端传入 code

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_token(cls, user: User):
        """
        自定义 jwt payload
        """
        token = super().get_token(user)
        token["is_staff"] = user.is_staff
        return token

    def generate_token_result(
        self,
        user: User,
        user_id_field: str,
        expire_time: datetime,
        access: str,
        refresh: str,
    ) -> dict:
        """
        生成登录接口返回结果

        :param user: 用户对象
        :param user_id_field: 用户主键字段
        :param expire_time: 过期时间
        :param access: access token
        :param refresh: refresh token
        :return:
        """
        return dict(
            id=getattr(user, user_id_field),
            username=user.username,
            is_active=user.is_active,
            expire_time=expire_time,
            access=access,
            refresh=refresh,
        )

    def get_open_id(self, attrs: Dict[str, Any]) -> UUID:
        """
        重写获取 open_id 方法
        """
        return get_union_id(attrs["code"])

    def handle_new_openid(self, union_id: UUID) -> User:
        """
        重写处理新 union id 方法
        """
        super().handle_new_openid(union_id)


class PasswordLoginSerializer(DefaultOpenIdLoginSerializer):
    """
    密码登录
    """

    def generate_token_result(
        self,
        user: User,
        user_id_field: str,
        expire_time: datetime,
        access: str,
        refresh: str,
    ) -> dict:
        """
        生成登录接口返回结果

        :param user: 用户对象
        :param user_id_field: 用户主键字段
        :param expire_time: 过期时间
        :param access: access token
        :param refresh: refresh token
        :return:
        """
        return dict(
            id=getattr(user, user_id_field),
            username=user.username,
            is_active=user.is_active,
            expire_time=expire_time,
            access=access,
            refresh=refresh,
            is_superuser=user.is_superuser,
        )

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_staff"] = user.is_staff
        return token


class SmsMsgSerializer(serializers.Serializer):
    """
    发送短信验证码序列化器
    """
    phone = serializers.CharField(max_length=11, min_length=11, label="手机号", write_only=True)
    code = serializers.IntegerField(min_value=100000, max_value=999999, label="验证码", write_only=True, required=False)
    status = serializers.CharField(max_length=2, min_length=10, label="状态", read_only=True)

    def validate_phone(self, value: str) -> str:
        """
        验证手机号
        """
        if not re.match(r"^1[3456789]\d{9}$", value):
            raise ApiException

        return value

    def create(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        短信验证码
        """
        phone = validated_data["phone"]

        if not validated_data.get("code"):
            # 发送短信验证码
            VerifyCodeUtil.send_sms_verify_code(phone)
            return {"status": "send code"}
        else:
            # 验证短信验证码
            code = validated_data["code"]
            status = VerifyCodeUtil.verify_sms_code(phone, code)
            return {"status": "verify code " + str(status)}
