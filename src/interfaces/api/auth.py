from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infra.db.storage.session import get_session
from interfaces.api.auth_google import google_router
from schemas.models import TokenResponse, AccountRequest

from use_cases.auth.auth import AuthHandler
from adapters.account_adapter import AccountAdapter
from adapters.token_adapter import TokenAdapter
from config import constants

router = APIRouter(prefix="/auth", tags=['auth'])
router.include_router(google_router, tags=None)

def get_auth_handler(db:AsyncSession=Depends(get_session))->AuthHandler:
    return AuthHandler(
        account_adapter=AccountAdapter(db),
        token_adapter=TokenAdapter(
            access_token_exp=constants.ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_token_exp=constants.REFRESH_TOKEN_EXPIRE_DAYS
            ),
    )
    


@router.post("/login", response_model=TokenResponse)
async def login(request:AccountRequest, 
                auth_handler:AuthHandler=Depends(get_auth_handler)
                ):
    """로그인.
        parameter: Body(email, pwd)
        return: payload (access, refresh, exp ...)
    """
    
    token_response = await auth_handler.login(request.email, request.pwd)
    return token_response


@router.post("/signup")
async def signup(request:AccountRequest,
                 auth_handler:AuthHandler=Depends(get_auth_handler))->bool:
    """회원가입.
        parameter: Body(email, pwd, name)
        return: 회원가입 성공여부 (bool)
    """
    return await auth_handler.signup(request.email, request.pwd, request.name)
    
    

@router.post("/refresh-token", response_model=TokenResponse)
async def refresh(email:str, pwd:str,
                auth_handler:AuthHandler=Depends(get_auth_handler)):
    # TODO: 리프레시 토큰 검증 후 새토큰 발급
    return
    