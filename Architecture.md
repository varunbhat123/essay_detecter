# Architecture

## System architecture

The application follows a simple but modular full-stack design:

- The frontend handles user interaction and visual presentation.
- The backend provides the processing API and implements the detection logic.
- The detection pipeline is built from feature extraction, perplexity scoring, and heuristic classification.
- The evaluation module compares predictions against labeled dataset samples.

## Frontend architecture

The frontend is built with Next.js and the App Router. The main page renders a dark-themed essay input interface. The main user flow is:

1. User enters or pastes an essay.
2. The interface counts words and characters.
3. The user triggers analysis.
4. The frontend calls the backend detection endpoint.
5. The returned sentence-level highlights and overall score are displayed.

The frontend is intentionally thin and designed to consume structured JSON responses from the backend rather than doing detection logic in the browser.

## Backend architecture

The backend is organized into modules by responsibility:

```text
backend/app/
├── core/
│   └── config.py
├── routes/
│   ├── analyze.py
│   ├── detect.py
│   ├── evaluate.py
│   └── health.py
├── detector/
│   ├── engine.py
│   └── scoring.py
├── models/
│   ├── detection.py
│   └── features.py
├── utils/
│   ├── feature_extractor.py
│   └── perplexity.py
├── evaluation/
│   └── evaluator.py
├── dataset/
│   ├── builder.py
│   └── __init__.py
├── main.py
└── ...
```

### Route layer

Routes expose key API endpoints:

- /api/health for service health checks
- /api/detect for essay analysis
- /api/evaluate for dataset benchmarking

### Detector layer

The detector contains the heuristic scoring engine. It calculates sentence-level scores and maps them to statuses, while preserving explainability.

### Feature layer

The feature extractor computes sentence metrics and essay aggregates from raw text. This keeps detection logic decoupled from text parsing logic.

### Evaluation layer

The evaluation module uses a dataset directory, compares predictions to labels, and reports metrics such as accuracy, precision, recall, F1, and confusion matrix.

## Processing flow

When a user submits text, the following pipeline runs:

1. Text is normalized and sentence-split.
2. Sentence features are extracted.
3. Sentence perplexity is computed via the local GPT-2 model.
4. Scores are combined using weighted signals.
5. A sentence-level status is assigned.
6. The overall essay score is aggregated.
7. The result is returned as structured JSON.

## Design principles

- Explainability: scores are based on identifiable features rather than opaque model outputs.
- Modularity: each responsibility lives in its own module.
- Extensibility: adding a different model or new features is straightforward.
- Dataset readiness: the system can evaluate on folders of labeled text samples.

## Trade-offs

This design keeps the model transparent and easy to debug, but it also means the detection algorithm is a stylized heuristic rather than a fully learned classifier. That makes it flexible for experimentation but less robust than an end-to-end trained model.
