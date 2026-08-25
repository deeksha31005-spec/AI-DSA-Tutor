import streamlit as st
import pandas as pd
import joblib


# -----------------------------
# Load model and dataset
# -----------------------------
model = joblib.load("model.pkl")
df = pd.read_csv("problems.csv")


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="AI DSA Tutor",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# Title
# -----------------------------
st.title("🤖 AI DSA Tutor")
st.subheader("Your Beginner-Friendly DSA Learning Assistant")

st.write(
    "Practice Data Structures and Algorithms with the help of a simple ML-based "
    "difficulty predictor."
)

st.divider()


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📚 DSA Topics")

topic = st.sidebar.selectbox(
    "Choose a topic",
    ["All"] + sorted(df["topic"].unique().tolist())
)


# -----------------------------
# Problem selection
# -----------------------------
if topic == "All":
    filtered_df = df
else:
    filtered_df = df[df["topic"] == topic]


if len(filtered_df) > 0:

    problem_index = st.selectbox(
        "Choose a DSA Problem",
        range(len(filtered_df)),
        format_func=lambda x: filtered_df.iloc[x]["question"]
    )

    problem = filtered_df.iloc[problem_index]

    st.header("📝 Problem")

    st.write(problem["question"])

    st.write("### 💡 Hint")

    if "hint" in problem:
        st.info(problem["hint"])

    st.write("### 📌 Topic")

    st.write(problem["topic"])

    st.write("### ⏱️ Time Complexity")

    st.write(problem["time_complexity"])

    st.write("### 💾 Space Complexity")

    st.write(problem["space_complexity"])

    st.divider()


    # -----------------------------
    # ML Difficulty Prediction
    # -----------------------------

    question_length = len(problem["question"])

    hint_count = 3

    has_recursion = (
        1 if problem["topic"].lower() == "recursion" else 0
    )

    has_nested_loop = (
        1 if "n^2" in str(problem["time_complexity"]).lower()
        else 0
    )

    uses_logarithmic = (
        1 if "log" in str(problem["time_complexity"]).lower()
        else 0
    )


    input_data = pd.DataFrame({
        "question_length": [question_length],
        "hint_count": [hint_count],
        "has_recursion": [has_recursion],
        "has_nested_loop": [has_nested_loop],
        "uses_logarithmic": [uses_logarithmic]
    })


    prediction = model.predict(input_data)[0]


    st.subheader("🤖 AI Difficulty Prediction")

    if prediction == "Easy":
        st.success("Predicted Difficulty: Easy")

    elif prediction == "Medium":
        st.warning("Predicted Difficulty: Medium")

    else:
        st.error("Predicted Difficulty: Hard")


else:

    st.warning("No problems found for this topic.")
