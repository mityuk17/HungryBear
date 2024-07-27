from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from database.schemas.general import Tool, User, Tarif


def start_menu() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    
    kb_builder.button(text="Сервисы")
    kb_builder.button(text="Профиль")
    kb_builder.button(text="О проекте")
    
    kb_builder.adjust(1, 2)
    
    return kb_builder.as_markup(resize_keyboard=True)


def pick_tool_menu(tools: list[Tool]) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    
    for tool in tools:
        kb_builder.button(text=tool.name, callback_data=f"tool_{tool.id}")
    
    kb_builder.adjust(1, repeat=True)
    
    return kb_builder.as_markup()


def profile() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    
    kb_builder.button(text="$BEAR", callback_data="about-points")
    kb_builder.button(text="Пополнить баланс", callback_data="deposit")
    kb_builder.button(text="Управление подпиской", callback_data="manage-subscription")
    kb_builder.adjust(2, 1)
    
    return kb_builder.as_markup()


def back_to_profile() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    
    kb_builder.button(text="Назад", callback_data="profile")
    
    return kb_builder.as_markup()


def payment_keyboard(amount: int, payment_id: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text=f"Пополнить на {amount} ⭐️", pay=True)
    kb_builder.button(text="Назад", callback_data=f"cancel-payment_{payment_id}")
    
    kb_builder.adjust(1, repeat=True)
    
    return kb_builder.as_markup()



def manage_subscription_menu(user_data: User) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    if user_data.active_subscription() == Tarif.Free:
        kb_builder.button(text="Оформить продвинутую подписку | 49 $BEAR", callback_data=f"buy-subscription_{Tarif.Advanced}")
    else:
        kb_builder.button(text=f"""{"✅" if user_data.auto_renewal else "❌"}Автопродление""", callback_data="switch-autorenewal")
    
    kb_builder.button(text="Назад", callback_data="profile")
    
    kb_builder.adjust(1, repeat=True)

    return kb_builder.as_markup()