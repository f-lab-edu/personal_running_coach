from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class TokenPayload(BaseModel):  ## jwt payload 용
    user_id:str
    exp:int
    issued_at:int
    token_type:str = 'access'  # or "refresh"
    
    
class TokenResponse(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type:str = "bearer "
    exp:int


class AccountResponse(BaseModel):
    id:int
    email:str
    pwd_hash:str
    name:str
    sns:Optional[str] = None

class TrainSession(BaseModel):
    session_id:str
    created_at:datetime
    distance:float
    stream_data:dict  ## TODO heartrate,watts,
    
    
class TrainGoal(BaseModel):
    user_id:str
    goal:str
    target_date:datetime
    created_at:datetime
    
class CoachAdvice(BaseModel):
    user_id:str
    created_at:datetime
    advice:str
    
    