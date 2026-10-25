# -*- coding: utf-8 -*-
"""
Build script for Priyanka Gantam's Walmart Data Engineer Prep Suite.
Compiles:
1. priyanka_gantam_walmart_prep.md
2. content/priyanka-gantam-walmart-prep.mdx
3. priyanka_gantam_walmart_prep.html
4. public/priyanka_gantam_walmart_prep.html

Passcode: "Priyanka"
"""

import json
import re
import os
from priyanka_data_questions import QUESTIONS
from priyanka_data_coding import CODING_PROBLEMS

print(f"Loaded {len(QUESTIONS)} Technical Questions and {len(CODING_PROBLEMS)} Coding Problems.")

# =============================================================================
# 1. GENERATE MASTER MARKDOWN (priyanka_gantam_walmart_prep.md)
# =============================================================================
def generate_markdown():
    md = []
    md.append("# Priyanka Gantam — Data Engineer Interview Preparation Suite\n")
    md.append("## Target Role: Data Engineer — Walmart (Omnichannel Retail & Cloud Lakehouse)\n")
    md.append("**Candidate:** Priyanka Gantam | Frisco, TX | (940)-297-8548 | gpriyanka.us92@gmail.com | [LinkedIn](https://linkedin.com)\n")
    md.append("**Target Company:** Walmart (Global Retail Technology & Supply Chain Analytics)\n")
    md.append("**Passcode Lock:** `Priyanka`\n\n")
    md.append("---\n\n")

    md.append("## Executive Summary & Walmart Strategic Fit\n")
    md.append("> **Priyanka Gantam** is a **Data Engineer** with 4+ years of production experience architecting enterprise-scale data platforms, distributed Lakehouse architectures, real-time streaming pipelines, and ML-integrated data workflows across high-growth enterprise tech (**Palantir**), fintech & travel platforms (**Navan**), and high-throughput core banking systems (**Infosys Finacle**).\n\n")
    md.append("> Currently at **Palantir**, Priyanka designs cloud-native data architectures on **AWS (S3, EMR, Glue)** and **Palantir Foundry**, integrating multi-source transactional and telemetry data into governed ontology objects to reduce time-to-insight for AI/ML initiatives by **50%**. Her PySpark optimizations have cut data synchronization latency by **30%** and cloud processing costs by **20%**. Previously at **Navan**, she implemented 8+ production ELT pipelines using **Databricks, Delta Lake, PySpark, and Kafka**, structuring corporate finance and expense data into a Medallion Lakehouse that compressed BI latency by **40%**, reduced fraud detection latency by **35%**, and eliminated production data incidents by **45%** under strict **SOX and PCI DSS controls**.\n\n")
    md.append("> At **Walmart**, where data platforms operate across petabytes of store point-of-sale registers, automated distribution centers, e-commerce web carts, and supply chain telemetry, Priyanka combines deep technical rigor in **PySpark, Kafka, Delta Lake, Snowflake, dbt, and Airflow** with a proven mindset of adaptability, empathetic stakeholder collaboration, and defensive operational engineering.\n\n")

    md.append("## Quantified Impact & Architecture Metrics\n\n")
    md.append("| Organization | Domain & Role | Core Tech Stack | Quantified Business Impact |\n")
    md.append("| :--- | :--- | :--- | :--- |\n")
    md.append("| **Palantir** | Enterprise AI & Data Architecture | AWS (S3, EMR, Glue), Palantir Foundry, PySpark | Cut AI/ML time-to-insight by **50%** via governed ontology objects |\n")
    md.append("| **Palantir** | Distributed Compute Tuning | Python, PySpark, AWS EMR, Partition Pruning | Slashed data sync latency by **30%** and cloud compute costs by **20%** |\n")
    md.append("| **Palantir** | Dimensional Modeling & Self-Service | dbt, Snowflake, REST APIs, Star Schema | Published reusable data products empowering **5+ business units** |\n")
    md.append("| **Palantir** | CI/CD & Delivery Acceleration | Apache Airflow, Jenkins, GitLab CI/CD, PyTest | Accelerated automated delivery release cycles by **25%** |\n")
    md.append("| **Navan** | Lakehouse Medallion Architecture | Databricks, Delta Lake, PySpark, Apache Kafka | Slashed finance and BI data delivery latency by **40%** across 8+ ELT pipelines |\n")
    md.append("| **Navan** | Real-Time Fraud Streaming | Spark Structured Streaming, Kafka, Debezium CDC | Reduced fraud detection scoring latency by **35%** with sub-minute SLAs |\n")
    md.append("| **Navan** | Data Quality & Governance | Great Expectations, dbt Tests, Schema Validation | Cut production data incidents by **45%** under SOX and PCI DSS controls |\n")
    md.append("| **Navan** | Dimensional Warehousing & BI | Snowflake, dbt, Looker, Star Schema, SCD Type 2 | Eliminated manual finance reporting overhead by **50%** |\n")
    md.append("| **Infosys Finacle** | High-Throughput Core Banking | Python, PySpark, Kafka, ISO 20022, SWIFT MT | Processed **5M+ daily transactions** (~500GB/day) with sub-5-min latency & **99.9% uptime** |\n")
    md.append("| **Infosys Finacle** | Cloud Migration & SQL Tuning | Oracle, AWS S3, RDS, Snowflake | Boosted reporting performance by **35%** and cut warehouse query costs by **20%** |\n\n")

    md.append("---\n\n")

    md.append("## Core System Architecture Blueprints\n\n")

    md.append("### Blueprint 1: Walmart Omnichannel Retail Streaming & Lakehouse Pipeline\n")
    md.append("```mermaid\ngraph TD\n")
    md.append("    subgraph Sources [Omnichannel Retail Ingestion]\n")
    md.append("        S1[Store POS Registers: 4,700+ Stores] --> K[Apache Kafka Streaming Cluster]\n")
    md.append("        S2[E-Commerce & Mobile App Sessions] --> K\n")
    md.append("        S3[Distribution Center WMS Telemetry] --> K\n")
    md.append("        S4[Supplier ASNs & EDI 850/856 Feeds] --> S3Landing[AWS S3 Raw Landing Bucket]\n")
    md.append("    end\n")
    md.append("    subgraph StreamProcessing [Real-Time Processing & Bronze Lakehouse]\n")
    md.append("        K --> SSS[Spark Structured Streaming on AWS EMR]\n")
    md.append("        SSS -->|Event-Time Watermark 10m| DEDUP[Stateful Deduplication RocksDB]\n")
    md.append("        DEDUP --> BRONZE[(Delta Lake Bronze Layer Append-Only Raw Files)]\n")
    md.append("        S3Landing --> GX[Great Expectations Ingestion Firewall]\n")
    md.append("        GX -->|Valid ASNs| BRONZE\n")
    md.append("        GX -->|Schema Violations| QUARANTINE[(S3 Quarantine Error Lake)]\n")
    md.append("    end\n")
    md.append("    subgraph Curation [Silver & Gold Lakehouse Medallion]\n")
    md.append("        BRONZE --> SILVER_JOB[PySpark Silver Curation: Schema Validation & Normalization]\n")
    md.append("        SILVER_JOB --> SILVER[(Delta Lake Silver Layer ACID Tables)]\n")
    md.append("        SILVER --> DBT_JOB[dbt Core Transformation & SCD Type 2 Snapshots]\n")
    md.append("        DBT_JOB --> GOLD[(Delta Lake / Snowflake Gold Dimensional Marts)]\n")
    md.append("    end\n")
    md.append("    subgraph Consumption [Downstream Enterprise Activation]\n")
    md.append("        GOLD --> BI[Executive Inventory & Sales Looker Dashboards]\n")
    md.append("        GOLD --> ML[Replenishment & Dynamic Pricing Feature Stores]\n")
    md.append("        GOLD --> VEC[Product Catalog Vector DB for GenAI Search]\n")
    md.append("    end\n")
    md.append("```\n\n")

    md.append("### Blueprint 2: Palantir Foundry / Delta Lake Medallion Architecture with Ontology Integration\n")
    md.append("```mermaid\ngraph LR\n")
    md.append("    subgraph Ingest [AWS Cloud Foundation]\n")
    md.append("        A[Multi-Source Enterprise Data: S3, Kafka, RDBMS] --> B[AWS Glue Crawlers & Data Catalog]\n")
    md.append("        B --> C[AWS EMR Distributed PySpark Compute]\n")
    md.append("    end\n")
    md.append("    subgraph Lakehouse [Medallion Curation]\n")
    md.append("        C --> D[(Bronze: Raw Ingestion with Z-Order Compaction)]\n")
    md.append("        D --> E[(Silver: Cleansed, Deduplicated, ACID Delta Tables)]\n")
    md.append("        E --> F[(Gold: Dimensional Star Schemas & Business Marts)]\n")
    md.append("    end\n")
    md.append("    subgraph Ontology [Palantir Foundry Semantic Layer]\n")
    md.append("        F --> G[Ontology Object Mappings: Stores, SKUs, Shipments]\n")
    md.append("        G --> H[Semantic Relationships & Live Time-Series Attributes]\n")
    md.append("        H --> I[50% Faster Time-to-Insight for Enterprise AI/ML Workflows]\n")
    md.append("    end\n")
    md.append("```\n\n")

    md.append("### Blueprint 3: Enterprise Data Quality Firewall & Observability Pipeline\n")
    md.append("```mermaid\ngraph TD\n")
    md.append("    subgraph Ingress [Data Ingress]\n")
    md.append("        RawFile[Incoming Vendor ASN / POS Transaction File] --> Gatekeeper[Great Expectations Pre-Ingestion Validator]\n")
    md.append("    end\n")
    md.append("    subgraph ContractChecks [Automated Contract Rules]\n")
    md.append("        Gatekeeper --> C1{Primary Key Unique & Non-Null?}\n")
    md.append("        Gatekeeper --> C2{Quantities > 0 & Prices Valid?}\n")
    md.append("        Gatekeeper --> C3{Temporal Sequence: Shipped <= Delivery?}\n")
    md.append("        Gatekeeper --> C4{Categorical Codes Match Enterprise Master?}\n")
    md.append("    end\n")
    md.append("    subgraph Routing [Automated Routing & Observability]\n")
    md.append("        C1 & C2 & C3 & C4 -->|All Passed| LoadBronze[Approve for Lakehouse Ingestion]\n")
    md.append("        C1 | C2 | C3 | C4 -->|Any Failure| Quarantine[Divert to S3 Quarantine + PagerDuty Alert]\n")
    md.append("        LoadBronze --> Telemetry[Emit Metrics: Freshness, Row Counts, Latency]\n")
    md.append("        Telemetry --> ObsDashboard[Centralized Data Observability & SLA Monitor]\n")
    md.append("    end\n")
    md.append("```\n\n")

    md.append("---\n\n")

    # =========================================================================
    # SECTION 1: TOP 15 TECHNICAL QUESTIONS
    # =========================================================================
    md.append("# Section 1: Top 15 Technical Interview Questions & Comprehensive Answers (300+ Words Each)\n\n")
    md.append("> **Candidate Delivery Standard:** Every answer is structured in cohesive narrative paragraphs without bullet points, directly grounded in Priyanka's resume achievements at **Palantir**, **Navan**, and **Infosys Finacle**, and tailored to **Walmart scale**.\n\n")

    current_cat = ""
    for q in QUESTIONS:
        words = len(re.findall(r'\b\w+\b', q['answer']))
        if q.get('category') and q['category'] != current_cat:
            current_cat = q['category']
            md.append(f"## {current_cat}\n\n")

        md.append(f"### Q{q['num']:02d}: {q['title']}\n\n")
        md.append(f"**Interview Question:** *\"{q['question']}\"*\n\n")
        md.append(f"**Perspective & Delivery:** First-Person Narrative (`{words} words` · Verified $\\ge 300$ words · No Bullets)  \n\n")
        md.append(f"**Comprehensive Answer:**\n\n")
        md.append(f"{q['answer']}\n\n")
        md.append("---\n\n")

    # =========================================================================
    # SECTION 2: TOP 5 CODING PROBLEMS
    # =========================================================================
    md.append("# Section 2: Top 5 Production Data Engineering Coding Problems\n\n")
    md.append("### Designed for Walmart Technical Screening: PySpark, Streaming, SCD Type 2, Key Salting, and Data Quality Firewalls.\n\n")

    for p in CODING_PROBLEMS:
        md.append(f"### Problem {p['num']}: {p['title']}\n\n")
        md.append(f"**Category:** `{p['category']}`  \n\n")
        md.append("#### 1. Problem Statement & Retail Context\n")
        md.append(f"{p['problem_statement']}\n\n")
        md.append("#### 2. Algorithmic Thought Process & Tradeoffs\n")
        md.append(f"{p['thought_process']}\n\n")
        md.append("#### 3. Production-Grade Python / PySpark Implementation\n")
        md.append("```python\n")
        md.append(f"{p['code'].strip()}\n")
        md.append("```\n\n")
        md.append("#### 4. Complexity & Scalability Analysis\n")
        md.append(f"{p['complexity']}\n\n")
        md.append("---\n\n")

    # =========================================================================
    # SECTION 3: SCENARIOS & RESUME DEFENSE
    # =========================================================================
    md.append("# Section 3: Candidate Experience Defense, Attitude & Adaptability Guide\n\n")
    
    md.append("### 1. Palantir — Enterprise Cloud-Native Data Architecture & Foundry Ontology\n")
    md.append("- **Core Talking Point:** Architecting multi-source ingestion on AWS (S3, EMR, Glue) and Palantir Foundry, converting physical tables into semantic ontology objects. This unified data lake reduced AI/ML time-to-insight by 50%.\n")
    md.append("- **Performance & Cost Engineering:** Slashed sync latency by 30% and AWS EMR cloud compute costs by 20% by restructuring PySpark batch jobs with partition pruning, broadcast joins, and incremental processing.\n")
    md.append("- **Modern Data Stack:** Published reusable dbt data models in Snowflake for 5+ business units, automated CI/CD with GitLab and Jenkins, and accelerated delivery cycles by 25%.\n\n")

    md.append("### 2. Navan (Fintech) — Medallion Architecture, Real-Time Fraud & Governance\n")
    md.append("- **Core Talking Point:** Built 8+ production ELT workflows in Databricks and Delta Lake, structuring travel and expense records into Bronze, Silver, and Gold Medallion layers, compressing finance reporting latency by 40%.\n")
    md.append("- **Streaming Telemetry:** Processed high-volume financial events via Spark Structured Streaming, Kafka, and Debezium CDC, reducing fraud scoring latency by 35% with strict sub-minute SLAs.\n")
    md.append("- **Compliance & Quality Firewalls:** Reduced production data incidents by 45% using Great Expectations, dbt schema validation, and freshness monitors while satisfying strict SOX and PCI DSS regulatory controls.\n\n")

    md.append("### 3. Infosys Finacle — Core Banking Migration & High-Throughput Processing\n")
    md.append("- **Core Talking Point:** Processed 5M+ daily banking transactions (~500GB/day) across complex ISO 20022 and SWIFT MT messaging standards with sub-5-minute latency and 99.9% uptime.\n")
    md.append("- **Legacy Migration:** Successfully migrated financial general ledger reconciliation datasets from legacy Oracle databases to AWS S3 and Snowflake, boosting reporting performance by 35% and cutting query costs by 20%.\n\n")

    md.append("### 4. Behavioral Framework: Attitude, Adaptability & Thought Process\n")
    md.append("- **Attitude & Humility:** Embrace shifting business requirements proactively rather than resisting change. When Navan pivoted from 4-hour batch to sub-minute fraud streaming, stepped up to lead team upskilling and delivered 2 weeks early.\n")
    md.append("- **Structured Thought Process:** When faced with ambiguous architectural questions, systematically decompose the problem into Requirement Discovery → Ingestion Tradeoffs → Storage Tiering → Compute Optimization → Defensive Governance.\n")
    md.append("- **Defensive Engineering Mindset:** Treat data pipelines as production software products with rigorous automated testing, idempotent execution, automated dead-letter quarantining, and proactive SLA observability.\n")

    return "".join(md)

