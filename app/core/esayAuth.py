import json
import hashlib
from datetime import datetime
import time
import uuid
import secrets
from fastapi import Depends
from fastapi import Header
from fastapi import Request
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials
from app.core import config
from app.core._errors import HTTPAPIException
from app.core._status_code import trace_codes
from app.core._status_code import status_codes
from app.core._status_code import HTTPEXCEPTION_DEFAULT_HEADER


def auth_selector():
    if config.settings.ALLOW_AUTH_METHOD[0] == "HTTP_BASIC_AUTH":
        return HTTPBasic()
    else:
        return None


""" Created by Jin 2020/05

be used to do auth

general , check the accesstoken,onetimetoken,userid,clientid........

"""


async def get_redis(request: Request):
    """

    return Redis client -> aioredis.Redis

    """

    return request.app.state.OMI_CACHE_MANAGER


async def get_real_ip(request: Request, X_Forwarded_For: str = Header(None)):
    """

    server to server . white list check .

    """
    host = request.client.host
    if X_Forwarded_For:
        ip = X_Forwarded_For.split(",")[0]  # get client ip
    else:
        ip = host  # some times, request.client cant get the real ip

    # can do ipcheck or some other check in this function
    #
    # if ip in list:
    #     pass
    # else:
    #     pass
    check = 1

    if not check:
        raise HTTPAPIException(
            status_code=status_codes.FORBIDDEN,
            trace_code=trace_codes.AUTH_IP_NOT_IN_LIST_151_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)
    return host  # 只要过了check 这里返回host还是X_Forwarded_For里的ip已经无所谓了


async def get_client(x_ClientId: str = Header(None),
                     ip: str = Depends(get_real_ip)):
    """

    client check .
    if u want to refuse some request form some kind of device ,
    do it just at this function
    but u should not do any mapping at here

    """

    # if x_ClientId not in config.settings.CLIENT_PERMISSION_LIST:
    #     raise HTTPAPIException(
    #                     status_code=status_codes.FORBIDDEN,
    #                     detail=error.PERMISSION_DENIED_403_MESSAGE,
    #                     headers=error.HTTPEXCEPTION_DEFAULT_HEADER)

    return x_ClientId


async def use_basic_auth(credentials: any = Depends(auth_selector())):
    if credentials == None:
        return None
    authed_client_id = config.settings.HTTP_BASIC_AUTH_PERMITED_CLIENTS
    # authed_client_id = [("user","pass"),("user1","pass1")]
    for (username, password) in authed_client_id:
        correct_username = secrets.compare_digest(
            credentials.username, username)
        correct_password = secrets.compare_digest(
            credentials.password, password)
        if correct_username and correct_password:
            return username

    raise HTTPAPIException(
        status_code=status_codes.UNAUTHORIZED,
        trace_code=trace_codes.BASIC_AUTH_115_ERROR,
        headers=HTTPEXCEPTION_DEFAULT_HEADER)


# 服务间认证 基于httpBasic
async def get_client_from(
        username=Depends(use_basic_auth)):
    """
    client check .
    if u want to refuse some request form some kind of device ,
    do it just at this function
    but u should not do any mapping at here

    """

    # if x_ClientId not in config.settings.CLIENT_PERMISSION_LIST:
    #     raise HTTPAPIException(
    #                     status_code=status_codes.FORBIDDEN,
    #                     detail=error.PERMISSION_DENIED_403_MESSAGE,
    #                     headers=error.HTTPEXCEPTION_DEFAULT_HEADER)
    return username


async def get_onetimetoken(
        x_AccessToken: str = Header(...),
        x_OnetimeToken: str = Header(...),
        r: object = Depends(get_redis),
):
    """
    return onetimetoken->str
    onetimetoken check

    """

    # get tokenSet from redis
    tokenSet = await get_tokenSet(x_AccessToken, r)

    onetimetoken = tokenSet.get("onetime_token")

    # header check
    if onetimetoken is None \
            or not onetimetoken \
            or onetimetoken != x_OnetimeToken:
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_ONETIMETOKEN_152_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)

    DOMAIN = config.settings.REDIS_DOMAIN_ONETIME_TOKEN

    k = (
            config.settings.REDIS_PREFIX
            + DOMAIN
            + config.settings.ACCESSTOKEN_PREFIX
            + x_AccessToken
    )

    onetimetokenSet = await r.get(k)

    # validity check
    if not onetimetokenSet or not isinstance(onetimetokenSet, str):
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_ONETIMETOKEN_152_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)
    try:
        onetimetokenSet = json.loads(onetimetokenSet)
    except Exception:
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_ONETIMETOKENSTRUCTURE_153_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)

    if onetimetoken != onetimetokenSet.get("onetime_token"):
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_ONETIMETOKENSTRUCTURE_153_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)

    now = int(time.time())
    expire = int(onetimetokenSet.get("expires_in"))
    if now > expire:
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_ONETIMETOKEN_EXPIRED_154_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)

    return onetimetoken


