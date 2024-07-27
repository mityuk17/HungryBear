from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from database.schemas.general import Payment, PaymentStatus, Tarif
from database.crud.general.user import get_user, update_user
from database.crud.general.payment import create_payment, update_payment, get_payment
import utils.texts.general as general_texts
import utils.keyboards.general as general_keyboards
from utils.states import General as GeneralStates
from datetime import datetime, timedelta


router = Router(name="General-Subscription")

@router.callback_query(F.data=="manage-subscription")
async def manage_subscription(callback: CallbackQuery):
    await callback.answer()
    user = await get_user(callback.from_user.id)
    await callback.message.answer(text=general_texts.manage_subscription_menu(user), reply_markup=general_keyboards.manage_subscription_menu(user))
    await callback.message.delete()


@router.callback_query(F.data == "switch-autorenewal")
async def switch_autorenewal(callback: CallbackQuery):
    await callback.answer()
    
    user = await get_user(callback.from_user.id)
    user.auto_renewal = not(user.auto_renewal)
    await update_user(user)
    
    await callback.message.edit_reply_markup(reply_markup=general_keyboards.manage_subscription_menu(user))


@router.callback_query(F.data.startswith("buy-subscription_"))
async def buy_subscription(callback: CallbackQuery):
    tarif = callback.data.split("_")[-1]
    price = Tarif.price(tarif)
    user = await get_user(callback.from_user.id)
    if user.balance < price:
        await callback.answer(general_texts.insufficient_balance(), show_alert=True)
        return
    
    await callback.answer()
    user.balance -= price
    user.tarif = tarif
    endtime = datetime.today() + timedelta(days=30)
    user.subsctiption_endtime = endtime
    await update_user(user)
    
    await callback.message.answer(text=general_texts.subscription_bought(tarif=tarif, endtime=endtime), reply_markup=general_keyboards.back_to_profile())
    await callback.message.delete()
    
