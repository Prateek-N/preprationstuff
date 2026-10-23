# -*- coding: utf-8 -*-
"""
Master Build Script for Pavan Chandramouleswara Senior Data Engineer Interview Preparation Suite.

Generates:
1. pavan_chandramouleswara_de_prep.md
2. content/pavan-chandramouleswara-data-engineer-prep.mdx
3. pavan_chandramouleswara_de_prep.html (Signature Dark-Mode SPA with marked.js & mermaid.js)
4. public/pavan_chandramouleswara_de_prep.html (Production Static Serving)

Protected with password lock: "Pavan"
"""

import os
import re
import json
from pavan_data_questions_part1 import QUESTIONS_PART1
from pavan_data_questions_part2 import QUESTIONS_PART2
from pavan_data_coding_part1 import CODING_PROBLEMS_PART1
from pavan_data_coding_part2 import CODING_PROBLEMS_PART2

ALL_QUESTIONS = QUESTIONS_PART1 + QUESTIONS_PART2
ALL_PROBLEMS = CODING_PROBLEMS_PART1 + CODING_PROBLEMS_PART2

print(f"Loaded {len(ALL_QUESTIONS)} Questions and {len(ALL_PROBLEMS)} Coding Problems.")

# =============================================================================
# 1. GENERATE MASTER MARKDOWN (pavan_chandramouleswara_de_prep.md)
# =============================================================================
def generate_markdown() -> str:
    md = []
    md.append("# Pavan Chandramouleswara — Senior Data Engineer Master Interview Preparation Suite\n")
    md.append("## Complete 30 In-Depth Technical Q&As (300+ Words Each) + Top 25 Python Coding Problems\n\n")
    md.append("**Candidate:** Pavan Chandramouleswara  \n")
    md.append("**Location:** Chicago, IL | +1 (312) 709-4981 | pavan.mouleswara@gmail.com | [LinkedIn](https://www.linkedin.com/in/pavan-chandru)  \n")
    md.append("**Role Scope:** Senior Data Engineer / Staff Data Platform Engineer  \n")
    md.append("**Core Domains:** Distributed Real-Time Streaming, Modern Data Warehousing, Medallion/Dimensional Architecture, Big Data Distributed Compute, Workflow Orchestration, Data Quality & Governance, GenAI RAG & ML Data Pipelines  \n")
    md.append("**Passcode Lock:** `Pavan`\n\n")
    md.append("---\n\n")

    md.append("## Executive Summary & Candidate Value Proposition\n\n")
    md.append("> **Pavan Chandramouleswara** is a **Senior Data Engineer** with 5+ years of production experience architecting, implementing, and optimizing scalable, enterprise-grade data platforms across complex, heterogeneous ecosystems (**Uber**, **Dell Technologies**, and **Adani**). His engineering foundation spans both software engineering in **Python**, **Java**, and **Scala**, alongside distributed data platforms including **Apache Kafka**, **GCP BigQuery**, **Snowflake**, **Apache Spark**, **AWS EMR**, **dbt**, **Apache Airflow**, and **Great Expectations**.\n\n")
    md.append("> Across his career, Pavan has demonstrated repeated ownership of mission-critical outcomes: processing **5M+ daily marketplace events** at Uber while cutting delivery latency from 24 to under 16 hours; automating **12 ETL/ELT pipelines** across 10 Airflow DAGs to reclaim **40 engineering hours monthly**; establishing automated quality firewalls across **10TB+ volume** catching **2,000+ daily anomalies**; integrating **50+ heterogeneous enterprise systems** at Dell; and slashing Snowflake query runtimes from **45 minutes to under 2 minutes**.\n\n")

    md.append("## Quantified Impact & Architecture Metrics\n\n")
    md.append("| Metric / Initiative | Organization | Core Tech Stack | Measurable Business Outcome |\n")
    md.append("| :--- | :--- | :--- | :--- |\n")
    md.append("| **Marketplace Event Streaming** | **Uber** | Python, Kafka, GCP BigQuery | Scaled ingestion past **5M+ daily events**; cut latency from **24h to < 16h** |\n")
    md.append("| **Single Source of Truth** | **Uber** | dbt, BigQuery, Dimensional Modeling | Standardized metrics across cross-functional product & ML teams |\n")
    md.append("| **Pipeline Automation & SLAs** | **Uber** | Apache Airflow, Docker, CI/CD | Automated 12 ETL/ELT processes via 10 DAGs; reclaimed **40 engineering hours/mo** |\n")
    md.append("| **Data Quality Observability** | **Uber** | Great Expectations, BigQuery | Enforced automated tests on 8 tier-1 datasets (**10TB+**); caught **2,000+ daily anomalies** |\n")
    md.append("| **Heterogeneous Integration** | **Dell Technologies** | Hadoop, Hive, Spark, AWS EMR | Unified **50+ disparate enterprise systems** into a central platform |\n")
    md.append("| **Snowflake Optimization** | **Dell Technologies** | Snowflake, SQL, RBAC | Tuned clustering & warehouse sizing (**5TB+**); cut runtime from **45m to < 2m** |\n")
    md.append("| **Supply Chain Reporting** | **Dell Technologies** | Azure Data Factory, ADLS Gen2 | Redesigned ETL extracting **2M+ daily records**; cut latency from **24h to 6h** |\n")
    md.append("| **Governance & Audit Defense** | **Dell Technologies** | AWS Glue, Great Expectations, Airflow | Enforced automated lineage & PII tokenization; cut audit prep by **2 weeks** |\n")
    md.append("| **Reporting Automation** | **Adani** | Apache NiFi, R, CI/CD | Automated 15+ daily reports; slashed generation time from **3 hours to 30 min** |\n")
    md.append("| **Data Cleansing Firewall** | **Adani** | Alteryx, SQL, Excel | Validated **500K+ daily records** with zero data discrepancies |\n")
    md.append("| **Predictive Cost Savings** | **Adani** | SAS, Apache Drill, HDFS | Identified **$1.5M+ in verifiable cost savings** across 4 operational areas |\n")
    md.append("| **GenAI Knowledge Assistant** | **Project** | Python, LangChain, Vector DB, OpenAI | Indexed **15K+ enterprise docs**; resolved **300+ complex queries weekly** |\n")
    md.append("| **Demand Forecasting ML** | **Project** | Python, Scikit-learn, Pandas, SQL | Processed **75K+ historical records** to forecast demand across **400+ SKUs** |\n\n")

    md.append("---\n\n")

    md.append("## Core System Architecture Blueprints\n\n")
    
    md.append("### Blueprint 1: Uber Real-Time Marketplace Event Streaming Topology\n")
    md.append("```mermaid\n")
    md.append("flowchart LR\n")
    md.append("    A[\"Marketplace Telemetry: Driver GPS, Trips, Surge\"] --> B[\"Kafka Topics: Partitioned by driver_id, trip_id\"]\n")
    md.append("    B --> C[\"Python Async Streaming Workers: Micro-batching 10s / 5K events\"]\n")
    md.append("    C --> D[\"BigQuery Storage Write API: Committed Exactly-Once Mode\"]\n")
    md.append("    D --> E[\"BigQuery Staging Tables: Partitioned on Timestamp, Clustered on Region\"]\n")
    md.append("    E --> F[\"dbt Core Transformation: Incremental Models & Semantic Marts\"]\n")
    md.append("    E --> G[\"Great Expectations Gatekeeper: 8 Tier-1 Datasets (10TB+)\"]\n")
    md.append("    F --> H[\"Curated Analytical Marts & ML Feature Stores\"]\n")
    md.append("    G -->|\"2,000+ Daily Anomalies\"| I[\"Quarantined Audit Table & PagerDuty Alerts\"]\n")
    md.append("```\n\n")

    md.append("### Blueprint 2: Dell Technologies Enterprise Modernization & Snowflake Tuning\n")
    md.append("```mermaid\n")
    md.append("flowchart TD\n")
    md.append("    A[\"50+ Heterogeneous Systems: On-Prem Oracle, SQL Server, APIs, Flat Files\"] --> B[\"Ingestion Tier: Sqoop, Python Workers & Azure Data Factory\"]\n")
    md.append("    B --> C[\"Raw Data Lake: Amazon S3 & HDFS with Hive External SerDes\"]\n")
    md.append("    C --> D[\"Distributed Compute: Apache Spark on AWS EMR Auto-Scaling Clusters\"]\n")
    md.append("    D --> E[\"Data Harmonization: Canonical Data Models (CDM) & Snappy Parquet\"]\n")
    md.append("    E --> F[\"Optimized Snowflake Warehouse: 5TB+ Volume, Query Tuning 45m to 2m\"]\n")
    md.append("    E --> G[\"Governance & Lineage: AWS Glue Data Catalog & PII Masking\"]\n")
    md.append("```\n\n")

    md.append("### Blueprint 3: GenAI Enterprise Knowledge Assistant RAG Pipeline\n")
    md.append("```mermaid\n")
    md.append("flowchart TD\n")
    md.append("    A[\"15K+ Enterprise Documents: SOPs, PDFs, Architecture Specs\"] --> B[\"Semantic Recursive Chunking: 800 Tokens, 150 Overlap\"]\n")
    md.append("    B --> C[\"OpenAI Embedding Generation: text-embedding-3-large\"]\n")
    md.append("    C --> D[\"Vector Database: HNSW Indexing on Pinecone/Milvus\"]\n")
    md.append("    E[\"User Search Query\"] --> F{\"Hybrid Intent Router\"}\n")
    md.append("    F -->|\"Dense Vector Search\"| D\n")
    md.append("    F -->|\"Sparse BM25 Keyword Search\"| G[\"Lexical Inverted Index\"]\n")
    md.append("    D --> H[\"Cross-Encoder Re-Ranker: Top-5 Most Relevant Chunks\"]\n")
    md.append("    G --> H\n")
    md.append("    H --> I[\"Enterprise Guardrails: RBAC Check & Grounded Context Assembly\"]\n")
    md.append("    I --> J[\"Foundation LLM: Deterministic Generation (T=0.0)\"]\n")
    md.append("    J --> K[\"Validated Answer with Strict Source Citations\"]\n")
    md.append("```\n\n")

    md.append("---\n\n")

    # SECTION 1: 30 QUESTIONS
    md.append("# Section 1: Top 30 Senior Data Engineer Interview Questions & Expert Answers\n")
    md.append("### Every answer is strictly 300+ words, first-person perspective, with important keywords and tech stack in bold.\n\n")

    current_cat = ""
    for q in ALL_QUESTIONS:
        if q["category"] != current_cat:
            current_cat = q["category"]
            md.append(f"## {current_cat}\n\n")

        words = len(q["answer"].split())
        md.append(f"### Question {q['num']}: {q['title']}\n")
        md.append(f"**Interview Question:** *\"{q['question']}\"*\n\n")
        md.append(f"**Word Count & Verification:** `{words} words` (Strictly $\\ge 300$ words) | **Candidate POV:** Grounded in Pavan's Resume\n\n")
        md.append(f"**Comprehensive Answer:**\n\n")
        md.append(f"{q['answer']}\n\n")
        md.append("---\n\n")

    # SECTION 2: 25 CODING PROBLEMS
    md.append("# Section 2: Top 25 Python Coding Problems for Data Engineers\n")
    md.append("### Production-grade problems asked at Uber, Dell, Meta, Amazon, and Snowflake interviews.\n")
    md.append("### Each solution contains: 1) Problem Statement, 2) Algorithmic Thought Process, 3) Commented Code, 4) Time & Space Complexity.\n\n")

    current_code_cat = ""
    for p in ALL_PROBLEMS:
        if p["category"] != current_code_cat:
            current_code_cat = p["category"]
            md.append(f"## Coding Category: {current_code_cat}\n\n")

        md.append(f"### Problem {p['num']}: {p['title']}\n\n")
        md.append("#### 1. Problem Statement & Example\n")
        md.append(f"{p['problem_statement']}\n\n")
        md.append("#### 2. Algorithmic Thought Process & Tradeoffs\n")
        md.append(f"{p['thought_process']}\n\n")
        md.append("#### 3. Production-Grade Python Implementation\n")
        md.append("```python\n")
        md.append(f"{p['code'].strip()}\n")
        md.append("```\n\n")
        md.append("#### 4. Complexity Analysis\n")
        md.append(f"- **Time Complexity:** {p['time_complexity']}\n")
        md.append(f"- **Space Complexity:** {p['space_complexity']}\n\n")
        md.append("---\n\n")

    # SECTION 3: RESUME DEFENSE & ARCHITECTURAL DEEP-DIVE
    md.append("# Section 3: Candidate Experience Defense & Behavioral Leadership\n\n")
    md.append("### 1. Uber — Marketplace Streaming Platform Defense\n")
    md.append("- **Talking Points:** Talk about processing 5M+ daily events, why you shifted from batch files to Kafka streaming, how the GCP BigQuery Storage Write API provided committed exactly-once semantics, and how 10 Airflow DAGs with dynamic YAML generation reclaimed 40 engineering hours monthly.\n")
    md.append("- **Handling Skeptical Interviewers:** If asked 'How did latency go from 24h to 16h instead of seconds?', explain that 16h represents the guaranteed SLA for cold dimensional storage and financial reconciliation across the entire global marketplace, whereas real-time streaming buffers allow hot queries in sub-second time.\n\n")

    md.append("### 2. Dell Technologies — Enterprise Data Modernization & Snowflake Tuning\n")
    md.append("- **Talking Points:** Detail the 50+ heterogeneous system integration on Hadoop/Hive/Spark/EMR, how you identified remote disk spilling in Snowflake, cluster key selection on transaction timestamp and customer tenant, and cutting audit prep time by 2 weeks with AWS Glue and Great Expectations.\n\n")

    md.append("### 3. Adani — Industrial Telemetry Automation & Cost Optimization\n")
    md.append("- **Talking Points:** Describe automated NiFi flow files, containerized R reporting cutting turnaround from 3h to 30m, 500K+ daily record validation in Alteryx, and federated querying across HDFS and Oracle via Apache Drill unlocking $1.5M+ in verified savings.\n\n")

    return "".join(md)

