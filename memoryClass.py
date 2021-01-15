from databases import *


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
        pacifiers = []  # список пустых квизов, для сортировки, и дальнейшем слиянием с answer_data
        for database in self.name_db:
            if session.query(database).filter_by(name=self.text).count():  # проверка, есть ли такая команда в БД.
                for i in session.query(database).filter_by(name=self.text):  # находим такую запись в БД.
                    # создаем объект класса Data и добавляем ее в список
                    answer_data.append(Data(i.number_game, i.points, i.__tablename__))
            else:  # если записи нет, значит создавем пустышку класса Data
                pacifiers.append(Data(0, 0, database.__tablename__))

        answer_data = sorted(answer_data, key=lambda data: data.games,
                             reverse=True)  # сортируем список по убыванию (кол-во игр)
        pacifiers = sorted(pacifiers, key=lambda data: data.name_kviz)  # сортируем список по алфавиту
        answer_data.extend(pacifiers)  # слияние двух списков

        return answer_data


class Data:
    """
    Класс - шаблон для хранения информации
    """

    def __init__(self, games, points, name_kviz):
        self.games = games
        self.points = points
        self.name_kviz = name_kviz
