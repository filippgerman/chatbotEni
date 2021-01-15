def number_games_str(number):
    """
    :param number: int кол-во игр в квизе
    :return: str ответ для пользоваеля, с правельным склонением
    """
    if number == 1:
        return 'в 1 квизе'
    else:
        return f'в {number} квизах'


def remove_line(text):
    """
    :param text: str принимает строку
    :return: str строку без первого слеша
    """
    if '/' in text:
        return text.replace('/', '', 1)
    return text


def remove_spaces(name):
    """
    :param name: str название команды
    :return: str название команды без пробелов в строке
    """
    return ' '.join(name.split())


def formatting(text):
    """
    проверяет есть ли лишние пробелы или слеши и убирает их
    :param text: str текст
    :return: str
    """
    return remove_spaces(remove_line(text))
