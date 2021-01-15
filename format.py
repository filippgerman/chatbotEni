def number_games_str(number):
    """
    :param number: int кол-во игр в квизе
    :return: str ответ для пользоваеля, с правельным склонением
    """
    if number == 1:
        return 'в 1 квизе'
    else:
        return f'в {number} квизах'
