from fastapi import APIRouter, Depends

import app.core.esayAuth as auth

router = APIRouter()


@router.get("/mock/auth/get_redis")
async def get_redis(r=Depends(auth.get_redis)):
    await r.set("alpha","beta",expire=60)
    res = await r.get("alpha")
    return res

@router.get("/mock/auth/get_real_ip")
async def get_real_ip(ip=Depends(auth.get_real_ip)):

    return ip
@router.get("/mock/auth/get_client")
async def get_client(client=Depends(auth.get_client)):

    return client
@router.get("/mock/auth/onetimetoken")
async def get_onetimetoken(onetimetoken=Depends(auth.get_onetimetoken)):

    return onetimetoken


@router.get("/mock/auth/is_same_person")
async def is_same_person(user_id=Depends(auth.is_same_person)):

    return user_id

@router.get("/mock/auth/get_current_user")
async def get_current_user(ak=Depends(auth.get_current_user)):

    return ak

@router.get("/mock/auth/get_exchange_user")
async def get_exchange_user(ak=Depends(auth.get_exchange_user)):

    return ak
@router.get("/mock/auth/get_current_user_server")
async def get_current_user_server(ak=Depends(auth.get_current_user_server)):
    return ak
@router.get("/mock/auth/get_admin_user")
async def get_admin_user(ak=Depends(auth.get_admin_user)):
    return ak

@router.get("/mock/auth/get_client_from")
async def get_client_from(ak=Depends(auth.get_client_from)):
    return ak







