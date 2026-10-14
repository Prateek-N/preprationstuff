# -*- coding: utf-8 -*-
"""
Master Generator Script for Asha Jyothi Uchula
Alignment Health - Remote Data Analyst Technical & Operational Interview Master Suite
Generates:
1. asha_alignment_health_prep.md (Pure Markdown Guide)
2. content/asha-alignment-health-prep.mdx (Protected Nextra MDX with <PasswordGate>)
3. asha_alignment_health_prep.html (Standalone Protected Web Application)
4. public/asha_alignment_health_prep.html (Static Production HTML)
"""

import json
import os
import re

from asha_alignment_data_part1 import questions_part1
from asha_alignment_data_part2 import questions_part2

all_questions = questions_part1 + questions_part2
print(f"Total Questions Loaded: {len(all_questions)}")

# =========================================================================
# 1. GENERATE MASTER MARKDOWN FILE & NEXTRA MDX FILE
# =========================================================================

md_lines = []

# Title & Metadata Header
md_lines.append("# Alignment Health — Remote Data Analyst Interview Master Preparation Guide")
md_lines.append("**Candidate:** Asha Jyothi Uchula | Senior Public Health Data Analyst (MPH in Epidemiology & Biostatistics | Molina Healthcare, Optum, Cipla)")
md_lines.append("**Target Role:** Remote Data Analyst — Alignment Health (Embedded Operational Analytics Partner)")
md_lines.append("**Target Focus:** Medicare Advantage, CMS Star Ratings Optimization (Part C & D), HEDIS/CAHPS/HOS Quality Programs, HCC Risk Adjustment & Suspecting, Population Health Management, SDOH Analytics, Value-Based Care (VBC), and Snowflake/Databricks Cloud Infrastructure.\n")
md_lines.append("---\n")

# Executive Alignment Section
md_lines.append("## Executive Strategy & Role Alignment\n")
md_lines.append("Alignment Health is breaking the mold in conventional healthcare, dedicated to putting seniors first—specifically the chronically ill and frail. The **Remote Data Analyst** role requires an embedded analytics partner and subject matter expert who works across operational domains (Operations, Finance, IT, Quality, Clinical, Compliance) to transform complex operational and claims datasets into actionable insights, dashboards, and KPI frameworks that drive strategic decisions and care outcomes.\n")
md_lines.append("Asha Jyothi Uchula's background bridges advanced **MPH Epidemiology and Biostatistics** training from the **University of New Haven** with deep enterprise data analytics at **Molina Healthcare**, **Optum**, and **Cipla**:\n")
md_lines.append("1. **Medicare Advantage & CMS Star Ratings Mastery:** Engineered automated HEDIS and CAHPS pipelines across **28 clinical quality measures** at **Molina Healthcare**, sustaining a **99.8-point accuracy** rate and eliminating **320 manual analyst hours quarterly** while modeling Tukey outlier deletion and Health Equity Index (HEI) cut-point shifts.\n")
md_lines.append("2. **Clinical Risk Stratification & Machine Learning:** Deployed **XGBoost** and **scikit-learn** models stratifying 420K+ members by **HCC risk scores**, **SDOH Z-codes**, and comorbidity clusters, averting **1,800 preventable 30-day readmissions** worth **$4.1M in avoided acute costs**.\n")
md_lines.append("3. **Operational Partnership & Data Storytelling:** Consolidated **18 disparate data sources** into unified **Power BI** and **Tableau** dashboards on **Databricks** and **Snowflake**, compressing executive reporting cycles from **5 days to 4 hours** and surfacing **$2.7M in actionable quality improvement (QI) opportunities**.\n")
md_lines.append("4. **High-Scale Cloud Data Engineering:** Extracted and transformed **500GB+ of monthly claims data** at **Optum** via **SQL**, **Python**, **dbt**, and **AWS Glue**, building Master Member 360 profiles across **HL7 FHIR**, **EDI 837/835**, and EHR systems (Epic, Cerner).\n")
md_lines.append("5. **Enterprise Data Governance & Audit Readiness:** Authored **22 data dictionaries** and **8 data lineage maps** for a **40TB warehouse**, reducing audit prep turnaround from **8 days to 36 hours** while ensuring flawless **HIPAA** and **NCQA** compliance.\n\n")
md_lines.append("---\n")

