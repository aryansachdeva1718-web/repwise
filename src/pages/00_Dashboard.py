import streamlit as st
from tracker import *
from streamlit_calendar import calendar

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

st.subheader("🗓️ Workout Calendar")

calendar_state = calendar(
    events=get_calendar_events(),
    options={
        "initialView": "dayGridMonth",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": ""
        }
    },
    custom_css={
        ".fc-event": {
            "background-color": "#3b82f6",
            "border-radius": "8px",
            "border": "none",
            "font-size": "12px",
            "text-align": "center",
            "padding": "2px"
        },
        ".fc-toolbar-title": {
            "font-size": "24px",
            "font-weight": "bold"
        },
        ".fc-day-today": {
            "background-color": "#1f2937"
        }
    },
    key="workout_calendar"
)

selected_date = None

if (calendar_state and calendar_state["callback"] == "eventClick"):
    selected_date = calendar_state["eventClick"]["event"]["start"]

if selected_date:
    st.subheader(f"📋 Workout Details - {selected_date}")
    details = get_workout_details(selected_date)
    st.dataframe(
        details,
        use_container_width=True
    )

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
