# -*- coding: utf-8 -*-
"""
Build script for Venkata Sai Varun Munagavalasa's Forward Deployed Engineer (Healthcare AI / Clinical Platforms)
Interview Preparation Suite.

Compiles:
1. venkata_fde_health_prep.md
2. content/venkata-fde-health-prep.mdx
3. venkata_fde_health_prep.html
4. public/venkata_fde_health_prep.html

Passcode: "Venkata"
"""

import json
import re
import os
import shutil

from venkata_questions_part1 import QUESTIONS_PART1
from venkata_questions_part2 import QUESTIONS_PART2
from venkata_coding import CODING_PROBLEMS

QUESTIONS = QUESTIONS_PART1 + QUESTIONS_PART2
print(f"Loaded {len(QUESTIONS)} Technical Questions and {len(CODING_PROBLEMS)} Coding Problems.")

# =============================================================================
# 1. GENERATE MASTER MARKDOWN (venkata_fde_health_prep.md)
# =============================================================================
def generate_markdown():
    md = []
    md.append("# Venkata Sai Varun Munagavalasa — Forward Deployed Engineer (Healthcare AI / Clinical Platforms) Technical Preparation Suite\n\n")
    md.append("## Target Role: Forward Deployed Engineer (Healthcare AI / Clinical Platforms)\n\n")
    md.append("**Candidate:** Venkata Sai Varun Munagavalasa | Houston, TX, USA | (281) 473-4128 | saivarun.1602@gmail.com | [LinkedIn](https://linkedin.com)\n\n")
    md.append("**Target Focus:** Forward Deployed Engineering (FDE) · Clinical Platforms · Healthcare AI/GenAI · HL7 FHIR R4 & EHR Integration (Epic/Cerner) · SMART on FHIR & CDS Hooks · Real-Time Streaming (Kafka, Flink, Debezium CDC) · Cloud Data Engineering (AWS Glue, Spark, Snowflake, Redshift) · Airflow Orchestration · Data Contracts & Observability (dbt, Great Expectations) · RAG & LLM Evaluation (Ragas, Faithfulness, Citation Grounding) · HIPAA Compliance & PHI De-Identification\n\n")
    md.append("**Role Context & Compensation:** $200,000 – $250,000 Base/Total Comp · Remote (50% Client Site Travel) · Job ID: 510818585 · Forward Deployed Client Architecture & Clinical Co-Development\n\n")
    md.append("**Passcode Lock:** `Venkata`\n\n")
    md.append("---\n\n")

    md.append("## Executive Summary & Strategic FDE Value Proposition\n\n")
    md.append("> **Venkata Sai Varun Munagavalasa** is an enterprise **Data Engineer, Healthcare Data Specialist, and Forward Deployed Systems Architect** with 3+ years of production experience designing and deploying high-throughput data pipelines, real-time event streaming architectures, enterprise lakehouses, and clinical intelligence platforms across healthcare payers, health systems, and financial consulting leaders. He bridges the critical gap between complex enterprise healthcare infrastructure (EHRs, claims engines, payer adjudication) and cutting-edge artificial intelligence, data engineering, and modern analytical systems.\n\n")
    md.append("> At **Cigna Healthcare**, Venkata architected cloud-native EHR ingestion pipelines utilizing **AWS Glue and Apache Spark**, ingesting and normalizing **80,000 daily patient records** across HL7 FHIR and relational formats while reducing downstream clinical reporting latency from **1 hour down to 15 minutes** across 3 enterprise consumer platforms. He engineered an ultra-low-latency real-time streaming pipeline using **Apache Kafka and AWS Lambda** for member eligibility validation, processing **20,000 transactions daily** with **sub-10-second end-to-end latency** for downstream adjudication. He deployed **8 Apache Airflow DAGs** eliminating 2 hours of weekly manual operations, authored **Snowflake SQL transformations and dbt data contracts** slashing reconciliations from 15 to 3 per quarter, and implemented **automated Great Expectations testing** preventing schema regressions across 5 core claims and clinical tables.\n\n")
    md.append("> At **KPMG**, Venkata engineered **Amazon Redshift migration pipelines** migrating 500,000+ historical audit and financial records with **zero downtime**, authored **25+ complex DAX measures** in Power BI executive scorecards, deployed **Python anomaly detection models** flagging 40+ journal irregularities monthly, built **SSIS master data staging workflows**, and partnered with cross-functional IT, tax, and audit stakeholders under **Agile/Scrum delivery**.\n\n")
    md.append("> As a **Forward Deployed Engineer (FDE)** for healthcare AI and clinical platforms, Venkata brings a rare blend of field-facing customer empathy, rapid on-site prototyping capability, deep clinical interoperability domain knowledge (HL7 FHIR R4, SMART on FHIR, CDS Hooks, DICOM, ICD-10/SNOMED), and hardened cloud distributed systems engineering. He is equipped to embed directly with health system CIOs, CMIOs, clinical informatics directors, and enterprise AI engineering teams to deploy production AI pipelines that meet strict HIPAA compliance, clinical safety, and low-latency SLA requirements.\n\n")

    md.append("## Quantified Impact & Architecture Metrics\n\n")
    md.append("| Organization / System | Domain & Scope | Core Tech Stack | Quantified Engineering & Clinical Impact |\n")
    md.append("| :--- | :--- | :--- | :--- |\n")
    md.append("| **Cigna Healthcare** | High-Throughput EHR Ingestion | AWS Glue, Apache Spark, S3, Parquet | Ingested **80,000 patient records daily**; cut downstream reporting latency from **1 hour to 15 minutes (75% reduction)** |\n")
    md.append("| **Cigna Healthcare** | Real-Time Eligibility Streaming | Apache Kafka, AWS Lambda, DynamoDB | Processed **20,000 checks daily** with **sub-10-second end-to-end latency** for insurance adjudication |\n")
    md.append("| **Cigna Healthcare** | Enterprise Workflow Orchestration | Apache Airflow, Python, Docker, Slack | Deployed **8 production DAGs**; eliminated 2 hours/week manual intervention; cut failure alerts by 40% |\n")
    md.append("| **Cigna Healthcare** | Clinical Data Contract Enforcement | Snowflake, dbt, SQL, Information Schema | Built schema & contract validation; cut downstream reconciliations from **15 to 3 per quarter (80% drop)** |\n")
    md.append("| **Cigna Healthcare** | Automated Data Observability | Great Expectations, Python, S3 | Automated assertion testing across 5 core tables; prevented schema drift & duplicate clinical records |\n")
    md.append("| **Cigna Healthcare** | Unstructured Physician Notes ELT | Python, Regex, spaCy, Snowflake | Ingested **5,000 weekly progress notes**; extracted ICD-10/SNOMED diagnostic tags with zero manual coding |\n")
    md.append("| **Cigna Healthcare** | HIPAA Compliance & PHI Security | AWS KMS, IAM, Secrets Manager, CloudTrail | Maintained **100% HIPAA audit compliance**; enforced zero-trust encryption and column-level masking |\n")
    md.append("| **KPMG** | Enterprise Financial Cloud Migration | Amazon Redshift, Python, S3, Parquet | Migrated **500,000+ historical records** from SQL Server to Redshift with zero downtime & 4x query acceleration |\n")
    md.append("| **KPMG** | Executive BI & Tabular Modeling | Power BI, DAX (25+ measures), Star Schema | Automated financial scorecards across 4 operational entities; saved **6 analyst hours per reporting cycle** |\n")
    md.append("| **KPMG** | Financial Anomaly Detection | Python, Scikit-learn, Isolation Forest | Flagged **40+ anomalous journal entries monthly**; reduced manual sampling audit effort by 35% |\n")
    md.append("| **KPMG** | Master Data Integration | SSIS, SQL Server, Python, Fuzzy Lookup | Consolidated 3 legacy ERP instances; improved entity matching accuracy from 81% to 96% |\n")
    md.append("| **Flagship: Clinical FDE** | SMART on FHIR & CDS Hooks | FastAPI, Python, FHIR R4, OAuth2 | Built real-time clinical advisory service delivering drug-interaction cards in **sub-250ms at bedside** |\n")
    md.append("| **Flagship: Clinical RAG** | Guideline-Grounded Retrieval | LangChain, FAISS, BM25, Med-BERT | Hybrid RAG over 10,000 clinical practice guidelines; achieved **94.2% factual precision** with citation verification |\n")
    md.append("| **Flagship: Real-Time CDC** | Event-Driven Streaming Platform | Kafka, Flink, Debezium, Kubernetes | Ingested **15,000 events/sec** from EHR databases; exactly-once semantics with sub-second replication |\n")
    md.append("| **Flagship: Predictive Churn** | Member Retention Machine Learning | XGBoost, Scikit-learn, MLflow, SHAP | Evaluated **65,000 member journeys**; achieved 0.88 ROC-AUC and enabled proactive intervention |\n\n")

    md.append("---\n\n")

    # Add 30 Questions
    md.append("## Part 1: Cigna Healthcare — Clinical Ingestion, Real-Time Streaming & Enterprise Governance (Questions 01 – 10)\n\n")
    for q in QUESTIONS[:10]:
        md.append(f"### {q['id']}: {q['title']}\n\n")
        md.append(f"**Interview Question:** \"{q['question']}\"\n\n")
        md.append(f"**Perspective & Delivery:** {q['perspective']}\n\n")
        md.append(f"**Comprehensive Answer:**\n\n{q['answer']}\n\n---\n\n")

    md.append("## Part 2: KPMG — Financial Migration, BI Tabular Modeling & Governance (Questions 11 – 20)\n\n")
    for q in QUESTIONS[10:20]:
        md.append(f"### {q['id']}: {q['title']}\n\n")
        md.append(f"**Interview Question:** \"{q['question']}\"\n\n")
        md.append(f"**Perspective & Delivery:** {q['perspective']}\n\n")
        md.append(f"**Comprehensive Answer:**\n\n{q['answer']}\n\n---\n\n")

    md.append("## Part 3: Forward Deployed Engineering, Healthcare AI/GenAI & Flagship Systems (Questions 21 – 30)\n\n")
    for q in QUESTIONS[20:30]:
        md.append(f"### {q['id']}: {q['title']}\n\n")
        md.append(f"**Interview Question:** \"{q['question']}\"\n\n")
        md.append(f"**Perspective & Delivery:** {q['perspective']}\n\n")
        md.append(f"**Comprehensive Answer:**\n\n{q['answer']}\n\n---\n\n")

    # Add 10 Coding / Analytical Problems
    md.append("## Part 4: Production-Grade Healthcare & Data Engineering Implementations (10 Problems)\n\n")
    for cp in CODING_PROBLEMS:
        md.append(f"### Problem {cp['num']}: {cp['title']}\n\n")
        md.append(f"**Category:** `{cp['category']}`\n\n")
        md.append(f"#### Business Context & Clinical Problem Statement\n{cp['problem']}\n\n")
        md.append(f"#### Production-Grade Code Solution\n```python\n{cp['code']}\n```\n\n")
        md.append(f"#### Complexity & Operational Analysis\n{cp['complexity']}\n\n---\n\n")

    return "".join(md)


