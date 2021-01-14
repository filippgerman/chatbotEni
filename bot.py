import logging

import sqlalchemy

from aiogram.types import ContentType

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import BaseStorage
from aiogram.types import ParseMode, InputMediaPhoto, ChatActions
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.utils.markdown import text, bold
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types

logging.basicConfig(level=logging.INFO)  # начало логирования.

bot = Bot(token="1499371935:AAFwkvjwl-zMWagXDRJu-OmqruMHkvNKAU4")  # токен нашего бота
dp = Dispatcher(bot, storage=MemoryStorage())  # Диспетчер


class States(StatesGroup):
    """
    Состояния пользователя
    """
    mode_selection = State()  # выбор режима

    # режимы
    team_rating = State()  # рейтинг команды
    multiple_rating = State()  # множественный рейтинг
    comparison_teams = State()  # сравнение команд


# начало
@dp.message_handler(commands=['start'], state='*')
async def start_work(message: types.Message):
    """
    Стратовое сообщение при включении бота (приветствие)
    """
    await bot.send_message(message.from_user.id, 'Приветствие')
    await States.mode_selection.set()  # переключение в состояние (Выбор режима)
    await mode_buttons(message)  # вызов функции показывающую кнопки с режимом


@dp.message_handler(state=States.mode_selection, content_types=types.ContentTypes.TEXT)
async def distribution(message: types.Message):
    """
    Функция распределения, обрабатывает ответ пользователя и присваевает необходимое состояние состояние
    """
    if message.text == 'Рейтинг команды':
        await States.team_rating.set()  # переключение на состояние 'рейтинг команды'
        await bot.send_message(message.from_user.id, 'Введите название команды: ')
    elif message.text == 'Рейтинг склеенный':
        await States.multiple_rating.set()  # переключение на состояние 'множественный рейтинг'
        await bot.send_message(message.from_user.id, 'Если в разных квизах вы играете под разными названиями,'
                                                     ' запросите общий рейтинг.\n'
                                                     'Пример: команда 1+команда 2 + ...\n'
                                                     'Введите название команд: ')
    elif message.text == 'Сравнение команд':
        await States.comparison_teams.set()  # переключение на состояние 'сравнение команд'
        await bot.send_message(message.from_user.id,
                               'Если вы хотите сравнить две команды, введите их названия через "/"\n'
                               'Пример: команда 1/команда 2\n'
                               'Введите название команд: ')
    else:
        await bot.send_message(message.from_user.id,
                               'Такого режима нет, пожалуйста выбирите из существующих режимов: ')


@dp.message_handler(state=States.team_rating, content_types=types.ContentTypes.TEXT)
async def rating(message: types.Message):
    """
    Пользователь вводит название команды
    отправляет сообщением ретинг команды
    """
    await bot.send_message(message.from_user.id, 'Сообщение с рейтингом')

    await States.mode_selection.set()  # возвращения статуса для выбора режима
    await mode_buttons(message)  # вызов функции показывающую кнопки с режимом


@dp.message_handler(state=States.multiple_rating, content_types=types.ContentTypes.TEXT)
async def multiple_rating(message: types.Message):
    """
    Пользователь вводит название команд
    функция отправляет суммарный ретинг этих команд
    """
    await bot.send_message(message.from_user.id, 'Сообщение с склееным рейтингом')

    await States.mode_selection.set()  # возвращения статуса для выбора режима
    await mode_buttons(message)  # вызов функции показывающую кнопки с режимом


@dp.message_handler(state=States.comparison_teams, content_types=types.ContentTypes.TEXT)
async def comparison_teams(message: types.Message):
    """
    Пользователь вводит название команд
    функция отправляет сравнение этих команд
    """
    await bot.send_message(message.from_user.id, 'Сообщение с сравнением')

    await States.mode_selection.set()  # возвращения статуса для выбора режима
    await mode_buttons(message)  # вызов функции показывающую кнопки с режимом


# кнопки
@dp.message_handler(state='mode_selection')
async def mode_buttons(message: types.Message):
    keyboard_1 = types.KeyboardButton("Рейтинг команды")
    keyboard_2 = types.KeyboardButton("Рейтинг склеенный")
    keyboard_3 = types.KeyboardButton("Сравнение команд")

    button = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
        .add(keyboard_1).add(keyboard_2).add(keyboard_3)

    await message.answer(text(f"Выберите одну из кнопок"),
                         reply_markup=button)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)  # поллинг, для получения обновлени от бота
