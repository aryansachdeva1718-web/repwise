# June 18

Worked On

- Recovery score system design

Learned

- Product prioritization
- Function decomposition
- Handling edge cases
- Recovery score heuristics
- Architecture planning before coding

Important Realization

Not every intelligent feature needs Machine Learning.

Rule-based systems can create useful software.

Decision Taken

Will postpone scikit-learn.

Will focus on building intelligent logic first.


# June 19

## Focus: Recovery System Architecture

### Key Learnings

**1. Personalized scoring > fixed thresholds**  
Static fatigue thresholds don’t work. Using volume ratio (`today_volume / avg_volume`) makes scoring user-specific.

**2. Historical data matters**  
Chose last **10 workout sessions** — enough data without including outdated performance.

**3. Edge cases shape design**  
Excluded current date from average volume calculation to avoid skewed recovery scores.

**4. Missing data should not be faked**  
If workout history is insufficient, skip fatigue score and scale remaining score instead.

**5. Scope discipline matters**  
Dropped sleep quality tracking since accurate monitoring is unrealistic for current project scope.

### Biggest Takeaway

Building projects is not just coding.

Good architecture means handling real-world edge cases before they become bugs.

# June 20

Built complete recovery scoring subsystem.

Implemented:
- fatigue_score() based on workout volume vs historical average
- sleep_score() using sleep duration thresholds
- calorie_score() using bodyweight-based maintenance calories (33x multiplier)
- recovery_score() combining all recovery parameters
- interpret_score() for recovery feedback

Key learning:
- Learned how to combine multiple scoring systems into one analytics pipeline
- Improved pandas filtering and validation handling using .empty and .iloc
- Understood importance of handling missing data instead of forcing calculations

# June 22

## Focus: Calorie Trend Analysis & Code Refactoring

### Key Learnings

**1. Trends are better than isolated values**  
Single day calorie intake means little without comparing recent eating patterns.

**2. Recent data > entire history**  
Used last 3 entries instead of full history to reflect current eating habits.

**3. Relative comparison improves analysis**  
Used percentage-based thresholds (±20%) instead of fixed calorie differences.

**4. Handle insufficient history**  
If fewer than 3 past entries exist, skip analysis instead of forcing output.

**5. Large files become hard to manage**  
362 lines in a single file made future scaling difficult.

**6. Code should be split by responsibility**  
Separated project into tracker, recovery, helpers, and main modules.

**7. Testing after every change is critical**  
Verified imports and functionality after each file split.

### Biggest Takeaway

Analytics become more meaningful when current data is compared against user history rather than viewed independently.

Organizing code into maintainable architecture is also important.

# June 26

## Focus: Workout Recommendation Engine Architecture

### Key Learnings

**1. Exercise-level data is important**

Built an exercise database mapping each exercise to primary and secondary muscles.

---

**2. Recommendation logic needs muscle tracking**

The system must know which muscles were trained before suggesting the next workout.

---

**3. Compound vs isolation exercises differ**

Compound lifts affect multiple muscles, while isolation movements may have little or no secondary involvement.

---

## Biggest Takeaway

Smart systems are built on well-structured logic before adding machine learning.

# June 28

## Focus: Muscle Recovery Tracking Logic

### Key Learnings

**1. Historical workout data can be used to track muscle recovery**

Built logic to identify the latest training date for each muscle based on exercise history.

---

**2. Exercise-to-muscle mapping enables deeper analytics**

Used primary and secondary muscle mappings to understand which muscles were involved in past workouts.

---

**3. Datetime handling is essential for analytics**

Calculated days since each muscle was last trained using Python datetime functions.

---

## Biggest Takeaway

Good recommendation systems depend on structured tracking logic before introducing AI/ML.

# June 29

Refactored workout history system to separately track primary and secondary muscle involvement for each exercise.

Built recovery tracking logic to calculate days since each muscle was trained directly or indirectly.

Updated recommendation engine to filter recently trained muscles, detect overdue muscles, and generate recovery-aware workout recommendations using priority scoring with secondary muscle fatigue penalties.

