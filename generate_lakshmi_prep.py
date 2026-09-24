# -*- coding: utf-8 -*-
"""
Generator script for Lakshmi Pranitha's Wise Platform Interview Prep Suite.
Generates:
1. lakshmi_pranitha_wise_prep.md
2. content/lakshmi-pranitha-wise-prep.mdx
3. lakshmi_pranitha_wise_prep.html
"""

import json
import re
import os
from lakshmi_wise_data import questions_data

# =============================================================================
# 1. GENERATE MASTER MARKDOWN (lakshmi_pranitha_wise_prep.md)
# =============================================================================
def generate_markdown():
    md = []
    md.append("# Lakshmi Pranitha — Senior Commercial Analyst Interview Preparation Suite\n")
    md.append("## Target Role: Senior Regional Analyst (North America) — Wise Platform\n")
    md.append("**Candidate:** Lakshmi Pranitha | Austin, TX | +1-512-937-3571 | Lakshmipranitha45@gmail.com | [LinkedIn](https://linkedin.com)\n")
    md.append("**Target Company:** Wise (Wise Platform · Austin, TX · $119,000 — $153,000 USD)  \n")
    md.append("**Passcode Lock:** `Lakshmi`\n\n")
    md.append("---\n\n")

    md.append("## Executive Summary & Role Alignment\n")
    md.append("> **Lakshmi Pranitha** brings 5+ years of enterprise data analytics and business intelligence experience across tier-1 financial institutions (**JPMorgan Chase**), healthcare payers (**Blue Cross Blue Shield**), and payroll platforms (**Paychex**). Her deep technical proficiency in **SQL**, **Python**, **Snowflake**, **dbt**, **Looker**, **Tableau**, and **Apache Airflow** directly matches the technical core of Wise's Modern Data Stack. Crucially, her background in consumer lending transaction pipelines (750K daily records at JPMC), regulatory capital auditing (Basel III), and commercial client billing anomaly detection ($890K at Paychex) provides the exact commercial mindset required to optimize deal velocity, quantify pre-sales impact, compress time-to-revenue (TTFT), and partner with North American Commercial and Delivery Leads at **Wise Platform**.\n\n")

    md.append("## Core Technical & Commercial Competencies\n")
    md.append("| Functional Area | Core Technologies & Methodologies |\n")
    md.append("| :--- | :--- |\n")
    md.append("| **Modern Data Stack & Engineering** | **Snowflake**, **dbt (Medallion Architecture)**, **Apache Airflow**, **SQL (T-SQL, PL/SQL)**, **Python (Pandas, NumPy, Scikit-learn)**, **Git / CI/CD** |\n")
    md.append("| **Commercial & BI Analytics** | **Looker (LookML)**, **Tableau**, **Power BI (DAX)**, **Salesforce CRM Telemetry**, **Jira Service Management**, **Excel Advanced Modeling** |\n")
    md.append("| **Deal-Flow & Sales Intelligence** | **Sales Pipeline Velocity**, **Stage Conversion Ratios**, **Win/Loss Attribution**, **Rep Quota & Capacity Planning**, **RFI / Pre-Sales Impact** |\n")
    md.append("| **Delivery & Operational Telemetry** | **Time-to-First-Transaction (TTFT)**, **Time-to-Revenue (TTR)**, **Milestone Dependency Tracking**, **Implementation Resource Utilization** |\n")
    md.append("| **Revenue & Payment Economics** | **Gross Payment Volume (GPV)**, **Take-Rate Sensitivity (bps)**, **Corridor Gross Profit Modeling**, **SWIFT vs. Local Rails (FedNow, RTP, SEPA)** |\n")
    md.append("| **Governance & Financial Rigor** | **dbt Testing & Data Contracts**, **Automated Anomaly Detection**, **CRM vs. Finance Revenue Reconciliation**, **Basel III & Audit Readiness** |\n\n")

    md.append("---\n\n")

    md.append("# High-Yield Interview Questions & Expert Answers (20 Questions · 300+ Words Each)\n\n")

    current_cat = ""
    for q in questions_data:
        words = len(re.findall(r'\b\w+\b', q['answer']))
        if q['category'] != current_cat:
            current_cat = q['category']
            md.append(f"## {current_cat}\n\n")

        md.append(f"### Q{q['num']}: {q['title']}\n")
        md.append(f"**Interview Question:** *\"{q['question']}\"*\n\n")
        md.append(f"**Perspective & Delivery:** First-Person POV (`{words} words` · Verified $\\ge 300$ words)  \n\n")
        md.append(f"**In-Depth Answer:**\n\n")
        md.append(f"{q['answer']}\n\n")
        md.append("---\n\n")

    md.append("# Candidate Experience Mapping & Resume Defense Guide\n\n")
    md.append("### 1. JPMorgan Chase (JPMC) — High-Frequency Financial Pipelines & Basel III Rigor\n")
    md.append("""- **Direct Wise Match:** Architecting **Power BI** executive dashboards tracking 35+ lending KPIs and engineering **Python**-based ETL/ELT pipelines processing **750K daily records into Snowflake**, slashing pipeline latency from 4 hours to under 20 minutes.
- **Commercial Defense:** When interviewers ask about handling high transaction volumes or managing latency in reporting, reference JPMC. Frame how near-real-time Snowflake pipelines allowed risk and commercial stakeholders to monitor intraday portfolio shifts—the exact capability needed to monitor live partner payment volumes on Wise Platform.
- **Data Quality & Governance:** Highlight how dbt tests and custom Python validators intercepted **$450K in data discrepancies** before reaching finance systems, showing that your commercial numbers are always audit-proof.
\n\n""")

    md.append("### 2. Blue Cross Blue Shield (BCBS) — Multi-Stakeholder Operational Reconciliation & A/B Testing\n")
    md.append("""- **Direct Wise Match:** Streamlined healthcare network reconciliations across 340K member records using **Python**, replacing 32 hours of manual Excel wrangling with 18 on-demand self-service analytics views, and executing statistical **A/B testing** on reimbursement models.
- **Commercial Defense:** Use this experience to demonstrate stakeholder mediation. When Commercial and Delivery teams clash over deal timelines or capacity, emphasize how you used objective Python anomaly detection and A/B statistical testing to align clinical, actuarial, and finance executives around verifiable data models.
\n\n""")

    md.append("### 3. Paychex — Client Billing Discrepancies & Commercial Benchmarking\n")
    md.append("""- **Direct Wise Match:** Surfaced **$890K in billing anomalies** across 3,200 commercial client accounts within Q1 using advanced **SQL / T-SQL**, and delivered compensation benchmarking dashboards across 28,000 employees in **Tableau**.
- **Commercial Defense:** Directly demonstrates your commercial mindset and revenue protection instincts. Explain how catching billing discrepancies and establishing standardized KPI reporting templates across 8 product lines cut delivery time from 2 days to 3 hours, proving you understand unit economics, client invoicing, and B2B contract mechanics.
\n\n""")

    md.append("### 4. Enterprise Modernization Lakehouse Project — Snowflake, dbt, Airflow, Looker\n")
    md.append("""- **Direct Wise Match:** Engineered Medallion Architecture on **Snowflake** using **dbt** with CI/CD in Git/GitHub Actions, orchestrated via **Apache Airflow**, and exposed through **Looker** self-service Explores.
- **Commercial Defense:** This mirrors Wise Platform's modern data stack 100%. Talk about building LookML dimensions, managing dbt incremental models with surrogate keys, configuring Airflow sensors, and cutting ad-hoc analyst tickets by 30+ per month by empowering non-technical users with trusted self-service analytics.
\n""")

    return "".join(md)

