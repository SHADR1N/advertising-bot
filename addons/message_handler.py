import re

from aiogram import types as aiotypes
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database.enjine_db import get_or_create_user

from addons.keyboards import create_inline_knb, create_reply_knb


class NewPublication(StatesGroup):
    link = State()
    category = State()
    subscribers = State()
    price = State()
    hours_top = State()
    hours_wall = State()
    count_view = State()
    mutual_pr = State()
    admin = State()


class MessageHandler:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def is_valid_telegram_url(url):
        pattern = r'https?:\/\/(?:www\.)?t\.me\/([a-zA-Z0-9_]+){1,32}\/?$'
        return bool(re.match(pattern, url))

    @staticmethod
    async def get_info_publication(uid, state: FSMContext):
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

            state_data = await state.get_data()
            data = (
                state_data.get("link", ""),
                state_data.get("category", ""),
                state_data.get("subscribers", ""),
                state_data.get("price", ""),
                state_data.get("hours_top", ""),
                state_data.get("hours_wall", ""),
                state_data.get("count_view", ""),
                state_data.get("mutual_pr", ""),
                state_data.get("admin", ""),
            )
            return message.format(*data)

    async def state_script(self, message: aiotypes.Message, state: FSMContext):
        data = message.text
        uid = message.from_user.id
        mid = message.message_id
        current_state = await state.get_state()
        knb = await create_inline_knb([{"❌ Отмена": "cancel"}])

        if current_state == "NewPublication:admin":
            await state.update_data(admin=data)

            knb = await create_inline_knb([
                {"Отправить пост": "send_post"},
                {"Удалить пост и создать новый": "delete_and_create"}
            ])
            text = await self.get_info_publication(uid, state)
            return await self.bot.send_message(uid, text=text, reply_markup=knb, disable_web_page_preview=True)

        if current_state == "NewPublication:mutual_pr":
            if data not in ("Да", "Нет"):
                knb = await create_reply_knb([["Да", "Нет"]])
                return await self.bot.send_message(uid,
                                                   "Ответ должен быть, Да или Нет.\n🤝 Взаимопиар (Да/Нет):",
                                                   reply_markup=knb)

            await state.update_data(mutual_pr=data)

            await NewPublication.next()

            knb = aiotypes.ReplyKeyboardRemove()
            return await self.bot.send_message(uid, "✅ Ссылка на Админа:", reply_markup=knb)

        if current_state == "NewPublication:count_view":
            if not data.isdigit():
                return await self.bot.send_message(uid,
                                                   "Охват должен быть целым числом.\n👁 Охват поста:",
                                                   reply_markup=knb)

            await state.update_data(count_view=int(data))

            await NewPublication.next()
            knb = await create_reply_knb([["Да", "Нет"]])
            return await self.bot.send_message(uid, "🤝 Взаимопиар (Да/Нет):", reply_markup=knb)

        if current_state == "NewPublication:hours_wall":
            if not data.isdigit():
                return await self.bot.send_message(uid,
                                                   "Кол-во часов должно быть целым числом.\n👉 Часов в ленте:",
                                                   reply_markup=knb)

            await state.update_data(hours_wall=int(data))

            await NewPublication.next()
            return await self.bot.send_message(uid, "👁 Охват поста:", reply_markup=knb)

        if current_state == "NewPublication:hours_top":
            if not data.isdigit():
                return await self.bot.send_message(uid,
                                                   "Кол-во часов должно быть целым числом.\n🌍 Часов в топе:",
                                                   reply_markup=knb)

            await state.update_data(hours_top=int(data))

            await NewPublication.next()
            return await self.bot.send_message(uid, "👉 Часов в ленте:", reply_markup=knb)

        if current_state == "NewPublication:price":
            if not data.isdigit():
                return await self.bot.send_message(uid,
                                                   "Стоимость должна быть целым числом.\n💳 Стоимость рекламы:",
                                                   reply_markup=knb)

            await state.update_data(price=int(data))
            await NewPublication.next()
            return await self.bot.send_message(uid, "🌍 Часов в топе:", reply_markup=knb)

        if current_state == "NewPublication:subscribers":
            if not data.isdigit():
                return await self.bot.send_message(uid,
                                                   "Кол-во подписчиков должно быть целым числом.\n📈 Подписчиков:",
                                                   reply_markup=knb)

            await state.update_data(subscribers=int(data))
            await NewPublication.next()
            return await self.bot.send_message(uid, "💳 Стоимость рекламы:", reply_markup=knb)

        if current_state == "NewPublication:category":
            await state.update_data(category=data)
            await NewPublication.next()
            return await self.bot.send_message(uid, "📈 Подписчиков:", reply_markup=knb)

        if current_state == "NewPublication:link":
            if await self.is_valid_telegram_url(data):
                await state.update_data(link=data)
                await NewPublication.next()
                return await self.bot.send_message(uid, "🔘 Категория:", reply_markup=knb)
            else:
                return await self.bot.send_message(uid,
                                                   "❌ Ссылка на канал не верная.\n"
                                                   "📢 Канал (введите ссылку на канал в формате https://t.me/username)",
                                                   reply_markup=knb, disable_web_page_preview=True)

        return await message.answer("Не известная команда.")

    async def answer(self, message: aiotypes.Message, state: FSMContext):
        uid = message.from_user.id
        text = message.text
        current_state = await state.get_state()
        await get_or_create_user(uid)

        if current_state:
            return await self.state_script(message, state)

        if text == "/start":
            keyboard = [
                {"Добавить объявление": "new_publication"}
            ]
            knb = await create_inline_knb(keyboard)

            text_answer = "📣 Просим обратить ваше внимание, на правила публикаций постов на нашем канале.\n\n" \
                          "❌ БОТЫ, ПОРНО, ЗАРАБОТКИ, СТАВКИ.\n\n" \
                          "🚫 ТАКИЕ ПОСТЫ ПРОВЕРКУ НЕ ПРОХОДЯТ, ПОСТ БУДЕТ УДАЛЁН А ВЫ ЗАБАНЕНЫ."

            return await message.answer(text_answer, reply_markup=knb)

        keyboard = [
            {"Добавить объявление": "new_publication"}
        ]
        knb = await create_inline_knb(keyboard)

        text_answer = "📣 Просим обратить ваше внимание, на правила публикаций постов на нашем канале.\n\n" \
                      "❌ БОТЫ, ПОРНО, ЗАРАБОТКИ, СТАВКИ.\n\n" \
                      "🚫 ТАКИЕ ПОСТЫ ПРОВЕРКУ НЕ ПРОХОДЯТ, ПОСТ БУДЕТ УДАЛЁН А ВЫ ЗАБАНЕНЫ."

        return await self.bot.send_message(uid, text_answer, reply_markup=knb)