Completed Phase 1 backend logic for AI Fitness Tracker.

# July 4

## Tasks Completed

- Created a dedicated **Log Workout** page in Streamlit.
- Added a workout date picker using `st.date_input()`.
- Added an exercise dropdown using `exercise_database`.
- Implemented dynamic set generation based on the selected number of sets.
- Added reps and weight input fields for each workout set.
- Refactored workout-saving logic by introducing `save_workout()` in `tracker.py`.
- Separated UI from business logic, allowing both the CLI and Streamlit interfaces to reuse the same backend.
- Integrated the Streamlit workout page with `save_workout()`.
- Verified successful workout logging to the CSV through the Streamlit interface.
- Preserved automatic Personal Record (PR) detection within the Streamlit workflow.

---

## Design Decisions

- All workout processing and saving logic remains inside `tracker.py`.
- Streamlit is responsible only for collecting user input and displaying results.
- The new `save_workout()` function serves as a shared backend for both the CLI and Streamlit interfaces, eliminating code duplication.
- Multiple PRs achieved within the same workout session are intentionally preserved to maximize user feedback and motivation.
- Workout data continues to be stored in the existing CSV format, ensuring full backward compatibility with the CLI version.
- UI and backend responsibilities are kept separate to improve maintainability and simplify future integration with databases, APIs, or additional frontends.

# July 6

## Tasks Completed

- Designed the dashboard backend architecture.
- Implemented `get_workout_dates()` to retrieve unique workout session dates.
- Implemented `get_total_workout_sessions()` using reusable backend helpers.
- Designed `get_total_exercises_logged()` using unique `(Date, Exercise)` pairs.
- Finalized the dashboard layout and replaced the workout streak with a workout calendar for better long-term user motivation.

## Concepts Learned

### Pandas
- `.shape`
- `.drop_duplicates()`
- `.tolist()`

### Design Principles
- Single Responsibility Principle for backend helper functions.
- Importance of reusable backend APIs before building the UI.

## Next Steps

- Implement `get_total_exercises_logged()`.
- Build `get_recent_workouts()`.
- Start rendering the dashboard metrics and workout calendar in Streamlit.

# July 7

## Tasks Completed

- Implemented `get_recent_workouts()` helper function using a complete Pandas pipeline.
- Learned and applied:
  - `groupby()`
  - `agg()`
  - `reset_index()`
- Implemented `get_last_workout_date()` helper function.
- Improved dashboard architecture by keeping all business logic inside `tracker.py`.
- Added empty-state handling for the Recent Workouts section.

## Design Decisions

- Dashboard remains presentation-only; all data processing stays inside `tracker.py`.
- Dates continue to be stored in ISO format (`YYYY-MM-DD`) inside CSV files for reliable sorting and parsing.
- Dashboard gracefully handles first-time users by displaying an informational message instead of an empty table.
- Helper functions were designed to remain reusable across future pages (analytics, calendar, recommendations).

# July 8

## Tasks Completed

- Improved understanding of the Streamlit Calendar component's interaction model.
- Stored the calendar widget output in a variable (`calendar_state`) instead of rendering it directly.
- Explored the FullCalendar event callback payload and identified the path required to extract the selected workout date.
- Designed the workflow for displaying workout details after clicking a workout event.
- Implemented backend function `get_workout_details(date)` to retrieve all exercises performed on a selected workout date.

## Concepts Learned

### Dictionary Traversal

Learned how nested dictionaries can be accessed step-by-step:

```python
calendar_state
    ↓
eventClick
    ↓
event
    ↓
start
```

which corresponds to

```python
calendar_state["eventClick"]["event"]["start"]
```

### Backend/UI Separation

Continued following the project's architecture:

```
Calendar
      ↓
selected_date
      ↓
tracker.py
      ↓
CSV lookup
      ↓
DataFrame
      ↓
Streamlit display
```

The UI never accesses CSV files directly. All data retrieval remains inside `tracker.py`.

