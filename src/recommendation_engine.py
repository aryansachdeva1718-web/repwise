import pandas as pd
from exercise_database import exercise_database
from helpers import workout_sets_file
from datetime import datetime

def get_last_trained_muscles():
    workout_df = pd.read_csv(workout_sets_file)
    muscle_history = {}

    for _, row in workout_df.iterrows():
        exercise = row["Exercise"]
        date = row["Date"]

        if exercise in exercise_database:
            primary = exercise_database[exercise]["primary"]
            secondary = exercise_database[exercise]["secondary"]
            
            for muscle in primary:
                if muscle not in muscle_history:
                    muscle_history[muscle] = {"last_primary": None,"last_secondary": None}
                if muscle_history[muscle]["last_primary"] is None or date > muscle_history[muscle]["last_primary"]:
                    muscle_history[muscle]["last_primary"] = date


            for muscle in secondary:
                if muscle not in muscle_history:
                    muscle_history[muscle] = {"last_primary": None,"last_secondary": None}
                if muscle_history[muscle]["last_secondary"] is None or date > muscle_history[muscle]["last_secondary"]:
                    muscle_history[muscle]["last_secondary"] = date
                
    return muscle_history

def days_since_last_trained():
    muscle_history = get_last_trained_muscles()
    days_since = {}

    today = datetime.today()

    for muscle, info in muscle_history.items():
        primary_days = None
        secondary_days = None

        if info["last_primary"] is not None:
            primary_days = datetime.strptime(info["last_primary"],"%Y-%m-%d")
            primary_difference = (today - primary_days).days
            primary_days = primary_difference
            
        if info["last_secondary"] is not None:
            secondary_days = datetime.strptime(info["last_secondary"],"%Y-%m-%d")
            secondary_difference = (today - secondary_days).days
            secondary_days = secondary_difference

        days_since[muscle] = {"primary_days": primary_days,"secondary_days": secondary_days}

    return days_since

def filter_recently_trained(muscle_days):

    filtered_muscles = {}
    for muscle, info in muscle_days.items():
        if info["primary_days"] is not None and info["primary_days"] <= 1:
            continue     

        filtered_muscles[muscle] = info
    return filtered_muscles

def check_overdue_muscles(filtered_muscles):

    overdue_muscles = {}

    for muscle, info in filtered_muscles.items():

        if info["primary_days"] is not None and info["primary_days"] >= 7:
            overdue_muscles[muscle] = info["primary_days"]

    if overdue_muscles:
        highest_days = max(overdue_muscles.values())
        highest_overdue = []
        for muscle, days in overdue_muscles.items():
            if days == highest_days:
                highest_overdue.append(muscle)

        return highest_overdue
    
    return None

def calculate_priority_scores(filtered_muscles):

    priority_scores = {}

    for muscle, info in filtered_muscles.items():
        if info["primary_days"] is None: 
            continue
        
        score = info["primary_days"] * 2
        if info["secondary_days"] is not None and info["secondary_days"] <= 1:
            score = score -2           
        priority_scores[muscle] = score

    return priority_scores

def sort_priority_scores(priority_scores):

    sorted_scores = dict(sorted(priority_scores.items(), key=lambda x: x[1], reverse=True) )
    return sorted_scores

def recommend_next_workout():

    muscle_days = days_since_last_trained()
    filtered_muscles = filter_recently_trained(muscle_days)
    overdue = check_overdue_muscles(filtered_muscles)

    if overdue:
        return {
        "training_focus": "neglected_muscle",
        "muscles": overdue,
        "top_recommendation": overdue[0],
        "reason": "Hasn't been trained for over 7 days."}

    priority_scores = calculate_priority_scores(filtered_muscles)
    sorted_scores = sort_priority_scores(priority_scores)
    ranking = list(sorted_scores.keys())

    return {
    "training_focus": "balanced_recommendation",
    "recommendations": ranking,
    "top_recommendation": ranking[0],
    "reason": "Based on muscle recovery and training frequency."}
