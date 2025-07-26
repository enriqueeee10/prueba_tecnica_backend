from fastapi import APIRouter, HTTPException, Depends, status
from dependency_injector.wiring import inject, Provide

from app.contexts.auth.infrastructure.api.schemas import (
    LoginRequest,
    LoginResponse,
    ValidateTokenRequest,
    ValidateTokenResponse,
)
from app.contexts.auth.application.commands.login_command import LoginCommand
from app.contexts.auth.application.commands.login_handler import LoginHandler
from app.contexts.auth.application.queries.validate_token_query import (
    ValidateTokenQuery,
)
from app.contexts.auth.application.queries.validate_token_handler import (
    ValidateTokenHandler,
)
from app.shared.domain.exceptions import DomainException, NotFoundError, ValidationError
from app.config.container import Container

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
@inject
async def login(
    request: LoginRequest,
    handler: LoginHandler = Depends(Provide[Container.login_handler]),
):
    try:
        command = LoginCommand(email=request.email, password=request.password)

        result = await handler.handle(command)

        return LoginResponse(**result)

    except (NotFoundError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/validate", response_model=ValidateTokenResponse)
@inject
async def validate_token(
    request: ValidateTokenRequest,
    handler: ValidateTokenHandler = Depends(Provide[Container.validate_token_handler]),
):
    try:
        query = ValidateTokenQuery(token=request.token)
        result = await handler.handle(query)

        return ValidateTokenResponse(**result)

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
