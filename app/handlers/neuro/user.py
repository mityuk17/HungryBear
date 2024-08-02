from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from database.schemas.general import User, Tarif
from database.crud.general.user import get_user, update_user
from database.crud.neuro.prompt import all_prompts, get_prompt
import utils.texts.neuro as neuro_texts
import utils.keyboards.neuro as neuro_keyboards
from utils.states import Neuro as NeuroStates
from tools.neuro.yandexgpt import YandexGPT


router = Router(name="Neuro-User")



async def yandexgpt_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data({"active_tool": "Нейросеть"})
    user = await get_user(callback.from_user.id)
    
    await callback.message.answer(text=neuro_texts.menu(), reply_markup=neuro_keyboards.main_menu(user))
    await callback.message.delete()


@router.callback_query(F.data == "neuro-menu")
async def yandexgpt_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(None)
    
    await callback.message.delete()
    
    
@router.message(F.text.startswith("Режим чата"))
async def toggle_chat_mode(message: Message):
    user = await get_user(message.from_user.id)
    user.gpt_chat_mode = not(user.gpt_chat_mode)
    await update_user(user)
    
    await message.answer(text=neuro_texts.chat_mode_toggle(user.gpt_chat_mode), reply_markup=neuro_keyboards.main_menu(user))
    
    
@router.message(F.text == "Готовые промты")
async def prompts(message: Message):
    user = await get_user(message.from_user.id)
    if user.active_subscription() == Tarif.Free:
        await message.answer(neuro_texts.no_subscription_prompts())
        return
    
    prompts = await all_prompts()
    await message.answer(text=neuro_texts.prompts_menu(), reply_markup=neuro_keyboards.prompts_list(prompts))
    

@router.callback_query(F.data.startswith("prompt_"))
async def pick_prompt(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    prompt_id = int(callback.data.split("_")[-1])
    
    prompt = await get_prompt(prompt_id)

    dialog = [{"role": "system", "text": prompt.text}]
    
    await state.update_data({"dialog": dialog})
    
    await callback.message.edit_text(text=neuro_texts.new_dialog(prompt.name), reply_markup=neuro_keyboards.end_dialog())
    

@router.callback_query(F.data == "end-dialog")
async def end_dialog(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(None)
    
    user = await get_user(callback.from_user.id)
    
    await state.update_data({"dialog": None})
    
    await callback.message.answer(text=neuro_texts.dialog_ended(), reply_markup=neuro_keyboards.main_menu(user))
    

async def get_message(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    
    if not user.gpt_chat_mode:
        dialog = [{"role": "user", "text": message.text}]
        response = response = await YandexGPT.text_completion(dialog)
        
        await message.reply(text=response, reply_markup=neuro_keyboards.main_menu(user))
    
    else:
        dialog = (await state.get_data()).get("dialog")
        
        if not dialog:
            dialog = [{"role": "user", "text": message.text}]
            response = await YandexGPT.text_completion(dialog)
            dialog.append({"role": "assistant", "text": response})
        else:
            dialog.append({"role": "user", "text": message.text})
            response = await YandexGPT.text_completion(dialog)
            dialog.append({"role": "assistant", "text": response})
            
        await state.update_data({"dialog": dialog})
        await message.reply(text=response, reply_markup=neuro_keyboards.end_dialog())
    

@router.message(F.text == "Генерация изображения")
async def image_mode(message: Message, state: FSMContext):
    await message.answer("Фунционал находится в разработке")
    return
    
    user = await get_user(message.from_user.id)
    
    if user.active_subscription() == Tarif.Free:
        await message.answer(text=neuro_texts.no_subscription_images(), reply_markup=neuro_keyboards.main_menu(user))
        return
    
    await state.set_state(NeuroStates.get_image_prompt)
    
    await message.answer(text=neuro_texts.get_image_prompt(), reply_markup=neuro_keyboards.cancle_image_prompt())
    

@router.message(NeuroStates.get_image_prompt)
async def image_generation(message: Message, state: FSMContext):
    await state.set_state(None)
    
    prompt = message.text
    
    image = "image"
    
    await message.reply(image)
    
    
    

    
    

    