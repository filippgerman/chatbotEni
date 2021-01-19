class Statistics:
    """
    Класс необходим для содержания информации, перед отправкой пользователю.
    """

    def __init__(self, name_kviz):
        self.name_kviz = name_kviz
        self.points_str = ''
        self.games_str = ''
        self.games = 0
        self.points = 0
        self.average = ''

    def __repr__(self):
        return f"{self.name_kviz} кол-во очков: {self.points} кол-во игр: {self.games}  среднее: {self.average}"

    def add_points(self, points):
        """
        :param points: int кол-во очков команды
        """
        self.points_str += str(f" / {points}")
        self.points += points

    def add_games(self, games):
        """
        :param games: int кол-во игр команды
        """
        self.games_str += str(f" / {games}")
        self.games += games

    def add_average(self, average):
        """
        :param average: среднее кол-во балов
        """
        self.average += str(f" / {average}")
