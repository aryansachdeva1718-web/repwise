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