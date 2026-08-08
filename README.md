# RepWise

A modular Python fitness tracking app — workout logging, analytics, recovery scoring, and workout recommendations, via CLI and a Streamlit dashboard. Backed by SQLite.

## Features

**Logging**
- Log workouts (sets, reps, weight, exercise metadata) via CLI or Streamlit
- Log daily metrics: sleep, calories, bodyweight
- Automatic PR detection (multiple PRs per session supported)

**Dashboard**
- Workout overview, calendar, clickable history
- Session breakdowns and summaries

**Analytics**
- Total/average session volume, volume trends
- Exercise progression graphs
- Bodyweight trends

**Recovery**
- Daily recovery score (0–100) from sleep, calories, and relative fatigue (based on historical volume)
- Auto-scales when workout history is sparse
- Training recommendations based on recovery status

**Recommendations**
- Rule-based engine: detects neglected muscles, ranks priority by training frequency, recovery, and secondary muscle fatigue
- Gives reasoning for each recommendation

## Database

SQLite, relational schema:
- Tables: `workout_sessions`, `exercises`, `workout_sets` + category/muscle mapping tables
- Primary/foreign keys, referential integrity, `ON DELETE RESTRICT`, indexes, transactions

**Hevy migration pipeline**: CSV → Pandas → validate/clean → normalize → chronological sort → insert (dedup'd, transactional).

Current imported data: 224 sessions, 147 exercises, 5,426 sets. Raw workout data only — no precomputed metrics (volume/recovery calculated on demand).

## Stack

Python, Pandas, SQLite/SQL, Streamlit, Matplotlib

## Structure

```
repwise/
├── data/                 # CSVs (daily metrics, Hevy exports)
├── database/             # connection.py, schema.py
├── importers/             # migrate.py (Hevy import pipeline)
├── src/
│   ├── app.py             # Streamlit entry
│   ├── main.py            # CLI entry
│   ├── tracker.py
│   ├── recovery.py
│   ├── recommendation_engine.py
│   ├── exercise_database.py
│   └── pages/              # Streamlit pages (dashboard, logging, analytics, recovery, recommendations)
├── tools/                 # DB check/query scripts
└── repwise.db
```

## Run it

```bash
git clone https://github.com/aryansachdeva1718-web/repwise.git
cd repwise
pip install -r requirements.txt
py -m streamlit run src/app.py
```

## Status

**Done:** workout tracking, Streamlit dashboard, analytics, recovery scoring, rule-based recommendations, SQLite schema, full Hevy data migration.

**Next:** move logging/analytics/recovery/recommendations to be fully DB-backed, muscle recovery visualization, then AI/ML-based recommendations and recovery prediction.

**Later:** auth, cloud DB, forecasting, mobile UI, export, Docker/deployment.
