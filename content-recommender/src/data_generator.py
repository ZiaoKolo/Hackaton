# -*- coding: utf-8 -*-
"""Legacy entrypoint.

Dataset generation logic is implemented in `src/dataset_builder.py`.

Regenerate datasets:
    python src/data_generator.py
"""


from __future__ import annotations

from pathlib import Path

from src.dataset_builder import write_users_raw_and_clean


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    write_users_raw_and_clean(
        root / "data" / "users_raw.json",
        root / "data" / "users_clean.csv",
        n=50,
        seed=42,
    )


if __name__ == "__main__":
    main()


