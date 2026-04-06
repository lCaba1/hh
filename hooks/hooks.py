from fastapi import Request
from fastapi.responses import JSONResponse

from exceptions.exceptions import (
    OwnerNotFoundException, OwnerHasHorsesException,
    HorseNotFoundException, HorseHasResultsException,
    JockeyNotFoundException, JockeyHasResultsException,
    RaceNotFoundException, RaceHasResultsException,
    RaceResultNotFoundException, HorseAlreadyInRaceException, JockeyAlreadyInRaceException
)


async def owner_not_found_handler(request: Request, exc: OwnerNotFoundException):
    return JSONResponse(status_code=404, content={"message": str(exc) or "Владелец не найден"})


async def owner_has_horses_handler(request: Request, exc: OwnerHasHorsesException):
    return JSONResponse(status_code=400, content={"message": str(exc)})


async def horse_not_found_handler(request: Request, exc: HorseNotFoundException):
    return JSONResponse(status_code=404, content={"message": str(exc) or "Лошадь не найдена"})


async def horse_has_results_handler(request: Request, exc: HorseHasResultsException):
    return JSONResponse(status_code=400, content={"message": str(exc)})


async def jockey_not_found_handler(request: Request, exc: JockeyNotFoundException):
    return JSONResponse(status_code=404, content={"message": str(exc) or "Жокей не найден"})


async def jockey_has_results_handler(request: Request, exc: JockeyHasResultsException):
    return JSONResponse(status_code=400, content={"message": str(exc)})


async def race_not_found_handler(request: Request, exc: RaceNotFoundException):
    return JSONResponse(status_code=404, content={"message": str(exc) or "Состязание не найдено"})


async def race_has_results_handler(request: Request, exc: RaceHasResultsException):
    return JSONResponse(status_code=400, content={"message": str(exc)})


async def race_result_not_found_handler(request: Request, exc: RaceResultNotFoundException):
    return JSONResponse(status_code=404, content={"message": str(exc) or "Результат не найден"})


async def horse_already_in_race_handler(request: Request, exc: HorseAlreadyInRaceException):
    return JSONResponse(status_code=400, content={"message": str(exc)})


async def jockey_already_in_race_handler(request: Request, exc: JockeyAlreadyInRaceException):
    return JSONResponse(status_code=400, content={"message": str(exc)})


# -------------------- REGISTRY --------------------

exception_handlers = {
    OwnerNotFoundException: owner_not_found_handler,
    OwnerHasHorsesException: owner_has_horses_handler,

    HorseNotFoundException: horse_not_found_handler,
    HorseHasResultsException: horse_has_results_handler,

    JockeyNotFoundException: jockey_not_found_handler,
    JockeyHasResultsException: jockey_has_results_handler,

    RaceNotFoundException: race_not_found_handler,
    RaceHasResultsException: race_has_results_handler,

    RaceResultNotFoundException: race_result_not_found_handler,
    HorseAlreadyInRaceException: horse_already_in_race_handler,
    JockeyAlreadyInRaceException: jockey_already_in_race_handler
}