# July 9

# Work Completed

## ❤️ Recovery Page

- Built a complete Recovery page using Streamlit.
- Added workout date selector with the latest workout selected by default.
- Connected frontend with the recovery backend (`recovery_score()`).
- Displayed:
  - Overall Recovery Score
  - Sleep Score
  - Calorie Score
  - Fatigue Score
  - Recovery Status
  - Recovery Recommendation
- Handled insufficient workout history by displaying Fatigue as **N/A**.
- Refactored the recovery backend to return structured dictionaries instead of a single numeric score.

---

## 🤖 Recommendation Page

- Built the complete Recommendation (Coach) page.
- Connected frontend with the recommendation engine.
- Displays:
  - Today's recommended training focus
  - Priority ranking of muscles
  - Neglected muscle alerts
  - Recommendation reason
- Refactored recommendation backend to return structured data including:
  - Top recommendation
  - Recommendation ranking
  - Recommendation reason

---

# Concepts Learned

- Using `st.selectbox()` with `format_func` to display user-friendly dates while keeping raw backend values.
- Returning structured dictionaries from backend functions instead of primitive values.
- Keeping business logic inside backend modules while restricting Streamlit pages to presentation only.
- Designing backend functions that can be reused by different frontends.

---

# Architecture Improvements

- Recovery system now returns:
  - Recovery Score
  - Sleep Score
  - Calorie Score
  - Fatigue Score
  - Recovery Status
  - Recommendation Message
- Recommendation engine now returns:
  - Training Focus
  - Top Recommendation
  - Priority Ranking
  - Recommendation Reason
- Improved separation between backend computation and frontend rendering following the **Single Responsibility Principle**.

---

# Learnings

Today's session focused on integrating backend systems with Streamlit. The biggest takeaway was understanding how returning structured data from backend functions simplifies frontend development and keeps responsibilities clearly separated.

# July 28 – August 8

## Focus: Database Architecture, SQL and Hevy Data Migration

This phase focused on moving RepWise from CSV-based persistent storage toward a structured SQLite database while simultaneously developing practical SQL knowledge.

---

## Database Architecture

Designed the initial SQLite architecture for RepWise.

Created a relational structure separating:

- workout sessions
- exercises
- workout sets
- exercise categories
- primary muscles
- secondary muscles

Established relationships between the tables using primary and foreign keys.

### Concepts Learned

- Primary keys
- Foreign keys
- One-to-one relationships
- One-to-many relationships
- Many-to-one relationships
- Referential integrity
- Foreign key constraints
- `ON DELETE RESTRICT`
- Database schema vs database instance
- Indexes
- SQLite `PRAGMA` statements

---

## SQL Theory

Completed the major SQL concepts required for the current RepWise database work.

### Learned / Revised

- Joins
- Outer joins
- CTEs
- Window functions
- Transactions
- `ORDER BY`
- `GROUP BY`
- Aggregations
- Foreign-key related queries
- Database integrity checks

The focus was intentionally kept practical rather than spending excessive time on SQL theory.

The goal was to understand enough SQL to begin learning SQLite directly while implementing RepWise.

---

## SQLite Architecture

Created the RepWise SQLite database and implemented the initial schema.

Learned how Python communicates with SQLite through:

```python
conn = get_connection()
cursor = conn.cursor()
cursor.execute(...)
```

---

# August 9, 2026

## Focus: SQLite Database Integration — Query and Transaction Layer

### Tasks Completed

- Created the database query/data-access layer in `database/queries.py`.
- Tested database queries for workout sessions and workout history.
- Added exercise history retrieval.
- Added recent workout retrieval.
- Added daily metrics retrieval.
- Added SQLite write functions.
- Tested workout session and workout set insertion.
- Tested daily metrics insertion and retrieval.
- Built a transaction-based workout write pipeline.
- Tested successful transactions.
- Tested transaction rollback.
- Cleaned all temporary test data after testing.

---

## Concepts Learned

