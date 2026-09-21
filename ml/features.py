import pandas as pd


def create_features(df):

    if df.empty:
        return df

    df = df.copy()

    df["session_date"] = pd.to_datetime(df["session_date"])

    df = df.sort_values(
        ["exercise_id", "session_date", "session_id"]
    )

    # -----------------------------------------------------
    # Latest/current performance
    # -----------------------------------------------------

    df["last_e1rm"] = df["best_e1rm"]

    df["last_volume"] = df["total_volume"]

    # -----------------------------------------------------
    # Recent averages - including current session
    # -----------------------------------------------------

    df["recent_avg_e1rm"] = (
        df
        .groupby("exercise_id")["best_e1rm"]
        .transform(
            lambda x:
            x.rolling(3, min_periods=1).mean()
        )
    )

    df["recent_avg_volume"] = (
        df
        .groupby("exercise_id")["total_volume"]
        .transform(
            lambda x:
            x.rolling(3, min_periods=1).mean()
        )
    )

    # -----------------------------------------------------
    # Historical best - including current session
    # -----------------------------------------------------

    df["historical_best_e1rm"] = (
        df
        .groupby("exercise_id")["best_e1rm"]
        .cummax()
    )

    # -----------------------------------------------------
    # Days since previous session
    # -----------------------------------------------------

    previous_date = (
        df
        .groupby("exercise_id")["session_date"]
        .shift(1)
    )

    df["days_since_last"] = (
        df["session_date"] - previous_date
    ).dt.days

    # -----------------------------------------------------
    # Session experience
    # -----------------------------------------------------

    df["exercise_session_count"] = (
        df
        .groupby("exercise_id")
        .cumcount()
        + 1
    )

    return df


def create_target(df):

    if df.empty:
        return df

    df = df.copy()

    df["target_e1rm"] = (
        df
        .groupby("exercise_id")["best_e1rm"]
        .shift(-1)
    )

    return df


def build_ml_dataset():

    from .dataset import build_exercise_dataset

    df = build_exercise_dataset()

    df = create_features(df)

    df = create_target(df)

    return df


if __name__ == "__main__":

    df = build_ml_dataset()

    print(df.head())