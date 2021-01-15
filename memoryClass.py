from databases import *
from format import remove_spaces


class Connector:
    """
    Основной класс взаиможействи с БД, получения информации по команде
    """
    name_db = [Einstein, KvizPlease, Kvizium, Mozgoboy, Mozgva, Squiz]  # список всех таблиц в БД.

    def __init__(self, text):
        self.text = text  # название команды которое передает ползователь

    def get(self):
        """
        :return: список объектов, класса Data,со всей инф. по команде
        """
        answer_data = []  # ответ отсортированный список объектов Data
        names_team = self.text.split('+')  # название команд
        for db in self.name_db:  # проверяем по всем БД
            obj = Data(0, 0, db.__tablename__)  # создаем пустой объект

            for name in names_team:  # движемся по названием команд
                name = remove_spaces(name)  # (исп. метод format_name, убирает пробелы в имени)

                if session.query(db).filter_by(name=name).count():  # проверяем есть ли такая команда в БД
                    for i in session.query(db).filter_by(name=name):
                        obj.games += i.number_game  # складываем знаяения команд, из одной БД
                        obj.points += i.points

            answer_data.append(obj)  # добавляем объект в список
            # сортируем список по кол-ву игр, и по алфавиту
            answer_data = sorted(answer_data, key=lambda data: (-data.games, data.name_kviz))

        return answer_data


class Data:
    """
    Класс - шаблон для хранения информации
    """

    def __init__(self, games, points, name_kviz):
        self.games = games  # кол-во игр
        self.points = points  # кол-во очков
        self.name_kviz = name_kviz  # название БД

    def __repr__(self):
        return f"{self.games=} {self.points=} {self.name_kviz=}"
