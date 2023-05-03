import json
import logging
import random

import emoji
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

from config_file import config

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

bot = Bot(config.token_api.get_secret_value())
dp = Dispatcher(bot, storage=storage)


class StateGame(StatesGroup):
    the_bot = State()
    the_user = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    print("start")
    users_data_file = open('users/' + str(message.from_user.id) + '.txt', 'w')
    json_data = json.dumps({"count": 0, "random_number": random.randint(1, 100), "command": "start"})
    users_data_file.write(json_data)
    users_data_file.close()
    kb = [
        [
            types.KeyboardButton(text="Я загадываю число боту от 1 до 100"),
            types.KeyboardButton(text="Бот загадывает мне число от 1 до 100")
        ],
    ]
    keyboar = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери режим"
    )
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer(
        "Привет, я бот Угадай число " + message.from_user.username + "\n Выбери режим в котором будешь играть",
        reply_markup=keyboar)


@dp.message_handler(filters.Text(equals="Я загадываю число боту от 1 до 100"))
async def user(message: types.Message):
    await StateGame.the_user.set()
    await message.reply("Если готов ответь да или нет (отказ от игры)")


@dp.message_handler(filters.Text(equals="Бот загадывает мне число от 1 до 100"))
async def bote(message: types.Message):
    await StateGame.the_bot.set()
    await message.reply("Если готов ответь да или нет (отказ от игры)")


choice_yes = [
    'Да',
    'да'
]


@dp.message_handler(filters.Text(contains=choice_yes, ignore_case=True), state=StateGame.the_bot)
async def play(message: types.Message, state: FSMContext):
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


choice_note = [
    'нет',
    'Нет'
]


@dp.message_handler(filters.Text(contains=choice_note, ignore_case=True), state=StateGame.the_user)
async def mes(message: types.Message, state: FSMContext):
    users_data_file = open('users/' + str(message.from_user.id) + '.txt', 'r+')
    json_data = json.loads(users_data_file.readline())
    users_data_file.truncate(0)  # ОЧИЩАЕМ файл от содержимого
    users_data_file.seek(0)
    users_data_file.write(
        json.dumps({"count": json_data['count']}))
    users_data_file.close()
    await message.reply("Жаль, пока пока.")
    await state.finish()
    await message.answer("Для того чтобы начать игру заново нажмите /start.")


choice_no = [
    'Нет',
    'нет'
]


@dp.message_handler(filters.Text(contains=choice_no, ignore_case=True), state=StateGame.the_bot)
async def mes(message: types.Message, state: FSMContext):
    users_data_file = open('users/' + str(message.from_user.id) + '.txt', 'r+')
    json_data = json.loads(users_data_file.readline())
    users_data_file.truncate(0)  # ОЧИЩАЕМ файл от содержимого
    users_data_file.seek(0)
    users_data_file.write(
        json.dumps({"count": json_data['count'], "random_number": json_data['random_number'], "command": "нет"}))
    users_data_file.close()
    await message.reply("Жаль, пока пока.")
    await state.finish()
    await message.answer("Для того чтобы начать игру заново нажмите /start.")


choice_ye = [
    'Да',
    'да'
]


@dp.message_handler(filters.Text(contains=choice_ye, ignore_case=True), state=StateGame.the_user)
async def play(message: types.Message, state: FSMContext):
    users_data_file = open('users/' + str(message.from_user.id) + '.txt', 'r+')
    json_data = json.loads(users_data_file.readline())
    if json_data["command"] == "нет":
        await message.answer("Нажмите /start для того чтобы начать игру заново.")
    users_data_file.truncate(0)  # ОЧИЩАЕМ файл от содержимого
    users_data_file.seek(0)
    users_data_file.write(
        json.dumps({"count": json_data['count'], "command": "да"}))
    users_data_file.close()
    kb = [
        [
            types.KeyboardButton(text="Верно"),
            types.KeyboardButton(text="Не попал")
        ],
    ]
    keyboar = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери режим"
    )
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.reply("Отличный выбор! Я отгадываю, а ты пиши верно или я не попал", reply_markup=keyboar)
    mese = random.randint(1, 100)
    await message.answer(mese)


choice_yet = ['Верно',
              'верно']


@dp.message_handler(filters.Text(contains=choice_yet, ignore_case=True), state=StateGame.the_user)
async def answer_bot(message: types.Message, state: FSMContext):
    await message.answer("я выиграл" + emoji.emojize(":clown_face:"))
    await state.finish()
    await message.answer("Для того чтобы начать игру заново нажмите /start.")
    return


choice_not = [
    'Не попал',
    'не попал'
]


@dp.message_handler(filters.Text(contains=choice_not, ignore_case=True), state=StateGame.the_user)
async def game_user(message: types.Message, state: FSMContext):
    users_data_file = open('users/' + str(message.from_user.id) + '.txt', 'r+')
    json_data = json.loads(users_data_file.readline())
    users_data_file.truncate(0)  # ОЧИЩАЕМ файл от содержимого
    users_data_file.seek(0)
    users_data_file.write(
        json.dumps({"count": json_data['count'] + 1}))
    users_data_file.close()
    mes = random.randint(1, 100)
    if json_data['count'] + 1 > 5:
        await message.answer("Я неудачник, я проиграл" + emoji.emojize(":clown_face:"))
        await state.finish()
        await message.answer("Для того чтобы начать игру заново нажмите /start.")
        return
    await message.answer(mes)


@dp.message_handler(lambda message: message.text.isdigit(), state=StateGame.the_bot)
async def number(message: types.Message, state: FSMContext):
    users_data_file = open('users/' + str(message.from_user.id) + '.txt', 'r+')
    json_data = json.loads(users_data_file.readline())
    if json_data["command"] == "start":
        await message.answer("Введите да или нет, чтобы начать игру.")
    else:
        users_data_file.truncate(0)  # ОЧИЩАЕМ файл от содержимого
        users_data_file.seek(0)
        users_data_file.write(json.dumps({"count": json_data['count'] + 1, "random_number": json_data['random_number'],
                                          "command": json_data['command']}))
        users_data_file.close()
        if json_data['count'] + 1 > 5:
            await message.answer("Неудачник, ты проиграл" + emoji.emojize(":clown_face:"))
            await state.finish()
            await message.answer("Для того чтобы начать игру заново нажмите /start.")
            return
        new_mes = int(message.text)
        if new_mes == int(json_data['random_number']):
            await message.answer("Ты угадал! Поздравляю!!!")
            await state.finish()
            await message.answer("Для того чтобы начать игру заново нажмите /start.")
        elif new_mes < int(json_data['random_number']):
            await message.answer("Мое число больше. Думай дальше!")
        else:
            await message.answer("Мое число меньше! Давай думай!)")


@dp.message_handler(state=StateGame.the_bot)
async def other_messages(message: types.Message, state: FSMContext):
    await message.answer("Введите корректное сообщение (Да или Нет) или введите число, если это требуется.")


@dp.message_handler(state=StateGame.the_user)
async def other_messages(message: types.Message, state: FSMContext):
    await message.answer("Введите корректное сообщение (Правильно или Не правильно) или введите число, если это требуется.")


async def main():
    await dp.stop_polling(bot)


if __name__ == '__main__':
    executor.start_polling(dp)  # запуск бота
