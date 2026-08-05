from app.utils.feature_extractor import extract_features_from_text


class FeatureService:
    """Service layer for text feature extraction."""

    def extract(self, essay: str):
        return extract_features_from_text(essay)