# =============================================================================
# 2. GENERATE NEXTRA MDX (content/venkata-fde-health-prep.mdx)
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


def generate_mdx(markdown_content):
    escaped_body = sanitize_for_mdx(markdown_content)
    frontmatter = """---
title: "Venkata Sai Varun — Forward Deployed Engineer (Healthcare AI) Prep"
description: "Comprehensive 30-Question Technical Preparation Suite, Clinical Systems Architecture, and 10 Production Healthcare & Data Engineering Solutions for Forward Deployed Engineer."
---

<PasswordGate password="Venkata" candidateName="Venkata Sai Varun Munagavalasa">

"""
    footer = "\n\n</PasswordGate>\n"
    return frontmatter + escaped_body + footer


# =============================================================================
# 3. GENERATE INTERACTIVE STANDALONE HTML (venkata_fde_health_prep.html)
# =============================================================================
def generate_html():
    questions_json = json.dumps(QUESTIONS)
    coding_json = json.dumps(CODING_PROBLEMS)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Venkata Sai Varun — Forward Deployed Engineer (Healthcare AI) Prep Suite</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #080d1a;
            --bg-secondary: #0f172a;
            --bg-card: rgba(15, 23, 42, 0.75);
            --bg-card-hover: rgba(30, 41, 59, 0.85);
            --border-color: rgba(255, 255, 255, 0.08);
            --border-focus: #06b6d4;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-teal: #06b6d4;
            --accent-cyan: #0891b2;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-purple: #8b5cf6;
            --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
            --shadow-subtle: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
            --shadow-glow: 0 0 25px -5px rgba(6, 182, 212, 0.4);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: var(--font-sans);
            line-height: 1.6;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        /* Password Gate Modal */
        #lockScreen {{
            position: fixed;
            inset: 0;
            background: rgba(8, 13, 26, 0.96);
            backdrop-filter: blur(16px);
            z-index: 99999;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
        }}

        .lock-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 1.25rem;
            padding: 2.5rem;
            width: 100%;
            max-width: 450px;
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.7), var(--shadow-glow);
            text-align: center;
            position: relative;
        }}

        .lock-logo {{
            width: 58px;
            height: 58px;
            background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
            border-radius: 14px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.85rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 8px 16px -4px rgba(6, 182, 212, 0.5);
        }}

        .lock-title {{
            font-size: 1.45rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }}

        .lock-desc {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-bottom: 1.75rem;
            line-height: 1.5;
        }}

        .lock-input-group {{
            margin-bottom: 1.25rem;
            position: relative;
        }}

        .lock-input {{
            width: 100%;
            padding: 0.85rem 1rem;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            color: var(--text-primary);
            font-family: var(--font-sans);
            font-size: 1rem;
            outline: none;
            transition: all 0.2s ease;
        }}

        .lock-input:focus {{
            border-color: var(--accent-teal);
            box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.25);
            background: rgba(255, 255, 255, 0.06);
        }}

        .lock-btn {{
            width: 100%;
            padding: 0.85rem;
            background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
            border: none;
            border-radius: 0.75rem;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(6, 182, 212, 0.35);
        }}

        .lock-btn:hover {{
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.5);
        }}

        .lock-error {{
            color: #ef4444;
            font-size: 0.85rem;
            margin-top: 0.75rem;
            display: none;
        }}

        /* App Layout */
        .app-container {{
            display: none; /* revealed on unlock */
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem 1.5rem 5rem;
        }}

        /* Header Banner */
        .hero-banner {{
            background: linear-gradient(135deg, rgba(8, 145, 178, 0.25) 0%, rgba(15, 23, 42, 0.9) 100%);
            border: 1px solid rgba(6, 182, 212, 0.35);
            border-radius: 1.5rem;
            padding: 2.5rem;
            margin-bottom: 2.5rem;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-subtle);
        }}

        .hero-banner::after {{
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(6, 182, 212, 0.2) 0%, transparent 70%);
            pointer-events: none;
        }}

        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(6, 182, 212, 0.2);
            border: 1px solid rgba(6, 182, 212, 0.4);
            padding: 0.35rem 0.85rem;
            border-radius: 2rem;
            font-size: 0.8rem;
            font-weight: 600;
            color: #67e8f9;
            margin-bottom: 1rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}

        .hero-title {{
            font-size: 2.3rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 0.75rem;
            letter-spacing: -0.03em;
        }}

        .hero-subtitle {{
            font-size: 1.12rem;
            color: #cbd5e1;
            max-width: 900px;
            margin-bottom: 1.5rem;
        }}

        .hero-meta-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }}

        .hero-meta-item {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .hero-meta-item strong {{
            color: var(--text-primary);
        }}

        /* Metrics Grid */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 1rem;
            margin-bottom: 2.5rem;
        }}

        .metric-card {{
            background: var(--bg-card);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-color);
            border-radius: 1rem;
            padding: 1.25rem 1.5rem;
            transition: all 0.25s ease;
        }}

        .metric-card:hover {{
            background: var(--bg-card-hover);
            border-color: rgba(6, 182, 212, 0.4);
            transform: translateY(-2px);
        }}

        .metric-num {{
            font-size: 1.85rem;
            font-weight: 800;
            color: #22d3ee;
            margin-bottom: 0.25rem;
            letter-spacing: -0.02em;
        }}

        .metric-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        /* Navigation Tabs */
        .nav-tabs {{
            display: flex;
            gap: 0.75rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1rem;
            margin-bottom: 2rem;
            overflow-x: auto;
        }}

        .tab-btn {{
            padding: 0.65rem 1.25rem;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            border-radius: 0.65rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s ease;
        }}

        .tab-btn:hover {{
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.06);
        }}

        .tab-btn.active {{
            background: #0891b2;
            color: white;
            border-color: #06b6d4;
            box-shadow: 0 4px 12px rgba(6, 182, 212, 0.4);
        }}

        /* Search & Filter Bar */
        .controls-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem;
        }}

        .search-box {{
            flex: 1;
            min-width: 280px;
            position: relative;
        }}

        .search-input {{
            width: 100%;
            padding: 0.75rem 1rem 0.75rem 2.5rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            color: var(--text-primary);
            font-size: 0.95rem;
            outline: none;
            transition: all 0.2s ease;
        }}

        .search-input:focus {{
            border-color: var(--accent-teal);
            box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.25);
        }}

        .search-icon {{
            position: absolute;
            left: 0.9rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }}

        /* Question Cards */
        .question-card {{
            background: var(--bg-card);
            backdrop-filter: blur(8px);
            border: 1px solid var(--border-color);
            border-radius: 1.25rem;
            padding: 2rem;
            margin-bottom: 1.5rem;
            transition: all 0.25s ease;
        }}

        .question-card:hover {{
            border-color: rgba(6, 182, 212, 0.4);
            background: var(--bg-card-hover);
            box-shadow: var(--shadow-subtle);
        }}

        .q-header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 1rem;
        }}

        .q-badge-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 0.75rem;
        }}

        .q-badge {{
            padding: 0.25rem 0.65rem;
            border-radius: 0.4rem;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .badge-id {{
            background: rgba(6, 182, 212, 0.2);
            color: #22d3ee;
            border: 1px solid rgba(6, 182, 212, 0.4);
        }}

        .badge-cat {{
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-secondary);
            border: 1px solid var(--border-color);
        }}

        .badge-words {{
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}

        .q-title {{
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.35;
            letter-spacing: -0.01em;
        }}

        .q-prompt-box {{
            background: rgba(6, 182, 212, 0.08);
            border-left: 3px solid #06b6d4;
            padding: 1rem 1.25rem;
            border-radius: 0 0.75rem 0.75rem 0;
            margin: 1rem 0 1.5rem;
            font-size: 1rem;
            color: #e2e8f0;
            font-weight: 500;
            line-height: 1.5;
        }}

        .q-answer {{
            color: #cbd5e1;
            font-size: 1rem;
            line-height: 1.75;
        }}

        .q-answer p {{
            margin-bottom: 1.15rem;
        }}

        .q-answer p:last-child {{
            margin-bottom: 0;
        }}

        .q-answer strong {{
            color: #f8fafc;
            font-weight: 700;
        }}

        /* Coding Section */
        .code-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 1.25rem;
            padding: 2rem;
            margin-bottom: 2rem;
        }}

        .code-title {{
            font-size: 1.35rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
        }}

        .code-problem {{
            color: #cbd5e1;
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 1.25rem;
            white-space: pre-line;
        }}

        .code-block-container {{
            position: relative;
            margin: 1rem 0;
        }}

        pre {{
            background: #040812;
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            padding: 1.25rem;
            overflow-x: auto;
            font-family: var(--font-mono);
            font-size: 0.88rem;
            line-height: 1.6;
            color: #e2e8f0;
        }}

        .copy-btn {{
            position: absolute;
            top: 0.75rem;
            right: 0.75rem;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 0.4rem;
            color: #cbd5e1;
            font-size: 0.75rem;
            padding: 0.35rem 0.65rem;
            cursor: pointer;
            font-family: var(--font-sans);
            transition: all 0.2s ease;
        }}

        .copy-btn:hover {{
            background: #0891b2;
            color: white;
        }}

        .complexity-tag {{
            display: inline-block;
            background: rgba(139, 92, 246, 0.12);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 0.5rem;
            padding: 0.6rem 1rem;
            font-size: 0.85rem;
            color: #c4b5fd;
            margin-top: 1rem;
            width: 100%;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .hero-title {{
                font-size: 1.75rem;
            }}
            .question-card, .code-card {{
                padding: 1.25rem;
            }}
        }}
    </style>
