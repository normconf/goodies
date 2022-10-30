"""
NormConf Goodies
"""
__author__ = "Ben Labaschin"
__version__ = "0.0.1"
__maintainer__ = "Ben Labaschin, Vicki Boykis"
__email__ = "benjaminlabaschin@gmail.com"

from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from app import configure_logger
from app.config import Settings, get_settings
from app.normconf import normie_router
from app.schemas import HealthCheck, HealthCheckContent

log = configure_logger()

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:8000",
    "https://localhost:8000",
    "http://localhost:443",
    "https://localhost:443",
    "http://*.normconf.com",
    "https://*.normconf.com",
    "http://normconf.com",
    "https://normconf.com",
    "http://normconf.com/*",
    "https://normconf.com/*",
    "http://api.normcomf.com:8000",
    "https://api.normcomf.com:8000",
    "http://api.normcomf.com:80",
    "https://api.normcomf.com:80",
    "http://api.normcomf.com:443",
    "https://api.normcomf.com:443",
    "http://api-inference.huggingface.co/models/gpt2",
    "https://api-inference.huggingface.co/models/gpt2",
    "http://api-inference.huggingface.co/",
    "https://api-inference.huggingface.co/" "http://api-inference.huggingface.co/*",
    "https://api-inference.huggingface.co/*",
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

def my_schema():
    openapi_schema = get_openapi(
        title="NormConf Goodies App",
        version="0.0.1",
        description="Send random goods to the normies",
        routes=app.routes,
    )
    openapi_schema["info"] = {
        "title": "NormConf Goodies App",
        "version": "0.0.1",
        "description": "Send random goods to the normies",
        "termsOfService": "https://normconf.com/",
        "contact": {
            "name": "NormConf",
            "url": "https://normconf.com/",
            "email": "benjaminlabaschin@gmail.com",
        },
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

limiter = Limiter(key_func=get_remote_address, default_limits=["1000/hour"])

# App Setup
app = FastAPI(middleware=middleware)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.openapi = my_schema

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
def root():
    return {"message": f"{get_settings().app_version}"}


# Routers
app.include_router(normie_router, tags=["normconf"])
