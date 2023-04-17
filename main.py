import json
import logging
import random

import emoji
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import filters
from aiogram.utils import executor

from config_file import config

logging.basicConfig(level=logging.INFO)

bot = Bot(config.token_api.get_secret_value())
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    print("start")
    users_data_file = open('users/' + str(message.from_user.id) + '.txt', 'w')
    json_data = json.dumps({"count": 0, "random_number": random.randint(1, 30), "command": "start"})
    users_data_file.write(json_data)
    users_data_file.close()
    await message.answer("Привет, будем играть в игру Угадай число, " + message.from_user.username + "?")


choice_yes = [
    'Да',
    'да'
]


@dp.message_handler(filters.Text(contains=choice_yes, ignore_case=True))
async def play(message: types.Message):
    users_data_file = open('users/' + str(message.from_user.id) + '.txt', 'r+')
    json_data = json.loads(users_data_file.readline())
    if json_data["command"] == "нет":
        await message.answer("Нажмите /start для того чтобы начать игру заново.")
    users_data_file.truncate(0)  # ОЧИЩАЕМ файл от содержимого
    users_data_file.seek(0)
    users_data_file.write(
        json.dumps({"count": json_data['count'], "random_number": json_data['random_number'], "command": "да"}))
    users_data_file.close()

    await message.reply("Отличный выбор! Я загадываю число, а ты попробуй угадать.")


choice_no = [
    'Нет',
    'нет'
]


@dp.message_handler(filters.Text(contains=choice_no, ignore_case=True))
async def mes(message: types.Message):
    users_data_file = open('users/' + str(message.from_user.id) + '.txt', 'r+')
    json_data = json.loads(users_data_file.readline())
    users_data_file.truncate(0)  # ОЧИЩАЕМ файл от содержимого
    users_data_file.seek(0)
    users_data_file.write(
        json.dumps({"count": json_data['count'], "random_number": json_data['random_number'], "command": "нет"}))
    users_data_file.close()
    await message.reply("Жаль, пока пока.")
    await message.answer("Для того чтобы начать игру заново нажмите /start.")


@dp.message_handler(lambda message: message.text.isdigit())
async def number(message: types.Message):
    users_data_file = open('users/' + str(message.from_user.id) + '.txt', 'r+')
    json_data = json.loads(users_data_file.readline())
    if json_data["command"] == "start":
        await message.answer("Введите да или нет, чтобы начать игру.")
    else:
        users_data_file.truncate(0)  # ОЧИЩАЕМ файл от содержимого
        users_data_file.seek(0)
        users_data_file.write(json.dumps({"count": json_data['count'] + 1, "random_number": json_data['random_number'], "command": json_data['command']}))
        users_data_file.close()
        if json_data['count'] + 1 > 5:
            await message.answer("Неудачник, ты проиграл" + emoji.emojize(":clown_face:"))
            await message.answer("Для того чтобы начать игру заново нажмите /start.")
            return
        new_mes = int(message.text)
        if new_mes == int(json_data['random_number']):
            await message.answer("Ты угадал! Поздравляю!!!")
            await message.answer("Для того чтобы начать игру заново нажмите /start.")
        elif new_mes < int(json_data['random_number']):
            await message.answer("Мое число больше. Думай дальше!")
        else:
            await message.answer("Мое число меньше! Давай думай!)")


@dp.message_handler()
async def other_messages(message: types.Message):
    await message.answer("Введите корректное сообщение (Да или Нет) или введите число, если это требуется.")


async def main():
    await dp.stop_polling(bot)


if __name__ == '__main__':
    executor.start_polling(dp)  # запуск бота
