# AI Essay Detector Backend

This directory contains the FastAPI backend for the AI Essay Detector.

## Structure

```text
backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── dataset/
│   ├── detector/
│   ├── domain/
│   ├── evaluation/
│   ├── infrastructure/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── __init__.py
│   └── main.py
├── dataset/
│   ├── human/
│   ├── ai/
│   └── splits/
│       ├── train.csv
│       ├── validation.csv
│       └── test.csv
├── scripts/
│   └── build_dataset.py
├── requirements.txt
├── .env.example
└── README.md
```

## Dataset folder expectations

Place essay source files into either of these folders:

- `dataset/human/` for human-authored text samples
- `dataset/ai/` for AI-generated samples

The builder will:

1. read each file,
2. clean and normalize the text,
3. split it into sentences,
4. compute metadata,
5. generate train/validation/test CSV files under `dataset/splits/`.

## Running the dataset builder

```bash
python scripts/build_dataset.py
```

This script loads essays and creates train/validation/test splits in `dataset/splits/`.

## Environment

Copy `.env.example` to `.env` and update values as needed.

## Run locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
