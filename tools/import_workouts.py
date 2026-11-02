
from pathlib import Path

from database.connection import get_connection
from importers.migrate import import_hevy_csv


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "workouts.csv"


def main():
    if not CSV_PATH.is_file():
        raise FileNotFoundError(
            f"Workout CSV not found: {CSV_PATH}\n"
            "Place your exported workout history at data/workouts.csv."
        )

    conn = get_connection()

    try:
        import_hevy_csv(str(CSV_PATH), conn)
        print("Workout import completed successfully!")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
