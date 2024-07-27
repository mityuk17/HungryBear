from bot import bot, dispatcher
from handlers import general_user_router, general_deposit_router, general_subscription_router
from database.base import init_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.base import notificate_subscription_endtime, monitor_subscription_endtime
import asyncio
import logging


async def start():
    scheduler = AsyncIOScheduler()
    logging.basicConfig(level=logging.INFO)
    await init_db()
    scheduler.add_job(monitor_subscription_endtime, "interval", [3], minutes=3)
    scheduler.add_job(notificate_subscription_endtime, "interval", [12*60*60], minutes=12*60*60)
    dispatcher.include_router(general_user_router)
    dispatcher.include_router(general_deposit_router)
    dispatcher.include_router(general_subscription_router)
    scheduler.start()
    await dispatcher.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(start())