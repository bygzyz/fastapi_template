import aiohttp
from aiohttp import ClientError


async def request_http(
        method,
        url,
        data=None,
        headers=None
):
    ###
    origin_headers = {'Content-Type': "application/json"}
    ###

    if headers:
        origin_headers.update(headers)
    try:
        async with aiohttp.request(method=method, url=str(url), data=data,
                                   headers=origin_headers) as response:
            status_code = response.status
            responses = await response.text()
            return {
                "status_code": status_code,
                "response": responses
            }

    except ClientError as e:
        status_code = 530
        responses = str(e)
        return {
            "status_code": status_code,
            "response": responses
        }
