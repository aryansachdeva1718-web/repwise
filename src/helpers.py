import pandas as pd
from datetime import date

from exercise_database import exercise_database
from database.queries import get_daily_metrics_history


def get_date():
    return str(date.today())

def select_exercise():

    exercises = list(exercise_database.keys())

    print("\nSelect Exercise:")

    for i, exercise in enumerate(
        exercises,
        start=1
    ):
        print(f"{i}. {exercise}")

    choice = int(input("Enter choice: "))

    return exercises[choice - 1]