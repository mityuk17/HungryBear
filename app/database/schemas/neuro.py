from database.base import Base
from sqlalchemy import Column, BigInteger, ForeignKey
from sqlmodel import Field



class GPTMessage(Base):
    role: str
    text: str
    

class Prompt(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    text: str
    active: bool = Field(default=True)