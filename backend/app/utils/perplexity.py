from __future__ import annotations

import math
from dataclasses import dataclass

import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast


@dataclass
class PerplexityScore:
    sentence: str
    token_count: int
    log_likelihood: float
    perplexity: float


class LocalPerplexityCalculator:
    """Compute sentence-level perplexity using a local GPT-2 model.

    This utility calculates token probabilities only; it does not classify text
    as AI-generated or human-written.
    """

    def __init__(
        self,
        model_name: str = "gpt2",
        device: str | None = None,
        max_length: int = 1024,
    ) -> None:
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.max_length = max_length
        self.tokenizer = GPT2TokenizerFast.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

    @staticmethod
    def _safe_perplexity(log_likelihood: float, token_count: int) -> float:
        if token_count <= 0:
            return 0.0
        average_negative_log_likelihood = -log_likelihood / token_count
        return math.exp(average_negative_log_likelihood)

    @torch.no_grad()
    def score_sentence(self, sentence: str) -> PerplexityScore:
        if not sentence.strip():
            return PerplexityScore(sentence=sentence, token_count=0, log_likelihood=0.0, perplexity=0.0)

        inputs = self.tokenizer(
            sentence,
            return_tensors="pt",
            truncation=True,
            max_length=self.max_length,
        )
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        outputs = self.model(**inputs, labels=inputs["input_ids"])
        shift_logits = outputs.logits[..., :-1, :].contiguous()
        shift_labels = inputs["input_ids"][..., 1:].contiguous()

        loss_fct = torch.nn.CrossEntropyLoss(reduction="none")
        loss = loss_fct(
            shift_logits.view(-1, shift_logits.size(-1)),
            shift_labels.view(-1),
        )
        token_loss = loss.view(shift_labels.size(0), -1)
        sentence_log_likelihood = -token_loss.sum(dim=1).item()
        token_count = shift_labels.numel()

        return PerplexityScore(
            sentence=sentence,
            token_count=token_count,
            log_likelihood=sentence_log_likelihood,
            perplexity=self._safe_perplexity(sentence_log_likelihood, token_count),
        )

    def score_sentences(self, sentences: list[str]) -> list[PerplexityScore]:
        return [self.score_sentence(sentence) for sentence in sentences]

    def average_perplexity(self, sentences: list[str]) -> float:
        scored = self.score_sentences(sentences)
        if not scored:
            return 0.0
        return sum(item.perplexity for item in scored) / len(scored)
