import streamlit as st
import pandas as pd
import joblib
import random

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI DSA Tutor",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# LOAD DATA AND MODEL
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv("problems.csv")


@st.cache_resource
def load_model():
    return joblib.load("model.pkl")


try:
    df = load_data()
except Exception as e:
    st.error("❌ Could not load problems.csv")
    st.write(e)
    st.stop()


try:
    model = load_model()
except Exception as e:
    st.error("❌ Could not load model.pkl")
    st.write(e)
    st.stop()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def find_column(dataframe, possible_names):
    """
    Finds a column even if its name is slightly different.
    """
    for name in possible_names:
        if name in dataframe.columns:
            return name

    # Try lowercase matching
    lower_columns = {
        str(col).lower().strip(): col
        for col in dataframe.columns
    }

    for name in possible_names:
        if name.lower() in lower_columns:
            return lower_columns[name.lower()]

    return None


def normalize_difficulty(value):
    """
    Converts different difficulty names into:
    Easy / Medium / Difficult
    """

    value = str(value).strip().lower()

    if value in ["easy", "beginner", "basic"]:
        return "Easy"

    if value in ["medium", "moderate", "intermediate"]:
        return "Medium"

    if value in ["difficult", "difficultly", "hard", "advanced"]:
        return "Difficult"

    return str(value).title()


def get_question_features(question):
    """
    Creates the same five features used while training
    the Decision Tree model.
    """

    question = str(question).lower()

    question_length = len(question.split())

    # Count possible hints in the question
    hint_count = question.count("hint")

    # Check recursion-related words
    has_recursion = int(
        "recursion" in question
        or "recursive" in question
    )

    # Check nested-loop-related words
    has_nested_loop = int(
        "nested loop" in question
        or "nested loops" in question
        or "two loops" in question
    )

    # Check logarithmic complexity
    uses_logarithmic = int(
        "logarithmic" in question
        or "log n" in question
        or "o(log" in question
        or "binary search" in question
    )

    return pd.DataFrame([{
        "question_length": question_length,
        "hint_count": hint_count,
        "has_recursion": has_recursion,
        "has_nested_loop": has_nested_loop,
        "uses_logarithmic": uses_logarithmic
    }])


def predict_difficulty(question):
    """
    Uses the trained ML model to predict difficulty.
    """

    try:
        features = get_question_features(question)
        prediction = model.predict(features)[0]
        return normalize_difficulty(prediction)

    except Exception:
        return "Not available"


# =========================================================
# FIND DATASET COLUMNS
# =========================================================

topic_col = find_column(
    df,
    ["topic", "Topic", "category", "Category"]
)

question_col = find_column(
    df,
    ["question", "Question", "problem", "Problem"]
)

hint_col = find_column(
    df,
    ["hint", "Hint"]
)

time_col = find_column(
    df,
    [
        "time_complexity",
        "Time Complexity",
        "time complexity",
        "time"
    ]
)

space_col = find_column(
    df,
    [
        "space_complexity",
        "Space Complexity",
        "space complexity",
        "space"
    ]
)

difficulty_col = find_column(
    df,
    [
        "difficulty",
        "Difficulty",
        "level",
        "Level"
    ]
)


# =========================================================
# TITLE
# =========================================================

st.title("🤖 AI DSA Tutor")

st.subheader("Your Beginner-Friendly DSA Learning Assistant")

st.write(
    "Practice Data Structures and Algorithms with "
    "difficulty-based questions and AI-powered difficulty prediction."
)

st.divider()


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

if topic_col is None:
    st.error("❌ Topic column was not found in problems.csv")
    st.write("Available columns:", list(df.columns))
    st.stop()

if question_col is None:
    st.error("❌ Question/Problem column was not found in problems.csv")
    st.write("Available columns:", list(df.columns))
    st.stop()


# =========================================================
# TOPIC SELECTION
# =========================================================

st.markdown("### 📚 Choose a DSA Topic")

