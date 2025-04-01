from fastapi import FastAPI
from src.application.api.endpoints.healthcheck import hc
from src.application.api.endpoints.users import users
from src.application.api.endpoints.roles import roles


routes = [hc.router, users.router, roles.router]


def register_api_routes(app: FastAPI, prefix: str):
    for route in routes:
        app.include_router(route, prefix=prefix)
    return app.routes
