from fastapi import FastAPI

from infra.redis_service_impl import service_redis
from src.application.middleware.cors import CustomCORSMiddleware
from src.application.api.register_api import register_api_routes
from src.application.settings import settings
from src.application.logger_settings import logging_setup


def create_app():
    logging_setup(settings=settings)

    app = FastAPI(
        title=settings.TITLE,
        docs_url=f"{settings.GLOBAL_PREFIX_URL}/docs",
        openapi_url=f"{settings.GLOBAL_PREFIX_URL}/openapi.json",
        redoc_url=f"{settings.GLOBAL_PREFIX_URL}/redoc",
        debug=settings.DEBUG,
    )

    service_redis.configure(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db_number=settings.REDIS_DB_NUMBER,
    )

    # middleware
    app.add_middleware(
        CustomCORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
        allow_credentials=settings.CORS_CREDENTIALS,
        max_age=settings.CORS_MAX_AGE,
    )

    # routes
    register_api_routes(
        app=app,
        prefix=settings.GLOBAL_PREFIX_URL,
    )

    return app