async def get_tokenSet(x_AccessToken, r) -> dict:
    """
    return tokenSet->dict

    """
    tokenSet = {}
    DOMAIN = config.settings.REDIS_DOMAIN_ACCESS_TOKEN
    k = config.settings.REDIS_PREFIX + DOMAIN \
        + config.settings.ACCESSTOKEN_PREFIX + x_AccessToken
    tokenSet = await r.get(k)

    # isinstance maybe is not necessary
    if not tokenSet or not isinstance(tokenSet, str):
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_ACCESSTOKEN_155_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)
    try:
        tokenSet = json.loads(tokenSet)
    except Exception:
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_ACCESSTOKENSTRUCTURE_156_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)
    return tokenSet


async def is_same_person(
        # x_jwtToken:str=Header(None),
        x_AccessToken: str = Header(...),
        x_Userid: str = Header(...),
        client: str = Depends(get_client),
        r: object = Depends(get_redis),
):
    """
    userid check
    return x_Userid(short user id for service ,
    frontend cant only get the short userid)

    这里没有加入进一步的交叉认证以及db查询，如果有需求，可以在这里进行更进一步的user Check

    """
    # if (not x_Userid) or (not x_AccessToken):
    #     raise HTTPAPIException(
    #         status_code=status_codes.HTTP_400_BAD_REQUEST,
    #         detail={
    #             "code": error.PARAM_ENTRY_101_ERROR,
    #             "msg": error.PARAM_ENTRY_101_ERROR_MESSAGE,
    #         },
    #         headers=HTTPEXCEPTION_DEFAULT_HEADER
    #     )

    tokenSet = await get_tokenSet(x_AccessToken, r)

    if x_Userid != tokenSet.get("user_id_short"):
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_USEID_159_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)

    now = int(time.time())
    expire = int(tokenSet.get("expires_in"))
    AccessToken = tokenSet.get("access_token")

    # expire
    if now > expire:
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_ACCESSTOKEN_EXPIRED_157_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)

    # sha Sign
    # tk = sha(
    #         x_jwtToken = x_jwtToken,
    #         x_Userid = x_Userid,
    #         client = client,
    #         time = "15999999999")#时间从tokenSet取出

    if AccessToken != x_AccessToken:
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_ACCESSTOKEN_155_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)

    return x_Userid


async def get_current_user(
        # x_jwtToken:str=Header(None),
        x_AccessToken: str = Header(None),
        x_Userid: str = Depends(is_same_person),
        r: object = Depends(get_redis),
) -> str:
    """
    user check
    todo
    is same person?

    """

    userSet = await get_Userset(x_Userid, r)

    usertype = userSet.get("user_type")

    if str(usertype) not in config.settings.USER_PERMISSION_LIST_USER:
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_USERTYPE_158_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)

    return x_AccessToken


async def get_exchange_user(
        # x_jwtToken:str=Header(None),
        x_AccessToken: str = Header(None),
        x_OnetimeToken: str = Depends(get_onetimetoken),
        x_Userid: str = Depends(is_same_person),
        r: object = Depends(get_redis),
) -> str:
    """
    exchange user check
    todo
    is same person?
    onetimetoken is valid?
    userid's authority is ok?

    """

    userSet = await get_Userset(x_Userid, r)

    usertype = userSet.get("user_type")
    if str(usertype) not in config.settings.USER_PERMISSION_LIST_EXCHANGE:
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_USERTYPE_158_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)

    return x_AccessToken


async def get_current_user_server(
        x_jwtToken: str = Header(None),
        x_AccessToken: str = Header(None),
        x_Userid: str = Header(None),
        client: str = Depends(get_client),
) -> str:
    """
    server check
    todo
    is client id in the permission list?

    """

    # for now, server is not be seen as a user

    if client not in config.settings.CLIENT_PERMISSION_LIST:
        raise HTTPAPIException(
            status_code=status_codes.FORBIDDEN,
            trace_code=trace_codes.AUTH_INVALID_USERTYPE_158_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)

    return x_AccessToken


