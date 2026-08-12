import streamlit as st
from tracker import *
from recovery import *
from recommendation_engine import *
from streamlit_calendar import calendar

st.title("🏠 RepWise Dashboard")
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
    latest_date = get_last_workout_date()

    if latest_date:
        recovery = recovery_score(latest_date)

        if recovery is not None:
            recovery_value = f"{round(recovery['score'])}/100"
        else:
            recovery_value = "N/A"
    else:
        recovery_value = "-"

    st.metric(
        label="❤️ Latest Recovery",
        value=recovery_value)
    
st.caption(f"📆 Last Workout: {get_last_workout_date()}")

recommendation = recommend_next_workout()

if recommendation["training_focus"] == "neglected_muscle":

    st.success(
        f"🎯 Train **{', '.join(recommendation['muscles'])}**"
    )

else:

    st.info(
        f"🎯 Priority Muscle: **{recommendation['recommendations'][0]}**"
    )

st.caption(recommendation["reason"])

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
session_id = None

if calendar_state and calendar_state["callback"] == "eventClick":

    event = calendar_state["eventClick"]["event"]

    selected_date = pd.to_datetime(
        event["start"]
    ).strftime("%Y-%m-%d")

    workout_df = get_workout_history()

    if not workout_df.empty:

        workout_df["Date"] = pd.to_datetime(
            workout_df["Date"]
        ).dt.strftime("%Y-%m-%d")

        matching_sessions = (
            workout_df[
                workout_df["Date"] == selected_date
            ]["Session_ID"]
            .drop_duplicates()
            .tolist()
        )

        if matching_sessions:
            session_id = matching_sessions[0]


if session_id is not None:

    details = get_workout_details(session_id)

    if details.empty:
        st.info("No workout found for this session.")

    else:
        formatted_date = pd.to_datetime(
            selected_date
        ).strftime("%d %b %Y")

        st.subheader(
            f"📋 Workout Details - {formatted_date}"
        )

        # your existing details display continues here

    if details.empty:
        st.info("No workout found for this date.")

    else:
        formatted_date = (pd.to_datetime(selected_date).strftime("%d %b %Y"))
        st.subheader(f"📋 Workout Details - {selected_date}")
        

        exercise_count = details["Exercise"].nunique()
        total_sets = len(details)
        total_volume = (details["Weight"] * details["Reps"]).sum()

        summary_col1, summary_col2, summary_col3 = st.columns(3)
    
        with summary_col1:
            st.metric(
                label="Exercises",
                value=exercise_count)

        with summary_col2:
            st.metric(
                label = "Sets",
                value = total_sets)
        
        with summary_col3:
            st.metric(
                label= "Volume",
                value=f"{total_volume:,} kg")
        
        st.divider()

        groups = list(details.groupby("Exercise"))

        for i, (exercise, group) in enumerate(groups):

            st.markdown(f"### 💪 {exercise}")

            for _, row in group.iterrows():
                st.write(
                    f"**Set {row['Set']}** • "
                    f"{row['Weight']} kg × "
                    f"{row['Reps']} reps"
                )

            if i != len(groups) - 1:
                st.divider()
    
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
