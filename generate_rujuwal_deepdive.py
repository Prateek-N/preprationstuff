# -*- coding: utf-8 -*-
"""
Generator script for Rujuwal Garg Resume Deep-Dive.
Generates:
1. rujuwal_garg_resume_deepdive.md
2. content/rujuwal-garg-resume-deepdive.mdx
3. rujuwal_garg_resume_deepdive.html
"""

import json
import re
import os
from rujuwal_deepdive_data import companies_data, selected_projects_data

# =============================================================================
# 1. GENERATE MASTER MARKDOWN (rujuwal_garg_resume_deepdive.md)
# =============================================================================
def generate_markdown():
    md = []
    md.append("# Rujuwal Garg — Resume Deep-Dive & Enterprise Project Master Reference\n")
    md.append("## Team Lead | Data Analytics, Business Intelligence & AI Solutions\n")
    md.append("**Delhi, India** | +91-9211199998 | rujuwal1@gmail.com | [linkedin.com/in/rujuwalgarg](https://linkedin.com/in/rujuwalgarg)  \n")
    md.append("**Passcode Lock:** `RG`\n\n")
    md.append("---\n\n")

    md.append("## Professional Summary\n")
    md.append("> **Team Lead** with 4+ years of experience across **Data Analytics**, **Business Intelligence**, **AI Engineering**, and cross-functional operations. Promoted from **Data Analyst** at **SilverSpace** in May 2025, automated recruiting KPI reporting for **Vizva** (a part of SilverSpace) to reduce reporting efforts by **70%**. Skilled in **SQL**, **Python**, **MongoDB**, **Power BI**, and **Azure**, with expertise in team mentoring, vendor coordination, stakeholder collaboration, and AI delivery.\n\n")

    md.append("## Technical & Leadership Skills Matrix\n")
    md.append("| Category | Core Competencies & Technologies |\n")
    md.append("| :--- | :--- |\n")
    md.append("| **Analytics & Programming** | **SQL**, **Python**, **Pandas**, **NumPy**, **Exploratory Data Analysis (EDA)**, **Root-Cause Analysis**, **Customer Segmentation**, **A/B Performance Analysis** |\n")
    md.append("| **Business Intelligence** | **Power BI**, **DAX (Data Analysis Expressions)**, **Tableau**, **Looker Studio**, **Advanced Excel Formulas & VBA Macros**, **Power Query** |\n")
    md.append("| **Databases & Data Engineering** | **MongoDB**, **Azure SQL Database**, **Google BigQuery**, **MySQL**, **PostgreSQL**, **Azure Data Factory (ADF)**, **ETL Pipelines**, **PySpark**, **Apache Airflow** |\n")
    md.append("| **AI Engineering & Frameworks** | **Retrieval-Augmented Generation (RAG)**, **LangChain**, **LlamaIndex**, **Model Context Protocol (MCP)**, **Multi-Agent Systems**, **Neo4j Graph Databases**, **Scikit-learn**, **FastAPI** |\n")
    md.append("| **Cloud & MLOps Deployment** | **Microsoft Azure**, **Google Cloud Platform (GCP)**, **Amazon Web Services (AWS)**, **Docker**, **Kubernetes**, **MLflow**, **LangSmith** |\n")
    md.append("| **Leadership & Operations** | **Team Mentoring (4 junior engineers)**, **Cross-Functional Delivery**, **Standard Operating Procedures (SOPs)**, **Metric Governance**, **Vendor Coordination (Vizva)**, **Compensation & Incentive Administration** |\n\n")
    md.append("---\n\n")

    md.append("# Comprehensive Company-by-Company Deep-Dive\n\n")

    total_bullets = 0
    for comp in companies_data:
        md.append(f"## {comp['company_name']} — {comp['role']}\n")
        md.append(f"**Tenure:** {comp['tenure']} | **Location:** {comp['location']}  \n")
        md.append(f"**Organizational Context:** {comp['promotion_note']}\n\n")

        # Dummy Project Section
        proj = comp["project"]
        md.append(f"### Enterprise Dummy Project: {proj['name']}\n")
        md.append(f"**Strategic Objective:** *{proj['tagline']}*  \n")
        md.append(f"**Project Tech Stack:** {', '.join(['`' + t + '`' for t in proj['tech_stack']])}\n\n")
        md.append(f"**Architecture & Business Problem Overview:**\n{proj['overview']}\n\n")

        md.append("```\n")
        md.append("PROJECT HIGH-LEVEL ARCHITECTURE & WORKFLOW BLUEPRINT:\n")
        if comp["company_id"] == "silverspace_lead":
            md.append("""
+--------------------------+    +--------------------------+    +----------------------------+
|   Unstructured Sources   |    |    Relational Sources    |    |      Document Records      |
| Recruiter Transcripts    |    | Azure SQL (Candidates,   |    | MongoDB (Flexible Profiles,|
| Jira / ATS Interviews    |    | Placements, Milestones)  |    | Dynamic Assessment Schemas)|
+------------+-------------+    +------------+-------------+    +-------------+--------------+
             |                               |                                |
             v                               v                                v
+--------------------------------------------------------------------------------------------+
|                    Unified Data Ingestion & Transformation Layer (Python ETL)              |
+--------------------------------------------------------------------------------------------+
             |                                                                |
             v                                                                v
+----------------------------+                                  +----------------------------+
| Autonomous Agent Platform  |                                  |   Enterprise BI Layer      |
| LangGraph + LlamaIndex     |                                  | Power BI Semantic Star     |
| FastAPI Microservices      |                                  | Schema (60+ DAX Measures)  |
| Model Context Protocol     |                                  | Executive KPI Scorecards   |
| LangSmith Observability    |                                  | Operational Bottlenecks    |
+-------------+--------------+                                  +--------------+-------------+
              |                                                                |
              v                                                                v
+----------------------------+                                  +----------------------------+
| External Vendor Routing    |                                  | Multi-Location Incentive   |
| Automated Scheduling Sync  |                                  | Governance Engine          |
| Vizva & Client Partners    |                                  | Tiered Tech Payout Audit   |
+----------------------------+                                  +----------------------------+
""")
        elif comp["company_id"] == "silverspace_analyst":
            md.append("""
+-----------------------+     +-----------------------+     +-----------------------+
|  Legacy Sourcing Log  |     | Technical Interviews  |     |  Sales Billing Master |
| (Excel Spreadsheet A) |     | (Excel Spreadsheet B) |     | (Excel Spreadsheet C) |
+-----------+-----------+     +-----------+-----------+     +-----------+-----------+
            |                             |                             |
            +-----------------------------+-----------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|               Phase 1: Excel Formula & Macro Stabilization (VBA & LAMBDA)         |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|               Phase 2: Azure Blob Storage Landing & Azure Data Factory (ADF)      |
|               Mapping Data Flows (CDC, Deduplication, Surrogate Keys)             |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|               Phase 3: Centralized Azure SQL Database (Star-Schema Data Mart)     |
|               Dim_Candidate | Dim_Recruiter | Dim_Client | Fact_Outreach | Fact_PL|
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|               Phase 4: Interactive Power BI Dashboards (Sub-1.2s Cloud Refresh)   |
|               Outreach Quotas | Funnel Drop-off Ratios | 9-Day Latency Detection  |
+-----------------------------------------------------------------------------------+
""")
        elif comp["company_id"] == "vaco_google":
            md.append("""
+-----------------------------------------------------------------------------------+
|                    Global Hotel Partner Real-Time Pricing Feed                    |
|                2,000+ Hotel Partners · Billions of Auction Rows Daily             |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                 Automated Google Cloud Storage (GCS) Ingestion Worker             |
|                 Python / Cloud Functions · Schema Parsing · Null Diagnostics      |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                 Google BigQuery High-Frequency Analytics Warehouse                |
|                 Partitioning (_PARTITIONDATE) · Clustering (market_id, hotel_id)  |
|                 Window CTEs · Subquery Inlining · Cost & Latency Cut by 40%       |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|        BI Visualization & A/B Root-Cause Diagnostics Layer                        |
|   Looker Studio (4 Regional Dashboards) | Tableau (6 Streams) | Discrepancy Matrix|
+-----------------------------------------------------------------------------------+
""")
        else:
            md.append("""
+-----------------------------------------------------------------------------------+
|                  Profitmart Core MySQL Transactional Databases                     |
|                  Millions of Order Logs · Leverage Ratios · Execution Timestamps  |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                  Python (Pandas / NumPy) & SQL ETL Data Cleansing                 |
|                  Window Deduplication · Missing Value Imputation · Reconciliations|
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                  Exploratory Data Analysis & Statistical Modeling                 |
|                  Pareto Volume Analysis (8% Traders = 62% Brokerage Revenue)      |
|                  Churn Early Warning: Margin Call Drops within 14 Days            |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                  Executive Financial Performance Workbooks (Excel / SQL)          |
|                  Branch Revenue Breakdown · Active Trader Telemetry Dashboards    |
+-----------------------------------------------------------------------------------+
""")
        md.append("```\n\n")

        md.append(f"### Detailed Breakdown of Resume Bullet Points for {comp['company_name']}\n\n")

        for b in comp["bullets"]:
            total_bullets += 1
            words = len(re.findall(r'\b\w+\b', b["explanation"]))
            md.append(f"#### Bullet Point #{b['bullet_num']}\n")
            md.append(f"> **Resume Bullet:** *\"{b['bullet_text']}\"*\n\n")
            md.append(f"**Explanation (1st-Person POV · Simple & Concise):**\n\n")
            md.append(f"{b['explanation']}\n\n")
            md.append("---\n\n")

    # Selected Projects Section
    md.append("# Selected Enterprise Projects\n\n")
    for sp in selected_projects_data:
        md.append(f"### {sp['title']}\n")
        md.append(f"**Tech Stack:** {', '.join(['`' + t + '`' for t in sp['tech_stack']])}\n\n")
        md.append(f"{sp['overview']}\n\n")
        md.append("---\n\n")

    # Behavioral & Interview Storytelling Guide
    md.append("# Enterprise Interview Defense & System Architecture Playbook\n\n")
    md.append("### 1. Framework: The STAR Method for Rujuwal Garg\n")
    md.append("""When discussing any project from this deep dive in technical and hiring manager rounds, structure your answers using the **STAR** framework:
- **Situation:** Set the business context (e.g., decentralized Excel files causing 15 hours of manual reporting toil, or unpartitioned BigQuery queries driving high GCP costs).
- **Task:** Clarify your specific ownership (e.g., leading the Azure cloud migration, designing the LangGraph agent architecture, or authoring enterprise data governance standards).
- **Action:** Deep-dive into technical execution with specific engineering tools, schema designs, algorithms, and frameworks (**Azure Data Factory**, **FastAPI**, **LangChain**, **DAX**, **SQL window functions**).
- **Result:** Quantify the business outcome (**70% reduction in reporting effort**, **40% query performance optimization**, **zero calculation discrepancies**, or **15% decrease in customer churn**).
\n\n""")

    md.append("### 2. Key Architectural Decisions & Trade-Offs\n")
    md.append("""| Architectural Choice | Alternative Considered | Engineering Rationale for Chosen Path |
| :--- | :--- | :--- |
| **LangGraph Multi-Agent Architecture** | Linear LangChain Chains | Recruitment operations require cyclical human-in-the-loop validation, dynamic conditional branching, and checkpoint state recovery when scheduling interviews. |
| **Model Context Protocol (MCP)** | Ad-hoc REST endpoint wrappers | MCP provides standardized protocol interfaces, client authorization separation, and sandboxed tool execution for candidate search and calendar booking. |
| **Azure SQL Star Schema + ADF** | Keeping Google Sheets + Zapier | Relational star-schema with surrogate keys and CDC guarantees ACID consistency, sub-second Power BI querying, and audited data lineage across 200K+ records. |
| **BigQuery Partitioning & Clustering** | Brute-force full table scans | Partitioning by `_PARTITIONDATE` and clustering on `(market_id, hotel_id)` reduces scanned data volume by >80%, cutting query execution times by 40% and saving substantial cloud costs. |
| **Hybrid Polyglot Persistence (Azure SQL + MongoDB)** | Monolithic Single Database | Azure SQL enforces relational financial integrity for placements and incentives, while MongoDB provides flexible document schema for dynamic candidate resumes and interview evaluations. |
\n\n""")

    md.append("### 3. Anticipated High-Level Interview Questions & Strategic Responses\n")
    md.append("""**Q1: How did you transition from Data Analyst to Team Lead so quickly at SilverSpace?**  
*Strategic Response:* "My promotion within 11 months was driven by taking end-to-end technical ownership beyond immediate ticket assignments. In **Project CloudTalent**, I observed that recruitment reporting was bleeding 15 hours a week in manual Excel toil. Rather than simply maintaining spreadsheets, I architected the cloud migration to Azure SQL and Power BI, cutting reporting effort by 70%. When leading **Project CognitiveOps**, I stepped up to mentor 4 junior engineers, established enterprise-wide data governance documentation, coordinated external vendor scheduling with Vizva, and integrated frontier AI solutions (LangGraph and MCP) with our enterprise data pipelines."

**Q2: How did you handle data validation and governance when building reporting models?**  
*Strategic Response:* "Data without governance breeds executive distrust. I authored an enterprise Metric Catalog defining 45+ standard KPIs, detailing source tables, exact SQL/DAX formulas, and ownership. Within our ETL pipelines, I embedded pre-load assertions verifying referential integrity, zero duplicate surrogate keys, and statistical anomaly bounds before refreshing reporting marts. If an ADF pipeline or Python script detected schema drift or volume drops, it halted loading and triggered automated alerts before morning leadership reviews."

**Q3: Walk me through your RAG and Agentic AI architecture.**  
*Strategic Response:* "In **Project CognitiveOps**, we recognized that vanilla RAG with simple vector search fails on multi-hop talent matching queries like 'Find Python engineers with Azure experience who passed Round 1 and are willing to relocate.' We decomposed the problem into a multi-agent system using **LangGraph**: a Supervisor Agent inspects intent, a Database Agent queries structured **Azure SQL** and **MongoDB** collections via parameterized queries, a Retrieval Agent leverages **LlamaIndex** with hybrid HNSW vector search over interview notes, and a Synthesizer formats candidate dossiers. We integrated **LangSmith** for distributed tracing and token latency monitoring, and **MLflow** for prompt and embedding model lifecycle versioning."
\n""")

    return "".join(md)