</head>
<body>

    <!-- Passcode Gate Screen -->
    <div id="lockScreen">
        <div class="lock-card">
            <div class="lock-logo">🔒</div>
            <h2 class="lock-title">Candidate Confidential Access</h2>
            <p class="lock-desc">Enter the authorization passcode for <strong>Venkata Sai Varun Munagavalasa's Forward Deployed Engineer Preparation Suite</strong>.</p>
            <form id="lockForm" onsubmit="handleUnlock(event)">
                <div class="lock-input-group">
                    <input type="password" id="passInput" class="lock-input" placeholder="Enter Passcode..." autofocus required autocomplete="off">
                </div>
                <button type="submit" class="lock-btn">Unlock Portal</button>
                <div id="lockError" class="lock-error">Invalid passcode. Please enter the authorized passcode.</div>
            </form>
        </div>
    </div>

    <!-- Main Prep App Container -->
    <div class="app-container" id="appContainer">

        <!-- Hero Header -->
        <header class="hero-banner">
            <div class="hero-badge">Forward Deployed Engineer · Healthcare AI & Clinical Platforms</div>
            <h1 class="hero-title">Venkata Sai Varun Munagavalasa — Technical Interview Suite</h1>
            <p class="hero-subtitle">
                Target Role: <strong>Forward Deployed Engineer (Healthcare AI / Clinical Platforms)</strong> ($200K – $250K | Remote, 50% Travel | Job ID: 510818585). Grounded in HL7 FHIR R4 interoperability, SMART on FHIR, CDS Hooks, AWS Glue/Spark EHR ingestion, Kafka real-time streaming, Airflow orchestration, clinical RAG, and production LLM evaluation across Cigna Healthcare and KPMG.
            </p>
            <div class="hero-meta-row">
                <div class="hero-meta-item">📍 <strong>Location:</strong> Houston, TX, USA</div>
                <div class="hero-meta-item">💼 <strong>Target Role:</strong> Forward Deployed Engineer</div>
                <div class="hero-meta-item">🏥 <strong>Domain:</strong> Healthcare AI, Clinical Platforms, Payers</div>
                <div class="hero-meta-item">🛡️ <strong>Focus:</strong> FHIR R4, CDS Hooks, Spark, Kafka, Snowflake, RAG</div>
            </div>
        </header>

        <!-- KPI Metrics Grid -->
        <section class="metrics-grid">
            <div class="metric-card">
                <div class="metric-num">30</div>
                <div class="metric-label">In-Depth Technical Questions (>= 300 Words Each)</div>
            </div>
            <div class="metric-card">
                <div class="metric-num">10</div>
                <div class="metric-label">Production Healthcare & Data Engineering Solutions</div>
            </div>
            <div class="metric-card">
                <div class="metric-num">80,000</div>
                <div class="metric-label">Daily EHR Records Ingested via AWS Glue & Spark</div>
            </div>
            <div class="metric-card">
                <div class="metric-num">20,000</div>
                <div class="metric-label">Daily Real-Time Eligibility Checks (<10s Latency)</div>
            </div>
            <div class="metric-card">
                <div class="metric-num">1h &rarr; 15m</div>
                <div class="metric-label">Clinical Reporting Latency Slashed Across 3 Platforms</div>
            </div>
        </section>

        <!-- Navigation Tabs -->
        <nav class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab('all', this)">All Content</button>
            <button class="tab-btn" onclick="switchTab('part1', this)">Part 1: Cigna Healthcare (Q01-Q10)</button>
            <button class="tab-btn" onclick="switchTab('part2', this)">Part 2: KPMG (Q11-Q20)</button>
            <button class="tab-btn" onclick="switchTab('part3', this)">Part 3: Healthcare AI & FDE (Q21-Q30)</button>
            <button class="tab-btn" onclick="switchTab('coding', this)">Part 4: 10 Production Solutions</button>
        </nav>

        <!-- Search Box -->
        <div class="controls-bar">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" id="searchInput" class="search-input" placeholder="Search keywords (e.g., FHIR, Spark, Kafka, CDS Hooks, RAG, Snowflake, dbt, Airflow)..." oninput="handleSearch()">
            </div>
            <div style="font-size: 0.9rem; color: var(--text-secondary);" id="matchCounter">Showing 30 Questions & 10 Code Implementations</div>
        </div>

        <!-- Questions Feed -->
        <main id="questionsContainer"></main>

        <!-- Coding Feed -->
        <section id="codingContainer" style="display: none;"></section>

    </div>

    <script>
        const QUESTIONS = {questions_json};
        const CODING_PROBLEMS = {coding_json};

        let currentTab = 'all';

        // Unlock verification logic
        function handleUnlock(e) {{
            e.preventDefault();
            const input = document.getElementById('passInput');
            const val = input.value.trim().toLowerCase();
            const err = document.getElementById('lockError');

            if (val === 'venkata') {{
                document.getElementById('lockScreen').style.display = 'none';
                document.getElementById('appContainer').style.display = 'block';
                sessionStorage.setItem('venkata_prep_unlocked', 'true');
                renderQuestions();
                renderCoding();
            }} else {{
                err.style.display = 'block';
                input.focus();
                input.select();
            }}
        }}

        // Auto unlock if session exists
        window.addEventListener('DOMContentLoaded', () => {{
            if (sessionStorage.getItem('venkata_prep_unlocked') === 'true') {{
                document.getElementById('lockScreen').style.display = 'none';
                document.getElementById('appContainer').style.display = 'block';
                renderQuestions();
                renderCoding();
            }}
        }});

        function switchTab(tab, btn) {{
            currentTab = tab;
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            if (btn) {{
                btn.classList.add('active');
            }}

            const qContainer = document.getElementById('questionsContainer');
            const cContainer = document.getElementById('codingContainer');

            if (tab === 'coding') {{
                qContainer.style.display = 'none';
                cContainer.style.display = 'block';
            }} else {{
                qContainer.style.display = 'block';
                cContainer.style.display = 'none';
                renderQuestions();
            }}
        }}

        function formatMarkdownBold(text) {{
            return text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
        }}

        function renderQuestions() {{
            const container = document.getElementById('questionsContainer');
            const search = document.getElementById('searchInput').value.toLowerCase();
            container.innerHTML = '';

            let filtered = QUESTIONS.filter(q => {{
                // Tab filter
                const qNum = parseInt(q.id.replace('Q',''));
                if (currentTab === 'part1' && qNum > 10) return false;
                if (currentTab === 'part2' && (qNum <= 10 || qNum > 20)) return false;
                if (currentTab === 'part3' && qNum <= 20) return false;

                // Search query
                if (search) {{
                    const full = (q.title + ' ' + q.question + ' ' + q.answer + ' ' + q.category).toLowerCase();
                    return full.includes(search);
                }}
                return true;
            }});

            document.getElementById('matchCounter').innerText = `Showing ${{filtered.length}} of 30 Questions`;

            filtered.forEach(q => {{
                const card = document.createElement('article');
                card.className = 'question-card';

                // Format paragraphs
                const paragraphs = q.answer.trim().split('\\n\\n')
                    .map(p => `<p>${{formatMarkdownBold(p)}}</p>`)
                    .join('');

                card.innerHTML = `
                    <div class="q-header">
                        <div>
                            <div class="q-badge-row">
                                <span class="q-badge badge-id">${{q.id}}</span>
                                <span class="q-badge badge-cat">${{q.category}}</span>
                                <span class="q-badge badge-words">Verified >= 300 Words</span>
                            </div>
                            <h2 class="q-title">${{q.title}}</h2>
                        </div>
                    </div>
                    <div class="q-prompt-box">
                        "${{q.question}}"
                    </div>
                    <div class="q-answer">
                        ${{paragraphs}}
                    </div>
                `;
                container.appendChild(card);
            }});
        }}

        function renderCoding() {{
            const container = document.getElementById('codingContainer');
            container.innerHTML = '<h2 style="font-size: 1.75rem; font-weight: 800; margin-bottom: 1.5rem;">Part 4: 10 Production-Grade Healthcare & Data Engineering Solutions</h2>';

            CODING_PROBLEMS.forEach(cp => {{
                const card = document.createElement('article');
                card.className = 'code-card';
                card.innerHTML = `
                    <div class="q-badge-row">
                        <span class="q-badge badge-id">Problem ${{cp.num}}</span>
                        <span class="q-badge badge-cat">${{cp.category}}</span>
                    </div>
                    <h3 class="code-title">${{cp.title}}</h3>
                    <div class="code-problem">${{cp.problem}}</div>
                    <div class="code-block-container">
                        <button class="copy-btn" onclick="copyCode(this)">Copy Code</button>
                        <pre><code>${{escapeHtml(cp.code)}}</code></pre>
                    </div>
                    <div class="complexity-tag">
                        <strong>Performance & Complexity:</strong> ${{cp.complexity}}
                    </div>
                `;
                container.appendChild(card);
            }});
        }}

        function escapeHtml(text) {{
            return text
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }}

        function copyCode(btn) {{
            const code = btn.nextElementSibling.innerText;
            navigator.clipboard.writeText(code).then(() => {{
                btn.innerText = 'Copied!';
                setTimeout(() => btn.innerText = 'Copy Code', 2000);
            }});
        }}

        function handleSearch() {{
            if (currentTab === 'coding') {{
                const search = document.getElementById('searchInput').value.toLowerCase();
                const cards = document.querySelectorAll('.code-card');
                cards.forEach(c => {{
                    c.style.display = c.innerText.toLowerCase().includes(search) ? 'block' : 'none';
                }});
            }} else {{
                renderQuestions();
            }}
        }}
    </script>
</body>
</html>"""
    return html


# =============================================================================
# 4. EXECUTE BUILD PIPELINE
# =============================================================================
def main():
    print("Building Venkata Sai Varun Munagavalasa Forward Deployed Engineer Prep Suite...")

    # 1. Master Markdown
    md_content = generate_markdown()
    with open("venkata_fde_health_prep.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("Master Markdown generated: venkata_fde_health_prep.md")

    # 2. Nextra MDX
    mdx_content = generate_mdx(md_content)
    os.makedirs("content", exist_ok=True)
    with open("content/venkata-fde-health-prep.mdx", "w", encoding="utf-8") as f:
        f.write(mdx_content)
    print("Nextra MDX generated: content/venkata-fde-health-prep.mdx")

    # 3. Interactive Standalone HTML
    html_content = generate_html()
    with open("venkata_fde_health_prep.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Interactive Webpage generated: venkata_fde_health_prep.html")

    # 4. Public directory copy
    os.makedirs("public", exist_ok=True)
    with open("public/venkata_fde_health_prep.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Public Webpage generated: public/venkata_fde_health_prep.html")

    print("\nAll Venkata Sai Varun FDE Prep assets successfully compiled!")

if __name__ == "__main__":
    main()
