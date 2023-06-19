from aiogram import types


async def create_reply_knb(keyboards: list, row_width=2) -> types.ReplyKeyboardMarkup:
    knb = types.ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=True)
    for keyboard in keyboards:

        if isinstance(keyboard, list):
            knb.add(
                *[types.KeyboardButton(text=text) for text in keyboard]
            )

        else:
            knb.add(
                types.KeyboardButton(text=keyboard)
            )

    return knb


async def create_inline_knb(keyboards: list, row_width=2) -> types.InlineKeyboardMarkup:
    knb = types.InlineKeyboardMarkup(row_width=row_width)

    for keyboard in keyboards:
        knb.add(
            *[types.InlineKeyboardButton(text=text, callback_data=callback) for text, callback in keyboard.items()]
        )

    return knb
