from typing import Any, List

from pydantic import BaseModel

########## Health Schemas ############  # noqa: E266


class HealthCheckContent(BaseModel):
    """Content for HealthCheck response containing endpoint health details"""

    status: str
    description: str = "Basic Model Health Check"
    details: List[Any]


class HealthCheck(BaseModel):
    """Response returned by `/health` endpoint."""

    status_code: int
    media_type: str = "application/health+json"
    content: HealthCheckContent
