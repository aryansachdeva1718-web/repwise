import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from helpers import *
from database.queries import (
    save_workout_session,
    save_daily_metrics,
    get_workout_history,
    get_daily_metrics_history,
    get_exercise_history,
    get_workout_dates as db_get_workout_dates,
    get_recent_workouts as db_get_recent_workouts,
    get_workout_details as db_get_workout_details,
    get_bodyweight_history as db_get_bodyweight_history,
    get_all_exercises as db_get_all_exercises
)

#----------DAILY METRICS FUNCTION----------
def log_daily_metrics(date, sleep, calories, bodyweight):

    save_daily_metrics(
        date=date,
        sleep=sleep,
        calories=calories,
        bodyweight=bodyweight
    )

#----------WORKOUT INPUT FUNCTION----------
def log_workout():

    print("\n--- WORKOUT LOGGING ---")

    date = get_date()

    start_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    title = input("Enter workout title: ")

    exercises = []

    while True:

        exercise = select_exercise()

        set_number = int(
            input("Enter total sets: ")
        )

        reps_list = []
        weight_list = []

        for i in range(set_number):

            print(f"\nSet {i + 1}")

            reps = int(
                input("Enter reps: ")
            )

            weight = float(
                input("Enter weight: ")
            )

            reps_list.append(reps)
            weight_list.append(weight)

        exercises.append({
            "exercise": exercise,
            "reps": reps_list,
            "weights": weight_list
        })

        another = input(
            "Add another exercise? (y/n): "
        )

        if another.lower() != "y":
            break

    end_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    try:

        session_id, pr_messages = save_workout_session(
            title=title,
            start_time=start_time,
            end_time=end_time,
            exercises=exercises
        )

    except Exception as e:

        print("\nWorkout could not be saved.")
        print(f"Error: {e}")

        return None

    for message in pr_messages:
        print(message)

    print(
        f"\nWorkout saved successfully."
        f" Session ID: {session_id}\n"
    )

    return date

def save_workout(
    date,
    exercise,
    reps_list,
    weight_list,
    session_id=None
):
    if session_id is None:
        raise ValueError(
            "session_id is required when saving a workout."
        )

    return save_workout_session(
        title="Workout",
        start_time=f"{date} 00:00:00",
        exercises=[
            {
                "exercise": exercise,
                "reps": reps_list,
                "weights": weight_list
            }
        ]
    )

#----------ANALYTICS & GRAPHS----------
def workout_summary(date):
    workout_df = get_workout_history()

    if workout_df.empty:
        return None

    today_data = workout_df[workout_df["Date"] == date].copy()

    if today_data.empty:
        return None

    today_data["Volume"] = (today_data["Weight"] * today_data["Reps"])
    total_sets = len(today_data)
    exercise_count = today_data["Exercise"].nunique()
    total_volume = today_data["Volume"].sum()
    valid_weight_data = today_data[today_data["Weight"].notna()]

    if valid_weight_data.empty:
        heaviest_exercise = None
        heaviest_weight = None
    else:
        heaviest_row = valid_weight_data.loc[valid_weight_data["Weight"].idxmax()]
        heaviest_exercise = heaviest_row["Exercise"]
        heaviest_weight = heaviest_row["Weight"]

    return {
        "exercise_count": exercise_count,
        "total_sets": total_sets,
        "total_volume": total_volume,
        "heaviest_exercise": heaviest_exercise,
        "heaviest_weight": heaviest_weight
    }

def plot_progress(date):
    workout_df = get_workout_history()

    if workout_df.empty:
        return

    today_data = workout_df[workout_df["Date"] == date]

    if today_data.empty:
        return

    today_exercises = today_data["Exercise"].unique()

    for exercise in today_exercises:

        exercise_data = workout_df[workout_df["Exercise"] == exercise].copy()

        # Ignore sets where weight is NULL
        exercise_data = exercise_data[exercise_data["Weight"].notna()]

        if exercise_data.empty:
            continue

        progress = (exercise_data.groupby("Date")["Weight"].max())

        plt.figure()
        plt.plot(
            progress.index,
            progress.values,
            marker="o"
        )

        plt.title(f"{exercise} Progress")
        plt.xlabel("Date")
        plt.ylabel("Max Weight (kg)")
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        plt.show()

