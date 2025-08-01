from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from infra.db.orm.models import User

from config.logger import get_logger

logger = get_logger(__name__)


## account
async def get_user_by_email(email: str,
                            db: AsyncSession) -> User | None:
    try:
        res = await db.execute(
            select(User).where(User.email == email)
        )
        return res.scalar_one_or_none()
    except Exception as e:
        logger.exception(str(e))
        raise HTTPException(status_code=400, detail=str(e))

        
async def add_user(user: User,
                   db: AsyncSession) -> None:
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
    except Exception as e:
        logger.exception(str(e))
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


async def update_user(user: User,
                      db: AsyncSession) -> None:
    
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception as e:
        logger.exception(str(e))
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


async def delete_user(user: User,
                      db: AsyncSession) -> None:
    try:
        await db.delete(user)
        await db.commit()
    except Exception as e:
        logger.exception(str(e))
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))




