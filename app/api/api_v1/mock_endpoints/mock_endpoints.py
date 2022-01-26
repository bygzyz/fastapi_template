"""
mock databases(仅单元测试使用)
"""

from fastapi import APIRouter, Body, Query, Request, status as s
from fastapi import status
from fastapi.responses import JSONResponse

from app.core._status_code import status_codes as sc, \
    trace_codes as tc

router = APIRouter()


# ================================================
# user 的模拟的 database 的api
# =================================================

@router.get("/mock/contents/user_contents")
async def obtain_user_contents():
    """
    用户内容一览检索
    """
    print("进入了mock user_contents_mock")

    return {
        'code': 100,
        'message': 'success',
        'detail': {
            "page": 1,
            "has_next": False,
            "total_pages": 1,
            "count": 4,
            "contents": [
                {
                    "product_type": "any_share_cloud",
                    "content_id": "48b315de07cb4c8a97a67f6cc796f73a",
                    "record_id": "2282c01a-5b88-4d00-9f0f-73c3cd53403d-"
                                 "2020-07-01:15:12:38",
                    "content_name": "11",
                    "publisher": "222",
                    "description": "333333",
                    "content_type": "application",
                    "version": "string",
                    "thumbnail_url": "string"
                },
                {
                    "product_type": "any_share_cloud",
                    "content_id": "7c53ed76c8b94a8da04b3823feb7f49d",
                    "record_id": "d2308d73-5682-4b74-9f54-53f19ffe0642-"
                                 "2020-07-01:15:32:31",
                    "content_name": "ys",
                    "publisher": "yeses",
                    "description": "asksaveasfilename,c",
                    "content_type": "application",
                    "version": "string",
                    "thumbnail_url": "string"
                }
            ]
        }
    }


@router.get('/mock/contents/user_content_details')
async def obtain_user_content_details(
        content_id: str
):
    """
    用户内容详细检索_mock_db
    """
    items = {
        "contents": {
            "content_id": "123",
            "record_id": "4ac75a52-85c6-478e-946"
                         "1-6e0438317b0e-2020-06-09:16:15:09",
            "product_type": "any_robot_cloud",
            "content_name": "tes",
            "publisher": "string",
            "description": "123",
            "content_type": "service",
            "version": "123",
            "product_info": "string",
            "logo_url": "string",
            "preview_media_urls": {
                "image_urls": [
                    "string"
                ],
                "video_urls": [
                    "string"
                ]
            },
            "support_info": {
                "phone": "string",
                "email": "string"
            },
            "count": 0,
            "file_size": "1"
        }
    }
    if content_id == '123':
        return JSONResponse(status_code=sc.OK, content={
            'code': 100,
            'message': 'success',
            'detail': items,
        })
    else:
        return JSONResponse(status_code=sc.NOT_FOUND, content={
            'code': sc.NOT_FOUND,
            'message': tc.DATA_NOT_FOUND_109,
            'detail': {}
        })


@router.get("/mock/contents/content_terms")
async def content_terms_get(
        request: Request
):
    """
    内容term检索_mock_db
    """
    record_id = request.query_params.get('record_id')
    term_type = request.query_params.get('term_type')
    items = {
        "relations": {
            "record_id": "123",
            "term_type": term_type,
            "terms": [
                {
                    "term_id": "123",
                    "slug": "string",
                    "text": "string",
                    "description": "321"
                },
                {
                    "term_id": "234",
                    "slug": "string",
                    "text": "string",
                    "description": "122223"
                }
            ]
        }
    }

    items1 = {
        "relations": {
            "record_id": "123",
            "term_type": term_type,
            "terms": []
        }
    }

    if record_id == '123':
        return JSONResponse(status_code=sc.OK, content={
            'code': 100,
            'message': 'success',
            'detail': items
        })
    else:
        return JSONResponse(status_code=sc.OK, content={
            'code': 100,
            'message': 'success',
            'detail': items1
        })


# ================================================
# manager 的模拟的 database 的api
# =================================================


@router.post('/mock/contents/mgr_content')
async def mgr_content_add():
    """
    insert 一条数据到 content_list
    """
    return {
        'code': 100,
        'message': 'success',
        'detail': {
            "content_id": "7de9b2a9497b435994745c4a56861d01",
            "record_id": "d4dc3ee6958b42d2b04f88c4d4919d41"
        }
    }


@router.put('/mock/contents/mgr_content')
async def mgr_content_edit(
        content_id: str = Body(...),
        record_id: str = Body(...),
):
    """
    insert 一条数据到 content_list
    """

    if content_id == '123':
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'code': 100,
                'message': 'success',
                'detail': {
                    "content_id": "123",
                    "record_id": record_id
                }
            })
    else:
        return JSONResponse(status_code=sc.NOT_FOUND, content={
            'code': tc.DATA_NOT_FOUND_109,
            'message': "根据当前的数据,未查询到结果",
            'detail': {}
        })


