import streamlit as st
import pandas as pd
import joblib
import html

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

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(99,102,241,0.10), transparent 28%),
            radial-gradient(circle at 90% 10%, rgba(14,165,233,0.10), transparent 25%),
            #f6f8fc;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #111827 0%,
                #172554 55%,
                #1e1b4b 100%
            );
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] .stSelectbox label {
        color: #cbd5e1 !important;
        font-weight: 600;
    }

    .sidebar-brand {
        padding: 8px 0 20px 0;
    }

    .sidebar-logo {
        font-size: 38px;
        margin-bottom: 5px;
    }

    .sidebar-title {
        font-size: 23px;
        font-weight: 800;
        color: white;
    }

    .sidebar-subtitle {
        color: #cbd5e1;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 5px;
    }

    .sidebar-card {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 16px;
        margin-top: 16px;
    }

    .sidebar-card-title {
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .sidebar-stat {
        display: flex;
        justify-content: space-between;
        padding: 7px 0;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        font-size: 13px;
    }

    .sidebar-stat:last-child {
        border-bottom: none;
    }

    .sidebar-footer {
        color: #94a3b8;
        font-size: 11px;
        text-align: center;
        margin-top: 30px;
        line-height: 1.5;
    }

    /* =====================================================
       HERO
       ===================================================== */

    .hero {
        position: relative;
        overflow: hidden;
        border-radius: 28px;
        padding: 42px 45px;
        margin-bottom: 28px;

        background:
            radial-gradient(
                circle at 85% 20%,
                rgba(129,140,248,0.45),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #111827 0%,
                #312e81 48%,
                #4f46e5 100%
            );

        box-shadow: 0 20px 50px rgba(30,41,59,0.20);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.18);
        color: #e0e7ff;
        border-radius: 999px;
        padding: 7px 14px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 14px;
    }

    .hero-title {
        color: white;
        font-size: 42px;
        font-weight: 850;
        margin: 0;
        line-height: 1.1;
    }

    .hero-description {
        color: #dbeafe;
        font-size: 16px;
        line-height: 1.7;
        max-width: 760px;
        margin-top: 14px;
    }

    .hero-mini {
        color: #c7d2fe;
        font-size: 13px;
        margin-top: 20px;
    }

    /* =====================================================
       SECTION TITLES
       ===================================================== */

    .section-heading {
        font-size: 24px;
        font-weight: 800;
        color: #111827;
        margin-top: 28px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 18px;
    }

    /* =====================================================
       METRIC CARDS
       ===================================================== */

    .metric-card {
        background: rgba(255,255,255,0.92);
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 22px;
        min-height: 125px;
        box-shadow: 0 8px 25px rgba(15,23,42,0.06);
    }

    .metric-icon {
        font-size: 25px;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 850;
        color: #111827;
        line-height: 1;
    }

    .metric-label {
        color: #64748b;
        font-size: 13px;
        margin-top: 8px;
        font-weight: 600;
    }

    /* =====================================================
       SELECTOR CARD
       ===================================================== */

    .selector-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 20px 22px 10px 22px;
        box-shadow: 0 8px 25px rgba(15,23,42,0.05);
    }

    /* =====================================================
       PROBLEM CARD
       ===================================================== */

    .problem-card {
        background: white;
        border-radius: 22px;
        border: 1px solid #e2e8f0;
        padding: 30px;
        margin-top: 10px;
        box-shadow: 0 12px 30px rgba(15,23,42,0.07);
    }

    .problem-label {
        color: #6366f1;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }

    .problem-title {
        color: #111827;
        font-size: 25px;
        font-weight: 800;
        line-height: 1.4;
        margin: 0;
    }

    /* =====================================================
       INFO CARDS
       ===================================================== */

    .info-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 20px;
        height: 100%;
        box-shadow: 0 7px 20px rgba(15,23,42,0.05);
    }

    .info-title {
        color: #475569;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    /* =====================================================
       COMPLEXITY
       ===================================================== */

    .complexity-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 7px 20px rgba(15,23,42,0.05);
    }

    .complexity-icon {
        font-size: 24px;
    }

    .complexity-label {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
        margin-top: 7px;
    }

    .complexity-value {
        color: #111827;
        font-size: 22px;
        font-weight: 850;
        margin-top: 4px;
    }

    /* =====================================================
       AI RESULT
       ===================================================== */

    .ai-panel {
        border-radius: 24px;
        padding: 28px;
        margin-top: 8px;
        background:
            radial-gradient(
                circle at 90% 10%,
                rgba(99,102,241,0.12),
                transparent 35%
            ),
            white;
        border: 1px solid #dbeafe;
        box-shadow: 0 12px 35px rgba(79,70,229,0.10);
    }

    .ai-panel-title {
        font-size: 13px;
        color: #6366f1;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .ai-panel-subtitle {
        color: #64748b;
        font-size: 13px;
        margin-top: 5px;
    }

    .difficulty-badge {
        display: inline-block;
        padding: 12px 24px;
        border-radius: 999px;
        font-size: 22px;
        font-weight: 850;
        margin-top: 17px;
    }

    .easy {
        background: #dcfce7;
        color: #166534;
        border: 1px solid #bbf7d0;
    }

    .medium {
        background: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
    }

    .hard {
        background: #fee2e2;
        color: #991b1b;
        border: 1px solid #fecaca;
    }

    .confidence-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
    }

    .confidence-number {
        font-size: 30px;
        font-weight: 850;
        color: #4f46e5;
    }

    .confidence-label {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
        margin-top: 5px;
    }

    /* =====================================================
       HINTS
       ===================================================== */

    .hint-intro {
        background: linear-gradient(135deg, #eef2ff, #f0f9ff);
        border: 1px solid #c7d2fe;
        border-radius: 18px;
        padding: 16px 18px;
        color: #3730a3;
        font-size: 14px;
        margin-bottom: 12px;
    }

    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        padding: 35px 0 10px 0;
        line-height: 1.7;
    }

    /* =====================================================
       STREAMLIT ELEMENT IMPROVEMENTS
       ===================================================== */

    div[data-testid="stExpander"] {
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        overflow: hidden;
        background: white;
    }

    div[data-testid="stMetric"] {
        background: white;
        border-radius: 15px;
        padding: 10px;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LOAD DATA
# =========================================================

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
    st.error("⚠️ Unable to load the project files.")
    st.code(str(e))
    st.stop()


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "topic",
    "question",
    "difficulty",
    "time_complexity",
    "space_complexity"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "The following required columns are missing from problems.csv:"
    )
    st.write(missing_columns)
    st.stop()


