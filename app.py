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
except Exception as e:
    st.error("Could not load problems.csv")
    st.write(e)
    st.stop()


try:
    model = load_model()
except Exception as e:
    st.error("Could not load model.pkl")
    st.write(e)
    st.stop()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def find_column(dataframe, possible_names):

    for name in possible_names:
        if name in dataframe.columns:
            return name

    lower_columns = {
        str(col).lower().strip(): col
        for col in dataframe.columns
    }

    for name in possible_names:
        if name.lower().strip() in lower_columns:
            return lower_columns[name.lower().strip()]

    return None


def normalize_difficulty(value):

    value = str(value).strip().lower()

    if value in ["easy", "beginner", "basic"]:
        return "Easy"

    if value in ["medium", "moderate", "intermediate"]:
        return "Medium"

    if value in ["difficult", "difficulty", "hard", "advanced"]:
        return "Difficult"

    return str(value).title()


def get_question_features(question):

    question = str(question).lower()

    question_length = len(question.split())

    hint_count = question.count("hint")

    has_recursion = int(
        "recursion" in question
        or "recursive" in question
    )

    has_nested_loop = int(
        "nested loop" in question
        or "nested loops" in question
        or "two loops" in question
    )

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

    try:

        features = get_question_features(question)

        prediction = model.predict(features)[0]

        return normalize_difficulty(prediction)

    except Exception:

        return "Not available"


def detect_concepts(question):

    text = question.lower()

    concepts = []

    keywords = {
        "Arrays": ["array", "arrays"],
        "Strings": ["string", "strings"],
        "Linked List": ["linked list", "linkedlist"],
        "Stack": ["stack"],
        "Queue": ["queue"],
        "Tree": ["tree", "binary tree"],
        "Graph": ["graph", "bfs", "dfs"],
        "Recursion": ["recursion", "recursive"],
        "Binary Search": ["binary search"],
        "Sorting": ["sort", "sorting"],
        "Hashing": ["hash", "hashmap", "dictionary"],
        "Dynamic Programming": ["dynamic programming", "dp"],
        "Greedy": ["greedy"],
    }

    for concept, words in keywords.items():

        for word in words:

            if word in text:
                concepts.append(concept)
                break

    if not concepts:
        concepts.append("General DSA")

    return concepts


def get_generic_hint(question, concepts):

    text = question.lower()

    if "binary search" in text:
        return (
            "Think about how you can repeatedly divide the search space "
            "into two halves instead of checking every element."
        )

    if "recursion" in text or "recursive" in text:
        return (
            "Identify the base case first. Then determine how the problem "
            "becomes smaller in each recursive call."
        )

    if "linked list" in text:
        return (
            "Think about how the current node connects to the next node. "
            "Try solving it by carefully moving through the links."
        )

    if "tree" in text:
        return (
            "Think about the traversal required. Consider whether "
            "DFS or BFS is more appropriate."
        )

    if "graph" in text:
        return (
            "Consider representing the graph using an adjacency list. "
            "Then decide whether BFS or DFS fits the problem."
        )

    if "array" in text:
        return (
            "Try walking through the array once and keep track of the "
            "information you need instead of repeatedly scanning it."
        )

    if "string" in text:
        return (
            "Look for patterns in the characters. Ask yourself whether "
            "two pointers, hashing, or a frequency table could help."
        )

    return (
        "Break the problem into smaller steps. Identify the input, output, "
        "main operation, and the most efficient data structure you can use."
    )