@router.delete("/mock/contents/mgr_draft")
async def mgr_draft_delete(
        content_id: str = Query(..., title="内容ID", max_length=100),
):
    """
    管理员草稿删除
    """
    if content_id == '123':
        return JSONResponse(
            status_code=sc.OK,
            content={
                "code": sc.OK,
                "message": "管理员草稿删除成功",
                "detail": {}
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'code': tc.DATA_NOT_FOUND_109,
                'message': tc.get_reason_phrase(tc.DATA_NOT_FOUND_109),
                "detail": {}
            }
        )


@router.post("/mock/terms/mgr_term")
async def mgr_term_add(
        slug: str = Body(...),
        text: str = Body(...),
):
    """
    管理员term新建
    """
    if slug == 'qwer' or text == 'qwer':
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                'code': tc.DATA_ALREADY_EXIST_111,
                'message': tc.get_reason_phrase(tc.DATA_ALREADY_EXIST_111),
                'detail': {}
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'code': sc.OK,
                'message': '新建term成功',
                'detail': {}
            }
        )


@router.put("/mock/terms/mgr_term")
async def mgr_term_change(
        request_params: dict,
):
    """
    管理员term修改
    """

    if request_params['term_id'] == 'qwer':
        return JSONResponse(
            status_code=sc.OK,
            content={
                'code': sc.OK,
                'message': "管理员term修改成功",
                'detail': {}
            })
    else:
        return JSONResponse(
            status_code=sc.CONFLICT,
            content={
                'code': tc.DATA_ALREADY_EXIST_111,
                'message': tc.get_reason_phrase(tc.DATA_ALREADY_EXIST_111),
                'detail': {},
            }
        )


@router.delete("/mock/terms/mgr_term")
async def mgr_term_delete(
        term_id: str = Query(...)
):
    """
    管理员term删除
    """
    if term_id == 'qwer':
        return JSONResponse(
            status_code=sc.OK,
            content={
                'code': sc.OK,
                'message': '管理员term删除成功',
                'detail': {}
            }
        )
    else:
        return JSONResponse(
            status_code=sc.NOT_FOUND,
            content={
                'code': tc.DATA_NOT_FOUND_109,
                'message': tc.get_reason_phrase(tc.DATA_NOT_FOUND_109),
                'detail': {}
            }
        )


@router.put("/mock/contents/contents_delete")
async def mock_mgr_content_delete(
        # content_id: Query(...)
        request_params: dict
):
    """mock 管理员内容删除"""
    item = {
        "code": tc.SUCCESS,
        "message": tc.get_reason_phrase(tc.SUCCESS),
        "detail": {}
    }
    if request_params['conditions']['content_id'] == "no_exist":
        item = {
            'code': tc.DATA_NOT_FOUND_109,
            'message': tc.get_reason_phrase(tc.DATA_NOT_FOUND_109),
            'detail': ''
        }
        return JSONResponse(status_code=sc.NOT_FOUND,
                            content=item)
    return JSONResponse(status_code=sc.OK,
                        content=item)


@router.get("/mock/contents/content_detail")
async def mock_mgr_content_detail(
        record_id: str = Query(...)
):
    """mock 管理员内容详细"""
    item = {
        "status": "success",
        "detail": {
            "content_id": "1111",
            "record_id": "22222",
            "product_type": "any_share_cloud",
            "content_name": "平行世界",
            "publisher": "维度",
            "description": "dark",
            "content_type": "solution",
            "version": "1",
            "product_info": "对称世界",
            "logo_url": "1",
            "thumbnail_url": "1",
            "preview_media_urls": {
                "image_urls": [
                    "www.qiu.com"
                ],
                "video_urls": [
                    "www.1%.com"
                ]
            },
            "support_info": {
                "email": "user@example.com",
                "phone": "15076523453"
            },
            "file_list": [
                {
                    "file_name": "全能李德胜",
                    "file_id": "moi"
                },
                {
                    "file_name": "少年李德胜",
                    "file_id": "fin"
                }
            ]
        }
    }
    if record_id == "no_exist":
        item = {
            'code': tc.DATA_NOT_FOUND_109,
            'message': tc.get_reason_phrase(tc.DATA_NOT_FOUND_109),
            'detail': ''
        }
        return JSONResponse(status_code=sc.NOT_FOUND,
                            content=item)

    return JSONResponse(status_code=s.HTTP_200_OK, content=item)


