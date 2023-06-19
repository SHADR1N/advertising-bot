from dotenv import dotenv_values
from aiogram import Bot, Dispatcher


API_TOKEN = {**dotenv_values(".env")}["API_TOKEN"]
print(API_TOKEN)