# =========================================================
# DATASET INFORMATION
# =========================================================

total_problems = len(df)
total_topics = df["topic"].nunique()

easy_count = int(
    (df["difficulty"].astype(str).str.strip() == "Easy").sum()
)

medium_count = int(
    (df["difficulty"].astype(str).str.strip() == "Medium").sum()
)

hard_count = int(
    (df["difficulty"].astype(str).str.strip() == "Hard").sum()
)

topics = sorted(
    df["topic"].dropna().astype(str).unique().tolist()
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">🤖</div>
            <div class="sidebar-title">AI DSA Tutor</div>
            <div class="sidebar-subtitle">
                Your intelligent companion for learning
                Data Structures & Algorithms.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🎯 Choose Your Topic")

    selected_topic = st.selectbox(
        "Select DSA Topic",
        topics,
        label_visibility="collapsed"
    )

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-card-title">
                📊 Dataset Overview
            </div>

            <div class="sidebar-stat">
                <span>📚 Problems</span>
                <b>%d</b>
            </div>

            <div class="sidebar-stat">
                <span>🧩 Topics</span>
                <b>%d</b>
            </div>

            <div class="sidebar-stat">
                <span>🟢 Easy</span>
                <b>%d</b>
            </div>

            <div class="sidebar-stat">
                <span>🟡 Medium</span>
                <b>%d</b>
            </div>

            <div class="sidebar-stat">
                <span>🔴 Hard</span>
                <b>%d</b>
            </div>
        </div>
        """
        % (
            total_problems,
            total_topics,
            easy_count,
            medium_count,
            hard_count
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-card">

            <div class="sidebar-card-title">
                🧠 AI Model
            </div>

            <div style="font-size:13px;">
                🌳 Decision Tree Classifier
            </div>

            <br>

            <div style="font-size:13px;">
                🔢 5 ML Features
            </div>

            <br>

            <div style="font-size:13px;">
                🎯 Easy • Medium • Hard
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-footer">
            Built with<br>
            Python • Pandas • Scikit-learn • Streamlit<br><br>
            AI DSA Tutor © 2026
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FILTER PROBLEMS BY TOPIC
# =========================================================

topic_df = (
    df[df["topic"].astype(str) == str(selected_topic)]
    .reset_index(drop=True)
)

if topic_df.empty:
    st.warning("No problems found for this topic.")
    st.stop()


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            ✨ AI-POWERED LEARNING PLATFORM
        </div>

        <h1 class="hero-title">
            AI DSA Tutor
        </h1>

        <div class="hero-description">
            Practice Data Structures & Algorithms with
            intelligent difficulty prediction, progressive
            hints, examples and complexity analysis.
        </div>

        <div class="hero-mini">
            🌳 Powered by a Machine Learning Decision Tree
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD METRICS
# =========================================================

st.markdown(
    """
    <div class="section-heading">
        📊 Learning Dashboard
    </div>

    <div class="section-description">
        Explore the problem collection and practice with AI assistance.
    </div>
    """,
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">📚</div>
            <div class="metric-value">{total_problems}</div>
            <div class="metric-label">DSA Problems</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">🧩</div>
            <div class="metric-value">{total_topics}</div>
            <div class="metric-label">Topics Covered</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-icon">🧠</div>
            <div class="metric-value">5</div>
            <div class="metric-label">ML Features</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-icon">🌳</div>
            <div class="metric-value">AI</div>
            <div class="metric-label">Decision Tree Model</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PROBLEM SELECTION
# =========================================================

st.markdown(
    """
    <div class="section-heading">
        🎯 Choose Your Challenge
    </div>

    <div class="section-description">
        Select a problem and let the AI analyze its difficulty.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="selector-card">',
    unsafe_allow_html=True
)

