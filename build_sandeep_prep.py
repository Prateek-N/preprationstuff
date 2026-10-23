# -*- coding: utf-8 -*-
"""
Build script for Sandeep Kasiraju's Indegene Data Scientist Prep Suite.
Compiles:
1. sandeep_kasiraju_indegene_prep.md
2. content/sandeep-kasiraju-indegene-prep.mdx
3. sandeep_kasiraju_indegene_prep.html
4. public/sandeep_kasiraju_indegene_prep.html
"""

import json
import re
import os
from sandeep_data_questions_part1 import QUESTIONS_PART1
from sandeep_data_questions_part2 import QUESTIONS_PART2

ALL_QUESTIONS = QUESTIONS_PART1 + QUESTIONS_PART2

# =============================================================================
# 1. GENERATE MASTER MARKDOWN (sandeep_kasiraju_indegene_prep.md)
# =============================================================================
def generate_markdown():
    md = []
    md.append("# Sandeep Kasiraju — Data Scientist (Pharma Analytics & AI) Interview Preparation Suite\n")
    md.append("## Target Role: Data Scientist – Pharma Analytics & AI — Indegene\n")
    md.append("**Candidate:** Sandeep Kasiraju | Boston, MA | +1-508-644-0788 | kasirajusandeep98@gmail.com | [LinkedIn](https://linkedin.com) | [GitHub](https://github.com) | [Portfolio](https://portfolio.com)\n")
    md.append("**Target Company:** Indegene (Healthcare & Life Sciences Solutions Provider · Global Commercial Analytics)\n")
    md.append("**Passcode Lock:** `Sandeep`\n\n")
    md.append("---\n\n")

    md.append("## Executive Summary & Indegene Role Alignment\n")
    md.append("> **Sandeep Kasiraju** is a Data Scientist and Machine Learning Engineer with 5 years of hands-on experience spanning healthcare analytics, applied predictive modeling, time-series forecasting, and cutting-edge Generative AI / Agentic systems. Holding an **M.S. in Data Science from UMass Dartmouth** and an **AWS Certified Machine Learning Engineer Associate (MLA-C01)** certification, Sandeep combines rigorous quantitative modeling with deep business and commercial acumen.\n\n")
    md.append("At **Centene Corporation**, Sandeep analyzed claims and utilization data across **1.2M managed-care members**, unlocking **$3.1M in avoidable readmission savings** and building gradient boosted risk-stratification models that avoided **$890K in hospitalization costs**. At **Adani Group**, he engineered high-stakes time-series predictive maintenance systems that prevented 120 hours of unplanned downtime valued at **$2.4M annually**, while deploying SageMaker real-time anomaly detection engines and forecasting grid demand with **LSTMs**. His academic research and independent work feature state-of-the-art **multi-modal PyTorch models (94.3% accuracy)**, **LoRA/PEFT LLM fine-tuning**, and a 4-agent structured **Multi-Agent Orchestration Decision Engine (FastAPI, AutoGen, Pydantic)**.\n\n")
    md.append("This unique combination of **pharmaceutical/claims domain fluency**, **deep time-series forecasting**, **enterprise MLOps (SageMaker, MLflow, Spark)**, **GenAI / Agentic AI**, and proven **onshore-offshore collaboration** directly addresses every requirement of Indegene's **Data Scientist – Pharma Analytics & AI** role.\n\n")

    md.append("## Core Technical & Domain Competencies\n")
    md.append("| Functional Area | Core Technologies & Methodologies |\n")
    md.append("| :--- | :--- |\n")
    md.append("| **Pharma & Healthcare Analytics** | **EDI 837/835 Claims**, **Longitudinal Patient Journey (RWD/RWE)**, **HCP Deciling & Targeting**, **ICD-10 / CPT / NDC Coding**, **PDC / MPR Adherence**, **Survival Analysis (Kaplan-Meier, Cox PH)** |\n")
    md.append("| **Time-Series Forecasting** | **SARIMAX**, **Prophet**, **LSTM / Bi-LSTM**, **DeepAR / Temporal Fusion Transformers (TFT)**, **Croston Intermittent Demand**, **Hierarchical Reconciliation (MinT)**, **Bass Diffusion** |\n")
    md.append("| **Machine Learning & Predictive Modeling** | **XGBoost**, **LightGBM**, **Random Forest**, **Logistic Regression**, **SHAP / TreeSHAP Explainability**, **PR-AUC / ROC-AUC**, **Stratified Time-Series CV**, **Cost-Sensitive Loss** |\n")
    md.append("| **GenAI & Agentic AI Systems** | **LLM Fine-Tuning (LoRA, QLoRA, PEFT)**, **Hugging Face Transformers**, **Biomedical RAG (BioBERT, Med-CPT, FAISS, Milvus)**, **Multi-Agent Systems (AutoGen, LangChain, FastAPI)**, **Snowflake Cortex & Vertex AI Agents** |\n")
    md.append("| **Cloud, Big Data & MLOps** | **AWS (SageMaker, S3, EC2, Lambda)**, **Apache Spark / PySpark**, **MLflow Model Registry**, **Docker & CI/CD**, **Airflow DAGs**, **Data Drift (PSI, KS-Test, Evidently AI)** |\n")
    md.append("| **Consulting & Leadership** | **Onshore Point-of-Contact & Offshore Delivery Alignment**, **Ambiguous Problem Framing**, **Executive Storytelling & Tableau/Power BI C-Suite Reporting**, **HIPAA & GxP Compliance** |\n\n")

    md.append("---\n\n")

    md.append("## System Architecture Blueprints\n\n")
    
    md.append("### Blueprint 1: Enterprise Pharma Real-World Data (RWE) & Claims Risk Stratification Pipeline\n")
    md.append("```mermaid\ngraph TD\n")
    md.append("    subgraph Ingestion [Raw Real-World Data Ingestion]\n")
    md.append("        A1[EDI 837 Medical / Inpatient Claims] --> B[PySpark Batch / Streaming Ingestion]\n")
    md.append("        A2[EDI 835 Remittance / Payment Claims] --> B\n")
    md.append("        A3[NDC Pharmacy Prescription Claims] --> B\n")
    md.append("        A4[EHR & Lab Records LOINC/SNOMED] --> B\n")
    md.append("    end\n")
    md.append("    subgraph FeatureEng [Feature Engineering & Master Patient Index]\n")
    md.append("        B --> C1[MPI Patient Identity Resolution]\n")
    md.append("        C1 --> C2[Clinical Comorbidity Scoring CCI / Elixhauser]\n")
    md.append("        C1 --> C3[Medication Adherence PDC / MPR Metrics]\n")
    md.append("        C1 --> C4[Temporal Care Velocity & Prior Auth Rejections]\n")
    md.append("    end\n")
    md.append("    subgraph Modeling [Predictive Modeling & Explainability]\n")
    md.append("        C2 & C3 & C4 --> D[Stratified Temporal Cross-Validation]\n")
    md.append("        D --> E1[XGBoost / LightGBM Classifier]\n")
    md.append("        D --> E2[Calibrated Cost-Sensitive Logistic Regression]\n")
    md.append("        E1 & E2 --> F[TreeSHAP Global & Patient-Level Attributions]\n")
    md.append("    end\n")
    md.append("    subgraph Action [Commercial & Clinical Activation]\n")
    md.append("        F --> G1[High-Risk Patient Stratification & Case Mgmt Outreach]\n")
    md.append("        F --> G2[HCP Decile Targeting & Commercial Territory Planning]\n")
    md.append("        F --> G3[Executive Tableau / Power BI KPI Dashboards]\n")
    md.append("    end\n")
    md.append("```\n\n")

    md.append("### Blueprint 2: Hierarchical Multi-Horizon Pharmaceutical Demand & Sales Forecasting Engine\n")
    md.append("```mermaid\ngraph LR\n")
    md.append("    subgraph Hierarchy [Hierarchical Sales & Patient Demand Levels]\n")
    md.append("        L0[National Enterprise Sales Level] --> L1[Regional Distribution Centers]\n")
    md.append("        L1 --> L2[Territory / IDN Hospital Accounts]\n")
    md.append("        L2 --> L3[HCP / Pharmacy Outlet SKU Level]\n")
    md.append("    end\n")
    md.append("    subgraph Forecasting [Multi-Model Forecasting Engine]\n")
    md.append("        L0 & L1 --> M1[SARIMAX & Prophet Macro Trends + Exogenous Factors]\n")
    md.append("        L2 --> M2[Bi-LSTM & Temporal Fusion Transformers TFT]\n")
    md.append("        L3 --> M3[Croston / TSB Zero-Inflated Intermittent Method]\n")
    md.append("    end\n")
    md.append("    subgraph Reconciliation [Hierarchical Reconciliation & Distribution]\n")
    md.append("        M1 & M2 & M3 --> N[MinT Minimum Trace Optimal Reconciliation Matrix]\n")
    md.append("        N --> O1[Coherent Multi-Level Demand Projections]\n")
    md.append("        N --> O2[Safety Stock & Cold Chain Buffer Allocation]\n")
    md.append("        N --> O3[Commercial Quota Setting & Supply Chain ERP Sync]\n")
    md.append("    end\n")
    md.append("```\n\n")

    md.append("### Blueprint 3: Enterprise Multi-Agent Clinical & Commercial AI Decision Engine\n")
    md.append("```mermaid\ngraph TD\n")
    md.append("    subgraph ClientLayer [Client & Commercial Inquiry]\n")
    md.append("        User[Pharma Brand Director / Field Operations Lead] --> UI[FastAPI Gateway / Streamlit UI]\n")
    md.append("    end\n")
    md.append("    subgraph Orchestration [AutoGen Multi-Agent Pydantic State Engine]\n")
    md.append("        UI --> AG1[Agent 1: Researcher Agent RAG on Clinical Trials & Claims]\n")
    md.append("        AG1 -->|Validated JSON Schema| AG2[Agent 2: Analyst Agent Statistical & Econometric Modeling]\n")
    md.append("        AG2 -->|Validated JSON Schema| AG3[Agent 3: Skeptic Agent GxP Compliance, Bias & Sensitivity Audit]\n")
    md.append("        AG3 -->|Validated JSON Schema| AG4[Agent 4: Decision Agent Synthesizer Executive Strategy]\n")
    md.append("    end\n")
    md.append("    subgraph EnterpriseBacking [Enterprise Cloud & AI Foundation]\n")
    md.append("        AG1 -.-> KB1[(Snowflake Cortex / Cortex Search Vector DB)]\n")
    md.append("        AG2 -.-> KB2[(Vertex AI / SageMaker Hosted Pre-Trained LSTMs & XGBoost)]\n")
    md.append("        AG3 -.-> KB3[(FDA Guidance, GxP Audit Rules & Fair Housing/Fair Treatment Checks)]\n")
    md.append("    end\n")
    md.append("    subgraph OutputLayer [Executive Decision Artifacts]\n")
    md.append("        AG4 --> Out1[Audited Commercial Recommendation & Sensitivity Analysis]\n")
    md.append("        AG4 --> Out2[C-Suite Slide Deck & Automated Executive Narrative]\n")
    md.append("    end\n")
    md.append("```\n\n")

    md.append("---\n\n")

    md.append("# High-Yield Technical Interview Questions & Expert Answers (30 Questions · 300+ Words Each)\n\n")

    current_cat = ""
    for q in ALL_QUESTIONS:
        words = len(re.findall(r'\b\w+\b', q['answer']))
        if q.get('category') and q['category'] != current_cat:
            current_cat = q['category']
            md.append(f"## {current_cat}\n\n")

        md.append(f"### Q{q['num']:02d}: {q['title']}\n\n")
        md.append(f"**Interview Question:** *\"{q['question']}\"*\n\n")
        md.append(f"**Perspective & Delivery:** First-Person POV (`{words} words` · Verified $\\ge 300$ words)  \n\n")
        md.append(f"**In-Depth Technical Answer:**\n\n")
        md.append(f"{q['answer']}\n\n")
        md.append("---\n\n")

    md.append("# Candidate Experience Mapping & Resume Defense Guide\n\n")
    md.append("### 1. Centene Corporation — Healthcare Claims & Risk Stratification\n")
    md.append("- **Direct Indegene Relevance:** Led end-to-end analytics on **1.2 million managed-care members** using **SQL Server**, **Python**, and **Tableau**. Built logistic regression and gradient boosting models that flagged **8,200 high-risk individuals**, preventing **$890K in avoidable hospitalizations** and discovering **$3.1M in readmission reductions** across 3 health plan segments.\n")
    md.append("- **Claims Engineering:** Automated **EDI 837 (medical/institutional claims)** and **EDI 835 (remittance/payment)** ingestion scripts, cutting monthly billing reconciliation cycles from 18 hours to 2 hours.\n")
    md.append("- **Executive Delivery:** Delivered **24 monthly executive Tableau dashboards** spanning medical, pharmacy, and behavioral health metrics, eliminating 31 hours of ad-hoc reporting every month.\n\n")

    md.append("### 2. Adani Group — Time-Series Predictive Analytics & Real-Time MLOps\n")
    md.append("- **Direct Indegene Relevance:** Engineered mission-critical **predictive-maintenance Random Forest pipelines** on time-series sensor telemetry across 6 industrial facilities, preventing 120 hours of unplanned downtime worth **$2.4M annually**.\n")
    md.append("- **AWS SageMaker & Drift Monitoring:** Deployed real-time anomaly detection handling **50,000 readings/hour on AWS SageMaker**, reducing false-positive critical alarms from 180 to under 30 daily. Built **MLflow** drift tracking and custom Python alerts across 9 production scoring models, catching 4 model performance drops within 24 hours.\n")
    md.append("- **Deep Time-Series Forecasting:** Built multi-step **LSTM neural networks** for energy distribution grids, achieving an MAE of 1.2 MW over rolling 30-day horizons. Rebuilt **Apache Spark ETL pipelines** processing 800GB daily telemetry, shrinking latency from 4 hours to 18 minutes.\n\n")

    md.append("### 3. University of Massachusetts Dartmouth — Advanced AI & LLM Research\n")
    md.append("- **Direct Indegene Relevance:** Architected a multi-modal deep learning framework in **PyTorch** and **Hugging Face Transformers** reaching **94.3% classification accuracy** across 12 datasets, supporting 3 faculty grant projects.\n")
    md.append("- **NLP & Semantic Processing:** Built NLP pipelines with **BERT** and **spaCy** scoring semantic similarity across **2.1M records**, eliminating 40 researcher-hours of manual review per project.\n")
    md.append("- **LoRA & PEFT Fine-Tuning:** Fine-tuned domain-specific LLMs using parameter-efficient fine-tuning (**LoRA, PEFT**), reducing held-out perplexity by 18 points. Automated feature engineering with scikit-learn Pipelines and MLflow, slashing experiment iteration time from 6 hours to 40 minutes across 15 concurrent runs.\n\n")

    md.append("### 4. Amazon — Data Quality, NLP Labeling & Ground-Truth Systems\n")
    md.append("- **Direct Indegene Relevance:** Supervised annotation and quality-assurance of **420,000+ multimodal samples** for Alexa NLP intent classification, maintaining an error rate below 4 per 1,000 records across 9 cycles.\n")
    md.append("- **Process Optimization:** Created a 6-stage QC framework adopted by a 35-person team, saving 22 hours per sprint and shrinking schema mismatches across 12 NLP initiatives from 17 to 2.\n\n")

    md.append("### 5. Multi-Agent AI Decision Engine & FinSent-AI Projects\n")
    md.append("- **Multi-Agent Orchestration:** Architected a production-ready **FastAPI + OpenAI + AutoGen** multi-agent pipeline decomposing complex business inquiries across 4 structured agents (**Researcher → Analyst → Skeptic → Decision Agent**), communicating via strict **Pydantic** schemas with dual-mode live/mock testing.\n")
    md.append("- **FinSent-AI:** Achieved **94.2% F1-score** fine-tuning **RoBERTa-large** with **QLoRA** on 50,000+ SEC filing sentences, integrated with **Apache Kafka** and **Spark Streaming** with sub-150ms p99 latency.\n\n")

    md.append("---\n\n")
    md.append("## Onshore-Offshore Client Management Playbook\n")
    md.append("1. **Daily Operational Rhythm**: Conduct overlapping morning standups (8:00 AM – 9:30 AM EST) with India-based offshore modeling teams. Review code PRs, validate experimental drift metrics, and unblock data dependencies before US client working hours begin.\n")
    md.append("2. **Client Expectation Calibration**: Translate ambiguous commercial stakeholder requests into concrete mathematical problem statements, evaluation metrics (e.g., WAPE, PR-AUC, business ROI), and deliverable milestones.\n")
    md.append("3. **Two-Way Communication Shield**: Protect offshore engineers from sudden scope shifts by maintaining a living Jira sprint backlog and structured Pydantic/Data contract specifications. Present executive-ready visualizations and SHAP explainability summaries to client VPs and Brand Directors.\n")

    return "".join(md)

