from abc import ABC, abstractmethod


class TokenPort(ABC):
    
    
    @abstractmethod
    def create_access_token(self, user_id:str)->str:  ## TODO: jwt response. 
        ...
        
    @abstractmethod
    def create_refresh_token(self, user_id:str)->str:  ## TODO: jwt response. 
        ...
        
    @abstractmethod
    def verify_access_token(self, token:str)->dict:  ## TODO: jwt response. 
        ...
        
    @abstractmethod
    def verify_refresh_token(self, token:str)->dict:  ## TODO: jwt response. 
        ...
    
    @abstractmethod
    def invalidate_refresh_token(self, token:str)->dict:  ## TODO: jwt response. 
        ### 토큰 삭제
        ...
    
    
    