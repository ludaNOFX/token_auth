from fastapi import FastAPI
from src.application.api.endpoints.healthcheck import hc


routes = [
    hc.router,
]


def register_api_routes(app: FastAPI, prefix: str):
    for route in routes:
        app.include_router(route, prefix=prefix)
    return app.routes
