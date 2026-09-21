import joblib
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import numpy as np
import pandas as pd

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

def prepare_data():

    df = build_ml_dataset()

    # Create delta target
    df["target_change"] = (
        df["target_e1rm"] - df["last_e1rm"]
    )

    df = df.dropna(
        subset=FEATURE_COLUMNS
        + ["target_change", "target_e1rm"]
    )

    df = df.sort_values(
        ["session_date", "session_id"]
    )

    X = df[FEATURE_COLUMNS]

    # Model will now learn CHANGE
    y = df["target_change"]

    return df, X, y

def train_model():

    df, X, y = prepare_data()

    # -----------------------------------------------------
    # Chronological 80/20 split
    # -----------------------------------------------------

    split_index = int(len(df) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    test_df = df.iloc[split_index:].copy()

    # -----------------------------------------------------
    # Train Linear Regression
    # -----------------------------------------------------

    model = LinearRegression()

    model.fit(
        X_train,
        y_train
    )

    MODEL_DIR = Path(__file__).resolve().parent / "models"
    MODEL_DIR.mkdir(exist_ok=True)

    MODEL_PATH = MODEL_DIR / "e1rm_delta_model.joblib"

    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to: {MODEL_PATH}")

    # -----------------------------------------------------
    # Predictions
    # -----------------------------------------------------
    predicted_change = model.predict(X_test)

    # Actual next e1RM
    actual_e1rm = (df.iloc[split_index:]["target_e1rm"].to_numpy())

    # Convert predicted change back into e1RM
    predicted_e1rm = (X_test["last_e1rm"].to_numpy()+ predicted_change) 

    # -----------------------------------------------------
    # Overall model evaluation
    # -----------------------------------------------------

    mae = mean_absolute_error(
        actual_e1rm,
        predicted_e1rm
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual_e1rm,
            predicted_e1rm
        )
    )

    delta_r2 = r2_score(
        y_test,
        predicted_change
    )

    # -----------------------------------------------------
    # Naive baseline
    # -----------------------------------------------------
    baseline_e1rm = (
    X_test["last_e1rm"].to_numpy()
    )

    baseline_mae = mean_absolute_error(
    actual_e1rm,
    baseline_e1rm
    )

    print("\n===== DELTA MODEL PERFORMANCE =====")

    print(f"Next-e1RM MAE:  {mae:.2f}")
    print(f"Next-e1RM RMSE: {rmse:.2f}")
    print(f"Delta R²:       {delta_r2:.3f}")
    print(f"Baseline MAE:   {baseline_mae:.2f}")

    # -----------------------------------------------------
    # Add predictions to test dataframe
    # -----------------------------------------------------

    # Actual next-session e1RM
    test_df["actual_e1rm"] = test_df["target_e1rm"]

    # Predicted next-session e1RM
    test_df["predicted_change"] = predicted_change

    test_df["predicted_e1rm"] = (
        test_df["last_e1rm"]
        + test_df["predicted_change"]
    )

    # Baseline = assume no change
    test_df["baseline_prediction"] = test_df["last_e1rm"]

    # Absolute errors
    test_df["model_error"] = abs(
        test_df["actual_e1rm"]
        - test_df["predicted_e1rm"]
    )

    test_df["baseline_error"] = abs(
        test_df["actual_e1rm"]
        - test_df["baseline_prediction"]
    )

    # -----------------------------------------------------
    # Per-exercise diagnostics
    # -----------------------------------------------------

    exercise_results = (
        test_df
        .groupby("exercise_name")
        .agg(
            samples=("exercise_name", "size"),

            model_mae=(
                "model_error",
                "mean"
            ),

            baseline_mae=(
                "baseline_error",
                "mean"
            )
        )
        .reset_index()
    )

    exercise_results["improvement"] = (
        exercise_results["baseline_mae"]
        - exercise_results["model_mae"]
    )

    exercise_results = (
        exercise_results
        .sort_values(
            "samples",
            ascending=False
        )
    )

    print("\n===== PER-EXERCISE PERFORMANCE =====")

    print(
        exercise_results.head(20).to_string(
            index=False
        )
    )

    # -----------------------------------------------------
    # Worst predictions
    # -----------------------------------------------------

    worst_predictions = (
        test_df
        .sort_values(
            "model_error",
            ascending=False
        )
        .head(15)
    )

    print("\n===== WORST PREDICTIONS =====")

    print(
        worst_predictions[
            [
                "session_date",
                "exercise_name",
                "last_e1rm",
                "actual_e1rm",
                "predicted_e1rm",
                "model_error"
            ]
        ].to_string(
            index=False
        )
    )

    # -----------------------------------------------------
    # Model coefficients
    # -----------------------------------------------------

    print("\n===== MODEL COEFFICIENTS =====")

    for feature, coefficient in zip(
        FEATURE_COLUMNS,
        model.coef_
    ):
        print(
            f"{feature:25s}: "
            f"{coefficient:.5f}"
        )

    print(
        f"{'Intercept':25s}: "
        f"{model.intercept_:.5f}"
    )

    return model


if __name__ == "__main__":

    train_model()