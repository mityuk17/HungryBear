from datetime import datetime, timedelta
from database.crud.general.user import users_with_subscription, update_user
from database.schemas.general import Tarif
from bot import bot
from utils.texts import general as general_texts


async def monitor_subscription_endtime(interval: int):
    #interval - minutes
    users = await users_with_subscription()
    
    for user in users:
        if user.subsctiption_endtime <= datetime.today() + timedelta(minutes=interval):
            if user.auto_renewal:
                price = Tarif.price(user.tarif)
                if user.balance > price:
                    user.subsctiption_endtime += timedelta(days=30)
                    user.balance -= price
                    await bot.send_message(chat_id=user.id, text=general_texts.subscription_autorenewed(user.tarif))
                    
                else:
                    tarif = user.tarif
                    user.auto_renewal = False
                    user.tarif = Tarif.Free
                    await bot.send_message(chat_id=user.id, text=general_texts.subscription_cancelled(tarif))
                    
            else:
                tarif = user.tarif
                user.tarif = Tarif.Free
                await bot.send_message(chat_id=user.id, text=general_texts.subscription_ended(tarif))
                
            await update_user(user)


async def notificate_subscription_endtime(interval: int):
    #interval - minutes
    users = await users_with_subscription()
    
    for user in users:
        if user.subsctiption_endtime <= datetime.today() + timedelta(minutes=interval):
            await bot.send_message(chat_id=user.id, text=general_texts.notificate_about_subscription_endtime(user))
    