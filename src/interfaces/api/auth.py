from fastapi import APIRouter
from schemas.models import TokenResponse


router = APIRouter(prefix="/auth")



@router.post("/login", response_model=TokenResponse)
async def login(email:str, pwd:str):
    
    return

@router.post("/signup")
async def signup(email:str, pwd:str):
    
    return

@router.get("/oauth/google", response_model=TokenResponse)
async def login(email:str, pwd:str):
    
    return
    

@router.post("/refresh-token", response_model=TokenResponse)
async def login(email:str, pwd:str):
    # TODO: 리프레시 토큰 검증 후 새토큰 발급
    return
    