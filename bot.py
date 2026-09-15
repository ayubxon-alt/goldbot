import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN topilmadi. .env fayliga BOT_TOKEN=... qo'shing.")
if not WEBAPP_URL or not WEBAPP_URL.startswith("https://"):
    raise RuntimeError(
        "WEBAPP_URL topilmadi yoki https:// bilan boshlanmayapti. "
        "Telegram Mini App faqat HTTPS manzilda ishlaydi."
    )

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def webapp_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🟡 Oltin narxlarini ko'rish",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ]
    )


def webapp_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🟡 Narxlar", web_app=WebAppInfo(url=WEBAPP_URL))]
        ],
        resize_keyboard=True,
    )


@dp.message(CommandStart())
async def on_start(message: Message):
    text = (
        "Assalomu alaykum! 👋\n\n"
        "Bu bot orqali oltinning turli proba (585, 750 va h.k.) bo'yicha "
        "joriy narxini ko'rishingiz mumkin.\n\n"
        "Pastdagi tugmani bosing 👇"
    )
    await message.answer(text, reply_markup=webapp_inline_keyboard())
    await message.answer(
        "Istalgan vaqt shu tugmadan ham foydalanishingiz mumkin:",
        reply_markup=webapp_menu_keyboard(),
    )


@dp.message()
async def on_any_message(message: Message):
    await message.answer(
        "Narxlarni ko'rish uchun /start buyrug'ini yuboring yoki quyidagi "
        "tugmadan foydalaning 👇",
        reply_markup=webapp_inline_keyboard(),
    )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