# Questions Grouping by Domain
domains = [
    ("Domain 1: Medicare Advantage, CMS Star Ratings & HEDIS / CAHPS Quality Programs (Q1 - Q6)", 1, 6),
    ("Domain 2: Population Health Management, Risk Stratification & Predictive Analytics (Q7 - Q12)", 7, 12),
    ("Domain 3: Cross-Functional Operational Analytics & Business Partnership (Q13 - Q18)", 13, 18),
    ("Domain 4: Cloud Data Engineering, SQL, Snowflake & Pipeline Automation (Q19 - Q24)", 19, 24),
    ("Domain 5: BI Dashboard Design & Visual Data Storytelling (Q25 - Q27)", 25, 27),
    ("Domain 6: Data Governance, HIPAA, Regulatory Compliance & Alignment Health Mission (Q28 - Q30)", 28, 30)
]

for domain_title, start_id, end_id in domains:
    md_lines.append(f"## {domain_title}\n")
    for q in all_questions:
        if start_id <= q["id"] <= end_id:
            md_lines.append(f"### Question {q['id']}: {q['question']}")
            md_lines.append(f"**Competency Domain:** {q['category']}\n")
            md_lines.append(q['answer'].strip() + "\n")
            md_lines.append("---\n")

raw_markdown = "\n".join(md_lines)

# Write master pure markdown file
with open("asha_alignment_health_prep.md", "w", encoding="utf-8") as f:
    f.write(raw_markdown)
print("Wrote asha_alignment_health_prep.md successfully.")

# Write Nextra MDX with PasswordGate
mdx_frontmatter = """---
title: Asha Jyothi Uchula — Alignment Health Remote Data Analyst Interview Prep Guide
description: Comprehensive interview preparation master guide for Remote Data Analyst at Alignment Health (Medicare Advantage) — 30 in-depth ~300-word Q&As across CMS Star Ratings, HEDIS, CAHPS, HCC Risk Adjustment, Population Health, SQL, Snowflake, Databricks, and Operational Analytics.
---

<PasswordGate password="Asha" candidateName="Asha Jyothi Uchula">

"""

mdx_closing = """

</PasswordGate>
"""

def sanitize_mdx(mdx_str):
    parts = mdx_str.split('```')
    for i in range(0, len(parts), 2):
        # Only sanitize markdown prose outside code fences
        parts[i] = parts[i].replace('<=', '&le;')
        # Sanitize < followed by number or space
        parts[i] = re.sub(r'<(?=[0-9\s])', '&lt;', parts[i])
        # Replace curly braces in prose with HTML entities so MDX never evaluates them as JS variables
        parts[i] = parts[i].replace('{', '&#123;').replace('}', '&#125;')
    return '```'.join(parts)

sanitized_md_content = sanitize_mdx(raw_markdown)

with open("content/asha-alignment-health-prep.mdx", "w", encoding="utf-8") as f:
    f.write(mdx_frontmatter + sanitized_md_content + mdx_closing)
print("Wrote content/asha-alignment-health-prep.mdx successfully with <PasswordGate>.")


# =========================================================================
# 2. GENERATE PROTECTED STANDALONE HTML APPLICATION
# =========================================================================

items_data = []

for q in all_questions:
    def format_answer(ans):
        paragraphs = [p.strip() for p in ans.strip().split("\n\n") if p.strip()]
        return "".join([f'<p class="conv-p">{p.replace(chr(10), " ")}</p>' for p in paragraphs])

    # Assign filter categories
    filter_type = "stars"
    if 1 <= q["id"] <= 6:
        filter_type = "stars"
    elif 7 <= q["id"] <= 12:
        filter_type = "risk"
    elif 13 <= q["id"] <= 18:
        filter_type = "ops"
    elif 19 <= q["id"] <= 24:
        filter_type = "dataeng"
    elif 25 <= q["id"] <= 27:
        filter_type = "bi"
    else:
        filter_type = "gov"

    items_data.append({
        "num": q["id"],
        "type": filter_type,
        "title": f"Q{q['id']}: {q['question']}",
        "category": "Alignment Health Interview",
        "subCategory": q["category"],
        "difficulty": "Senior / Embedded Analyst",
        "search_text": f"{q['question']} {q['category']} {q['answer']}".lower(),
        "html_content": f"""
        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-purple">Interview Question {q['id']}</span></h4>
          <p class="body-p" style="font-weight: 700; font-size: 1.1rem; color: #f8fafc; line-height: 1.5;">{q['question']}</p>
        </div>
        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-cyan">In-Depth Strategic Response (~300 Words)</span></h4>
          {format_answer(q['answer'])}
        </div>
        """
    })

