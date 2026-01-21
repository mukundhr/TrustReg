# TrustReg — Domain-Aware Governance for Legal LLM Outputs

TrustReg is an experimental AI governance framework for legal large language model (LLM) outputs.  
It studies **why hallucination-based governance fails**, and demonstrates how **domain-aware harm modeling and policy learning** can improve decision safety while preserving usefulness.

Instead of treating hallucinations as the core problem, TrustReg treats governance as a **decision policy optimization problem** over harm and utility.

---

## Motivation

LLMs are increasingly used in legal contexts such as:

- Human rights analysis  
- Case interpretation  
- Legal document summarization  
- Legal assistance tools  

A confident but incorrect answer in law can cause **real-world harm**.  
However, most governance systems focus only on hallucination detection or factual mismatch.

TrustReg was built to answer a deeper question:

> How should LLM outputs be governed based on their real decision consequences?

---

## Key Insight

> Hallucination detection is not governance.  
> Governance is consequence-aware decision control.

---

## TrustReg Evolution

TrustReg was developed through multiple experimental phases:

| Phase | Governance Strategy | Result |
|------|---------------------|--------|
| v1 | Hallucination detection | Failed to reduce harm |
| v2 | Harm minimization | Collapsed into blocking |
| v3 | Utility-aware governance | Stable but misaligned |
| v3+ | Domain-aware harm modeling | Reduced harm and preserved utility |
| v3+RF/XGB | Policy learning | Exposed harm–utility frontier |

Each failure informed the next design step.

---

## Governance Formulation

TrustReg models governance as a **policy optimization problem**:

GovTarget = Harm − λ · Utility


Where:

- **Harm** penalizes unsafe approvals and unsafe blocks  
- **Utility** rewards correct approvals  
- **λ** controls the safety–usefulness tradeoff  

---

## Domain-Aware Harm Features

TrustReg introduces causal governance features:

- **FactRisk** — Probability that the answer contains incorrect or fabricated factual claims.  
- **InterpretationRisk** — Risk that the legal interpretation of the answer is misleading or incorrect.  
- **RetrievalMismatch** — Degree to which the answer is unsupported by the retrieved source text.  
- **ConfidenceGap** — Difference between answer confidence and retrieval evidence strength.  
- **DomainRisk** — Intrinsic risk level of the domain in which the answer is given.  
- **ActionRisk** — Likelihood that the answer encourages user action with real-world consequences.  
- **AuthorityRisk** — Risk of the answer falsely claiming legal authority or precedent.  
- **SeverityRisk** — Severity of the legal consequences discussed in the answer.  
- **ArticleRisk** — Importance level of the legal article or right involved.  
- **ImpactRisk** — Degree to which the answer can influence user legal decisions.  
  

These features model **legal decision consequences**, not just text similarity.

---

## Policy Learners

Three governance policies are evaluated:

| Model | Purpose |
|------|--------|
| Linear Regression | Baseline governance |
| Random Forest | Safety-oriented policy |
| XGBoost | Utility-oriented policy |

---

## Final Test Results

| Model | Harm ↓ | Utility ↑ |
|------|-------|----------|
| Linear Regression | 740 | 427 |
| Random Forest | 676 | 461 |
| XGBoost | 684 | 533 |

**Interpretation:**

- Random Forest minimizes harm  
- XGBoost maximizes utility  
- Linear Regression provides a balanced baseline  

This exposes a **governance frontier**, not a single best model.

---

## Core Findings

1. Hallucination detection alone does not reduce legal decision harm.  
2. Harm-only optimization collapses into censorship.  
3. Utility-aware governance stabilizes decisions.  
4. Domain-aware harm modeling enables real improvement.  
5. Model choice controls the harm–utility tradeoff.  

---

## TrustReg Dashboard

A Streamlit dashboard visualizes:

- Governance evolution  
- Harm vs Utility tradeoff  
- LR vs RF vs XGB comparison  
- Governance frontier  
- TrustReg Evolution Story 

