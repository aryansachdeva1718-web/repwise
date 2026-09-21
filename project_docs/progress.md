# Workout Summary

Current Features:
- total sets
- total volume
- heaviest lift
- exercise count

PR detection logic mostly completed (~80%)
Decision:
Pause PR detection polishing.
Reason:
Feature is already functional.

Higher priority features will provide more value.

# Graph Plotting

Built:
- matplotlib progress graphs

Learned:
- plt.plot()
- looping through exercises
- groupby("Date")["Weight"].max()

Problem:
- date sorting issue

# Recovery System Design 

## Goal

Develop a modular recovery scoring system (0–100) that estimates user recovery after each workout session.

---

## Inputs Used

- Sleep
- Calories
- Bodyweight
- Workout Volume

---

## Weight Distribution

- Sleep → 50 points
- Calories → 30 points
- Workout Fatigue → 20 points
- Total → 100 points

---

## Sleep Scoring

- ≥8 hrs → 50
- 7–8 hrs → 42
- 6–7 hrs → 35
- 5–6 hrs → 20
- <5 hrs → 10

---

## Calorie Scoring

Maintenance Calories = Bodyweight × 33

- 100% maintenance → 30
- 90% → 25
- 80% → 18
- 70% → 10
- <70% → 5

---

## Fatigue Scoring (Final Design)

Abandoned fixed workout volume thresholds.

Recovery now compares today's workout volume against the user's historical average.

Formula:

```text
volume_ratio = today_volume / avg_volume
```

Historical average is calculated using the previous **10 workout sessions**.

Scoring:

- ratio ≤ 1.0 → 20
- 1.0–1.2 → 16
- 1.2–1.4 → 12
- 1.4–1.7 → 7
- >1.7 → 3

---

## Historical Data Decisions

- Use the previous **10 workout sessions**.
- Exclude the current workout date while calculating historical averages.
- If fewer than 10 historical sessions exist:
  - Skip fatigue analysis.
  - Scale the remaining recovery score back to 100 instead of inventing fatigue data.

---

## Rest Day Logic

If no workout exists for the selected date:

- Treat it as a rest day.
- Fatigue score automatically becomes maximum.

---

## Architecture Decisions

Recovery logic is completely separated from workout logging.

### `workout_summary()`

Responsible only for:

- Total Sets
- Total Volume
- Heaviest Lift
- Exercise Count

### `recovery_score()`

Responsible only for:

- Fetching daily metrics
- Fetching workout data
- Calling scoring functions
- Computing final recovery score
- Generating recovery recommendations

This follows the **Single Responsibility Principle (SRP)**.

---

## Planned Function Structure

- `sleep_score()`
- `calorie_score()`
- `fatigue_score()`
- `get_avg_volume()`
- `recovery_score()`

Each helper performs a single task and is reused by the main recovery pipeline.

# Workout Recommendation Engine Logic

## Current Scoring Logic 

Priority Score = Days Since Last Trained × 2

Example:

Chest → 1 day → Score 2

Back → 4 days → Score 8

Quads → 6 days → Score 12


## Planned Future Improvements

### 1. Recovery Score Modifier

Higher recovery score increases training priority.


### 2. Weekly Frequency Penalty

Muscles trained too frequently get score reduction.


### 3. Primary Muscle Penalty

If muscle trained as primary muscle yesterday, heavily reduce score.


### 4. Secondary Muscle Penalty

If muscle was engaged as secondary muscle yesterday, slight score reduction.


### 5. High Priority Isolation Rule

If one muscle score is significantly higher than others:

Recommend only that muscle.


### 6. Multi Muscle Recommendation Rule

If multiple muscles have similar scores:

Allow training multiple muscles.


### 7. Exercise Recommendation Layer

Convert recommended muscles into actual exercise suggestions.

# Streamlit - v0.5 Completion

## Overview

Completed the first fully functional Streamlit version of the AI Fitness Tracker.

The application now provides an end-to-end fitness tracking workflow including workout logging, daily metric tracking, recovery analysis, workout recommendations, analytics, and interactive workout history.

---

## Pages Completed

### Home
- Added landing page
- Latest recovery overview
- Workout recommendation preview
- Quick statistics
- Heaviest lift summary
- Application navigation

### Dashboard
- Workout calendar
- Interactive workout history
- Clickable workout details
- Session summary
- Recent workout table
- Latest recovery
- Recommendation preview

### Log Workout
- Streamlit workout logger
- Exercise database integration
- Set logging
- PR detection

### Log Daily Metrics
- Daily metrics logging
- Sleep tracking
- Calories tracking
- Bodyweight tracking
- Default current date selection

### Recovery
- Recovery score visualization
- Historical recovery lookup
- Sleep / Calories / Fatigue breakdown
- Recovery interpretation

### Recommendation
- Rule-based workout recommendation engine
- Neglected muscle detection
- Balanced recommendation ranking
- Recommendation reasoning