#Calorie Trend
def calorie_trend(date):
    daily_df = get_daily_metrics_history()

    if daily_df.empty:
        print("\nNo daily metrics found.")
        return

    today_data = daily_df[daily_df["Date"] == date]

    if today_data.empty:
        print("\nNo daily metrics found for this workout date.")
        return

    calories = today_data["Calories"].iloc[0]

    history_data = daily_df[daily_df["Date"] != date]

    if len(history_data) < 3:
        print("\nNot enough history for calorie trend analysis.")
        return

    recent_data = history_data.tail(3)

    avg_calories = recent_data["Calories"].mean()

    if calories > avg_calories * 1.20:
        print("\nCalorie intake is significantly "
            "higher than your recent average.")

    elif calories < avg_calories * 0.80:
        print("\nCalorie intake is significantly "
            "lower than your recent average.")

    else:
        print("\nCalorie intake is consistent "
            "with your recent average.")

def consistency_tracker(date):

    workout_dates = get_workout_dates()

    if not workout_dates:
        print("\nNo workouts found.")
        return

    today = datetime.strptime(date, "%Y-%m-%d")
    seven_days_ago = today - timedelta(days=6)

    workout_days = 0

    for workout_date in workout_dates:

        workout_datetime = datetime.strptime(workout_date[:10],"%Y-%m-%d")

        if seven_days_ago <= workout_datetime <= today:
            workout_days += 1

    print(f"\nYou trained {workout_days} times "
        "in the last 7 days.")

    if workout_days == 7:
        print("Consistency: Excellent 🔥")

    elif workout_days >= 5:
        print("Consistency: Very consistent 💪")

    elif workout_days >= 3:
        print("Consistency: Moderate 👍")

    elif workout_days >= 1:
        print("Consistency: Inconsistent ⚠️")

    else:
        print("No recent training logged.")

#----------DASHBOARD FUNCTIONS----------
def get_workout_dates():
    return db_get_workout_dates()

def get_total_workout_sessions():
    return len(get_workout_dates())

def get_total_exercises_logged():
    workout_df = get_workout_history()

    if workout_df.empty:
        return 0

    return workout_df["Exercise"].nunique()

def get_recent_workouts():
    return db_get_recent_workouts(limit=5)

def get_last_workout_date():
    workout_dates = get_workout_dates()

    if len(workout_dates) == 0:
        return "No Workouts"

    return pd.to_datetime(workout_dates[-1]).strftime("%d %b %Y")

def get_calendar_events():
    workout_dates = get_workout_dates()

    events = []

    for date in workout_dates:
        events.append(
            {
                "title": "💪",
                "start": date
            }
        )

    return events

def get_workout_details(session_id):
    return db_get_workout_details(session_id)

#----------STREAMLIT ANALYTICS----------
def get_total_volume():

    workout_df = get_workout_history()

    if workout_df.empty:
        return 0

    total_volume = (workout_df["Weight"] * workout_df["Reps"]).sum()

    return int(total_volume)

def get_average_session_volume():

    workout_df = get_workout_history()

    if workout_df.empty:
        return 0

    workout_df["Volume"] = workout_df["Weight"] * workout_df["Reps"]

    session_volume = (
        workout_df
        .groupby("Session_ID")["Volume"]
        .sum()
    )

    return round(session_volume.mean())

def get_volume_history():

    workout_df = get_workout_history()

    if workout_df.empty:
        return workout_df

    workout_df["Volume"] = workout_df["Weight"] * workout_df["Reps"]

    volume_history = (
        workout_df
        .groupby("Date")["Volume"]
        .sum()
        .reset_index()
    )

    volume_history["Date"] = pd.to_datetime(volume_history["Date"])
    return volume_history

def get_bodyweight_history():

    daily_df = db_get_bodyweight_history()

    if daily_df.empty:
        return daily_df

    daily_df["Date"] = pd.to_datetime(
        daily_df["Date"]
    )

    return daily_df[["Date", "Bodyweight"]]

def get_all_exercises():
    return db_get_all_exercises()

def get_exercise_progress(exercise):

    exercise_data = get_exercise_history(exercise)

    if exercise_data.empty:
        return exercise_data

    progress = (
        exercise_data
        .groupby("Date")["Weight"]
        .max()
        .reset_index()
    )

    progress["Date"] = pd.to_datetime(
        progress["Date"]
    )

    return progress

def get_heaviest_lift():

    workout_df = get_workout_history()

    if workout_df.empty:
        return None

    valid_weight_data = workout_df[
        workout_df["Weight"].notna()
    ]

    if valid_weight_data.empty:
        return None

    row = valid_weight_data.loc[
        valid_weight_data["Weight"].idxmax()
    ]

    return row["Exercise"], row["Weight"]

