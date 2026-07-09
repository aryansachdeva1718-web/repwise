### Why I Built This

I built this project to combine my passion for fitness and programming while learning software engineering, data analysis, and AI application development. The goal is to build a professional-grade fitness tracker that evolves from a simple workout logger into an intelligent workout recommendation system.

# AI Fitness Tracker

A modular Python fitness tracking application that logs workouts, analyzes training history, tracks recovery, and visualizes workout data through both a Command Line Interface (CLI) and a Streamlit dashboard.

---

## Current Features

### Workout Logging
- Log workouts through both CLI and Streamlit
- Select exercises from an exercise database
- Record sets, reps, and weights
- Automatic Personal Record (PR) detection
- Multiple PR detection within a single workout session

### Dashboard
- Workout Sessions counter
- Exercises Logged counter
- Last Workout tracker
- Recent Workout summary table
- Workout Calendar
- Recovery Page
- Workout Recommendation
- Graceful empty-state handling for first-time users

### Analytics Backend
- Workout volume calculation
- Recent workout aggregation
- Workout session tracking
- Exercise session tracking
- Modular data processing using Pandas

### Recovery System (Backend)
- Daily metrics tracking (sleep, calories, bodyweight)
- Recovery score framework
- Sleep score
- Calorie score
- Fatigue score
- Calorie trend analysis

### Architecture
- Modular Python architecture
- Reusable backend shared by CLI and Streamlit
- Exercise database with primary and secondary muscle mapping
- CSV-based persistent storage

---

## Planned Features

- Workout Calendar
- Recovery Score Dashboard
- Progress Graphs
- Muscle Recovery Visualization
- AI Workout Recommendation Engine
- Exercise Progress Analytics
- Recovery Insights
- Machine Learning-based Recovery Prediction

---

## Project Structure

```text
fitness-tracker/
├── data/
│   ├── workout_sets.csv
│   ├── daily_metrics.csv
│
├── project_docs/
│   ├── progress.md
│   ├── learning.md
│
├── screenshots/
│
├── src/
│   ├── app.py                 # Streamlit entry point
│   ├── tracker.py             # Workout logging + dashboard helpers
│   ├── recovery.py            # Recovery scoring
│   ├── helpers.py
│   ├── muscle_history.py
│   ├── recommendation_engine.py
│   └── pages/
│       ├── 00_Dashboard.py
│       ├── 01_Log_Workout.py
│       ├── 02_Workout_Recommendation.py
│       └── 03_Recovery.py
│
├── requirements.txt
└── README.md
```

---

## Tech Stack

- Python
- Pandas
- Streamlit
- Matplotlib
- CSV Storage
- Git
- GitHub

---

## How to Run

Clone the repository

```bash
git clone https://github.com/aryansachdeva1718-web/ai-fitness-tracker.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the Streamlit application

```bash
py -m streamlit run src/app.py
```

---

## Screenshots

*(To be updated as new pages are completed.)*

- Dashboard
- Workout Logging
- Recovery
- Workout Recommendation

---

## Current Development Status

The project is actively being built from scratch while documenting the complete development process.

Current focus:

- Streamlit Dashboard
- Workout Calendar
- Recovery Analytics

Upcoming milestones:

- Progress Graphs
- Recommendation Engine
- AI Features

---

## Future Improvements

- Authentication and user accounts
- Cloud database integration
- AI workout recommendations
- Personalized recovery suggestions
- Long-term performance forecasting
- Mobile-friendly UI
- Export workout history
- Docker deployment
