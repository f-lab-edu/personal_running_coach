from adapters.account_adapter import AccountAdapter
from adapters.token_adapter import TokenAdapter
from schemas.models import TokenResponse, AccountResponse
from config.logger import get_logger

logger = get_logger(__file__)

class AuthHandler():
    """
    검증 핸들러.
    """
    def __init__(self, 
                 account_adapter:AccountAdapter, 
                 token_adapter:TokenAdapter,
                 ):
        self.account_adapter = account_adapter
        self.token_adapter = token_adapter
    
    
    async def login(self, email:str, pwd:str)->TokenResponse:
        """
        수동로그인 
        (아이디,비밀번호 미스매치) 실패시 401 에러
        """

        try:
            res = await self.account_adapter.login_account(email, pwd)
        except Exception as e:
            logger.exception(str(e))
            raise
        else:
            
            token = self.token_adapter.create_access_token(user_id=res.id)
            # TODO refresh 토큰 생성. 같이 리턴.
        return token
    
    async def signup(self, email:str, pwd:str, name:str)->bool:
        """
        회원가입
        """
        try:
            res = await self.account_adapter.create_account(email, pwd, name)
        except Exception as e:
            logger.exception(str(e))
            raise
        
        return True if res else False
