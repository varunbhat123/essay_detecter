from __future__ import annotations

from app.utils.perplexity import LocalPerplexityCalculator, PerplexityScore


class PerplexityService:
    """Service for computing sentence perplexity with a local GPT-2 model."""

    def __init__(self, model_name: str = "gpt2") -> None:
        self.calculator = LocalPerplexityCalculator(model_name=model_name)

    def score_text(self, text: str) -> list[PerplexityScore]:
        sentences = [part.strip() for part in text.replace("\n", " ").split(".") if part.strip()]
        return self.calculator.score_sentences(sentences)

    def average_perplexity(self, text: str) -> float:
        sentences = [part.strip() for part in text.replace("\n", " ").split(".") if part.strip()]
        return self.calculator.average_perplexity(sentences)
