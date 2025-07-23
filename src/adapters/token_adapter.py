from ports.token_port import *


class TokenAdapter(TokenPort):
    
    def create_access_token(self, user_id:str)->str: 
        ...

    def create_refresh_token(self, user_id:str)->str: 
        ...

    def verify_access_token(self, token:str)->dict: 
        ...

    def verify_refresh_token(self, token:str)->dict: 
        ...
        
    ### 토큰 삭제
    def invalidate_refresh_token(self, token:str)->dict: 
        ...
    
    
    