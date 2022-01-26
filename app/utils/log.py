import logging.config
import sys


class RequireDebugFalse(logging.Filter):
    def filter(self, record):
        return False


class RequireDebugTrue(logging.Filter):
    def filter(self, record):
        return True


# 自定义信息获取
def info_get() -> dict:
    # 初始化返回值
    result = {}

    # 获取自定义日志信息
    frameObject = sys._getframe(2)
    path = frameObject.f_code.co_filename
    fileName = path.split('\\')[-1]
    lineNo = frameObject.f_lineno

    # 返回值设定
    result['path'] = path
    result['fileName'] = fileName
    result['lineNo'] = lineNo

    return result
