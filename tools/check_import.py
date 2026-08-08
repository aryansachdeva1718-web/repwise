import sqlite3

conn = sqlite3.connect("repwise.db")
cursor = conn.cursor()


# --------------------------------------------------------
# 1. Count rows
# --------------------------------------------------------

print("\n--- ROW COUNTS ---")

cursor.execute("SELECT COUNT(*) FROM workout_sessions;")
print("Sessions:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM exercises;")
print("Exercises:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM workout_sets;")
print("Sets:", cursor.fetchone()[0])


# --------------------------------------------------------
# 2. Show imported sessions
# --------------------------------------------------------

print("\n--- WORKOUT SESSIONS ---")

cursor.execute("""
SELECT
    session_id,
    hevy_session_key,
    title,
    start_time,
    end_time
FROM workout_sessions
ORDER BY start_time;
""")

for row in cursor.fetchall():
    print(row)


# --------------------------------------------------------
# 3. Show exercises
# --------------------------------------------------------

print("\n--- EXERCISES ---")

cursor.execute("""
SELECT
    exercise_id,
    name
FROM exercises
ORDER BY exercise_id;
""")

for row in cursor.fetchall():
    print(row)


# --------------------------------------------------------
# 4. Show sets with exercise names
# --------------------------------------------------------

print("\n--- WORKOUT SETS COLUMNS ---")

cursor.execute("PRAGMA table_info(workout_sets);")

for column in cursor.fetchall():
    print(column)


# --------------------------------------------------------
# 5. Check duplicate exercises
# --------------------------------------------------------

print("\n--- DUPLICATE EXERCISES ---")

cursor.execute("""
SELECT
    name,
    COUNT(*)
FROM exercises
GROUP BY name
HAVING COUNT(*) > 1;
""")

duplicates = cursor.fetchall()

if duplicates:
    for row in duplicates:
        print(row)
else:
    print("No duplicate exercises.")


# --------------------------------------------------------
# 6. Check foreign-key relationships
# --------------------------------------------------------

print("\n--- FOREIGN KEY CHECK ---")

cursor.execute("PRAGMA foreign_key_check;")

violations = cursor.fetchall()

if violations:
    for row in violations:
        print(row)
else:
    print("No foreign-key violations.")


conn.close()