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