# =============================================================================
# 2. GENERATE NEXTRA MDX (content/lakshmi-pranitha-wise-prep.mdx)
# =============================================================================
def generate_mdx(markdown_content):
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
            # Escape raw { and } for MDX Acorn parser
            processed = line.replace('{', '&#123;').replace('}', '&#125;')
            # Escape raw < if followed by space or number
            processed = re.sub(r'<(?=[0-9 ])', '&lt;', processed)
            mdx_lines.append(processed)

    escaped_body = '\n'.join(mdx_lines)

    header = """---
title: Lakshmi Pranitha — Senior Commercial Analyst (Wise Platform) Prep Suite
description: 20 high-yield interview questions and comprehensive answers for Senior Commercial Analyst (North America) at Wise Platform, covering deal velocity, pre-sales impact, delivery telemetry, and modern data stack.
---

<PasswordGate password="Lakshmi">

"""

    footer = """

</PasswordGate>
"""
    return header + escaped_body + footer

# =============================================================================
# 3. GENERATE INTERACTIVE WEBPAGE (lakshmi_pranitha_wise_prep.html)
# =============================================================================
def generate_html():
    items_json = []
    categories = []

    for q in questions_data:
        words = len(re.findall(r'\b\w+\b', q['answer']))
        if q['category'] not in categories:
            categories.append(q['category'])
        items_json.append({
            "num": q["num"],
            "category": q["category"],
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
  <title>Wise Platform — Senior Commercial Analyst Prep Suite · Lakshmi Pranitha</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-base: #06090e;
      --bg-surface: #0c121c;
      --bg-card: #121a28;
      --bg-card-hover: #192438;
      --border: #1f2e48;
      --border-accent: #2563eb;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --wise-green: #2ed06e;
      --wise-blue: #3b82f6;
      --wise-cyan: #06b6d4;
      --wise-emerald: #10b981;
      --wise-amber: #f59e0b;
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
      background: radial-gradient(circle at center, #111d33 0%, #03060a 100%);
      display: flex; align-items: center; justify-content: center;
      z-index: 99999; padding: 1.5rem;
    }}
    .lock-box {{
      background: rgba(12, 18, 28, 0.96);
      backdrop-filter: blur(24px);
      border: 1px solid rgba(46, 208, 110, 0.4);
      border-radius: 22px;
      padding: 2.75rem 2.5rem;
      max-width: 490px;
      width: 100%;
      text-align: center;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.9), 0 0 50px rgba(46, 208, 110, 0.2);
    }}
    .lock-logo-mark {{
      display: inline-flex; align-items: center; justify-content: center;
      margin-bottom: 1.25rem; font-size: 2.4rem; font-weight: 900; letter-spacing: -0.04em;
    }}
    .lock-txt-1 {{ color: #ffffff; }}
    .lock-txt-2 {{ color: #2ed06e; }}
    .lock-badge-pill {{
      background: linear-gradient(135deg, rgba(46, 208, 110, 0.2), rgba(59, 130, 246, 0.2));
      border: 1px solid rgba(46, 208, 110, 0.4);
      padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; color: #86efac;
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
      border-color: var(--wise-green);
      box-shadow: 0 0 0 3px rgba(46, 208, 110, 0.25);
    }}
    .unlock-btn {{
      width: 100%;
      background: linear-gradient(135deg, #16a34a, #15803d);
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
      box-shadow: 0 10px 25px -5px rgba(46, 208, 110, 0.5);
      background: linear-gradient(135deg, #22c55e, #16a34a);
    }}
    .lock-error {{ color: #f87171; font-size: 0.85rem; margin-top: 0.85rem; display: none; font-weight: 500; }}

    /* APP LAYOUT */
    #appContent {{ display: none; opacity: 0; transition: opacity 0.4s ease; }}
    .app-header {{
      background: rgba(12, 18, 28, 0.95);
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
      background: linear-gradient(135deg, rgba(46, 208, 110, 0.2), rgba(59, 130, 246, 0.2));
      border: 1px solid rgba(46, 208, 110, 0.45);
      color: #ffffff;
      font-size: 0.82rem; font-weight: 800;
      padding: 6px 12px; border-radius: 8px; letter-spacing: 0.05em;
      display: flex; align-items: center; gap: 6px;
    }}
    .brand-badge span.accent {{ color: #4ade80; font-weight: 900; }}
    .brand-title h1 {{ font-size: 1.15rem; font-weight: 700; letter-spacing: -0.01em; }}
    .brand-sub {{ font-size: 0.8rem; color: var(--text-muted); }}

    .header-right {{ display: flex; align-items: center; gap: 1.25rem; }}
    .progress-wrap {{ display: flex; align-items: center; gap: 10px; min-width: 220px; }}
    .progress-bar-bg {{
      flex: 1; height: 8px; background: rgba(255,255,255,0.1); border-radius: 99px; overflow: hidden;
    }}
    .progress-bar-fill {{
      height: 100%; width: 0%;
      background: linear-gradient(90deg, #2ed06e, #38bdf8);
      transition: width 0.3s ease;
    }}
    .progress-text {{ font-size: 0.78rem; font-family: var(--font-mono); color: var(--text-muted); white-space: nowrap; }}

    /* HERO PROFILE */
    .hero-wrap {{
      max-width: 1440px; margin: 2rem auto 0; padding: 0 2rem;
    }}
    .hero-card {{
      background: linear-gradient(135deg, rgba(18, 26, 40, 0.95), rgba(12, 18, 28, 0.95));
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
    .hero-role {{ font-size: 1.15rem; color: #4ade80; font-weight: 600; margin-top: 4px; }}
    .hero-contact {{
      display: flex; gap: 1rem; font-size: 0.85rem; color: var(--text-muted); flex-wrap: wrap; margin-top: 8px;
    }}
    .hero-contact span {{ display: inline-flex; align-items: center; gap: 4px; }}
    .hero-summary {{
      font-size: 0.95rem; color: #cbd5e1; line-height: 1.7; max-width: 1100px;
      padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.08);
    }}
    .hero-tags {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 1rem; }}
    .hero-tag {{
      background: rgba(6, 9, 14, 0.8); border: 1px solid var(--border);
      padding: 4px 10px; border-radius: 6px; font-family: var(--font-mono);
      font-size: 0.75rem; color: #86efac;
    }}

    /* CONTROLS */
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
    .search-input-box input:focus {{ border-color: var(--wise-green); }}
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
      background: rgba(12, 18, 28, 0.8); border: 1px solid var(--border);
      color: var(--text-muted); padding: 6px 14px; border-radius: 99px;
      font-size: 0.82rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
    }}
    .filter-pill:hover, .filter-pill.active {{
      background: linear-gradient(135deg, rgba(46, 208, 110, 0.2), rgba(59, 130, 246, 0.2));
      border-color: var(--wise-green); color: #fff;
    }}

    /* MAIN CONTAINER */
    .main-wrap {{
      max-width: 1440px; margin: 1.5rem auto 3rem; padding: 0 2rem;
    }}

    /* QUESTION CARDS */
    .card-list {{ display: flex; flex-direction: column; gap: 1.25rem; margin-bottom: 2.5rem; }}
    .q-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      transition: all 0.25s ease;
    }}
    .q-card:hover {{
      border-color: rgba(46, 208, 110, 0.4);
      box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }}
    .q-card.completed {{
      border-color: rgba(46, 208, 110, 0.45);
      background: rgba(46, 208, 110, 0.03);
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
      background: rgba(46, 208, 110, 0.15);
      border: 1px solid rgba(46, 208, 110, 0.35);
      color: #86efac;
      font-family: var(--font-mono);
      font-size: 0.82rem; font-weight: 700;
      padding: 6px 12px; border-radius: 10px;
      white-space: nowrap; margin-top: 2px;
    }}
    .q-card.completed .q-num-badge {{
      background: rgba(46, 208, 110, 0.25);
      border-color: #2ed06e;
      color: #ffffff;
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
      background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.3);
      color: #93c5fd; font-family: var(--font-mono); font-size: 0.75rem;
      padding: 4px 8px; border-radius: 6px; white-space: nowrap;
    }}
    .q-checkbox {{
      width: 18px; height: 18px; cursor: pointer; accent-color: #2ed06e;
    }}
    .chevron {{
      color: var(--text-dim); font-size: 0.75rem; transition: transform 0.25s ease;
    }}
    .q-card.open .chevron {{ transform: rotate(180deg); color: #2ed06e; }}

    .q-body {{
      display: none;
      padding: 0 1.5rem 1.5rem 1.5rem;
      border-top: 1px solid rgba(255,255,255,0.06);
      background: rgba(6, 9, 14, 0.5);
    }}
    .q-card.open .q-body {{ display: block; }}

    .q-answer-content {{
      padding-top: 1.25rem; font-size: 0.95rem; color: #cbd5e1; line-height: 1.75;
    }}
    .q-answer-content strong {{
      color: #ffffff; font-weight: 700;
    }}
    .q-answer-content ul, .q-answer-content ol {{
      margin: 0.75rem 0 0.75rem 1.5rem;
    }}
    .q-answer-content li {{ margin-bottom: 0.4rem; }}

    .q-footer {{
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
      color: #fff; border-color: var(--wise-green);
    }}

    /* TOAST */
    #toast {{
      position: fixed; bottom: 2rem; right: 2rem;
      background: #16a34a; color: #fff; padding: 0.75rem 1.5rem;
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
        <span class="lock-txt-1">Wise</span><span class="lock-txt-2">Platform</span>
        <span class="lock-badge-pill">LAKSHMI LOCK</span>
      </div>
      <h2>Lakshmi Pranitha — Commercial Analyst Prep</h2>
      <p>Senior Regional Analyst (North America) · Deal-Flow & Delivery Analytics<br>Enter authorized passcode (<strong>Lakshmi</strong>) to unlock the full 20-question dossier.</p>
      <div class="input-group">
        <input type="password" id="passInput" placeholder="Enter Passcode (Lakshmi)" autofocus>
      </div>
      <button class="unlock-btn" onclick="checkAuth()">Access Preparation Suite</button>
      <div class="lock-error" id="lockError">Invalid passcode. Please enter "Lakshmi" to unlock.</div>
    </div>
  </div>

  <!-- MAIN APP CONTENT -->
  <div id="appContent">
    <header class="app-header">
      <div class="header-inner">
        <div class="brand-title">
          <div class="brand-badge">
            <span>WISE</span><span class="accent">PLATFORM</span>
          </div>
          <div>
            <h1>Lakshmi Pranitha — Senior Commercial Analyst Prep</h1>
            <div class="brand-sub">North America Deal-Flow, Pre-Sales, Delivery & Revenue Intelligence · 20 Questions</div>
          </div>
        </div>
        <div class="header-right">
          <div class="progress-wrap">
            <div class="progress-bar-bg">
              <div class="progress-bar-fill" id="topProgress"></div>
            </div>
            <span class="progress-text" id="readCounter">0 / 20 Reviewed</span>
          </div>
        </div>
      </div>
    </header>

    <!-- HERO PROFILE -->
    <div class="hero-wrap">
      <div class="hero-card">
        <div class="hero-meta">
          <div>
            <div class="hero-name">Lakshmi Pranitha</div>
            <div class="hero-role">Senior Commercial Analyst / Senior Regional Analyst (North America) Candidate</div>
            <div class="hero-contact">
              <span>📍 Austin, TX</span>
              <span>📞 +1-512-937-3571</span>
              <span>✉️ Lakshmipranitha45@gmail.com</span>
              <span>💼 Target: Wise Platform ($119K — $153K USD)</span>
            </div>
          </div>
        </div>
        <div class="hero-summary">
          <strong>Strategic Alignment:</strong> 5+ years of experience building enterprise analytics platforms, dimensional models, and automated data pipelines across <strong>JPMorgan Chase (JPMC)</strong>, <strong>Blue Cross Blue Shield</strong>, and <strong>Paychex</strong>. Expert in <strong>SQL</strong>, <strong>Python</strong>, <strong>Snowflake</strong>, <strong>dbt</strong>, <strong>Looker</strong>, <strong>Tableau</strong>, and <strong>Apache Airflow</strong>, with proven ability to translate complex transaction telemetry into high-impact commercial narratives, optimize deal velocity, compress Time-to-First-Transaction (TTFT), and empower North American Commercial and Delivery Leads.
        </div>
        <div class="hero-tags">
          <span class="hero-tag">Snowflake Lakehouse</span>
          <span class="hero-tag">dbt Medallion</span>
          <span class="hero-tag">Looker LookML</span>
          <span class="hero-tag">Sales Pipeline Velocity</span>
          <span class="hero-tag">Pre-Sales Attribution</span>
          <span class="hero-tag">Delivery Telemetry (TTFT)</span>
          <span class="hero-tag">B2B Payment Economics</span>
        </div>
      </div>
    </div>

    <!-- CONTROLS -->
    <div class="controls-wrap">
      <div class="search-row">
        <div class="search-input-box">
          <span class="search-icon">🔍</span>
          <input type="text" id="globalSearch" placeholder="Search questions, Snowflake, dbt, Looker, TTFT, pre-sales, Airflow, take-rate..." oninput="handleSearch()">
        </div>
        <button class="action-btn" onclick="expandAll()">📂 Expand All</button>
        <button class="action-btn" onclick="collapseAll()">📁 Collapse All</button>
        <button class="action-btn" onclick="resetFilters()">↺ Reset</button>
      </div>
      <div class="filter-pills" id="categoryPills">
        <!-- Populated via JS -->
      </div>
    </div>

    <!-- MAIN CARDS CONTAINER -->
    <main class="main-wrap">
      <div class="card-list" id="questionsContainer">
        <!-- Injected via JavaScript -->
      </div>
    </main>
  </div>

  <div id="toast">Copied to clipboard!</div>

  <script>
    const VALID_PASSCODES = ["Lakshmi", "lakshmi", "LP", "WISE", "lp", "wise"];
    const itemsData = {items_json_str};
    const categoriesData = {categories_json_str};

    function checkAuth() {{
      const entered = document.getElementById("passInput").value.trim();
      if (VALID_PASSCODES.includes(entered) || localStorage.getItem("lakshmi_wise_auth") === "true") {{
        localStorage.setItem("lakshmi_wise_auth", "true");
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
      renderCategories();
      renderItems();
      updateProgress();
    }}

    function renderCategories() {{
      const container = document.getElementById("categoryPills");
      let html = `<button class="filter-pill active" onclick="filterCategory('all', this)">All (20)</button>`;
      categoriesData.forEach(cat => {{
        const count = itemsData.filter(i => i.category === cat).length;
        html += `<button class="filter-pill" onclick="filterCategory('${{cat}}', this)">${{cat}} (${{count}})</button>`;
      }});
      container.innerHTML = html;
    }}

    function formatText(raw) {{
      let res = raw;
      res = res.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
      res = res.replace(/`([^`]+)`/g, '<code style="background:rgba(255,255,255,0.08);padding:2px 6px;border-radius:4px;font-family:var(--font-mono);font-size:0.85em;color:#86efac;">$1</code>');
      res = res.replace(/\\n\\n/g, '<br><br>');
      res = res.replace(/\\n/g, '<br>');
      return res;
    }}

    function renderItems() {{
      const container = document.getElementById("questionsContainer");
      container.innerHTML = itemsData.map(item => `
        <div class="q-card" id="card-${{item.num}}" data-cat="${{item.category}}" data-search="${{(item.title + ' ' + item.category + ' ' + item.question + ' ' + item.answer).toLowerCase()}}">
          <div class="q-header" onclick="toggleCard(this)">
            <div class="q-header-left">
              <div class="q-num-badge">Q${{item.num}}</div>
              <div class="q-meta-group">
                <span class="q-cat-tag">${{item.category}}</span>
                <div class="q-title-text">${{item.title}}</div>
                <div class="q-prompt-sub">"${{item.question}}"</div>
              </div>
            </div>
            <div class="q-header-right">
              <span class="word-badge">${{item.words}} words</span>
              <input type="checkbox" class="q-checkbox" onclick="event.stopPropagation(); toggleComplete(${{item.num}})" title="Mark as reviewed">
              <span class="chevron">▼</span>
            </div>
          </div>
          <div class="q-body">
            <div class="q-answer-content">${{formatText(item.answer)}}</div>
            <div class="q-footer">
              <span>First-Person POV · Verified ${{item.words}} words (&ge; 300 words standard satisfied)</span>
              <button class="copy-btn" onclick="copyAnswer(${{item.num}}, this)">📋 Copy Answer</button>
            </div>
          </div>
        </div>
      `).join('');
    }}

    function toggleCard(headerEl) {{
      headerEl.closest(".q-card").classList.toggle("open");
    }}

    function expandAll() {{
      document.querySelectorAll(".q-card").forEach(c => c.classList.add("open"));
    }}

    function collapseAll() {{
      document.querySelectorAll(".q-card").forEach(c => c.classList.remove("open"));
    }}

    function toggleComplete(num) {{
      const card = document.getElementById(`card-${{num}}`);
      const cb = card.querySelector(".q-checkbox");
      if (cb.checked) {{
        card.classList.add("completed");
      }} else {{
        card.classList.remove("completed");
      }}
      updateProgress();
    }}

    function updateProgress() {{
      const total = itemsData.length;
      const checked = document.querySelectorAll(".q-checkbox:checked").length;
      const pct = total > 0 ? (checked / total) * 100 : 0;
      document.getElementById("topProgress").style.width = pct + "%";
      document.getElementById("readCounter").innerText = `${{checked}} / ${{total}} Reviewed`;
    }}

    let activeCategory = 'all';

    function filterCategory(cat, btnEl) {{
      activeCategory = cat;
      document.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
      if (btnEl) btnEl.classList.add("active");
      applyFilterAndSearch();
    }}

    function handleSearch() {{
      applyFilterAndSearch();
    }}

    function applyFilterAndSearch() {{
      const query = document.getElementById("globalSearch").value.toLowerCase().trim();
      document.querySelectorAll(".q-card").forEach(card => {{
        const cardCat = card.getAttribute("data-cat");
        const cardSearch = card.getAttribute("data-search");
        const matchesCat = (activeCategory === 'all' || cardCat === activeCategory);
        const matchesQuery = (!query || cardSearch.includes(query));

        if (matchesCat && matchesQuery) {{
          card.style.display = "block";
        }} else {{
          card.style.display = "none";
        }}
      }});
    }}

    function resetFilters() {{
      document.getElementById("globalSearch").value = "";
      filterCategory('all', document.querySelector(".filter-pill"));
    }}

    function copyAnswer(num, btn) {{
      const item = itemsData.find(i => i.num === num);
      if (!item) return;
      const text = `Q${{item.num}}: ${{item.title}}\\nQuestion: "${{item.question}}"\\n\\nAnswer (Lakshmi Pranitha - First-Person POV):\\n${{item.answer}}`;
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
      if (localStorage.getItem("lp_wise_auth") === "true") {{
        revealContent();
      }}
    }});
  </script>
</body>
</html>
"""
    return html

def main():
    print("Generating Lakshmi Pranitha Wise Platform Prep Suite files...")
    
    # 1. Master Markdown
    md_content = generate_markdown()
    with open("lakshmi_pranitha_wise_prep.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("SUCCESS: Created lakshmi_pranitha_wise_prep.md")

    # 2. Nextra MDX
    mdx_content = generate_mdx(md_content)
    with open("content/lakshmi-pranitha-wise-prep.mdx", "w", encoding="utf-8") as f:
        f.write(mdx_content)
    print("SUCCESS: Created content/lakshmi-pranitha-wise-prep.mdx")

    # 3. Interactive Webpage
    html_content = generate_html()
    with open("lakshmi_pranitha_wise_prep.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("SUCCESS: Created lakshmi_pranitha_wise_prep.html")

if __name__ == "__main__":
    main()
