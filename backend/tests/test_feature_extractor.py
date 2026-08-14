from app.utils.feature_extractor import extract_features_from_text, _split_sentences, _count_passive_voice

def test_split_sentences():
    text = "Hello world. This is a test! Is it working? Yes."
    sentences = _split_sentences(text)
    assert len(sentences) == 4
    assert sentences[0] == "Hello world."
    assert sentences[1] == "This is a test!"

def test_count_passive_voice():
    assert _count_passive_voice("The ball was thrown by him.") == 1
    assert _count_passive_voice("I am throwing the ball.") == 0
    assert _count_passive_voice("The cake is being baked.") == 1


def test_count_passive_voice_irregular_past_participle():
    assert _count_passive_voice("The work was thrown aside by the committee.") == 1

def test_extract_features_empty():
    features = extract_features_from_text("   ")
    assert features.sentence_count == 0

def test_extract_features():
    text = "This is a simple sentence. Another simple sentence here."
    features = extract_features_from_text(text)
    assert features.sentence_count == 2
    assert features.average_sentence_length > 0
    assert len(features.sentence_features) == 2
