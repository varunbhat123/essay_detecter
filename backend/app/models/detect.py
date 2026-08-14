from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class DetectRequest(BaseModel):
    essay: str = Field(..., min_length=1, description="Essay text to analyze")


class SentenceHighlightResponse(BaseModel):
    sentence: str = Field(..., description="Original sentence text")
    score: float = Field(..., ge=0.0, le=1.0, description="AI likelihood score")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Normalized confidence score")
    status: str = Field(..., description="Sentence classification status")
    reasons: list[str] = Field(..., description="Top reasons for the score")
    extracted_features: dict[str, Any] = Field(..., description="Feature values used for the sentence")


class DetectResponse(BaseModel):
    overall_score: float = Field(..., ge=0.0, le=1.0, description="Overall AI likelihood score")
    prediction: str = Field(..., description="Overall label prediction")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Normalized confidence score")
    summary: str = Field(..., description="Short summary of the detection result")
    status: str = Field(..., description="Processing status")
    sentence_highlights: list[SentenceHighlightResponse] = Field(..., description="Sentence-level highlights and reasons")
