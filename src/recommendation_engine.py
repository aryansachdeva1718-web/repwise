from muscle_history import days_since_last_trained

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
