import streamlit as st

st.set_page_config(
    page_title="RepWise",
    page_icon="🏋️",
    layout="wide"
)

st.title("🏋️ RepWise")
st.markdown("### Train Smarter. Track Better.")


st.divider()

st.subheader("📖 About RepWise")

st.write("""
**RepWise** is an intelligent strength training platform designed to help lifters
track workouts, monitor recovery, analyze performance, and make smarter training
decisions.

Rather than being just another workout logger, RepWise combines structured workout
tracking with recovery analysis, training analytics, and intelligent workout
recommendations—all within one unified platform.

The long-term vision is to integrate machine learning models trained on real-world
training history to provide personalized performance predictions and adaptive
training recommendations.
""")

st.divider()

st.subheader("🚀 Core Features")

feature_col1, feature_col2 = st.columns(2)

with feature_col1:
    st.markdown("""
- 💪 Workout Logging
- 🗓️ Interactive Workout Calendar
- ❤️ Recovery Analysis
- 📈 Performance Analytics
""")

with feature_col2:
    st.markdown("""
- 🎯 Workout Recommendation Engine
- 📊 Progress Visualization
- 🧠 Modular Python Backend
- 🌐 Streamlit Web Interface
""")

st.divider()

st.info(
    "Navigate using the sidebar to log workouts, record daily metrics, "
    "analyze performance, monitor recovery, and receive personalized "
    "workout recommendations."
)

st.caption(
    "Built with Python • Pandas • Streamlit • Matplotlib • Scikit-learn (Planned)"
)