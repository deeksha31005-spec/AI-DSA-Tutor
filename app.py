import streamlit as st
import pandas as pd
import joblib

# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="AI DSA Tutor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# LOAD FILES
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("problems.csv")


@st.cache_resource
def load_model():
    return joblib.load("model.pkl")


try:
    df = load_data()
    model = load_model()

except Exception as e:
    st.error("Unable to load the project files.")
    st.code(str(e))
    st.stop()


# ============================================================
# CHECK DATA
# ============================================================

required_columns = [
    "topic",
    "question",
    "difficulty",
    "time_complexity",
    "space_complexity"
]

missing = [
    col for col in required_columns
    if col not in df.columns
]

if missing:
    st.error("Missing columns in problems.csv:")
    st.write(missing)
    st.stop()


# ============================================================
# DATASET INFORMATION
# ============================================================

total_problems = len(df)
total_topics = df["topic"].nunique()

topics = sorted(
    df["topic"].dropna().astype(str).unique()
)

easy_count = (
    df["difficulty"]
    .astype(str)
    .str.strip()
    .eq("Easy")
    .sum()
)

medium_count = (
    df["difficulty"]
    .astype(str)
    .str.strip()
    .eq("Medium")
    .sum()
)

hard_count = (
    df["difficulty"]
    .astype(str)
    .str.strip()
    .eq("Hard")
    .sum()
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 AI DSA Tutor")

    st.caption(
        "Your intelligent companion for "
        "Data Structures & Algorithms."
    )

    st.divider()

    st.subheader("🎯 Practice")

    selected_topic = st.selectbox(
        "Choose a topic",
        topics
    )

    st.divider()

    st.subheader("📊 Dataset")

    st.metric(
        "Total Problems",
        total_problems
    )

    st.metric(
        "Topics",
        total_topics
    )

    st.write("Difficulty distribution")

    st.write(f"🟢 Easy: **{easy_count}**")
    st.write(f"🟡 Medium: **{medium_count}**")
    st.write(f"🔴 Hard: **{hard_count}**")

    st.divider()

    st.subheader("🧠 ML Model")

    st.write("🌳 Decision Tree")
    st.write("🔢 5 Features")
    st.write("🎯 Easy / Medium / Hard")

    st.divider()

    st.caption(
        "Built with Python, Pandas, "
        "Scikit-learn and Streamlit."
    )


# ============================================================
# HEADER
# ============================================================

st.title("🤖 AI DSA Tutor")

st.subheader(
    "Learn • Practice • Get Hints • Understand Difficulty"
)

st.write(
    "Practice Data Structures and Algorithms with "
    "AI-powered difficulty prediction and guided hints."
)

st.divider()


# ============================================================
# DASHBOARD
# ============================================================

st.header("📊 Learning Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📚 Problems",
        total_problems
    )

with col2:
    st.metric(
        "🧩 Topics",
        total_topics
    )

with col3:
    st.metric(
        "🌳 ML Model",
        "Decision Tree"
    )

with col4:
    st.metric(
        "💡 Hint Levels",
        "3"
    )


st.divider()


# ============================================================
# SELECT PROBLEM
# ============================================================

st.header("🎯 Choose Your Challenge")

topic_df = df[
    df["topic"].astype(str) == str(selected_topic)
].reset_index(drop=True)

if topic_df.empty:
    st.warning(
        "No problems are available for this topic."
    )
    st.stop()


problem_names = (
    topic_df["question"]
    .astype(str)
    .tolist()
)

selected_problem = st.selectbox(
    "Select a problem",
    problem_names
)

problem = topic_df[
    topic_df["question"].astype(str)
    == str(selected_problem)
].iloc[0]


# ============================================================
# PROBLEM
# ============================================================

st.header("📝 Problem")

st.info(
    str(problem["question"])
)

st.caption(
    f"Topic: **{problem['topic']}**"
)


# ============================================================
# EXAMPLE
# ============================================================

if (
    "example_input" in df.columns
    or "example_output" in df.columns
):

    st.header("💻 Example")

    ex1, ex2 = st.columns(2)

    with ex1:

        st.subheader("📥 Input")

        if "example_input" in df.columns:

            value = problem["example_input"]

            if pd.notna(value):
                st.code(
                    str(value),
                    language="text"
                )
            else:
                st.info(
                    "No example input available."
                )

        else:
            st.info(
                "No example input available."
            )

    with ex2:

        st.subheader("📤 Output")

        if "example_output" in df.columns:

            value = problem["example_output"]

            if pd.notna(value):
                st.code(
                    str(value),
                    language="text"
                )
            else:
                st.info(
                    "No example output available."
                )

        else:
            st.info(
                "No example output available."
            )


# ============================================================
# HINTS
# ============================================================

st.header("💡 Progressive Hints")

st.write(
    "Try solving the problem yourself first. "
    "Reveal the hints only when you need help."
)

hints_found = False

for i in range(1, 4):

    column_name = f"hint{i}"

    if column_name in df.columns:

        hint = problem[column_name]

        if (
            pd.notna(hint)
            and str(hint).strip() != ""
        ):

            hints_found = True

            with st.expander(
                f"💡 Hint {i} — Click to reveal"
            ):

                st.info(
                    str(hint)
                )


if not hints_found:

    st.warning(
        "No hint available for this problem."
    )


# ============================================================
# COMPLEXITY
# ============================================================

st.header("⚡ Complexity Analysis")

c1, c2, c3 = st.columns(3)

with c1:

    st.subheader("⏱️ Time")

    st.code(
        str(problem["time_complexity"])
    )

with c2:

    st.subheader("💾 Space")

    st.code(
        str(problem["space_complexity"])
    )

with c3:

    st.subheader("🧩 Topic")

    st.info(
        str(problem["topic"])
    )


# ============================================================
# ML FEATURES
# ============================================================

question = str(
    problem["question"]
)

question_lower = question.lower()

question_length = len(question)


# ------------------------------------------------------------
# ACTUAL HINT COUNT
# ------------------------------------------------------------

hint_count = 0

for i in range(1, 4):

    column_name = f"hint{i}"

    if column_name in df.columns:

        hint = problem[column_name]

        if (
            pd.notna(hint)
            and str(hint).strip() != ""
        ):

            hint_count += 1


# ------------------------------------------------------------
# RECURSION
# ------------------------------------------------------------

has_recursion = int(
    any(
        word in question_lower
        for word in [
            "recursion",
            "recursive",
            "backtracking"
        ]
    )
)


# ------------------------------------------------------------
# NESTED LOOP
# ------------------------------------------------------------

has_nested_loop = int(
    "nested loop" in question_lower
    or "nested loops" in question_lower
)


# ------------------------------------------------------------
# LOGARITHMIC
# ------------------------------------------------------------

uses_logarithmic = int(
    "log" in str(
        problem["time_complexity"]
    ).lower()
)


# ============================================================
# PREPARE MODEL INPUT
# ============================================================

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


# ============================================================
# AI PREDICTION
# ============================================================

try:

    prediction = model.predict(
        input_data
    )[0]

except Exception as e:

    st.error(
        "The ML model could not process "
        "this problem."
    )

    st.code(str(e))
    st.stop()


# ============================================================
# AI RESULT
# ============================================================

st.divider()

st.header("🤖 AI Difficulty Prediction")

if prediction == "Easy":

    st.success(
        "🟢 EASY"
    )

elif prediction == "Medium":

    st.warning(
        "🟡 MEDIUM"
    )

elif prediction == "Hard":

    st.error(
        "🔴 HARD"
    )

else:

    st.info(
        f"🤖 {prediction}"
    )


# ============================================================
# CONFIDENCE
# ============================================================

if hasattr(model, "predict_proba"):

    try:

        probabilities = model.predict_proba(
            input_data
        )[0]

        confidence = max(
            probabilities
        ) * 100

        st.metric(
            "AI Confidence",
            f"{confidence:.1f}%"
        )

        st.progress(
            min(confidence / 100, 1.0)
        )

    except Exception:

        st.info(
            "Confidence is not available."
        )


# ============================================================
# HOW AI MADE THE PREDICTION
# ============================================================

with st.expander(
    "🔍 How did the AI make this prediction?"
):

    st.write(
        "The Decision Tree uses these five features:"
    )

    f1, f2, f3, f4, f5 = st.columns(5)

    with f1:
        st.metric(
            "Question Length",
            question_length
        )

    with f2:
        st.metric(
            "Hint Count",
            hint_count
        )

    with f3:
        st.metric(
            "Recursion",
            "Yes" if has_recursion else "No"
        )

    with f4:
        st.metric(
            "Nested Loop",
            "Yes" if has_nested_loop else "No"
        )

    with f5:
        st.metric(
            "Log Complexity",
            "Yes" if uses_logarithmic else "No"
        )


# ============================================================
# ORIGINAL DATASET LABEL
# ============================================================

with st.expander(
    "📊 View dataset difficulty"
):

    actual_difficulty = str(
        problem["difficulty"]
    ).strip()

    st.write(
        "Original difficulty stored in "
        "problems.csv:"
    )

    if actual_difficulty == "Easy":

        st.success(
            f"Dataset Label: {actual_difficulty}"
        )

    elif actual_difficulty == "Medium":

        st.warning(
            f"Dataset Label: {actual_difficulty}"
        )

    elif actual_difficulty == "Hard":

        st.error(
            f"Dataset Label: {actual_difficulty}"
        )

    else:

        st.info(
            f"Dataset Label: {actual_difficulty}"
        )


# ============================================================
# ABOUT PROJECT
# ============================================================

with st.expander(
    "ℹ️ About AI DSA Tutor"
):

    st.write(
        """
        **AI DSA Tutor** is a beginner-friendly AI/ML
        application for practicing Data Structures
        and Algorithms.

        The application uses a Decision Tree Classifier
        to predict the difficulty of DSA problems.

        The model uses:

        • Question length  
        • Number of hints  
        • Recursion / backtracking  
        • Nested loops  
        • Logarithmic complexity  

        Each problem can contain three actual hints
        stored in the dataset.

        The application also provides:

        • Problem statements
        • Example input and output
        • Progressive hints
        • Time complexity
        • Space complexity
        • AI difficulty prediction
        • AI confidence
        • ML feature information
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 AI DSA Tutor • "
    "Python • Pandas • Scikit-learn • Streamlit • "
    "Decision Tree"
)
