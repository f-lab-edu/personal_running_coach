from fastapi import HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import httpx

from config.settings import google
from config.logger import get_logger
from adapters.account_adapter import AccountAdapter


logger = get_logger(__file__)

# google_auth_oauthlib, google_oauth2 등 라이브러리 사용
# https://developers.google.com/identity/protocols/oauth2?hl=ko
# https://ahn3330.tistory.com/166
# https://m.blog.naver.com/nan17a/222182983858


class GoogleHandler:
    """
    구글 핸들러.

    """
    def __init__(self, account_adapter:AccountAdapter):
        self.token_url = google.token_url
        self.account_adapter = account_adapter
    
    
    async def _get_access_token(self, code:str)->dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    "code": code,
                    "client_id": google.client_id,
                    "client_secret": google.client_secret,
                    "redirect_uri": google.redirect_uri,
                    "grant_type": "authorization_code"
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code for token")
        
        return response.json()
    
    
    
    
    async def handle_login(self, auth_code:str):
        """
        구글 authorization code 를 받아 엑세스 토큰 요청.
        엑세스 토큰 (json) 에서 id_token 추출.
        
        토큰 반환
        """
        
         # 1. access token 요청
        token_response = await self._get_access_token(auth_code)
        id_token_jwt = token_response.get("id_token")
        access_token = token_response.get("access_token")

        
        
        # 2. ID 토큰 검증 및 사용자 정보 파싱
        try:
            id_info = id_token.verify_oauth2_token(
                id_token_jwt,
                google_requests.Request(),
                google.client_id
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid ID token: {str(e)}")

        email = id_info.get("email")
        sub = id_info.get("sub")  # 구글 고유 사용자 ID
        print("idinfo",id_info)
        # token = await self.account_adapter.login_by_google(email=email, google_sub=sub)

        return id_info

    
