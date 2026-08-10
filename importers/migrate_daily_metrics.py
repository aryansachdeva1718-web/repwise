import pandas as pd

from database.connection import get_connection


DAILY_METRICS_FILE = "data/daily_metrics.csv"


def migrate_daily_metrics():
    df = pd.read_csv(DAILY_METRICS_FILE)

    conn = get_connection()

    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT OR REPLACE INTO daily_metrics (
                date,
                sleep,
                calories,
                bodyweight
            )
            VALUES (?, ?, ?, ?);
        """, (
            row["Date"],
            row["Sleep"],
            row["Calories"],
            row["Bodyweight"]
        ))

    conn.commit()
    conn.close()

    print(f"Migrated {len(df)} daily metric records.")


if __name__ == "__main__":
    migrate_daily_metrics()