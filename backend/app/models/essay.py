from pydantic import BaseModel, Field


class EssayRequest(BaseModel):
    essay: str = Field(..., min_length=1, description="Essay text to analyze")


class EssayResponse(BaseModel):
    prediction: str = Field(..., description="Prediction label")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Prediction confidence score")
    summary: str = Field(..., description="Analysis summary")
    word_count: int = Field(..., ge=0, description="Word count of the essay")
    character_count: int = Field(..., ge=0, description="Character count of the essay")
    status: str = Field(..., description="Processing status")
