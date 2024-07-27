from database.base import Base

from sqlalchemy import Column, BigInteger, ForeignKey
from sqlmodel import Field
from datetime import datetime


class Tarif:
    Free = "Базовая"
    Advanced = "Продвинутая"
    
    @classmethod
    def price(cls, tarif: str):
        match tarif:
            case cls.Free:
                return 0
            case cls.Advanced:
                return 49


class PaymentStatus:
    Created = "Создан"
    Succeded = "Произведён"
    Cancelled = "Отменён"
    


class User(Base, table=True):
    id: int = Field(sa_column=Column(BigInteger(), primary_key=True))
    username: str | None
    name: str | None
    balance: int = Field(default=0)
    subsctiption_endtime: datetime | None = Field(default=None)
    tarif: str | None = Field(default=Tarif.Free)
    auto_renewal: bool = Field(default=True)
    last_activity: datetime = Field(default=datetime.now())
    created_at: datetime = Field(default=datetime.now())
    
    def active_subscription(self) -> str:
        if not(self.subsctiption_endtime):
            return Tarif.Free
        if datetime.today() < self.subsctiption_endtime:
            return self.tarif
        else:
            return Tarif.Free
    

class Tool(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    active: bool = Field(default=True)


class Payment(Base, table=True):
    id: int | None = Field(default = None, primary_key=True)
    user_id: int = Field(sa_column=Column(BigInteger(), ForeignKey("user.id")))
    amount: int = Field(gt=0)
    status: str = Field(default=PaymentStatus.Created)
    created_at: datetime = Field(default=datetime.now())
    