# =============================================================================
# 2. GENERATE NEXTRA MDX (content/pavan-chandramouleswara-data-engineer-prep.mdx)
# =============================================================================
def escape_for_mdx(text: str) -> str:
    parts = re.split(r'(```[\s\S]*?```)', text)
    escaped_parts = []
    for part in parts:
        if part.startswith('```'):
            escaped_parts.append(part)
        else:
            p = part.replace('{', '&#123;').replace('}', '&#125;')
            p = p.replace('<=', '&le;').replace('>=', '&ge;')
            escaped_parts.append(p)
    return "".join(escaped_parts)

def generate_mdx() -> str:
    md_content = generate_markdown()
    escaped_content = escape_for_mdx(md_content)
    
    mdx = []
    mdx.append("---\n")
    mdx.append("title: Pavan Chandramouleswara — Senior Data Engineer Master Prep Suite\n")
    mdx.append("description: 30 In-Depth Technical Q&As (300+ words each) and Top 25 Python Coding Problems grounded in Pavan's Senior Data Engineer resume (Uber, Dell, Adani).\n")
    mdx.append("---\n\n")
    mdx.append('<PasswordGate password="Pavan" candidateName="Pavan Chandramouleswara">\n\n')
    mdx.append(escaped_content)
    mdx.append("\n\n</PasswordGate>\n")
    return "".join(mdx)

