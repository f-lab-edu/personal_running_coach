import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool

from ports.account_port import AccountPort
from schemas.models import AccountResponse, AccountRequest
from infra.db.orm.models import User
from infra.db.storage import repo
from config.logger import get_logger


logger = get_logger(__name__)

class AccountAdapter(AccountPort):
    def __init__(self,db:AsyncSession):
        self.db = db
        
    # bcrypt = 단방향 해시
    # 비밀번호 해시 후 솔트와 함께 저장.
    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    # 확인시 checkpw 로 암호문 비교 체크
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    async def create_account(self, email: str, pwd: str, name: str) -> AccountResponse:
        try:
            # Check if user already exists
            user = await repo.get_user_by_email(email=email, db=self.db)
            if user:
                raise HTTPException(status_code=400, detail="Email already exist")
            
            # Hash password
            hashed_password = await run_in_threadpool(self._hash_password, pwd)
            
            # Create new user
            new_user = User(
                email=email,
                hashed_pwd=hashed_password,
                name=name
            )
            
            await repo.add_user(new_user, self.db)
            
            return AccountResponse(
                id=new_user.id,
                email=new_user.email,
                name=new_user.name
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error {e}")
        
    async def get_account(self, email: str) -> AccountResponse:
        try:
            
            # Get user from database
            user = await repo.get_user_by_email(email=email, db=self.db)
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
        
    async def login_account(self, email: str, pwd: str) -> AccountResponse:
        try:
            # Find user by email
            user = await repo.get_user_by_email(email=email, db=self.db)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid email or password")
            
            # Verify password
            is_valid = await run_in_threadpool(self._verify_password, pwd, user.hashed_pwd )
            if not is_valid:
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
            raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")
        
    async def update_account(self, email: str, pwd: str, name: str) -> None:
        try:
            # Get user from database
            user = await repo.get_user_by_email(email=email, db=self.db)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            

           ## update
            if name is not None:
                user.name = name
            if pwd is not None:
                user.hashed_pwd = await run_in_threadpool(self._hash_password, pwd)
            
            await repo.update_user(user=user, db=self.db)

        except HTTPException:
            raise
        except Exception as e:
            logger.exception(str(e))
            raise HTTPException(status_code=500, detail="Internal server error")
        
    # https://blog.neonkid.xyz/262
    async def oauth_google(self, auth_code:str)->AccountResponse : 
        ...
        
    async def deactivate_account(self, email: str) -> bool:
        """계정 삭제"""
        try:
            # Find user by email
            user = await repo.get_user_by_email(email=email, db=self.db)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            #TODO: delete token  cascade??
            
            #TODO: delete sns connect
            
            # TODO: delete train session
            
            # Delete user
            await repo.delete_user(user=user, db=self.db)
            
            return True
        
        except HTTPException:
            raise
        except Exception as e:
            logger.exception(str(e))
            raise HTTPException(status_code=500, detail="Internal server error")
        