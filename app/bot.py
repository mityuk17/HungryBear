from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from config import settings
from database.crud.general.user import get_user, update_user
from database.schemas.general import User
from datetime import datetime


class UserUpdateMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            tg_user = event.from_user
            user = await get_user(tg_user.id)
            if user:
                user.username = tg_user.username
                user.last_activity = datetime.today()
                user.name = tg_user.full_name
                await update_user(user)
        except AttributeError:
            pass
        return await handler(event, data)

bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True))

storage = RedisStorage.from_url(f"redis://{settings.REDIS_USER}:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}")


dispatcher = Dispatcher(storage=storage)
dispatcher.message.middleware(UserUpdateMiddleware())
dispatcher.callback_query.middleware(UserUpdateMiddleware)




