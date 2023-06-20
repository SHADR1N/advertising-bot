from aiogram import types as aiotypes, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from addons.keyboards import create_inline_knb, create_reply_knb
from database.enjine_db import new_publication, check_last_publication, get_or_create_user


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


class CallbackHandler:
    def __init__(self, bot):
        self.bot: Bot = bot
        self.channel = -1001937339941

    @staticmethod
    async def get_info_publication(uid, state):
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

    async def send_message_to_channel(self, state: FSMContext):
        message = """🤝 #Продажа_рекламы
📢 Канал: {}
🔘 Категория: {} 
📈 Подписчиков: {}
💳 Стоимость рекламы: {} 
🌍 Часов в топе: {}
👉 Часов в ленте: {}
👁 Охват поста: {}
🤝 Взаимопиар: {}
✅ Админ: {}"""

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
        message = message.format(*data)
        await self.bot.send_message(self.channel, message, disable_web_page_preview=True)

    async def answer(self, message: aiotypes.CallbackQuery, state: FSMContext):
        data = message.data
        uid = message.from_user.id
        mid = message.message.message_id
        current_state = await state.get_state()
        await get_or_create_user(uid)

        if data == "cancel":
            await state.finish()
            return await self.bot.delete_message(chat_id=uid, message_id=mid)

        if current_state == "NewPublication:admin" and data in (
            "send_post", "delete_and_create"
        ):
            if data == "delete_and_create":
                keyboard = [
                    {"Добавить объявление": "new_publication"}
                ]
                knb = await create_inline_knb(keyboard)

                text_answer = "📣 Просим обратить ваше внимание, на правила публикаций постов на нашем канале.\n\n" \
                              "❌ БОТЫ, ПОРНО, ЗАРАБОТКИ, СТАВКИ.\n\n" \
                              "🚫 ТАКИЕ ПОСТЫ ПРОВЕРКУ НЕ ПРОХОДЯТ, ПОСТ БУДЕТ УДАЛЁН А ВЫ ЗАБАНЕНЫ."

                return await self.bot.edit_message_text(chat_id=uid, message_id=mid, text=text_answer, reply_markup=knb)

            if data == "send_post":
                state_data = await state.get_data()
                data = dict(
                    link=state_data.get("link", ""),
                    category=state_data.get("category", ""),
                    subscribers=state_data.get("subscribers", ""),
                    price=state_data.get("price", ""),
                    hours_top=state_data.get("hours_top", ""),
                    hours_wall=state_data.get("hours_wall", ""),
                    count_veiw=state_data.get("count_view", ""),
                    mutual_pr=state_data.get("mutual_pr", ""),
                    admin=state_data.get("admin", ""),
                )
                await new_publication(
                    uid,
                    **data
                )
                await self.send_message_to_channel(state)

            await state.finish()

            keyboard = [
                {"Добавить объявление": "new_publication"}
            ]
            knb = await create_inline_knb(keyboard)

            return await self.bot.edit_message_text(chat_id=uid, message_id=mid, text="✅ Пост опубликован", reply_markup=knb)

        if data == "new_publication":
            access = await check_last_publication(uid)
            if not access:
                return await self.bot.edit_message_text(chat_id=uid, message_id=mid, text="❌ Вы можете создать объявление 1 раз в 3 суток.")

            new_text = await self.get_info_publication(uid, state)
            keyboard = [
                {"❌ Отмена": "cancel"}
            ]

            knb = await create_inline_knb(keyboard)
            await NewPublication.link.set()
            await self.bot.edit_message_text(chat_id=uid, message_id=mid, text=new_text, disable_web_page_preview=True)
            return await self.bot.send_message(
                uid,
                "📢 Канал (введите ссылку на канал в формате https://t.me/username):",
                reply_markup=knb, disable_web_page_preview=True)

        keyboard = [
            {"Добавить объявление": "new_publication"}
        ]
        knb = await create_inline_knb(keyboard)

        text_answer = "📣 Просим обратить ваше внимание, на правила публикаций постов на нашем канале.\n\n" \
                      "❌ БОТЫ, ПОРНО, ЗАРАБОТКИ, СТАВКИ.\n\n" \
                      "🚫 ТАКИЕ ПОСТЫ ПРОВЕРКУ НЕ ПРОХОДЯТ, ПОСТ БУДЕТ УДАЛЁН А ВЫ ЗАБАНЕНЫ."


        try:
            await self.bot.edit_message_text(chat_id=uid, message_id=mid, text=text_answer, reply_markup=knb)
        except:
            await self.bot.send_message(uid, text_answer, reply_markup=knb)
        return