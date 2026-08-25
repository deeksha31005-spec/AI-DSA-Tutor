import streamlit as st
import pandas as pd
import joblib

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI DSA Tutor",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------------
# Load dataset and model
# ---------------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("problems.csv")


@st.cache_resource
def load_model():
    return joblib.load("model.pkl")


df = load_data()
model = load_model()

# ---------------------------------------------------------
# Title
# ---------------------------------------------------------

st.title("🤖 AI DSA Tutor")

st.write(
    "Practice DSA problems and get AI-based difficulty prediction "
    "using a Decision Tree machine learning model."
)

st.divider()

# ---------------------------------------------------------
# Choose topic
# ---------------------------------------------------------

topics = sorted(df["topic"].dropna().unique())

selected_topic = st.selectbox(
    "📚 Choose a DSA Topic",
    topics
)

# ---------------------------------------------------------
# Choose problem
# ---------------------------------------------------------

topic_df = df[df["topic"] == selected_topic].reset_index(drop=True)

problem_names = topic_df["question"].tolist()

selected_problem = st.selectbox(
    "📝 Choose a Problem",
    problem_names
)

# Get selected problem
problem = topic_df[
    topic_df["question"] == selected_problem
].iloc[0]

st.divider()

# ---------------------------------------------------------
# Display problem
# ---------------------------------------------------------

st.subheader("📄 Problem")

st.write(problem["question"])

# ---------------------------------------------------------
# Example
# ---------------------------------------------------------

st.subheader("🔹 Example")

col1, col2 = st.columns(2)

with col1:
    st.write("**Input:**")
    st.code(str(problem["example_input"]))

with col2:
    st.write("**Output:**")
    st.code(str(problem["example_output"]))

# ---------------------------------------------------------
# Hints
# ---------------------------------------------------------

st.subheader("💡 Hints")

hints_found = False

for i in range(1, 4):

    column_name = f"hint{i}"

    if column_name in df.columns:

        hint = problem[column_name]

        if pd.notna(hint) and str(hint).strip() != "":

            hints_found = True

            with st.expander(f"Hint {i}"):
                st.write(str(hint))

if not hints_found:
    st.info("No hint available for this problem.")

# ---------------------------------------------------------
# Complexity
# ---------------------------------------------------------

st.subheader("⚡ Complexity")

col1, col2 = st.columns(2)

with col1:
    st.write("**Time Complexity**")
    st.code(str(problem["time_complexity"]))

with col2:
    st.write("**Space Complexity**")
    st.code(str(problem["space_complexity"]))

# ---------------------------------------------------------
# Prepare ML features
# ---------------------------------------------------------

question = str(problem["question"])

question_length = len(question)

hint_count = 0

for i in range(1, 4):

    column_name = f"hint{i}"

    if column_name in df.columns:

        hint = problem[column_name]

        if pd.notna(hint) and str(hint).strip() != "":
            hint_count += 1


has_recursion = int(
    any(
        word in question.lower()
        for word in ["recursion", "recursive", "backtracking"]
    )
)

has_nested_loop = int(
    "nested loop" in question.lower()
)

uses_logarithmic = int(
    "log" in str(problem["time_complexity"]).lower()
)

# ---------------------------------------------------------
# Create feature dataframe
# ---------------------------------------------------------

features = [
    "question_length",
    "hint_count",
    "has_recursion",
    "has_nested_loop",
    "uses_logarithmic"
]

input_data = pd.DataFrame(
    [[
        question_length,
        hint_count,
        has_recursion,
        has_nested_loop,
        uses_logarithmic
    ]],
    columns=features
)

# ---------------------------------------------------------
# AI Prediction
# ---------------------------------------------------------

prediction = model.predict(input_data)[0]

st.divider()

st.subheader("🤖 AI Predicted Difficulty")

if prediction == "Easy":

    st.success("🟢 Easy")

elif prediction == "Medium":

    st.warning("🟡 Medium")

elif prediction == "Hard":

    st.error("🔴 Hard")

else:

    st.info(str(prediction))

# ---------------------------------------------------------
# Confidence
# ---------------------------------------------------------

if hasattr(model, "predict_proba"):

    probabilities = model.predict_proba(input_data)[0]

    classes = model.classes_

    confidence = max(probabilities) * 100

    st.write(
        f"**AI Confidence:** {confidence:.1f}%"
    )

# ---------------------------------------------------------
# Show actual dataset difficulty
# ---------------------------------------------------------

with st.expander("📊 Dataset Information"):

    st.write(
        "The difficulty stored in the dataset is:"
    )

    st.write(
        f"**{problem['difficulty']}**"
    )

    st.caption(
        "The value above comes from the dataset. "
        "The AI prediction above is generated by the trained Decision Tree model."
    )

# ---------------------------------------------------------
# Feature information
# ---------------------------------------------------------

with st.expander("🔍 ML Features Used"):

    st.write(
        "The Decision Tree uses these five features:"
    )

    st.write(
        f"**Question length:** {question_length}"
    )

    st.write(
        f"**Number of hints:** {hint_count}"
    )

    st.write(
        f"**Has recursion/backtracking:** {has_recursion}"
    )

    st.write(
        f"**Has nested loop:** {has_nested_loop}"
    )

    st.write(
        f"**Uses logarithmic complexity:** {uses_logarithmic}"
    )

st.divider()

st.caption(
    "AI DSA Tutor | Python • Pandas • Scikit-learn • Decision Tree • Streamlit"
)
