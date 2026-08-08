import sqlite3

conn = sqlite3.connect("repwise.db")

cursor = conn.cursor()

# 1. Check workout_sessions columns
print("\n--- workout_sessions columns ---")

cursor.execute("PRAGMA table_info(workout_sessions);")

for column in cursor.fetchall():
    print(column)

# 2. Check whether foreign keys are enabled
print("\n--- foreign_keys ---")

cursor.execute("PRAGMA foreign_keys;")

print(cursor.fetchone()[0])

# 3. Check for foreign-key violations
print("\n--- foreign_key_check ---")

cursor.execute("PRAGMA foreign_key_check;")

violations = cursor.fetchall()

if violations:
    for violation in violations:
        print(violation)
else:
    print("No foreign-key violations.")

conn.close()