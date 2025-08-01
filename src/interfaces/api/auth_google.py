from fastapi import APIRouter, Request, HTTPException
from starlette.responses import RedirectResponse
import urllib.parse

from use_cases.auth import oauth_google
from config.settings import google

google_router = APIRouter(prefix="/google")

google_handler = oauth_google.GoogleHandler()

@google_router.get("/login")
async def login_with_google():
    params = {
        "client_id": google.client_id,
        "redirect_uri": google.redirect_uri,
        "response_type": "code", 
        "scope": google.scope,
        "access_type": "offline",  # online 
        "prompt": "consent",
    }
    url = f"{google.auth_endpoint}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)


@google_router.get("/callback")
async def google_callback(request:Request):
    # get return code from google login
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="missing code")
    
    
    token = await google_handler.handle_login(auth_code=code)
    

    

    return token