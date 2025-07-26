from fastapi import FastAPI
from dependency_injector.wiring import inject, Provide

from app.config.settings import settings
from app.config.container import Container
from app.contexts.users.infrastructure.api.routes import router as users_router
from app.contexts.auth.infrastructure.api.routes import router as auth_router


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(
        title=settings.API_TITLE, version=settings.API_VERSION, debug=settings.DEBUG
    )

    app.container = container
    app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

    return app


app = create_app()

# Wire the container
app.container.wire(
    modules=[
        "app.contexts.users.infrastructure.api.routes",
        "app.contexts.auth.infrastructure.api.routes",
    ]
)


@app.get("/")
async def root():
    return {"message": "Hexagonal Architecture API with CQRS"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
