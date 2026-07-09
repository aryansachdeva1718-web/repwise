import streamlit as st
from tracker import *

st.title("📈 Analytics")

st.divider()

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

st.subheader("🏋 Exercise Progress")

exercise_list = get_all_exercises()

if len(exercise_list) == 0:

    st.info("No workouts logged yet.")

else:

    selected_exercise = st.selectbox(
        "Select Exercise",
        exercise_list
    )

    progress_df = get_exercise_progress(selected_exercise)

    st.line_chart(
        progress_df.set_index("Date")["Weight"]
    )

st.divider()

st.subheader("📊 Workout Volume Trend")

volume_df = get_volume_history()

if not volume_df.empty:

    st.line_chart(
        volume_df.set_index("Date")["Volume"]
    )

else:

    st.info("No workout history available.")

st.divider()

st.subheader("⚖️ Bodyweight Trend")

bodyweight_df = get_bodyweight_history()

if not bodyweight_df.empty:

    st.line_chart(
        bodyweight_df.set_index("Date")["Bodyweight"]
    )

else:

    st.info("No bodyweight history available.")