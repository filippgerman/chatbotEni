from memoryClass import Connector
from format import number_games_str, remove_line, remove_spaces, formatting
from statistic import Statistics

text = 'МНВС/Сделай счастливое лицо'

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
    info_on_games.append(Statistics(db.__tablename__))

for name in text.split('/'):
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

answer = f"Команда: {text}\n" \
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
        answer += f"{kviz.name_kviz}: 0 бал.\n"

print(answer)
