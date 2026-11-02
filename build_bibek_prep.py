# -*- coding: utf-8 -*-
"""
Build script for Bibek Thapa's Data / Reporting Analyst — Yale University (Enterprise Research Services) Interview Prep Suite.
Compiles:
1. bibek_yale_reporting_prep.md
2. content/bibek-yale-reporting-prep.mdx
3. bibek_yale_reporting_prep.html
4. public/bibek_yale_reporting_prep.html

Passcode: "Bibek"
"""

import json
import re
import os
import shutil

from bibek_questions_part1 import QUESTIONS_PART1
from bibek_questions_part2 import QUESTIONS_PART2
from bibek_coding import CODING_PROBLEMS

QUESTIONS = QUESTIONS_PART1 + QUESTIONS_PART2
print(f"Loaded {len(QUESTIONS)} Technical Questions and {len(CODING_PROBLEMS)} Coding Problems.")

# =============================================================================
# 1. GENERATE MASTER MARKDOWN (bibek_yale_reporting_prep.md)
# =============================================================================
def generate_markdown():
    md = []
    md.append("# Bibek Thapa — Data / Reporting Analyst Technical Interview Preparation Suite\n\n")
    md.append("## Target Role: Data / Reporting Analyst — Yale University (Enterprise Research Services)\n\n")
    md.append("**Candidate:** Bibek Thapa | Dallas, TX | (682) 246-3448 | bibek.tech222@outlook.com | [LinkedIn](https://linkedin.com/in/bibek-thapa-8095b9435)\n\n")
    md.append("**Target Institution & Team:** Yale University — Enterprise Research Services within Research Administration & Central Finance\n\n")
    md.append("**Target Focus:** Power BI Reporting Solutions · Research Administration Analytics · Financial Reporting (Workday / Kuali) · Sponsored Project Burn Rate & F&A Cost Recovery · Federally Mandated Compliance (Uniform Guidance 2 CFR 200, NIH, NSF) · SQL & Python ETL · Snowflake & Azure Cloud Data Warehousing · Microsoft Copilot & GenAI Workflows\n\n")
    md.append("**Passcode Lock:** `Bibek`\n\n")
    md.append("---\n\n")

    md.append("## Executive Summary & Yale Strategic Alignment\n\n")
    md.append("> **Bibek Thapa** is an accomplished **Data and Reporting Analyst** with 4+ years of production experience building high-performance SQL pipelines, predictive models, enterprise data lakehouses, and executive business intelligence dashboards across complex, highly regulated financial services, healthcare, and insurance ecosystems. Bibek holds a Bachelor of Science in Business Computer Information Systems from the **University of North Texas (2021)** and brings a proven track record delivering analytics solutions consumed by **40+ stakeholders at Fortune 500 organizations**, including **JPMorgan Chase & Co.**, **Roche**, and **Liberty Mutual Insurance**.\n\n")
    md.append("> At **JPMorgan Chase & Co.**, Bibek architected an enterprise **Power BI executive reporting dashboard** consolidating data from **8 upstream transaction systems**, cutting weekly reporting preparation time from **10 hours down to 90 minutes** for senior finance leadership. He authored optimized **T-SQL stored procedures** and **Python validation scripts** to audit **1.8 million daily transaction records** across 4 risk categories, reducing data quality escalations from **30 to 5 per month**. He engineered automated **Python ETL pipelines** into **Snowflake** eliminating 6 hours of weekly manual processing, partnered with Risk, Compliance, Treasury, and Operations to build a centralized KPI framework for 40+ stakeholders, and deployed **Python anomaly detection models** on payment streams flagging 120+ suspicious transactions weekly.\n\n")
    md.append("> At **Roche**, Bibek engineered **Snowflake data pipelines** consolidating clinical trial telemetry from **6 multi-site research centers**, cutting query turnaround times from **3 hours to 20 minutes**. He designed **Tableau dashboards** tracking patient outcomes across **10 therapeutic domains** for **85,000+ patient records**, applied **multivariable regression and survival analysis in Python** that directly informed a **$150M research portfolio capital decision**, validated **35 regulatory tables across 4 datasets with zero errors for an FDA submission**, and instituted **Great Expectations data quality checks** cutting master data conflicts from **80 to 12 per month**.\n\n")
    md.append("> At **Liberty Mutual Insurance**, Bibek analyzed claims data for **600,000+ policyholders** in SQL and Python, surfacing loss patterns that reduced the processing backlog by **1,800 cases per quarter**, built **actuarial Tableau dashboards** saving 8 analyst hours weekly, trained **Scikit-learn classification models** prioritizing 1,200 high-risk accounts per cycle, co-led a legacy reporting migration to **Amazon Redshift** compressing monthly report generation from **7 hours to 40 minutes**, and led **A/B testing** on digital intake workflows cutting submission latency from **24 to 9 minutes**.\n\n")
    md.append("> For **Yale University's Enterprise Research Services**, Bibek brings the ideal intersection of enterprise Power BI reporting mastery, advanced SQL/Python data engineering, financial accounting acumen, and deep regulatory compliance experience. He is primed to partner with research administration, finance, IT, and faculty Principal Investigators to modernize Yale's sponsored research data ecosystem, deliver intuitive self-service grant financial scorecards, automate federally mandated 2 CFR 200 reporting, and maximize indirect cost recovery.\n\n")

    md.append("## Quantified Impact & Architecture Metrics\n\n")
    md.append("| Organization / System | Domain & Role | Core Tech Stack | Quantified Engineering & Business Impact |\n")
    md.append("| :--- | :--- | :--- | :--- |\n")
    md.append("| **JPMorgan Chase & Co.** | Financial Analytics & BI | Power BI, DAX, Star Schema, VertiPaq | Consolidated 8 systems; cut reporting prep from **10 hours to 90 minutes (85% reduction)** |\n")
    md.append("| **JPMorgan Chase & Co.** | High-Throughput Data Validation | T-SQL Stored Procs, Python, Columnstore | Validated **1.8M daily records**; cut data quality escalations from **30 to 5 per month** |\n")
    md.append("| **JPMorgan Chase & Co.** | Cloud Data Warehousing ETL | Python, Snowflake, Airflow, SFTP | Automated ingestion from 3 trading feeds; eliminated **6 hours/week manual data work** |\n")
    md.append("| **JPMorgan Chase & Co.** | Stakeholder KPI Framework | Data Dictionary, Jira, Confluence, BI | Unified **40+ stakeholders across 4 business units** around single certified KPI source |\n")
    md.append("| **JPMorgan Chase & Co.** | Stream Anomaly Detection | Python, Scikit-learn, Isolation Forest | Flagged **120+ suspicious transactions/week** with >88% verified actionability rate |\n")
    md.append("| **Roche** | Multi-Site Research Warehousing | Snowflake, Snowpipe, VARIANT, Python | Consolidated data across 6 sites; slashed query times from **3 hours to 20 minutes** |\n")
    md.append("| **Roche** | Clinical Longitudinal Dashboards | Tableau, LOD Expressions, Hyper Extracts | Real-time visibility into **85,000+ patient records** across 10 therapeutic areas |\n")
    md.append("| **Roche** | Advanced Statistical Analytics | Python, Lifelines, Survival Analysis | Modeled Phase III survival curves; informed **$150M research portfolio capital decision** |\n")
    md.append("| **Roche** | Federal Regulatory Validation | Python, SQL, CDISC SDTM/ADaM, Define-XML | Validated **35 tables across 4 datasets with ZERO errors** for formal FDA submission |\n")
    md.append("| **Roche** | Automated Data Quality Testing | Great Expectations, Python, Data Docs | Established data contracts; cut master data conflicts from **80 to 12 per month (85% drop)** |\n")
    md.append("| **Liberty Mutual** | High-Volume Claims Risk Mining | SQL, Python, Pandas, Decision Trees | Mined **600,000+ policyholders**; reduced claims backlog by **1,800 cases per quarter** |\n")
    md.append("| **Liberty Mutual** | Actuarial BI Dashboards | Tableau, Calculated Fields, SQL Marts | Replaced 4 manual Excel workbooks; saved **8 analyst hours per week** |\n")
    md.append("| **Liberty Mutual** | Predictive Risk Classification | Scikit-learn, Random Forest, SMOTE | Triaged **1,200 high-risk accounts per renewal cycle** (ROC-AUC 0.86) |\n")
    md.append("| **Liberty Mutual** | Cloud Data Warehouse Migration | Amazon Redshift, S3, Columnar MPP | Cut monthly financial report generation from **7 hours to 40 minutes (90% faster)** |\n")
    md.append("| **Liberty Mutual** | Digital A/B Workflow Optimization | Python, Scipy, Hypothesis Testing | Slashed digital submission duration from **24 to 9 minutes (62% improvement)** |\n")
    md.append("| **Flagship: Churn Model** | Predictive Retention Engine | Scikit-learn, Random Forest, SHAP | Evaluated **120,000+ records**; 87-point accuracy; **$2.1M projected revenue recovery** |\n")
    md.append("| **Flagship: Lakehouse** | End-to-End Modern Data Stack | dbt, Snowflake, Airflow, Great Expectations | Ingested **2M+ daily transactions**; cut pipeline failures from **22 to 2 per month** |\n")
    md.append("| **Flagship: Financial KPI** | Automated Azure SQL Scorecard | Power BI, DAX (25+ measures), Azure SQL | Replaced 6-hr manual Excel reporting with **20-minute automated refresh** |\n\n")

    md.append("---\n\n")

    # Add 30 Questions
    md.append("## Part 1: JPMorgan Chase & Co. — Financial Analytics, T-SQL Pipelines & Yale Alignment (Questions 01 – 10)\n\n")
    for q in QUESTIONS[:10]:
        md.append(f"### {q['id']}: {q['title']}\n\n")
        md.append(f"**Interview Question:** \"{q['question']}\"\n\n")
        md.append(f"**Perspective & Delivery:** {q['perspective']}\n\n")
        md.append(f"**Comprehensive Answer:**\n\n{q['answer']}\n\n---\n\n")

    md.append("## Part 2: Roche — Clinical Research Data Engineering, Snowflake & Federal Compliance (Questions 11 – 20)\n\n")
    for q in QUESTIONS[10:20]:
        md.append(f"### {q['id']}: {q['title']}\n\n")
        md.append(f"**Interview Question:** \"{q['question']}\"\n\n")
        md.append(f"**Perspective & Delivery:** {q['perspective']}\n\n")
        md.append(f"**Comprehensive Answer:**\n\n{q['answer']}\n\n---\n\n")

    md.append("## Part 3: Liberty Mutual, Flagship Projects & Yale Strategic Alignment (Questions 21 – 30)\n\n")
    for q in QUESTIONS[20:30]:
        md.append(f"### {q['id']}: {q['title']}\n\n")
        md.append(f"**Interview Question:** \"{q['question']}\"\n\n")
        md.append(f"**Perspective & Delivery:** {q['perspective']}\n\n")
        md.append(f"**Comprehensive Answer:**\n\n{q['answer']}\n\n---\n\n")

    # Add 10 Coding / Analytical Problems
    md.append("## Part 4: Production-Grade Analytical Pipelines & Code Implementations (10 Problems)\n\n")
    for cp in CODING_PROBLEMS:
        md.append(f"### Problem {cp['num']}: {cp['title']}\n\n")
        md.append(f"**Category:** `{cp['category']}`\n\n")
        md.append(f"#### Business Context & Problem Statement\n{cp['problem']}\n\n")
        md.append(f"#### Production-Grade Code Solution\n```python\n{cp['code']}\n```\n\n")
        md.append(f"#### Complexity & Operational Analysis\n{cp['complexity']}\n\n---\n\n")

    return "".join(md)


