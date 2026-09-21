import streamlit as st
from tracker import *
from ml.predict import predict_next_e1rm


st.title("📈 Analytics")

st.divider()

# ---------------------------------------------------------
# OVERALL STATS
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Workout Sessions",
        get_total_workout_sessions()
    )

with col2:
    st.metric(
        "Exercises Logged",
        get_total_exercises_logged()
    )

col3, col4 = st.columns(2)

with col3:
    st.metric(
        "Total Volume",
        f"{get_total_volume():,} kg"
    )

with col4:
    st.metric(
        "Avg Session Volume",
        f"{get_average_session_volume():,.0f} kg"
    )


st.divider()


# ---------------------------------------------------------
# EXERCISE PROGRESS
# ---------------------------------------------------------

st.subheader("🏋 Exercise Progress")

exercise_list = get_all_exercises()

if len(exercise_list) == 0:

    st.info("No workouts logged yet.")

else:

    selected_exercise = st.selectbox(
        "Select Exercise",
        exercise_list
    )

    progress_df = get_exercise_progress(
        selected_exercise
    )

    if not progress_df.empty:

        st.line_chart(
            progress_df.set_index("Date")["Weight"]
        )

    else:

        st.info(
            "No progress history available "
            "for this exercise."
        )

    # -----------------------------------------------------
    # ML PERFORMANCE PREDICTION
    # -----------------------------------------------------

    st.subheader("🤖 Predicted Next Performance")

    prediction = predict_next_e1rm(
        selected_exercise
    )

    if prediction is None:

        st.info(
            "Not enough workout history to generate "
            "a prediction for this exercise yet."
        )

    else:

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Current e1RM",
            f"{prediction['current_e1rm']:.1f} kg"
        )

        col2.metric(
            "Predicted Next e1RM",
            f"{prediction['predicted_e1rm']:.1f} kg"
        )

        col3.metric(
            "Expected Change",
            f"{prediction['predicted_change']:+.1f} kg"
        )

        st.caption(
            "Experimental ML prediction based on "
            "recent performance, training volume "
            "and exercise history."
        )


st.divider()


# ---------------------------------------------------------
# WORKOUT VOLUME TREND
# ---------------------------------------------------------

st.subheader("📊 Workout Volume Trend")

volume_df = get_volume_history()

if not volume_df.empty:

    st.line_chart(
        volume_df.set_index("Date")["Volume"]
    )

else:

    st.info(
        "No workout history available."
    )


st.divider()


# ---------------------------------------------------------
# BODYWEIGHT TREND
# ---------------------------------------------------------

st.subheader("⚖️ Bodyweight Trend")

bodyweight_df = get_bodyweight_history()

if not bodyweight_df.empty:

    st.line_chart(
        bodyweight_df.set_index("Date")["Bodyweight"]
    )

else:

    st.info(
        "No bodyweight history available."
    )