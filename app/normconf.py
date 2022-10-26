from io import BytesIO
from pathlib import Path
from random import choice
from zipfile import ZIP_DEFLATED, ZipFile
from requests import post

import structlog
from fastapi import APIRouter
from fastapi.responses import FileResponse, StreamingResponse
from pandas import read_html

from app import surprises
from app.config import get_settings

log = structlog.get_logger()
settings = get_settings()

normie_router = APIRouter(responses={404: {"description": "Auth router not found"}})

goodies_path = 'app/goodies/'

@normie_router.get('/schedule')
def get_schedule(as_markdown:bool=True, as_csv:bool=False, as_excel:bool=False):
    """Return NormConf Schedule\n

    Args:\n
        as_markdown (bool, optional): Returns scedule as markdown. Defaults to True.
        as_csv (bool, optional): Returns schedule as CSV. Defaults to False.
        as_excel (bool, optional): Returns schedule as excel. Defaults to False.

    Returns:\n
        DataFrame: Returns schedule as Pandas DataFrame
    """
    schedule = read_html('https://normconf.com/', header=0)[0]

    if sum([as_markdown, as_csv, as_excel]) != 1:
        raise ValueError("Only one file return type expected, but got multiple or none!")

    if as_csv:
        return schedule.to_csv()

    elif as_excel: 
        return schedule.to_excel("ye_olde_nc_schedule.xlsx", sheet_name='Ye Olde NormConf Schedule')  

    elif as_markdown:
        return schedule.to_markdown(tablefmt="github", index=False)

    return schedule

@normie_router.get('/normconf')
def get_normconf():
    """Return ASCII file of normconf
    """
    return FileResponse(Path(f'{goodies_path}normconf_ascii.txt'))


@normie_router.get('/zen')
def get_zen():
    """Return Zen of Normcore by Vincent D. Warmerdam
    """
    return FileResponse(Path(f'{goodies_path}zen_of_normcore.txt'))

@normie_router.get('/get_talk')
def get_talk(payload:str):
    
    API_URL = "https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": f"Bearer {settings.hugging_face_api_key}"}
    
    response = post(API_URL, headers=headers, json=payload)    
        
    return response.json()


@normie_router.get('/random_goodies')
def get_random_goodie():
    """Return random goodie file from goodies directory
    """
    goodie = choice(surprises)

    if goodie.endswith('.png'):
        return FileResponse(goodie,
                            media_type='image/png',
                            filename=goodie[len(goodies_path):],
                            headers={'Cache-Control': 'no-cache'})

    return FileResponse(Path(f'{goodie}'), headers={'Cache-Control': 'no-cache'})


@normie_router.get('/allthegoodies')
def get_goodies():
    """Return all the goodes from goodies directory
    """

    goodies_len = len(goodies_path)
    zip_io = BytesIO()
    with ZipFile(zip_io, mode='w', compression=ZIP_DEFLATED) as temp_zip:
        for file in surprises:
            if "rickroll" in file:
                continue
            temp_zip.write(file, file[goodies_len:])

    return StreamingResponse(iter([zip_io.getvalue()]),
                             media_type="application/x-zip-compressed", 
                             headers = { "Content-Disposition": f"attachment; filename=allthegoodies.zip"}
                            )


