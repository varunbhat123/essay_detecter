from __future__ import annotations

import math
import re
from collections import Counter
from statistics import mean

import textstat

from app.models.features import EssayFeatures, SentenceFeature


TRANSITION_WORDS = {
    "however",
    "moreover",
    "therefore",
    "furthermore",
    "consequently",
    "although",
    "meanwhile",
    "nevertheless",
    "nonetheless",
    "besides",
    "similarly",
    "thus",
    "whereas",
    "otherwise",
    "in contrast",
    "on the other hand",
}


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _split_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def _tokenize_words(sentence: str) -> list[str]:
    return re.findall(r"\b[a-zA-Z]+\b", sentence.lower())


def _compute_vocabulary_diversity(words: list[str]) -> float:
    if not words:
        return 0.0
    unique_words = set(words)
    return len(unique_words) / len(words)


def _compute_lexical_richness(words: list[str]) -> float:
    if not words:
        return 0.0
    unique_words = set(words)
    return len(unique_words) / len(set(w for w in words if len(w) > 2)) if any(len(w) > 2 for w in words) else 0.0


def _compute_repeated_word_ratio(words: list[str]) -> float:
    if not words:
        return 0.0
    counts = Counter(words)
    repeated = sum(count - 1 for count in counts.values() if count > 1)
    return repeated / len(words)


def _compute_repeated_phrase_ratio(sentence: str) -> float:
    if not sentence:
        return 0.0
    tokens = _tokenize_words(sentence)
    if len(tokens) < 2:
        return 0.0
    bigrams = [" ".join(tokens[i : i + 2]) for i in range(len(tokens) - 1)]
    if not bigrams:
        return 0.0
    repeats = 0
    counts = Counter(bigrams)
    repeats = sum(count - 1 for count in counts.values() if count > 1)
    return repeats / len(bigrams)


def _compute_transition_word_frequency(sentence: str) -> float:
    tokens = _tokenize_words(sentence)
    if not tokens:
        return 0.0
    transition_count = 0
    sentence_lower = sentence.lower()
    for word in TRANSITION_WORDS:
        if word in sentence_lower:
            transition_count += sentence_lower.count(word)
    return transition_count / len(tokens)


def _count_passive_voice(sentence: str) -> int:
    irregular_participles = (
        "thrown|made|known|given|built|found|left|seen|done|shown|told|kept|written|taken|"
        "brought|chosen|driven|spoken|hidden|fed|led|felt|held|sold|taught|caught|paid|said"
    )
    pattern = (
        r"\b(?:am|is|are|was|were|be|been|being)\b"
        r"(?:\s+\w+){0,2}\s+"
        rf"(?:\w+(?:ed|en)|(?:{irregular_participles}))\b"
    )
    matches = re.findall(pattern, sentence.lower())
    return len(matches)


def _compute_punctuation_frequency(sentence: str) -> float:
    if not sentence:
        return 0.0
    punctuation_count = sum(1 for ch in sentence if ch in ",.;:!?()-[]{}\"'\n")
    return punctuation_count / len(sentence)


def _compute_capitalization_patterns(sentence: str) -> dict[str, float]:
    total = len(sentence) or 1
    upper_count = sum(1 for ch in sentence if ch.isupper())
    starts_upper = sum(1 for ch in sentence.split()[:3] if ch and ch[0].isupper())
    return {
        "uppercase_ratio": upper_count / total,
        "sentence_start_uppercase_ratio": starts_upper / max(1, len(sentence.split()[:3])),
    }


def _compute_burstiness(words: list[str]) -> float:
    if len(words) < 2:
        return 0.0
    counts = Counter(words)
    if sum(counts.values()) <= 1:
        return 0.0
    frequencies = list(counts.values())
    mean_freq = mean(frequencies)
    variance = sum((value - mean_freq) ** 2 for value in frequencies) / len(frequencies)
    return math.sqrt(variance) / (mean_freq + 1e-9)


def _compute_entropy(words: list[str]) -> float:
    if not words:
        return 0.0
    counts = Counter(words)
    total = len(words)
    entropy = 0.0
    for count in counts.values():
        probability = count / total
        entropy -= probability * math.log2(probability)
    return entropy


def _compute_sentence_complexity(sentence: str) -> float:
    words = _tokenize_words(sentence)
    if not words:
        return 0.0
    clauses = len(re.findall(r"\b(?:because|although|while|when|if|since|that|which|who)\b", sentence.lower()))
    punctuation = sum(1 for ch in sentence if ch in ",;:")
    return (len(words) + clauses + punctuation) / max(1, len(words))


