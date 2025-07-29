from abc import ABC, abstractmethod
from schemas.models import TokenPayload, TokenResponse


class TokenPort(ABC):
    
    
    @abstractmethod
    def create_access_token(self, user_id:str)->TokenResponse: 
        ...
        
    @abstractmethod
    def create_refresh_token(self, user_id:str)->TokenResponse: 
        ...
        
    @abstractmethod
    def verify_access_token(self, jwt_str:str)->TokenPayload: 
        ...
        
    @abstractmethod
    def verify_refresh_token(self, jwt_str:str)->TokenPayload: 
        ...
    
    @abstractmethod
    def invalidate_refresh_token(self, jwt_str:str)->bool: 
        ### 토큰 삭제
        ...
    
    
    