import logging

import sqlalchemy

from aiogram.types import ContentType

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.markdown import text, bold
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
from memoryClass import Connector
from format import number_games_str, remove_spaces, remove_line, formatting
from statistic import Statistics

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
        await States.team_rating.set()  # переключение на состояние 'рейтинг команды'
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
                               'Такого режима нет, пожалуйста выбирите из кнопок: ')


@dp.message_handler(state=States.team_rating, content_types=types.ContentTypes.TEXT)
async def rating(message: types.Message):
    """
    Пользователь вводит название команды
    отправляет сообщением ретинг команды
    """
    response = Connector(message.text).get()

    sum_games = 0  # сумма игр по всем квизам
    sum_points = 0  # сумма очков по всме квизам
    count_kviz = 0  # кол-во квизов

    for el in response:
        if el.points > 0:  # проверка не пустышка ли это
            count_kviz += 1
            sum_games += el.games
            sum_points += el.points

    # основа для ответа пользователю
    answer = f"Команда: {message.text}\n" \
             f"Всего игр: {sum_games} ({number_games_str(count_kviz)})\n" \
             f"Всего баллов {sum_points} ({number_games_str(count_kviz)})\n" \
             f"Подробно:" + ("\n" * 2)

    for row in response:
        if row.points > 0:  # проверка не пустышка ли
            answer += f"{row.name_kviz}\n" \
                      f"Всего: {row.points} бал.\n" \
                      f"Всего игр: {row.games}\n" \
                      f"Среднее: {round((row.points / row.games), 2)}" + ("\n" * 2)
        else:  # если квиз пустышка то добавляем упрощ. строку
            answer += f"{row.name_kviz}: 0 бал.\n"

    await bot.send_message(message.from_user.id, answer)  # отправка ответа пользователю

    await States.mode_selection.set()  # возвращения статуса для выбора режима
    await mode_buttons(message)  # вызов функции показывающую кнопки с режимом


@dp.message_handler(state=States.comparison_teams, content_types=types.ContentTypes.TEXT)
async def comparison_teams(message: types.Message):
    """
    Пользователь вводит название команд
    функция отправляет сравнение этих команд
    """

    # основа для ответа пользователю:
    all_games = f"Всего игр: "
    all_points = f"Всего баллов "
    info_on_games = []

    for db in Connector.name_db:
        """
        объекты квизов, статистика, необходимы для записи
        информации по всем квизам от каждой команды.
        Объекты в себе хранят склеенную инфу по пользователям
        """
        info_on_games.append(Statistics(Connector.name_kviz.get(db.__tablename__)))

    for name in message.text.split('/'):
        name = remove_spaces(name)  # форматируем имя, убираем пробелы
        response = Connector(name).get()  # получаем список объектов с инф. по квизам

        sum_games = 0  # сумма игр по всем квизам
        sum_points = 0  # сумма очков по всме квизам
        count_kviz = 0  # кол-во квизов

        for el in response:
            if el.points > 0:  # проверка не пустышка ли это
                count_kviz += 1  # счетчик не пустых квизов
                sum_games += el.games
                sum_points += el.points

        # добавляем данные по каждомой команде в одну строку через /
        all_games += f" / {sum_games} ({number_games_str(count_kviz)})"
        all_points += f" / {sum_points} ({number_games_str(count_kviz)})"

        # бежим по списку объектов и вытаскиваем информацию по каждому квизу
        for row in response:
            for kviz in info_on_games:
                # ищем нужный объект квиза созданный заранее.
                # и добавляем значения другого пользователя
                if kviz.name_kviz == row.name_kviz:
                    kviz.add_points(row.points)  # доб кол-во очков
                    kviz.add_games(row.games)  # доб кол-во игр
                    if row.games == 0:  # проверка не пустышка ли это (на ноль делить нальзя)
                        kviz.add_average(0)  # если игр не было, сразу присваиваем 0
                    else:  # если игры были то производим вычисления
                        kviz.add_average(round(row.points / row.games, 2))  # преобразовываем среднее значение

    # сортируем список по кол-ву игр, а потом уже по алфавиту
    info_on_games = sorted(info_on_games, key=lambda data: (-data.games, data.name_kviz))

    answer = f"Команда: {message.text}\n" \
             f"{formatting(all_games)}\n" \
             f"{formatting(all_points)}\n" \
             f"Подробно:" + ("\n" * 2)
    # добавляем к ответу информацию по квизам
    for kviz in info_on_games:
        if kviz.points > 0:
            answer += f"{kviz.name_kviz}\n" \
                      f"Всего: {formatting(kviz.points_str)} бал.\n" \
                      f"Всего игр: {formatting(kviz.games_str)}\n" \
                      f"Среднее: {formatting(kviz.average)}" + ("\n" * 2)
        else:
            answer += f"{Connector.name_kviz.get(kviz.name_kviz)}: 0 бал.\n"

    await bot.send_message(message.from_user.id, answer)  # ответ пользователю
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