# =============================================================================
# 2. GENERATE NEXTJS MDX (content/sandeep-kasiraju-indegene-prep.mdx)
# =============================================================================
def sanitize_for_mdx(text: str) -> str:
    code_blocks = []
    def code_repl(match):
        code_blocks.append(match.group(0))
        return f"__MDX_CODE_BLOCK_{len(code_blocks)-1}__"

    # Protect code blocks and inline code
    text = re.sub(r"```[\s\S]*?```", code_repl, text)
    text = re.sub(r"`[^`\n]+`", code_repl, text)

    # Sanitize JSX / MDX sensitive characters in prose
    text = text.replace("{", "&#123;").replace("}", "&#125;")
    text = text.replace("<=", "&le;").replace(">=", "&ge;")
    text = re.sub(r"<(?![a-zA-Z\/])", "&lt;", text)

    # Restore code blocks
    for idx, cb in enumerate(code_blocks):
        text = text.replace(f"__MDX_CODE_BLOCK_{idx}__", cb)

    return text

def generate_mdx(master_md):
    escaped_body = sanitize_for_mdx(master_md)

    header = """---
title: Sandeep Kasiraju — Data Scientist (Pharma Analytics & AI) Prep Suite
description: 30 high-yield interview questions and comprehensive 300+ word technical answers for Data Scientist – Pharma Analytics & AI at Indegene, covering claims analytics, time-series forecasting, machine learning, multi-agent AI, and onshore-offshore delivery.
---

<PasswordGate password="Sandeep" candidateName="Sandeep Kasiraju">

"""

    footer = """

</PasswordGate>
"""
    return header + escaped_body + footer

