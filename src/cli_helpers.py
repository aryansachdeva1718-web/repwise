from src.tracker import *
from src.recovery import *
from src.recommendation_engine import *

def display_recovery(date):

    recovery = recovery_score(date)

    if recovery is None:
        return

    print("\n==============================")
    print("      RECOVERY REPORT")
    print("==============================")

    print(f"\nRecovery Score : {round(recovery['score'])}/100")

    print(f"Sleep Score    : {recovery['sleep']}/50")
    print(f"Calorie Score  : {recovery['calories']}/30")
    print(f"Fatigue Score  : {recovery['fatigue']}/20")

    print(f"\nStatus : {recovery['status']}")
    print(recovery["message"])

def display_workout_summary(date):

    summary = workout_summary(date)

    if summary is None:
        return

    print("\n==============================")
    print("      WORKOUT SUMMARY")
    print("==============================")

    print(f"\nExercises : {summary['exercise_count']}")
    print(f"Sets      : {summary['total_sets']}")
    print(f"Volume    : {summary['total_volume']} kg")

    print(
        f"Heaviest Lift : "
        f"{summary['heaviest_exercise']} "
        f"({summary['heaviest_weight']} kg)"
    )

def display_recommendation():

    recommendation = recommend_next_workout()

    print("\n==============================")
    print("   WORKOUT RECOMMENDATION")
    print("==============================")

    if recommendation["training_focus"] == "neglected_muscle":

        print("\nRecommended Muscle(s):")

        for muscle in recommendation["muscles"]:
            print(f"- {muscle}")

    else:

        print("\nPriority Order:")

        for i, muscle in enumerate(recommendation["recommendations"], 1):
            print(f"{i}. {muscle}")

    print(f"\nReason:")
    print(recommendation["reason"])

def display_progress(date):

    plot_progress(date)

def cli_log_daily_metrics():

    print("\n--- DAILY METRICS ---")

    date = get_date()

    sleep = float(input("Enter sleep hours: "))
    calories = int(input("Enter calories: "))
    bodyweight = float(input("Enter bodyweight: "))

    log_daily_metrics(
        date,
        sleep,
        calories,
        bodyweight
    )

    print("\nDaily metrics logged successfully.")