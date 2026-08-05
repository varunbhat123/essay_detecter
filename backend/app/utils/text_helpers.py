def count_words(text: str) -> int:
    return len(text.split()) if text.strip() else 0


def count_characters(text: str) -> int:
    return len(text)