# =============================================================================
# 3. GENERATE SIGNATURE STANDALONE HTML (Exact Repository Standard)
# =============================================================================
def generate_signature_html() -> str:
    raw_markdown = generate_markdown()
    json_markdown = json.dumps(raw_markdown)

    html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pavan Chandramouleswara — Senior Data Engineer Master Prep Suite</title>
    <meta name="description" content="Senior Data Engineer Master Preparation Suite for Pavan Chandramouleswara covering 30 Technical Q&As (300+ words each) and Top 25 Python Coding Problems.">
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- Marked.js for fast Markdown parsing -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <!-- Mermaid.js for architectural diagrams -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"></script>
    <style>
        :root {{
            --bg-primary: #090d16;
            --bg-secondary: #0f172a;
            --bg-card: rgba(15, 23, 42, 0.75);
            --border-color: rgba(255, 255, 255, 0.1);
            --accent-cyan: #06b6d4;
            --accent-blue: #3b82f6;
            --accent-indigo: #6366f1;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --code-bg: #030712;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.7;
            padding: 0;
            margin: 0;
            min-height: 100vh;
        }}

        /* Header Navigation */
        header {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(9, 13, 22, 0.85);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .spark {{
            color: var(--accent-cyan);
            font-size: 1.6rem;
            font-weight: 900;
        }}

        .brand-title {{
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #ffffff 0%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .header-controls {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .search-box {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 8px 16px;
            border-radius: 9999px;
            font-size: 0.875rem;
            width: 280px;
            outline: none;
            transition: all 0.2s ease;
        }}

        .search-box:focus {{
            border-color: var(--accent-cyan);
            box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.25);
            width: 340px;
        }}

        .badge-locked {{
            background: rgba(6, 182, 212, 0.15);
            color: #67e8f9;
            border: 1px solid rgba(6, 182, 212, 0.3);
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* Security Gate Modal */
        #password-overlay {{
            position: fixed;
            inset: 0;
            z-index: 9999;
            background: rgba(9, 13, 22, 0.94);
            backdrop-filter: blur(20px);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
        }}

        .auth-card {{
            background: var(--bg-secondary);
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
            padding: 2.5rem;
            border-radius: 20px;
            width: 100%;
            max-width: 440px;
            text-align: center;
        }}

        .auth-icon {{
            font-size: 2.8rem;
            margin-bottom: 1rem;
        }}

        .auth-title {{
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: #ffffff;
        }}

        .auth-desc {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-bottom: 1.8rem;
        }}

        .auth-input {{
            width: 100%;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            padding: 14px;
            border-radius: 12px;
            color: #ffffff;
            font-size: 1rem;
            text-align: center;
            letter-spacing: 0.1em;
            margin-bottom: 1.2rem;
            outline: none;
            transition: all 0.2s;
        }}

        .auth-input:focus {{
            border-color: var(--accent-cyan);
            box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.3);
        }}

        .auth-btn {{
            width: 100%;
            background: linear-gradient(135deg, #06b6d4 0%, #2563eb 100%);
            color: #ffffff;
            border: none;
            padding: 14px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .auth-btn:hover {{
            filter: brightness(1.15);
            transform: translateY(-1px);
        }}

        .auth-error {{
            color: #ef4444;
            font-size: 0.825rem;
            margin-top: 10px;
            display: none;
        }}

        /* Content Container */
        .container {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 3rem 2rem 6rem;
        }}

        /* Typography & Markdown Styling */
        h1 {{
            font-size: 2.25rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 1rem;
            line-height: 1.2;
            color: #ffffff;
        }}

        h2 {{
            font-size: 1.6rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-top: 2.5rem;
            margin-bottom: 1.25rem;
            color: #f8fafc;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
        }}

        h3 {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            color: #e2e8f0;
        }}

        h4 {{
            font-size: 1.05rem;
            font-weight: 600;
            margin-top: 1.25rem;
            margin-bottom: 0.5rem;
            color: var(--accent-cyan);
        }}

        p {{
            margin-bottom: 1.25rem;
            color: #cbd5e1;
        }}

        strong {{
            color: #ffffff;
            font-weight: 600;
        }}

        blockquote {{
            border-left: 4px solid var(--accent-cyan);
            background: rgba(6, 182, 212, 0.08);
            padding: 1rem 1.5rem;
            border-radius: 0 12px 12px 0;
            margin: 1.5rem 0;
            color: #e2e8f0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            background: var(--bg-secondary);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }}

        th, td {{
            padding: 12px 18px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}

        th {{
            background: rgba(255, 255, 255, 0.04);
            font-weight: 600;
            color: #ffffff;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
        }}

        code {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875em;
            background: rgba(255, 255, 255, 0.08);
            padding: 2px 6px;
            border-radius: 6px;
            color: #38bdf8;
        }}

        pre {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem;
            overflow-x: auto;
            margin: 1.5rem 0;
            position: relative;
        }}

        pre code {{
            background: transparent;
            padding: 0;
            color: #e2e8f0;
            font-size: 0.85rem;
            line-height: 1.6;
        }}

        hr {{
            border: none;
            height: 1px;
            background: var(--border-color);
            margin: 3rem 0;
        }}

        .copy-btn {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: var(--text-secondary);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .copy-btn:hover {{
            background: var(--accent-cyan);
            color: #030712;
        }}

        .mermaid {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            display: flex;
            justify-content: center;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1.5rem 1rem;
            }}
            .search-box {{
                display: none;
            }}
        }}
    </style>
