import json
import re
from teja_purpose_data_part1 import QUESTIONS_PART1
from teja_purpose_data_part2 import QUESTIONS_PART2

ALL_QUESTIONS = QUESTIONS_PART1 + QUESTIONS_PART2

print(f"Total questions loaded: {len(ALL_QUESTIONS)}")

# 1. Generate Markdown Guide
md_content = """# Teja Talluri — Purpose Financial Data Quality Analyst Interview Master Preparation Guide

**Candidate:** Teja Talluri | Senior Data Analyst & AI/ML Analytics Specialist (5+ Years Exp | Uber, Dish Network, Cipla)  
**Target Organization:** Purpose Financial (Enterprise Data Team · Greenville, SC · Intentional, Thoughtful Financial Services)  
**Target Role:** Data Quality Analyst (Data Integrity, SQL Auditing, Python Automation, Governance & Scorecards)  
**Core Tech Stack:** SQL (Oracle, PostgreSQL, SQL Server, Snowflake), Python, dbt, Apache Airflow, Great Expectations, Medallion Architecture, Data Governance, Tableau/Power BI  
**Master Access Key:** `Teja`  

---

## Executive Summary & Strategic Fit

At **Purpose Financial**, data is the foundation of every meaningful decision made for customers. The **Data Quality Analyst** role on the **Enterprise Data team** plays a critical role in monitoring, assessing, and improving data quality across cloud environments—building scorecards, conducting audits, automating validation processes, and partnering with business, BI, and technology teams to certify data for consumption.

**Teja Talluri** brings over 5 years of enterprise analytics, data engineering, and data quality leadership:
1. **Multi-Engine SQL Mastery:** Expert SQL development across **Oracle, PostgreSQL, SQL Server, Snowflake, and Presto/Hive**, authoring complex window functions, automated anomaly detection scripts, and financial ledger reconciliations.
2. **Automated Data Quality & Observability:** Implemented **Data Contracts**, **Great Expectations**, and **dbt** testing suites at **Dish Network** and **Uber**, eliminating $1.8M in infrastructure costs, preventing $2.1M in fraudulent claims, and reducing executive reporting cycles from 12 hours to 2 hours.
3. **Data Governance & Certification:** Standardized **Data Dictionaries**, **Data Lineage** in **DataHub**, and instituted formal **Data Certification Scorecards** that verified tables for executive BI and self-service consumption.
4. **Cross-Functional Communication:** Proven track record translating dense technical breakdowns into actionable business implications for senior leadership, engineering leads, and business operations.

---

## 30 In-Depth Technical & Operational Interview Q&As (~300 Words Each)

"""

for q in ALL_QUESTIONS:
    md_content += f"### Question {q['num']}: {q['title']}\n\n"
    md_content += f"**Category:** {q['category']} | **Sub-Category:** {q['subCategory']} | **Difficulty:** {q['difficulty']}\n\n"
    md_content += f"{q['answer']}\n\n"
    md_content += "---\n\n"

with open("teja_purpose_financial_prep.md", "w", encoding="utf-8") as f:
    f.write(md_content)
print("Saved teja_purpose_financial_prep.md")


