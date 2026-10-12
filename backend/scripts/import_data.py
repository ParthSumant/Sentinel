"""
SENTINEL ONE-TIME DATA IMPORTER

Purpose:
    Import/transform the supplied source CSV into Supabase.

Important:
    The Sentinel backend does NOT read the CSV during normal operation.

Architecture:

    Source CSV
        ↓
    This script (one-time)
        ↓
    Supabase
        ↓
    Sentinel FastAPI
        ↓
    React frontend

The exact column mapping must be implemented against the actual
CSV supplied for the project. Do not invent mappings.
"""

from pathlib import Path


def main():
    csv_path = Path("data/sentinel.csv")

    if not csv_path.exists():
        print("Source CSV not found.")
        print()
        print("Place the supplied dataset at:")
        print("    data/sentinel.csv")
        print()
        print("Then implement the dataset-specific mapping.")
        return

    print(f"Found source CSV: {csv_path}")
    print()
    print("Dataset detected.")
    print(
        "The importer is intentionally waiting for the actual "
        "CSV schema before mapping columns into Supabase."
    )


if __name__ == "__main__":
    main()
