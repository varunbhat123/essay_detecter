from pydantic import BaseModel, Field


class EssayRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Essay text to analyze")


class EssayResponse(BaseModel):
    score: float = Field(..., description="Estimated AI likelihood score")
    label: str = Field(..., description="Predicted label")
    explanation: str = Field(..., description="High-level explanation for the result")
