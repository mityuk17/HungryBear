from database.base import get_session
from database.schemas.general import Payment
from sqlmodel import select


async def create_payment(payment_data : Payment) -> Payment:
    session = await get_session()
    
    session.add(payment_data)
    await session.commit()
    await session.refresh(payment_data)
    await session.close()
    
    return payment_data


async def get_payment(payment_id: int) -> Payment | None:
    session = await get_session()
    
    statement = select(Payment).where(Payment.id == payment_id)
    result = await session.exec(statement)
    payment = result.one_or_none()
    await session.close()
    
    return payment


async def update_payment(payment_data: Payment) -> Payment:
    session = await get_session()
    
    session.add(payment_data)
    await session.commit()
    await session.refresh(payment_data)
    await session.close()
    
    return payment_data