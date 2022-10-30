from json import loads
from os import listdir
from pathlib import Path
from random import choice

import structlog
from fastapi import APIRouter
from fastapi.responses import FileResponse, PlainTextResponse, Response
from pandas import read_html
from requests import post

from app.config import get_settings
from app.schemas import GetTalkRequest, TalkResponse

log = structlog.get_logger()

normie_router = APIRouter(responses={404: {"description": "Auth router not found"}})

#### Cached at top so as to not run every curl
goodies_path = "app/goodies/media/"
surprises = [goodies_path + file for file in listdir(Path(goodies_path))]
link_path = Path("app/goodies/links.txt")
links = open(link_path).read().splitlines()


@normie_router.get("/schedule")
def get_schedule(as_markdown: bool = True, as_csv: bool = False, as_excel: bool = False):
    """Return NormConf Schedule\n

    Args:\n
        as_markdown (bool, optional): Returns scedule as markdown. Defaults to True.
        as_csv (bool, optional): Returns schedule as CSV. Defaults to False.
        as_excel (bool, optional): Returns schedule as excel. Defaults to False.

    Returns:\n
        DataFrame: Returns schedule as Pandas DataFrame
    """
    schedule = read_html("https://normconf.com/", header=0)[0]

    if sum([as_markdown, as_csv, as_excel]) != 1:
        raise ValueError("Only one file return type expected, but got multiple or none!")

    if as_csv:
        return schedule.to_csv()

    elif as_excel:
        return schedule.to_excel(
            "ye_olde_nc_schedule.xlsx", sheet_name="Ye Olde NormConf Schedule"
        )

    elif as_markdown:
        return PlainTextResponse(
            schedule.to_markdown(tablefmt="github", index=False),
            headers={"Cache-Control": "no-cache", "Content-Disposition": "inline"},
        )

    return schedule


@normie_router.get("/ascii")
def get_normconf():
    """Return ASCII file of normconf"""
    return PlainTextResponse(
        Path(f"{goodies_path}normconf_ascii.txt").read_text(),
        headers={"Cache-Control": "no-cache", "Content-Disposition": "inline"},
    )


@normie_router.get("/zen")
def get_zen():
    """Return Zen of Normcore by Vincent D. Warmerdam"""
    return PlainTextResponse(Path(f"{goodies_path}zen_of_normcore.txt").read_text())


@normie_router.post("/get_talk")
def get_talk(request: GetTalkRequest):  # -> TalkResponse:

    settings = get_settings()

    log.info(settings.hugging_face_api_key)

    assert settings.hugging_face_api_key is not None, ValueError("Huggingface key not provided.")

    API_URL = "https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": f"Bearer {settings.hugging_face_api_key}"}

    response = post(API_URL, headers=headers, json=request.talk_title)
    log.info(response)

    assert response is not None, ValueError("Huggingface Response returned none object")

    try:
        content = loads(response.text)[0]["generated_text"]
        return TalkResponse(talk_content=content)

    except ValueError as e:
        log.error(e)
        raise e


@normie_router.get("/random_goodies")
def get_random_goodie():
    """Return random goodie file from goodies directory"""
    goodie = choice(surprises)

    if goodie.endswith(".png"):
        return FileResponse(
            goodie,
            media_type="image/png",
            filename=goodie[len(goodies_path) :],
            headers={"Cache-Control": "no-cache", "Content-Disposition": "inline"},
        )

    return PlainTextResponse(
        Path(f"{goodie}").read_text(),
        headers={"Cache-Control": "no-cache", "Content-Disposition": "inline"},
    )


@normie_router.get("/wisdom")
def get_random_wisdom():
    """Get a random hand-picked link"""
    random_link = choice(links)

    return Response(random_link + "\n")