### 1. Database Access Layer

SQL queries should not be scattered throughout `tracker.py`, `recovery.py`, Streamlit pages, and other application modules.

Instead:

```text
Application
    ↓
queries.py
    ↓
SQLite
```

## Aug 10, 2026 — Backend Data Migration (CSV → SQLite)

### What changed
Migrated `tracker.py`, `recovery.py`, `recommendation_engine.py` off direct CSV access onto DB-backed query functions.

### Key function migrations
- `load_workout_data()`, `load_daily_data()` → `get_workout_history()`, `get_daily_metrics_history()`, `get_exercise_history()`
- Analytics now DB-backed: `get_total_volume()`, `get_average_session_volume()`, `get_volume_history()`, `get_bodyweight_history()`, `get_all_exercises()`, `get_exercise_progress()`, `get_heaviest_lift()`
- Recommendation engine now pulls history via `get_workout_history()` instead of reading `workout_sets.csv` directly

### Function semantics worth remembering
- `get_average_session_volume()` = average of **per-workout totals** (not average of individual sets). Answers "avg volume per workout session."
- `get_volume_history()` = date → total workout volume (for trend plotting).
- `get_heaviest_lift()` = scans full history, returns max valid weight + exercise.

### Pipelines unchanged (logic-wise, just data source swapped)
**Recovery:**

Daily Metrics → Sleep Score + Calorie Score + Workout Fatigue Score → Recovery Score → Interpretation

Fatigue calc still uses last 10 sessions; skips scoring if insufficient history.

**Recommendation:**

Workout History → Exercise→Muscle Mapping → Last Trained Muscle → Days Since Training
→ Recently Trained Filter → Overdue Muscle Check → Priority Scores → Recommendation

Primary/secondary muscle involvement still tracked separately.

### Cleanup
- `helpers.py` stripped of CSV-loading responsibility.
- Confirmed `load_daily_data()` was an unused/dead definition, not an active dependency.
- `pd.read_csv(...)` / `DAILY_METRICS_FILE` no longer in active app flow.

### Big lesson
Migration ≠ swapping one line (`pd.read_csv(...)` → `get_workout_history()`). The real win is that higher-level modules no longer need to know **where** data lives:

UI → Business Logic → Database Query Layer → SQLite

DB layer = single source of truth. If we ever move SQLite → Postgres later, only the query layer changes — not tracker/recovery/recommendation/Streamlit/CLI.

### Status
| Component | Status |
|---|---|
| Backend migration | ✅ Complete |
| CSV cleanup | ✅ Complete |
| Tracker / Recovery / Recommendation | ✅ Migrated |
| Helpers | ✅ Cleaned |
| Streamlit | ✅ Connected |
| Testing | ⏳ Next session |

### Next session
Systematic end-to-end testing (not new features):

Database → Queries → Tracker → Recovery → Recommendation → Streamlit UI → E2E workflow

Cover normal + edge cases — confirms migration works as a *system*, not just per-function.

# August 11

## Focus: SQLite + Streamlit Integration Debugging

### What We Tested

Started testing the migrated SQLite backend through the Streamlit application instead of relying only on isolated backend tests.

The first issue appeared when running Streamlit:

```
streamlit : The term 'streamlit' is not recognized
```

The application was then launched through the correct Python environment.

### Dashboard Calendar Debugging

When clicking a workout on the dashboard calendar, the application initially displayed:

```
No workout found for this date.
```

The problem was caused by a mismatch between the calendar event data and the new SQLite session-based architecture.

The dashboard originally attempted to retrieve workout details using the selected date, while:

```
get_workout_details(session_id)
```

expects a `session_id`.

### Key Learning

The calendar should identify a workout session rather than directly querying workout data by date.

The relationship is:

```
Calendar Event
      ↓
session_id
      ↓
workout_sessions
      ↓
workout_sets
      ↓
Workout Details
```

### Debugging Process

The calendar callback structure was inspected when errors appeared involving:

- `extendedProps`
- `id`

