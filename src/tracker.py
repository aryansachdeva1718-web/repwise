import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from helpers import *

#----------DAILY METRICS FUNCTION----------
def log_daily_metrics():

    daily_df = load_daily_data()
    print("\n--- DAILY METRICS ---")

    date = get_date()
    sleep = float(input("Enter sleep hours: "))
    calories = int(input("Enter calories: "))
    bodyweight = float(input("Enter bodyweight: "))

    new_daily_entry = {
        "Date": date,
        "Sleep": sleep,
        "Calories": calories,
        "Bodyweight": bodyweight
    }

    daily_df = pd.concat([daily_df, pd.DataFrame([new_daily_entry])],
    ignore_index=True)

    daily_df.to_csv(daily_metrics_file, index=False)

    print(daily_df.tail())

#----------WORKOUT INPUT FUNCTION----------
def log_workout():
    print("\n--- WORKOUT LOGGING ---")

    workout_df = load_workout_data()
    date = get_date()

    while True:
        
        exercise = select_exercise()
        set_number = int(input("Enter total sets: "))
        
        for i in range(set_number):
            print(f"\nSet {i+1}")

            reps = int(input("Enter reps: "))
            weight = float(input("Enter weight: "))

            exercise_history = workout_df[workout_df["Exercise"] == exercise]

            if exercise_history.empty:
                print("First time doing this exercise")
            else:
                max_weight = exercise_history["Weight"].max()
                if weight > max_weight:
                     print(f"New {exercise} PR: Previous {max_weight} kg -> Current {weight} kg ")

            new_workout_entry = {
                "Date": date,
                "Exercise": exercise,
                "Set": i + 1,
                "Reps": reps,
                "Weight": weight
            }

            workout_df = pd.concat( [workout_df, pd.DataFrame([new_workout_entry])],
            ignore_index=True)

        another = input("Add another exercise? (y/n): ")

        if another.lower() != "y":
            break
    
    workout_df.to_csv(workout_sets_file, index=False)
    workout_summary(date) 
    choice = input("\nDo you want to see progress graphs? (y/n): ")

    if choice.lower() in ["y", "yes"]:
        plot_progress(date) 

    print("\nWorkout saved successfully.\n")
    print(workout_df.tail(10))
    return date

def save_workout(date, exercise, reps_list, weight_list):
    workout_df = load_workout_data()
    pr_messages = []

    for set_number, (reps, weight) in enumerate(zip(reps_list, weight_list), start=1):
            exercise_history = workout_df[workout_df["Exercise"] == exercise]

            if exercise_history.empty:
                max_weight = 0
                if set_number == 1:
                    pr_messages.append(f"First time doing {exercise}!")

            else:
                max_weight = exercise_history["Weight"].max()

            if weight > max_weight:
                if max_weight == 0:
                    pr_messages.append(f"🏆 Starting PR for {exercise}: {weight} kg")
                else:
                    pr_messages.append(f"🏆 New {exercise} PR: Previous {max_weight} kg → Current {weight} kg")

            new_workout_entry = {
            "Date": str(date),
            "Exercise": exercise,
            "Set": set_number,
            "Reps": reps,
            "Weight": weight}

            workout_df = pd.concat([workout_df, pd.DataFrame([new_workout_entry])],ignore_index=True)

    workout_df.to_csv(workout_sets_file, index=False)
    return pr_messages

#----------ANALYTICS & GRAPHS----------
def workout_summary(date):
    workout_df = load_workout_data()
    today_data = workout_df[workout_df["Date"] == date]

    total_sets = len(today_data)
    exercise_count = today_data["Exercise"].nunique()
    today_data["Volume"] = (today_data["Weight"] * today_data["Reps"])
    total_volume = today_data["Volume"].sum()

    heaviest_row = today_data.loc[today_data["Weight"].idxmax()]
    heaviest_exercise = heaviest_row["Exercise"]
    heaviest_weight = heaviest_row["Weight"]

    print("\n")
    print("==============================")
    print("      WORKOUT SUMMARY")
    print("==============================")
    print(f"\nExercises Performed: {exercise_count}")
    print(f"Total Sets Done: {total_sets}")
    print(f"Total Volume: {total_volume} kg")
    print(f"Heaviest Lift: {heaviest_exercise} ({heaviest_weight} kg) ")
    print("\nWorkout completed successfully.\n")

def plot_progress(date):
    workout_df = load_workout_data()
    today_data = workout_df[workout_df["Date"] == date]

    today_exercises = today_data["Exercise"].unique()

    for exercise in today_exercises:
        exercise_data = workout_df[workout_df["Exercise"] == exercise]

    progress = exercise_data.groupby("Date")["Weight"].max()

    plt.figure()
    plt.plot(progress.index,progress.values,marker="o")
    plt.title(f"{exercise} Progress")
    plt.xlabel("Date")
    plt.ylabel("Max Weight (kg)")
    # Rotate dates so they don't overlap
    plt.xticks(rotation=45)
     # Adds grid lines
    plt.grid()
    # Prevent cutting labels
    plt.tight_layout()
    plt.show()

#Calorie Trend
def calorie_trend(date):
    daily_df = load_daily_data()
    today_data = daily_df[daily_df["Date"] == date]
    calories = today_data["Calories"].iloc[0]

    history_data = daily_df[daily_df["Date"] != date]
    if len(history_data) < 3:
        print("\nNot enough history for calorie trend analysis.")
        return
    recent_data = history_data.tail(3)
    avg_calories = recent_data["Calories"].mean()

    if calories > avg_calories * 1.20:
        print("\nCalorie intake is significantly higher than your recent average.")
    elif calories < avg_calories * 0.80:
        print("\nCalorie intake is significantly lower than your recent average.")
    else:
        print("\nCalorie intake is consistent with your recent average.")

def consistency_tracker(date):

    workout_df = load_workout_data()
    unique_dates = workout_df["Date"].unique()
    today = datetime.strptime(date, "%Y-%m-%d")
    seven_days_ago = today - timedelta(days=6)

    workout_days = 0
    for workout_date in unique_dates:

        workout_datetime = datetime.strptime(workout_date, "%Y-%m-%d")

        if workout_datetime >= seven_days_ago:
            workout_days += 1

    print(f"\nYou trained {workout_days} times in the last 7 days.")

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
    workout_df = load_workout_data()

    if workout_df.empty:
        return []

    workout_dates = (workout_df["Date"].drop_duplicates().sort_values().tolist())

    return workout_dates

def get_total_workout_sessions():
    return len(get_workout_dates())

def get_total_exercises_logged():
    workout_df = load_workout_data()

    if workout_df.empty:
        return 0

    exercise_sessions = (workout_df[["Date", "Exercise"]].drop_duplicates())
    return exercise_sessions.shape[0]

def get_recent_workouts():
    workout_df = load_workout_data()

    summary = (
        workout_df
        .groupby(["Date", "Exercise"])
        .agg({
            "Weight": "max",
            "Set": "count"
        })
        .reset_index()
        .rename(
            columns={
            "Weight": "Max Weight",
            "Set": "Total Sets"
            })
        .sort_values(by="Date", ascending=False)
        .head(5)
        .reset_index(drop=True)
        )
    
    summary["Date"] = pd.to_datetime(summary["Date"])
    summary["Date"] = summary["Date"].dt.strftime("%d %b %Y")

    return summary

def get_last_workout_date():
    workout_dates = get_workout_dates()

    if len(workout_dates) == 0:
        return "No Workouts"

    return (pd.to_datetime(workout_dates[-1]).strftime("%d %b %Y"))




