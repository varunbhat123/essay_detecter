from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def _detect_score(essay: str) -> dict:
    response = client.post("/api/detect", json={"essay": essay})
    assert response.status_code == 200
    return response.json()


def test_detect_endpoint():
    response = client.post("/api/detect", json={"essay": "This is a simple test essay. It has multiple sentences. It should return a valid response."})
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert "overall_score" in data
    assert "sentence_highlights" in data
    assert len(data["sentence_highlights"]) == 3
    assert data["sentence_highlights"][0]["sentence"] == "This is a simple test essay."


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "AI Essay Detector"}


def test_detector_score_ordering_for_human_ai_and_mixed_essays():
    human_essay = (
        "I still remember the first time I stood in the lab and realized how much I wanted to understand the world through science. "
        "The process was messy and uncertain, but every failed experiment taught me to look more carefully, ask better questions, and keep going. "
        "When I solved a small problem on my own, it felt like a door opening, not because I had the perfect answer, but because I had learned how to think. "
        "That is the kind of patient curiosity I want to carry into college and beyond."
    )
    mixed_essay = (
        "I am deeply interested in research and problem-solving, and I have worked hard to improve my skills through practice and reflection. "
        "My goals are to explore science, contribute to meaningful projects, and develop a thoughtful understanding of complex issues. "
        "I believe this path will help me grow both personally and academically while preparing me for future challenges."
    )
    ai_style_essay = (
        "I am deeply committed to innovation and excellence because innovation drives progress and excellence creates opportunity. "
        "I value creativity, resilience, and leadership because these qualities enable meaningful impact and long-term success. "
        "Therefore, I believe my dedication to learning, collaboration, and problem-solving will allow me to contribute meaningfully to society. "
        "Moreover, I seek to develop my skills with purpose, perseverance, and a clear commitment to growth."
    )

    human_result = _detect_score(human_essay)
    mixed_result = _detect_score(mixed_essay)
    ai_result = _detect_score(ai_style_essay)

    assert human_result["overall_score"] < mixed_result["overall_score"] < ai_result["overall_score"]
    assert human_result["prediction"] in {"Likely Human Written", "Suspicious"}
    assert ai_result["prediction"] in {"Suspicious", "Likely AI Generated"}
    assert ai_result["overall_score"] >= mixed_result["overall_score"]

