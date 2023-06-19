from aiogram import types as aiotypes


class MessageHandler:
    def __init__(self, bot):
        self.bot = bot

    async def answer(self, message: aiotypes.Message):
        return await message.answer("Не известная команада.")