# -*- coding: utf-8 -*-
import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram import html
import sqlite3


logging.basicConfig(level=logging.INFO)
bot = Bot(token="6732763632:AAGepGNtJtDXh8anadn6yRyl40vIU7c9i1Q")
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Найти информацию о фильме")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    con = sqlite3.connect("userdata.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users")
    register = True
    for user in cursor.fetchall():
        if int(user[0]) == message.from_user.id:
            register = False
    if register:
        cursor.execute("INSERT INTO users (bool, id) VALUES (?, ?)", (0, message.from_user.id))
        con.commit()
    con.close()
    await message.answer("Привет, это бот который выдает информацию о фильме по названию!", reply_markup=keyboard)


@dp.message(F.text)
async def get_message(message: types.Message):
    con = sqlite3.connect("userdata.db")
    cursor = con.cursor()
    if message.text == "Найти информацию о фильме":
        cursor.execute(f"UPDATE users SET bool = '1' WHERE id='{message.from_user.id}'")
        con.commit()
        await message.answer("Введите название фильма и отправьте!")
    else:
        cursor.execute(f"SELECT bool FROM users WHERE id='{message.from_user.id}'")
        text = cursor.fetchone()[0]
        if text:
            cursor.execute(f"UPDATE users SET bool = '0' WHERE id='{message.from_user.id}'")
            con.commit()
            with open('movies.json', 'r', encoding='utf-8') as f:
                pages = json.loads(f.read())
                user_text = message.text
                for page in pages:
                    info = [info for info in [lists for lists in list(page.items())[0][1]] if user_text in info['title']]
                    if info:
                        text = f'Название фильма: {info[0]["title"]}\n'\
                               f'Жанр: {info[0]["genre"]}\n'\
                               f'Год выхода: {info[0]["year"]}\n'\
                               f'Страна: {info[0]["country"]}\n'\
                               f'{html.quote(info[0]["link"])}'
                        await message.answer(text)
                        break
                if not info:
                    await message.answer("Информация о фильме не найдена!")
    con.close()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