topics = sorted(
    df[topic_col]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_topic = st.selectbox(
    "Select a topic:",
    ["All"] + topics
)


# =========================================================
# DIFFICULTY SELECTION
# =========================================================

st.markdown("### 🎯 Choose Difficulty Level")

selected_difficulty = st.radio(
    "Select the level you want to practice:",
    ["Easy", "Medium", "Difficult"],
    horizontal=True
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()


# Filter by topic
if selected_topic != "All":

    filtered_df = filtered_df[
        filtered_df[topic_col]
        .astype(str)
        .str.strip()
        .str.lower()
        == selected_topic.strip().lower()
    ]


# Filter by difficulty
if difficulty_col is not None:

    normalized_difficulties = (
        filtered_df[difficulty_col]
        .apply(normalize_difficulty)
    )

    filtered_df = filtered_df[
        normalized_difficulties == selected_difficulty
    ]


# =========================================================
# DISPLAY RESULT
# =========================================================

st.divider()

if filtered_df.empty:

    st.warning(
        f"⚠️ No {selected_difficulty} problem was found "
        f"for the topic '{selected_topic}'."
    )

    st.info(
        "Your dataset needs to contain problems for this "
        "topic and difficulty level."
    )

    st.stop()


# =========================================================
# SELECT A PROBLEM
# =========================================================

# Randomly select one problem
selected_row = filtered_df.sample(
    n=1,
    random_state=random.randint(1, 100000)
).iloc[0]


question = str(selected_row[question_col])


# =========================================================
# PROBLEM
# =========================================================

st.markdown("## 📄 Problem")

st.info(question)


# =========================================================
# HINT
# =========================================================

st.markdown("## 💡 Hint")

if hint_col is not None:

    hint = selected_row[hint_col]

    if pd.notna(hint):
        with st.expander("Click to view hint"):
            st.write(str(hint))
    else:
        st.write("No hint available for this problem.")

else:
    st.write("No hint available.")


# =========================================================
# TOPIC
# =========================================================

st.markdown("## 📌 Topic")

st.write(str(selected_row[topic_col]))


# =========================================================
# TIME COMPLEXITY
# =========================================================

st.markdown("## ⏱️ Time Complexity")

if time_col is not None and pd.notna(selected_row[time_col]):

    st.code(str(selected_row[time_col]))

else:

    st.write("Not available")


# =========================================================
# SPACE COMPLEXITY
# =========================================================

st.markdown("## 💾 Space Complexity")

if space_col is not None and pd.notna(selected_row[space_col]):

    st.code(str(selected_row[space_col]))

else:

    st.write("Not available")


# =========================================================
# SELECTED DIFFICULTY
# =========================================================

st.markdown("## 🎯 Selected Difficulty")

if difficulty_col is not None:

    actual_difficulty = normalize_difficulty(
        selected_row[difficulty_col]
    )

else:

    actual_difficulty = selected_difficulty


if actual_difficulty == "Easy":
    st.success("🟢 Easy")

elif actual_difficulty == "Medium":
    st.warning("🟡 Medium")

else:
    st.error("🔴 Difficult")


# =========================================================
# AI DIFFICULTY PREDICTION
# =========================================================

st.markdown("## 🤖 AI Difficulty Prediction")

prediction = predict_difficulty(question)

if prediction == "Easy":

    st.success(
        f"Predicted Difficulty: {prediction} 🟢"
    )

elif prediction == "Medium":

    st.warning(
        f"Predicted Difficulty: {prediction} 🟡"
    )

elif prediction == "Difficult":

    st.error(
        f"Predicted Difficulty: {prediction} 🔴"
    )

else:

    st.info(
        f"Predicted Difficulty: {prediction}"
    )


# =========================================================
# NEW PROBLEM BUTTON
# =========================================================

st.divider()

if st.button("🔄 Get Another Problem"):

    st.rerun()


# =========================================================
# INFORMATION
# =========================================================

st.divider()

st.caption(
    "AI DSA Tutor | Built with Python, Pandas, "
    "Scikit-learn and Streamlit"
)
