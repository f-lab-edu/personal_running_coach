import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends

from ports.account_port import AccountPort
from schemas.models import AccountResponse, AccountUpdateRequest
from infra.db.orm.models import User
from infra.db.storage import repo
from infra.db.storage.session import get_session
from config.logger import get_logger
from config import constants


logger = get_logger(__name__)

class AccountAdapter(AccountPort):
    def __init__(self):
        pass
        
    # bcrypt = 단방향 해시
    # 비밀번호 해시 후 솔트와 함께 저장.
    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    # 확인시 checkpw 로 암호문 비교 체크
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    async def create_account(self, email: str, pwd: str, name: str, 
                             db: AsyncSession = Depends(get_session)) -> AccountResponse:
        try:
            # Check if user already exists
            user = await repo.get_user_by_email(email=email, db=db)
            if user:
                raise HTTPException(status_code=400, detail="Email already exist")
            
            # Hash password
            hashed_password = self._hash_password(pwd)
            
            # Create new user
            new_user = User(
                email=email,
                hashed_pwd=hashed_password,
                name=name
            )
            
            await repo.add_user(new_user, db)
            
            return AccountResponse(
                id=new_user.id,
                email=new_user.email,
                name=new_user.name
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.exception(str(e))
            raise HTTPException(status_code=500, detail="Internal server error")
        
    async def get_account(self, email: str, db: AsyncSession = Depends(get_session)) -> AccountResponse:
        try:
            
            # Get user from database
            user = await repo.get_user_by_email(email=email, db=db)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            return AccountResponse(
                id=user.id,
                email=user.email,
                name=user.name
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.exception(f"Error getting account: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        
    async def login_account(self, email: str, pwd: str, db: AsyncSession = Depends(get_session)) -> AccountResponse:
        try:
            # Find user by email
            user = await repo.get_user_by_email(email=email, db=db)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid email or password")
            
            # Verify password
            if not self._verify_password(pwd, user.hashed_pwd):
                raise HTTPException(status_code=401, detail="Invalid email or password")
            
            return AccountResponse(
                id=user.id,
                email=user.email,
                name=user.name
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.exception(str(e))
            raise HTTPException(status_code=500, detail="Internal server error")
        
    async def update_account(self, email: str, 
                             acct_request: AccountUpdateRequest, 
                             db: AsyncSession = Depends(get_session)) -> None:
        try:
            # Get user from database
            user = await repo.get_user_by_email(email=email, db=db)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            

           ## update
            if acct_request.name is not None:
                user.name = acct_request.name
            if acct_request.pwd is not None:
                user.hashed_pwd = self._hash_password(acct_request.pwd)
            
            await repo.update_user(user=user, db=db)
            
            
        except HTTPException:
            raise
        except Exception as e:
            logger.exception(str(e))
            raise HTTPException(status_code=500, detail="Internal server error")
        
    # https://blog.neonkid.xyz/262
    async def oauth_google(self, auth_code:str)->AccountResponse : 
        ...
        
    async def deactivate_account(self, email: str, db: AsyncSession = Depends(get_session)) -> bool:
        """계정 삭제"""
        try:
            # Find user by email
            user = await repo.get_user_by_email(email=email, db=db)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            #TODO: delete token  cascade??
            
            #TODO: delete sns connect
            
            # TODO: delete train session
            
            # Delete user
            await repo.delete_user(user=user, db=db)
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.exception(str(e))
            raise HTTPException(status_code=500, detail="Internal server error")
        