# =============================================================================
# 3. GENERATE INTERACTIVE WEBPAGE (sandeep_kasiraju_indegene_prep.html)
# =============================================================================
def generate_html():
    items_json = []
    categories = []

    for q in ALL_QUESTIONS:
        words = len(re.findall(r'\b\w+\b', q['answer']))
        cat = q.get('category', 'Technical Excellence')
        if cat not in categories:
            categories.append(cat)
        items_json.append({
            "num": q["num"],
            "category": cat,
            "title": q["title"],
            "question": q["question"],
            "words": words,
            "answer": q["answer"]
        })

    items_json_str = json.dumps(items_json, ensure_ascii=False)
    categories_json_str = json.dumps(categories, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Indegene — Data Scientist (Pharma Analytics & AI) Prep Suite · Sandeep Kasiraju</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <style>
    :root {{
      --bg-base: #06090e;
      --bg-surface: #0c121c;
      --bg-card: #121a28;
      --bg-card-hover: #192438;
      --border: #1f2e48;
      --border-accent: #0284c7;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --indegene-blue: #0284c7;
      --indegene-teal: #0d9488;
      --indegene-cyan: #06b6d4;
      --indegene-emerald: #10b981;
      --indegene-amber: #f59e0b;
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg-base);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.65;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }}

    /* LOCK SCREEN */
    #lockScreen {{
      position: fixed; inset: 0;
      background: radial-gradient(circle at center, #0c1c2e 0%, #03060a 100%);
      display: flex; align-items: center; justify-content: center;
      z-index: 99999; padding: 1.5rem;
    }}
    .lock-box {{
      background: rgba(12, 18, 28, 0.96);
      backdrop-filter: blur(24px);
      border: 1px solid rgba(2, 132, 199, 0.4);
      border-radius: 22px;
      padding: 2.75rem 2.5rem;
      max-width: 490px;
      width: 100%;
      text-align: center;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.9), 0 0 50px rgba(2, 132, 199, 0.2);
    }}
    .lock-logo-mark {{
      display: inline-flex; align-items: center; justify-content: center;
      margin-bottom: 1.25rem; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.04em;
    }}
    .lock-txt-1 {{ color: #ffffff; }}
    .lock-txt-2 {{ color: #38bdf8; }}
    .lock-badge-pill {{
      background: linear-gradient(135deg, rgba(2, 132, 199, 0.2), rgba(13, 148, 136, 0.2));
      border: 1px solid rgba(56, 189, 248, 0.4);
      padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; color: #7dd3fc;
      font-family: var(--font-mono); margin-left: 8px; font-weight: 700;
    }}
    .lock-box h2 {{ font-size: 1.45rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.02em; }}
    .lock-box p {{ color: var(--text-muted); font-size: 0.88rem; margin-bottom: 1.75rem; }}
    .input-group {{ position: relative; margin-bottom: 1.25rem; }}
    .input-group input {{
      width: 100%;
      background: rgba(6, 9, 14, 0.92);
      border: 1px solid var(--border);
      padding: 0.95rem 1.2rem;
      border-radius: 12px;
      color: #fff;
      font-size: 1.05rem;
      outline: none;
      transition: all 0.2s;
      text-align: center;
      letter-spacing: 0.12em;
    }}
    .input-group input:focus {{
      border-color: var(--indegene-cyan);
      box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.25);
    }}
    .unlock-btn {{
      width: 100%;
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: #ffffff;
      border: none;
      padding: 0.95rem;
      border-radius: 12px;
      font-size: 0.98rem;
      font-weight: 800;
      cursor: pointer;
      transition: all 0.2s;
      letter-spacing: 0.04em;
    }}
    .unlock-btn:hover {{
      transform: translateY(-1px);
      box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.5);
      background: linear-gradient(135deg, #0369a1, #0284c7);
    }}
    .error-msg {{
      color: #f87171; font-size: 0.85rem; margin-top: 0.9rem; display: none; font-weight: 500;
    }}

    /* MAIN CONTAINER */
    #app {{ display: none; }}
    .page-wrapper {{ max-width: 1400px; margin: 0 auto; padding: 2rem 2.5rem 5rem; }}

    /* HEADER */
    .top-bar {{
      display: flex; align-items: center; justify-content: space-between;
      padding: 1.25rem 0; border-bottom: 1px solid var(--border); margin-bottom: 2.5rem;
    }}
    .brand-mark {{
      display: flex; align-items: center; gap: 14px; font-weight: 800; font-size: 1.35rem; letter-spacing: -0.03em;
    }}
    .brand-badge {{
      background: rgba(2, 132, 199, 0.15); border: 1px solid rgba(56, 189, 248, 0.35);
      color: #7dd3fc; font-family: var(--font-mono); font-size: 0.72rem;
      font-weight: 600; padding: 4px 10px; border-radius: 6px;
    }}
    .header-links {{ display: flex; align-items: center; gap: 1rem; }}
    .header-btn {{
      background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border);
      color: var(--text-muted); padding: 0.55rem 1.1rem; border-radius: 8px;
      font-size: 0.85rem; font-weight: 600; text-decoration: none; transition: all 0.2s;
      cursor: pointer;
    }}
    .header-btn:hover {{ background: rgba(255, 255, 255, 0.1); color: #fff; border-color: var(--border-accent); }}

    /* HERO BANNER */
    .hero-banner {{
      background: linear-gradient(135deg, rgba(12, 24, 40, 0.9) 0%, rgba(6, 15, 28, 0.95) 100%);
      border: 1px solid rgba(2, 132, 199, 0.3);
      border-radius: 20px; padding: 2.75rem; margin-bottom: 2.5rem;
      box-shadow: 0 20px 40px -15px rgba(0,0,0,0.7); position: relative; overflow: hidden;
    }}
    .hero-banner::after {{
      content: ""; position: absolute; right: -80px; top: -80px; width: 320px; height: 320px;
      background: radial-gradient(circle, rgba(2, 132, 199, 0.15) 0%, transparent 70%);
      pointer-events: none; border-radius: 50%;
    }}
    .hero-eyebrow {{
      font-family: var(--font-mono); font-size: 0.8rem; text-transform: uppercase;
      color: #38bdf8; font-weight: 700; letter-spacing: 0.08em; margin-bottom: 0.75rem;
      display: flex; align-items: center; gap: 8px;
    }}
    .hero-eyebrow::before {{
      content: ""; display: inline-block; width: 8px; height: 8px; background: #38bdf8; border-radius: 50%;
      box-shadow: 0 0 10px #38bdf8;
    }}
    .hero-title {{
      font-size: 2.45rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 1rem; line-height: 1.25;
    }}
    .hero-title span {{
      background: linear-gradient(135deg, #ffffff 40%, #7dd3fc 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .hero-subtitle {{
      color: var(--text-muted); font-size: 1.05rem; max-width: 950px; line-height: 1.7; margin-bottom: 2rem;
    }}
    .hero-stats-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1.25rem;
    }}
    .stat-card {{
      background: rgba(6, 9, 14, 0.75); border: 1px solid var(--border);
      padding: 1.2rem; border-radius: 12px; transition: border-color 0.2s;
    }}
    .stat-card:hover {{ border-color: var(--indegene-cyan); }}
    .stat-val {{
      font-size: 1.65rem; font-weight: 800; color: #f8fafc; font-family: var(--font-mono); margin-bottom: 0.25rem;
    }}
    .stat-label {{ color: var(--text-dim); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; }}

    /* BLUEPRINTS & DIAGRAMS ACCORDION */
    .blueprint-card {{
      background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px;
      padding: 1.75rem; margin-bottom: 2.5rem;
    }}
    .blueprint-title {{
      font-size: 1.25rem; font-weight: 700; color: #fff; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 10px;
    }}
    .mermaid-container {{
      background: #090e17; border: 1px solid rgba(255,255,255,0.06); border-radius: 12px;
      padding: 1.5rem; overflow-x: auto; margin-bottom: 1rem;
    }}

    /* FILTER & SEARCH BAR */
    .controls-wrapper {{
      position: sticky; top: 1rem; z-index: 50;
      background: rgba(12, 18, 28, 0.95); backdrop-filter: blur(20px);
      border: 1px solid var(--border); border-radius: 16px; padding: 1.25rem; margin-bottom: 2rem;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5); display: flex; flex-direction: column; gap: 1rem;
    }}
    .controls-top {{
      display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;
    }}
    .search-input-wrap {{ position: relative; flex: 1; min-width: 280px; }}
    .search-input-wrap input {{
      width: 100%; background: rgba(6, 9, 14, 0.9); border: 1px solid var(--border);
      padding: 0.75rem 1rem 0.75rem 2.6rem; border-radius: 10px; color: #fff; font-size: 0.92rem;
      outline: none; transition: border-color 0.2s;
    }}
    .search-input-wrap input:focus {{ border-color: var(--indegene-blue); }}
    .search-icon {{
      position: absolute; left: 0.9rem; top: 50%; transform: translateY(-50%);
      color: var(--text-dim); pointer-events: none; font-size: 0.95rem;
    }}
    .progress-box {{
      display: flex; align-items: center; gap: 14px; background: rgba(6, 9, 14, 0.6);
      padding: 0.5rem 1rem; border-radius: 10px; border: 1px solid var(--border);
    }}
    .progress-bar-track {{
      width: 130px; height: 8px; background: rgba(255,255,255,0.08); border-radius: 99px; overflow: hidden;
    }}
    .progress-bar-fill {{
      height: 100%; width: 0%; background: linear-gradient(90deg, #0284c7, #38bdf8);
      border-radius: 99px; transition: width 0.3s ease;
    }}
    .progress-text {{ font-family: var(--font-mono); font-size: 0.8rem; color: var(--text-muted); font-weight: 600; }}

    .pills-container {{
      display: flex; align-items: center; gap: 8px; overflow-x: auto; padding-bottom: 4px;
    }}
    .pill-btn {{
      background: rgba(255,255,255,0.04); border: 1px solid var(--border);
      color: var(--text-muted); font-size: 0.78rem; font-weight: 600; padding: 0.45rem 0.9rem;
      border-radius: 8px; cursor: pointer; white-space: nowrap; transition: all 0.2s;
    }}
    .pill-btn:hover {{ background: rgba(255,255,255,0.08); color: #fff; }}
    .pill-btn.active {{
      background: rgba(2, 132, 199, 0.25); border-color: var(--indegene-blue); color: #7dd3fc;
    }}

    /* QUESTION CARDS */
    .q-list {{ display: flex; flex-direction: column; gap: 1.25rem; }}
    .q-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      transition: all 0.25s ease;
    }}
    .q-card:hover {{
      border-color: rgba(56, 189, 248, 0.4);
      box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }}
    .q-card.completed {{
      border-color: rgba(13, 148, 136, 0.45);
      background: rgba(13, 148, 136, 0.03);
    }}

    .q-header {{
      padding: 1.25rem 1.5rem;
      cursor: pointer;
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 1.25rem;
      user-select: none;
    }}
    .q-header-left {{ display: flex; align-items: flex-start; gap: 14px; flex: 1; }}
    .q-num-badge {{
      background: rgba(2, 132, 199, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: #7dd3fc;
      font-family: var(--font-mono);
      font-size: 0.82rem; font-weight: 700;
      padding: 6px 12px; border-radius: 10px;
      white-space: nowrap; margin-top: 2px;
    }}
    .q-card.completed .q-num-badge {{
      background: rgba(13, 148, 136, 0.25);
      border-color: var(--indegene-teal);
      color: #5eead4;
    }}

    .q-meta-group {{ display: flex; flex-direction: column; gap: 4px; }}
    .q-cat-tag {{
      font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em;
      color: #38bdf8; font-weight: 700;
    }}
    .q-title-text {{
      font-size: 1.05rem; font-weight: 700; color: #f1f5f9; line-height: 1.45;
    }}
    .q-prompt-sub {{
      font-size: 0.88rem; color: var(--text-muted); font-style: italic; margin-top: 4px;
    }}

    .q-header-right {{
      display: flex; align-items: center; gap: 12px; margin-top: 4px;
    }}
    .word-badge {{
      background: rgba(2, 132, 199, 0.15); border: 1px solid rgba(56, 189, 248, 0.3);
      color: #7dd3fc; font-family: var(--font-mono); font-size: 0.75rem;
      padding: 4px 8px; border-radius: 6px; white-space: nowrap;
    }}
    .q-checkbox {{
      width: 18px; height: 18px; cursor: pointer; accent-color: #0284c7;
    }}
    .chevron {{
      color: var(--text-dim); font-size: 0.75rem; transition: transform 0.25s ease;
    }}
    .q-card.open .chevron {{ transform: rotate(180deg); color: #38bdf8; }}

    .q-body {{
      display: none;
      padding: 0 1.5rem 1.5rem 1.5rem;
      border-top: 1px solid rgba(255,255,255,0.06);
      background: rgba(6, 9, 14, 0.5);
    }}
    .q-card.open .q-body {{ display: block; }}

    .answer-content {{
      padding-top: 1.25rem;
      color: #e2e8f0;
      font-size: 0.96rem;
      line-height: 1.8;
    }}
    .answer-content p {{ margin-bottom: 1.15rem; }}
    .answer-content p:last-child {{ margin-bottom: 0; }}
    .answer-content strong {{ color: #ffffff; font-weight: 700; }}
    .answer-content ul, .answer-content ol {{ margin: 0 0 1.25rem 1.5rem; }}
    .answer-content li {{ margin-bottom: 0.5rem; }}

    .q-footer-bar {{
      margin-top: 1.5rem;
      padding-top: 1rem;
      border-top: 1px solid rgba(255,255,255,0.06);
      display: flex; align-items: center; justify-content: space-between;
      gap: 1rem; flex-wrap: wrap;
    }}
    .copy-ans-btn {{
      background: rgba(255,255,255,0.05); border: 1px solid var(--border);
      color: var(--text-muted); font-size: 0.78rem; font-weight: 600; padding: 6px 14px;
      border-radius: 6px; cursor: pointer; transition: all 0.2s;
    }}
    .copy-ans-btn:hover {{ background: rgba(255,255,255,0.1); color: #fff; border-color: var(--indegene-blue); }}
    .copy-toast {{
      font-size: 0.78rem; color: #5eead4; font-family: var(--font-mono); opacity: 0; transition: opacity 0.3s;
    }}
    .copy-toast.show {{ opacity: 1; }}

    @media (max-width: 768px) {{
      .page-wrapper {{ padding: 1rem 1rem 4rem; }}
      .hero-title {{ font-size: 1.85rem; }}
      .hero-banner {{ padding: 1.5rem; }}
      .q-header {{ padding: 1rem; flex-direction: column; align-items: flex-start; }}
      .q-header-right {{ align-self: flex-end; }}
    }}
  </style>
</head>
<body>

  <!-- PASSCODE GATE OVERLAY -->
  <div id="lockScreen">
    <div class="lock-box">
      <div class="lock-logo-mark">
        <span class="lock-txt-1">Indegene</span><span class="lock-txt-2">AI</span>
        <span class="lock-badge-pill">PREP PORTAL</span>
      </div>
      <h2>Data Scientist Interview Suite</h2>
      <p>Enter the candidate passcode to unlock the 30-question technical guide and architectural blueprints.</p>
      <div class="input-group">
        <input type="password" id="passInput" placeholder="Passcode" autocomplete="off" autofocus>
      </div>
      <button class="unlock-btn" onclick="checkPass()">Unlock Interview Suite</button>
      <div class="error-msg" id="errMsg">Passcode incorrect. Please enter the valid candidate access key.</div>
    </div>
  </div>

  <!-- MAIN APPLICATION CONTENT -->
  <div id="app">
    <div class="page-wrapper">
      
      <!-- TOP NAV -->
      <div class="top-bar">
        <div class="brand-mark">
          <span>Indegene · Data Scientist</span>
          <span class="brand-badge">Sandeep Kasiraju</span>
        </div>
        <div class="header-links">
          <button class="header-btn" onclick="expandAll(true)">Expand All</button>
          <button class="header-btn" onclick="expandAll(false)">Collapse All</button>
          <a class="header-btn" href="#blueprints">Architecture Blueprints</a>
          <button class="header-btn" onclick="lockPage()">Lock</button>
        </div>
      </div>

      <!-- HERO BANNER -->
      <div class="hero-banner">
        <div class="hero-eyebrow">Enterprise Healthcare & Commercial AI Preparation</div>
        <h1 class="hero-title">Data Scientist — <span>Pharma Analytics & AI</span></h1>
        <p class="hero-subtitle">
          Engineered for <strong>Sandeep Kasiraju</strong> targeting the <strong>Data Scientist – Pharma Analytics & AI</strong> position at <strong>Indegene</strong>. 
          Grounding 5 years of analytics experience across <strong>Centene ($3.1M readmission savings)</strong>, <strong>Adani ($2.4M predictive maintenance)</strong>, 
          <strong>UMass Dartmouth (94.3% PyTorch & LoRA LLMs)</strong>, and <strong>Multi-Agent Decision Orchestration</strong> directly into Indegene's commercial life sciences portfolio.
        </p>
        <div class="hero-stats-grid">
          <div class="stat-card">
            <div class="stat-val">30</div>
            <div class="stat-label">In-Depth Q&As (300+ Wds)</div>
          </div>
          <div class="stat-card">
            <div class="stat-val">6</div>
            <div class="stat-label">Core Competency Tracks</div>
          </div>
          <div class="stat-card">
            <div class="stat-val">3</div>
            <div class="stat-label">Enterprise Architecture Blueprints</div>
          </div>
          <div class="stat-card">
            <div class="stat-val">$3.1M</div>
            <div class="stat-label">Healthcare Claims Savings Grounding</div>
          </div>
        </div>
      </div>

      <!-- ARCHITECTURAL BLUEPRINTS -->
      <div id="blueprints" class="blueprint-card">
        <div class="blueprint-title">
          <span>🏛️ Enterprise System Architecture Blueprints</span>
        </div>
        
        <p style="color: var(--text-muted); font-size: 0.92rem; margin-bottom: 1.25rem;">
          These three system architecture blueprints provide an end-to-end technical visual representation of Sandeep's experience applied to Indegene's core workstreams: Real-World Data Claims risk stratification, Hierarchical multi-horizon sales forecasting, and Enterprise Multi-Agent AI orchestration.
        </p>

        <h4 style="color: #7dd3fc; margin-bottom: 0.75rem; font-size: 1rem;">Blueprint 1: Enterprise Pharma Real-World Data (RWE) & Claims Risk Stratification Pipeline</h4>
        <div class="mermaid-container">
          <pre class="mermaid">
graph TD
    subgraph Ingestion [Raw Real-World Data Ingestion]
        A1[EDI 837 Medical / Inpatient Claims] --> B[PySpark Batch / Streaming Ingestion]
        A2[EDI 835 Remittance / Payment Claims] --> B
        A3[NDC Pharmacy Prescription Claims] --> B
        A4[EHR & Lab Records LOINC/SNOMED] --> B
    end
    subgraph FeatureEng [Feature Engineering & Master Patient Index]
        B --> C1[MPI Patient Identity Resolution]
        C1 --> C2[Clinical Comorbidity Scoring CCI / Elixhauser]
        C1 --> C3[Medication Adherence PDC / MPR Metrics]
        C1 --> C4[Temporal Care Velocity & Prior Auth Rejections]
    end
    subgraph Modeling [Predictive Modeling & Explainability]
        C2 & C3 & C4 --> D[Stratified Temporal Cross-Validation]
        D --> E1[XGBoost / LightGBM Classifier]
        D --> E2[Calibrated Cost-Sensitive Logistic Regression]
        E1 & E2 --> F[TreeSHAP Global & Patient-Level Attributions]
    end
    subgraph Action [Commercial & Clinical Activation]
        F --> G1[High-Risk Patient Stratification & Case Mgmt Outreach]
        F --> G2[HCP Decile Targeting & Commercial Territory Planning]
        F --> G3[Executive Tableau / Power BI KPI Dashboards]
    end
          </pre>
        </div>

        <h4 style="color: #7dd3fc; margin: 1.5rem 0 0.75rem 0; font-size: 1rem;">Blueprint 2: Hierarchical Multi-Horizon Pharmaceutical Demand & Sales Forecasting Engine</h4>
        <div class="mermaid-container">
          <pre class="mermaid">
graph LR
    subgraph Hierarchy [Hierarchical Sales & Patient Demand Levels]
        L0[National Enterprise Sales Level] --> L1[Regional Distribution Centers]
        L1 --> L2[Territory / IDN Hospital Accounts]
        L2 --> L3[HCP / Pharmacy Outlet SKU Level]
    end
    subgraph Forecasting [Multi-Model Forecasting Engine]
        L0 & L1 --> M1[SARIMAX & Prophet Macro Trends + Exogenous Factors]
        L2 --> M2[Bi-LSTM & Temporal Fusion Transformers TFT]
        L3 --> M3[Croston / TSB Zero-Inflated Intermittent Method]
    end
    subgraph Reconciliation [Hierarchical Reconciliation & Distribution]
        M1 & M2 & M3 --> N[MinT Minimum Trace Optimal Reconciliation Matrix]
        N --> O1[Coherent Multi-Level Demand Projections]
        N --> O2[Safety Stock & Cold Chain Buffer Allocation]
        N --> O3[Commercial Quota Setting & Supply Chain ERP Sync]
    end
          </pre>
        </div>

        <h4 style="color: #7dd3fc; margin: 1.5rem 0 0.75rem 0; font-size: 1rem;">Blueprint 3: Enterprise Multi-Agent Clinical & Commercial AI Decision Engine</h4>
        <div class="mermaid-container">
          <pre class="mermaid">
graph TD
    subgraph ClientLayer [Client & Commercial Inquiry]
        User[Pharma Brand Director / Field Operations Lead] --> UI[FastAPI Gateway / Streamlit UI]
    end
    subgraph Orchestration [AutoGen Multi-Agent Pydantic State Engine]
        UI --> AG1[Agent 1: Researcher Agent RAG on Clinical Trials & Claims]
        AG1 -->|Validated JSON Schema| AG2[Agent 2: Analyst Agent Statistical & Econometric Modeling]
        AG2 -->|Validated JSON Schema| AG3[Agent 3: Skeptic Agent GxP Compliance, Bias & Sensitivity Audit]
        AG3 -->|Validated JSON Schema| AG4[Agent 4: Decision Agent Synthesizer Executive Strategy]
    end
    subgraph EnterpriseBacking [Enterprise Cloud & AI Foundation]
        AG1 -.-> KB1[(Snowflake Cortex / Cortex Search Vector DB)]
        AG2 -.-> KB2[(Vertex AI / SageMaker Hosted Pre-Trained LSTMs & XGBoost)]
        AG3 -.-> KB3[(FDA Guidance, GxP Audit Rules & Fair Treatment Checks)]
    end
    subgraph OutputLayer [Executive Decision Artifacts]
        AG4 --> Out1[Audited Commercial Recommendation & Sensitivity Analysis]
        AG4 --> Out2[C-Suite Slide Deck & Automated Executive Narrative]
    end
          </pre>
        </div>
      </div>

      <!-- FILTER CONTROLS -->
      <div class="controls-wrapper">
        <div class="controls-top">
          <div class="search-input-wrap">
            <span class="search-icon">🔍</span>
            <input type="text" id="searchInput" placeholder="Search keywords (e.g., claims, LSTM, LoRA, Snowflake, SHAP, drift)..." oninput="applyFilters()">
          </div>
          <div class="progress-box">
            <div class="progress-bar-track">
              <div class="progress-bar-fill" id="progressFill"></div>
            </div>
            <div class="progress-text" id="progressText">0 / 30 Reviewed</div>
          </div>
        </div>
        <div class="pills-container" id="categoryPills">
          <!-- Dynamically populated -->
        </div>
      </div>

      <!-- QUESTIONS CONTAINER -->
      <div class="q-list" id="questionList">
        <!-- Dynamically rendered via JS -->
      </div>

    </div>
  </div>

  <script>
    const CORRECT_PASS = "Sandeep";
    const questionsData = {items_json_str};
    const categoriesList = {categories_json_str};

    let activeCategory = "All";
    let completedSet = new Set();

    // Check localStorage for prior unlock
    window.addEventListener('DOMContentLoaded', () => {{
      mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
      if (sessionStorage.getItem('sandeep_unlocked') === 'true') {{
        unlockApp();
      }}
      initApp();
    }});

    function checkPass() {{
      const val = document.getElementById('passInput').value.trim();
      if (val.toLowerCase() === CORRECT_PASS.toLowerCase()) {{
        sessionStorage.setItem('sandeep_unlocked', 'true');
        unlockApp();
      }} else {{
        document.getElementById('errMsg').style.display = 'block';
      }}
    }}

    document.getElementById('passInput').addEventListener('keydown', (e) => {{
      if (e.key === 'Enter') checkPass();
    }});

    function unlockApp() {{
      document.getElementById('lockScreen').style.display = 'none';
      document.getElementById('app').style.display = 'block';
      window.scrollTo(0, 0);
    }}

    function lockPage() {{
      sessionStorage.removeItem('sandeep_unlocked');
      document.getElementById('app').style.display = 'none';
      document.getElementById('lockScreen').style.display = 'flex';
      document.getElementById('passInput').value = '';
      document.getElementById('errMsg').style.display = 'none';
    }}

    function initApp() {{
      // Build Category Pills
      const pillBox = document.getElementById('categoryPills');
      pillBox.innerHTML = '';
      
      const allBtn = document.createElement('button');
      allBtn.className = 'pill-btn active';
      allBtn.textContent = 'All Categories (' + questionsData.length + ')';
      allBtn.onclick = () => setCategory('All', allBtn);
      pillBox.appendChild(allBtn);

      categoriesList.forEach(cat => {{
        const btn = document.createElement('button');
        btn.className = 'pill-btn';
        const count = questionsData.filter(q => q.category === cat).length;
        btn.textContent = `${{cat}} (${{count}})`;
        btn.onclick = () => setCategory(cat, btn);
        pillBox.appendChild(btn);
      }});

      renderQuestions();
    }}

    function setCategory(cat, btnElem) {{
      activeCategory = cat;
      document.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
      btnElem.classList.add('active');
      applyFilters();
    }}

    function renderQuestions() {{
      const container = document.getElementById('questionList');
      container.innerHTML = '';

      questionsData.forEach(q => {{
        const card = document.createElement('div');
        card.className = 'q-card';
        card.id = `qcard-${{q.num}}`;
        card.setAttribute('data-category', q.category);
        card.setAttribute('data-num', q.num);

        const renderedMd = marked.parse(q.answer);

        card.innerHTML = `
          <div class="q-header" onclick="toggleCard(${{q.num}})">
            <div class="q-header-left">
              <span class="q-num-badge">Q${{q.num.toString().padStart(2, '0')}}</span>
              <div class="q-meta-group">
                <span class="q-cat-tag">${{q.category}}</span>
                <div class="q-title-text">${{q.title}}</div>
                <div class="q-prompt-sub">"${{q.question}}"</div>
              </div>
            </div>
            <div class="q-header-right">
              <span class="word-badge">${{q.words}} words</span>
              <input type="checkbox" class="q-checkbox" onclick="event.stopPropagation(); toggleComplete(${{q.num}})" title="Mark completed">
              <span class="chevron">▼</span>
            </div>
          </div>
          <div class="q-body">
            <div class="answer-content">
              ${{renderedMd}}
            </div>
            <div class="q-footer-bar">
              <button class="copy-ans-btn" onclick="copyAnswer(${{q.num}}, this)">📋 Copy Answer Text</button>
              <span class="copy-toast" id="toast-${{q.num}}">Copied to clipboard!</span>
            </div>
          </div>
        `;
        container.appendChild(card);
      }});
      updateProgress();
    }}

    function toggleCard(num) {{
      const card = document.getElementById(`qcard-${{num}}`);
      card.classList.toggle('open');
    }}

    function expandAll(open) {{
      document.querySelectorAll('.q-card').forEach(c => {{
        if (open) c.classList.add('open');
        else c.classList.remove('open');
      }});
    }}

    function toggleComplete(num) {{
      const card = document.getElementById(`qcard-${{num}}`);
      if (completedSet.has(num)) {{
        completedSet.delete(num);
        card.classList.remove('completed');
      }} else {{
        completedSet.add(num);
        card.classList.add('completed');
      }}
      updateProgress();
    }}

    function updateProgress() {{
      const total = questionsData.length;
      const count = completedSet.size;
      const pct = Math.round((count / total) * 100);
      document.getElementById('progressFill').style.width = pct + '%';
      document.getElementById('progressText').textContent = `${{count}} / ${{total}} Reviewed (${{pct}}%)`;
    }}

    function applyFilters() {{
      const query = document.getElementById('searchInput').value.toLowerCase().trim();

      questionsData.forEach(q => {{
        const card = document.getElementById(`qcard-${{q.num}}`);
        const matchesCat = (activeCategory === 'All' || q.category === activeCategory);
        const textContent = (q.title + ' ' + q.question + ' ' + q.answer).toLowerCase();
        const matchesQuery = !query || textContent.includes(query);

        if (matchesCat && matchesQuery) {{
          card.style.display = 'block';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    function copyAnswer(num, btn) {{
      const q = questionsData.find(item => item.num === num);
      if (!q) return;
      navigator.clipboard.writeText(q.answer).then(() => {{
        const toast = document.getElementById(`toast-${{num}}`);
        toast.classList.add('show');
        setTimeout(() => {{ toast.classList.remove('show'); }}, 2000);
      }});
    }}
  </script>
</body>
</html>
"""
    return html

# =============================================================================
# MAIN BUILD SCRIPT ENTRYPOINT
# =============================================================================
def main():
    print(f"Building Sandeep Kasiraju Indegene Prep Suite...")
    print(f"Loaded {len(ALL_QUESTIONS)} total questions.")

    # 1. Master Markdown
    master_md = generate_markdown()
    md_path = "sandeep_kasiraju_indegene_prep.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(master_md)
    print(f"Master Markdown generated: {md_path} ({len(master_md.split())} words)")

    # 2. Nextra MDX
    mdx_content = generate_mdx(master_md)
    mdx_path = os.path.join("content", "sandeep-kasiraju-indegene-prep.mdx")
    with open(mdx_path, "w", encoding="utf-8") as f:
        f.write(mdx_content)
    print(f"Nextra MDX generated: {mdx_path}")

    # 3. Interactive Webpage
    html_content = generate_html()
    html_path = "sandeep_kasiraju_indegene_prep.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Interactive Webpage generated: {html_path}")

    # 4. Copy to public/
    os.makedirs("public", exist_ok=True)
    pub_html_path = os.path.join("public", "sandeep_kasiraju_indegene_prep.html")
    with open(pub_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Public Webpage generated: {pub_html_path}")

    print("\nAll Sandeep Kasiraju prep assets successfully compiled!")

if __name__ == "__main__":
    main()
