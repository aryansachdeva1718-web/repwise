from database.connection import get_connection
from importers.migrate import import_hevy_csv

conn = get_connection()

import_hevy_csv(
    "data/workouts.csv",
    conn
)

conn.close()