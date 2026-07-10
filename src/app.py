import streamlit as st
from tracker import *
from recovery import *
from recommendation_engine import *

st.set_page_config(
    page_title="RepWise",
    page_icon="🏋️",
    layout="wide"
)

st.title("🏋️ RepWise")
st.markdown("### Train Smarter. Track Better.")
st.caption("A data-driven fitness tracker built using Python, Pandas and Streamlit.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📅 Workout Sessions",
        get_total_workout_sessions()
    )

with col2:
    st.metric(
        "💪 Exercises Logged",
        get_total_exercises_logged()
    )

with col3:
    latest_date = get_last_workout_date()

    if latest_date:
        recovery = recovery_score(latest_date)
        st.metric(
            "❤️ Latest Recovery",
            f"{round(recovery['score'])}/100"
        )
    else:
        st.metric(
            "❤️ Latest Recovery",
            "-"
        )

st.caption(f"Last Workout: **{get_last_workout_date()}**")

st.divider()

recommendation = recommend_next_workout()

st.subheader("🎯 Today's Recommendation")

if recommendation["training_focus"] == "neglected_muscle":

    st.success(
        f"Train **{', '.join(recommendation['muscles'])}**"
    )

else:

    st.info(
        f"Priority Muscle: **{recommendation['recommendations'][0]}**"
    )

st.caption(recommendation["reason"])

st.divider()

st.subheader("📊 Quick Stats")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🏋 Total Volume",
        f"{get_total_volume():,} kg"
    )

with col2:
    st.metric(
        "📈 Avg Session",
        f"{get_average_session_volume():,.0f} kg"
    )

with col3:
    st.metric(
        "💪 Unique Exercises",
        len(get_all_exercises())
    )

heaviest = get_heaviest_lift()

if heaviest:

    st.info(
        f"🥇 **Heaviest Lift**\n\n{heaviest[0]} — **{heaviest[1]} kg**"
    )

st.divider()

st.subheader("🚀 Navigation")

st.markdown("""
Use the **sidebar** to navigate through the application.

- 🏠 Dashboard
- 📝 Log Workout
- 📝 Log Daily Metrics
- 📈 Analytics
- ❤️ Recovery
- 🤖 Recommendation
""")