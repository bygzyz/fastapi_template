# -*- coding: UTF-8 -*-
from pydantic import BaseModel, PositiveInt
from typing import Union, Dict, Any


class Message(BaseModel):
    code: int
    message: str


class MessageModel(BaseModel):
    code: PositiveInt = None
    message: str = None
    detail: Union[Dict, Any] = None