The event data was adjusted until the dashboard correctly retrieved the session ID and passed it into `get_workout_details(session_id)`.

### Important Architecture Insight

The migration changed the application's fundamental data relationship.

Previously:

```
Date → Workout Data
```

Now:

```
Date → Workout Session → Workout Sets
```

This is a stronger structure because one session can contain multiple exercises while maintaining a single workout identity.

### Biggest Takeaway

Debugging database-backed applications requires tracing the entire data flow instead of fixing only the visible error.

```
UI
↓
Calendar callback
↓
Session ID
↓
SQL query
↓
Workout sets
↓
DataFrame
↓
UI
```

---

# August 12

## Focus: End-to-End Workout Logging Testing

### Goal

Validate the complete Streamlit workout logging workflow after the SQLite migration.

The objective was to test the actual application rather than only individual functions.

### Exercise Database Debugging

The workout logger initially displayed only 22 exercises even though the new `exercise_database.py` contained 50.

Investigated the imported module directly using:

```python
import exercise_database as exercise_db

exercise_db.__file__
len(exercise_db.exercise_database)
```

Confirmed that Streamlit was loading `src/exercise_database.py` and that it contained all 50 intended exercises.

The earlier 22-exercise list was caused by stale/import state rather than the final exercise database itself.

### Exercise Name Consistency

Confirmed that the new exercise catalog uses the exact names expected by SQLite.

Examples:

- Leg Press (Machine)
- Bench Press (Barbell)
- Seated Leg Curl (Machine)

This is important because workout logging resolves:

```
Exercise Name
      ↓
SQLite exercise lookup
      ↓
exercise_id
```

Using inconsistent names such as `Leg Press` instead of `Leg Press (Machine)` causes the database lookup to fail.

### Session ID Architecture

Reviewed the relationship between workout sessions and exercises.

A `session_id` belongs to the entire workout session, not to an individual exercise.

Example:

```
Session 228
│
├── Leg Press (Machine)
│   ├── Set 1
│   ├── Set 2
│   └── Set 3
│
└── Seated Leg Curl (Machine)
    ├── Set 1
    ├── Set 2
    └── Set 3
```

This confirmed that multiple exercises can correctly share one `session_id`.

### `save_workout_session()` Understanding

Reviewed the database save pipeline:

```
save_workout()
      ↓
save_workout_session()
      ↓
create_workout_session()
      ↓
session_id
      ↓
exercise name → exercise_id
      ↓
add_workout_set()
      ↓
commit
```

The entire workout is saved inside one transaction.

If an error occurs, `conn.rollback()` prevents a partially saved workout.

### Successful Tests

**Test 1 — Single Exercise**

Logged: Leg Press (Machine), 3 sets

Result:

```
Workout logged successfully!
Session ID: 227
```

**Test 2 — Multiple Exercises**

Logged:
- Leg Press (Machine), 3 sets
- Seated Leg Curl (Machine), 3 sets

Result:

```
Workout logged successfully!
Session ID: 228
```

This successfully demonstrated that multiple exercises can be stored under one workout session.

### Final Verification

The dashboard calendar successfully retrieved and displayed the workout details after the earlier session-ID debugging.

The complete workflow is now:

```
Streamlit UI
    ↓
Exercise Selection
    ↓
Workout Session Creation
    ↓
session_id
    ↓
Exercise Name → exercise_id
    ↓
Workout Sets
    ↓
SQLite Transaction
    ↓
Dashboard Calendar
    ↓
Session Details
```

### Cleanup

The two test sessions created during validation were:

- Session 227
- Session 228

These were temporary testing records and were identified for deletion without removing the underlying exercise records.

### Biggest Takeaway

The SQLite migration is no longer theoretical.

The application has now been tested through the actual Streamlit interface, including:

- Exercise selection
- Set input
- SQLite exercise lookup
- Session creation
- Multiple exercises per session
- Set insertion
- Transaction handling
- Session retrieval
- Calendar integration
- Workout detail display

