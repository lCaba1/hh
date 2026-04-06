class RacingException(Exception):
    """Базовое исключение для системы скачек"""
    pass


class OwnerNotFoundException(RacingException):
    """Владелец не найден"""
    pass


class OwnerHasHorsesException(RacingException):
    """Нельзя удалить владельца, у которого есть лошади"""
    pass


class HorseNotFoundException(RacingException):
    """Лошадь не найдена"""
    pass


class HorseHasResultsException(RacingException):
    """Нельзя удалить лошадь, участвовавшую в состязаниях"""
    pass


class JockeyNotFoundException(RacingException):
    """Жокей не найден"""
    pass


class JockeyHasResultsException(RacingException):
    """Нельзя удалить жокея, участвовавшего в состязаниях"""
    pass


class RaceNotFoundException(RacingException):
    """Состязание не найдено"""
    pass


class RaceHasResultsException(RacingException):
    """Нельзя удалить состязание с результатами"""
    pass


class RaceResultNotFoundException(RacingException):
    """Результат состязания не найден"""
    pass


class HorseAlreadyInRaceException(RacingException):
    """Лошадь уже участвует в этом состязании"""
    pass


class JockeyAlreadyInRaceException(RacingException):
    """Жокей уже участвует в этом состязании"""
    pass
