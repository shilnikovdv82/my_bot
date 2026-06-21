import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import OpenAI

# === Настройки ===
TELEGRAM_TOKEN = ""
OPENROUTER_KEY = "d"
MODEL = "meta-llama/llama-3.3-70b-instruct:free"

# === Инициализация ===
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я твой ИИ-помощник. Спрашивай что угодно.")

@dp.message()
async def chat_handler(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": message.text}],
    )
    answer = response.choices[0].message.content
    await message.answer(answer)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
