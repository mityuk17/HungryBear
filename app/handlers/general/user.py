from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.schemas.general import User
from database.crud.general.user import get_user, create_user
from database.crud.general.tool import active_tools
import utils.texts.general as general_texts
import utils.keyboards.general as general_keyboards


router = Router(name="General-User")


@router.message(CommandStart())
async def start(message: Message):
    telegram_user = message.from_user
    user = await get_user(telegram_user.id)
    
    if not user:
        new_user = User(
            id=telegram_user.id,
            username=telegram_user.username,
            name=telegram_user.full_name
        )
        await create_user(new_user)
    
    await message.answer(
        text=general_texts.start_menu(),
        reply_markup=general_keyboards.start_menu())
    
    
@router.message(F.text == "Сервисы")
async def tools_list(message: Message):
    tools = await active_tools()
    
    await message.answer(
        text=general_texts.pick_tool_menu(),
        reply_markup=general_keyboards.pick_tool_menu(tools)
    )
    

@router.message(F.text == "Профиль")
async def user_profile(message: Message):
    user = await get_user(message.from_user.id)
    
    user_info = general_texts.user_info(user)
    
    await message.answer(text=user_info, reply_markup=general_keyboards.profile())


@router.message(F.text == "О проекте")
async def abot_project(message: Message):
    await message.answer(text=general_texts.about_project())
    

@router.callback_query(F.data == "profile")
async def user_profile_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    
    user = await get_user(callback.from_user.id)
    user_info = general_texts.user_info(user)    
    await callback.message.answer(text=user_info, reply_markup=general_keyboards.profile())
    await callback.message.delete()
    

@router.callback_query(F.data == "about-points")
async def about_points(callback: CallbackQuery):
    await callback.answer()
    
    await callback.message.answer(text=general_texts.points_info())



              