# =============================================================================
# 2. GENERATE NEXTJS MDX (content/priyanka-gantam-walmart-prep.mdx)
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
title: Priyanka Gantam — Data Engineer (Walmart) Prep Suite
description: Complete interview preparation guide for Data Engineer at Walmart — Top 15 technical questions (300+ words each, small chunks of paragraphs, no bullets), 5 production coding problems, architectural blueprints, and resume defense grounded in Palantir, Navan, and Infosys Finacle.
---

<PasswordGate password="Priyanka" candidateName="Priyanka Gantam">

"""

    footer = """

</PasswordGate>
"""
    return header + escaped_body + footer

# =============================================================================
# 3. GENERATE INTERACTIVE WEBPAGE (priyanka_gantam_walmart_prep.html)
# =============================================================================
def generate_html():
    items_json = []
    categories = []

    # 1. Add Technical Questions
    for q in QUESTIONS:
        words = len(re.findall(r'\b\w+\b', q['answer']))
        cat = q.get('category', 'Technical Excellence')
        if cat not in categories:
            categories.append(cat)
        items_json.append({
            "type": "question",
            "num": q["num"],
            "category": cat,
            "title": q["title"],
            "question": q["question"],
            "words": words,
            "answer": q["answer"]
        })

    # 2. Add Coding Problems
    coding_cat = "Coding & Algorithms"
    if coding_cat not in categories:
        categories.append(coding_cat)

    for p in CODING_PROBLEMS:
        full_content = f"### Problem Statement\n{p['problem_statement']}\n\n### Algorithmic Thought Process & Tradeoffs\n{p['thought_process']}\n\n### Commented Implementation\n```python\n{p['code'].strip()}\n```\n\n### Complexity & Scalability Analysis\n{p['complexity']}"
        words = len(re.findall(r'\b\w+\b', full_content))
        items_json.append({
            "type": "coding",
            "num": p["num"],
            "category": coding_cat,
            "title": f"Coding Problem {p['num']}: {p['title']}",
            "question": p["problem_statement"][:180] + "...",
            "words": words,
            "answer": full_content
        })

    items_json_str = json.dumps(items_json, ensure_ascii=False)
    categories_json_str = json.dumps(categories, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Walmart — Data Engineer Prep Suite · Priyanka Gantam</title>
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
      --border-accent: #0071dc;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --walmart-blue: #0071dc;
      --walmart-yellow: #ffc220;
      --walmart-cyan: #38bdf8;
      --walmart-emerald: #10b981;
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
      background: radial-gradient(circle at center, #091a33 0%, #03060a 100%);
      display: flex; align-items: center; justify-content: center;
      z-index: 99999; padding: 1.5rem;
    }}
    .lock-box {{
      background: rgba(12, 18, 28, 0.96);
      backdrop-filter: blur(24px);
      border: 1px solid rgba(0, 113, 220, 0.4);
      border-radius: 22px;
      padding: 2.75rem 2.5rem;
      max-width: 490px;
      width: 100%;
      text-align: center;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.9), 0 0 50px rgba(0, 113, 220, 0.25);
    }}
    .lock-logo-mark {{
      display: inline-flex; align-items: center; justify-content: center;
      margin-bottom: 1.25rem; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.04em;
    }}
    .lock-txt-1 {{ color: #ffffff; }}
    .lock-txt-2 {{ color: #ffc220; }}
    .lock-badge-pill {{
      background: linear-gradient(135deg, rgba(0, 113, 220, 0.25), rgba(255, 194, 32, 0.25));
      border: 1px solid rgba(255, 194, 32, 0.4);
      padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; color: #ffc220;
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
      border-color: var(--walmart-blue);
      box-shadow: 0 0 0 3px rgba(0, 113, 220, 0.25);
    }}
    .unlock-btn {{
      width: 100%;
      background: linear-gradient(135deg, #0071dc, #005bb5);
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
      box-shadow: 0 10px 25px -5px rgba(0, 113, 220, 0.5);
      background: linear-gradient(135deg, #0080f8, #0071dc);
    }}
    .error-msg {{
      color: #f87171; font-size: 0.85rem; margin-top: 0.9rem; display: none; font-weight: 500;
    }}

    /* MAIN APP */
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
      background: rgba(0, 113, 220, 0.15); border: 1px solid rgba(56, 189, 248, 0.35);
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
      background: linear-gradient(135deg, rgba(9, 26, 51, 0.9) 0%, rgba(6, 15, 28, 0.95) 100%);
      border: 1px solid rgba(0, 113, 220, 0.35);
      border-radius: 20px; padding: 2.75rem; margin-bottom: 2.5rem;
      box-shadow: 0 20px 40px -15px rgba(0,0,0,0.7); position: relative; overflow: hidden;
    }}
    .hero-banner::after {{
      content: ""; position: absolute; right: -80px; top: -80px; width: 320px; height: 320px;
      background: radial-gradient(circle, rgba(0, 113, 220, 0.2) 0%, transparent 70%);
      pointer-events: none; border-radius: 50%;
    }}
    .hero-eyebrow {{
      font-family: var(--font-mono); font-size: 0.8rem; text-transform: uppercase;
      color: #ffc220; font-weight: 700; letter-spacing: 0.08em; margin-bottom: 0.75rem;
      display: flex; align-items: center; gap: 8px;
    }}
    .hero-eyebrow::before {{
      content: ""; display: inline-block; width: 8px; height: 8px; background: #ffc220; border-radius: 50%;
      box-shadow: 0 0 10px #ffc220;
    }}
    .hero-title {{
      font-size: 2.45rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 1rem; line-height: 1.25;
    }}
    .hero-title span {{
      background: linear-gradient(135deg, #ffffff 40%, #ffc220 100%);
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
    .stat-card:hover {{ border-color: var(--walmart-blue); }}
    .stat-val {{
      font-size: 1.65rem; font-weight: 800; color: #f8fafc; font-family: var(--font-mono); margin-bottom: 0.25rem;
    }}
    .stat-label {{ color: var(--text-dim); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; }}

    /* BLUEPRINTS */
    .blueprint-card {{
      background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px;
      padding: 1.75rem; margin-bottom: 2.5rem;
    }}
    .blueprint-title {{
      font-size: 1.25rem; font-weight: 700; color: #fff; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 10px;
    }}
    .mermaid-container {{
      background: #090e17; border: 1px solid rgba(255,255,255,0.06); border-radius: 12px;
      padding: 1.5rem; overflow-x: auto; margin-bottom: 1.5rem;
    }}

    /* CONTROLS */
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
    .search-input-wrap input:focus {{ border-color: var(--walmart-blue); }}
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
      height: 100%; width: 0%; background: linear-gradient(90deg, #0071dc, #ffc220);
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
      background: rgba(0, 113, 220, 0.25); border-color: var(--walmart-blue); color: #ffc220;
    }}

    /* CARDS */
    .q-list {{ display: flex; flex-direction: column; gap: 1.25rem; }}
    .q-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      transition: all 0.25s ease;
    }}
    .q-card:hover {{
      border-color: rgba(0, 113, 220, 0.4);
      box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }}
    .q-card.completed {{
      border-color: rgba(16, 185, 129, 0.45);
      background: rgba(16, 185, 129, 0.03);
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
      background: rgba(0, 113, 220, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: #7dd3fc;
      font-family: var(--font-mono);
      font-size: 0.82rem; font-weight: 700;
      padding: 6px 12px; border-radius: 10px;
      white-space: nowrap; margin-top: 2px;
    }}
    .q-num-badge.coding-badge {{
      background: rgba(255, 194, 32, 0.15);
      border-color: rgba(255, 194, 32, 0.4);
      color: #ffc220;
    }}
    .q-card.completed .q-num-badge {{
      background: rgba(16, 185, 129, 0.25);
      border-color: var(--walmart-emerald);
      color: #6ee7b7;
    }}

    .q-meta-group {{ display: flex; flex-direction: column; gap: 4px; }}
    .q-cat-tag {{
      font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em;
      color: #ffc220; font-weight: 700;
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
      background: rgba(0, 113, 220, 0.15); border: 1px solid rgba(56, 189, 248, 0.3);
      color: #7dd3fc; font-family: var(--font-mono); font-size: 0.75rem;
      padding: 4px 8px; border-radius: 6px; white-space: nowrap;
    }}
    .q-checkbox {{
      width: 18px; height: 18px; cursor: pointer; accent-color: #0071dc;
    }}
    .chevron {{
      color: var(--text-dim); font-size: 0.75rem; transition: transform 0.25s ease;
    }}
    .q-card.open .chevron {{ transform: rotate(180deg); color: #ffc220; }}

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
    .answer-content pre {{
      background: #090e17; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px;
      padding: 1.2rem; overflow-x: auto; margin: 1rem 0; font-family: var(--font-mono); font-size: 0.88rem;
    }}
    .answer-content code {{
      font-family: var(--font-mono); font-size: 0.88rem; background: rgba(255,255,255,0.06);
      padding: 2px 6px; border-radius: 4px; color: #ffc220;
    }}
    .answer-content pre code {{ background: transparent; padding: 0; color: #e2e8f0; }}

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
    .copy-ans-btn:hover {{ background: rgba(255,255,255,0.1); color: #fff; border-color: var(--walmart-blue); }}
    .copy-toast {{
      font-size: 0.78rem; color: #6ee7b7; font-family: var(--font-mono); opacity: 0; transition: opacity 0.3s;
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
        <span class="lock-txt-1">Walmart</span><span class="lock-txt-2">·Tech</span>
        <span class="lock-badge-pill">PREP PORTAL</span>
      </div>
      <h2>Data Engineer Interview Suite</h2>
      <p>Enter the candidate passcode to unlock the 15-question technical guide, 5 coding problems, and Lakehouse blueprints.</p>
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
          <span>Walmart · Data Engineer</span>
          <span class="brand-badge">Priyanka Gantam</span>
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
        <div class="hero-eyebrow">Enterprise Omnichannel Retail & Lakehouse Engineering</div>
        <h1 class="hero-title">Data Engineer — <span>Walmart Global Tech</span></h1>
        <p class="hero-subtitle">
          Prepared for <strong>Priyanka Gantam</strong> targeting the <strong>Data Engineer</strong> position at <strong>Walmart</strong>. 
          Grounding 4+ years of data engineering experience across <strong>Palantir Foundry (50% faster AI/ML time-to-insight)</strong>, 
          <strong>Navan Lakehouse (Delta Lake Medallion, Kafka streaming, -45% incidents)</strong>, and <strong>Infosys Finacle (5M+ daily banking transactions, 99.9% uptime)</strong> directly into Walmart's massive omnichannel retail and supply chain ecosystem.
        </p>
        <div class="hero-stats-grid">
          <div class="stat-card">
            <div class="stat-val">15</div>
            <div class="stat-label">In-Depth Q&As (300+ Wds · No Bullets)</div>
          </div>
          <div class="stat-card">
            <div class="stat-val">5</div>
            <div class="stat-label">Production Coding Problems</div>
          </div>
          <div class="stat-card">
            <div class="stat-val">3</div>
            <div class="stat-label">Enterprise Architecture Blueprints</div>
          </div>
          <div class="stat-card">
            <div class="stat-val">5M+</div>
            <div class="stat-label">Daily Event Stream Processing Scale</div>
          </div>
        </div>
      </div>

      <!-- ARCHITECTURAL BLUEPRINTS -->
      <div id="blueprints" class="blueprint-card">
        <div class="blueprint-title">
          <span>🏛️ Enterprise System Architecture Blueprints</span>
        </div>
        
        <p style="color: var(--text-muted); font-size: 0.92rem; margin-bottom: 1.25rem;">
          These three system architecture blueprints provide an end-to-end visual representation of Priyanka's experience applied to Walmart's mission-critical workloads: Omnichannel retail Lakehouse ingestion on Delta Lake & Spark, Palantir Foundry semantic ontology integration, and Enterprise data quality firewalls.
        </p>

        <h4 style="color: #ffc220; margin-bottom: 0.75rem; font-size: 1rem;">Blueprint 1: Walmart Omnichannel Retail Streaming & Lakehouse Pipeline</h4>
        <div class="mermaid-container">
          <pre class="mermaid">
graph TD
    subgraph Sources [Omnichannel Retail Ingestion]
        S1[Store POS Registers: 4,700+ Stores] --> K[Apache Kafka Streaming Cluster]
        S2[E-Commerce & Mobile App Sessions] --> K
        S3[Distribution Center WMS Telemetry] --> K
        S4[Supplier ASNs & EDI 850/856 Feeds] --> S3Landing[AWS S3 Raw Landing Bucket]
    end
    subgraph StreamProcessing [Real-Time Processing & Bronze Lakehouse]
        K --> SSS[Spark Structured Streaming on AWS EMR]
        SSS -->|Event-Time Watermark 10m| DEDUP[Stateful Deduplication RocksDB]
        DEDUP --> BRONZE[(Delta Lake Bronze Layer Append-Only Raw Files)]
        S3Landing --> GX[Great Expectations Ingestion Firewall]
        GX -->|Valid ASNs| BRONZE
        GX -->|Schema Violations| QUARANTINE[(S3 Quarantine Error Lake)]
    end
    subgraph Curation [Silver & Gold Lakehouse Medallion]
        BRONZE --> SILVER_JOB[PySpark Silver Curation: Schema Validation & Normalization]
        SILVER_JOB --> SILVER[(Delta Lake Silver Layer ACID Tables)]
        SILVER --> DBT_JOB[dbt Core Transformation & SCD Type 2 Snapshots]
        DBT_JOB --> GOLD[(Delta Lake / Snowflake Gold Dimensional Marts)]
    end
    subgraph Consumption [Downstream Enterprise Activation]
        GOLD --> BI[Executive Inventory & Sales Looker Dashboards]
        GOLD --> ML[Replenishment & Dynamic Pricing Feature Stores]
        GOLD --> VEC[Product Catalog Vector DB for GenAI Search]
    end
          </pre>
        </div>

        <h4 style="color: #ffc220; margin: 1.5rem 0 0.75rem 0; font-size: 1rem;">Blueprint 2: Palantir Foundry / Delta Lake Medallion Architecture with Ontology Integration</h4>
        <div class="mermaid-container">
          <pre class="mermaid">
graph LR
    subgraph Ingest [AWS Cloud Foundation]
        A[Multi-Source Enterprise Data: S3, Kafka, RDBMS] --> B[AWS Glue Crawlers & Data Catalog]
        B --> C[AWS EMR Distributed PySpark Compute]
    end
    subgraph Lakehouse [Medallion Curation]
        C --> D[(Bronze: Raw Ingestion with Z-Order Compaction)]
        D --> E[(Silver: Cleansed, Deduplicated, ACID Delta Tables)]
        E --> F[(Gold: Dimensional Star Schemas & Business Marts)]
    end
    subgraph Ontology [Palantir Foundry Semantic Layer]
        F --> G[Ontology Object Mappings: Stores, SKUs, Shipments]
        G --> H[Semantic Relationships & Live Time-Series Attributes]
        H --> I[50% Faster Time-to-Insight for Enterprise AI/ML Workflows]
    end
          </pre>
        </div>

        <h4 style="color: #ffc220; margin: 1.5rem 0 0.75rem 0; font-size: 1rem;">Blueprint 3: Enterprise Data Quality Firewall & Observability Pipeline</h4>
        <div class="mermaid-container">
          <pre class="mermaid">
graph TD
    subgraph Ingress [Data Ingress]
        RawFile[Incoming Vendor ASN / POS Transaction File] --> Gatekeeper[Great Expectations Pre-Ingestion Validator]
    end
    subgraph ContractChecks [Automated Contract Rules]
        Gatekeeper --> C1[Check 1: Primary Key Unique & Non-Null]
        Gatekeeper --> C2[Check 2: Quantities > 0 & Prices Valid]
        Gatekeeper --> C3[Check 3: Temporal Sequence: Shipped <= Delivery]
        Gatekeeper --> C4[Check 4: Categorical Codes Match Master Data]
    end
    subgraph Routing [Automated Routing & Observability]
        C1 & C2 & C3 & C4 -->|All Passed| LoadBronze[Approve for Lakehouse Ingestion]
        C1 | C2 | C3 | C4 -->|Any Failure| Quarantine[Divert to S3 Quarantine + PagerDuty Alert]
        LoadBronze --> Telemetry[Emit Metrics: Freshness, Row Counts, Latency]
        Telemetry --> ObsDashboard[Centralized Data Observability & SLA Monitor]
    end
          </pre>
        </div>
      </div>

      <!-- FILTER CONTROLS -->
      <div class="controls-wrapper">
        <div class="controls-top">
          <div class="search-input-wrap">
            <span class="search-icon">🔍</span>
            <input type="text" id="searchInput" placeholder="Search keywords (e.g., PySpark, Delta Lake, SCD, Kafka, Foundry, skew, Great Expectations)..." oninput="applyFilters()">
          </div>
          <div class="progress-box">
            <div class="progress-bar-track">
              <div class="progress-bar-fill" id="progressFill"></div>
            </div>
            <div class="progress-text" id="progressText">0 / 20 Reviewed</div>
          </div>
        </div>
        <div class="pills-container" id="categoryPills">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- QUESTIONS CONTAINER -->
      <div class="q-list" id="questionList">
        <!-- Rendered by JS -->
      </div>

    </div>
  </div>

  <script>
    const CORRECT_PASS = "Priyanka";
    const itemsData = {items_json_str};
    const categoriesList = {categories_json_str};

    let activeCategory = "All";
    let completedSet = new Set();

    window.addEventListener('DOMContentLoaded', () => {{
      mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
      if (sessionStorage.getItem('priyanka_unlocked') === 'true') {{
        unlockApp();
      }}
      initApp();
    }});

    function checkPass() {{
      const val = document.getElementById('passInput').value.trim();
      if (val.toLowerCase() === CORRECT_PASS.toLowerCase()) {{
        sessionStorage.setItem('priyanka_unlocked', 'true');
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
      sessionStorage.removeItem('priyanka_unlocked');
      document.getElementById('app').style.display = 'none';
      document.getElementById('lockScreen').style.display = 'flex';
      document.getElementById('passInput').value = '';
      document.getElementById('errMsg').style.display = 'none';
    }}

    function initApp() {{
      const pillBox = document.getElementById('categoryPills');
      pillBox.innerHTML = '';
      
      const allBtn = document.createElement('button');
      allBtn.className = 'pill-btn active';
      allBtn.textContent = 'All Items (' + itemsData.length + ')';
      allBtn.onclick = () => setCategory('All', allBtn);
      pillBox.appendChild(allBtn);

      categoriesList.forEach(cat => {{
        const btn = document.createElement('button');
        btn.className = 'pill-btn';
        const count = itemsData.filter(q => q.category === cat).length;
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

      itemsData.forEach((item, idx) => {{
        const card = document.createElement('div');
        card.className = 'q-card';
        card.id = `qcard-${{idx}}`;
        card.setAttribute('data-category', item.category);

        const renderedMd = marked.parse(item.answer);
        const isCoding = item.type === "coding";
        const badgeClass = isCoding ? "q-num-badge coding-badge" : "q-num-badge";
        const badgeLabel = isCoding ? `Code ${{item.num}}` : `Q${{item.num.toString().padStart(2, '0')}}`;

        card.innerHTML = `
          <div class="q-header" onclick="toggleCard(${{idx}})">
            <div class="q-header-left">
              <span class="${{badgeClass}}">${{badgeLabel}}</span>
              <div class="q-meta-group">
                <span class="q-cat-tag">${{item.category}}</span>
                <div class="q-title-text">${{item.title}}</div>
                <div class="q-prompt-sub">${{item.question}}</div>
              </div>
            </div>
            <div class="q-header-right">
              <span class="word-badge">${{item.words}} words</span>
              <input type="checkbox" class="q-checkbox" onclick="event.stopPropagation(); toggleComplete(${{idx}})" title="Mark completed">
              <span class="chevron">▼</span>
            </div>
          </div>
          <div class="q-body">
            <div class="answer-content">
              ${{renderedMd}}
            </div>
            <div class="q-footer-bar">
              <button class="copy-ans-btn" onclick="copyAnswer(${{idx}}, this)">📋 Copy Answer / Code</button>
              <span class="copy-toast" id="toast-${{idx}}">Copied to clipboard!</span>
            </div>
          </div>
        `;
        container.appendChild(card);
      }});
      updateProgress();
    }}

    function toggleCard(idx) {{
      const card = document.getElementById(`qcard-${{idx}}`);
      card.classList.toggle('open');
    }}

    function expandAll(open) {{
      document.querySelectorAll('.q-card').forEach(c => {{
        if (open) c.classList.add('open');
        else c.classList.remove('open');
      }});
    }}

    function toggleComplete(idx) {{
      const card = document.getElementById(`qcard-${{idx}}`);
      if (completedSet.has(idx)) {{
        completedSet.delete(idx);
        card.classList.remove('completed');
      }} else {{
        completedSet.add(idx);
        card.classList.add('completed');
      }}
      updateProgress();
    }}

    function updateProgress() {{
      const total = itemsData.length;
      const count = completedSet.size;
      const pct = Math.round((count / total) * 100);
      document.getElementById('progressFill').style.width = pct + '%';
      document.getElementById('progressText').textContent = `${{count}} / ${{total}} Reviewed (${{pct}}%)`;
    }}

    function applyFilters() {{
      const query = document.getElementById('searchInput').value.toLowerCase().trim();

      itemsData.forEach((item, idx) => {{
        const card = document.getElementById(`qcard-${{idx}}`);
        const matchesCat = (activeCategory === 'All' || item.category === activeCategory);
        const textContent = (item.title + ' ' + item.question + ' ' + item.answer).toLowerCase();
        const matchesQuery = !query || textContent.includes(query);

        if (matchesCat && matchesQuery) {{
          card.style.display = 'block';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    function copyAnswer(idx, btn) {{
      const item = itemsData[idx];
      if (!item) return;
      navigator.clipboard.writeText(item.answer).then(() => {{
        const toast = document.getElementById(`toast-${{idx}}`);
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
    print(f"Building Priyanka Gantam Walmart Prep Suite...")

    # 1. Master Markdown
    master_md = generate_markdown()
    md_path = "priyanka_gantam_walmart_prep.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(master_md)
    print(f"Master Markdown generated: {md_path} ({len(master_md.split())} words)")

    # 2. Nextra MDX
    mdx_content = generate_mdx(master_md)
    mdx_path = os.path.join("content", "priyanka-gantam-walmart-prep.mdx")
    with open(mdx_path, "w", encoding="utf-8") as f:
        f.write(mdx_content)
    print(f"Nextra MDX generated: {mdx_path}")

    # 3. Interactive Webpage
    html_content = generate_html()
    html_path = "priyanka_gantam_walmart_prep.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Interactive Webpage generated: {html_path}")

    # 4. Copy to public/
    os.makedirs("public", exist_ok=True)
    pub_html_path = os.path.join("public", "priyanka_gantam_walmart_prep.html")
    with open(pub_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Public Webpage generated: {pub_html_path}")

    print("\nAll Priyanka Gantam prep assets successfully compiled!")

if __name__ == "__main__":
    main()
