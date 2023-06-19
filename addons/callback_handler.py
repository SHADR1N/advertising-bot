from aiogram import types as aiotypes, Bot


class CallbackHandler:
    def __init__(self, bot):
        self.bot: Bot = bot

    @staticmethod
    async def get_info_publication(uid):
        message = """🤝 Продажа рекламы
📝 Для подачи объявления, заполните анкету, в которой обязательно должны быть заполнены такие пункты как: 

📢 Канал: {}
🔘 Категория: {} 
📈 Подписчиков: {}
💳 Стоимость рекламы: {} 
🌍 Часов в топе: {}
👉 Часов в ленте: {}
👁 Охват поста: {}
🤝 Взаимопиар: {}
✅ Админ: {}

📡 К публикаций принимаются только правильно заполненные объявления.
Закидывать анкету можно не чаще чем 1 раз в 3 дня.
😡 Порно, боты, ставки и всякую дичь не предлагать, сразу бан с пометкой спам."""

        data = ()
        return message.format(data)

    async def answer(self, message: aiotypes.CallbackQuery):
        data = message.data
        uid = message.from_user.id
        mid = message.message.message_id

        if data == "new_publication":
            new_text = ""
            return await self.bot.edit_message_text(chat_id=uid, message_id=mid, new_text, reply_markup=knb)

        return await message.answer("Не известная команада.")