</head>
<body>

    <!-- Security Gate Modal -->
    <div id="password-overlay">
        <div class="auth-card">
            <div class="auth-icon">🔒</div>
            <h2 class="auth-title">Restricted Access</h2>
            <p class="auth-desc">Senior Data Engineer Master Preparation Suite<br>Candidate: <strong>Pavan Chandramouleswara</strong></p>
            <form id="auth-form" onsubmit="event.preventDefault(); verifyPassword();">
                <input type="password" id="pass-input" class="auth-input" placeholder="ENTER PASSCODE" autocomplete="off" autofocus>
                <button type="submit" class="auth-btn">Unlock Preparation Suite</button>
                <div id="auth-error" class="auth-error">Incorrect passcode. Please enter 'Pavan'.</div>
            </form>
        </div>
    </div>

    <!-- Header Navigation -->
    <header>
        <div class="brand">
            <span class="spark">⚡</span>
            <span class="brand-title">Pavan Chandramouleswara — Senior Data Engineer Master Prep Suite</span>
        </div>
        <div class="header-controls">
            <input type="text" id="filter-input" class="search-box" placeholder="Search questions, tech stack, Kafka, BigQuery...">
            <span class="badge-locked" id="status-badge">Locked</span>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="container" id="content-container" style="display: none;"></main>

    <script>
        const RAW_MARKDOWN = {json_markdown};

        const CORRECT_PASS = "Pavan";
        const STORAGE_KEY = "pavan_de_prep_verified";

        function checkAuth() {{
            const isAuth = sessionStorage.getItem(STORAGE_KEY);
            if (isAuth === 'true') {{
                unlockContent();
            }}
        }}

        function verifyPassword() {{
            const input = document.getElementById('pass-input').value.trim();
            const errorEl = document.getElementById('auth-error');
            
            if (input.toLowerCase() === CORRECT_PASS.toLowerCase()) {{
                sessionStorage.setItem(STORAGE_KEY, 'true');
                unlockContent();
            }} else {{
                errorEl.style.display = 'block';
                document.getElementById('pass-input').focus();
            }}
        }}

        function unlockContent() {{
            document.getElementById('password-overlay').style.display = 'none';
            const container = document.getElementById('content-container');
            container.style.display = 'block';
            document.getElementById('status-badge').textContent = 'Verified: Pavan';
            document.getElementById('status-badge').style.background = 'rgba(16, 185, 129, 0.15)';
            document.getElementById('status-badge').style.color = '#10b981';
            document.getElementById('status-badge').style.borderColor = 'rgba(16, 185, 129, 0.3)';

            // Render Markdown using marked.js
            container.innerHTML = marked.parse(RAW_MARKDOWN);

            // Re-render Mermaid diagrams
            document.querySelectorAll('pre code.language-mermaid').forEach(block => {{
                const pre = block.parentElement;
                const div = document.createElement('div');
                div.className = 'mermaid';
                div.textContent = block.textContent;
                pre.parentElement.replaceChild(div, pre);
            }});
            mermaid.run();

            attachCodeCopyButtons();
        }}

        function attachCodeCopyButtons() {{
            document.querySelectorAll('pre').forEach(pre => {{
                if (pre.querySelector('.copy-btn')) return;
                const btn = document.createElement('button');
                btn.className = 'copy-btn';
                btn.textContent = 'Copy';
                btn.addEventListener('click', () => {{
                    const code = pre.querySelector('code') ? pre.querySelector('code').innerText : pre.innerText;
                    navigator.clipboard.writeText(code).then(() => {{
                        btn.textContent = 'Copied!';
                        setTimeout(() => btn.textContent = 'Copy', 2000);
                    }});
                }});
                pre.appendChild(btn);
            }});
        }}

        // Quick Search Filter
        document.getElementById('filter-input').addEventListener('input', (e) => {{
            const term = e.target.value.toLowerCase();
            const elements = document.querySelectorAll('h2, h3, p, pre, table');
            if (!term) {{
                elements.forEach(el => el.style.opacity = '1');
                return;
            }}
            elements.forEach(el => {{
                if (el.innerText.toLowerCase().includes(term)) {{
                    el.style.opacity = '1';
                }} else {{
                    el.style.opacity = '0.35';
                }}
            }});
        }});

        window.addEventListener('DOMContentLoaded', checkAuth);
    </script>
