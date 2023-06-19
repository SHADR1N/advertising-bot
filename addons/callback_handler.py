from aiogram import types as aiotypes


class CallbackHandler:
    def __init__(self, bot):
        self.bot = bot

    async def answer(self, message: aiotypes.CallbackQuery):
        return await message.answer("Не известная команада.")
