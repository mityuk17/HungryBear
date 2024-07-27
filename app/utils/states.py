from aiogram.fsm.state import StatesGroup, State


class General(StatesGroup):
    get_amount_for_deposit = State()
    