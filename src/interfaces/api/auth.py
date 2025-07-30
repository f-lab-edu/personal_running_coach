from fastapi import APIRouter
from schemas.models import TokenResponse
from interfaces.api.auth_google import google_router

router = APIRouter(prefix="/auth")
router.include_router(google_router)


@router.post("/login", response_model=TokenResponse)
async def login(email:str, pwd:str):
    
    return

@router.post("/signup")
async def signup(email:str, pwd:str):
    
    return
    

@router.post("/refresh-token", response_model=TokenResponse)
async def login(email:str, pwd:str):
    # TODO: 리프레시 토큰 검증 후 새토큰 발급
    return
    