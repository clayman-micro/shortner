from datetime import datetime

from aiohttp import web
from aiohttp_metrics import setup as setup_metrics  # type: ignore
from aiohttp_micro import AppConfig, setup as setup_micro
from aiohttp_openapi import (
    JSONResponse,
    Parameter,
    ParameterIn,
    register_operation,
    RequestBody,
    setup as setup_openapi,
)
from marshmallow import fields, Schema


class ShortURLPayloadSchema(Schema):
    origin = fields.Str(description="Origin URL")
    disposable = fields.Bool(
        missing=False, description="Short URL should be disposable"
    )


class ShortURLSchema(Schema):
    key = fields.Int(data_key="id", dump_only=True)
    url = fields.Str(description="Short URL")
    disposable = fields.Bool(default=False)
    created = fields.DateTime(
        dump_only=True,
        default=datetime.utcnow,
        doc_default="The current datetime",
    )


class AddResponseSchema(Schema):
    short_url = fields.Nested(ShortURLSchema, data_key="shortURL")


class FetchResponseSchema(Schema):
    short_urls = fields.List(
        fields.Nested(ShortURLSchema), data_key="shortURLs"
    )


RequestIDParameter = Parameter(
    in_=ParameterIn.header,
    name="X-Request-ID",
    schema={"type": "string", "format": "uuid"},
    required=True,
)


@register_operation(
    description="Get short URLs list",
    parameters=(RequestIDParameter,),
    responses=(
        JSONResponse(
            description="Collection of short urls", schema=FetchResponseSchema
        ),
    ),
)
async def fetch_short_urls(request: web.Request) -> web.Response:
    return web.Response(status=200)


@register_operation(
    description="Get short URLs list",
    parameters=(RequestIDParameter,),
    request_body=RequestBody(
        description="Add short URL for origin", schema=ShortURLPayloadSchema
    ),
    responses=(
        JSONResponse(
            description="New short URL added",
            schema=AddResponseSchema,
            status_code=201,
        ),
    ),
)
async def add_short_url(request: web.Request) -> web.Response:
    return web.Response(status=200)


def init(app_name: str, config: AppConfig) -> web.Application:
    app = web.Application()

    setup_micro(app, app_name=app_name, config=config)
    setup_metrics(app)

    app.router.add_post("/api/short", add_short_url, name="api.add_short_url")
    app.router.add_get(
        "/api/short", fetch_short_urls, name="api.fetch_short_urls"
    )

    setup_openapi(
        app,
        title="Shortner",
        version=app["distribution"].version,
        description="Shortner service API",
    )

    return app
