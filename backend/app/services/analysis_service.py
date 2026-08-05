class AnalysisService:
    """Placeholder service for essay analysis."""

    async def analyze(self, essay: str) -> dict[str, object]:
        return {
            "prediction": "pending",
            "confidence": 0.0,
            "summary": "AI detection logic is not implemented yet.",
            "word_count": len(essay.split()),
            "character_count": len(essay),
            "status": "placeholder",
        }
