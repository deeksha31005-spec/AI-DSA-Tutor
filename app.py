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
# CUSTOM PROFESSIONAL CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
    ========================= */

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(124, 58, 237, 0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at top left,
                rgba(14, 165, 233, 0.08),
                transparent 25%
            ),
            #f7f8fc;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Hide default Streamlit menu/footer */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* =========================
       SIDEBAR
    ========================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #111827 0%,
                #172554 50%,
                #1e1b4b 100%
            );
        border-right: none;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] .stSelectbox label {
        color: #cbd5e1 !important;
        font-weight: 600;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15);
    }

    /* =========================
       HERO
    ========================= */

    .hero {
        padding: 35px 38px;
        border-radius: 24px;
        background:
            linear-gradient(
                135deg,
                #111827 0%,
                #312e81 48%,
                #4f46e5 100%
            );
        box-shadow:
            0 18px 45px rgba(49, 46, 129, 0.22);
        margin-bottom: 25px;
        color: white;
        position: relative;
        overflow: hidden;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        right: -70px;
        top: -70px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 14px;
        border-radius: 30px;
        background: rgba(255,255,255,0.13);
        border: 1px solid rgba(255,255,255,0.18);
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 13px;
    }

    .hero-title {
        font-size: 43px;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        font-size: 17px;
        color: #dbeafe;
        margin-top: 9px;
        max-width: 780px;
        line-height: 1.6;
    }

    /* =========================
       SECTION TITLES
    ========================= */

    .section-title {
        font-size: 24px;
        font-weight: 800;
        color: #111827;
        margin-top: 25px;
        margin-bottom: 13px;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 14px;
        margin-top: -7px;
        margin-bottom: 16px;
    }

    /* =========================
       METRIC CARDS
    ========================= */

    .metric-card {
        background: rgba(255,255,255,0.96);
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 21px;
        min-height: 120px;
        box-shadow: 0 7px 22px rgba(15,23,42,0.06);
        transition: all 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(15,23,42,0.10);
    }

    .metric-icon {
        font-size: 24px;
        margin-bottom: 5px;
    }

    .metric-number {
        font-size: 28px;
        font-weight: 800;
        color: #111827;
    }

    .metric-label {
        font-size: 13px;
        color: #64748b;
        margin-top: 2px;
    }

    /* =========================
       PROBLEM CARD
    ========================= */

    .problem-card {
        background: white;
        border-radius: 22px;
        padding: 30px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 9px 28px rgba(15,23,42,0.07);
        margin-bottom: 20px;
    }

    .problem-label {
        color: #6366f1;
        font-size: 13px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }

    .problem-question {
        font-size: 23px;
        font-weight: 750;
        color: #111827;
        line-height: 1.45;
    }

    /* =========================
       CODE / EXAMPLE CARDS
    ========================= */

    .example-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 6px 20px rgba(15,23,42,0.05);
    }

    .example-title {
        font-size: 15px;
        font-weight: 750;
        color: #334155;
        margin-bottom: 8px;
    }

    /* =========================
       INFO CARDS
    ========================= */

    .info-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(15,23,42,0.05);
    }

    .info-icon {
        font-size: 27px;
    }

    .info-label {
        font-size: 13px;
        color: #64748b;
        margin-top: 6px;
    }

    .info-value {
        font-size: 21px;
        font-weight: 800;
        color: #111827;
        margin-top: 4px;
    }

    /* =========================
       AI RESULT
    ========================= */

    .ai-panel {
        background:
            linear-gradient(
                135deg,
                #ffffff 0%,
                #f5f3ff 100%
            );
        border: 1px solid #ddd6fe;
        border-radius: 22px;
        padding: 27px;
        box-shadow: 0 9px 28px rgba(79,70,229,0.10);
    }

    .ai-title {
        color: #4f46e5;
        font-size: 14px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .ai-description {
        color: #64748b;
        font-size: 13px;
        margin-top: 4px;
        margin-bottom: 18px;
    }

    /* =========================
       DIFFICULTY BADGES
    ========================= */

    .difficulty-badge {
        display: inline-block;
        padding: 11px 25px;
        border-radius: 40px;
        font-size: 22px;
        font-weight: 800;
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

    /* =========================
       HINT BOX
    ========================= */

    .hint-intro {
        background:
            linear-gradient(
                135deg,
                #eef2ff,
                #f5f3ff
            );
        border: 1px solid #ddd6fe;
        border-radius: 17px;
        padding: 17px 20px;
        margin-bottom: 12px;
        color: #4338ca;
        font-size: 14px;
        font-weight: 600;
    }

    /* =========================
       FEATURE BOX
    ========================= */

    .feature-box {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 15px;
        padding: 14px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(15,23,42,0.04);
    }

    .feature-value {
        font-size: 19px;
        font-weight: 800;
        color: #111827;
    }

    .feature-label {
        font-size: 11px;
        color: #64748b;
        margin-top: 3px;
    }

    /* =========================
       FOOTER
    ========================= */

    .footer {
        margin-top: 45px;
        padding-top: 20px;
        border-top: 1px solid #e5e7eb;
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
    }

    /* =========================
       STREAMLIT INPUTS
    ========================= */

    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
    }

    .stButton button {
        border-radius: 12px;
        font-weight: 700;
    }

    /* =========================
       MOBILE
    ========================= */

    @media (max-width: 768px) {

        .hero-title {
            font-size: 31px;
        }

        .hero {
            padding: 25px;
        }

        .problem-card {
            padding: 22px;
        }

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


df = load_data()
model = load_model()


# =========================================================
# DATASET INFORMATION
# =========================================================

total_problems = len(df)

total_topics = (
    df["topic"].dropna().nunique()
    if "topic" in df.columns
    else 0
)

easy_count = (
    int((df["difficulty"] == "Easy").sum())
    if "difficulty" in df.columns
    else 0
)

medium_count = (
    int((df["difficulty"] == "Medium").sum())
    if "difficulty" in df.columns
    else 0
)

hard_count = (
    int((df["difficulty"] == "Hard").sum())
    if "difficulty" in df.columns
    else 0
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:28px;
            font-weight:800;
            margin-bottom:4px;
        ">
            🤖 AI DSA Tutor
        </div>

        <div style="
            color:#cbd5e1;
            font-size:13px;
            line-height:1.5;
            margin-bottom:18px;
        ">
            Your intelligent companion for
            Data Structures & Algorithms.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🎯 Learning Center")

    topics = sorted(
        df["topic"].dropna().unique()
    )

    selected_topic = st.selectbox(
        "Select DSA Topic",
        topics
    )

    topic_df = (
        df[df["topic"] == selected_topic]
        .reset_index(drop=True)
    )

    st.divider()

    st.markdown("### 📊 Dataset Overview")

    st.write(
        f"📚 **Problems:** {total_problems}"
    )

    st.write(
        f"🧩 **Topics:** {total_topics}"
    )

    st.write(
        f"🟢 **Easy:** {easy_count}"
    )

    st.write(
        f"🟡 **Medium:** {medium_count}"
    )

    st.write(
        f"🔴 **Hard:** {hard_count}"
    )

    st.divider()

    st.markdown(
        """
        <div style="
            background:rgba(255,255,255,0.08);
            padding:14px;
            border-radius:12px;
            font-size:12px;
            line-height:1.6;
        ">
        🌳 <b>ML Model</b><br>
        Decision Tree Classifier<br><br>

        🧠 <b>ML Features</b><br>
        5 problem characteristics<br><br>

        ⚡ <b>Prediction</b><br>
        Easy • Medium • Hard
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HERO HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            ✨ AI-POWERED LEARNING PLATFORM
        </div>

        <div class="hero-title">
            🤖 AI DSA Tutor
        </div>

        <div class="hero-subtitle">
            Practice Data Structures & Algorithms with
            intelligent difficulty prediction, guided hints,
            examples and complexity analysis.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD METRICS
# =========================================================

st.markdown(
    '<div class="section-title">📊 Learning Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Explore the DSA problem collection and practice with AI assistance.'
    '</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">📚</div>
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
            <div class="metric-icon">🧩</div>
            <div class="metric-number">{total_topics}</div>
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
            <div class="metric-icon">🌳</div>
            <div class="metric-number">AI</div>
            <div class="metric-label">Decision Tree Model</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PROBLEM SELECTION
# =========================================================

st.markdown(
    '<div class="section-title">🎯 Choose Your Challenge</div>',
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
# PROBLEM DISPLAY
# =========================================================

st.markdown(
    '<div class="section-title">📝 Problem</div>',
    unsafe_allow_html=True
)

safe_question = html.escape(
    str(problem["question"])
)

st.markdown(
    f"""
    <div class="problem-card">

        <div class="problem-label">
            {html.escape(str(problem["topic"]))} • DSA Challenge
        </div>

        <div class="problem-question">
            {safe_question}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# EXAMPLE INPUT / OUTPUT
# =========================================================

st.markdown(
    '<div class="section-title">💻 Example</div>',
    unsafe_allow_html=True
)

example_col1, example_col2 = st.columns(2)

with example_col1:

    st.markdown(
        '<div class="example-title">📥 Example Input</div>',
        unsafe_allow_html=True
    )

    st.code(
        str(problem["example_input"]),
        language="text"
    )


with example_col2:

    st.markdown(
        '<div class="example-title">📤 Expected Output</div>',
        unsafe_allow_html=True
    )

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

st.markdown(
    """
    <div class="hint-intro">
        💡 Stuck? Reveal the hints one at a time and
        try solving the problem yourself before opening the next hint.
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
                f"💡 Hint {i}  •  Click to reveal"
            ):

                st.info(
                    str(hint)
                )


if not hints_found:

    st.warning(
        "No hint available for this problem."
    )


# =========================================================
# COMPLEXITY ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">⚡ Complexity Analysis</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown(
        f"""
        <div class="info-card">

            <div class="info-icon">⏱️</div>

            <div class="info-label">
                TIME COMPLEXITY
            </div>

            <div class="info-value">
                {html.escape(str(problem["time_complexity"]))}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        f"""
        <div class="info-card">

            <div class="info-icon">💾</div>

            <div class="info-label">
                SPACE COMPLEXITY
            </div>

            <div class="info-value">
                {html.escape(str(problem["space_complexity"]))}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        f"""
        <div class="info-card">

            <div class="info-icon">📚</div>

            <div class="info-label">
                TOPIC
            </div>

            <div class="info-value">
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

# Count actual hints
hint_count = 0

for i in range(1, 4):

    column_name = f"hint{i}"

    if column_name in df.columns:

        hint = problem[column_name]

        if pd.notna(hint) and str(hint).strip() != "":
            hint_count += 1


# Recursion / backtracking feature
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


# Nested loop feature
has_nested_loop = int(
    "nested loop" in question.lower()
)


# Logarithmic feature
uses_logarithmic = int(
    "log" in str(
        problem["time_complexity"]
    ).lower()
)


# =========================================================
# PREPARE MODEL INPUT
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

prediction = model.predict(input_data)[0]


# =========================================================
# AI CONFIDENCE
# =========================================================

confidence = None

if hasattr(model, "predict_proba"):

    probabilities = model.predict_proba(
        input_data
    )[0]

    confidence = float(
        max(probabilities) * 100
    )


# =========================================================
# AI RESULT
# =========================================================

st.markdown(
    '<div class="section-title">🤖 AI Difficulty Analysis</div>',
    unsafe_allow_html=True
)

ai_col1, ai_col2 = st.columns([1.5, 1])

with ai_col1:

    if prediction == "Easy":
        badge_class = "easy"
        icon = "🟢"

    elif prediction == "Medium":
        badge_class = "medium"
        icon = "🟡"

    else:
        badge_class = "hard"
        icon = "🔴"

    st.markdown(
        f"""
        <div class="ai-panel">

            <div class="ai-title">
                AI PREDICTED DIFFICULTY
            </div>

            <div class="ai-description">
                Decision Tree analysis based on
                five problem characteristics.
            </div>

            <div class="difficulty-badge {badge_class}">
                {icon} {html.escape(str(prediction))}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with ai_col2:

    if confidence is not None:

        st.markdown(
            """
            <div style="
                background:white;
                border:1px solid #e5e7eb;
                border-radius:20px;
                padding:25px;
                box-shadow:0 7px 22px rgba(15,23,42,0.06);
            ">
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "### 🎯 AI Confidence"
        )

        st.markdown(
            f"""
            <div style="
                font-size:30px;
                font-weight:800;
                color:#4f46e5;
                margin-bottom:5px;
            ">
                {confidence:.1f}%
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            min(confidence / 100, 1.0)
        )

        st.caption(
            "Confidence calculated from the Decision Tree model."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    else:

        st.info(
            "AI confidence is not available for this model."
        )


# =========================================================
# ML FEATURES
# =========================================================

with st.expander("🧠 See How the AI Made This Prediction"):

    st.markdown(
        """
        The Decision Tree model analyzes five numerical
        features extracted from the selected DSA problem.
        """
    )

    f1, f2, f3, f4, f5 = st.columns(5)

    with f1:

        st.markdown(
            f"""
            <div class="feature-box">
                <div class="feature-value">
                    {question_length}
                </div>
                <div class="feature-label">
                    Question Length
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f2:

        st.markdown(
            f"""
            <div class="feature-box">
                <div class="feature-value">
                    {hint_count}
                </div>
                <div class="feature-label">
                    Hint Count
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f3:

        st.markdown(
            f"""
            <div class="feature-box">
                <div class="feature-value">
                    {"Yes" if has_recursion else "No"}
                </div>
                <div class="feature-label">
                    Recursion
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f4:

        st.markdown(
            f"""
            <div class="feature-box">
                <div class="feature-value">
                    {"Yes" if has_nested_loop else "No"}
                </div>
                <div class="feature-label">
                    Nested Loop
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f5:

        st.markdown(
            f"""
            <div class="feature-box">
                <div class="feature-value">
                    {"Yes" if uses_logarithmic else "No"}
                </div>
                <div class="feature-label">
                    Log Complexity
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# DATASET REFERENCE
# =========================================================

with st.expander("📊 View Dataset Reference"):

    actual_difficulty = problem["difficulty"]

    st.write(
        "This is the original difficulty label stored "
        "in the training dataset."
    )

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
        "The AI prediction above is generated independently "
        "by the trained Decision Tree model."
    )


# =========================================================
# ABOUT PROJECT
# =========================================================

with st.expander("ℹ️ About AI DSA Tutor"):

    about_col1, about_col2 = st.columns(2)

    with about_col1:

        st.markdown(
            """
            ### 🎓 What is AI DSA Tutor?

            AI DSA Tutor is an educational AI/ML application
            designed to help students practice Data Structures
            and Algorithms.

            It provides:

            - 📚 DSA practice problems
            - 💡 Problem-specific hints
            - ⚡ Time complexity
            - 💾 Space complexity
            - 🤖 ML-based difficulty prediction
            - 🎯 Prediction confidence
            """
        )

    with about_col2:

        st.markdown(
            """
            ### 🧠 Machine Learning

            The project uses a **Decision Tree Classifier**.

            The model analyzes:

            1. Question length
            2. Number of hints
            3. Recursion presence
            4. Nested-loop presence
            5. Logarithmic complexity

            The model predicts:

            🟢 Easy

            🟡 Medium

            🔴 Hard
            """
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        🤖 <b>AI DSA Tutor</b>
        &nbsp; • &nbsp;
        Python
        &nbsp; • &nbsp;
        Pandas
        &nbsp; • &nbsp;
        Scikit-learn
        &nbsp; • &nbsp;
        Decision Tree
        &nbsp; • &nbsp;
        Streamlit

        <br><br>

        Built as an AI/ML educational project

    </div>
    """,
    unsafe_allow_html=True
)
