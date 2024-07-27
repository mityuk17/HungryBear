from database.base import get_session
from database.schemas.general import Tool
from sqlmodel import select


async def create_tool(tool_data: Tool) -> Tool:
    session = await get_session()
    
    session.add(tool_data)
    await session.commit()
    await session.refresh(tool_data)
    await session.close()
    
    return tool_data


async def get_tool(tool_id: int) -> Tool | None:
    session = await get_session()
    
    statement = select(Tool).where(Tool.id == tool_id)
    result = await session.execute(statement)
    tool = result.one_or_none()
    await session.close()
    
    return tool


async def update_tool(tool_data: Tool) -> Tool:
    session = await get_session()
    
    session.add(tool_data)
    await session.commit()
    await session.refresh(tool_data)
    await session.close()
    
    return tool_data


async def active_tools() -> list[Tool]:
    session = await get_session()
    
    statement = select(Tool).where(Tool.active == True)
    result = await session.exec(statement)
    tools = result.all()
    await session.close()
    
    return tools
    