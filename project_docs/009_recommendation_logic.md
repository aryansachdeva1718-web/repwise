# Workout Recommendation Engine Logic

## Current Scoring Logic (V1)

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