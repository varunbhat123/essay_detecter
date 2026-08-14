from app.evaluation.evaluator import (
    compute_accuracy,
    compute_confusion_matrix,
    compute_f1_score,
    compute_precision,
    compute_recall,
    generate_evaluation_report,
)


def test_metric_helpers() -> None:
    y_true = ["human", "human", "ai", "ai"]
    y_pred = ["human", "ai", "ai", "ai"]

    assert compute_accuracy(y_true, y_pred) == 0.75
    assert compute_precision(y_true, y_pred, positive_label="ai") == 0.6666666666666666
    assert compute_recall(y_true, y_pred, positive_label="ai") == 1.0
    assert compute_f1_score(y_true, y_pred, positive_label="ai") == 0.8

    matrix = compute_confusion_matrix(y_true, y_pred, labels=["human", "ai"])
    assert matrix.tolist() == [[1, 1], [0, 2]]

    report = generate_evaluation_report(y_true, y_pred, labels=["human", "ai"], positive_label="ai")
    assert report["accuracy"] == 0.75
    assert report["precision"] == 0.6666666666666666
    assert report["recall"] == 1.0
    assert report["f1_score"] == 0.8
