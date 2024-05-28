import asyncio
import json
import datetime
from main import check_news_update
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from config import token, user_id

from itertools import islice


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)



@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["All news","Last 5 news","New news 🙃"]
    await message.reply("Hi, I am new in development, don't judge too harshly!")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Newswire", reply_markup=keyboard)


@dp.message_handler(Text(equals="All news"))
async def get_all_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in reversed(news_dict.items()):
        news =  f"{hunderline(v['article_title'])}\n" \
                f"{hbold(datetime.date.fromtimestamp(v['article_date_timestamp']))}\n" \
                f"{hcode(v['article_desc'])}\n" \
                f"{hlink(v['article_title'], v['article_url'])}"

        await message.answer(news)



@dp.message_handler(Text(equals="Last 5 news"))
async def get_last_five_news(message: types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)


    for k, v in islice(reversed(news_dict.items()), 5, None):
        news =  f"{hunderline(v['article_title'])}\n" \
                f"{hbold(datetime.date.fromtimestamp(v['article_date_timestamp']))}\n" \
                f"{hcode(v['article_desc'])}\n" \
                f"{hlink(v['article_title'], v['article_url'])}"

        await message.answer(news)



@dp.message_handler(Text(equals="New news 🙃"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in reversed(fresh_news.items()):
            news = f"{hunderline(v['article_title'])}\n" \
                   f"{hbold(datetime.date.fromtimestamp(v['article_date_timestamp']))}\n" \
                   f"{hcode(v['article_desc'])}\n" \
                   f"{hlink(v['article_title'], v['article_url'])}"

            await message.answer(news)

    else:
        await message.answer("I don't have a new news for you...")



async def news_every_minute():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hunderline(v['article_title'])}\n" \
                       f"{hbold(datetime.date.fromtimestamp(v['article_date_timestamp']))}\n" \
                       f"{hcode(v['article_desc'])}\n" \
                       f"{hlink(v['article_title'], v['article_url'])}"

                # get your id @userinfobot
                await bot.send_message(user_id, news, disable_notification=True)

        else:
            await bot.send_message(user_id, "i don't have a new news...", disable_notification=True)

        await asyncio.sleep(1800)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)