### Analytics
- Workout statistics
- Total volume
- Average session volume
- Exercise progression graphs
- Workout volume trend
- Bodyweight trend

---

## Backend Improvements

- Added analytics helper functions
- Added workout history retrieval functions
- Added exercise progression retrieval
- Added volume history generation
- Added bodyweight history generation
- Added heaviest lift calculation
- Improved backend/frontend separation
- Reused backend across CLI and Streamlit

---

## Architecture Improvements

Continued moving towards a service-oriented architecture.

Backend functions now return structured data instead of printing directly, allowing the same logic to power both the CLI and Streamlit interfaces.

---

## Streamlit Concepts Learned

- Multi-page applications
- Session state basics
- Metrics
- Columns
- Selectbox
- Date input
- Number input
- Dataframes
- Interactive Calendar integration
- Event callbacks
- Custom CSS styling
- Built-in line charts
- Page layout design

---

## Status

Streamlit Version 1

Status: ✅ Complete

Remaining work before AI integration:
- UI polishing
- Better visual styling
- Improved responsiveness
- Final screenshots
- README update

# SQL - v0.6 Completion

## Status

✅ Completed — August 8, 2026

## Goal

Move RepWise from CSV-based persistent workout storage toward a structured SQLite database capable of handling the complete Hevy workout history.

---

## Database Architecture

Implemented SQLite database architecture containing:

- `workout_sessions`
- `exercises`
- `workout_sets`
- exercise categories
- primary muscle mappings
- secondary muscle mappings

Established primary-key and foreign-key relationships between the tables.

---

## Hevy Migration

Built a complete Hevy CSV → SQLite migration pipeline.

### Pipeline

```text
Hevy CSV
   ↓
Pandas loading
   ↓
Column validation
   ↓
Data cleaning
   ↓
Datetime conversion
   ↓
Chronological sorting
   ↓
Session grouping
   ↓
SQLite insertion
```

# Database Integration - v0.7 Completion
**Milestone:** SQLite Backend Migration

**Status:** ✅ Complete

**Completion Date:** August 13, 2026

---

## Overview

v0.7 marks the completion of RepWise's migration from CSV-based storage to a SQLite backend. The migration is not just implemented — it has been fully validated end-to-end through the live Streamlit application, across every major feature: import, manual logging, dashboard, recovery, recommendations, and analytics.

---

## What v0.7 Delivers

### Core Architecture
- **SQLite backend** replacing the previous CSV-based storage
- **Removal of obsolete CSV dependencies** from the application logic
- **Workout session architecture** — a `session_id` represents a full workout, containing one or more exercises
- **Workout sets architecture** — sets belong to exercises, exercises belong to sessions
- **Exercise database** — a verified 50-exercise catalog, with exercise names resolving directly to SQLite `exercise_id` records

### Data Import
- **Updated Hevy CSV importing** — supports re-exported/updated Hevy data
- **Incremental Hevy imports** — re-importing an updated export does not duplicate previously migrated workouts, via a dedup check on `hevy_session_key` (the workout `start_time`)

### Logging & Tracking
- **Manual workout logging** through Streamlit, fully SQLite-backed
- **Multiple exercises per workout session**, correctly grouped under a single `session_id`
- **Daily metrics stored in SQLite** (Sleep, Calories, Bodyweight, etc.)

### Dashboard & Insights
- **Session-based dashboard retrieval** (replacing the earlier date-based approach)
- **Recovery Score**, combining Sleep + Calories + Fatigue (fatigue driven by recent workout volume), mapped to status levels: `Excellent / Good / Moderate / Poor / Very Poor`
- **Recovery date normalization**, ensuring date comparisons between workouts and daily metrics are consistent
- **Workout recommendations**, generated from migrated workout and recovery data
- **Analytics**, reading and operating on the full migrated workout history

---

## End-to-End Data Flows (Verified)

**Import → Analytics pipeline:**
```
Hevy Export
   ↓
CSV Import
   ↓
SQLite
   ↓
Workout Sessions
   ↓
Workout Sets
   ↓
Dashboard
   ↓
Recovery
   ↓
Recommendations
   ↓
Analytics
```

**Manual logging pipeline:**
```text
Streamlit Workout Logger
        ↓
Workout Session
        ↓
session_id
        ↓
Exercise Name
        ↓
exercise_id
        ↓
Workout Sets
        ↓
SQLite
```

---

## Completed Checklist

- [x] SQLite backend migration
- [x] Removal of obsolete CSV dependencies
- [x] Workout session architecture
- [x] Workout sets architecture
- [x] Exercise database
- [x] 50-exercise workout catalog
- [x] Manual workout logging
- [x] Multiple exercises per workout
- [x] Session-based dashboard retrieval
- [x] Updated Hevy CSV importing
- [x] Incremental Hevy imports
- [x] Daily metrics stored in SQLite
- [x] Recovery Score
- [x] Recovery date normalization
- [x] Workout recommendations
- [x] Analytics
- [x] End-to-end Streamlit testing

---

## Key Takeaway