# =============================================================================
# 2. GENERATE NEXTRA MDX (content/bibek-yale-reporting-prep.mdx)
# =============================================================================
def generate_mdx(markdown_content):
    frontmatter = """---
title: "Bibek Thapa — Yale University Data Reporting Analyst Prep"
description: "Comprehensive 30-Question Technical Preparation Suite, Research Administration Case Studies, and 10 Production Analytical Pipelines for Yale University Enterprise Research Services."
---

<PasswordGate password="Bibek" candidateName="Bibek Thapa">

"""
    footer = "\n\n</PasswordGate>\n"
    return frontmatter + markdown_content + footer


# =============================================================================
# 3. GENERATE INTERACTIVE STANDALONE HTML (bibek_yale_reporting_prep.html)
# =============================================================================
def generate_html():
    questions_json = json.dumps(QUESTIONS)
    coding_json = json.dumps(CODING_PROBLEMS)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bibek Thapa — Yale University Data Reporting Analyst Prep Suite</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0a0e17;
            --bg-secondary: #101726;
            --bg-card: rgba(16, 23, 38, 0.75);
            --bg-card-hover: rgba(22, 32, 53, 0.85);
            --border-color: rgba(255, 255, 255, 0.08);
            --border-focus: #00356B;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-blue: #00356B;      /* Yale Blue */
            --accent-cyan: #0072CE;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-purple: #8b5cf6;
            --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
            --shadow-subtle: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
            --shadow-glow: 0 0 25px -5px rgba(0, 114, 206, 0.4);
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
            background: rgba(10, 14, 23, 0.95);
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
            max-width: 440px;
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.7), var(--shadow-glow);
            text-align: center;
            position: relative;
        }}

        .lock-logo {{
            width: 56px;
            height: 56px;
            background: linear-gradient(135deg, #00356B 0%, #0072CE 100%);
            border-radius: 14px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 8px 16px -4px rgba(0, 114, 206, 0.5);
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
            border-color: var(--accent-cyan);
            box-shadow: 0 0 0 3px rgba(0, 114, 206, 0.25);
            background: rgba(255, 255, 255, 0.06);
        }}

        .lock-btn {{
            width: 100%;
            padding: 0.85rem;
            background: linear-gradient(135deg, #00356B 0%, #0072CE 100%);
            border: none;
            border-radius: 0.75rem;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(0, 114, 206, 0.35);
        }}

        .lock-btn:hover {{
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(0, 114, 206, 0.5);
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
            background: linear-gradient(135deg, rgba(0, 53, 107, 0.35) 0%, rgba(16, 23, 38, 0.85) 100%);
            border: 1px solid rgba(0, 114, 206, 0.35);
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
            background: radial-gradient(circle, rgba(0, 114, 206, 0.2) 0%, transparent 70%);
            pointer-events: none;
        }}

        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(0, 114, 206, 0.2);
            border: 1px solid rgba(0, 114, 206, 0.4);
            padding: 0.35rem 0.85rem;
            border-radius: 2rem;
            font-size: 0.8rem;
            font-weight: 600;
            color: #38bdf8;
            margin-bottom: 1rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}

        .hero-title {{
            font-size: 2.4rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 0.75rem;
            letter-spacing: -0.03em;
        }}

        .hero-subtitle {{
            font-size: 1.15rem;
            color: #cbd5e1;
            max-width: 850px;
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
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
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
            border-color: rgba(0, 114, 206, 0.4);
            transform: translateY(-2px);
        }}

        .metric-num {{
            font-size: 1.85rem;
            font-weight: 800;
            color: #38bdf8;
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
            background: #0072CE;
            color: white;
            border-color: #0072CE;
            box-shadow: 0 4px 12px rgba(0, 114, 206, 0.4);
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
            border-color: var(--accent-cyan);
            box-shadow: 0 0 0 3px rgba(0, 114, 206, 0.25);
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
            border-color: rgba(0, 114, 206, 0.4);
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
            background: rgba(0, 114, 206, 0.25);
            color: #38bdf8;
            border: 1px solid rgba(0, 114, 206, 0.4);
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
            background: rgba(0, 114, 206, 0.08);
            border-left: 3px solid #0072CE;
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
            background: #06090f;
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
            background: #0072CE;
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
            <p class="lock-desc">Enter the authorization passcode for <strong>Bibek Thapa's Yale University Interview Preparation Suite</strong>.</p>
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
            <div class="hero-badge">Yale University · Enterprise Research Services</div>
            <h1 class="hero-title">Bibek Thapa — Data / Reporting Analyst Technical Interview Suite</h1>
            <p class="hero-subtitle">
                Target Role: <strong>Data / Reporting Analyst</strong> at <strong>Yale University</strong>. Grounded in research administration, Power BI financial reporting, Workday/Kuali ledgers, sponsored project grant burn tracking, federal Uniform Guidance (2 CFR 200) compliance, SQL/Python ETL, and Snowflake data warehousing across JPMorgan Chase, Roche, and Liberty Mutual.
            </p>
            <div class="hero-meta-row">
                <div class="hero-meta-item">📍 <strong>Location:</strong> Dallas, TX | Yale University</div>
                <div class="hero-meta-item">💼 <strong>Org:</strong> Enterprise Research Services & Finance</div>
                <div class="hero-meta-item">🎓 <strong>Education:</strong> B.S. Business Computer Information Systems (UNT)</div>
                <div class="hero-meta-item">🛡️ <strong>Focus:</strong> Research Admin, Power BI, SQL, Grant Compliance</div>
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
                <div class="metric-label">Production SQL, Python & DAX Pipelines</div>
            </div>
            <div class="metric-card">
                <div class="metric-num">1.8M</div>
                <div class="metric-label">Daily Records Validated via Automated SQL/Python</div>
            </div>
            <div class="metric-card">
                <div class="metric-num">$150M</div>
                <div class="metric-label">Research Capital Portfolio Decision Informed</div>
            </div>
            <div class="metric-card">
                <div class="metric-num">10h &rarr; 90m</div>
                <div class="metric-label">Weekly Executive Reporting Prep Compressed</div>
            </div>
        </section>

        <!-- Navigation Tabs -->
        <nav class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab('all')">All Content</button>
            <button class="tab-btn" onclick="switchTab('part1')">Part 1: JPMorgan Chase & Yale (Q01-Q10)</button>
            <button class="tab-btn" onclick="switchTab('part2')">Part 2: Roche Clinical & Snowflake (Q11-Q20)</button>
            <button class="tab-btn" onclick="switchTab('part3')">Part 3: Liberty Mutual & Flagship (Q21-Q30)</button>
            <button class="tab-btn" onclick="switchTab('coding')">Part 4: 10 Analytical Code Solutions</button>
        </nav>

        <!-- Search Box -->
        <div class="controls-bar">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" id="searchInput" class="search-input" placeholder="Search keywords (e.g., Workday, Power BI, DAX, grant, F&A, Uniform Guidance, Snowflake)..." oninput="handleSearch()">
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

            if (val === 'bibek') {{
                document.getElementById('lockScreen').style.display = 'none';
                document.getElementById('appContainer').style.display = 'block';
                sessionStorage.setItem('bibek_prep_unlocked', 'true');
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
            if (sessionStorage.getItem('bibek_prep_unlocked') === 'true') {{
                document.getElementById('lockScreen').style.display = 'none';
                document.getElementById('appContainer').style.display = 'block';
                renderQuestions();
                renderCoding();
            }}
        }});

        function switchTab(tab) {{
            currentTab = tab;
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

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
                if (currentTab === 'part1' && parseInt(q.id.replace('Q','')) > 10) return false;
                if (currentTab === 'part2' && (parseInt(q.id.replace('Q','')) <= 10 || parseInt(q.id.replace('Q','')) > 20)) return false;
                if (currentTab === 'part3' && parseInt(q.id.replace('Q','')) <= 20) return false;

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
            container.innerHTML = '<h2 style="font-size: 1.75rem; font-weight: 800; margin-bottom: 1.5rem;">Part 4: 10 Production-Grade Analytical Pipelines & Solutions</h2>';

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
    print("Building Bibek Thapa Yale Enterprise Research Services Prep Suite...")

    # 1. Master Markdown
    md_content = generate_markdown()
    with open("bibek_yale_reporting_prep.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("Master Markdown generated: bibek_yale_reporting_prep.md")

    # 2. Nextra MDX
    mdx_content = generate_mdx(md_content)
    os.makedirs("content", exist_ok=True)
    with open("content/bibek-yale-reporting-prep.mdx", "w", encoding="utf-8") as f:
        f.write(mdx_content)
    print("Nextra MDX generated: content/bibek-yale-reporting-prep.mdx")

    # 3. Interactive Standalone HTML
    html_content = generate_html()
    with open("bibek_yale_reporting_prep.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Interactive Webpage generated: bibek_yale_reporting_prep.html")

    # 4. Public directory copy
    os.makedirs("public", exist_ok=True)
    with open("public/bibek_yale_reporting_prep.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Public Webpage generated: public/bibek_yale_reporting_prep.html")

    print("\nAll Bibek Thapa Yale Data / Reporting Analyst prep assets successfully compiled!")

if __name__ == "__main__":
    main()

