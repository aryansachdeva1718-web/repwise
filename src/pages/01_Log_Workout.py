import streamlit as st
from tracker import *

st.title("🏋️ Log Workout")
st.divider()

date = st.date_input("Workout Date")

exercise = st.selectbox(
    "Select Exercise",
    list(exercise_database.keys()))

sets = st.number_input(
    "Number of Sets",
    min_value=1,
    max_value=10,
    value=3)

reps_list = []
weight_list = []

for i in range(sets):
    st.subheader(f"Set {i+1}")
    reps = st.number_input(f"Reps (Set {i+1})",
    min_value=1,
    step=1,
    key=f"reps_{i}")

    weight = st.number_input(
    f"Weight (kg) (Set {i+1})",
    min_value=0.0,
    step=2.5,
    key=f"weight_{i}")

    reps_list.append(reps)
    weight_list.append(weight)

if st.button("Log Workout"):
    pr_messages = save_workout(date, exercise, reps_list, weight_list)
    st.success("Workout logged successfully! ✅")

    if pr_messages:
        st.success("\n\n".join(pr_messages))