# 2. Generate Nextra MDX
def sanitize_mdx(text):
    # Convert code blocks temporarily
    code_blocks = []
    def code_repl(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"
    
    text = re.sub(r"```[\s\S]*?```", code_repl, text)
    text = re.sub(r"`[^`\n]+`", code_repl, text)

    # Sanitize prose
    text = text.replace("{", "&#123;").replace("}", "&#125;")
    text = text.replace("<=", "&le;").replace(">=", "&ge;")
    text = re.sub(r"<(?![a-zA-Z\/])", "&lt;", text)

    # Restore code blocks
    for idx, cb in enumerate(code_blocks):
        text = text.replace(f"__CODE_BLOCK_{idx}__", cb)

    return text

mdx_content = """---
title: Teja Talluri — Purpose Financial Data Quality Analyst Interview Prep Guide
description: Comprehensive interview preparation master guide for Data Quality Analyst at Purpose Financial — 30 in-depth ~300-word Q&As across SQL (Oracle, Postgres, Snowflake), Python automation, Data Contracts, Great Expectations, Medallion Architecture, and Data Governance.
---

<PasswordGate password="Teja" candidateName="Teja">

# Purpose Financial — Data Quality Analyst Interview Master Preparation Guide
**Candidate:** Teja Talluri | Senior Data Analyst & AI/ML Analytics Specialist (Uber, Dish Network, Cipla)  
**Target Role:** Data Quality Analyst — Purpose Financial (Enterprise Data Team · Greenville, SC)  
**Target Focus:** Data Quality Dimensions, Multi-Engine SQL (Oracle, Postgres, SQL Server, Snowflake), Python Automation, Data Contracts, Medallion Architecture, Financial Reconciliation, and Executive BI Certification.  

---

## Executive Summary & Role Alignment

At Purpose Financial, data isn't just numbers — it's the foundation of every meaningful decision made for customers. The **Data Quality Analyst** on the **Enterprise Data team** plays a critical role in monitoring, assessing, and improving data quality across cloud environments — building scorecards, conducting audits, automating validation processes, and partnering with business, BI, and technology teams to certify data for consumption.

Teja Talluri's background directly matches every requirement of the role:
1. **Multi-Engine SQL Expertise:** Deep hands-on experience authoring complex SQL across **Oracle, PostgreSQL, SQL Server, Snowflake, and Presto/Hive**, including window functions, financial balance roll-forward reconciliations, and automated duplicate detection.
2. **Python Automation & Data Validation:** Engineered validation frameworks using **Python, Great Expectations, PySpark, and dbt**, automating data profiling, distribution tracking (PSI, Z-scores), and anomaly alerting.
3. **Medallion Lakehouse & Cloud Architecture:** Migrated 14 legacy ETL workflows to modern Medallion Architecture (Bronze/Silver/Gold) on **Snowflake** and **AWS Redshift**, slashing execution times from 6 hours to 47 minutes.
4. **Data Governance & Certification:** Instituted enterprise **Data Contracts**, **Data Dictionaries**, **Data Lineage** maps in **DataHub**, and **Data Quality Scorecards** certifying tables for BI and executive reporting.

---

"""

for q in ALL_QUESTIONS:
    clean_answer = sanitize_mdx(q['answer'])
    clean_title = sanitize_mdx(q['title'])
    clean_sub = sanitize_mdx(q['subCategory'])

    mdx_content += f"### {clean_title}\n\n"
    mdx_content += f"**Domain:** {clean_sub} | **Role Level:** Senior Data Quality Analyst\n\n"
    mdx_content += f"{clean_answer}\n\n"
    mdx_content += "---\n\n"

mdx_content += "</PasswordGate>\n"

with open("content/teja-purpose-financial-prep.mdx", "w", encoding="utf-8") as f:
    f.write(mdx_content)
print("Saved content/teja-purpose-financial-prep.mdx")


# 3. Generate Standalone Interactive HTML Portal
html_items = []
for q in ALL_QUESTIONS:
    # Convert markdown bold to <strong> and paragraphs
    paragraphs = q['answer'].strip().split("\n\n")
    html_paragraphs = []
    for p in paragraphs:
        if p.startswith("```"):
            # Format code block
            code_text = p.strip("`").replace("sql\n", "").replace("python\n", "").replace("yaml\n", "")
            html_paragraphs.append(f'<pre><code>{code_text}</code></pre>')
        else:
            p_html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", p)
            html_paragraphs.append(f'<p class="conv-p">{p_html}</p>')

    item_html = f"""
        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-purple">Interview Question {q['num']}</span></h4>
          <p class="body-p" style="font-weight: 700; font-size: 1.1rem; color: #f8fafc; line-height: 1.5;">{q['title']}</p>
        </div>
        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-cyan">In-Depth Strategic Response (~300 Words)</span></h4>
          {''.join(html_paragraphs)}
        </div>
    """

    search_text = (q['title'] + " " + q['subCategory'] + " " + q['answer']).lower()

    html_items.append({
        "num": q['num'],
        "type": q['type'],
        "title": q['title'],
        "category": q['category'],
        "subCategory": q['subCategory'],
        "difficulty": q['difficulty'],
        "search_text": search_text,
        "html_content": item_html
    })

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Teja Talluri — Purpose Financial Data Quality Analyst Interview Suite</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-primary: #0a0f1d;
      --bg-secondary: #0f172a;
      --bg-card: #1e293b;
      --bg-card-hover: #273549;
      --accent-teal: #0d9488;
      --accent-cyan: #06b6d4;
      --accent-blue: #3b82f6;
      --accent-purple: #a855f7;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --border-color: rgba(255, 255, 255, 0.08);
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-sans);
      background-color: var(--bg-primary);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }}

    /* Password Lock Modal */
    #lockOverlay {{
      position: fixed;
      inset: 0;
      background: rgba(10, 15, 29, 0.94);
      backdrop-filter: blur(16px);
      z-index: 9999;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }}

    .lock-card {{
      background: linear-gradient(145deg, #131d35, #0d1527);
      border: 1px solid rgba(13, 148, 136, 0.3);
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.8), 0 0 40px rgba(13, 148, 136, 0.15);
      border-radius: 24px;
      padding: 3rem 2.5rem;
      max-width: 490px;
      width: 100%;
      text-align: center;
      animation: modalFadeIn 0.5s ease-out;
    }}

    @keyframes modalFadeIn {{
      from {{ opacity: 0; transform: translateY(20px) scale(0.97); }}
      to {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}

    .lock-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.35rem 0.85rem;
      border-radius: 9999px;
      background: rgba(13, 148, 136, 0.15);
      border: 1px solid rgba(13, 148, 136, 0.35);
      color: #2dd4bf;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 1.25rem;
    }}

    .lock-title {{
      font-size: 1.75rem;
      font-weight: 800;
      color: #fff;
      margin-bottom: 0.5rem;
      letter-spacing: -0.02em;
    }}

    .lock-candidate {{
      font-size: 1.2rem;
      font-weight: 700;
      color: var(--accent-cyan);
      margin-bottom: 0.5rem;
    }}

    .lock-sub {{
      color: var(--text-muted);
      font-size: 0.88rem;
      margin-bottom: 2rem;
      line-height: 1.5;
    }}

    .lock-input-group {{
      display: flex;
      gap: 0.75rem;
      margin-bottom: 1rem;
    }}

    .lock-input {{
      flex: 1;
      padding: 0.85rem 1.25rem;
      border-radius: 12px;
      background: rgba(10, 15, 29, 0.7);
      border: 1px solid var(--border-color);
      color: #fff;
      font-size: 1rem;
      font-family: var(--font-sans);
      outline: none;
      transition: all 0.2s;
    }}

    .lock-input:focus {{
      border-color: var(--accent-teal);
      box-shadow: 0 0 15px rgba(13, 148, 136, 0.35);
    }}

    .lock-btn {{
      padding: 0.85rem 1.5rem;
      border-radius: 12px;
      background: linear-gradient(135deg, #0d9488, #0284c7);
      color: #fff;
      font-weight: 600;
      font-size: 0.95rem;
      border: none;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .lock-btn:hover {{
      opacity: 0.92;
      transform: translateY(-1px);
    }}

    .lock-error {{
      color: #f87171;
      font-size: 0.85rem;
      font-weight: 500;
      min-height: 1.25rem;
    }}

    /* Header */
    header {{
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 1000;
      padding: 1rem 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
    }}

    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 0.85rem;
    }}

    .brand-icon {{
      width: 42px;
      height: 42px;
      border-radius: 12px;
      background: linear-gradient(135deg, #0d9488, #0ea5e9);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      font-size: 1.25rem;
      color: #fff;
      box-shadow: 0 0 20px rgba(13, 148, 136, 0.4);
    }}

    .brand-info h1 {{
      font-size: 1.1rem;
      font-weight: 700;
      letter-spacing: -0.01em;
    }}

    .brand-info p {{
      font-size: 0.75rem;
      color: var(--text-muted);
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}

    .btn-lock {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 0.5rem 0.85rem;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .btn-lock:hover {{
      color: #fff;
      border-color: rgba(255, 255, 255, 0.2);
    }}

    /* Main Container */
    .app-layout {{
      display: flex;
      flex: 1;
      max-width: 1680px;
      width: 100%;
      margin: 0 auto;
      padding: 1.5rem 2rem;
      gap: 2rem;
    }}

    /* Sidebar List */
    .sidebar {{
      width: 440px;
      flex-shrink: 0;
      display: flex;
      flex-direction: column;
      height: calc(100vh - 120px);
      position: sticky;
      top: 90px;
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      overflow: hidden;
    }}

    .search-box {{
      padding: 1rem;
      border-bottom: 1px solid var(--border-color);
    }}

    .search-input {{
      width: 100%;
      background: rgba(10, 15, 29, 0.6);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 0.65rem 1rem;
      color: #fff;
      font-size: 0.85rem;
      font-family: var(--font-sans);
      outline: none;
      transition: all 0.2s;
    }}

    .search-input:focus {{
      border-color: var(--accent-teal);
    }}

    .filter-tabs {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
      padding: 0.75rem 1rem;
      background: rgba(10, 15, 29, 0.3);
      border-bottom: 1px solid var(--border-color);
    }}

    .filter-btn {{
      padding: 0.3rem 0.65rem;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid transparent;
      color: var(--text-muted);
      font-size: 0.75rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.15s;
    }}

    .filter-btn:hover, .filter-btn.active {{
      background: rgba(13, 148, 136, 0.18);
      border-color: rgba(13, 148, 136, 0.4);
      color: #2dd4bf;
    }}

    .items-scroll {{
      flex: 1;
      overflow-y: auto;
      padding: 0.5rem;
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
    }}

    .items-scroll::-webkit-scrollbar {{
      width: 5px;
    }}
    .items-scroll::-webkit-scrollbar-thumb {{
      background: rgba(255, 255, 255, 0.1);
      border-radius: 4px;
    }}

    .item-card {{
      padding: 0.85rem 1rem;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid transparent;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
    }}

    .item-card:hover {{
      background: rgba(255, 255, 255, 0.05);
      border-color: rgba(255, 255, 255, 0.1);
    }}

    .item-card.active {{
      background: linear-gradient(135deg, rgba(13, 148, 136, 0.15), rgba(6, 182, 212, 0.08));
      border-color: rgba(13, 148, 136, 0.4);
    }}

    .item-card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .item-badge {{
      font-size: 0.68rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 0.15rem 0.45rem;
      border-radius: 4px;
    }}

    .badge-teal {{ background: rgba(13, 148, 136, 0.2); color: #2dd4bf; }}
    .badge-blue {{ background: rgba(59, 130, 246, 0.2); color: #60a5fa; }}
    .badge-purple {{ background: rgba(168, 85, 247, 0.2); color: #c084fc; }}
    .badge-amber {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; }}
    .badge-cyan {{ background: rgba(6, 182, 212, 0.2); color: #22d3ee; }}
    .badge-emerald {{ background: rgba(16, 185, 129, 0.2); color: #34d399; }}

    .item-num {{
      font-size: 0.75rem;
      font-family: var(--font-mono);
      color: var(--text-muted);
    }}

    .item-title {{
      font-size: 0.85rem;
      font-weight: 600;
      color: #e2e8f0;
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    /* Detail View Panel */
    .detail-panel {{
      flex: 1;
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 2.25rem 2.5rem;
      overflow-y: auto;
      max-height: calc(100vh - 120px);
      position: sticky;
      top: 90px;
    }}

    .detail-panel::-webkit-scrollbar {{
      width: 6px;
    }}
    .detail-panel::-webkit-scrollbar-thumb {{
      background: rgba(255, 255, 255, 0.12);
      border-radius: 4px;
    }}

    .detail-header {{
      margin-bottom: 2rem;
      padding-bottom: 1.5rem;
      border-bottom: 1px solid var(--border-color);
    }}

    .detail-tag {{
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--accent-cyan);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.6rem;
    }}

    .detail-title {{
      font-size: 1.6rem;
      font-weight: 800;
      color: #fff;
      line-height: 1.35;
      letter-spacing: -0.01em;
    }}

    .section-block {{
      margin-bottom: 1.75rem;
    }}

    .sec-title {{
      font-size: 0.9rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--accent-teal);
      margin-bottom: 0.75rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .conv-p {{
      color: #cbd5e1;
      font-size: 1.02rem;
      line-height: 1.75;
      margin-bottom: 1.15rem;
    }}

    strong {{
      color: #f1f5f9;
      font-weight: 700;
    }}

    pre {{
      background: rgba(10, 15, 29, 0.85);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1.25rem;
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 0.88rem;
      line-height: 1.6;
      color: #38bdf8;
      margin: 1rem 0 1.5rem;
    }}

    code {{
      font-family: var(--font-mono);
      font-size: 0.9em;
      color: #38bdf8;
    }}

    .btn-copy-ans {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 0.4rem 0.8rem;
      border-radius: 6px;
      font-size: 0.78rem;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .btn-copy-ans:hover {{
      color: #fff;
      background: rgba(255, 255, 255, 0.12);
    }}
  </style>
</head>
<body>

  <!-- Glassmorphic Password Lock Overlay -->
  <div id="lockOverlay">
    <div class="lock-card">
      <div class="lock-badge">🔒 Restricted Interview Guide</div>
      <div class="lock-title">Purpose Financial Interview Portal</div>
      <div class="lock-candidate">Teja</div>
      <div class="lock-sub">Data Quality Analyst · Enterprise Data Team<br>(Oracle · Postgres · SQL Server · Snowflake · Python · Governance)</div>
      
      <form id="lockForm" onsubmit="handleUnlock(event)">
        <div class="lock-input-group">
          <input type="password" id="passInput" class="lock-input" placeholder="Enter Access Password..." autocomplete="off" autofocus />
          <button type="submit" class="lock-btn">Unlock</button>
        </div>
        <div id="lockError" class="lock-error"></div>
      </form>
    </div>
  </div>

  <!-- Header -->
  <header>
    <div class="brand-wrap">
      <div class="brand-icon">T</div>
      <div class="brand-info">
        <h1>Teja Talluri — Purpose Financial Prep Suite</h1>
        <p>Data Quality Analyst (Enterprise Data · SQL & Python Automation · Data Governance) · 30 Strategic Q&As</p>
      </div>
    </div>
    <div class="header-actions">
      <button class="btn-lock" onclick="lockPage()">Lock Guide</button>
    </div>
  </header>

  <!-- App Layout -->
  <div class="app-layout">
    <!-- Sidebar -->
    <div class="sidebar">
      <div class="search-box">
        <input type="text" id="searchInput" class="search-input" placeholder="Search SQL, Python, Great Expectations, Medallion..." oninput="handleSearch()" />
      </div>
      <div class="filter-tabs">
        <button class="filter-btn active" onclick="setFilter('all', this)">All (30)</button>
        <button class="filter-btn" onclick="setFilter('dq_core', this)">DQ Core (6)</button>
        <button class="filter-btn" onclick="setFilter('tech_sql', this)">SQL & Lakehouse (6)</button>
        <button class="filter-btn" onclick="setFilter('gov_compliance', this)">Governance & PII (3)</button>
        <button class="filter-btn" onclick="setFilter('bi_cert', this)">BI & Observability (3)</button>
        <button class="filter-btn" onclick="setFilter('ml_anomaly', this)">Anomaly & ML (3)</button>
        <button class="filter-btn" onclick="setFilter('eng_arch', this)">dbt & CI/CD (3)</button>
        <button class="filter-btn" onclick="setFilter('comm_lead', this)">Leadership & RCA (6)</button>
      </div>
      <div class="items-scroll" id="itemsList"></div>
    </div>

    <!-- Detail View -->
    <div class="detail-panel" id="detailPanel">
      <!-- Dynamic Content Injected Here -->
    </div>
  </div>

  <script>
    const MASTER_PASS = "Teja";
    const SESSION_KEY = "teja_purpose_unlocked";
    const ALL_ITEMS = {json.dumps(html_items)};

    let currentFilter = "all";
    let currentSelectedNum = 1;

    function checkAuth() {{
      if (sessionStorage.getItem(SESSION_KEY) === "true") {{
        document.getElementById("lockOverlay").style.display = "none";
      }} else {{
        document.getElementById("lockOverlay").style.display = "flex";
        setTimeout(() => document.getElementById("passInput").focus(), 100);
      }}
    }}

    function handleUnlock(e) {{
      e.preventDefault();
      const val = document.getElementById("passInput").value.trim();
      const err = document.getElementById("lockError");
      if (val.toLowerCase() === MASTER_PASS.toLowerCase()) {{
        sessionStorage.setItem(SESSION_KEY, "true");
        document.getElementById("lockOverlay").style.display = "none";
        err.innerText = "";
      }} else {{
        err.innerText = "Incorrect password. Please try again.";
        const card = document.querySelector(".lock-card");
        card.style.animation = "none";
        card.offsetHeight;
        card.style.animation = "modalFadeIn 0.3s ease-out";
      }}
    }}

    function lockPage() {{
      sessionStorage.removeItem(SESSION_KEY);
      document.getElementById("passInput").value = "";
      document.getElementById("lockOverlay").style.display = "flex";
      document.getElementById("passInput").focus();
    }}

    function setFilter(type, btn) {{
      currentFilter = type;
      document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      renderList();
    }}

    function handleSearch() {{
      renderList();
    }}

    function renderList() {{
      const query = document.getElementById("searchInput").value.trim().toLowerCase();
      const listContainer = document.getElementById("itemsList");
      listContainer.innerHTML = "";

      const filtered = ALL_ITEMS.filter(item => {{
        const matchesFilter = currentFilter === 'all' || item.type === currentFilter;
        const matchesQuery = !query || item.search_text.includes(query);
        return matchesFilter && matchesQuery;
      }});

      if (filtered.length === 0) {{
        listContainer.innerHTML = `<div style="padding: 2rem; text-align: center; color: var(--text-muted); font-size: 0.85rem;">No matching questions found.</div>`;
        return;
      }}

      filtered.forEach(item => {{
        const card = document.createElement("div");
        card.className = `item-card ${{item.num === currentSelectedNum ? "active" : ""}}`;
        card.onclick = () => selectItem(item.num);

        let badgeClass = "badge-teal";
        let badgeLabel = "DQ Core";
        if (item.type === "tech_sql") {{ badgeClass = "badge-blue"; badgeLabel = "SQL"; }}
        else if (item.type === "gov_compliance") {{ badgeClass = "badge-purple"; badgeLabel = "Governance"; }}
        else if (item.type === "bi_cert") {{ badgeClass = "badge-cyan"; badgeLabel = "BI Cert"; }}
        else if (item.type === "ml_anomaly") {{ badgeClass = "badge-amber"; badgeLabel = "Anomaly"; }}
        else if (item.type === "eng_arch") {{ badgeClass = "badge-emerald"; badgeLabel = "dbt & ELT"; }}
        else if (item.type === "comm_lead") {{ badgeClass = "badge-teal"; badgeLabel = "Leadership"; }}

        card.innerHTML = `
          <div class="item-card-header">
            <span class="item-badge ${{badgeClass}}">${{badgeLabel}}</span>
            <span class="item-num">#${{item.num}}</span>
          </div>
          <div class="item-title">${{item.title}}</div>
        `;
        listContainer.appendChild(card);
      }});

      if (!filtered.some(i => i.num === currentSelectedNum)) {{
        selectItem(filtered[0].num);
      }}
    }}

    function selectItem(num) {{
      currentSelectedNum = num;
      document.querySelectorAll(".item-card").forEach(c => c.classList.remove("active"));
      
      const item = ALL_ITEMS.find(i => i.num === num);
      if (!item) return;

      const panel = document.getElementById("detailPanel");
      panel.innerHTML = `
        <div class="detail-header">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span class="detail-tag">${{item.category}} · ${{item.subCategory}}</span>
            <button class="btn-copy-ans" onclick="copyAnswer()">Copy Answer</button>
          </div>
          <h2 class="detail-title">${{item.title}}</h2>
        </div>
        ${{item.html_content}}
      `;
      panel.scrollTop = 0;

      const cards = document.querySelectorAll(".item-card");
      cards.forEach(card => {{
        if (card.querySelector(".item-num") && card.querySelector(".item-num").innerText === `#${{num}}`) {{
          card.classList.add("active");
        }}
      }});
    }}

    function copyAnswer() {{
      const text = document.querySelector(".detail-panel").innerText;
      navigator.clipboard.writeText(text).then(() => {{
        const btn = document.querySelector(".btn-copy-ans");
        const orig = btn.innerText;
        btn.innerText = "Copied!";
        setTimeout(() => btn.innerText = orig, 2000);
      }});
    }}

    // Init
    checkAuth();
    renderList();
    selectItem(1);
  </script>
</body>
</html>
"""

with open("teja_purpose_financial_prep.html", "w", encoding="utf-8") as f:
    f.write(html_template)
print("Saved teja_purpose_financial_prep.html")

with open("public/teja_purpose_financial_prep.html", "w", encoding="utf-8") as f:
    f.write(html_template)
print("Saved public/teja_purpose_financial_prep.html")
