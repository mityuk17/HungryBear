from database.base import get_session
from database.schemas.general import User
from sqlmodel import select
from datetime import datetime


async def create_user(user_data : User) -> User:
    session = await get_session()
    
    session.add(user_data)
    await session.commit()
    await session.refresh(user_data)
    await session.close()
    
    return user_data


async def get_user(user_id: int) -> User | None:
    session = await get_session()
    
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)
    user = result.one_or_none()
    await session.close()
    
    return user


async def update_user(user_data: User) -> User:
    session = await get_session()
    
    session.add(user_data)
    await session.commit()
    await session.refresh(user_data)
    await session.close()
    
    return user_data


async def users_with_subscription() -> list[User]:
    session = await get_session()
    
    statement = select(User).where(User.subsctiption_endtime > datetime.today())
    result = await session.exec(statement)
    users = result.all()
    await session.close()
    
    return users