import streamlit as st
from recommendation_engine import *

st.title("🏋 Coach")

st.divider()

recommendation = recommend_next_workout()

if recommendation["training_focus"] == "neglected_muscle":

    st.subheader("🎯 Today's Focus")

    for muscle in recommendation["muscles"]:
        st.success(f"Train **{recommendation['top_recommendation'].title()}** today!")

    st.divider()

    st.subheader("⚠ Neglected Muscles")

    for muscle in recommendation["muscles"]:
        st.write(f"• {muscle.title()}")

    st.divider()

    st.subheader("📌 Reason")

    st.info(recommendation["reason"])

else:

    st.subheader("🎯 Today's Focus")

    st.success(
        f"Train **{recommendation['top_recommendation'].title()}** today!"
    )

    st.divider()

    st.subheader("🏋 Training Priority")

    medals = ["🥇", "🥈", "🥉"]

    for i, muscle in enumerate(recommendation["recommendations"]):

        if i < 3:
            prefix = medals[i]
        else:
            prefix = f"{i+1}."

        st.write(f"{prefix} **{muscle.title()}**")

    st.divider()

    st.subheader("📌 Reason")

    st.info(recommendation["reason"])