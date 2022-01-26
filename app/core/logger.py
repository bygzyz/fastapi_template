import os
import logging.config

from app.utils.log import info_get
from app.core.config import settings

# 日志目录配置
BASE_DIR = os.getcwd()  # 根目录
BASE_LOG_DIR = os.path.join(BASE_DIR, "log")
LOGGER_INFO_FILENAME = os.path.join(BASE_LOG_DIR,
                                    settings.SERVER_NAME + "-info.log")
LOGGER_ERROR_FILENAME = os.path.join(BASE_LOG_DIR,
                                     settings.SERVER_NAME + "-error.log")
if not os.path.exists(BASE_LOG_DIR):
    os.mkdir(BASE_LOG_DIR)

# 日志格式
LOGGING_CONFIG = {
    "version": 1,
    # 禁用已经存在的logger实例
    "disable_existing_loggers": False,
    # 定义日志 格式化的 工具
    "formatters": {
        'standard': {
            'format': '[%(levelname)s][%(asctime)s][%(module)s %('
                      'funcName)s]%(message)s '
        },
        'ietf_rfc5424': {
            'format': '%(asctime)s %(hostname)s %(name)s %(process)d - - [%('
                      'levelname)s:%(levelno)s][%(module)s %(funcName)s]%('
                      'message)s '
        },
        "simple": {
            "format": "[%(levelname)s][%(asctime)s][%(filename)s:%("
                      "lineno)d]%(message)s "
        },
        "info": {
            "format": "[%(asctime)s][app_name:%(name)s][%(levelname)s:"
                      "%(levelno)s][%(message)s]"
        },
        "error": {
            "format": "[%(levelname)s][%(asctime)s][%(filename)s:%("
                      "lineno)d]%(message)s "
        },
    },
    # 过滤
    "filters": {
        "require_debug_true": {
            "()": "app.utils.log.RequireDebugTrue"
        }
    },
    # 日志处理器
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],  # 只有在为True时才在屏幕打印日志
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "default": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",  # 保存到文件，自动切
            "filename": LOGGER_INFO_FILENAME,  # 日志文件
            "maxBytes": 1024 * 1024 * 50,  # 日志大小 50M
            "backupCount": 3,
            "formatter": "info",
            "encoding": "utf-8",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",  # 保存到文件，自动切
            "filename": LOGGER_ERROR_FILENAME,  # 日志文件
            "maxBytes": 1024 * 1024 * 50,  # 日志大小 50M
            "backupCount": 5,
            "formatter": "error",
            "encoding": "utf-8",
        },
        "logstash": {
            "level": "INFO",
            "class": "logstash.TCPLogstashHandler",
            "host": settings.LOG_STASH_HOST,
            "port": settings.LOG_STASH_PORT,
            "tags": [],  # TODO Logstash里面显示的标签
            "version": 1,  # TODO 版本
            # 'type' field in logstash message. Default value: 'logstash'.
            # 'fqdn': False,
            # 'encoding': "utf-8"
        },
    },
    # logger实例
    "loggers": {
        # 默认的logger应用如下配置
        "": {
            "handlers": ["default", "console", "error"],  # 上线之后可以把'console'移除
            "level": "DEBUG",
            "propagate": True,
        },
        # 系统log配置
        settings.APP_NAME: {
            "handlers": ["default", "console", "error", "logstash"],
            "level": "ERROR",
        },
    },
}


class Logger:
    logging.config.dictConfig(LOGGING_CONFIG)  # 导入上面定义的logging配置
    logger = logging.getLogger(settings.APP_NAME)


class LoggerProxy:
    logger = Logger().logger

    # INFO
    @classmethod
    def info(cls, *args):
        # 自定义日志信息
        info = info_get()
        # 编辑信息
        msg = ",".join(args)

        # 输出日志
        cls.logger.info(
            msg, extra={"lineNo": info.get("lineNo"),
                        "fileName": info.get("fileName")}
        )

    # DEBUG
    @classmethod
    def debug(cls, *args):
        # 自定义日志信息
        info = info_get()
        # 编辑信息
        msg = ",".join(args)

        # 输出日志
        cls.logger.debug(
            msg, extra={"lineNo": info.get("lineNo"),
                        "fileName": info.get("fileName")}
        )

    # WARNING
    @classmethod
    def warning(cls, *args):
        # 自定义日志信息
        info = info_get()
        # 编辑信息
        msg = ",".join(args)

        # 输出日志
        cls.logger.warning(
            msg, extra={"lineNo": info.get("lineNo"),
                        "fileName": info.get("fileName")}
        )

    # ERROR
    @classmethod
    def error(cls, *args):
        # 自定义日志信息
        info = info_get()
        # 编辑信息
        msg = ",".join(args)

        # 输出日志
        cls.logger.error(
            msg,
            exc_info=True,
            extra={"lineNo": info.get("lineNo"),
                   "fileName": info.get("fileName")},
        )

    # CRITICAL
    @classmethod
    def critical(cls, *args):
        # 自定义日志信息
        info = info_get()
        # 编辑信息
        msg = ",".join(args)

        # 输出日志
        cls.logger.critical(
            msg,
            exc_info=True,
            extra={"lineNo": info.get("lineNo"),
                   "fileName": info.get("fileName")},
        )


logger = LoggerProxy
