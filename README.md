### Why I Built This

I built this project to combine my passion for fitness and programming while learning software engineering, data analysis, and AI application development. The goal is to build a professional-grade fitness tracker that evolves from a simple workout logger into an intelligent workout recommendation system.

# RepWise

A modular Python fitness tracking application that logs workouts, analyzes training history, tracks recovery, and visualizes workout data through both a Command Line Interface (CLI) and a Streamlit dashboard.

---

## Current Features

### Workout Logging
- Log workouts through both CLI and Streamlit
- Log daily metrics (sleep, calories, bodyweight)
- Select exercises from an exercise database
- Record sets, reps, and weights
- Automatic Personal Record (PR) detection
- Multiple PR detection within a single workout session
- Automatic workout session grouping by date

### Dashboard
- Workout overview with key metrics
- Interactive workout calendar
- Clickable workout history with detailed session breakdown
- Session summary (exercises, sets, volume)
- Last workout tracking
- Recent workout summary table
- Graceful empty-state handling for first-time users

### Analytics
- Workout statistics
- Total volume
- Average session volume
- Exercise progression graphs
- Workout volume trend
- Bodyweight trend

### Recovery System
- Daily recovery score (0–100)
- Sleep score analysis
- Calorie score analysis
- Relative fatigue scoring using historical workout volume
- Automatic scaling when workout history is insufficient
- Recovery status and training recommendations
- View recovery data for any logged workout date

### Workout Recommendation
- Rule-based muscle recommendation engine
- Neglected muscle detection
- Muscle priority ranking based on recovery and training frequency
- Secondary muscle fatigue consideration
- Training focus with recommendation reasoning

### Analytics Backend
- Workout volume calculation
- Recent workout aggregation
- Workout session tracking
- Exercise session tracking
- Historical volume analysis
- Calendar event generation
- Workout detail retrieval by date
- Modular data processing using Pandas

### Architecture
- Modular Python architecture
- Reusable backend shared by CLI and Streamlit
- Separation of business logic and presentation layer
- Exercise database with primary and secondary muscle mapping
- CSV-based persistent storage
- Structured backend responses for Streamlit integration

---

## Planned Features

- Muscle Recovery Visualization
- AI Workout Recommendation Engine
- Machine Learning-based Recovery Prediction

---

## Project Structure

```text
repwise/
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
│   ├── exercise_database.py
│   └── pages/
│       ├── 00_Dashboard.py
│       ├── 01_Log_Workout.py
│       ├── 02_Log_Daily_Metrics.py
│       ├── 03_Analytics.py
│       ├── 04_Recovery_Score.py
│       └── 05_Workout_Recommendation.py
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
git clone https://github.com/aryansachdeva1718-web/repwise.git
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

Upcoming milestones:

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
