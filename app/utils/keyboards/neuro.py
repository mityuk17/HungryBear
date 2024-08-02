from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from database.schemas.general import User
from database.schemas.neuro import Prompt


def main_menu(user_data: User) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    
    kb_builder.button(text=f"""Режим чата {"✅" if user_data.gpt_chat_mode else "❌"}""")
    kb_builder.button(text="Готовые промты")
    kb_builder.button(text="Генерация изображения")
    kb_builder.button(text="Меню")
    
    kb_builder.adjust(1, repeat=True)
    
    return kb_builder.as_markup(resize_keyboard=True)


def prompts_list(prompts_list: list[Prompt]) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    
    for prompt in prompts_list:
        kb_builder.button(text=prompt.name, callback_data=f"prompt_{prompt.id}")
    
    kb_builder.adjust(1, repeat=True)
    
    return kb_builder.as_markup()


def end_dialog() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    
    kb_builder.button(text="Сбросить диалог", callback_data="end-dialog")
    
    return kb_builder.as_markup()


def cancle_image_prompt() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    
    kb_builder.button(text="Отмена", callback_data="neuro-menu")
    
    return kb_builder.as_markup()

