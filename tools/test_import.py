from database.connection import get_connection
from importers.migrate import import_hevy_csv


conn = get_connection()

import_hevy_csv(
    "data/hevy_export.csv",
    conn
)

conn.close()