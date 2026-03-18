# backend/app/schemas/result.py

from pydantic import BaseModel


class ResultResponse(BaseModel):
    id: str

    finding: str
    confidence: float

    purpose: str        # screening / diagnostic
    preset: str         # standard / high

    image_url: str

    suggestion: str