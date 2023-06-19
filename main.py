from addons.message_handler import MessageHandler
from addons.callback_handler import CallbackHandler

from database.models import main as create_tables

from dotenv import dotenv_values

from aiogram import Bot, Dispatcher, executor
from aiogram import types as aiotypes


API_TOKEN = {**dotenv_values(".env")}["API_TOKEN"]
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

message_handler = MessageHandler(bot)
callback_handler = CallbackHandler(bot)


@dp.message_handler()
async def aio_message(message: aiotypes.Message):
    return await message_handler.answer(message)


@dp.callback_query_handler()
async def aio_callback(call: aiotypes.CallbackQuery):
    return await callback_handler.answer(call)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=create_tables)
