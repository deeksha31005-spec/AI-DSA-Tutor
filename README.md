# 🤖 AI DSA Tutor

A beginner-friendly AI/ML based website designed to help students learn and practice Data Structures and Algorithms (DSA).

The project uses Machine Learning to predict the difficulty level of a DSA problem as **Easy, Medium, or Hard** based on features extracted from the problem.

---

## 📌 Project Overview

Learning Data Structures and Algorithms can be difficult for beginners because problems can have different levels of complexity.

The **AI DSA Tutor** provides a simple platform where students can:

- 📚 Select a DSA topic
- 📝 Select a problem
- 👀 Read the problem statement
- 💡 View hints for solving the problem
- ⏱️ View time complexity
- 💾 View space complexity
- 🤖 Get an AI-predicted difficulty level
- 📊 Understand the characteristics of the problem

The main purpose of this project is to demonstrate how **Machine Learning can be applied to an educational problem**.

---

## 🎯 Objectives

The main objectives of this project are:

1. To create a simple AI-powered DSA learning website.
2. To help beginners practice different DSA topics.
3. To use Machine Learning to classify DSA problems by difficulty.
4. To provide hints that help students solve problems independently.
5. To create an easy-to-use interface using Streamlit.
6. To demonstrate a practical application of Python, Pandas and Scikit-learn.

---

## 🧠 Machine Learning Component

The project uses a **Decision Tree Classifier** for predicting the difficulty of DSA problems.

The model predicts one of three classes:

- 🟢 Easy
- 🟡 Medium
- 🔴 Hard

The model is trained using features related to the characteristics of a DSA problem.

### Features Used

The Machine Learning model uses the following features:

- `question_length`
- `hint_count`
- `has_recursion`
- `has_nested_loop`
- `uses_logarithmic`

These features help the model identify patterns between problem characteristics and their difficulty levels.

---

## 🌳 Machine Learning Algorithm

### Decision Tree Classifier

A Decision Tree is a supervised Machine Learning algorithm that can be used for classification.

In this project, the Decision Tree learns patterns from the training dataset and predicts whether a problem is:

**Easy / Medium / Hard**

The model is intentionally kept simple because this is a beginner-level educational project.

Example:

```text
Problem Features
       ↓
Feature Extraction
       ↓
Decision Tree Model
       ↓
Difficulty Prediction
       ↓
Easy / Medium / Hard