# =============================================================================
# 2. GENERATE NEXTRA MDX (content/rujuwal-garg-resume-deepdive.mdx)
# =============================================================================
def generate_mdx(markdown_content):
    # Escape raw JSX curly braces outside code fences
    lines = markdown_content.split('\n')
    mdx_lines = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            mdx_lines.append(line)
            continue

        if in_code_block:
            mdx_lines.append(line)
        else:
            # Replace raw { and } with HTML entities so MDX doesn't treat them as JS
            processed = line.replace('{', '&#123;').replace('}', '&#125;')
            # Escape raw < if it looks like an unclosed JSX tag (except known tags)
            # Replace `< ` or `<2` with `&lt; `
            processed = re.sub(r'<(?=[0-9 ])', '&lt;', processed)
            mdx_lines.append(processed)

    escaped_body = '\n'.join(mdx_lines)

    header = """---
title: Rujuwal Garg — Team Lead, Data Analytics & AI Solutions Resume Deep-Dive
description: Comprehensive project-by-project deep-dive into Rujuwal Garg's resume covering SilverSpace Inc., Vaco Binary Semantics (Google Hotel Ads), Profitmart, and enterprise AI engineering.
---

<PasswordGate password="RG">

"""

    footer = """

</PasswordGate>
"""
    return header + escaped_body + footer

