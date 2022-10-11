from io import BytesIO
from os import listdir
from pathlib import Path
from random import choice
from zipfile import ZIP_DEFLATED, ZipFile

import structlog
from fastapi import APIRouter
from fastapi.responses import FileResponse, StreamingResponse

log = structlog.get_logger()

normie_router = APIRouter(prefix="/normconf", responses={404: {"description": "Auth router not found"}})

goodies_path = 'app/goodies/'
surprises = [goodies_path + file for file in listdir(Path('app/goodies/'))]
vicki = [url for url in open('app/goodies/queen.txt').read().splitlines()]

@normie_router.get('/normconf')
def get_normconf():
    """Return ASCII file of normconf
    """
    return FileResponse(Path(f'{goodies_path}normconf_ascii.txt'))


@normie_router.get('/random_goodies')
def random_goodies():
    """Return random goodie file from goodies directory
    """
    goodie = choice(surprises)

    if goodie.endswith('.png'):
        return FileResponse(goodie, media_type='image/png', filename=goodie[len(goodies_path):])

    return FileResponse(goodie)


@normie_router.get('/allthegoodies')
def get_goodies():
    """Return all the goodes from goodies directory
    """

    goodies_len = len(goodies_path)
    zip_io = BytesIO()
    with ZipFile(zip_io, mode='w', compression=ZIP_DEFLATED) as temp_zip:
        for file in surprises:
            temp_zip.write(file, file[goodies_len:])

    return StreamingResponse(iter([zip_io.getvalue()]),
                             media_type="application/x-zip-compressed", 
                             headers = { "Content-Disposition": f"attachment; filename=allthegoodies.zip"}
                            )

@normie_router.get('/queen_vicki')
def queen():
    """Return link from Vicki's site
    """
    site = choice(vicki)

    return site