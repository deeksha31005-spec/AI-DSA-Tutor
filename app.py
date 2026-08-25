import streamlit as st
import pandas as pd
import joblib
import re

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI DSA Tutor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# DARK PROFESSIONAL THEME
# =========================================================

st.markdown("""
<style>

    /* Main application */
    .stApp {
        background: #0b1020;
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111936 0%, #0b1020 100%);
        border-right: 1px solid #27345c;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    /* Headings */
    h1, h2, h3 {
        color: #ffffff !important;
    }

    p, label {
        color: #cbd5e1 !important;
    }

    /* Hero */
    .hero {
        background: linear-gradient(
            135deg,
            #171f4b 0%,
            #30256d 50%,
            #4c2f91 100%
        );
        padding: 38px;
        border-radius: 24px;
        margin-bottom: 30px;
        border: 1px solid #5b4bb7;
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.20);
        padding: 8px 16px;
        border-radius: 30px;
        font-size: 13px;
        letter-spacing: 1px;
        color: #ddd6fe;
        margin-bottom: 15px;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 10px;
        color: white;
    }

    .hero-subtitle {
        font-size: 18px;
        line-height: 1.7;
        color: #ddd6fe;
        max-width: 850px;
    }

    /* Cards */
    .metric-card {
        background: linear-gradient(145deg, #151d3b, #10162d);
        border: 1px solid #29365e;
        border-radius: 18px;
        padding: 22px;
        min-height: 135px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }

    .metric-icon {
        font-size: 27px;
    }

    .metric-number {
        font-size: 30px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 8px;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 14px;
        margin-top: 4px;
    }

    /* Section */
    .section-title {
        font-size: 25px;
        font-weight: 750;
        color: white;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Problem card */
    .problem-card {
        background: #111936;
        border: 1px solid #29365e;
        border-radius: 20px;
        padding: 28px;
        margin-top: 10px;
        margin-bottom: 20px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.25);
    }

    .problem-title {
        font-size: 25px;
        font-weight: 750;
        color: #ffffff;
        margin-bottom: 15px;
    }

    .problem-text {
        font-size: 17px;
        line-height: 1.8;
        color: #dbeafe;
    }

    /* Info cards */
    .info-card {
        background: #121a34;
        border: 1px solid #29365e;
        border-radius: 16px;
        padding: 20px;
        min-height: 110px;
    }

    .info-label {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .info-value {
        color: #ffffff;
        font-size: 17px;
        font-weight: 650;
    }

    /* Difficulty badges */
    .difficulty-easy {
        display: inline-block;
        padding: 9px 18px;
        border-radius: 30px;
        background: #064e3b;
        color: #6ee7b7;
        border: 1px solid #10b981;
        font-weight: 750;
        font-size: 15px;
    }

    .difficulty-medium {
        display: inline-block;
        padding: 9px 18px;
        border-radius: 30px;
        background: #713f12;
        color: #fde68a;
        border: 1px solid #f59e0b;
        font-weight: 750;
        font-size: 15px;
    }

    .difficulty-hard {
        display: inline-block;
        padding: 9px 18px;
        border-radius: 30px;
        background: #7f1d1d;
        color: #fecaca;
        border: 1px solid #ef4444;
        font-weight: 750;
        font-size: 15px;
    }

    /* AI prediction */
    .ai-box {
        background: linear-gradient(135deg, #19134b, #261b61);
        border: 1px solid #6d5bd0;
        border-radius: 20px;
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 15px 40px rgba(76,47,145,0.25);
    }

    .ai-title {
        font-size: 16px;
        color: #c4b5fd;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    .ai-prediction {
        font-size: 34px;
        font-weight: 850;
        color: white;
        margin-top: 8px;
    }

    /* Hint */
    .hint-box {
        background: linear-gradient(135deg, #132e2a, #102522);
        border: 1px solid #1f8f72;
        border-radius: 18px;
        padding: 22px;
        margin-top: 15px;
        color: #d1fae5;
        line-height: 1.7;
    }

    .hint-number {
        color: #6ee7b7;
        font-weight: 800;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        border: 1px solid #5b4bb7;
        background: linear-gradient(135deg, #4c2f91, #6d4cc7);
        color: white;
        font-weight: 700;
    }

    .stButton > button:hover {
        border-color: #a78bfa;
        color: white;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #111936;
        border-color: #34436f;
        color: white;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background: #111936;
        border: 1px solid #29365e;
        border-radius: 15px;
    }

    /* Divider */
    hr {
        border-color: #29365e;
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


try:
    df = load_data()
    model = load_model()
except Exception as e:
    st.error("❌ Could not load the project files.")
    st.code(str(e))
    st.stop()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def find_column(dataframe, possible_names):
    """
    Find a column without depending on exact capitalization.
    """
    normalized = {
        str(col).strip().lower().replace(" ", "_"): col
        for col in dataframe.columns
    }

    for name in possible_names:
        key = name.strip().lower().replace(" ", "_")
        if key in normalized:
            return normalized[key]

    return None


def count_hints(value):
    """
    Count actual hints stored in the CSV.
    Supports:
    - one hint
    - numbered hints
    - hints separated by |
    - hints separated by new lines
    """
    if pd.isna(value):
        return 0

    text = str(value).strip()

    if not text:
        return 0

    # Try common separators
    if "|" in text:
        parts = [x.strip() for x in text.split("|") if x.strip()]
        return len(parts)

    # Numbered hints such as:
    # Hint 1: ...
    # Hint 2: ...
    numbered = re.findall(
        r"(?:hint\s*\d+\s*:)",
        text,
        flags=re.IGNORECASE
    )

    if numbered:
        return len(numbered)

    # Multiple lines
    lines = [x.strip() for x in text.splitlines() if x.strip()]

    if len(lines) > 1:
        return len(lines)

    return 1


def get_hints(value):
    """
    Return actual hints from CSV in a clean list.
    """
    if pd.isna(value):
        return []

    text = str(value).strip()

    if not text:
        return []

    # Pipe-separated
    if "|" in text:
        return [x.strip() for x in text.split("|") if x.strip()]

    # Numbered hints
    pattern = r"(?:Hint\s*\d+\s*:\s*)"
    parts = re.split(pattern, text, flags=re.IGNORECASE)

    parts = [x.strip() for x in parts if x.strip()]

    if len(parts) > 1:
        return parts

    # Newline separated
    lines = [x.strip() for x in text.splitlines() if x.strip()]

    if len(lines) > 1:
        return lines

    return [text]


def get_text(row, column):
    if column is None:
        return "Not available"

    value = row[column]

    if pd.isna(value):
        return "Not available"

    return str(value)


def calculate_features(row):
    """
    Create the EXACT five features used when model.pkl was trained.
    """

    question_col = find_column(
        df,
        [
            "question",
            "problem",
            "description",
            "problem_statement",
            "question_text"
        ]
    )

    hint_col = find_column(
        df,
        [
            "hints",
            "hint",
            "solution_hint",
            "solution_hints"
        ]
    )

    text = get_text(row, question_col).lower()

    question_length = len(text)

    hint_count = count_hints(row[hint_col]) if hint_col else 0

    has_recursion = int(
        any(word in text for word in [
            "recursion",
            "recursive",
            "recursive function"
        ])
    )

    has_nested_loop = int(
        (
            "nested loop" in text
            or "two loops" in text
            or "nested loops" in text
        )
    )

    uses_logarithmic = int(
        any(word in text for word in [
            "binary search",
            "logarithmic",
            "o(log",
            "o(log n)",
            "divide and conquer"
        ])
    )

    return pd.DataFrame([{
        "question_length": question_length,
        "hint_count": hint_count,
        "has_recursion": has_recursion,
        "has_nested_loop": has_nested_loop,
        "uses_logarithmic": uses_logarithmic
    }])


def difficulty_badge(difficulty):

    difficulty = str(difficulty).strip().lower()

    if difficulty == "easy":
        return '<span class="difficulty-easy">🟢 EASY</span>'

    if difficulty == "medium":
        return '<span class="difficulty-medium">🟡 MEDIUM</span>'

    if difficulty == "hard":
        return '<span class="difficulty-hard">🔴 HARD</span>'

    return f'<span class="difficulty-medium">{difficulty.upper()}</span>'


# =========================================================
# FIND DATASET COLUMNS
# =========================================================

topic_col = find_column(
    df,
    ["topic", "category", "data_structure", "type"]
)

problem_col = find_column(
    df,
    ["problem", "question", "title", "problem_name", "name"]
)

description_col = find_column(
    df,
    ["description", "problem_statement", "question", "problem"]
)

hint_col = find_column(
    df,
    ["hints", "hint", "solution_hint", "solution_hints"]
)

time_col = find_column(
    df,
    ["time_complexity", "time", "time_complexity_big_o"]
)

space_col = find_column(
    df,
    ["space_complexity", "space", "space_complexity_big_o"]
)

difficulty_col = find_column(
    df,
    ["difficulty", "level"]
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center; padding:10px 0 25px 0;">
        <div style="font-size:45px;">🤖</div>
        <div style="font-size:25px; font-weight:800; color:white;">
            AI DSA Tutor
        </div>
        <div style="color:#94a3b8; font-size:13px;">
            Learn • Practice • Improve
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 Select DSA Topic")

    if topic_col:
        topics = sorted(
            df[topic_col].dropna().astype(str).unique().tolist()
        )
    else:
        topics = ["All"]

    selected_topic = st.selectbox(
        "Topic",
        topics,
        label_visibility="collapsed"
    )

    st.divider()

    # Dataset statistics
    st.markdown("### 📊 Dataset Overview")

    st.markdown(
        f"**📚 Problems:** {len(df)}",
        unsafe_allow_html=True
    )

    st.markdown(
        f"**🧩 Topics:** {len(topics)}",
        unsafe_allow_html=True
    )

    if difficulty_col:
        counts = df[difficulty_col].value_counts()

        easy_count = counts.get("Easy", 0)
        medium_count = counts.get("Medium", 0)
        hard_count = counts.get("Hard", 0)

        st.markdown(
            f"🟢 **Easy:** {easy_count}"
        )

        st.markdown(
            f"🟡 **Medium:** {medium_count}"
        )

        st.markdown(
            f"🔴 **Hard:** {hard_count}"
        )

    st.divider()

    st.markdown("### 🤖 ML Model")

    st.markdown("""
    **Decision Tree Classifier**

    🌱 Beginner-friendly ML

    🎯 Predicts:
    Easy • Medium • Hard

    🧠 Features:
    5 problem characteristics
    """)


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

    <div class="hero-badge">
        ✨ AI-POWERED LEARNING PLATFORM
    </div>

    <div class="hero-title">
        🤖 AI DSA Tutor
    </div>

    <div class="hero-subtitle">
        Practice Data Structures & Algorithms with
        intelligent difficulty prediction, helpful hints,
        complexity analysis and AI-powered guidance.
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# DASHBOARD METRICS
# =========================================================

st.markdown(
    '<div class="section-title">📊 Learning Dashboard</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📚</div>
        <div class="metric-number">{len(df)}</div>
        <div class="metric-label">DSA Problems</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">🧩</div>
        <div class="metric-number">{len(topics)}</div>
        <div class="metric-label">Topics Covered</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">🧠</div>
        <div class="metric-number">5</div>
        <div class="metric-label">ML Features</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">🌳</div>
        <div class="metric-number">AI</div>
        <div class="metric-label">Decision Tree Model</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# FILTER PROBLEMS
# =========================================================

if topic_col:
    filtered_df = df[
        df[topic_col].astype(str) == str(selected_topic)
    ].copy()
else:
    filtered_df = df.copy()


if len(filtered_df) == 0:

    st.warning("No problems available for this topic.")

    st.stop()


# =========================================================
# PROBLEM SELECTION
# =========================================================

st.markdown(
    '<div class="section-title">🎯 Choose a Problem</div>',
    unsafe_allow_html=True
)

problem_names = []

for index, row in filtered_df.iterrows():

    if problem_col:
        name = get_text(row, problem_col)
    else:
        name = f"Problem {index + 1}"

    problem_names.append((index, name))


selected_problem_name = st.selectbox(
    "Select a problem",
    [x[1] for x in problem_names]
)

selected_index = next(
    x[0]
    for x in problem_names
    if x[1] == selected_problem_name
)

selected_row = df.loc[selected_index]


# =========================================================
# PROBLEM DISPLAY
# =========================================================

st.markdown(
    '<div class="section-title">📝 Problem</div>',
    unsafe_allow_html=True
)

problem_text = get_text(selected_row, description_col)

st.markdown(f"""
<div class="problem-card">

    <div class="problem-title">
        {selected_problem_name}
    </div>

    <div class="problem-text">
        {problem_text}
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# INFORMATION CARDS
# =========================================================

info1, info2, info3 = st.columns(3)

with info1:

    topic_value = (
        get_text(selected_row, topic_col)
        if topic_col else "Not available"
    )

    st.markdown(f"""
    <div class="info-card">
        <div class="info-label">📌 TOPIC</div>
        <div class="info-value">{topic_value}</div>
    </div>
    """, unsafe_allow_html=True)


with info2:

    time_value = (
        get_text(selected_row, time_col)
        if time_col else "Not available"
    )

    st.markdown(f"""
    <div class="info-card">
        <div class="info-label">⏱️ TIME COMPLEXITY</div>
        <div class="info-value">{time_value}</div>
    </div>
    """, unsafe_allow_html=True)


with info3:

    space_value = (
        get_text(selected_row, space_col)
        if space_col else "Not available"
    )

    st.markdown(f"""
    <div class="info-card">
        <div class="info-label">💾 SPACE COMPLEXITY</div>
        <div class="info-value">{space_value}</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# HINTS
# =========================================================

st.markdown(
    '<div class="section-title">💡 Hints</div>',
    unsafe_allow_html=True
)

if hint_col:

    hints = get_hints(selected_row[hint_col])

    if hints:

        for i, hint in enumerate(hints, start=1):

            with st.expander(
                f"💡 Hint {i} — Click to reveal",
                expanded=False
            ):

                st.markdown(
                    f"""
                    <div class="hint-box">
                        <span class="hint-number">Hint {i}</span>
                        <br><br>
                        {hint}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.info("No hint available for this problem.")

else:

    st.info(
        "No hint column was found in problems.csv."
    )


# =========================================================
# AI DIFFICULTY PREDICTION
# =========================================================

st.markdown(
    '<div class="section-title">🤖 AI Difficulty Prediction</div>',
    unsafe_allow_html=True
)

try:

    features_df = calculate_features(selected_row)

    prediction = model.predict(features_df)[0]

    # Confidence
    confidence = None

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(features_df)[0]

        confidence = max(probabilities) * 100

    st.markdown(
        f"""
        <div class="ai-box">

            <div class="ai-title">
                🌳 DECISION TREE AI PREDICTION
            </div>

            <div class="ai-prediction">
                {difficulty_badge(prediction)}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if confidence is not None:

        st.progress(
            min(int(confidence), 100)
        )

        st.caption(
            f"AI Confidence: {confidence:.1f}%"
        )

    # Show model features for transparency
    with st.expander("🔍 View features used by the AI"):

        st.dataframe(
            features_df,
            use_container_width=True,
            hide_index=True
        )

except Exception as e:

    st.error("⚠️ AI prediction could not be calculated.")

    with st.expander("Technical details"):
        st.code(str(e))


# =========================================================
# ORIGINAL DATASET DIFFICULTY
# =========================================================

if difficulty_col:

    actual_difficulty = get_text(
        selected_row,
        difficulty_col
    )

    st.markdown(
        '<div class="section-title">📌 Dataset Information</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "The following is the difficulty stored in the dataset. "
        "The AI prediction above is generated by the trained Decision Tree."
    )

    st.markdown(
        difficulty_badge(actual_difficulty),
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div style="
    text-align:center;
    padding:25px;
    border-top:1px solid #29365e;
    color:#64748b;
">
    🤖 <b style="color:#a78bfa;">AI DSA Tutor</b>
    &nbsp; • &nbsp;
    Learn DSA with Machine Learning
    <br><br>
    <span style="font-size:12px;">
        Python • Pandas • Scikit-learn • Streamlit • Decision Tree
    </span>
</div>
""", unsafe_allow_html=True)
