from addons.message_handler import MessageHandler
from addons.callback_handler import CallbackHandler

from database.models import main as create_tables

from dotenv import dotenv_values

from aiogram import Bot, Dispatcher, executor
from aiogram import types as aiotypes
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


API_TOKEN = {**dotenv_values(".env")}["API_TOKEN"]
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

message_handler = MessageHandler(bot)
callback_handler = CallbackHandler(bot)


@dp.message_handler(state="*")
async def aio_message(message: aiotypes.Message, state: FSMContext):
    return await message_handler.answer(message, state)


@dp.callback_query_handler(state="*")
async def aio_callback(call: aiotypes.CallbackQuery, state: FSMContext):
    return await callback_handler.answer(call, state)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=create_tables)
