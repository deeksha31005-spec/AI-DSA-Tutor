import streamlit as st
import pandas as pd
import joblib

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI DSA Tutor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 17px;
        color: #667085;
        margin-bottom: 25px;
    }

    /* Metric cards */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.05);
        text-align: center;
    }

    .metric-number {
        font-size: 28px;
        font-weight: 700;
    }

    .metric-label {
        color: #667085;
        font-size: 14px;
    }

    /* Section headings */
    .section-title {
        font-size: 23px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    /* Problem card */
    .problem-card {
        background-color: white;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Complexity cards */
    .complexity-card {
        background-color: white;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.04);
    }

    .complexity-title {
        color: #667085;
        font-size: 14px;
    }

    .complexity-value {
        font-size: 23px;
        font-weight: 700;
    }

    /* Difficulty badges */
    .easy-badge {
        background-color: #dcfce7;
        color: #166534;
        padding: 12px 22px;
        border-radius: 30px;
        font-size: 22px;
        font-weight: 700;
        text-align: center;
    }

    .medium-badge {
        background-color: #fef3c7;
        color: #92400e;
        padding: 12px 22px;
        border-radius: 30px;
        font-size: 22px;
        font-weight: 700;
        text-align: center;
    }

    .hard-badge {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 12px 22px;
        border-radius: 30px;
        font-size: 22px;
        font-weight: 700;
        text-align: center;
    }

    /* AI card */
    .ai-card {
        background-color: white;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
        text-align: center;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #667085;
        font-size: 13px;
        padding-top: 25px;
        padding-bottom: 10px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv("problems.csv")


@st.cache_resource
def load_model():
    return joblib.load("model.pkl")


df = load_data()
model = load_model()


# =========================================================
# DATASET INFORMATION
# =========================================================

total_problems = len(df)
total_topics = df["topic"].nunique()

easy_count = len(df[df["difficulty"] == "Easy"])
medium_count = len(df[df["difficulty"] == "Medium"])
hard_count = len(df[df["difficulty"] == "Hard"])


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🤖 AI DSA Tutor")

    st.markdown(
        "### Your AI-powered DSA learning assistant"
    )

    st.divider()

    st.markdown("### 📚 Learning Options")

    topics = sorted(df["topic"].dropna().unique())

    selected_topic = st.selectbox(
        "Choose Topic",
        topics
    )

    topic_df = df[
        df["topic"] == selected_topic
    ].reset_index(drop=True)

    st.divider()

    st.markdown("### 📊 Dataset")

    st.write(f"**Problems:** {total_problems}")
    st.write(f"**Topics:** {total_topics}")
    st.write(f"**Easy:** {easy_count}")
    st.write(f"**Medium:** {medium_count}")
    st.write(f"**Hard:** {hard_count}")

    st.divider()

    st.caption(
        "Built using Python, Pandas, Scikit-learn and Streamlit."
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🤖 AI DSA Tutor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Practice Data Structures & Algorithms with AI-powered difficulty prediction.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# TOP METRICS
# =========================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-number">{total_problems}</div>
            <div class="metric-label">DSA Problems</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-number">{total_topics}</div>
            <div class="metric-label">Topics</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-number">5</div>
            <div class="metric-label">ML Features</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-number">🌳</div>
            <div class="metric-label">Decision Tree AI</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# =========================================================
# PROBLEM SELECTION
# =========================================================

st.markdown(
    '<div class="section-title">📝 Select a Problem</div>',
    unsafe_allow_html=True
)

problem_names = topic_df["question"].tolist()

selected_problem = st.selectbox(
    "Choose a problem to practice",
    problem_names,
    label_visibility="collapsed"
)

problem = topic_df[
    topic_df["question"] == selected_problem
].iloc[0]


# =========================================================
# PROBLEM CARD
# =========================================================

st.markdown(
    '<div class="section-title">📄 Problem</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="problem-card">
        <h3>{problem["question"]}</h3>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# EXAMPLE
# =========================================================

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 📥 Example Input")

    st.code(
        str(problem["example_input"]),
        language="text"
    )

with col2:

    st.markdown("### 📤 Expected Output")

    st.code(
        str(problem["example_output"]),
        language="text"
    )


# =========================================================
# HINTS
# =========================================================

st.markdown(
    '<div class="section-title">💡 Smart Hints</div>',
    unsafe_allow_html=True
)

hints_found = False

for i in range(1, 4):

    column_name = f"hint{i}"

    if column_name in df.columns:

        hint = problem[column_name]

        if pd.notna(hint) and str(hint).strip() != "":

            hints_found = True

            with st.expander(
                f"💡 Hint {i} — Click to reveal"
            ):

                st.info(str(hint))


if not hints_found:

    st.warning(
        "No hint available for this problem."
    )


# =========================================================
# COMPLEXITY
# =========================================================

st.markdown(
    '<div class="section-title">⚡ Complexity Analysis</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown(
        f"""
        <div class="complexity-card">
            <div class="complexity-title">
                📈 Time Complexity
            </div>
            <div class="complexity-value">
                {problem["time_complexity"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        f"""
        <div class="complexity-card">
            <div class="complexity-title">
                💾 Space Complexity
            </div>
            <div class="complexity-value">
                {problem["space_complexity"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        f"""
        <div class="complexity-card">
            <div class="complexity-title">
                📚 Topic
            </div>
            <div class="complexity-value">
                {problem["topic"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# =========================================================
# ML FEATURE EXTRACTION
# =========================================================

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
        for word in [
            "recursion",
            "recursive",
            "backtracking"
        ]
    )
)


has_nested_loop = int(
    "nested loop" in question.lower()
)


uses_logarithmic = int(
    "log" in str(
        problem["time_complexity"]
    ).lower()
)


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


# =========================================================
# AI PREDICTION
# =========================================================

prediction = model.predict(input_data)[0]


# =========================================================
# AI RESULT
# =========================================================

st.markdown(
    '<div class="section-title">🤖 AI Difficulty Prediction</div>',
    unsafe_allow_html=True
)

ai_col1, ai_col2 = st.columns([2, 1])


with ai_col1:

    if prediction == "Easy":

        badge = """
        <div class="easy-badge">
            🟢 EASY
        </div>
        """

    elif prediction == "Medium":

        badge = """
        <div class="medium-badge">
            🟡 MEDIUM
        </div>
        """

    elif prediction == "Hard":

        badge = """
        <div class="hard-badge">
            🔴 HARD
        </div>
        """

    else:

        badge = f"""
        <div class="medium-badge">
            🤖 {prediction.upper()}
        </div>
        """

    st.markdown(
        f"""
        <div class="ai-card">
            <h3>AI Predicted Difficulty</h3>
            {badge}
        </div>
        """,
        unsafe_allow_html=True
    )


with ai_col2:

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            input_data
        )[0]

        confidence = max(probabilities) * 100

        st.metric(
            "AI Confidence",
            f"{confidence:.1f}%"
        )

        st.progress(
            min(confidence / 100, 1.0)
        )

    else:

        st.info(
            "Confidence is not available."
        )


# =========================================================
# ML FEATURES
# =========================================================

with st.expander("🔍 View ML Features Used by the AI"):

    st.write(
        "The Decision Tree uses five features to predict "
        "the difficulty of the selected DSA problem."
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


# =========================================================
# DATASET DIFFICULTY
# =========================================================

with st.expander("📊 View Dataset Difficulty"):

    st.write(
        "This is the difficulty label stored in the training dataset."
    )

    actual_difficulty = problem["difficulty"]

    if actual_difficulty == "Easy":

        st.success(
            f"Dataset label: {actual_difficulty}"
        )

    elif actual_difficulty == "Medium":

        st.warning(
            f"Dataset label: {actual_difficulty}"
        )

    else:

        st.error(
            f"Dataset label: {actual_difficulty}"
        )

    st.caption(
        "The AI prediction above is generated by the trained "
        "Decision Tree model."
    )


# =========================================================
# ABOUT SECTION
# =========================================================

with st.expander("ℹ️ About AI DSA Tutor"):

    st.write(
        """
        **AI DSA Tutor** is a beginner-friendly AI/ML web application
        designed to help students practice Data Structures and Algorithms.

        The application uses a Decision Tree machine learning model
        to predict whether a DSA problem is Easy, Medium, or Hard.

        The model uses five features:

        • Question length

        • Number of hints

        • Presence of recursion or backtracking

        • Presence of nested loops

        • Logarithmic time complexity

        The application also provides problem-specific hints and
        complexity information directly from the dataset.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🤖 AI DSA Tutor &nbsp;|&nbsp;
        Python • Pandas • Scikit-learn • Decision Tree • Streamlit
        <br>
        Built as a beginner AI/ML project
    </div>
    """,
    unsafe_allow_html=True
)