# =============================================================================
# 3. GENERATE INTERACTIVE WEBPAGE (rujuwal_garg_resume_deepdive.html)
# =============================================================================
def generate_html():
    items_json = []
    item_counter = 0

    for comp in companies_data:
        for b in comp["bullets"]:
            item_counter += 1
            words = len(re.findall(r'\b\w+\b', b["explanation"]))
            items_json.append({
                "num": item_counter,
                "bullet_num": b["bullet_num"],
                "company_id": comp["company_id"],
                "company_name": comp["company_name"],
                "role": comp["role"],
                "project_name": comp["project"]["name"],
                "bullet_text": b["bullet_text"],
                "words": words,
                "explanation": b["explanation"]
            })

    items_json_str = json.dumps(items_json, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rujuwal Garg — Resume Deep-Dive & Project Architecture Suite</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-base: #090d16;
      --bg-surface: #0f172a;
      --bg-card: #141e33;
      --bg-card-hover: #1b2845;
      --border: #243454;
      --border-accent: #38bdf8;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --rg-blue: #3b82f6;
      --rg-cyan: #06b6d4;
      --rg-emerald: #10b981;
      --rg-purple: #8b5cf6;
      --rg-amber: #f59e0b;
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg-base);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.6;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }}

    /* LOCK SCREEN */
    #lockScreen {{
      position: fixed; inset: 0;
      background: radial-gradient(circle at center, #172554 0%, #030712 100%);
      display: flex; align-items: center; justify-content: center;
      z-index: 99999; padding: 1.5rem;
    }}
    .lock-box {{
      background: rgba(15, 23, 42, 0.96);
      backdrop-filter: blur(24px);
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 22px;
      padding: 2.75rem 2.5rem;
      max-width: 480px;
      width: 100%;
      text-align: center;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.9), 0 0 50px rgba(56, 189, 248, 0.2);
    }}
    .lock-logo-mark {{
      display: inline-flex; align-items: center; justify-content: center;
      margin-bottom: 1.5rem; font-size: 2.5rem; font-weight: 900; letter-spacing: -0.04em;
    }}
    .lock-txt-1 {{ color: #ffffff; }}
    .lock-txt-2 {{ color: #38bdf8; }}
    .lock-badge-pill {{
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(139, 92, 246, 0.2));
      border: 1px solid rgba(56, 189, 248, 0.4);
      padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; color: #7dd3fc;
      font-family: var(--font-mono); margin-left: 8px; font-weight: 700;
    }}
    .lock-box h2 {{ font-size: 1.45rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.02em; }}
    .lock-box p {{ color: var(--text-muted); font-size: 0.88rem; margin-bottom: 1.75rem; }}
    .input-group {{ position: relative; margin-bottom: 1.25rem; }}
    .input-group input {{
      width: 100%;
      background: rgba(8, 13, 22, 0.92);
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
      border-color: var(--rg-cyan);
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
      background: linear-gradient(135deg, #38bdf8, #0284c7);
    }}
    .lock-error {{ color: #f87171; font-size: 0.85rem; margin-top: 0.85rem; display: none; font-weight: 500; }}

    /* APP LAYOUT */
    #appContent {{ display: none; opacity: 0; transition: opacity 0.4s ease; }}
    .app-header {{
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border);
      position: sticky; top: 0; z-index: 1000;
      padding: 1rem 2rem;
    }}
    .header-inner {{
      max-width: 1440px; margin: 0 auto;
      display: flex; align-items: center; justify-content: space-between;
      gap: 1.5rem; flex-wrap: wrap;
    }}
    .brand-title {{ display: flex; align-items: center; gap: 14px; }}
    .brand-badge {{
      background: linear-gradient(135deg, rgba(6, 182, 212, 0.25), rgba(59, 130, 246, 0.15));
      border: 1px solid rgba(6, 182, 212, 0.5);
      color: #ffffff;
      font-size: 0.82rem; font-weight: 800;
      padding: 6px 12px; border-radius: 8px; letter-spacing: 0.05em;
      display: flex; align-items: center; gap: 6px;
    }}
    .brand-badge span.accent {{ color: #38bdf8; font-weight: 900; }}
    .brand-title h1 {{ font-size: 1.15rem; font-weight: 700; letter-spacing: -0.01em; }}
    .brand-sub {{ font-size: 0.8rem; color: var(--text-muted); }}

    .header-right {{ display: flex; align-items: center; gap: 1.25rem; }}
    .progress-wrap {{ display: flex; align-items: center; gap: 10px; min-width: 220px; }}
    .progress-bar-bg {{
      flex: 1; height: 8px; background: rgba(255,255,255,0.1); border-radius: 99px; overflow: hidden;
    }}
    .progress-bar-fill {{
      height: 100%; width: 0%;
      background: linear-gradient(90deg, #38bdf8, #10b981);
      transition: width 0.3s ease;
    }}
    .progress-text {{ font-size: 0.78rem; font-family: var(--font-mono); color: var(--text-muted); white-space: nowrap; }}

    /* HERO PROFILE */
    .hero-wrap {{
      max-width: 1440px; margin: 2rem auto 0; padding: 0 2rem;
    }}
    .hero-card {{
      background: linear-gradient(135deg, rgba(20, 30, 51, 0.9), rgba(15, 23, 42, 0.95));
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 2rem 2.25rem;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }}
    .hero-meta {{
      display: flex; justify-content: space-between; align-items: flex-start;
      gap: 1.5rem; flex-wrap: wrap; margin-bottom: 1.25rem;
    }}
    .hero-name {{ font-size: 2rem; font-weight: 800; letter-spacing: -0.03em; color: #fff; }}
    .hero-role {{ font-size: 1.15rem; color: #38bdf8; font-weight: 600; margin-top: 4px; }}
    .hero-contact {{
      display: flex; gap: 1rem; font-size: 0.85rem; color: var(--text-muted); flex-wrap: wrap; margin-top: 8px;
    }}
    .hero-contact span {{ display: inline-flex; align-items: center; gap: 4px; }}
    .hero-summary {{
      font-size: 0.95rem; color: #cbd5e1; line-height: 1.65; max-width: 1100px;
      padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.08);
    }}

    /* SEARCH & FILTER CONTROLS */
    .controls-wrap {{
      max-width: 1440px; margin: 1.5rem auto 0; padding: 0 2rem;
      display: flex; flex-direction: column; gap: 1rem;
    }}
    .search-row {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
    .search-input-box {{
      flex: 1; min-width: 280px; position: relative;
    }}
    .search-input-box input {{
      width: 100%; background: var(--bg-surface);
      border: 1px solid var(--border); border-radius: 12px;
      padding: 0.85rem 1.15rem 0.85rem 2.75rem; color: #fff;
      font-size: 0.92rem; outline: none; transition: border-color 0.2s;
    }}
    .search-input-box input:focus {{ border-color: var(--rg-cyan); }}
    .search-icon {{
      position: absolute; left: 1rem; top: 50%; transform: translateY(-50%);
      color: var(--text-dim); pointer-events: none; font-size: 1rem;
    }}

    .action-btn {{
      background: var(--bg-surface); border: 1px solid var(--border);
      color: var(--text-main); padding: 0.75rem 1.25rem; border-radius: 12px;
      font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
      display: inline-flex; align-items: center; gap: 6px;
    }}
    .action-btn:hover {{
      background: var(--bg-card-hover); border-color: var(--border-accent);
    }}

    .filter-pills {{
      display: flex; gap: 8px; flex-wrap: wrap;
    }}
    .filter-pill {{
      background: rgba(15, 23, 42, 0.8); border: 1px solid var(--border);
      color: var(--text-muted); padding: 6px 14px; border-radius: 99px;
      font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
    }}
    .filter-pill:hover, .filter-pill.active {{
      background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(59, 130, 246, 0.2));
      border-color: var(--rg-cyan); color: #fff;
    }}

    /* MAIN CONTAINER */
    .main-wrap {{
      max-width: 1440px; margin: 1.5rem auto 3rem; padding: 0 2rem;
    }}

    /* DUMMY PROJECT HERO CARDS */
    .project-hero {{
      background: linear-gradient(135deg, rgba(20, 30, 51, 0.95), rgba(15, 23, 42, 0.95));
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 1.75rem;
      margin-bottom: 1.5rem;
    }}
    .project-hero-badge {{
      display: inline-flex; align-items: center; gap: 6px;
      padding: 4px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;
      letter-spacing: 0.04em; margin-bottom: 0.75rem;
      background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    .project-hero h3 {{ font-size: 1.35rem; font-weight: 700; color: #fff; margin-bottom: 0.35rem; }}
    .project-hero .tagline {{ font-size: 0.9rem; color: #93c5fd; font-style: italic; margin-bottom: 1rem; }}
    .project-hero p {{ font-size: 0.92rem; color: #cbd5e1; line-height: 1.65; margin-bottom: 1rem; }}
    .project-tech-chips {{ display: flex; flex-wrap: wrap; gap: 6px; }}
    .tech-chip {{
      background: rgba(8, 13, 22, 0.8); border: 1px solid var(--border);
      padding: 3px 8px; border-radius: 6px; font-family: var(--font-mono);
      font-size: 0.75rem; color: #7dd3fc;
    }}

    /* BULLET CARDS */
    .card-list {{ display: flex; flex-direction: column; gap: 1.25rem; margin-bottom: 2.5rem; }}
    .b-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      transition: all 0.25s ease;
    }}
    .b-card:hover {{
      border-color: rgba(56, 189, 248, 0.4);
      box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }}
    .b-card.completed {{
      border-color: rgba(16, 185, 129, 0.4);
      background: rgba(16, 185, 129, 0.03);
    }}

    .b-header {{
      padding: 1.25rem 1.5rem;
      cursor: pointer;
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 1.25rem;
      user-select: none;
    }}
    .b-header-left {{ display: flex; align-items: flex-start; gap: 14px; flex: 1; }}
    .b-num-badge {{
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: #38bdf8;
      font-family: var(--font-mono);
      font-size: 0.82rem; font-weight: 700;
      padding: 6px 12px; border-radius: 10px;
      white-space: nowrap; margin-top: 2px;
    }}
    .b-card.completed .b-num-badge {{
      background: rgba(16, 185, 129, 0.15);
      border-color: rgba(16, 185, 129, 0.35);
      color: #10b981;
    }}

    .b-meta-group {{ display: flex; flex-direction: column; gap: 4px; }}
    .b-company-tag {{
      font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em;
      color: var(--text-dim); font-weight: 700;
    }}
    .b-resume-text {{
      font-size: 0.98rem; font-weight: 600; color: #f1f5f9; line-height: 1.5;
    }}

    .b-header-right {{
      display: flex; align-items: center; gap: 12px; margin-top: 4px;
    }}
    .word-badge {{
      background: rgba(139, 92, 246, 0.15); border: 1px solid rgba(139, 92, 246, 0.3);
      color: #c4b5fd; font-family: var(--font-mono); font-size: 0.75rem;
      padding: 4px 8px; border-radius: 6px; white-space: nowrap;
    }}
    .b-checkbox {{
      width: 18px; height: 18px; cursor: pointer; accent-color: #10b981;
    }}
    .chevron {{
      color: var(--text-dim); font-size: 0.75rem; transition: transform 0.25s ease;
    }}
    .b-card.open .chevron {{ transform: rotate(180deg); color: #38bdf8; }}

    .b-body {{
      display: none;
      padding: 0 1.5rem 1.5rem 1.5rem;
      border-top: 1px solid rgba(255,255,255,0.06);
      background: rgba(8, 13, 22, 0.5);
    }}
    .b-card.open .b-body {{ display: block; }}

    .b-explanation {{
      padding-top: 1.25rem; font-size: 0.95rem; color: #cbd5e1; line-height: 1.7;
    }}
    .b-explanation strong {{
      color: #fff; font-weight: 700;
    }}
    .b-explanation ul, .b-explanation ol {{
      margin: 0.75rem 0 0.75rem 1.5rem;
    }}
    .b-explanation li {{ margin-bottom: 0.4rem; }}

    .b-footer {{
      margin-top: 1.25rem; padding-top: 1rem;
      border-top: 1px solid rgba(255,255,255,0.06);
      display: flex; justify-content: space-between; align-items: center;
      font-size: 0.8rem; color: var(--text-dim); flex-wrap: wrap; gap: 10px;
    }}
    .copy-btn {{
      background: var(--bg-surface); border: 1px solid var(--border);
      color: var(--text-muted); padding: 5px 12px; border-radius: 8px;
      font-size: 0.78rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
    }}
    .copy-btn:hover {{
      color: #fff; border-color: var(--rg-cyan);
    }}

    /* TOAST */
    #toast {{
      position: fixed; bottom: 2rem; right: 2rem;
      background: #10b981; color: #fff; padding: 0.75rem 1.5rem;
      border-radius: 10px; font-weight: 700; font-size: 0.88rem;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5); z-index: 100000;
      display: none; animation: slideIn 0.2s ease;
    }}
    @keyframes slideIn {{
      from {{ transform: translateY(10px); opacity: 0; }}
      to {{ transform: translateY(0); opacity: 1; }}
    }}
  </style>
</head>
<body>

  <!-- PASSCODE LOCK SCREEN -->
  <div id="lockScreen">
    <div class="lock-box">
      <div class="lock-logo-mark">
        <span class="lock-txt-1">Prep</span><span class="lock-txt-2">Suite</span>
        <span class="lock-badge-pill">RG LOCK</span>
      </div>
      <h2>Rujuwal Garg — Resume Deep-Dive</h2>
      <p>Team Lead | Data Analytics, Business Intelligence & AI Solutions<br>Enter authorized passcode to unlock the full dossier.</p>
      <div class="input-group">
        <input type="password" id="passInput" placeholder="Enter Passcode (RG)" autofocus>
      </div>
      <button class="unlock-btn" onclick="checkAuth()">Access Dossier</button>
      <div class="lock-error" id="lockError">Invalid passcode. Please enter "RG" to unlock.</div>
    </div>
  </div>

  <!-- MAIN APP CONTENT -->
  <div id="appContent">
    <header class="app-header">
      <div class="header-inner">
        <div class="brand-title">
          <div class="brand-badge">
            <span>PREP</span><span class="accent">SUITE</span>
          </div>
          <div>
            <h1>Rujuwal Garg — Resume Deep-Dive</h1>
            <div class="brand-sub">Team Lead | Data Analytics & AI Solutions · Passcode Protected</div>
          </div>
        </div>
        <div class="header-right">
          <div class="progress-wrap">
            <div class="progress-bar-bg">
              <div class="progress-bar-fill" id="topProgress"></div>
            </div>
            <span class="progress-text" id="readCounter">0 / 19 Reviewed</span>
          </div>
        </div>
      </div>
    </header>

    <!-- HERO PROFILE -->
    <div class="hero-wrap">
      <div class="hero-card">
        <div class="hero-meta">
          <div>
            <div class="hero-name">Rujuwal Garg</div>
            <div class="hero-role">Team Lead | Data Analytics, Business Intelligence & AI Solutions</div>
            <div class="hero-contact">
              <span>📍 Delhi, India</span>
              <span>📞 +91-9211199998</span>
              <span>✉️ rujuwal1@gmail.com</span>
              <span>🔗 linkedin.com/in/rujuwalgarg</span>
            </div>
          </div>
        </div>
        <div class="hero-summary">
          <strong>Professional Profile:</strong> Team Lead with 4+ years of experience across <strong>Data Analytics</strong>, <strong>Business Intelligence</strong>, <strong>AI Engineering</strong>, and cross-functional operations. Promoted from Data Analyst at SilverSpace in May 2025, automated recruiting KPI reporting for Vizva (a part of SilverSpace) to reduce reporting efforts by <strong>70%</strong>. Skilled in <strong>SQL</strong>, <strong>Python</strong>, <strong>MongoDB</strong>, <strong>Power BI</strong>, and <strong>Azure</strong>, with expertise in team mentoring, vendor coordination, stakeholder collaboration, and AI delivery.
        </div>
      </div>
    </div>

    <!-- CONTROLS -->
    <div class="controls-wrap">
      <div class="search-row">
        <div class="search-input-box">
          <span class="search-icon">🔍</span>
          <input type="text" id="globalSearch" placeholder="Search keywords, tech stack, SQL, Power BI, LangGraph, BigQuery..." oninput="handleSearch()">
        </div>
        <button class="action-btn" onclick="expandAll()">📂 Expand All</button>
        <button class="action-btn" onclick="collapseAll()">📁 Collapse All</button>
        <button class="action-btn" onclick="resetFilters()">↺ Reset</button>
      </div>
      <div class="filter-pills" id="companyPills">
        <button class="filter-pill active" onclick="filterCompany('all', this)">All Companies (19)</button>
        <button class="filter-pill" onclick="filterCompany('silverspace_lead', this)">SilverSpace Lead (8)</button>
        <button class="filter-pill" onclick="filterCompany('silverspace_analyst', this)">SilverSpace Analyst (5)</button>
        <button class="filter-pill" onclick="filterCompany('vaco_google', this)">Vaco Google Ads (4)</button>
        <button class="filter-pill" onclick="filterCompany('profitmart_intern', this)">Profitmart Intern (2)</button>
      </div>
    </div>

    <!-- MAIN CARDS CONTAINER -->
    <main class="main-wrap">
      <div id="companyProjectsWrap">
        <!-- Injected via JavaScript -->
      </div>
    </main>
  </div>

  <div id="toast">Copied to clipboard!</div>

  <script>
    const PASSCODE = "RG";
    const itemsData = {items_json_str};

    const companyMetadata = {{
      "silverspace_lead": {{
        "name": "SilverSpace Inc.",
        "role": "Team Lead | Data Analytics and AI Solutions (May 2025 – Present)",
        "project_title": "Project CognitiveOps — Enterprise Agentic Talent Intelligence & Multi-Location Incentive Governance Platform",
        "tagline": "Multi-Tenant Agentic Digital Assistant, Real-Time BI Intelligence, and Automated Compensation Governance",
        "desc": "As Team Lead, Rujuwal architected and spearheaded Project CognitiveOps, a centralized, multi-tenant enterprise platform engineered to unify fragmented recruitment operations, candidate intelligence, interviewer allocation, and technical compensation governance across SilverSpace and its global vendor network (including Vizva Consultancy Services). The platform bridges structured relational operational data with unstructured interview transcripts and company policy knowledge.",
        "tech": ["Python", "FastAPI", "LangGraph", "LangChain", "LlamaIndex", "Model Context Protocol (MCP)", "Power BI", "DAX", "Azure SQL Database", "MongoDB", "Docker", "Kubernetes", "MLflow", "LangSmith", "Apache Airflow", "Excel / openpyxl"]
      }},
      "silverspace_analyst": {{
        "name": "SilverSpace Inc.",
        "role": "Data Analyst (Jun 2024 – May 2025)",
        "project_title": "Project CloudTalent — Recruitment KPI Automation, Data Warehousing & Cloud Modernization",
        "tagline": "Enterprise Cloud Migration from Excel Spreadsheets to Azure Data Factory, Azure SQL & Power BI",
        "desc": "When Rujuwal joined Vizva (a division of SilverSpace), recruitment, sales, and candidate pipeline tracking were conducted entirely through decentralized, error-prone Excel spreadsheets. This caused version collisions, broken formulas, and over 15 hours of manual reporting toil every week. Rujuwal designed and executed Project CloudTalent, migrating recruitment tracking to a centralized Azure SQL Database cloud data mart.",
        "tech": ["Azure SQL Database", "Azure Data Factory (ADF)", "Power BI", "DAX", "SQL", "Python", "Pandas", "Excel VBA / Advanced Macros", "Azure Blob Storage"]
      }},
      "vaco_google": {{
        "name": "Vaco Binary Semantics LLP",
        "role": "Associate Data Analyst - Google Hotel Ads Project (Jul 2022 – Jun 2024)",
        "project_title": "Project BidOptima — High-Frequency Hotel Ad Auction Analytics, BigQuery Optimization & Price Parity Diagnostics",
        "tagline": "Google Hotel Ads Pricing Telemetry, BigQuery SQL Performance Tuning, and Regional Market BI Dashboards",
        "desc": "At Vaco Binary Semantics, Rujuwal was embedded within the dedicated analytical operations group supporting the Google Hotel Ads program. Google Hotel Ads connects travelers searching on Google with real-time hotel booking rates. He built Project BidOptima to ingest, clean, and analyze high-velocity hotel bid auctions, price accuracy discrepancies, and partner ad performance across thousands of global hotel chains.",
        "tech": ["Google BigQuery", "Google Cloud Storage (GCS)", "SQL", "Looker Studio", "Tableau", "Python", "A/B Testing", "Root-Cause Analysis", "Data Validation"]
      }},
      "profitmart_intern": {{
        "name": "Profitmart",
        "role": "Data Analyst Intern (Jan 2022 – May 2022)",
        "project_title": "Project TradePulse — Customer Trading Telemetry, Account Activity Modeling & Reporting Automation",
        "tagline": "Exploratory Data Analysis, Data Cleaning Pipelines, and Financial Performance Analytics",
        "desc": "During his internship at Profitmart, a retail financial brokerage firm, Rujuwal established his core data engineering and analytical foundations. He worked on Project TradePulse, analyzing customer trading volumes, account churn indicators, margin call occurrences, and brokerage fee revenues across retail investor accounts to uncover behavioral patterns and support executive reporting.",
        "tech": ["Python", "Pandas", "NumPy", "SQL", "MySQL", "Excel", "Data Cleansing", "Exploratory Data Analysis"]
      }}
    }};

    function checkAuth() {{
      const entered = document.getElementById("passInput").value.trim();
      if (entered === PASSCODE || localStorage.getItem("rg_auth") === "true") {{
        localStorage.setItem("rg_auth", "true");
        revealContent();
      }} else {{
        document.getElementById("lockError").style.display = "block";
      }}
    }}

    document.getElementById("passInput").addEventListener("keypress", function(e) {{
      if (e.key === "Enter") checkAuth();
    }});

    function revealContent() {{
      document.getElementById("lockScreen").style.display = "none";
      const app = document.getElementById("appContent");
      app.style.display = "block";
      setTimeout(() => app.style.opacity = "1", 20);
      renderSections();
      updateProgress();
    }}

    function formatText(raw) {{
      let res = raw;
      res = res.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
      res = res.replace(/`([^`]+)`/g, '<code style="background:rgba(255,255,255,0.08);padding:2px 6px;border-radius:4px;font-family:var(--font-mono);font-size:0.85em;color:#7dd3fc;">$1</code>');
      res = res.replace(/\\n\\n/g, '<br><br>');
      res = res.replace(/\\n/g, '<br>');
      return res;
    }}

    function renderSections() {{
      const container = document.getElementById("companyProjectsWrap");
      const companies = ["silverspace_lead", "silverspace_analyst", "vaco_google", "profitmart_intern"];

      let html = "";
      companies.forEach(compId => {{
        const meta = companyMetadata[compId];
        const bullets = itemsData.filter(i => i.company_id === compId);

        html += `
          <section class="company-section" data-comp="${{compId}}">
            <div class="project-hero">
              <div class="project-hero-badge">DUMMY PROJECT ARCHITECTURE</div>
              <h3>${{meta.project_title}}</h3>
              <div class="tagline">${{meta.role}} · ${{meta.tagline}}</div>
              <p>${{meta.desc}}</p>
              <div class="project-tech-chips">
                ${{meta.tech.map(t => `<span class="tech-chip">${{t}}</span>`).join('')}}
              </div>
            </div>

            <div class="card-list">
              ${{bullets.map(b => `
                <div class="b-card" id="card-${{b.num}}" data-comp="${{b.company_id}}" data-search="${{(b.bullet_text + ' ' + b.explanation + ' ' + meta.project_title).toLowerCase()}}">
                  <div class="b-header" onclick="toggleCard(this)">
                    <div class="b-header-left">
                      <div class="b-num-badge">Bullet #${{b.bullet_num}}</div>
                      <div class="b-meta-group">
                        <span class="b-company-tag">${{b.company_name}}</span>
                        <div class="b-resume-text">"${{b.bullet_text}}"</div>
                      </div>
                    </div>
                    <div class="b-header-right">
                      <span class="word-badge">${{b.words}} words</span>
                      <input type="checkbox" class="b-checkbox" onclick="event.stopPropagation(); toggleComplete(${{b.num}})" title="Mark as reviewed">
                      <span class="chevron">▼</span>
                    </div>
                  </div>
                  <div class="b-body">
                    <div class="b-explanation">${{formatText(b.explanation)}}</div>
                    <div class="b-footer">
                      <span>First-Person POV · Simple & Layman Explanation (${{b.words}} words)</span>
                      <button class="copy-btn" onclick="copyExplanation(${{b.num}}, this)">📋 Copy Explanation</button>
                    </div>
                  </div>
                </div>
              `).join('')}}
            </div>
          </section>
        `;
      }});

      container.innerHTML = html;
    }}

    function toggleCard(headerEl) {{
      headerEl.closest(".b-card").classList.toggle("open");
    }}

    function expandAll() {{
      document.querySelectorAll(".b-card").forEach(c => c.classList.add("open"));
    }}

    function collapseAll() {{
      document.querySelectorAll(".b-card").forEach(c => c.classList.remove("open"));
    }}

    function toggleComplete(num) {{
      const card = document.getElementById(`card-${{num}}`);
      const cb = card.querySelector(".b-checkbox");
      if (cb.checked) {{
        card.classList.add("completed");
      }} else {{
        card.classList.remove("completed");
      }}
      updateProgress();
    }}

    function updateProgress() {{
      const total = itemsData.length;
      const checked = document.querySelectorAll(".b-checkbox:checked").length;
      const pct = total > 0 ? (checked / total) * 100 : 0;
      document.getElementById("topProgress").style.width = pct + "%";
      document.getElementById("readCounter").innerText = `${{checked}} / ${{total}} Reviewed`;
    }}

    let activeComp = 'all';

    function filterCompany(compId, btnEl) {{
      activeComp = compId;
      document.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
      if (btnEl) btnEl.classList.add("active");
      applyFilterAndSearch();
    }}

    function handleSearch() {{
      applyFilterAndSearch();
    }}

    function applyFilterAndSearch() {{
      const query = document.getElementById("globalSearch").value.toLowerCase().trim();
      document.querySelectorAll(".company-section").forEach(sec => {{
        const secComp = sec.getAttribute("data-comp");
        let visibleCount = 0;

        sec.querySelectorAll(".b-card").forEach(card => {{
          const cardSearch = card.getAttribute("data-search");
          const matchesComp = (activeComp === 'all' || secComp === activeComp);
          const matchesQuery = (!query || cardSearch.includes(query));

          if (matchesComp && matchesQuery) {{
            card.style.display = "block";
            visibleCount++;
          }} else {{
            card.style.display = "none";
          }}
        }});

        if (visibleCount > 0) {{
          sec.style.display = "block";
        }} else {{
          sec.style.display = "none";
        }}
      }});
    }}

    function resetFilters() {{
      document.getElementById("globalSearch").value = "";
      filterCompany('all', document.querySelector(".filter-pill"));
    }}

    function copyExplanation(num, btn) {{
      const item = itemsData.find(i => i.num === num);
      if (!item) return;
      const text = `Bullet #${{item.bullet_num}} (${{item.company_name}})\\nResume Bullet: "${{item.bullet_text}}"\\n\\nDeep-Dive Explanation:\\n${{item.explanation}}`;
      navigator.clipboard.writeText(text).then(() => showToast(btn));
    }}

    function showToast(btn) {{
      const toast = document.getElementById("toast");
      toast.style.display = "block";
      if (btn) {{
        const orig = btn.innerText;
        btn.innerText = "✓ Copied!";
        setTimeout(() => btn.innerText = orig, 1800);
      }}
      setTimeout(() => toast.style.display = "none", 2200);
    }}

    window.addEventListener("DOMContentLoaded", () => {{
      if (localStorage.getItem("rg_auth") === "true") {{
        revealContent();
      }}
    }});
  </script>
</body>
</html>
"""
    return html

def main():
    print("Generating Rujuwal Garg Resume Deep-Dive files...")
    
    # 1. Master Markdown
    md_content = generate_markdown()
    with open("rujuwal_garg_resume_deepdive.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("SUCCESS: Created rujuwal_garg_resume_deepdive.md")

    # 2. Nextra MDX
    mdx_content = generate_mdx(md_content)
    with open("content/rujuwal-garg-resume-deepdive.mdx", "w", encoding="utf-8") as f:
        f.write(mdx_content)
    print("SUCCESS: Created content/rujuwal-garg-resume-deepdive.mdx")

    # 3. Interactive Webpage
    html_content = generate_html()
    with open("rujuwal_garg_resume_deepdive.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("SUCCESS: Created rujuwal_garg_resume_deepdive.html")

if __name__ == "__main__":
    main()
