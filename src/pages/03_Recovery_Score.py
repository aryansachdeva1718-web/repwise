import streamlit as st
import pandas as pd
from tracker import *
from recovery import *

st.title("❤️ Recovery")
st.divider()


workout_dates = get_workout_dates()

if len(workout_dates) == 0:
    st.info(
        "No workouts logged yet.\n\n"
        "Log your first workout to calculate recovery."
    )
    st.stop()


selected_date = st.selectbox( "📅 Workout",
    options=workout_dates,
    index=len(workout_dates) - 1,          # Latest workout selected by default
    format_func=lambda x: pd.to_datetime(x).strftime("%d %b %Y")
)
st.divider()


recovery_data = recovery_score(selected_date)

if recovery_data is None:
    st.warning(
        "Daily metrics not found for this workout.\n\n"
        "Please log Sleep, Calories and Bodyweight first."
    )
    st.stop()


st.subheader("Recovery Score")

st.metric(
    label="",
    value=f"{recovery_data['score']}/100"
)

st.write(f"**Status:** {recovery_data['status']}")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "😴 Sleep",
        f"{recovery_data['sleep']}/50"
    )

with col2:
    st.metric(
        "🍽 Calories",
        f"{recovery_data['calories']}/30"
    )

with col3:

    if recovery_data["history_available"]:
        st.metric(
            "🏋 Fatigue",
            f"{recovery_data['fatigue']}/20"
        )
    else:
        st.metric(
            "🏋 Fatigue",
            "N/A"
        )

st.divider()


st.subheader("Recommendation")

st.info(recovery_data["message"])

