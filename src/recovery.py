import pandas as pd
import matplotlib.pyplot as plt
from helpers import *

#----------RECOVERY SYSTEM----------
#Average volume over last 10 sessions
def get_avg_volume(workout_df, date):

    historical_workouts = workout_df[workout_df["Date"] < date].copy()

    historical_workouts["Volume"] = (historical_workouts["Reps"] * historical_workouts["Weight"])

    daily_volume = (
        historical_workouts
        .groupby("Date")["Volume"]
        .sum()
        .sort_index()
    )

    recent_sessions = daily_volume.tail(10)

    if len(recent_sessions) < 10:
        return None

    return recent_sessions.mean()

#Today Volume
def get_today_volume(date):

    workout_df = load_workout_data()

    today_workout = workout_df[workout_df["Date"] == date].copy()
    today_workout["Volume"] = (today_workout["Reps"] * today_workout["Weight"])

    total_volume = today_workout["Volume"].sum()

    return total_volume

#Fatigue Score
def fatigue_score(today_volume, avg_volume):

    ratio = today_volume / avg_volume

    if ratio <= 1.0:
        score = 20
    elif ratio <= 1.2:
        score = 16
    elif ratio <= 1.4:
        score = 12
    elif ratio <= 1.7:
        score = 7
    else:
        score = 3
    return score

#Sleep Score
def sleep_score(sleep_hours):

    if sleep_hours >= 8:
        score = 50
    elif sleep_hours >= 7:
        score = 42
    elif sleep_hours >= 6:
        score = 35
    elif sleep_hours >= 5:
        score = 20
    else:
        score = 10
    return score

#Calorie Score
def calorie_score(calories, bodyweight):
    
    maintenance = bodyweight * 33
    ratio = calories / maintenance

    if ratio >= 0.95:
        score = 30
    elif ratio >= 0.85:
        score = 25
    elif ratio >= 0.75:
        score = 18
    elif ratio >= 0.60:
        score = 10
    else:
        score = 5
    return score
 
#Interpret Score
def interpret_score(score):

    if score >= 85:
        status =  "Excellent"
        message = "You are well recovered and ready for hard training."

    elif score >= 70:
        status = "Good"
        message = "Recovery looks good. Performance should be solid."

    elif score >= 55:
        status = "Moderate"
        message = "Recovery is decent. Avoid pushing to absolute limits."

    elif score >= 40:
        status = "Poor"
        message ="Recovery is lower than ideal. Consider lighter training."

    else:
        status = "Very Poor"
        message = "Sleep, nutrition or fatigue may be limiting recovery today."

    return {
        "status": status,
        "message": message}

#Recovery Score
def recovery_score(date):
    daily_df = load_daily_data()
    today_data = daily_df[daily_df["Date"] == date]

    if today_data.empty:
        return None

    sleep_hours = today_data["Sleep"].iloc[0]
    calories = today_data["Calories"].iloc[0]
    bodyweight = today_data["Bodyweight"].iloc[0]

    sleep_points = sleep_score(sleep_hours)
    calorie_points = calorie_score(calories, bodyweight)

    today_volume = get_today_volume(date)
    avg_volume = get_avg_volume(workout_df ,date)
    
    if avg_volume is not None:

        fatigue_points = fatigue_score(today_volume, avg_volume)
        total_score = ( sleep_points + calorie_points + fatigue_points)
        history_available = True
    
    else:
        fatigue_points = None

        total_score = sleep_points + calorie_points
        total_score = (total_score / 80) * 100
        history_available = False

    interpretation = interpret_score(total_score)

    return {
    "score": round(total_score),
    "sleep": sleep_points,
    "calories": calorie_points,
    "fatigue": fatigue_points,
    "history_available": history_available,
    "status": interpretation["status"],
    "message": interpretation["message"]
}

    
    