items_json_str = json.dumps(items_data)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Asha Jyothi Uchula — Alignment Health Remote Data Analyst Interview Suite</title>
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

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background-color: var(--bg-primary);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.6;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }}

    /* Glassmorphic Password Lock Overlay */
    #lockOverlay {{
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(10, 15, 29, 0.88);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      z-index: 99999;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }}

    .lock-card {{
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(13, 148, 136, 0.4);
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 40px rgba(13, 148, 136, 0.2);
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
      background: rgba(30, 41, 59, 0.4);
    }}

    .search-input {{
      width: 100%;
      padding: 0.75rem 1rem;
      border-radius: 8px;
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      color: #fff;
      font-size: 0.9rem;
      outline: none;
    }}

    .search-input:focus {{
      border-color: var(--accent-teal);
    }}

    .filter-tabs {{
      display: flex;
      gap: 0.4rem;
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border-color);
      background: rgba(10, 15, 29, 0.5);
      overflow-x: auto;
    }}

    .filter-btn {{
      padding: 0.4rem 0.75rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
    }}

    .filter-btn.active {{
      background: rgba(13, 148, 136, 0.2);
      border-color: rgba(13, 148, 136, 0.4);
      color: #5eead4;
    }}

    .items-scroll {{
      flex: 1;
      overflow-y: auto;
      padding: 0.75rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }}

    .item-card {{
      padding: 0.85rem 1rem;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .item-card:hover {{
      background: var(--bg-card-hover);
      border-color: rgba(255, 255, 255, 0.15);
      transform: translateX(3px);
    }}

    .item-card.active {{
      background: rgba(13, 148, 136, 0.18);
      border-color: var(--accent-teal);
    }}

    .item-card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.35rem;
    }}

    .item-badge {{
      font-size: 0.65rem;
      font-weight: 700;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      text-transform: uppercase;
    }}

    .badge-stars {{ background: rgba(13, 148, 136, 0.2); color: #5eead4; }}
    .badge-risk {{ background: rgba(59, 130, 246, 0.2); color: #93c5fd; }}
    .badge-ops {{ background: rgba(168, 85, 247, 0.2); color: #d8b4fe; }}
    .badge-dataeng {{ background: rgba(16, 185, 129, 0.2); color: #6ee7b7; }}
    .badge-bi {{ background: rgba(245, 158, 11, 0.2); color: #fde68a; }}
    .badge-gov {{ background: rgba(244, 63, 94, 0.2); color: #fecdd3; }}

    .item-num {{
      font-size: 0.75rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }}

    .item-title {{
      font-size: 0.875rem;
      font-weight: 600;
      color: #fff;
      line-height: 1.35;
    }}

    /* Detail View */
    .detail-panel {{
      flex: 1;
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 2.25rem 2.5rem;
      overflow-y: auto;
      max-height: calc(100vh - 120px);
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
      text-transform: uppercase;
      padding: 0.25rem 0.65rem;
      border-radius: 6px;
      margin-bottom: 0.75rem;
      background: rgba(13, 148, 136, 0.15);
      color: #2dd4bf;
      border: 1px solid rgba(13, 148, 136, 0.35);
    }}

    .detail-title {{
      font-size: 1.55rem;
      font-weight: 800;
      color: #fff;
      line-height: 1.35;
      letter-spacing: -0.02em;
    }}

    .section-block {{
      margin-bottom: 2rem;
    }}

    .sec-title {{
      font-size: 0.85rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.85rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .badge {{
      display: inline-block;
      padding: 0.3rem 0.65rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
    }}

    .badge-purple {{ background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }}
    .badge-cyan {{ background: rgba(6, 182, 212, 0.15); color: #22d3ee; border: 1px solid rgba(6, 182, 212, 0.3); }}
    .badge-teal {{ background: rgba(13, 148, 136, 0.15); color: #2dd4bf; border: 1px solid rgba(13, 148, 136, 0.3); }}

    .conv-p {{
      color: #cbd5e1;
      font-size: 0.98rem;
      line-height: 1.8;
      margin-bottom: 1.25rem;
    }}

    .conv-p strong {{
      color: #ffffff;
      font-weight: 700;
    }}

    .body-p {{
      color: #cbd5e1;
      font-size: 1.05rem;
      line-height: 1.7;
    }}

    .copy-btn-wrap {{
      display: flex;
      justify-content: flex-end;
      margin-bottom: 0.75rem;
    }}

    .btn-copy-ans {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 0.4rem 0.85rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .btn-copy-ans:hover {{
      color: #fff;
      border-color: rgba(255, 255, 255, 0.2);
    }}

    @media (max-width: 1024px) {{
      .app-layout {{ flex-direction: column; }}
      .sidebar {{ width: 100%; height: 350px; position: static; }}
    }}
  </style>
</head>
<body>

  <!-- Glassmorphic Password Lock Overlay -->
  <div id="lockOverlay">
    <div class="lock-card">
      <div class="lock-badge">🔒 Restricted Interview Guide</div>
      <div class="lock-title">Alignment Health Interview Portal</div>
      <div class="lock-candidate">Asha Jyothi Uchula</div>
      <div class="lock-sub">Remote Data Analyst · Embedded Operational Analytics Partner<br>(Medicare Advantage · Value-Based Care · Senior-First Mission)</div>
      
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
      <div class="brand-icon">A</div>
      <div class="brand-info">
        <h1>Asha Jyothi Uchula — Alignment Health Prep Suite</h1>
        <p>Remote Data Analyst (Medicare Advantage · Star Ratings · Operations Partner) · 30 Strategic Q&As</p>
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
        <input type="text" id="searchInput" class="search-input" placeholder="Search Star Ratings, HEDIS, SQL, ML..." oninput="handleSearch()" />
      </div>
      <div class="filter-tabs">
        <button class="filter-btn active" onclick="setFilter('all', this)">All (30)</button>
        <button class="filter-btn" onclick="setFilter('stars', this)">Stars & HEDIS (6)</button>
        <button class="filter-btn" onclick="setFilter('risk', this)">Risk & ML (6)</button>
        <button class="filter-btn" onclick="setFilter('ops', this)">Ops & VBC (6)</button>
        <button class="filter-btn" onclick="setFilter('dataeng', this)">SQL & Data (6)</button>
        <button class="filter-btn" onclick="setFilter('bi', this)">BI & Maps (3)</button>
        <button class="filter-btn" onclick="setFilter('gov', this)">Governance (3)</button>
      </div>
      <div class="items-scroll" id="itemsList"></div>
    </div>

    <!-- Detail View -->
    <div class="detail-panel" id="detailPanel">
      <!-- Dynamic Content Injected Here -->
    </div>
  </div>

  <script>
    const MASTER_PASS = "Asha";
    const SESSION_KEY = "asha_alignment_unlocked";
    const ALL_ITEMS = {items_json_str};

    let currentFilter = 'all';
    let currentSelectedNum = 1;

    // Check lock state
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
        listContainer.innerHTML = `<div style="padding: 2rem; text-align: center; color: var(--text-muted); font-size: 0.9rem;">No matching questions found.</div>`;
        return;
      }}

      filtered.forEach(item => {{
        const card = document.createElement("div");
        card.className = `item-card ${{item.num === currentSelectedNum ? 'active' : ''}}`;
        card.onclick = () => selectItem(item.num);

        let badgeClass = 'badge-stars';
        let badgeLabel = 'Stars/HEDIS';
        if (item.type === 'risk') {{ badgeClass = 'badge-risk'; badgeLabel = 'Risk / ML'; }}
        else if (item.type === 'ops') {{ badgeClass = 'badge-ops'; badgeLabel = 'Ops / VBC'; }}
        else if (item.type === 'dataeng') {{ badgeClass = 'badge-dataeng'; badgeLabel = 'SQL / Data'; }}
        else if (item.type === 'bi') {{ badgeClass = 'badge-bi'; badgeLabel = 'BI / Maps'; }}
        else if (item.type === 'gov') {{ badgeClass = 'badge-gov'; badgeLabel = 'Governance'; }}

        card.innerHTML = `
          <div class="item-card-header">
            <span class="item-badge ${{badgeClass}}">${{badgeLabel}}</span>
            <span class="item-num">#${{item.num}}</span>
          </div>
          <div class="item-title">${{item.title}}</div>
        `;
        listContainer.appendChild(card);
      }});

      // Auto select first if current not in filtered
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

      // Update active in sidebar
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

# Write standalone HTML in root and public
with open("asha_alignment_health_prep.html", "w", encoding="utf-8") as f:
    f.write(html_template)
print("Wrote asha_alignment_health_prep.html successfully.")

with open("public/asha_alignment_health_prep.html", "w", encoding="utf-8") as f:
    f.write(html_template)
print("Wrote public/asha_alignment_health_prep.html successfully.")