def get_strategy(question, concepts):

    if "Binary Search" in concepts:

        return """
1. Make sure the data is sorted.
2. Find the middle element.
3. Compare it with the target.
4. Eliminate half of the search space.
5. Repeat until the answer is found.

Typical complexity: O(log n)
"""

    if "Recursion" in concepts:

        return """
1. Identify the base case.
2. Define the recursive case.
3. Reduce the problem size.
4. Make the recursive call.
5. Combine the returned result if necessary.
"""

    if "Graph" in concepts:

        return """
1. Represent the graph.
2. Choose BFS or DFS.
3. Keep track of visited nodes.
4. Traverse the required nodes.
5. Stop when the required condition is satisfied.
"""

    if "Tree" in concepts:

        return """
1. Identify the root.
2. Decide which traversal is required.
3. Visit the nodes systematically.
4. Process each node according to the problem.
"""

    if "Array" in concepts:

        return """
1. Understand the required output.
2. Traverse the array.
3. Maintain the required information.
4. Update the result when necessary.
5. Check edge cases.
"""

    return """
1. Understand the input and output.
2. Break the problem into smaller steps.
3. Choose a suitable data structure.
4. Develop the basic algorithm.
5. Analyze time and space complexity.
"""


def recommend_problem(topic, difficulty):

    available = df.copy()

    if topic != "All":

        available = available[
            available[topic_col]
            .astype(str)
            .str.strip()
            .str.lower()
            == topic.strip().lower()
        ]

    if difficulty_col is not None:

        normalized = available[difficulty_col].apply(
            normalize_difficulty
        )

        available = available[
            normalized == difficulty
        ]

    if available.empty:
        return None

    return available.sample(
        n=1,
        random_state=random.randint(1, 100000)
    ).iloc[0]


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
# VALIDATE DATA
# =========================================================

