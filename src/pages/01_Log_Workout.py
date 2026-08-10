import streamlit as st
from tracker import *
from exercise_database import exercise_database
from datetime import datetime

st.title("🏋️ Log Workout")
st.divider()

date = st.date_input("Workout Date")

title = st.text_input(
    "Workout Title",
    value="Workout"
)

# ---------- EXERCISE INPUT ----------

if "exercise_count" not in st.session_state:
    st.session_state.exercise_count = 1


if st.button("➕ Add Exercise"):
    st.session_state.exercise_count += 1

exercises = []


for exercise_index in range(st.session_state.exercise_count):

    st.subheader(f"💪 Exercise {exercise_index + 1}")

    exercise = st.selectbox(
        "Select Exercise",
        list(exercise_database.keys()),
        key=f"exercise_{exercise_index}"
    )

    sets = st.number_input(
        "Number of Sets",
        min_value=1,
        max_value=10,
        value=3,
        key=f"sets_{exercise_index}"
    )

    reps_list = []
    weight_list = []


    for set_index in range(sets):

        col1, col2 = st.columns(2)

        with col1:
            reps = st.number_input(
                f"Reps — Set {set_index + 1}",
                min_value=1,
                step=1,
                key=f"reps_{exercise_index}_{set_index}"
            )

        with col2:
            weight = st.number_input(
                f"Weight (kg) — Set {set_index + 1}",
                min_value=0.0,
                step=2.5,
                key=f"weight_{exercise_index}_{set_index}"
            )

        reps_list.append(reps)
        weight_list.append(weight)


    exercises.append({
        "exercise": exercise,
        "reps": reps_list,
        "weights": weight_list
    })


st.divider()


# ---------- SAVE WORKOUT ----------

if st.button("💾 Log Workout", use_container_width=True):

    start_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    try:

        session_id, pr_messages = save_workout_session(
            title=title,
            start_time=start_time,
            exercises=exercises
        )

        st.success(
            f"Workout logged successfully! "
            f"Session ID: {session_id}"
        )

        if pr_messages:

            st.success(
                "\n\n".join(pr_messages)
            )

    except Exception as e:

        st.error(
            f"Workout could not be saved: {e}"
        )





