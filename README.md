# AI Admissions Essay Detector

An explainable, full-stack prototype for reviewing linguistic signals in admissions essays. It estimates an AI-likelihood score from text features and local language-model perplexity; it does not prove that an essay was written by AI and should not be used as the sole basis for high-stakes decisions.

## Main features

- Essay input and sentence-level highlighting in a Next.js interface.
- FastAPI endpoints for essay analysis, detection, health checks, and dataset evaluation.
- Explainable linguistic features, including lexical diversity, repetition, transitions, readability, entropy, burstiness, and sentence complexity.
- Local GPT-2 perplexity as one signal in a heuristic score.
- Dataset building and evaluation utilities for labeled human and AI text samples.

## Technology stack

- Frontend: Next.js 15, React 19, TypeScript, Tailwind CSS.
- Backend: Python, FastAPI, Pydantic, Uvicorn.
- NLP and evaluation: Transformers, PyTorch, scikit-learn, spaCy, NLTK, textstat, pandas, and NumPy.

## Architecture

The `frontend/` application collects essay text and calls the backend API. The `backend/` FastAPI application extracts sentence and essay features, calculates GPT-2 perplexity, applies the heuristic scoring engine, and returns an overall result with sentence highlights. Dataset utilities build labeled splits and the evaluator reports classification metrics for a supplied dataset.

## Backend setup

Use a supported Python environment (Python 3.12 is the available local development version):

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Optional settings are documented in `backend/.env.example`. On first use, Transformers may download the GPT-2 model into its local cache.

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

The frontend reads `NEXT_PUBLIC_API_BASE_URL` from `frontend/.env.local` and defaults to `http://localhost:8000`.

## API endpoints

- `GET /` — service metadata.
- `GET /api/health` — health check.
- `POST /api/detect` — full detection response with sentence highlights. Request body: `{ "essay": "..." }`.
- `POST /api/analyze` — summary analysis. Request body: `{ "essay": "..." }`.
- `POST /api/evaluate` — evaluates a supplied labeled dataset directory.

## Detection approach

The detector is a heuristic, not a trained binary classifier. It extracts sentence-level features, computes local GPT-2 perplexity, combines normalized signals with fixed weights, classifies each sentence as `likely_human`, `suspicious`, or `likely_ai`, and averages sentence scores for the essay-level score. Results are signals for review, not authorship determinations.

## Dataset information

The dataset builder expects source samples under `backend/dataset/human/` and `backend/dataset/ai/`. It writes train, validation, and test CSV splits under `backend/dataset/splits/`.

Run the builder from the backend directory:

```bash
python scripts/build_dataset.py
```

The evaluator accepts `.txt`, `.md`, and CSV inputs containing `text` and `source_label` fields. Root-level `data/` and `models/` directories are retained for local artifacts; `.gitkeep` preserves them when empty.

## Testing

Backend tests are in `backend/tests/`. Install the test runner in the active backend environment, then run:

```bash
cd backend
pip install pytest
pytest tests/
```

The frontend provides linting and build scripts:

```bash
cd frontend
npm run lint
npm run build
```

## Current limitations

- The scoring thresholds and weights have not been validated as an admissions-grade detector.
- Perplexity and style signals can produce false positives and false negatives.
- Results depend on representative, accurately labeled evaluation data.
- The current implementation is not a substitute for privacy, policy, legal, or human-review processes.

## Future improvements

- Validate and calibrate the scoring approach on held-out datasets.
- Add supervised models only after establishing robust dataset and evaluation practices.
- Improve dataset validation, error reporting, and evaluation metrics.
- Add performance safeguards, privacy controls, and audit capabilities before production use.