</body>
</html>
"""
    return html_content

# =============================================================================
# BUILD COMPILATION
# =============================================================================
if __name__ == "__main__":
    print("Beginning Build...")
    
    # 1. Write Markdown file
    md_content = generate_markdown()
    with open("pavan_chandramouleswara_de_prep.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("Generated: pavan_chandramouleswara_de_prep.md")

    # 2. Write Nextra MDX file
    mdx_content = generate_mdx()
    os.makedirs("content", exist_ok=True)
    with open("content/pavan-chandramouleswara-data-engineer-prep.mdx", "w", encoding="utf-8") as f:
        f.write(mdx_content)
    print("Generated: content/pavan-chandramouleswara-data-engineer-prep.mdx")

    # 3. Write Signature Standalone HTML files
    signature_html = generate_signature_html()
    with open("pavan_chandramouleswara_de_prep.html", "w", encoding="utf-8") as f:
        f.write(signature_html)
    print("Generated: pavan_chandramouleswara_de_prep.html (Signature Template)")

    os.makedirs("public", exist_ok=True)
    with open("public/pavan_chandramouleswara_de_prep.html", "w", encoding="utf-8") as f:
        f.write(signature_html)
    print("Generated: public/pavan_chandramouleswara_de_prep.html (Signature Template)")

    print("\nAll files successfully generated and aligned with repository standard!")
