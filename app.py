import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="TrustReg Governance Dashboard", layout="wide")

st.title("TrustReg: Legal LLM Governance Framework")

st.markdown("""
TrustReg is a multi-phase governance framework for legal LLM outputs.
This dashboard shows how governance **failed, evolved, and improved**
through domain-aware harm modeling and policy learning.
""")

# ---------------------------
# Load Data
# ---------------------------
base = Path.cwd()
candidate = base / "outputs" / "trustreg_model_comparison.csv"
if not candidate.exists():
    candidate = base.parent / "outputs" / "trustreg_model_comparison.csv"

df = pd.read_csv(candidate)

# ---------------------------
# Helper Functions
# ---------------------------
def decision_harm(predicted, true):
    if predicted == 1 and true == 0: return 5
    if predicted == 0 and true == 1: return 1
    return 0

def decision_utility(predicted, true):
    return 1 if predicted == 1 and true == 1 else 0

def compute_metrics(df, decision_col):
    pred = df[decision_col].apply(lambda d: 1 if d=="APPROVE" else 0)
    harm = df.apply(lambda r: decision_harm(pred.loc[r.name], r["binary_violation"]), axis=1)
    utility = df.apply(lambda r: decision_utility(pred.loc[r.name], r["binary_violation"]), axis=1)
    return harm.sum(), utility.sum()

# ---------------------------
# Sidebar
# ---------------------------
section = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Raw Data",
        "Governance Decisions",
        "Harm vs Utility",
        "Model Comparison",
        "TrustReg Evolution Story"
    ]
)

# ---------------------------
# Overview
# ---------------------------
if section == "Overview":
    st.header("Project Overview")

    st.markdown("""
**Problem:**  
Hallucination detection alone cannot ensure safe legal AI decisions.

**TrustReg Evolution:**

| Phase | Result |
|------|-------|
| v1 Hallucination Governance | Failed |
| v2 Harm Minimization | Collapsed into blocking |
| v3 Domain-Aware Governance | Reduced harm + preserved utility |
| v3 + RF/XGB | Tunable harm–utility frontier |
""")

    lr_harm, lr_util = compute_metrics(df, "TrustReg_v3")

    st.metric("Total Samples", len(df))
    st.metric("TrustReg v3 Harm", int(lr_harm))
    st.metric("TrustReg v3 Utility", int(lr_util))

# ---------------------------
# Raw Data
# ---------------------------
elif section == "Raw Data":
    st.header("Dataset Preview")
    st.dataframe(df.head(100))
    st.write("Columns:", df.columns.tolist())

# ---------------------------
# Governance Decisions
# ---------------------------
elif section == "Governance Decisions":
    st.header("TrustReg v3 Decision Distribution")

    counts = df["TrustReg_v3"].value_counts()

    fig = plt.figure()
    plt.bar(counts.index, counts.values)
    plt.title("TrustReg v3 Decisions")
    plt.xlabel("Decision")
    plt.ylabel("Count")
    st.pyplot(fig)

    st.markdown("TrustReg v3 is selective and stable.")

# ---------------------------
# Harm vs Utility
# ---------------------------
elif section == "Harm vs Utility":
    st.header("TrustReg v3 Governance Tradeoff")

    lr_harm, lr_util = compute_metrics(df, "TrustReg_v3")

    col1, col2 = st.columns(2)

    with col1:
        fig = plt.figure()
        plt.bar(["Harm","Utility"], [lr_harm, lr_util])
        plt.title("TrustReg v3 Outcomes")
        st.pyplot(fig)

    with col2:
        pred = df["TrustReg_v3"].apply(lambda d: 1 if d=="APPROVE" else 0)
        harm_vals = df.apply(lambda r: decision_harm(pred.loc[r.name], r["binary_violation"]), axis=1)
        util_vals = df.apply(lambda r: decision_utility(pred.loc[r.name], r["binary_violation"]), axis=1)

        fig = plt.figure()
        plt.scatter(harm_vals, util_vals)
        plt.title("Harm vs Utility Scatter")
        plt.xlabel("Harm")
        plt.ylabel("Utility")
        st.pyplot(fig)

# ---------------------------
# Model Comparison
# ---------------------------
elif section == "Model Comparison":
    st.header("Governance Model Comparison")

    lr_harm, lr_util = compute_metrics(df, "TrustReg_v3")
    rf_harm, rf_util = compute_metrics(df, "TrustReg_rf")
    xgb_harm, xgb_util = compute_metrics(df, "TrustReg_xgb")

    # ---- Final Table ----
    st.subheader("Final Governance Comparison (Test Set)")

    results_table = pd.DataFrame({
        "Model": ["Linear Regression", "Random Forest", "XGBoost"],
        "Harm": [740, 676, 684],
        "Utility": [427, 461, 533]
    })

    st.table(results_table)

    st.markdown("""
Random Forest minimizes harm.  
XGBoost preserves the most utility.  
Linear Regression provides a balanced baseline.
""")

    # ---- Harm Chart ----
    models = ["Linear", "Random Forest", "XGBoost"]
    harm_values = [lr_harm, rf_harm, xgb_harm]
    utility_values = [lr_util, rf_util, xgb_util]

    col1, col2 = st.columns(2)

    with col1:
        fig = plt.figure()
        plt.bar(models, harm_values)
        plt.title("Decision Harm by Model")
        plt.ylabel("Total Harm")
        st.pyplot(fig)

    with col2:
        fig = plt.figure()
        plt.bar(models, utility_values)
        plt.title("Decision Utility by Model")
        plt.ylabel("Total Utility")
        st.pyplot(fig)

    # ---- Frontier ----
    fig = plt.figure()
    plt.scatter(harm_values, utility_values)
    for i, m in enumerate(models):
        plt.text(harm_values[i]+5, utility_values[i]+5, m)

    plt.title("Governance Harm–Utility Frontier")
    plt.xlabel("Harm")
    plt.ylabel("Utility")
    st.pyplot(fig)

# ---------------------------
# TrustReg Evolution Story
# ---------------------------
elif section == "TrustReg Evolution Story":

    st.markdown("""
### Phase 1 — Hallucination Governance  
Failed to reduce harm.

### Phase 2 — Harm Minimization  
Blocked everything.

### Phase 3 — Utility-Aware Governance  
Stable but misaligned.

### Phase 4 — Domain-Aware Governance  
Reduced harm and preserved utility.

### Phase 5 — Policy Learning  
RF minimized harm.  
XGB maximized utility.

---
""")
