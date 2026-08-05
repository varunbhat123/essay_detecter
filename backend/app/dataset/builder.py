from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import pandas as pd


@dataclass
class DatasetRow:
    text: str
    source_label: str
    source_file: str
    sentence_count: int
    word_count: int
    character_count: int
    metadata: dict[str, str | int | float] = field(default_factory=dict)


class EssayDatasetBuilder:
    """Builds a cleaned, labeled dataset for training and evaluation."""

    def __init__(self, root_dir: str | Path | None = None) -> None:
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.dataset_dir = self.root_dir / "dataset"
        self.human_dir = self.dataset_dir / "human"
        self.ai_dir = self.dataset_dir / "ai"

    def load_essays(self, folder: str | Path) -> list[Path]:
        path = Path(folder)
        if not path.exists():
            return []
        return sorted(path.rglob("*"))

    def clean_text(self, text: str) -> str:
        cleaned = text.replace("\r", " ")
        cleaned = cleaned.replace("\n", " ")
        cleaned = " ".join(cleaned.split())
        return cleaned.strip()

    def split_into_sentences(self, text: str) -> list[str]:
        normalized = re.sub(r"\s+", " ", text).strip()
        parts = re.split(r"(?<=[.!?])\s+", normalized)
        return [part.strip() for part in parts if part.strip()]

    def store_metadata(self, text: str, source_label: str, source_file: str) -> dict[str, str | int | float]:
        sentences = self.split_into_sentences(text)
        return {
            "source_label": source_label,
            "source_file": source_file,
            "sentence_count": len(sentences),
            "word_count": len(text.split()),
            "character_count": len(text),
        }

    def build_rows(self, folder: str | Path, label: str) -> list[DatasetRow]:
        rows: list[DatasetRow] = []
        for file_path in self.load_essays(folder):
            if not file_path.is_file():
                continue
            text = file_path.read_text(encoding="utf-8", errors="ignore")
            cleaned = self.clean_text(text)
            if not cleaned:
                continue
            metadata = self.store_metadata(cleaned, label, str(file_path.name))
            rows.append(
                DatasetRow(
                    text=cleaned,
                    source_label=label,
                    source_file=str(file_path.name),
                    sentence_count=int(metadata["sentence_count"]),
                    word_count=int(metadata["word_count"]),
                    character_count=int(metadata["character_count"]),
                    metadata=metadata,
                )
            )
        return rows

    def to_dataframe(self, rows: Iterable[DatasetRow]) -> pd.DataFrame:
        records = []
        for row in rows:
            records.append(
                {
                    "text": row.text,
                    "source_label": row.source_label,
                    "source_file": row.source_file,
                    "sentence_count": row.sentence_count,
                    "word_count": row.word_count,
                    "character_count": row.character_count,
                    **row.metadata,
                }
            )
        return pd.DataFrame(records)

    def save_split(self, dataframe: pd.DataFrame, output_path: str | Path) -> None:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        dataframe.to_csv(output, index=False)

    def generate_splits(self, dataframe: pd.DataFrame, train_ratio: float = 0.7, val_ratio: float = 0.15, test_ratio: float = 0.15) -> dict[str, pd.DataFrame]:
        if abs(train_ratio + val_ratio + test_ratio - 1.0) > 1e-9:
            raise ValueError("Train, validation, and test ratios must sum to 1.0")

        shuffled = dataframe.sample(frac=1, random_state=42).reset_index(drop=True)
        train_end = int(len(shuffled) * train_ratio)
        val_end = train_end + int(len(shuffled) * val_ratio)

        train_df = shuffled.iloc[:train_end].reset_index(drop=True)
        val_df = shuffled.iloc[train_end:val_end].reset_index(drop=True)
        test_df = shuffled.iloc[val_end:].reset_index(drop=True)

        return {
            "train": train_df,
            "validation": val_df,
            "test": test_df,
        }

    def build_dataset(self) -> dict[str, pd.DataFrame]:
        human_rows = self.build_rows(self.human_dir, "human")
        ai_rows = self.build_rows(self.ai_dir, "ai")
        all_rows = human_rows + ai_rows
        dataframe = self.to_dataframe(all_rows)
        return self.generate_splits(dataframe)

    def save_dataset(self, output_dir: str | Path) -> dict[str, pd.DataFrame]:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        splits = self.build_dataset()
        for name, frame in splits.items():
            self.save_split(frame, output_path / f"{name}.csv")
        return splits
