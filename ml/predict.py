import joblib
from pathlib import Path

from .features import build_ml_dataset


FEATURE_COLUMNS = [
    "last_e1rm",
    "last_volume",
    "recent_avg_e1rm",
    "recent_avg_volume",
    "historical_best_e1rm",
    "days_since_last",
    "exercise_session_count"
]


MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "e1rm_delta_model.joblib"
)


def predict_next_e1rm(exercise_name):

    model = joblib.load(MODEL_PATH)

    df = build_ml_dataset()

    exercise_df = (
        df[df["exercise_name"] == exercise_name]
        .sort_values(["session_date", "session_id"])
    )

    if exercise_df.empty:
        return None

    latest = exercise_df.iloc[-1]

    # Make sure all required features exist
    if latest[FEATURE_COLUMNS].isna().any():
        return None

    X_latest = latest[FEATURE_COLUMNS].to_frame().T

    predicted_change = model.predict(X_latest)[0]

    current_e1rm = latest["last_e1rm"]

    predicted_e1rm = (
        current_e1rm + predicted_change
    )

    return {
        "exercise_name": latest["exercise_name"],
        "current_e1rm": current_e1rm,
        "predicted_change": predicted_change,
        "predicted_e1rm": predicted_e1rm
    }