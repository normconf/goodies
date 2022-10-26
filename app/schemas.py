from typing import Any, List

from pydantic import BaseModel, Field

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


class GetTalkRequest(BaseModel):
    talk_title: str = Field(title="Talk Title", description="Enter a talk title and receive its contents!")

class TalkResponse(BaseModel):
    talk_content: str = Field(title="Talk Content", description="The conent of a talk, before it even happens!")