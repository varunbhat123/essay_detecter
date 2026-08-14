# AI Detector for Admissions Essays

An AI-assisted admissions essay analysis application that evaluates
essay text and provides an estimated AI-generation likelihood.

## Tech Stack

-   Frontend: Next.js 15 + React + TypeScript
-   Backend: Python + FastAPI + Uvicorn
-   Detection: feature-based scoring and ML-oriented text analysis
-   API: REST

> **Important:** This detector provides a heuristic AI-likelihood
> signal. It is not definitive proof of AI or human authorship.

## Project Structure

``` text
AI-detector-for-admissions-essays-1/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── scoring.py
│   ├── detect.py
│   ├── analysis_service.py
│   ├── feature_extractor.py
│   ├── perplexity.py
│   └── build_dataset.py
├── frontend/
│   ├── app/
│   ├── components/
│   ├── features/
│   ├── lib/
│   ├── public/
│   └── package.json
├── data/
├── models/
├── tests/
├── Architecture.md
├── Dataset.md
├── Limitations.md
└── README.md
```

## Requirements

-   Python 3.12
-   Node.js
-   npm
-   Git
-   VS Code (recommended)

## 1. Clone

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI-detector-for-admissions-essays-1
```

## 2. Backend Setup

From the project root:

``` bash
python3 -m venv .venv-mac
source .venv-mac/bin/activate
```

If `.venv-mac` already exists:

``` bash
source .venv-mac/bin/activate
```

Install backend dependencies:

``` bash
pip install -r requirements.txt
```

If `requirements.txt` is not present, install the core packages:

``` bash
pip install fastapi uvicorn pydantic pandas numpy scikit-learn textstat pytest
```

Start FastAPI:

``` bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8765
```

Backend:

``` text
http://127.0.0.1:8765
```

Swagger:

``` text
http://127.0.0.1:8765/docs
```

OpenAPI:

``` text
http://127.0.0.1:8765/openapi.json
```

## 3. Frontend Setup

Open a second terminal:

``` bash
cd frontend
npm install
```

If an environment template exists:

``` bash
cp .env.example .env.local
```

Configure the frontend API URL to use:

``` text
http://127.0.0.1:8765
```

Start Next.js:

``` bash
npm run dev
```

Frontend:

``` text
http://localhost:3000
```

## 4. Run the Full Application

### Terminal 1 --- Backend

``` bash
source .venv-mac/bin/activate
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8765
```

### Terminal 2 --- Frontend

``` bash
cd frontend
npm run dev
```

Then open:

``` text
http://localhost:3000
```

Both servers must be running for essay analysis to work.

## 5. API Endpoints

  Method   Endpoint          Purpose
  -------- ----------------- --------------------
  GET      `/`               API root
  GET      `/api/health`     Health check
  POST     `/api/analyze`    Essay analysis
  POST     `/api/detect`     AI detection
  POST     `/api/evaluate`   Dataset evaluation

### Example detection request

``` bash
curl -X POST http://127.0.0.1:8765/api/detect   -H "Content-Type: application/json"   -d '{"essay":"I have always been fascinated by computer science. Building my first small application taught me how technology can solve real problems."}'
```

The response includes:

-   `overall_score`
-   `prediction`
-   `confidence`
-   `summary`
-   `status`
-   `sentence_highlights`

Sentence-level analysis can include:

-   AI likelihood
-   confidence
-   classification status
-   reasons
-   perplexity
-   burstiness
-   vocabulary diversity
-   readability
-   entropy
-   repeated phrase ratio
-   transition frequency
-   sentence complexity
-   lexical richness

## 6. Application Flow

``` text
Essay entered by user
        ↓
Next.js frontend
        ↓
POST /api/detect
        ↓
FastAPI backend
        ↓
Text / feature analysis
        ↓
Scoring engine
        ↓
Overall + sentence-level result
        ↓
Frontend displays prediction
```

## 7. Testing

Backend tests:

``` bash
pytest
```

Frontend production build:

``` bash
cd frontend
npm run build
```

Before committing, verify both backend tests and frontend build
successfully.

## 8. Git / GitHub

Do **not** commit:

``` text
.venv/
.venv-mac/
__pycache__/
.pytest_cache/
.next/
node_modules/
.env
.env.local
```

Commit:

-   source code
-   `requirements.txt`
-   `package.json`
-   `package-lock.json`
-   configuration templates such as `.env.example`
-   tests
-   documentation
-   required model artifacts

The repository should be reproducible without uploading local virtual
environments or dependency folders.

## 9. Troubleshooting

### Port 8765 already in use

``` bash
lsof -i :8765
```

Stop the old backend process, then start Uvicorn again.

### Port 3000 already in use

``` bash
lsof -i :3000
```

Stop the old Next.js process or use the port automatically selected by
Next.js.

### Frontend says `Failed to fetch`

1.  Confirm the backend is running.
2.  Open `http://127.0.0.1:8765/docs`.
3.  Check `.env.local`.
4.  Confirm the frontend points to `http://127.0.0.1:8765`.
5.  Restart the frontend after environment changes.

## 10. Documentation

-   `Architecture.md` --- system architecture
-   `Dataset.md` --- dataset information
-   `Limitations.md` --- detector limitations

## 11. Detection Limitations

AI detection is probabilistic. Human writing can resemble AI-generated
writing, and AI-generated writing can resemble human writing.

Results can vary with:

-   essay length
-   writing style
-   vocabulary
-   sentence structure
-   paraphrasing
-   readability
-   model-generated text style

The detector should therefore be used as a screening/support tool and
not as the sole basis for an admissions decision.

## 12. Quick Start

``` bash
# Terminal 1
source .venv-mac/bin/activate
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8765
```

``` bash
# Terminal 2
cd frontend
npm install
npm run dev
```

Open:

``` text
http://localhost:3000
```

## License

Add the project's chosen license here before public distribution.
