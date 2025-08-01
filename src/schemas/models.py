from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID



class TokenPayload(BaseModel):  ## jwt payload 용
    user_id:UUID
    exp:int
    issued_at:int
    token_type:str = 'access'  # or "refresh"
    

# 응답모델
class TokenResponse(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type:str = "bearer "
    exp:int

class AccountResponse(BaseModel):
    id:UUID
    email:EmailStr
    name:str
    sns:Optional[str] = None
    

#입력모델
class AccountRequest(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    pwd: Optional[str] = None  # 평문 비밀번호 (입력용)


class TrainSession(BaseModel):
    session_id:str
    created_at:datetime
    distance:float
    stream_data:dict  ## TODO heartrate,watts,
    
    
class TrainGoal(BaseModel):
    user_id:UUID
    goal:str
    target_date:datetime
    created_at:datetime
    
class CoachAdvice(BaseModel):
    user_id:UUID
    created_at:datetime
    advice:str
    
    