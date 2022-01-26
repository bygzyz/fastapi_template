"""
入口
"""

import os
import sys

import json
import traceback
import uvicorn
import time
import hashlib

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from omi_cache_manager import AsyncCacheManager

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.logger import logger
from app.core._status_code import trace_codes
from app.core import config

# app = FastAPI(**settings.FAST_API_INIT_ARGS)
app = FastAPI()


origins = [
    "http://127.0.0.1",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(settings.API_V1_STR+"/health")
async def health():
    return  JSONResponse(
            status_code=200,
            content={
                "health":"OK",
            },
        )

@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    s = traceback.format_exc()
    s_list = s.split("\n")
    s_list.pop()

    stack_list = []

    for s in s_list:
        stack_list.append(s.lstrip())

    if len(stack_list) > 6:
        stack_res = stack_list[-6:]
    else:
        stack_res = stack_list.pop()

    logger.error(str(exc))

    if settings.EXCHANGE_ENV == "production":
        return JSONResponse(
            status_code=500,
            content={
                "code": trace_codes.UNHANDLED_SYSTEM_EXCEPTION,
                "message": trace_codes.get_reason_phrase(
                    trace_codes.UNHANDLED_SYSTEM_EXCEPTION
                ),
                "detail": {"message": f"{exc}"},
            },
        )
    else:
        return JSONResponse(
            status_code=500,
            content={
                "code": trace_codes.UNHANDLED_SYSTEM_EXCEPTION,
                "message": trace_codes.get_reason_phrase(
                    trace_codes.UNHANDLED_SYSTEM_EXCEPTION
                ),
                "detail": {"message": f"{exc}", "stack": stack_res},
            },
        )


@app.on_event("startup")
async def startup_event():
    setting_dict = json.loads(settings.json())
    for k in setting_dict.keys():
        print(k, "=", setting_dict.get(k))
    AsyncCacheManager(
        app,  # None if no app context to set
        cache_backend=settings.CACHE_BACKEND,
        config={
            "CACHE_REDIS_SCHEME": settings.REDIS_SCHEME,
            "CACHE_REDIS_HOST": settings.REDIS_HOST,
            "CACHE_REDIS_PORT": settings.REDIS_PORT,
            "CACHE_REDIS_PASSWORD": settings.REDIS_PASSWORD,
            "CACHE_REDIS_DATABASE": settings.REDIS_DATABASE,
            "CACHE_REDIS_CONNECTION_TIMEOUT": 3,
            "CACHE_REDIS_ENCODING": 'utf-8',
            "CACHE_REDIS_USE_POOL": True,
            "CACHE_REDIS_POOL_MINSIZE": 1,  # no effect
            "CACHE_REDIS_POOL_MAXSIZE": 50,
            "CACHE_REDIS_USE_CLUSTER": False,  # for cluster not tested
            "CACHE_REDIS_MAX_IDLE_TIME": 0,
            "CACHE_REDIS_RETRY_ON_TIMEOUT": False,
            "CACHE_REDIS_IDLE_CHECK_INTERVAL": 1,
            "CACHE_KEY_PREFIX": ""
        }
    )
    settings.CACHE = app.state.OMI_CACHE_MANAGER

    return


@app.on_event("shutdown")
async def shutdown_event():
    # await settings.REDIS.disconnect()
    print("shutting down")
    return


app.include_router(api_router, prefix=settings.API_V1_STR)
if __name__ == "__main__":
    uvicorn.run(app="bootstrap:app", host="0.0.0.0", port=8000)
