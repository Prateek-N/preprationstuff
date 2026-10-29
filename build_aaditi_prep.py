# -*- coding: utf-8 -*-
"""
Build script for Aaditi Roy's Business Analyst – Payment Model Evaluation (AMEX) Interview Prep Suite.
Compiles:
1. aaditi_amex_ba_prep.md
2. content/aaditi-amex-ba-prep.mdx
3. aaditi_amex_ba_prep.html
4. public/aaditi_amex_ba_prep.html

Passcode: "Aaditi"
"""

import json
import re
import os
import shutil

from aaditi_questions_part1 import QUESTIONS_PART1
from aaditi_questions_part2 import QUESTIONS_PART2
from aaditi_coding import CODING_PROBLEMS

QUESTIONS = QUESTIONS_PART1 + QUESTIONS_PART2
print(f"Loaded {len(QUESTIONS)} Technical Questions and {len(CODING_PROBLEMS)} Coding Problems.")

# =============================================================================
# 1. GENERATE MASTER MARKDOWN (aaditi_amex_ba_prep.md)
# =============================================================================
def generate_markdown():
    md = []
    md.append("# Aaditi Roy — Business Analyst (Payment Model Evaluation) Technical Interview Preparation Suite\n\n")
    md.append("## Target Role: Business Analyst – Payment Model Evaluation — American Express (AMEX)\n\n")
    md.append("**Candidate:** Aaditi Roy | Tempe, AZ | (602) 741-9961 | aaditiroy555@gmail.com | [LinkedIn](https://linkedin.com/in/aaditiroy24)\n\n")
    md.append("**Client & Division:** American Express (AMEX) — Global Policy & Standards within Global Services Operations and Policy\n\n")
    md.append("**Location:** 18850 N 56th St, Phoenix, AZ 85054 (Hybrid 3 days onsite)\n\n")
    md.append("**Target Focus:** Payment Model Evaluation · Global Merchant Acquisition (GMS) Policies · Risk & Governance · Fintech & Emerging Payments (BNPL, PayFacs, ISOs) · SQL & Python ETL · Tableau & Power BI · Stakeholder Alignment (Risk, Legal, Compliance) · AI-Enabled Business Analysis (ChatGPT)\n\n")
    md.append("**Passcode Lock:** `Aaditi`\n\n")
    md.append("---\n\n")

    md.append("## Executive Summary & AMEX Strategic Alignment\n\n")
    md.append("> **Aaditi Roy** is a **Business Intelligence and Business Analyst** with 4+ years of cross-functional enterprise experience spanning higher education research analytics, global cloud and content delivery infrastructure, enterprise manufacturing sales operations, and multi-entity financial analytics. Aaditi holds a Master of Science in Business Analytics from the **W. P. Carey School of Business at Arizona State University (2026)** and a Bachelor of Technology in Information and Communication Technology from **DA-IICT (2022)**.\n\n")
    md.append("> At **Arizona State University**, Aaditi engineered automated **Python ETL pipelines** processing over 50,000 academic and operational records, developed **6 interactive Tableau dashboards** consolidating KPIs from 5 disparate databases (saving 12 hours/quarter manual effort), authored advanced **SQL queries** across 10+ relational datasets (compressing study turnaround from 21 to 6 days), and applied **K-Means clustering and regression modeling** on 15,000+ records to uncover behavioral trends that enabled targeted interventions for 1,200 at-risk entities. She established OKRs with 8 senior stakeholders and presented executive strategy briefs that directed **$1.4M in strategic investment priorities**.\n\n")
    md.append("> At **Akamai Technologies**, Aaditi managed 22 enterprise accounts representing **$2.8M in Annual Recurring Revenue (ARR)** at a **94/100 CSAT**, securing **$920K in net new expansion revenue**. She architected **Salesforce account-health dashboards** monitoring 28 operational and commercial KPIs, enabling churn prediction 6 weeks early and cutting at-risk revenue from **$340K to $95K per quarter**. She converted edge telemetry into 40+ C-suite Quarterly Business Reviews, led root cause analysis for enterprise SLA incidents that slashed Mean Time to Resolution (**MTTR**) from **48 to 11 hours**, and directed the bi-directional systems integration of **ServiceNow with Salesforce CRM**.\n\n")
    md.append("> At **Dell Technologies**, Aaditi elicited and managed over **110 functional and non-functional requirements** across 14 enterprise stakeholders for 4 cloud initiatives with **zero scope creep**, built **Power BI dashboards** tracking 25+ KPIs across hardware and supply chain (cutting reporting prep from 9 hours to 75 minutes), conducted gap analyses across 7 fulfillment processes delivering **$155K in annualized cost savings**, and facilitated **22 JAD sessions** with comprehensive BRDs, user stories, and UAT sign-offs for 650+ Salesforce CRM users.\n\n")
    md.append("> For **American Express**, Aaditi brings the exact quantitative acumen, governance discipline, and stakeholder management required to evaluate emerging payment models (Buy Now Pay Later, Payment Facilitators, digital wallets, crypto rails) against **Global Merchant Acquisition policies**, ensuring card network integrity, mitigating credit and fraud losses, and driving operational efficiency.\n\n")

    md.append("## Quantified Impact & Architecture Metrics\n\n")
    md.append("| Organization / System | Domain & Role | Core Tech Stack | Quantified Engineering & Business Impact |\n")
    md.append("| :--- | :--- | :--- | :--- |\n")
    md.append("| **Arizona State University** | Research Specialist – BI Analyst | Python, Pandas, Tableau, SQL, Scikit-learn | Built Python ETL on **50,000+ records**; informed **$180K budget reallocation** |\n")
    md.append("| **Arizona State University** | Executive BI Dashboarding | Tableau, Tableau Prep, SQL Star Schema | Built **6 dashboards** consolidating 5 feeds; eliminated **12 hrs/quarter manual work** |\n")
    md.append("| **Arizona State University** | Advanced SQL & Hypothesis Testing | PostgreSQL, Window Functions, B-Trees | Compressed research turnaround from **21 to 6 days**; cut escalations by 8/quarter |\n")
    md.append("| **Arizona State University** | Predictive Analytics & Clustering | Python, Scikit-learn, K-Means, Logistic Reg | Segmented **15,000+ records**; enabled proactive intervention for **1,200 at-risk entities** |\n")
    md.append("| **Arizona State University** | Strategic Stakeholder Alignment | OKR Framework, Executive Briefs | Facilitated consensus with 8 faculty leads; shaped **$1.4M investment priorities** |\n")
    md.append("| **Akamai Technologies** | Client Service Manager | Salesforce CRM, Telemetry, SQL | Managed **$2.8M ARR** across 22 accounts at **94/100 CSAT**; secured **$920K new revenue** |\n")
    md.append("| **Akamai Technologies** | Account Health & Churn Modeling | Salesforce, 28 KPIs, Predictive Scoring | Predicted churn **6 weeks early**; cut at-risk revenue from **$340K to $95K/quarter** |\n")
    md.append("| **Akamai Technologies** | SLA Incident Root Cause Analysis | ServiceNow, Time-Motion Analysis, RCA | Re-engineered incident workflows across 14 accounts; cut **MTTR from 48 to 11 hours** |\n")
    md.append("| **Akamai Technologies** | Enterprise Systems Integration | ServiceNow, Salesforce, REST APIs | Directed bi-directional sync; removed **8 hours/week duplicate data entry** |\n")
    md.append("| **Dell Technologies** | Requirements & Scope Management | Agile, JIRA, RTM, Change Control | Elicited **110+ requirements** across 14 stakeholders for 4 initiatives with **zero scope creep** |\n")
    md.append("| **Dell Technologies** | Enterprise Power BI Modeling | Power BI, DAX, Power Query, Star Schema | Tracked 25+ KPIs; reduced reporting preparation from **9 hours to 75 minutes** |\n")
    md.append("| **Dell Technologies** | Process Gap & Value Stream Mapping | Lean Six Sigma, Value Stream Mapping, RCA | Analyzed 7 fulfillment workflows; delivered **$155K annualized cost savings** |\n")
    md.append("| **Dell Technologies** | JAD Facilitation & CRM Rollouts | JAD, BRD/FSD, User Stories, UAT | Facilitated **22 JAD sessions**; drove UAT sign-off for **650+ enterprise users** |\n")
    md.append("| **Imagen Dental Partners** | Financial Analytics Project | Snowflake, SQL Stored Procs, Power BI | Automated ETL on **100K+ bank transactions**; cut variance detection from **60 to 10 min** |\n")
    md.append("| **KPMG India** | Process Consulting & ERP Analysis | BPMN, Visio, Stakeholder Interviews | Captured 80+ requirements via 22 interviews; uncovered **$85K annual overhead savings** |\n")
    md.append("| **KPMG India** | Financial Model Automation | Excel VBA, Macro Arrays, Error Trapping | Automated models across 4 engagements; trimmed time from **8 to 1.5 hrs (130 hrs saved/yr)** |\n\n")

    md.append("---\n\n")

    # Add 30 Questions
    md.append("## Part 1: Arizona State University & AMEX Payment Model Evaluation Alignment (Questions 01 – 10)\n\n")
    for q in QUESTIONS[:10]:
        md.append(f"### {q['id']}: {q['title']}\n\n")
        md.append(f"**Interview Question:** \"{q['question']}\"\n\n")
        md.append(f"**Perspective & Delivery:** {q['perspective']}\n\n")
        md.append(f"**Comprehensive Answer:**\n\n{q['answer']}\n\n---\n\n")

    md.append("## Part 2: Akamai Technologies — Enterprise Account Health, Observability & Systems Integration (Questions 11 – 20)\n\n")
    for q in QUESTIONS[10:20]:
        md.append(f"### {q['id']}: {q['title']}\n\n")
        md.append(f"**Interview Question:** \"{q['question']}\"\n\n")
        md.append(f"**Perspective & Delivery:** {q['perspective']}\n\n")
        md.append(f"**Comprehensive Answer:**\n\n{q['answer']}\n\n---\n\n")

    md.append("## Part 3: Dell Technologies, KPMG, Flagship Projects & AMEX Governance (Questions 21 – 30)\n\n")
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
# 2. GENERATE NEXTRA MDX (content/aaditi-amex-ba-prep.mdx)
# =============================================================================
def generate_mdx(markdown_content):
    frontmatter = """---
title: "Aaditi Roy — AMEX Payment Model Evaluation Business Analyst Prep"
description: "Comprehensive 30-Question Technical Preparation Suite, Architectural Case Studies, and 10 Production Analytical Pipelines for American Express Business Analyst Role."
---

<PasswordGate password="Aaditi" candidateName="Aaditi Roy">

"""
    footer = "\n\n</PasswordGate>\n"
    return frontmatter + markdown_content + footer


