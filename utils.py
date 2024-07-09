from exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError
from datetime import datetime


def data_processing(data):
    titles = data.get("titles", 0)
    first_cup = data.get("first_cup", "")

    if titles < 0:
        raise NegativeTitlesError("titles cannot be negative")

    try:
        first_cup_date = datetime.strptime(first_cup, "%Y-%m-%d")
    except ValueError:
        raise InvalidYearCupError("there was no world cup this year")

    if first_cup_date.year < 1930 or not first_cup_date.year % 4 == 2:
        raise InvalidYearCupError("there was no world cup this year")

    years_since_first_cup = datetime.now().year - first_cup_date.year
    max_possible_titles = years_since_first_cup // 4

    if titles > max_possible_titles:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")

    return "Data processada com sucesso!"
