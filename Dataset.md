# Dataset

## Dataset purpose

The dataset layer supports two things:

1. collecting raw essays into a structured format
2. evaluating a detector against labeled examples

The project expects both human-written and AI-generated examples to be stored separately so that labels can be inferred from the directory or metadata.

## Recommended folder layout

```text
backend/dataset/
├── human/
│   ├── essay_01.txt
│   ├── essay_02.txt
│   └── ...
├── ai/
│   ├── essay_01.txt
│   ├── essay_02.txt
│   └── ...
└── splits/
    ├── train.csv
    ├── validation.csv
    └── test.csv
```

## Supported input types

The dataset builder and evaluator support:

- plain text files like .txt
- markdown files like .md
- CSV files with columns such as text and source_label

For plain text files, the parent folder name is interpreted as the label when possible.

## Label conventions

The project uses simple binary labels:

- human
- ai

These labels are normalized to lowercase before evaluation.

## Data model

The dataset builder creates rows with metadata such as:

- text
- source_label
- source_file
- sentence_count
- word_count
- character_count
- metadata

This is used for both structured CSV generation and evaluation.

## Dataset builder behavior

The builder does the following:

- reads all files in the human and AI source folders
- normalizes whitespace and removes escaped line breaks
- strips empty content
- splits text into sentences
- stores metadata about each essay
- shuffles the dataset and generates train, validation, and test splits
- writes the splits as CSV files

## Evaluating on a dataset folder

The evaluation route accepts a dataset directory path and predicts labels for each row or file. It compares predictions to known labels and returns:

- accuracy
- precision
- recall
- F1 score
- confusion matrix
- number of samples

## Best practices

- Keep the human and AI folders balanced.
- Use a consistent essay format and clean file encoding.
- Make sure labels are accurate and consistent.
- Prefer a dedicated validation and test set for measuring generalization.

## Future dataset work

The template is ready for larger corpora, stronger labeling, and more robust training pipelines. As the project evolves, the dataset may also include metadata such as essay prompt, source institution, or date of generation.
