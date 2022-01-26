from pydantic import BaseModel
from typing import List, Type, Dict, Tuple, Any
from app.core._errors import HTTPAPIException
from app.core._status_code import StatuCode, TraceCode


class ResponseSchemaBuilder:

    @classmethod
    def schema_from_model(cls, model: Type[BaseModel],
                          status_code: StatuCode = StatuCode.OK) -> dict:
        return dict({
            "description": StatuCode.get_reason_phrase(status_code),
            "content": {
                "application/json": {
                    "schema": model.schema()
                }
            }
        }
        )

    @classmethod
    def schema_from_config(cls, config: Dict[str, List[Any]]) -> dict:
        result_dict = dict()
        result_dict = {**result_dict,
                       **ResponseSchemaBuilder.schema_from_models(
                           config["responses"])}
        result_dict = {**result_dict,
                       **ResponseSchemaBuilder.schema_from_models(
                           config["errors"])}
        return result_dict

    @classmethod
    def schema_from_models(
            cls,
            models: List[Tuple[StatuCode, Type[BaseModel]]]
    ) -> dict:
        resps_dict = dict()
        for (sc, model) in models:
            resps_dict[sc.value] = cls.schema_from_model(model)
        return resps_dict

    @classmethod
    def schema_from_errors(
            cls,
            errors: List[Tuple[StatuCode, TraceCode]]
    ) -> dict:
        resps_dict = dict()
        for (sc, tc) in errors:
            resps_dict[sc.value] = HTTPAPIException.schema_from_code(sc, tc)
        return resps_dict


def ResponseSchema(sc: StatuCode, model: Type[BaseModel]) -> Tuple[str, Any]:
    return sc.value, ResponseSchemaBuilder.schema_from_model(model)


def ResponseErrorSchema(sc: StatuCode, tc: TraceCode) -> Tuple[str, Any]:
    return sc.value, HTTPAPIException.schema_from_code(sc, tc)