def _compute_sentence_features(sentence: str, sentence_index: int) -> SentenceFeature:
    words = _tokenize_words(sentence)
    average_word_length = mean((len(word) for word in words)) if words else 0.0
    vocab_diversity = _compute_vocabulary_diversity(words)
    lexical_richness = _compute_lexical_richness(words)
    repeated_word_ratio = _compute_repeated_word_ratio(words)
    repeated_phrase_ratio = _compute_repeated_phrase_ratio(sentence)
    transition_word_frequency = _compute_transition_word_frequency(sentence)
    passive_voice_count = _count_passive_voice(sentence)
    readability_score = textstat.flesch_reading_ease(sentence)
    sentence_complexity = _compute_sentence_complexity(sentence)
    punctuation_frequency = _compute_punctuation_frequency(sentence)
    capitalization_patterns = _compute_capitalization_patterns(sentence)
    burstiness = _compute_burstiness(words)
    entropy = _compute_entropy(words)

    return SentenceFeature(
        sentence_index=sentence_index,
        sentence_text=sentence,
        sentence_length=len(sentence.split()),
        average_word_length=average_word_length,
        vocabulary_diversity=vocab_diversity,
        lexical_richness=lexical_richness,
        repeated_word_ratio=repeated_word_ratio,
        repeated_phrase_ratio=repeated_phrase_ratio,
        transition_word_frequency=transition_word_frequency,
        passive_voice_count=passive_voice_count,
        readability_score=readability_score,
        sentence_complexity=sentence_complexity,
        punctuation_frequency=punctuation_frequency,
        capitalization_patterns=capitalization_patterns,
        burstiness=burstiness,
        entropy=entropy,
    )


def extract_features_from_text(text: str) -> EssayFeatures:
    cleaned_text = _normalize_whitespace(text)
    sentences = _split_sentences(cleaned_text)

    if not sentences:
        return EssayFeatures(
            average_sentence_length=0.0,
            average_word_length=0.0,
            vocabulary_diversity=0.0,
            lexical_richness=0.0,
            repeated_word_ratio=0.0,
            repeated_phrase_ratio=0.0,
            transition_word_frequency=0.0,
            passive_voice_count=0,
            readability_score=0.0,
            sentence_complexity=0.0,
            punctuation_frequency=0.0,
            capitalization_patterns={},
            burstiness=0.0,
            entropy=0.0,
            sentence_count=0,
            sentence_features=[],
        )

    sentence_features = [
        _compute_sentence_features(sentence, index)
        for index, sentence in enumerate(sentences)
    ]

    all_words = []
    for sentence in sentences:
        all_words.extend(_tokenize_words(sentence))

    average_sentence_length = mean(item.sentence_length for item in sentence_features)
    average_word_length = mean(item.average_word_length for item in sentence_features)
    vocabulary_diversity = _compute_vocabulary_diversity(all_words)
    lexical_richness = _compute_lexical_richness(all_words)
    repeated_word_ratio = _compute_repeated_word_ratio(all_words)
    repeated_phrase_ratio = mean(item.repeated_phrase_ratio for item in sentence_features)
    transition_word_frequency = mean(item.transition_word_frequency for item in sentence_features)
    passive_voice_count = sum(item.passive_voice_count for item in sentence_features)
    readability_score = mean(item.readability_score for item in sentence_features)
    sentence_complexity = mean(item.sentence_complexity for item in sentence_features)
    punctuation_frequency = mean(item.punctuation_frequency for item in sentence_features)
    capitalization_patterns = {
        "uppercase_ratio": mean(item.capitalization_patterns["uppercase_ratio"] for item in sentence_features),
        "sentence_start_uppercase_ratio": mean(item.capitalization_patterns["sentence_start_uppercase_ratio"] for item in sentence_features),
    }
    burstiness = mean(item.burstiness for item in sentence_features)
    entropy = mean(item.entropy for item in sentence_features)

    return EssayFeatures(
        average_sentence_length=average_sentence_length,
        average_word_length=average_word_length,
        vocabulary_diversity=vocabulary_diversity,
        lexical_richness=lexical_richness,
        repeated_word_ratio=repeated_word_ratio,
        repeated_phrase_ratio=repeated_phrase_ratio,
        transition_word_frequency=transition_word_frequency,
        passive_voice_count=passive_voice_count,
        readability_score=readability_score,
        sentence_complexity=sentence_complexity,
        punctuation_frequency=punctuation_frequency,
        capitalization_patterns=capitalization_patterns,
        burstiness=burstiness,
        entropy=entropy,
        sentence_count=len(sentences),
        sentence_features=sentence_features,
    )
