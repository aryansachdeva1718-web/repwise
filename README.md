# RepWise

A modular Python fitness tracking application for workout logging, training analytics, recovery analysis, and workout recommendations.

RepWise combines a **SQLite-backed data layer**, reusable Python backend logic, and a **Streamlit dashboard** to turn raw workout history into useful training insights.

## Features

### 🏋️ Workout Logging

* Log workouts with exercises, sets, reps, and weight
* Log daily metrics including sleep, calories, and bodyweight
* Automatic Personal Record (PR) detection
* Multiple PRs supported within a single workout session
* Workout sessions grouped and stored chronologically

### 📊 Dashboard

* Workout overview and key statistics
* Interactive workout calendar
* Clickable workout history
* Detailed session breakdowns
* Recent workout summaries
* Latest recovery and recommendation previews

### 📈 Analytics

* Total workout volume
* Average session volume
* Exercise progression graphs
* Workout volume trends
* Bodyweight trends
* Historical workout analysis

### 🧠 Recovery System

RepWise calculates a **0–100 recovery score** using:

* Sleep
* Calorie intake
* Relative workout fatigue
* Historical workout volume

The fatigue component compares recent workout volume against the user's historical training volume rather than relying on fixed volume thresholds.

The system also:

* Handles insufficient workout history
* Automatically scales the score when fatigue data is unavailable
* Provides recovery status and training recommendations
* Supports recovery analysis for historical workout dates

### 🤖 Workout Recommendations

RepWise currently uses a **rule-based recommendation engine** that:

* Detects neglected muscles
* Tracks how recently muscles were trained
* Considers primary and secondary muscle involvement
* Accounts for secondary muscle fatigue
* Ranks muscles by training priority
* Provides reasoning behind recommendations

The rule-based system provides the foundation for future ML-based recommendations.

---

## Database

RepWise uses **SQLite** as its persistent relational database.

### Schema

Core tables include:

* `workout_sessions`
* `exercises`
* `workout_sets`
* Exercise category mappings
* Primary muscle mappings
* Secondary muscle mappings

The database uses:

* Primary and foreign keys
* Referential integrity
* `ON DELETE RESTRICT`
* Indexes
* Transactions
* Duplicate-session protection

### Hevy Migration Pipeline

Historical Hevy workout data is migrated through:

```text
Hevy CSV
   ↓
Pandas
   ↓
Validation & Cleaning
   ↓
Normalization
   ↓
Chronological Sorting
   ↓
SQLite Insertion
```

The migration process is transactional and protects against duplicate session imports.

### Current Dataset

The current database contains:

* **224 workout sessions**
* **147 exercises**
* **5,426 workout sets**

Raw workout data is stored in the database. Metrics such as workout volume, recovery, and recommendations are calculated from the stored data when requested rather than being precomputed and stored separately.

---

## Architecture

RepWise follows a modular architecture with a separation between the **presentation layer**, **business logic**, and **database layer**.

```text
Streamlit / CLI
       ↓
Application Logic
       ↓
Backend Modules
       ↓
Database Queries
       ↓
SQLite
```

The same backend logic can be reused by both the CLI and Streamlit interfaces.

This keeps UI code responsible for presentation while workout processing, analytics, recovery calculations, recommendations, and database operations remain separated.

---

## Tech Stack

* **Python**
* **Pandas**
* **SQLite**
* **SQL**
* **Streamlit**
* **Matplotlib**
* **Git / GitHub**

---

## Project Structure

```text
repwise/
├── data/
│   └── # CSV exports / input data
│
├── database/
│   ├── connection.py       # SQLite connection management
│   ├── schema.py           # Database schema
│   └── queries.py          # Database queries
│
├── importers/
│   └── migrate.py          # Hevy → SQLite migration pipeline
│
├── src/
│   ├── app.py              # Streamlit entry point
│   ├── main.py             # CLI entry point
│   ├── tracker.py          # Workout tracking and analytics
│   ├── recovery.py         # Recovery scoring
│   ├── helpers.py          # Shared helper functions
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
├── tools/
│   └── # Database testing and inspection scripts
│
├── project_docs/
│   ├── progress.md
│   └── learning.md
│
├── requirements.txt
└── repwise.db
```

---

## Run RepWise

Clone the repository:

```bash
git clone https://github.com/aryansachdeva1718-web/repwise.git
cd repwise
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
py -m streamlit run src/app.py
```

---

## Development Roadmap

### v0.1 — Workout Logging

* Workout logging
* Set and exercise tracking

### v0.2 — Recovery System

* Recovery scoring
* Sleep and calorie analysis
* Fatigue scoring

### v0.3 — Recommendation Engine

* Muscle priority system
* Neglected muscle detection

### v0.4 — Advanced Muscle Tracking

* Secondary muscle involvement
* Secondary muscle fatigue

### v0.5 — Streamlit UI

* Dashboard
* Workout logging interface
* Analytics
* Recovery and recommendation pages

### v0.6 — SQLite Migration

* Relational database architecture
* Hevy workout history migration
* Database constraints and indexes
* Transactional migration pipeline

### v0.7 — Database Integration

* Converted application logic from CSV-based storage to SQLite
* Database-backed workout tracking
* Database-backed analytics
* Database-backed recovery analysis
* Database-backed recommendations
* Completed end-to-end database workflow

### v0.8 — UI & Portfolio Polish

**Current phase**

* UI refinement
* Visual consistency
* Chart and layout improvements
* Final screenshots
* README and documentation updates

### Future — ML Integration

The next major development phase will focus on turning RepWise's existing analytics and rule-based systems into an ML-driven fitness application.

Planned work:

* Build an ML-ready dataset from historical workout data
* Feature engineering
* Recovery prediction
* Compare ML predictions against the existing rule-based recovery system
* ML-based workout recommendations
* Personalized training insights

---

## Future Improvements

Longer-term possibilities include:

* Muscle recovery visualization
* Long-term performance forecasting
* User authentication
* Cloud database integration
* Workout history export
* Mobile-friendly interface
* Docker deployment

---

## Project Status

**Current version: v0.8 — UI & Portfolio Polish**

RepWise currently has a complete end-to-end workflow covering:

**Workout Logging → SQLite Database → Analytics → Recovery Analysis → Workout Recommendations → Streamlit Dashboard**

The next major milestone is **ML integration**, beginning with ML theory, dataset preparation, feature engineering, and recovery prediction.

