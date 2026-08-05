from pathlib import Path

from app.dataset.builder import EssayDatasetBuilder


if __name__ == "__main__":
    builder = EssayDatasetBuilder()
    splits = builder.save_dataset(Path("dataset/splits"))
    print(f"Generated {len(splits['train'])} train rows")
    print(f"Generated {len(splits['validation'])} validation rows")
    print(f"Generated {len(splits['test'])} test rows")
