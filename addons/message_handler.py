from aiogram import types as aiotypes

from database.enjine_db import get_or_create_user

from addons.keyboards import create_inline_knb, create_reply_knb


class MessageHandler:
    def __init__(self, bot):
        self.bot = bot

    async def answer(self, message: aiotypes.Message):
        uid = message.from_user.id
        text = message.text

        if text == "/start":
            keyboard = [
                {"Добавить объявление": "new_publication"}
            ]
            knb = await create_inline_knb(keyboard)

            text_answer = "📣 Просим обратить ваше внимание, на правила публикаций постов на нашем канале.\n\n" \
                          "❌ БОТЫ, ПОРНО, ЗАРАБОТКИ, СТАВКИ.\n\n" \
                          "🚫 ТАКИЕ ПОСТЫ ПРОВЕРКУ НЕ ПРОХОДЯТ, ПОСТ БУДЕТ УДАЛЁН А ВЫ ЗАБАНЕНЫ."

            return await message.answer(text_answer, reply_markup=knb)

        await get_or_create_user(uid)
        return await message.answer("Не известная команада.")
