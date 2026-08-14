from pathlib import Path

from fastapi import APIRouter

from app.evaluation.evaluator import DatasetEvaluator

router = APIRouter(prefix="/api", tags=["evaluation"])

evaluator = DatasetEvaluator()


@router.post("/evaluate")
async def evaluate_dataset(payload: dict[str, str | float]) -> dict[str, object]:
    dataset_dir = payload.get("dataset_dir", "dataset")
    positive_label = str(payload.get("positive_label", "ai")).lower()
    threshold = float(payload.get("threshold", 0.5))
    result = evaluator.evaluate_dataset(Path(dataset_dir), positive_label=positive_label, threshold=threshold)
    return result