The core v0.7 workout workflow has reached the integration-testing stage.

# August 13

## Focus: v0.7 Final Integration Testing & Completion

**Goal:** Complete the final integration testing for v0.7 after the SQLite backend migration, verifying that the migrated database works correctly with the major RepWise features through the actual Streamlit application.

*(This session's testing is what closed out the v0.7 milestone — see `RepWise_v0.7_Completion_Summary.md` for the full milestone overview.)*

---

## 1. Updated Hevy Dataset

The previous Hevy export only contained data through August 3. A new Hevy CSV export was generated through August 12 and used to test incremental importing into the existing SQLite database.

The important part of this test was that existing workouts should not be duplicated. The importer uses the workout `start_time` as the `hevy_session_key`:

```python
SELECT session_id
FROM workout_sessions
WHERE hevy_session_key = ?
```

If the session already exists, it is skipped:

```python
if not is_new:
    conn.rollback()
    print(f"Skipping already imported workout: {start_time}")
    continue
```

This allows a complete new Hevy export to be imported without duplicating previously migrated workouts.

**Result:** Existing workouts were skipped and the newer workouts were imported successfully. This confirmed that the importer supports incremental migration from updated Hevy exports.

---

## 2. Recovery Score Debugging

Recovery initially displayed:

> Daily metrics not found for this workout.
> Please log Sleep, Calories and Bodyweight first.

The daily metrics were present in SQLite, so the issue was not missing data. The problem was a **date-format mismatch**.

The recovery system compared the workout date against the daily metrics date:

```python
today_data = daily_df[daily_df["Date"] == date]
```

The two values could have different formats, such as `2026-08-11` versus `2026-08-11 00:00:00`.

Both dates were normalized to the same format:

```python
daily_df["Date"] = pd.to_datetime(
    daily_df["Date"]
).dt.strftime("%Y-%m-%d")

date = pd.to_datetime(date).strftime("%Y-%m-%d")
```

After this change, Recovery successfully found the daily metrics.

**Key Learning:** Database migrations often expose hidden assumptions about data types and formatting. The database may contain the correct information while the application still fails because two representations of the same value are not normalized before comparison.

---

## 3. Recovery Score Successfully Tested

After fixing date normalization, the Recovery Score successfully appeared in RepWise.

The recovery system combines: **Sleep + Calories + Fatigue**

The fatigue component uses recent workout volume when sufficient workout history is available. The final score is interpreted into statuses such as: `Excellent`, `Good`, `Moderate`, `Poor`, `Very Poor`.

This confirmed that Recovery is successfully reading data from the migrated SQLite backend.

---

## 4. Workout Recommendations

Workout recommendations were also visible and functioning after the migration. This confirmed that the recommendation system can operate using the migrated workout and recovery data.

The broader pipeline is now:

```
SQLite Workout Data
        ↓
Recovery / Training Analysis
        ↓
Workout Recommendations
```

---

## 5. Analytics

Analytics were successfully displayed after importing the newer Hevy dataset. This confirmed that the analytics system can read the migrated workout history from SQLite and operate on the expanded dataset.

The end-to-end flow is now:

```
Hevy CSV
   ↓
Importer
   ↓
SQLite
   ↓
Workout History
   ↓
Analytics
```

---

## 6. Full v0.7 Workflow Verified

The major RepWise workflow is now functioning end-to-end:

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

Manual workout logging also works:

```
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

## Final Result

v0.7 is considered complete. The application has moved beyond simply having the SQLite migration implemented and has now been validated through the actual Streamlit workflow.

The most important lesson from this testing phase was that successful migration requires testing the entire data flow:

```
UI
↓
Application Logic
↓
Database Queries
↓
SQLite
↓
Application Logic
↓
UI
```

A feature can work correctly in isolation but still fail when connected to the migrated database. The Recovery date-format bug was a good example of this: the data existed correctly in SQLite, but the application could not find it until both date representations were normalized.

v0.7 is therefore a completed SQLite-backed integration milestone.
