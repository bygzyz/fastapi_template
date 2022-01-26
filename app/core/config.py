import secrets
import os
from typing import List, Union,Any
from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    validator,
)


class SettingUtils:
    ENV_CONFIG_SPLITER:str = ','
    ENV_PAIR_SPLITER: str = ':'

    @classmethod
    def os_get_env(cls, key: str, default: Any = None):
        value = os.getenv(key)
        if value is not None:
            return value
        else:
            return default

    @classmethod
    def os_get_env_list(cls, key: str, default: Any = None):
        set_val = os.getenv(key)
        if set_val is None:
            return default
        if set_val.find(cls.ENV_CONFIG_SPLITER) == -1:
            return [set_val]
        list = set_val.split(cls.ENV_CONFIG_SPLITER)
        result = []
        for v in list:
            if v is not None:
                result.append(v)
        return result

    @classmethod
    def os_get_env_tuple(cls, key: str, default: Any = None):
        set_val = os.getenv(key)
        if set_val is None:
            return default
        if set_val.find(cls.ENV_CONFIG_SPLITER) == -1:
            list = [set_val]
        else:
            list = set_val.split(cls.ENV_CONFIG_SPLITER)
        result = []
        for list_item in list:
            if list_item.find(cls.ENV_PAIR_SPLITER) == -1:
                raise ValueError(
                    "%s is not an mapping, use key:value" % list_item)
            pair = list_item.split(cls.ENV_PAIR_SPLITER)
            if len(pair) != 2:
                raise ValueError("%s has too many items" % list_item)
            result.append((pair[0], pair[1]))
        return result

    @classmethod
    def os_get_env_dict(cls, key: str, default=None):
        return dict(cls.os_get_env_tuple(key, default))


