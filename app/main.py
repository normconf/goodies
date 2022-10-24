"""
NormConf Goodies
"""
__author__ = "Ben Labaschin"
__version__ = "1.0.0"
__maintainer__ = "Ben Labaschin"
__email__ = "benjaminlabaschin@gmail.com"


from fastapi import Depends, FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from app import configure_logger
from app.config import Settings, get_settings
from app.normconf import normie_router
from app.schemas import HealthCheck, HealthCheckContent

log = configure_logger()

settings = get_settings()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://localhost:8000",
    "https://localhost:443"
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
        max_age=3600,
    )
]

# App Setup
app = FastAPI(
            title="NormConf Goodies App",
            description="Send random goods to the normies",
            docs_url="/docs",
            openapi_url="/api",
            middleware=middleware,
            )


@app.get("/", tags=["health"], response_model=HealthCheck, name="App Health Check")
def health() -> HealthCheck:
    return HealthCheck(status_code=200, content=HealthCheckContent(status="pass", details=[]))


@app.get("/info", tags=["status"], name="Information About App Environment")
def info(settings_: Settings = Depends(get_settings)):
    if not all(x is not None for x in settings_.__dict__.values()):
        missing_keys = [key for key, val in settings_.__dict__.items() if not val]
        return {"Missing Keys:": missing_keys}

    return {
        "app_env": settings_.app_env,
        "app_version": settings_.app_version,
        "all_env_variables": True,
    }


@app.get("/v1", tags=["status"], name="V1 Status Check")
async def root():
    return {"message": f"{settings.app_version}"}


# Routers
app.include_router(normie_router, tags=["normconf"])