@router.post("/mock/contents/release")
async def mock_mgr_content_release(
        request_params: dict
):
    """mock 管理员内容发布"""
    item = {
        "code": 100,
        "message": "success",
        "detail": {}
    }
    if request_params['tag_id_list'] == ['no_exist'] or \
            request_params["group_id_list"] == ['no_exist'] or \
            request_params['file_id_list'] == ['no_exist']:
        item = {
            "code": tc.VALIDATION_102_ERROR,
            "message": tc.get_reason_phrase(tc.VALIDATION_102_ERROR),
            "detail": {}
        }
        return JSONResponse(status_code=sc.BAD_REQUEST, content=item)

    if request_params['content_name'] == "the_same_name" and \
            request_params['content_id'] == "different_id":
        item = {
            "code": 111,
            "message": "Data Already Exist",
            "detail": {}
        }
        return JSONResponse(status_code=sc.CONFLICT, content=item)

    return JSONResponse(status_code=s.HTTP_200_OK,
                        content=item)


@router.put("/mock/contents/contents_status")
async def mock_mgr_content_status_update(request_params: dict):
    """mock 管理员内容状态更新"""
    item = {
        "code": 100,
        "message": "success",
        "detail": {}
    }
    if request_params['conditions']['content_id'] == "no_exist" or \
            request_params['conditions']['status'] == "no_exist":
        item = {
            'code': tc.DATA_NOT_FOUND_109,
            'message': tc.get_reason_phrase(tc.DATA_NOT_FOUND_109),
            'detail': ''
        }
        return JSONResponse(status_code=sc.NOT_FOUND,
                            content=item)

    return JSONResponse(status_code=sc.OK, content=item)


@router.get("/mock/contents/contents_list")
async def mgr_contents_list():
    """mock 管理员内容一览"""
    item = {
        "status": "success",
        "detail": {
            "count": 1,
            "contents": [
                {
                    "product_type": "any_share_cloud",
                    "content_id": "1111",
                    "record_id": "22222",
                    "content_name": "平行世界",
                    "content_type": "solution",
                    "publisher": "string",
                    "status": "cancel",
                    "release_date": "2020-06-01T17:33:34",
                    "release_manager": "长沙李德胜",
                    "cancel_date": "2020-07-01T14:05:30.152408",
                    "cancel_manager": "AZivbi9Z3MXbjnQi5xvR6Q",
                    "count": 0
                },
            ]},

    }
    return JSONResponse(status_code=s.HTTP_200_OK, content=item)


@router.get("/mock/contents/drafts_list")
async def mgr_drafts_list():
    """mock 管理员草稿一览"""
    item = {
        "status": "success",
        "detail": {
            "count": 1,
            "contents": [
                {
                    "product_type": "any_share_cloud",
                    "content_id": "alive",
                    "record_id": "d869eada-3bf8-45d2-"
                                 "f023a54c4183-2020-07-06:13:15:07",
                    "content_name": "月半李德胜",
                    "content_type": "application",
                    "publisher": "三和大神",
                    "created_date": "2020-07-06T13:15:07.836985"
                }
            ]},

    }
    return JSONResponse(status_code=s.HTTP_200_OK, content=item)


@router.post("/mock/draft/save")
async def mgr_draft_save(request_params: dict):
    """mock 管理员草稿保存"""
    item = {
        "code": 100,
        "message": "success",
        "detail": {}
    }
    if request_params['tag_id_list'] == ['no_exist'] or \
            request_params["group_id_list"] == ['no_exist'] or \
            request_params['file_id_list'] == ['no_exist']:
        item = {
            "code": tc.VALIDATION_102_ERROR,
            "message": tc.get_reason_phrase(tc.VALIDATION_102_ERROR),
            "detail": {}
        }
        return JSONResponse(status_code=sc.BAD_REQUEST, content=item)

    if request_params['content_name'] == "the_same_name" and \
            request_params['content_id'] == "different_id":
        item = {
            "code": 111,
            "message": "Data Already Exist",
            "detail": {}
        }
        return JSONResponse(status_code=sc.CONFLICT, content=item)
    return JSONResponse(status_code=s.HTTP_200_OK,
                        content=item)


@router.get("/mock/term/term_list_get")
async def get_term_list():
    """mock term一览"""
    item = {
        "status": "success",
        "term_type": "group",
        "detail": {
            "count": 2,
            "terms": [
                {
                    "term_id": "280904070346409f8220aa676e1a2b5b",
                    "slug": "fsfdsfsf",
                    "text": "dfsfsf",
                    "description": "sfdsfsf",
                    "product_type": "any_backup_cloud",
                    "content_type": "application"
                },
                {
                    "term_id": "2",
                    "slug": "gg",
                    "text": "ys",
                    "description": "sql77777",
                    "product_type": "any_share_cloud",
                    "content_type": "application"
                }
            ]},
        "count": 2
    }
    return JSONResponse(status_code=s.HTTP_200_OK,
                        content=item)
