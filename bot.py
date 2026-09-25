import asyncio
from collections import defaultdict
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InputMediaPhoto
from aiogram.client.session.aiohttp import AiohttpSession

TOKEN = "8887663780:AAE3R6cllPOw8ZpFNp8Sly--FGzcbeC84WM"

session = AiohttpSession(proxy="socks5://127.0.0.1:1080")
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

# عکس‌هایی که کاربر فرستاده، بر اساس chat_id ذخیره میشن
pending = defaultdict(list)

@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer(
        "هر تعداد عکس که می‌خوای بفرست (جدا جدا یا با هم).\n"
        "وقتی تموم شد، بنویس /done تا همه رو یه آلبوم برات بفرستم."
    )

@dp.message(Command("done"))
async def done(m: types.Message):
    photos = pending.pop(m.chat.id, [])
    if len(photos) < 2:
        await m.answer("حداقل ۲ تا عکس بفرست.")
        return
    media = [InputMediaPhoto(media=fid) for fid in photos]
    await bot.send_media_group(chat_id=m.chat.id, media=media)

@dp.message(lambda m: m.photo)
async def get_photo(m: types.Message):
    # بزرگ‌ترین سایز عکس رو ذخیره کن
    pending[m.chat.id].append(m.photo[-1].file_id)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