async def get_admin_user(
        x_jwtToken: str = Header(None),
        x_AccessToken: str = Header(...),
        x_Userid: str = Depends(is_same_person),
        r: object = Depends(get_redis),
        onetimetoken: str = Depends(get_onetimetoken),
) -> str:
    """
    admin check
    todo

    onetimetoken is valid?
    is same person?
    userid's authority is ok?

    """
    # r = await get_redis()

    userSet = await get_Userset(x_Userid, r)
    usertype = userSet.get("user_type")

    # authority check
    if str(usertype) not in config.settings.USER_PERMISSION_LIST_ADMIN:
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_USERTYPE_158_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)

    # if u need go Db Check
    # delete onetimeToken
    # onetimetoken = await disable_onetimeToken(x_AccessToken,r)
    return x_AccessToken


# async def disable_onetimeToken(x_AccessToken, r):

#     DOMAIN = config.settings.REDIS_DOMAIN_ONETIME_TOKEN
#     k = config.settings.REDIS_PREFIX+DOMAIN + \
#         config.settings.ACCESSTOKEN_PREFIX+x_AccessToken

#     count = r.delete(k)

#     return count


async def get_Userset(userid: str, r) -> dict:
    """
    get userset from redis
    return userset -> dict

    """
    DOMAIN = config.settings.REDIS_DOMAIN_USER
    k = config.settings.REDIS_PREFIX + DOMAIN + userid
    userSet = await r.get(k)
    if not userSet or not isinstance(userSet, str):
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_USEID_159_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)
    try:
        userSet = json.loads(userSet)
    except Exception:
        raise HTTPAPIException(
            status_code=status_codes.UNAUTHORIZED,
            trace_code=trace_codes.AUTH_INVALID_USEID_159_ERROR,
            headers=HTTPEXCEPTION_DEFAULT_HEADER)

    return userSet


def sha(x_jwtToken: str, x_Userid: str, client: str, time: str):
    SALT = time + x_jwtToken + client + x_Userid
    SECRECT = config.settings.ACCESSTOKEN_SEC
    sha = SECRECT + SALT
    sha = hashlib.sha1(sha.encode("utf-8"))
    encrypts = sha.hexdigest()
    return encrypts


async def onetimetoken_reset(request, x_AccessToken):
    """
    reset ontimetoken

    u should call this function before return in the function which depends
    get_admin_user,get_exchange_user

    """

    DOMAIN = config.settings.REDIS_DOMAIN_ONETIME_TOKEN
    k1 = (
            config.settings.REDIS_PREFIX
            + DOMAIN
            + config.settings.ACCESSTOKEN_PREFIX
            + x_AccessToken
    )
    DOMAIN = config.settings.REDIS_DOMAIN_ACCESS_TOKEN
    k2 = (
            config.settings.REDIS_PREFIX
            + DOMAIN
            + config.settings.ACCESSTOKEN_PREFIX
            + x_AccessToken
    )
    ####
    r = await get_redis(request)
    accessTokenSet = json.loads(await r.get(k2))

    onetimeToken, expire = await onetime_token_generater(accessTokenSet)
    print(onetimeToken)
    accessTokenSet["onetime_token"] = onetimeToken
    onetimeTokenSet = {
        "access_token": x_AccessToken,
        "onetime_token": onetimeToken,
        "token_id": str(uuid.uuid4()),
        "generate_date": int(time.time()),
        "user_id_short": accessTokenSet.get("user_id_short"),
        "user_id": accessTokenSet.get("user_id"),
        "expires_in": expire,
    }

    await r.set(k1, json.dumps(onetimeTokenSet), expire=expire)
    await r.set(k2, json.dumps(accessTokenSet), expire=expire)

    return onetimeToken


async def onetime_token_generater(accessTokenSet):
    # ONETIMETOKEN_SALT1: str = "15999999999"  # time
    # ONETIMETOKEN_SALT2: str = "accessTOken"  # accessTOken
    # ONETIMETOKEN_SALT3: str = "11111"  # userid
    # ONETIMETOKEN_SALT: str = ONETIMETOKEN_SALT1 + \
    #     ONETIMETOKEN_SALT2 + ONETIMETOKEN_SALT3

    now = int(time.time())
    expire = now + config.settings.ONETIME_TOKEN_EXPIRE_MINUTES * 60
    accessToken = accessTokenSet.get("access_token")
    userId = accessTokenSet.get("user_id")

    sec = config.settings.ONETIMETOKEN_SEC
    salt = str(expire) + accessToken + userId
    sha = sec + salt
    sha = hashlib.sha1(sha.encode("utf-8"))
    onetime_token = sha.hexdigest()
    return onetime_token, expire
