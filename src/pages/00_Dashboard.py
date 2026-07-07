import streamlit as st
from tracker import *

st.title("🏠 AI Fitness Dashboard")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="📅 Workout Sessions",
        value=get_total_workout_sessions()
    )

with col2:
    st.metric(
        label="💪 Exercises Logged",
        value=get_total_exercises_logged()
    )

with col3:
    st.metric(
        label="❤️ Recovery Score",
        value="Coming Soon"
    )

st.caption(f"📆 Last Workout: {get_last_workout_date()}")

st.divider()

st.subheader("📋 Recent Workouts")

recent_workouts = get_recent_workouts()
if recent_workouts.empty:
    st.info("No workouts logged yet.\n\nGo to the Log Workout page to record your first workout! 💪")

else:
    st.dataframe(
    recent_workouts,
    use_container_width=True
)
