SELECT
    session_id,
    title,
    start_time
FROM workout_sessions
ORDER BY session_id DESC
LIMIT 5;