Database migrations often expose hidden assumptions about data types and formatting — data can be correctly stored while the application still fails to find it, if two representations of the same value (e.g. `2026-08-11` vs `2026-08-11 00:00:00`) aren't normalized before comparison. The only reliable way to catch this class of bug is to test the **entire** data flow — UI → Application Logic → Database Queries → SQLite → Application Logic → UI — rather than validating each layer in isolation.

---

## Final Result

**v0.7 is complete.** RepWise now runs entirely on a validated SQLite backend, with every core feature — import, logging, dashboard, recovery, recommendations, and analytics — confirmed working end-to-end through the real application.

*For a detailed log of the final integration testing session that closed out this milestone, see `RepWise_Aug13_Work_Log.md`.*

# ML Integration - v0.8 Completion

**Milestone:** e_1rm Prediction

**Status:** ✅ v0.1 Complete

**Completion Date:** September 21, 2026

RepWise has progressed from a CSV-based workout logger into a SQLite-backed fitness analytics application with recovery analysis, workout recommendations, and a first end-to-end machine-learning prediction pipeline.

Current workflow:

```
Workout Logging
      ↓
SQLite Database
      ↓
Analytics
      ↓
Recovery Analysis
      ↓
Workout Recommendations
      ↓
ML Dataset
      ↓
Feature Engineering
      ↓
Training & Evaluation
      ↓
Saved Model
      ↓
Streamlit Prediction
```

## ***ML v0.1 — Performance Prediction***

## Phase 1 — Problem Definition

Selected the first ML problem:

Predict next-session exercise performance using historical exercise data.

The model operates at the exercise-session level, not whole-workout level.

One row represents:

one exercise × one workout session

---
## Phase 2 — ML Dataset

Created:

ml/dataset.py

Pipeline:

```
SQLite workout sets
      ↓
SQL joins
      ↓
Set-level calculations
      ↓
Exercise-session aggregation
```
Exercise-session fields include:

- session date
- exercise ID
- exercise name
- sets
- total reps
- total volume
- best weight
- best e1RM
- average RPE

e1RM currently uses:

```text
e1RM = weight × (1 + reps / 30)
```

---

## Phase 3 — Feature Engineering

Created:

```text
ml/features.py
```

Current features:

- `last_e1rm`
- `last_volume`
- `recent_avg_e1rm`
- `recent_avg_volume`
- `historical_best_e1rm`
- `days_since_last`
- `exercise_session_count`

Feature engineering is performed independently for each exercise and in chronological order.

---

## Phase 4 — First ML Model

Created:

```text
ml/train.py
```

Model:

```text
Linear Regression
```

Evaluation design:

- chronological 80/20 split
- no random shuffling
- naive baseline comparison
- MAE
- RMSE
- R²
- per-exercise diagnostics
- worst-prediction inspection
- coefficient inspection

### Current Dataset

```text
Total usable rows: 1545
Training rows:     1236
Testing rows:       309
```

### Absolute-Target Result

Initial model predicted absolute next-session e1RM.

```text
MAE:          7.54
RMSE:        12.00
R²:           0.936
Baseline MAE: 8.57
```

The high R² was partly caused by different exercises operating on very different absolute strength scales.

---

## Delta-Target Experiment

Changed the target to:

```text
target_change = next_e1rm - current_e1rm
```

Final e1RM prediction:

```text
predicted_next_e1rm
=
current_e1rm + predicted_change
```

Current results:

```text
Next-e1RM MAE:  7.54
Next-e1RM RMSE: 12.00
Delta R²:       0.363
Baseline MAE:   8.57
```

Important finding:

The absolute prediction error remained unchanged because the delta formulation is a linear reparameterization of the same Linear Regression problem when `last_e1rm` remains a feature.

However, **Delta R² = 0.363** provides a more useful view of how much session-to-session performance change the current feature set can explain.

---

## Model Diagnostics

Implemented:

- per-exercise MAE
- baseline MAE by exercise
- improvement over baseline
- worst-prediction inspection
- model coefficient output

Large errors were concentrated in more volatile exercises such as:

- machine leg press
- some machine/cable movements
- chest-supported rows
- exercises with large session-to-session e1RM changes

This suggests future gains are likely to come from:

- better feature engineering
- better treatment of exercise/equipment variability
- additional recovery/readiness variables
- improved e1RM quality controls

rather than immediately switching to a more complex model.

---

## Phase 5 — Model Persistence & Inference

Added:

```text
ml/predict.py
```

The trained model is saved using Joblib:

```text
ml/models/e1rm_delta_model.joblib
```

Live inference flow:

```text
Select Exercise
      ↓
Load Latest Exercise History
      ↓
Build Current Features
      ↓
Load Saved ML Model
      ↓
Predict e1RM Change
      ↓
Generate Next e1RM Prediction
```

---

## Streamlit ML Integration

The Analytics page now displays:

- Current e1RM
- Predicted Next e1RM
- Expected Change

This is the first complete ML feature exposed directly to the user.