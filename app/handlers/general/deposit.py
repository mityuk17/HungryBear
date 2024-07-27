from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from database.schemas.general import Payment, PaymentStatus
from database.crud.general.user import get_user, update_user
from database.crud.general.payment import create_payment, update_payment, get_payment
import utils.texts.general as general_texts
import utils.keyboards.general as general_keyboards
from utils.states import General as GeneralStates


router = Router(name="General-Deposit")


@router.callback_query(F.data.startswith("cancel-payment_"))
async def cancel_payment(callback: CallbackQuery):
    await callback.answer()
    
    payment_id = int(callback.data.split("_")[-1])
    payment = await get_payment(payment_id)
    payment.status = PaymentStatus.Cancelled
    await update_payment(payment)
    
    user = await get_user(callback.from_user.id)
    user_info = general_texts.user_info(user)    
    await callback.message.answer(text=user_info, reply_markup=general_keyboards.profile())
    await callback.message.delete()
    
    
@router.callback_query(F.data == "deposit")
async def get_amount_for_deposit(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(GeneralStates.get_amount_for_deposit)
    await callback.message.answer(text=general_texts.get_amount_for_deposit(), reply_markup=general_keyboards.back_to_profile())
    await callback.message.delete()


@router.message(GeneralStates.get_amount_for_deposit)
async def create_invoice(message: Message, state: FSMContext):
    amount = message.text
    if not amount.isdigit():
        await message.answer(text=general_texts.incorrect_amount_for_deposit, reply_markup=general_keyboards.back_to_profile())
        return
    amount = int(amount)
    await state.clear()
    
    payment_data = Payment(user_id=message.from_user.id, amount=amount)
    payment = await create_payment(payment_data)
    
    prices = [LabeledPrice(label="XTR", amount=amount)]
    await message.answer_invoice(
        title=f"Пополнение баланса",
        description=f"{amount} $BEAR",
        prices=prices,
        provider_token="",
        payload=f"deposit_{payment.id}",
        currency="XTR",
        reply_markup=general_keyboards.payment_keyboard(amount, payment.id)
    )

    
@router.pre_checkout_query()
async def proceed_query(query: PreCheckoutQuery):
    await query.answer(ok=True)
    

@router.message(F.successful_payment)
async def confirm_payment(message: Message):
    payment_data = message.successful_payment
    
    payment_id = int(payment_data.invoice_payload.split("_")[-1])    
    payment = await get_payment(payment_id)
    
    user = await get_user(payment.user_id)
    user.balance += payment.amount
    await update_user(user)
    
    payment.status == PaymentStatus.Succeded
    await update_payment(payment)
    
    await message.answer(text=general_texts.successful_payment(payment.amount), reply_markup=general_keyboards.start_menu())
