# Workout CSV Import Format

RepWise imports workout data from a Hevy CSV export and stores it in SQLite. The importer expects a specific set of column names. **All 14 required column headers must be present**, even if some individual cells are blank.

The importer does not currently automatically match alternative column names. If your CSV comes from another source, you may need to rename its columns to match this format.

## 1. Required Columns

Your CSV must contain these exact column names:

| Column | Description |
|---|---|
| `title` | Workout/session title |
| `start_time` | Workout start timestamp |
| `end_time` | Workout end timestamp |
| `description` | Workout description |
| `exercise_title` | Exercise name |
| `superset_id` | Superset identifier, if applicable |
| `exercise_notes` | Notes associated with the exercise/set |
| `set_index` | Set index/order from the export |
| `set_type` | Set type, such as normal or warm-up |
| `weight_kg` | Weight lifted, in kilograms |
| `reps` | Number of repetitions |
| `distance_km` | Distance, in kilometres |
| `duration_seconds` | Duration, in seconds |
| `rpe` | Rate of perceived exertion |

**Important:** Column names must match exactly. The importer checks for the presence of all required headers before processing the file.

## 2. Data Types and Cleaning

The importer processes the columns as follows:

### Text columns

The following columns are treated as text:

- `title`
- `description`
- `exercise_title`
- `exercise_notes`
- `set_type`
- `superset_id`

Text values are trimmed of surrounding whitespace. Missing text values are converted to empty strings during initial cleaning, and empty strings are then converted to missing values.

### Numeric columns

The following columns are converted to numeric values:

- `set_index`
- `weight_kg`
- `reps`
- `distance_km`
- `duration_seconds`
- `rpe`

Values that cannot be converted to numbers are treated as missing values rather than causing the conversion to fail.

### Timestamp columns

- `start_time`
- `end_time`

Timestamps are parsed and normalized to the format:

`YYYY-MM-DD HH:MM:SS`

The importer uses `start_time` to group rows belonging to the same workout session and to identify previously imported sessions.

## 3. How Workout Rows Are Imported

RepWise treats each CSV row as a workout set.

During import:

1. The CSV is loaded using Pandas.
2. The required columns are validated.
3. Text, numeric values, and timestamps are cleaned.
4. Rows are sorted and grouped by `start_time`.
5. A workout session is created or matched in SQLite.
6. Exercises are matched by name or created if they do not already exist.
7. Sets are inserted with their associated session and exercise IDs.

Workout-level information, such as the title and description, is taken from the rows belonging to that session.

## 4. Duplicate Handling

RepWise uses the normalized `start_time` as the workout session's import key (`hevy_session_key`).

If a session with that key already exists, the importer skips the session instead of importing it again. This helps prevent duplicate workout data when importing the same export more than once.

**Limitation:** Two distinct workouts with exactly the same normalized start timestamp may be treated as duplicates.

## 5. Transaction and Error Handling

Each workout session is imported inside a database transaction.

- If a session imports successfully, its changes are committed.
- If the session already exists, it is skipped.
- If an error occurs while importing a session, that session's transaction is rolled back and the importer reports the failure.

This prevents a failed session import from leaving partially inserted data for that session.

## 6. Using CSV Files from Other Sources

RepWise currently expects the exact column names listed in Section 1. It does not automatically map different column names to the expected schema.

If you are importing data from another workout app or a custom spreadsheet:

1. Export or prepare your data as a CSV file.
2. Rename the columns to match RepWise's required schema.
3. Ensure weight is represented in kilograms, distance in kilometres, and duration in seconds.
4. Ensure timestamps can be parsed by Pandas.
5. Check that each row represents a set and that session timestamps are consistent across rows belonging to the same workout.
6. Import the prepared CSV using the project's documented import procedure.

Some sources may not provide every field. The required headers must still exist, but whether blank values are appropriate depends on the field and how the rest of the application uses it.

Automatic column matching and more flexible import support may be added in a future version.

## 7. Import Limitations

Current limitations include:

- All 14 required column headers must be present.
- Alternative column names are not automatically mapped.
- Numeric values that cannot be parsed become missing values.
- Session deduplication relies on the normalized start timestamp.
- The importer does not automatically infer or convert different measurement units.

For reliable results, prepare your CSV according to the documented schema before importing it.