if topic_col is None or question_col is None:

    st.error("Required columns were not found in problems.csv")

    st.write(
        "Available columns:",
        list(df.columns)
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.title("🤖 AI DSA Tutor")

st.subheader(
    "Your AI-powered assistant for learning Data Structures and Algorithms"
)

st.write(
    "Practice DSA problems, get ML-based difficulty predictions, "
    "receive hints, understand concepts and improve your problem-solving skills."
)


st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📚 DSA Topics")

    topics = sorted(
        df[topic_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_topic = st.selectbox(
        "Choose Topic",
        ["All"] + topics
    )

    st.divider()

    st.info(
        """
        **How this tutor works**

        1. Choose a DSA topic.
        2. Practice a problem.
        3. Ask the ML model about difficulty.
        4. Get hints and strategy.
        5. Try another problem.
        """
    )


# =========================================================
# MAIN TABS
# =========================================================

practice_tab, ai_tab = st.tabs(
    ["🎯 Practice Problems", "🤖 AI Question Analyzer"]
)


# =========================================================
# PRACTICE TAB
# =========================================================

with practice_tab:

    st.header("🎯 DSA Practice")

    selected_difficulty = st.radio(
        "Choose difficulty",
        ["Easy", "Medium", "Difficult"],
        horizontal=True
    )

    if "practice_problem" not in st.session_state:

        st.session_state.practice_problem = None


    if st.button(
        "🎲 Generate Practice Problem",
        use_container_width=True
    ):

        problem = recommend_problem(
            selected_topic,
            selected_difficulty
        )

        st.session_state.practice_problem = problem


    problem = st.session_state.practice_problem


    if problem is None:

        st.info(
            "Choose a topic and difficulty, then click "
            "**Generate Practice Problem**."
        )

    else:

        question = str(problem[question_col])

        st.success("Problem generated successfully!")

        st.markdown("## 📄 Problem")

        st.info(question)


        # ---------------------------------------------
        # Problem information
        # ---------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown("### 📌 Topic")

            st.write(
                str(problem[topic_col])
            )

        with col2:

            st.markdown("### 🎯 Difficulty")

            if difficulty_col is not None:

                actual = normalize_difficulty(
                    problem[difficulty_col]
                )

            else:

                actual = selected_difficulty

            st.write(actual)

        with col3:

            st.markdown("### 🤖 ML Prediction")

            prediction = predict_difficulty(question)

            st.write(prediction)


        # ---------------------------------------------
        # Hint
        # ---------------------------------------------

        st.markdown("## 💡 Tutor Hint")

        if hint_col is not None:

            hint = problem[hint_col]

            if pd.notna(hint):

                with st.expander(
                    "Click to reveal the dataset hint"
                ):

                    st.write(str(hint))

            else:

                concepts = detect_concepts(question)

                with st.expander(
                    "Click to reveal AI tutor hint"
                ):

                    st.write(
                        get_generic_hint(
                            question,
                            concepts
                        )
                    )

        else:

            concepts = detect_concepts(question)

            with st.expander(
                "Click to reveal AI tutor hint"
            ):

                st.write(
                    get_generic_hint(
                        question,
                        concepts
                    )
                )


        # ---------------------------------------------
        # Strategy
        # ---------------------------------------------

        with st.expander(
            "🧠 Show Problem-Solving Strategy"
        ):

            concepts = detect_concepts(question)

            st.write(
                "Detected concepts:",
                ", ".join(concepts)
            )

            st.code(
                get_strategy(
                    question,
                    concepts
                )
            )


        # ---------------------------------------------
        # Complexity
        # ---------------------------------------------

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("### ⏱️ Time Complexity")

            if (
                time_col is not None
                and pd.notna(problem[time_col])
            ):

                st.code(
                    str(problem[time_col])
                )

            else:

                st.write(
                    "Complexity not available in dataset."
                )


        with c2:

            st.markdown("### 💾 Space Complexity")

            if (
                space_col is not None
                and pd.notna(problem[space_col])
            ):

                st.code(
                    str(problem[space_col])
                )

            else:

                st.write(
                    "Complexity not available in dataset."
                )


        st.divider()

        if st.button(
            "🔄 Generate Another Problem",
            use_container_width=True
        ):

            st.session_state.practice_problem = None

            st.rerun()


# =========================================================
# AI QUESTION ANALYZER
# =========================================================

with ai_tab:

    st.header("🤖 Ask the AI DSA Tutor")

    st.write(
        "Enter your own DSA question or problem statement. "
        "The ML model will analyze it and predict its difficulty."
    )


    user_question = st.text_area(
        "Enter your DSA problem:",
        placeholder=(
            "Example: Find an element in a sorted array "
            "using binary search."
        ),
        height=160
    )


    if st.button(
        "🔍 Analyze My Question",
        use_container_width=True
    ):

        if not user_question.strip():

            st.warning(
                "Please enter a DSA question first."
            )

        else:

            # -----------------------------------------
            # ML prediction
            # -----------------------------------------

            prediction = predict_difficulty(
                user_question
            )

            st.markdown(
                "## 🤖 AI Difficulty Prediction"
            )

            if prediction == "Easy":

                st.success(
                    "🟢 Predicted Difficulty: Easy"
                )

            elif prediction == "Medium":

                st.warning(
                    "🟡 Predicted Difficulty: Medium"
                )

            elif prediction == "Difficult":

                st.error(
                    "🔴 Predicted Difficulty: Difficult"
                )

            else:

                st.info(
                    f"Predicted Difficulty: {prediction}"
                )


            # -----------------------------------------
            # Concept detection
            # -----------------------------------------

            concepts = detect_concepts(
                user_question
            )

            st.markdown(
                "## 🧠 Detected DSA Concepts"
            )

            st.write(
                ", ".join(concepts)
            )


            # -----------------------------------------
            # AI hint
            # -----------------------------------------

            st.markdown(
                "## 💡 Tutor Hint"
            )

            st.info(
                get_generic_hint(
                    user_question,
                    concepts
                )
            )


            # -----------------------------------------
            # Strategy
            # -----------------------------------------

            st.markdown(
                "## 📝 Suggested Approach"
            )

            st.code(
                get_strategy(
                    user_question,
                    concepts
                )
            )


            # -----------------------------------------
            # Recommended problem
            # -----------------------------------------

            st.markdown(
                "## 🎯 Recommended Practice Problem"
            )

            recommendation = recommend_problem(
                "All",
                prediction
            )

            if recommendation is not None:

                st.success(
                    str(
                        recommendation[question_col]
                    )
                )

                if topic_col is not None:

                    st.write(
                        "Topic:",
                        str(
                            recommendation[topic_col]
                        )
                    )

            else:

                st.info(
                    "No matching practice problem "
                    "was found in the dataset."
                )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI DSA Tutor | Python • Pandas • Scikit-learn • "
    "Decision Tree • Streamlit"
)