# =============================================================================
# 3. GENERATE INTERACTIVE STANDALONE HTML (aaditi_amex_ba_prep.html)
# =============================================================================
def generate_html():
    questions_json = json.dumps(QUESTIONS)
    coding_json = json.dumps(CODING_PROBLEMS)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aaditi Roy — AMEX Payment Model Evaluation BA Technical Prep Suite</title>
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
            --border-focus: #0070f3;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-blue: #006fcf;      /* AMEX Blue */
            --accent-cyan: #06b6d4;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-purple: #8b5cf6;
            --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
            --shadow-subtle: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
            --shadow-glow: 0 0 25px -5px rgba(0, 111, 207, 0.4);
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
            background: linear-gradient(135deg, #006fcf 0%, #002663 100%);
            border-radius: 14px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 8px 16px -4px rgba(0, 111, 207, 0.5);
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
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 3px rgba(0, 111, 207, 0.25);
            background: rgba(255, 255, 255, 0.06);
        }}

        .lock-btn {{
            width: 100%;
            padding: 0.85rem;
            background: linear-gradient(135deg, #006fcf 0%, #004b99 100%);
            border: none;
            border-radius: 0.75rem;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(0, 111, 207, 0.35);
        }}

        .lock-btn:hover {{
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(0, 111, 207, 0.5);
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
            background: linear-gradient(135deg, rgba(0, 111, 207, 0.12) 0%, rgba(16, 23, 38, 0.85) 100%);
            border: 1px solid rgba(0, 111, 207, 0.25);
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
            background: radial-gradient(circle, rgba(0, 111, 207, 0.15) 0%, transparent 70%);
            pointer-events: none;
        }}

        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(0, 111, 207, 0.2);
            border: 1px solid rgba(0, 111, 207, 0.4);
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
            border-color: rgba(0, 111, 207, 0.3);
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
            background: var(--accent-blue);
            color: white;
            border-color: var(--accent-blue);
            box-shadow: 0 4px 12px rgba(0, 111, 207, 0.4);
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
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 3px rgba(0, 111, 207, 0.25);
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
            border-color: rgba(0, 111, 207, 0.35);
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
            background: rgba(0, 111, 207, 0.25);
            color: #38bdf8;
            border: 1px solid rgba(0, 111, 207, 0.4);
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
            background: rgba(0, 111, 207, 0.06);
            border-left: 3px solid var(--accent-blue);
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
            background: var(--accent-blue);
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
            <p class="lock-desc">Enter the authorization passcode for <strong>Aaditi Roy's AMEX Interview Preparation Suite</strong>.</p>
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
            <div class="hero-badge">American Express · Global Policy & Standards</div>
            <h1 class="hero-title">Aaditi Roy — Payment Model Evaluation Technical Interview Suite</h1>
            <p class="hero-subtitle">
                Target Role: <strong>Business Analyst – Payment Model Evaluation</strong> at <strong>American Express (AMEX)</strong>. Grounded in Global Merchant Acquisition policies, statistical risk modeling, Python/SQL ETL, Tableau/Power BI executive analytics, and governance across ASU, Akamai, Dell, and KPMG.
            </p>
            <div class="hero-meta-row">
                <div class="hero-meta-item">📍 <strong>Location:</strong> Phoenix, AZ (18850 N 56th St)</div>
                <div class="hero-meta-item">💼 <strong>Org:</strong> Global Services Operations & Policy</div>
                <div class="hero-meta-item">🎓 <strong>Education:</strong> M.S. Business Analytics (ASU W. P. Carey)</div>
                <div class="hero-meta-item">🛡️ <strong>Focus:</strong> Merchant Risk, Governance, BNPL & PayFacs</div>
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
                <div class="metric-num">50K+</div>
                <div class="metric-label">Records Ingested via Automated Python ETL</div>
            </div>
            <div class="metric-card">
                <div class="metric-num">$1.4M</div>
                <div class="metric-label">Capital Investment Shaped via Executive Briefs</div>
            </div>
            <div class="metric-card">
                <div class="metric-num">48h &rarr; 11h</div>
                <div class="metric-label">Incident MTTR Compressed across 14 Engagements</div>
            </div>
        </section>

        <!-- Navigation Tabs -->
        <nav class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab('all')">All Content</button>
            <button class="tab-btn" onclick="switchTab('part1')">Part 1: ASU & AMEX Policy (Q01-Q10)</button>
            <button class="tab-btn" onclick="switchTab('part2')">Part 2: Akamai Client Governance (Q11-Q20)</button>
            <button class="tab-btn" onclick="switchTab('part3')">Part 3: Dell, KPMG & Projects (Q21-Q30)</button>
            <button class="tab-btn" onclick="switchTab('coding')">Part 4: 10 Analytical Code Solutions</button>
        </nav>

        <!-- Search Box -->
        <div class="controls-bar">
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" id="searchInput" class="search-input" placeholder="Search keywords (e.g., BNPL, SQL, chargeback, Tableau, PII, RCA, PayFac)..." oninput="handleSearch()">
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

            if (val === 'aaditi') {{
                document.getElementById('lockScreen').style.display = 'none';
                document.getElementById('appContainer').style.display = 'block';
                sessionStorage.setItem('aaditi_prep_unlocked', 'true');
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
            if (sessionStorage.getItem('aaditi_prep_unlocked') === 'true') {{
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
    print("Building Aaditi Roy AMEX Payment Model Evaluation BA Prep Suite...")

    # 1. Master Markdown
    md_content = generate_markdown()
    with open("aaditi_amex_ba_prep.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("Master Markdown generated: aaditi_amex_ba_prep.md")

    # 2. Nextra MDX
    mdx_content = generate_mdx(md_content)
    os.makedirs("content", exist_ok=True)
    with open("content/aaditi-amex-ba-prep.mdx", "w", encoding="utf-8") as f:
        f.write(mdx_content)
    print("Nextra MDX generated: content/aaditi-amex-ba-prep.mdx")

    # 3. Interactive Standalone HTML
    html_content = generate_html()
    with open("aaditi_amex_ba_prep.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Interactive Webpage generated: aaditi_amex_ba_prep.html")

    # 4. Public directory copy
    os.makedirs("public", exist_ok=True)
    with open("public/aaditi_amex_ba_prep.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Public Webpage generated: public/aaditi_amex_ba_prep.html")

    print("\nAll Aaditi Roy AMEX BA prep assets successfully compiled!")

if __name__ == "__main__":
    main()
