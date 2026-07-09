import streamlit as st
from tracker import *
from datetime import date

st.title("📝 Log Daily Metrics")

st.divider()

selected_date = st.date_input("📅 Date", value = date.today())

sleep = st.number_input(
    "😴 Sleep (hours)",
    min_value=0.0,
    max_value=24.0,
    step=0.5
)

calories = st.number_input(
    "🔥 Calories",
    min_value=0,
    step=50
)

bodyweight = st.number_input(
    "⚖️ Bodyweight (kg)",
    min_value=20.0,
    max_value=300.0,
    step=0.1
)

if st.button("💾 Save Metrics", use_container_width=True):

    log_daily_metrics(
        selected_date.strftime("%Y-%m-%d"),
        sleep,
        calories,
        bodyweight
    )

    st.success("✅ Daily metrics logged successfully!")
