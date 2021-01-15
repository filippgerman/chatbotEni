class Statistics:
    def __init__(self, name_kviz):
        self.name_kviz = name_kviz
        self.points_str = ''
        self.games_str = ''
        self.games = 0
        self.points = 0
        self.average = ''

    def __repr__(self):
        return self.name_kviz

    def add_points(self, points):
        self.points_str += str(f" / {points}")
        self.points += points

    def add_games(self, games):
        self.games_str += str(f" / {games}")
        self.games += games

    def average_str(self):
        self.average += str(f" / {self.get_average()}")

    def get_average(self):
        if self.points > 0:
            return round((self.points / self.games), 2)
        else:
            return 0
