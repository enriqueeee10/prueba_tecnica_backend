from fastapi import APIRouter, HTTPException, Depends, status
from dependency_injector.wiring import inject, Provide

from app.contexts.users.infrastructure.api.schemas import (
    CreateUserRequest,
    CreateUserResponse,
    UserResponse,
    ErrorResponse,
)
from app.contexts.users.application.commands.create_user_command import (
    CreateUserCommand,
)
from app.contexts.users.application.commands.create_user_handler import (
    CreateUserHandler,
)
from app.contexts.users.application.queries.get_user_query import GetUserQuery
from app.contexts.users.application.queries.get_user_handler import GetUserHandler
from app.shared.domain.exceptions import (
    DomainException,
    NotFoundError,
    DuplicateError,
    ValidationError,
)
from app.config.container import Container

router = APIRouter()


@router.post(
    "/", response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED
)
@inject
async def create_user(
    request: CreateUserRequest,
    handler: CreateUserHandler = Depends(Provide[Container.create_user_handler]),
):
    try:
        command = CreateUserCommand(
            name=request.name, email=request.email, password=request.password
        )

        user_id = await handler.handle(command)

        return CreateUserResponse(user_id=user_id, message="User created successfully")

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DuplicateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
@inject
async def get_user(
    user_id: str, handler: GetUserHandler = Depends(Provide[Container.get_user_handler])
):
    try:
        query = GetUserQuery(user_id=user_id)
        user = await handler.handle(query)

        return UserResponse(
            user_id=user.user_id.value,
            name=user.name,
            email=user.email.value,
            is_active=user.is_active,
        )

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
