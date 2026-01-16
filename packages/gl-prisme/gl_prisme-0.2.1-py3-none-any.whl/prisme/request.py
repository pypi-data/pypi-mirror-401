from base64 import b64encode
from datetime import date, datetime
from typing import TypeVar

from dict2xml import Converter  # type: ignore
from xmltodict import parse as xml_to_dict


class Request[ResponseType]:

    wrap = "Request"
    method: str = "method"

    @classmethod
    def response_class(cls) -> type[ResponseType]:
        raise NotImplementedError("Must be implemented in subclass")  # pragma: no cover

    @staticmethod
    def prepare(
        value: str | datetime | date | bytes | dict | list | None,
    ) -> str | dict | list | None:
        if value is None:
            return ""
        if isinstance(value, datetime):
            value = f"{value:%Y-%m-%dT%H:%M:%S}"
        if isinstance(value, date):
            value = f"{value:%Y-%m-%d}"
        if type(value) is dict:
            return {k: Request.prepare(v) for k, v in value.items()}
        if type(value) is list:
            return [Request.prepare(v) for v in value]
        if type(value) is bytes:
            return b64encode(value).decode("utf-8")
        if value is None:
            return None
        return str(value)

    @property
    def dict(self) -> dict:
        raise NotImplementedError("Must be implemented in subclass")  # pragma: no cover

    autoclose_values = ["", None]

    @property
    def xml(self) -> str:
        return str(
            Converter(wrap=self.wrap, indent="  ", newlines=True).build(
                self.prepare(self.dict), closed_tags_for=self.autoclose_values
            )
        )


RequestType = TypeVar("RequestType", bound=Request)


class Response[RequestType]:
    def __init__(self, request: RequestType, xml: str):
        self.request = request
        self.xml = xml
        self.data: dict = xml_to_dict(xml) if xml is not None else None


ResponseType = TypeVar("ResponseType", bound=Response)