class DefaultSettings(BaseSettings):
    # =======================================
    # 环境变量获取
    # =======================================
    EXCHANGE_ENV: str = SettingUtils.os_get_env("EXCHANGE_ENV", "")

    # =======================================
    # 共通常量
    # =======================================
    VERSION: str = SettingUtils.os_get_env("VERSION", "V.1.0.0")
    APP_NAME: str = SettingUtils.os_get_env("APP_NAME", "business")
    SERVER_NAME: str = SettingUtils.os_get_env("SERVER_NAME",
                                               "Business-Develop")
    SERVER_HOST: AnyHttpUrl = SettingUtils.os_get_env("SERVER_HOST",
                                                      "http://0.0.0.0")

    # =======================================
    # API_V1_STR
    # =======================================
    API_V1_STR: str = SettingUtils.os_get_env("API_V1_STR", "")
    FAST_API_INIT_ARGS = {
        "docs_url": API_V1_STR,
        "openapi_url": API_V1_STR + "/openapi.json",
    }

    # =======================================
    # PROJECT_NAME
    # =======================================
    PROJECT_NAME: str = SettingUtils.os_get_env("PROJECT_NAME",
                                                "AiShu.Exchange.Business")
    # =======================================

    # =======================================
    # HTTP AUTH FOR PUBLIC
    # =======================================

    HTTP_AUTH_PUBLIC_CLIENT_ID = SettingUtils.os_get_env("HTTP_AUTH_PUBLIC_CLIENT_ID", "client_id")
    HTTP_AUTH_PUBLIC_CLIENT_SECRET = SettingUtils.os_get_env("HTTP_AUTH_PUBLIC_CLIENT_SECRET", "client_secret")

    # database basic auth unvisible to
    ALLOW_AUTH_METHOD: list = ["HTTP_BASIC_AUTH"]
    HTTP_BASIC_AUTH_PERMITED_CLIENTS: list = \
        [(HTTP_AUTH_PUBLIC_CLIENT_ID, HTTP_AUTH_PUBLIC_CLIENT_SECRET)]

    # =======================================
    # CLIENT_ID FOR RPC
    # =======================================

    # database basic auth unvisible to
    SERVICE_CLIENT_ID: str = SettingUtils.os_get_env("SERVICE_CLIENT_ID",
                                                     'client_id')
    SERVICE_CLIENT_SECRET: str = SettingUtils.os_get_env(
        "SERVICE_CLIENT_SECRET", 'client_secret')

    # =======================================
    # REDIS
    # =======================================
    REDIS_SCHEME: str = SettingUtils.os_get_env("REDIS_SCHEME", "redis")
    REDIS_HOST: str = SettingUtils.os_get_env("REDIS_HOST", "localhost")
    REDIS_PORT: str = SettingUtils.os_get_env("REDIS_PORT", "6379")
    REDIS_USER: str = SettingUtils.os_get_env("REDIS_USER", "")
    REDIS_PASSWORD: str = SettingUtils.os_get_env("REDIS_PASSWORD", None)
    REDIS_DATABASE: int = SettingUtils.os_get_env("REDIS_DATABASE", 0)

    # =======================================
    # CACHE BACKEND
    # =======================================
    CACHE_BACKEND: str = SettingUtils.os_get_env("CACHE_BACKEND",
                                                       "omi_cache_manager.aredis_backend.ARedisBackend")

    # =======================================
    # USE MOCK
    # =======================================
    USE_MOCK: bool = SettingUtils.os_get_env("USE_MOCK", False)

    # =======================================
    # API RESPONSE GLOBALS
    # =======================================
    API_RESPONSE_GLOBALS = {"false": False, "true": True, "null": None,
                            "'": "'"}

    # =======================================
    # RPC
    # =======================================
    HTTP_BACKEND: str = SettingUtils.os_get_env("HTTP_BACKEND", "omi_async_http_client.AioHttpClientBackend")
    RESOURCE_ENDPOINT: str = SettingUtils.os_get_env("RESOURCE_ENDPOINT",
                                                       "http://api-database-svc/api/v1/database")
    # =======================================
    # CLIENT_ID FOR RPC
    # =======================================

    CLIENT_ID: str = SettingUtils.os_get_env("CLIENT_ID", 'client_id')

    CLIENT_SECRET: str = SettingUtils.os_get_env("CLIENT_SECRET", 'client_secret')
    # =======================================

    # =======================================
    # LOGSTASH
    # =======================================
    LOG_STASH_HOST = SettingUtils.os_get_env("LOG_STASH_HOST", "localhost")
    LOG_STASH_PORT = SettingUtils.os_get_env("LOG_STASH_PORT", "9300")

    # =======================================
    # BACKEND_CORS_ORIGINS
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://127.0.0.1",
        "http://localhost",
        "http://localhost:8080",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
            cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # =======================================
    # Config for Database PAGING
    # =======================================
    RECORD_MAX_COUNT: int = SettingUtils.os_get_env("RECORD_MAX_COUNT", 1000)
    PAGE: int = SettingUtils.os_get_env("PAGE", 1)
    MAX_PAGE: int = SettingUtils.os_get_env("MAX_PAGE", 65535)
    PER_PAGE: int = SettingUtils.os_get_env("PER_PAGE", 1000)

    # =======================================
    # JWT SETTINGS
    # =======================================
    JWT_SECRET_KEY: str = SettingUtils.os_get_env("JWT_SECRET_KEY",
                                                  secrets.token_urlsafe(32))
    JWT_ALGORITHM: str = SettingUtils.os_get_env("JWT_ALGORITHM", "HS256")

    # =======================================
    # Config for Store
    # =======================================
    REDIS: object = None
    CACHE: object = None

    # =======================================
    # redis prefix
    # =======================================
    API_VERSION: str = SettingUtils.os_get_env("API_VERSION", "V1:")
    API_SCHEMA: str = SettingUtils.os_get_env("API_SCHEMA", "dev:")
    API_SERVICENAME: str = SettingUtils.os_get_env(
        "API_SERVICENAME", "business:")
    REDIS_DOMAIN_ACCESS_TOKEN: str = SettingUtils.os_get_env(
        "REDIS_DOMAIN_ACCESS_TOKEN", "TBL_ACCESS_TOKEN:")
    REDIS_DOMAIN_ONETIME_TOKEN: str = SettingUtils.os_get_env(
        "REDIS_DOMAIN_ONETIME_TOKEN", "TBL_ONETIME_TOKEN:")
    REDIS_DOMAIN_USER: str = SettingUtils.os_get_env(
        "REDIS_DOMAIN_USER", "TBL_USER:")
    REDIS_PREFIX: str = API_VERSION + API_SCHEMA + "account:"

    # =======================================
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = SettingUtils.os_get_env(
        "ACCESS_TOKEN_EXPIRE_MINUTES", 11520)
    # 60 minutes
    ONETIME_TOKEN_EXPIRE_MINUTES: int = SettingUtils.os_get_env(
        "ONETIME_TOKEN_EXPIRE_MINUTES", 60)
    ONETIME_TOKEN_EXPIRE_SECONDS: int = SettingUtils.os_get_env(
        "ONETIME_TOKEN_EXPIRE_SECONDS", 900)
    ACCESS_TOKEN_EXPIRE_SECONDS: int = SettingUtils.os_get_env(
        "ACCESS_TOKEN_EXPIRE_SECONDS", 3600)
    # =======================================

    class Config:
        case_sensitive = True
        validate_all = False
        if SettingUtils.os_get_env("EXCHANGE_ENV") is not None:
            env_file = SettingUtils.os_get_env("EXCHANGE_ENV") + ".env"
        else:
            env_file = ".env"


class AppSettings(DefaultSettings):

    # =======================================
    # TOKEN
    # =======================================
    ACCESSTOKEN_SEC: str = "accessToken"  # SEC
    ONETIMETOKEN_SEC: str = "onetimeToken"
    ACCESSTOKEN_PREFIX: str = "X_"

    # =======================================
    # USER AUTH
    # =======================================
    USER_PERMISSION_LIST_ADMIN: list = ["admin"]
    USER_PERMISSION_LIST_EXCHANGE: list = ["manager"]
    USER_PERMISSION_LIST_USER: list = ["user", "manager"]

    CLIENT_PERMISSION_LIST: list = ["2"]

    # =======================================

    pass


settings = AppSettings()