problem_names = topic_df["question"].astype(str).tolist()

selected_problem = st.selectbox(
    "Choose a DSA problem",
    problem_names,
    label_visibility="visible"
)

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# GET SELECTED PROBLEM
# =========================================================

problem = topic_df[
    topic_df["question"].astype(str) == str(selected_problem)
].iloc[0]


# =========================================================
# PROBLEM
# =========================================================

safe_question = html.escape(str(problem["question"]))

st.markdown(
    """
    <div class="section-heading">
        📝 Problem Statement
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="problem-card">

        <div class="problem-label">
            {html.escape(str(problem["topic"]))} • DSA PROBLEM
        </div>

        <div class="problem-title">
            {safe_question}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# EXAMPLE INPUT / OUTPUT
# =========================================================

if "example_input" in df.columns or "example_output" in df.columns:

    st.markdown(
        """
        <div class="section-heading">
            💻 Example
        </div>
        """,
        unsafe_allow_html=True
    )

    ex1, ex2 = st.columns(2)

    with ex1:
        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="info-title">📥 EXAMPLE INPUT</div>',
            unsafe_allow_html=True
        )

        if "example_input" in df.columns:
            st.code(
                str(problem["example_input"]),
                language="text"
            )
        else:
            st.info("No example input available.")

        st.markdown("</div>", unsafe_allow_html=True)

    with ex2:
        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="info-title">📤 EXPECTED OUTPUT</div>',
            unsafe_allow_html=True
        )

        if "example_output" in df.columns:
            st.code(
                str(problem["example_output"]),
                language="text"
            )
        else:
            st.info("No example output available.")

        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# HINTS
# =========================================================

st.markdown(
    """
    <div class="section-heading">
        💡 Progressive Hints
    </div>

    <div class="section-description">
        Try solving the problem yourself first. Reveal hints one at a time.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hint-intro">
        💡 <b>Tip:</b> Start with Hint 1. Only reveal the next hint
        if you need additional guidance.
    </div>
    """,
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
                f"💡 Hint {i} — Click to reveal",
                expanded=False
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
    """
    <div class="section-heading">
        ⚡ Complexity Analysis
    </div>

    <div class="section-description">
        Understand the computational cost of the selected problem.
    </div>
    """,
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f"""
        <div class="complexity-card">
            <div class="complexity-icon">⏱️</div>
            <div class="complexity-label">
                TIME COMPLEXITY
            </div>
            <div class="complexity-value">
                {html.escape(str(problem["time_complexity"]))}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="complexity-card">
            <div class="complexity-icon">💾</div>
            <div class="complexity-label">
                SPACE COMPLEXITY
            </div>
            <div class="complexity-value">
                {html.escape(str(problem["space_complexity"]))}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="complexity-card">
            <div class="complexity-icon">🧩</div>
            <div class="complexity-label">
                TOPIC
            </div>
            <div class="complexity-value">
                {html.escape(str(problem["topic"]))}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# ML FEATURE EXTRACTION
# =========================================================

question = str(problem["question"])

question_length = len(question)


# ---------------------------------------------------------
# IMPORTANT:
# Count the ACTUAL available hints
# ---------------------------------------------------------

hint_count = 0

for i in range(1, 4):

    column_name = f"hint{i}"

    if column_name in df.columns:

        hint = problem[column_name]

        if pd.notna(hint) and str(hint).strip() != "":
            hint_count += 1


# ---------------------------------------------------------
# Recursion / Backtracking
# ---------------------------------------------------------

question_lower = question.lower()

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


# ---------------------------------------------------------
# Nested Loop
# ---------------------------------------------------------

has_nested_loop = int(
    "nested loop" in question_lower
    or "nested loops" in question_lower
)


# ---------------------------------------------------------
# Logarithmic Complexity
# ---------------------------------------------------------

uses_logarithmic = int(
    "log" in str(
        problem["time_complexity"]
    ).lower()
)


# =========================================================
# MODEL INPUT
# =========================================================

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

try:

    prediction = model.predict(input_data)[0]

except Exception as e:

    st.error(
        "The trained model could not process this problem."
    )

    st.code(str(e))
    st.stop()


# =========================================================
# AI RESULT
# =========================================================

st.markdown(
    """
    <div class="section-heading">
        🤖 AI Difficulty Analysis
    </div>

    <div class="section-description">
        The trained Decision Tree analyzes the problem using
        five machine-learning features.
    </div>
    """,
    unsafe_allow_html=True
)


if prediction == "Easy":

    badge_class = "easy"
    badge_text = "🟢 EASY"

elif prediction == "Medium":

    badge_class = "medium"
    badge_text = "🟡 MEDIUM"

elif prediction == "Hard":

    badge_class = "hard"
    badge_text = "🔴 HARD"

else:

    badge_class = "medium"
    badge_text = f"🤖 {str(prediction).upper()}"


ai_col1, ai_col2 = st.columns([2.2, 1])

with ai_col1:

    st.markdown(
        f"""
        <div class="ai-panel">

            <div class="ai-panel-title">
                AI PREDICTED DIFFICULTY
            </div>

            <div class="ai-panel-subtitle">
                Prediction generated by the trained Decision Tree model
            </div>

            <div class="difficulty-badge {badge_class}">
                {badge_text}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with ai_col2:

    if hasattr(model, "predict_proba"):

        try:

            probabilities = model.predict_proba(
                input_data
            )[0]

            confidence = float(
                max(probabilities) * 100
            )

            st.markdown(
                f"""
                <div class="confidence-card">

                    <div class="confidence-number">
                        {confidence:.1f}%
                    </div>

                    <div class="confidence-label">
                        AI CONFIDENCE
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                min(confidence / 100, 1.0)
            )

        except Exception:

            st.info(
                "Confidence is not available."
            )

    else:

        st.info(
            "Confidence is not available for this model."
        )


# =========================================================
# ML FEATURES
# =========================================================

with st.expander(
    "🔍 See how the AI made this prediction"
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


# =========================================================
# DATASET LABEL
# =========================================================

with st.expander(
    "📊 View the original dataset difficulty"
):

    actual_difficulty = str(
        problem["difficulty"]
    ).strip()

    st.write(
        "This is the original difficulty label stored "
        "in problems.csv. It is separate from the AI prediction."
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


# =========================================================
# ABOUT
# =========================================================

with st.expander(
    "ℹ️ About AI DSA Tutor"
):

    st.markdown(
        """
        ### 🤖 What is AI DSA Tutor?

        AI DSA Tutor is a beginner-friendly AI/ML application
        designed to help students practice Data Structures
        and Algorithms.

        ### 🧠 Machine Learning

        The application uses a **Decision Tree Classifier**
        to predict whether a problem is:

        - 🟢 Easy
        - 🟡 Medium
        - 🔴 Hard

        ### 🔢 Features used by the model

        1. Question length
        2. Number of available hints
        3. Recursion / backtracking
        4. Nested loops
        5. Logarithmic time complexity

        ### 💡 Learning Support

        Each problem can contain up to three real hints
        stored directly in the dataset.

        The application also displays:

        - Example input
        - Expected output
        - Time complexity
        - Space complexity
        - AI predicted difficulty
        - AI confidence
        - ML feature values
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        🤖 <b>AI DSA Tutor</b><br>

        Learn • Practice • Analyze • Improve<br>

        Python • Pandas • Scikit-learn • Decision Tree • Streamlit

    </div>
    """,
    unsafe_allow_html=True
)
