from database.schemas.neuro import Prompt
from database.base import get_session
from sqlmodel import select


async def create_prompt(prompt_data: Prompt) -> Prompt:
    session = await get_session()
    
    session.add(prompt_data)
    await session.commit()
    await session.refresh(prompt_data)
    await session.close()
    
    return prompt_data


async def get_prompt(prompt_id: int) -> Prompt | None:
    session = await get_session()
    
    statement = select(Prompt).where(Prompt.id == prompt_id)
    result = await session.exec(statement)
    prompt = result.one_or_none()
    await session.close()
    
    return prompt


async def update_prompt(prompt_data: Prompt) -> Prompt:
    session = await get_session()
    
    session.add(prompt_data)
    await session.commit()
    await session.refresh(prompt_data)
    await session.close()
    
    return prompt_data


async def all_prompts() -> list[Prompt]:
    session = await get_session()
    
    statement = select(Prompt).where(Prompt.active == True)
    result = await session.exec(statement)
    prompts = result.all()
    await session.close()
    
    return prompts
