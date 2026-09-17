# -*- coding: utf-8 -*-
"""
Master Compilation Script for Rujuwal Garg - Gartner Agentic AI Interview Preparation Suite
Generates:
1. rujuwal_gartner_agentic_ai_prep.md
2. content/rujuwal-gartner-agentic-ai-prep.mdx
3. rujuwal_gartner_agentic_ai_prep.html
Passcode: "Gartner"
"""

import os
import re
import json
from rujuwal_resume_breakdown import resume_breakdown_markdown
from rujuwal_gartner_q1_to_q15 import questions_1_to_15
from rujuwal_gartner_q16_to_q30 import questions_16_to_30

all_questions = questions_1_to_15 + questions_16_to_30
print(f"Total technical questions loaded: {len(all_questions)}")

# =============================================================================
# WORD COUNT VALIDATION
# =============================================================================
print("\n--- Validating Question Word Counts (Target >= 300 words) ---")
all_passed = True
for q in all_questions:
    words = len(re.findall(r'\b\w+\b', q["answer"]))
    print(f"Q{q['id']} ({q['category'][:30]}...): {words} words")
    if words < 300:
        print(f"WARNING: Q{q['id']} has fewer than 300 words ({words})!")
        all_passed = False

if all_passed:
    print("\nALL 30 TECHNICAL QUESTIONS SATISFY THE >= 300 WORDS REQUIREMENT!\n")

# =============================================================================
# 1. GENERATE MASTER MARKDOWN FILE (rujuwal_gartner_agentic_ai_prep.md)
# =============================================================================
md_lines = []
md_lines.append("# Rujuwal Garg — Gartner Agentic AI Applications: Master Interview Preparation Suite")
md_lines.append("## End-to-End Resume Deconstruction, Technical Architecture, and 30 Enterprise Interview Deep Dives")
md_lines.append("")
md_lines.append("**Candidate:** Rujuwal Garg  ")
md_lines.append("**Target Role:** Software Engineer / Team Lead — Agentic AI Applications  ")
md_lines.append("**Company:** Gartner, Inc. (Sales & Service Delivery Enablement Tools)  ")
md_lines.append("**Location & Status:** Delhi, India / Gurgaon / Remote Hybrid  ")
md_lines.append("**Core Specialization:** Multi-Agent Systems, LangGraph / LangChain, Advanced RAG, FastAPI, AWS Cloud Architecture, Vector Databases, Evaluation & Guardrails  ")
md_lines.append("**Access Passcode:** `Gartner`  ")
md_lines.append("")
md_lines.append("---")
md_lines.append("")
md_lines.append(resume_breakdown_markdown)
md_lines.append("")
md_lines.append("---")
md_lines.append("")
md_lines.append("# Part 2: 30 Enterprise Technical Interview Deep Dives for Gartner Agentic AI")
md_lines.append("")
md_lines.append("This section contains 30 master technical interview questions and comprehensive answers tailored directly to Gartner's Agentic AI Applications job description. Every single answer contains at least 300 words with critical technical concepts and architectural components in **bold**.")
md_lines.append("")

current_cat = ""
for q in all_questions:
    if q["category"] != current_cat:
        current_cat = q["category"]
        md_lines.append(f"## Category: {current_cat}\n")
    
    md_lines.append(f"### Q{q['id']}: {q['question']}")
    md_lines.append(f"**Focus Area:** {q['category']}  ")
    md_lines.append("")
    md_lines.append(q["answer"])
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

with open("rujuwal_gartner_agentic_ai_prep.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))
print("Successfully generated rujuwal_gartner_agentic_ai_prep.md")


# =============================================================================
# 2. GENERATE NEXT DATA MDX FILE (content/rujuwal-gartner-agentic-ai-prep.mdx)
# =============================================================================
mdx_lines = []
mdx_lines.append("---")
mdx_lines.append("title: Rujuwal Garg — Gartner Agentic AI Applications Prep Guide")
mdx_lines.append("description: Comprehensive interview preparation guide for Gartner Agentic AI Applications — Resume deep dive, sample projects, and 30 master technical questions with architectural depth.")
mdx_lines.append("---")
mdx_lines.append("")
mdx_lines.append('<PasswordGate password="Gartner">')
mdx_lines.append("")
mdx_lines.append("# Rujuwal Garg — Gartner Agentic AI Applications: Master Interview Preparation Suite")
mdx_lines.append("## End-to-End Resume Deconstruction, Technical Architecture, and 30 Enterprise Interview Deep Dives")
mdx_lines.append("")
mdx_lines.append("**Candidate:** Rujuwal Garg  ")
mdx_lines.append("**Target Role:** Software Engineer / Team Lead — Agentic AI Applications  ")
mdx_lines.append("**Company:** Gartner, Inc. (Sales & Service Delivery Enablement Tools)  ")
mdx_lines.append("**Core Specialization:** Multi-Agent Systems, LangGraph / LangChain, Advanced RAG, FastAPI, AWS Cloud Architecture, Vector Databases, Evaluation & Guardrails  ")
mdx_lines.append("**Access Passcode:** `Gartner`  ")
mdx_lines.append("")
mdx_lines.append("---")
mdx_lines.append("")
mdx_lines.append(resume_breakdown_markdown)
mdx_lines.append("")
mdx_lines.append("---")
mdx_lines.append("")
mdx_lines.append("# Part 2: 30 Enterprise Technical Interview Deep Dives for Gartner Agentic AI")
mdx_lines.append("")

current_cat = ""
for q in all_questions:
    if q["category"] != current_cat:
        current_cat = q["category"]
        mdx_lines.append(f"## Category: {current_cat}\n")
    
    mdx_lines.append(f"### Q{q['id']}: {q['question']}")
    mdx_lines.append(f"**Focus Area:** {q['category']}  ")
    mdx_lines.append("")
    mdx_lines.append(q["answer"])
    mdx_lines.append("")
    mdx_lines.append("---")
    mdx_lines.append("")

mdx_lines.append("</PasswordGate>")

def clean_mdx_content(raw_text):
    parts = re.split(r'(```[\s\S]*?```)', raw_text)
    cleaned_parts = []
    for p in parts:
        if p.startswith('```'):
            cleaned_parts.append(p)
        else:
            # Escape raw { and } in text to avoid Acorn JS expression errors
            clean_p = p.replace('{', '&#123;').replace('}', '&#125;')
            # Escape unescaped < and > outside allowed JSX tags
            clean_p = re.sub(r'<(?!/?PasswordGate|/?span|/?div|/?p|/?strong|/?em|/?a|/?b|/?br|/?pre|/?code|/?h1|/?h2|/?h3|/?h4|/?table|/?thead|/?tbody|/?tr|/?th|/?td|/?ul|/?li)', '&lt;', clean_p)
            cleaned_parts.append(clean_p)
    return "".join(cleaned_parts)

final_mdx = clean_mdx_content("\n".join(mdx_lines))

with open("content/rujuwal-gartner-agentic-ai-prep.mdx", "w", encoding="utf-8") as f:
    f.write(final_mdx)
print("Successfully generated content/rujuwal-gartner-agentic-ai-prep.mdx")


# =============================================================================
# 3. GENERATE STANDALONE INTERACTIVE HTML (rujuwal_gartner_agentic_ai_prep.html)
# =============================================================================
json_questions_data = json.dumps(all_questions)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gartner Agentic AI Applications Prep Suite · Rujuwal Garg</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-base: #07090e;
      --bg-surface: #0f1422;
      --bg-card: #151d30;
      --bg-card-hover: #1b2640;
      --border: #233152;
      --border-accent: #3b82f6;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --gartner-blue: #002b49;
      --gartner-accent: #0072ce;
      --gartner-cyan: #06b6d4;
      --gartner-emerald: #10b981;
      --gartner-purple: #8b5cf6;
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
      background: radial-gradient(circle at center, #101c36 0%, #04060b 100%);
      display: flex; align-items: center; justify-content: center;
      z-index: 99999; padding: 1.5rem;
    }}
    .lock-box {{
      background: rgba(15, 20, 34, 0.98);
      backdrop-filter: blur(24px);
      border: 1px solid rgba(0, 114, 206, 0.4);
      border-radius: 24px;
      padding: 2.75rem 2.5rem;
      max-width: 500px;
      width: 100%;
      text-align: center;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.9), 0 0 50px rgba(0, 114, 206, 0.25);
    }}
    .lock-logo-mark {{
      display: inline-flex; align-items: center; justify-content: center;
      margin-bottom: 1.5rem; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.04em;
    }}
    .lock-txt-1 {{ color: #ffffff; }}
    .lock-txt-2 {{ color: #0072ce; }}
    .lock-badge-pill {{
      background: linear-gradient(135deg, rgba(0, 114, 206, 0.25), rgba(6, 182, 212, 0.25));
      border: 1px solid rgba(0, 114, 206, 0.5);
      padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; color: #38bdf8;
      font-family: var(--font-mono); margin-left: 8px; font-weight: 700;
    }}
    .lock-box h2 {{ font-size: 1.45rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.02em; }}
    .lock-box p {{ color: var(--text-muted); font-size: 0.88rem; margin-bottom: 1.75rem; }}
    .input-group {{ position: relative; margin-bottom: 1.25rem; }}
    .input-group input {{
      width: 100%;
      background: rgba(7, 9, 14, 0.95);
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
      border-color: var(--gartner-accent);
      box-shadow: 0 0 0 3px rgba(0, 114, 206, 0.25);
    }}
    .unlock-btn {{
      width: 100%;
      background: linear-gradient(135deg, #0072ce, #004b87);
      color: #ffffff;
      border: none;
      padding: 0.95rem;
      border-radius: 12px;
      font-size: 0.98rem;
      font-weight: 800;
      cursor: pointer;
      transition: all 0.2s;
      display: flex; align-items: center; justify-content: center; gap: 8px;
    }}
    .unlock-btn:hover {{
      background: linear-gradient(135deg, #005fa8, #003a6c);
      transform: translateY(-1px);
      box-shadow: 0 10px 25px -5px rgba(0, 114, 206, 0.4);
    }}
    .lock-err {{
      color: #f87171; font-size: 0.82rem; margin-top: 0.85rem; display: none; font-weight: 600;
    }}

    /* MAIN APP CONTENT */
    #appContent {{ display: none; opacity: 0; transition: opacity 0.3s ease; }}

    /* HEADER */
    .top-header {{
      background: linear-gradient(180deg, #0f1422 0%, #07090e 100%);
      border-bottom: 1px solid var(--border);
      padding: 2.25rem 2rem 1.75rem 2rem;
      position: relative;
      overflow: hidden;
    }}
    .top-header::after {{
      content: ''; position: absolute; top: 0; left: 15%; width: 550px; height: 180px;
      background: radial-gradient(circle, rgba(0, 114, 206, 0.15) 0%, transparent 70%);
      pointer-events: none;
    }}
    .header-container {{
      max-width: 1300px; margin: 0 auto;
      display: flex; justify-content: space-between; align-items: flex-start;
      gap: 2rem; flex-wrap: wrap; position: relative; z-index: 1;
    }}
    .candidate-profile {{ flex: 1; min-width: 320px; }}
    .title-row {{ display: flex; align-items: center; gap: 12px; margin-bottom: 0.65rem; flex-wrap: wrap; }}
    .candidate-name {{ font-size: 2rem; font-weight: 800; letter-spacing: -0.03em; color: #fff; }}
    .target-company-badge {{
      background: rgba(0, 114, 206, 0.15); border: 1px solid rgba(0, 114, 206, 0.4);
      color: #38bdf8; font-size: 0.78rem; font-weight: 700; padding: 4px 12px; border-radius: 9999px;
      font-family: var(--font-mono);
    }}
    .role-badge {{
      background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4);
      color: #34d399; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 9999px;
      font-family: var(--font-mono);
    }}
    .profile-subtitle {{
      color: var(--text-muted); font-size: 0.95rem; margin-bottom: 1rem; line-height: 1.5;
    }}
    .tags-container {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 0.75rem; }}
    .skill-tag {{
      background: rgba(21, 29, 48, 0.85); border: 1px solid var(--border);
      color: #cbd5e1; font-size: 0.78rem; padding: 3px 10px; border-radius: 6px;
      font-family: var(--font-mono); font-weight: 500;
    }}
    .skill-tag.accent {{ border-color: rgba(0, 114, 206, 0.4); color: #38bdf8; }}

    /* STATS CARD */
    .header-stats-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 1.25rem 1.75rem;
      min-width: 280px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }}
    .stat-row {{ display: flex; justify-content: space-between; margin-bottom: 0.75rem; font-size: 0.85rem; }}
    .stat-label {{ color: var(--text-muted); }}
    .stat-value {{ font-weight: 700; color: #fff; font-family: var(--font-mono); }}
    .stat-value.highlight {{ color: #38bdf8; }}
    .progress-bar-container {{
      width: 100%; height: 8px; background: rgba(255,255,255,0.06);
      border-radius: 9999px; overflow: hidden; margin: 10px 0 6px 0;
    }}
    .progress-bar-fill {{
      height: 100%; width: 0%; background: linear-gradient(90deg, #0072ce, #10b981);
      transition: width 0.3s ease; border-radius: 9999px;
    }}

    /* NAVIGATION & FILTERS */
    .sticky-nav-bar {{
      position: sticky; top: 0; z-index: 50;
      background: rgba(7, 9, 14, 0.92);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      padding: 0.85rem 2rem;
    }}
    .nav-inner {{
      max-width: 1300px; margin: 0 auto;
      display: flex; justify-content: space-between; align-items: center;
      gap: 1.25rem; flex-wrap: wrap;
    }}
    .cat-pills-wrap {{
      display: flex; gap: 8px; overflow-x: auto; padding-bottom: 4px; scrollbar-width: thin;
      max-width: 780px;
    }}
    .cat-pill {{
      background: var(--bg-card); border: 1px solid var(--border);
      color: var(--text-muted); font-size: 0.8rem; font-weight: 600;
      padding: 6px 14px; border-radius: 9999px; cursor: pointer;
      white-space: nowrap; transition: all 0.2s; font-family: var(--font-sans);
    }}
    .cat-pill:hover {{ border-color: var(--gartner-accent); color: #fff; }}
    .cat-pill.active {{
      background: linear-gradient(135deg, #0072ce, #004b87);
      border-color: #38bdf8; color: #fff; font-weight: 700;
      box-shadow: 0 4px 12px rgba(0, 114, 206, 0.3);
    }}

    .search-box-wrapper {{ position: relative; min-width: 240px; flex: 1; max-width: 380px; }}
    .search-box-wrapper input {{
      width: 100%; background: var(--bg-card); border: 1px solid var(--border);
      padding: 7px 14px 7px 34px; border-radius: 9999px; color: #fff;
      font-size: 0.85rem; outline: none; transition: border-color 0.2s;
    }}
    .search-box-wrapper input:focus {{ border-color: var(--gartner-accent); }}
    .search-icon {{
      position: absolute; left: 12px; top: 50%; transform: translateY(-50%);
      font-size: 0.85rem; color: var(--text-dim); pointer-events: none;
    }}

    /* MAIN CONTAINER */
    .main-layout {{
      max-width: 1300px; margin: 0 auto; padding: 2rem 2rem 4rem 2rem;
    }}

    /* SECTION HEADERS */
    .section-title-wrap {{
      margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 1rem;
    }}
    .section-title-wrap h2 {{
      font-size: 1.55rem; font-weight: 800; color: #fff; letter-spacing: -0.02em;
    }}
    .section-title-wrap p {{ color: var(--text-muted); font-size: 0.92rem; margin-top: 4px; }}

    /* ACCORDION CARDS */
    .cards-grid {{ display: flex; flex-direction: column; gap: 1.25rem; }}
    .q-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      transition: all 0.2s;
    }}
    .q-card:hover {{ border-color: rgba(0, 114, 206, 0.4); }}
    .q-header {{
      background: rgba(15, 20, 34, 0.7);
      padding: 1.15rem 1.5rem;
      display: flex; justify-content: space-between; align-items: center;
      cursor: pointer; user-select: none;
      border-bottom: 1px solid rgba(255,255,255,0.04);
    }}
    .q-header-left {{ display: flex; align-items: center; gap: 14px; flex: 1; }}
    .q-num-badge {{
      background: rgba(0, 114, 206, 0.2); color: #38bdf8;
      border: 1px solid rgba(0, 114, 206, 0.4);
      padding: 4px 10px; border-radius: 8px; font-size: 0.8rem;
      font-family: var(--font-mono); font-weight: 800; white-space: nowrap;
    }}
    .q-title-text {{ font-size: 1.05rem; font-weight: 700; color: #f1f5f9; }}
    .q-cat-tag {{
      display: inline-block; font-size: 0.72rem; color: #94a3b8; font-family: var(--font-mono);
      background: rgba(255,255,255,0.05); padding: 2px 8px; border-radius: 4px; margin-top: 4px;
    }}
    .q-header-right {{ display: flex; align-items: center; gap: 12px; }}
    .q-checkbox {{
      width: 18px; height: 18px; cursor: pointer; accent-color: var(--gartner-emerald);
    }}
    .q-toggle-btn {{
      background: none; border: none; color: var(--text-dim);
      font-size: 0.85rem; cursor: pointer; transition: transform 0.2s;
    }}
    .q-card.open .q-toggle-btn {{ transform: rotate(180deg); color: #38bdf8; }}
    .q-body {{
      display: none; padding: 1.75rem; color: #cbd5e1; font-size: 0.94rem; line-height: 1.75;
    }}
    .q-card.open .q-body {{ display: block; }}
    .q-body strong {{ color: #ffffff; font-weight: 700; }}

    .q-footer-bar {{
      display: flex; justify-content: space-between; align-items: center;
      border-top: 1px solid rgba(255,255,255,0.06); padding-top: 1.25rem; margin-top: 1.5rem;
      font-size: 0.82rem; color: var(--text-dim);
    }}
    .copy-btn {{
      background: rgba(0, 114, 206, 0.15); border: 1px solid rgba(0, 114, 206, 0.35);
      color: #38bdf8; font-size: 0.8rem; font-weight: 600; padding: 6px 14px;
      border-radius: 8px; cursor: pointer; transition: all 0.2s;
    }}
    .copy-btn:hover {{ background: rgba(0, 114, 206, 0.3); color: #fff; }}

    /* CODE STYLING */
    pre {{
      background: #090d17 !important;
      border: 1px solid #1c2742;
      border-radius: 10px;
      padding: 1.25rem;
      overflow-x: auto;
      margin: 1rem 0;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      line-height: 1.5;
    }}
    code {{
      font-family: var(--font-mono);
      font-size: 0.88em;
      background: rgba(0, 114, 206, 0.1);
      color: #38bdf8;
      padding: 2px 6px;
      border-radius: 4px;
    }}
    pre code {{
      background: transparent !important;
      color: #e2e8f0;
      padding: 0;
    }}

    /* TOAST */
    #toast {{
      position: fixed; bottom: 30px; right: 30px;
      background: #0072ce; color: #fff;
      padding: 12px 20px; border-radius: 10px;
      font-weight: 700; font-size: 0.88rem;
      box-shadow: 0 10px 25px rgba(0,0,0,0.6);
      display: none; z-index: 100000;
    }}

    @media (max-width: 768px) {{
      .header-container {{ flex-direction: column; }}
      .cat-pills-wrap {{ max-width: 100%; }}
      .top-header {{ padding: 1.5rem 1rem; }}
      .main-layout {{ padding: 1rem 1rem 3rem 1rem; }}
    }}
  </style>
</head>
<body>

  <!-- PASSCODE LOCK SCREEN -->
  <div id="lockScreen">
    <div class="lock-box">
      <div class="lock-logo-mark">
        <span class="lock-txt-1">GARTNER</span><span class="lock-txt-2">·AI</span>
        <span class="lock-badge-pill">AGENTIC AI APPLICATIONS</span>
      </div>
      <h2>Enterprise Preparation Suite</h2>
      <p>Candidate: Rujuwal Garg · Team Lead (Data Analytics & AI Engineering)</p>
      
      <form onsubmit="handleUnlock(event)">
        <div class="input-group">
          <input type="password" id="passInput" placeholder="Enter Access Passcode" autofocus autocomplete="off" />
        </div>
        <button type="submit" class="unlock-btn">
          <span>Unlock Interview Suite</span> ➔
        </button>
      </form>
      <div id="lockError" class="lock-err">Invalid Passcode. Hint: Company Name (Gartner)</div>
    </div>
  </div>

  <!-- MAIN APP CONTAINER -->
  <div id="appContent">

    <!-- TOP HEADER -->
    <header class="top-header">
      <div class="header-container">
        <div class="candidate-profile">
          <div class="title-row">
            <h1 class="candidate-name">Rujuwal Garg</h1>
            <span class="target-company-badge">Gartner · Agentic AI Applications</span>
            <span class="role-badge">Team Lead · 4+ Years Experience</span>
          </div>
          <p class="profile-subtitle">
            Delhi, India · rujuwal1@gmail.com · +91-9211199998 · Specialized in Multi-Agent Orchestration, Advanced RAG, FastAPI & Enterprise Knowledge Systems
          </p>
          <div class="tags-container">
            <span class="skill-tag accent">LangGraph</span>
            <span class="skill-tag accent">Multi-Agent Systems</span>
            <span class="skill-tag accent">Advanced RAG & RRF</span>
            <span class="skill-tag accent">FastAPI & Async</span>
            <span class="skill-tag accent">Model Context Protocol (MCP)</span>
            <span class="skill-tag">AWS ECS / Fargate</span>
            <span class="skill-tag">Amazon DynamoDB</span>
            <span class="skill-tag">OpenSearch / pgvector</span>
            <span class="skill-tag">LangSmith & RAGAS</span>
            <span class="skill-tag">MongoDB</span>
            <span class="skill-tag">NeMo Guardrails</span>
          </div>
        </div>

        <div class="header-stats-card">
          <div class="stat-row">
            <span class="stat-label">Interview Track</span>
            <span class="stat-value">Agentic AI Applications</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Technical Questions</span>
            <span class="stat-value highlight">30 Master Questions</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Depth Standard</span>
            <span class="stat-value">&ge; 300 Words / Answer</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Questions Reviewed</span>
            <span class="stat-value" id="qTrackerText">0 / 30 Completed</span>
          </div>
          <div class="progress-bar-container">
            <div class="progress-bar-fill" id="progressFill"></div>
          </div>
        </div>
      </div>
    </header>

    <!-- STICKY NAV -->
    <nav class="sticky-nav-bar">
      <div class="nav-inner">
        <div class="cat-pills-wrap" id="categoryPills">
          <!-- Populated by JS -->
        </div>
        <div class="search-box-wrapper">
          <span class="search-icon">🔍</span>
          <input type="text" id="searchInput" placeholder="Search keywords (e.g. LangGraph, RRF, DynamoDB)..." oninput="handleSearch()" />
        </div>
      </div>
    </nav>

    <!-- MAIN SECTIONS -->
    <main class="main-layout">
      <div class="section-title-wrap">
        <h2>30 Enterprise Technical Interview Questions & In-Depth Answers</h2>
        <p>Architected specifically for Gartner's Digital Assistant & Sales/Service Delivery Enablement Ecosystem</p>
      </div>

      <div class="cards-grid" id="questionsContainer">
        <!-- Populated by JS -->
      </div>
    </main>

  </div>

  <div id="toast">Copied to Clipboard!</div>

  <script>
    const questionsData = {json_questions_data};
    const PASSCODE = "Gartner";
    const STORAGE_KEY = "auth_rujuwal_gartner_prep";

    function checkAuth() {{
      if (sessionStorage.getItem(STORAGE_KEY) === "true") {{
        revealContent();
      }}
    }}

    function handleUnlock(e) {{
      if (e) e.preventDefault();
      const input = document.getElementById("passInput").value.trim();
      if (input.toLowerCase() === PASSCODE.toLowerCase()) {{
        sessionStorage.setItem(STORAGE_KEY, "true");
        revealContent();
      }} else {{
        document.getElementById("lockError").style.display = "block";
      }}
    }}

    function revealContent() {{
      document.getElementById("lockScreen").style.display = "none";
      const app = document.getElementById("appContent");
      app.style.display = "block";
      setTimeout(() => app.style.opacity = "1", 20);
      renderCategories();
      renderQuestions();
      updateProgress();
    }}

    let activeCategory = "ALL";

    function renderCategories() {{
      const cats = ["ALL", ...new Set(questionsData.map(q => q.category))];
      const container = document.getElementById("categoryPills");
      container.innerHTML = cats.map((cat, idx) => `
        <button class="cat-pill ${{idx === 0 ? 'active' : ''}}" onclick="filterCategory('${{cat}}', this)">
          ${{cat}}
        </button>
      `).join("");
    }}

    function filterCategory(cat, btn) {{
      activeCategory = cat;
      document.querySelectorAll(".cat-pill").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      applyFilters();
    }}

    function renderQuestions() {{
      const container = document.getElementById("questionsContainer");
      container.innerHTML = questionsData.map(q => {{
        return `
          <div class="q-card" id="card-${{q.id}}" data-category="${{q.category}}" data-search="${{(q.question + ' ' + q.category + ' ' + q.answer).toLowerCase()}}">
            <div class="q-header" onclick="toggleCard('card-${{q.id}}')">
              <div class="q-header-left">
                <span class="q-num-badge">Q${{q.id}}</span>
                <div>
                  <div class="q-title-text">${{q.question}}</div>
                  <span class="q-cat-tag">${{q.category}}</span>
                </div>
              </div>
              <div class="q-header-right">
                <input type="checkbox" class="q-checkbox" 
                       id="chk-${{q.id}}" 
                       onclick="event.stopPropagation(); toggleCheck('${{q.id}}')" 
                       title="Mark question reviewed" />
                <button class="q-toggle-btn">▼</button>
              </div>
            </div>
            <div class="q-body">
              <div class="q-answer-content">
                ${{formatMarkdownContent(q.answer)}}
              </div>
              <div class="q-footer-bar">
                <span>~${{q.answer.split(' ').length}} Words · Production Architecture Deep Dive</span>
                <button class="copy-btn" onclick="copyAnswer(${{q.id}}, this)">📋 Copy Answer</button>
              </div>
            </div>
          </div>
        `;
      }}).join("");

      // Restore checkboxes from localStorage
      questionsData.forEach(q => {{
        const key = `gartner_q_${{q.id}}`;
        if (localStorage.getItem(key) === "true") {{
          const el = document.getElementById(`chk-${{q.id}}`);
          if (el) el.checked = true;
        }}
      }});
      updateProgress();
    }}

    function toggleCard(id) {{
      const card = document.getElementById(id);
      if (card) card.classList.toggle("open");
    }}

    function toggleCheck(id) {{
      const key = `gartner_q_${{id}}`;
      const el = document.getElementById(`chk-${{id}}`);
      if (el) {{
        localStorage.setItem(key, el.checked ? "true" : "false");
      }}
      updateProgress();
    }}

    function updateProgress() {{
      const total = questionsData.length;
      let completed = 0;
      questionsData.forEach(q => {{
        if (localStorage.getItem(`gartner_q_${{q.id}}`) === "true") {{
          completed++;
        }}
      }});
      const pct = (completed / total) * 100;
      document.getElementById("progressFill").style.width = pct + "%";
      document.getElementById("qTrackerText").innerText = `${{completed}} / ${{total}} Completed (${{Math.round(pct)}}%)`;
    }}

    function copyAnswer(id, btn) {{
      const item = questionsData.find(q => q.id === id);
      if (!item) return;
      const text = `Q${{item.id}}: ${{item.question}}\\nCategory: ${{item.category}}\\n\\nANSWER:\\n${{item.answer}}`;
      navigator.clipboard.writeText(text).then(() => {{
        const toast = document.getElementById("toast");
        toast.style.display = "block";
        const orig = btn.innerText;
        btn.innerText = "✓ Copied!";
        setTimeout(() => {{
          toast.style.display = "none";
          btn.innerText = orig;
        }}, 2000);
      }});
    }}

    function formatMarkdownContent(raw) {{
      if (!raw) return "";
      let res = raw;
      // Code blocks
      res = res.replace(/```(python|sql|json|bash)?([\\s\\S]*?)```/g, '<pre><code>$2</code></pre>');
      // Inline code
      res = res.replace(/`([^`]+)`/g, '<code>$1</code>');
      // Bold
      res = res.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
      // Line breaks
      res = res.replace(/\\n\\n/g, '<br><br>');
      res = res.replace(/\\n/g, '<br>');
      return res;
    }}

    function handleSearch() {{
      applyFilters();
    }}

    function applyFilters() {{
      const query = document.getElementById("searchInput").value.toLowerCase().trim();
      document.querySelectorAll(".q-card").forEach(card => {{
        const cat = card.getAttribute("data-category");
        const text = card.getAttribute("data-search");
        const matchesCat = (activeCategory === "ALL" || cat === activeCategory);
        const matchesQuery = (!query || text.includes(query));
        if (matchesCat && matchesQuery) {{
          card.style.display = "block";
        }} else {{
          card.style.display = "none";
        }}
      }});
    }}

    window.addEventListener("DOMContentLoaded", checkAuth);
  </script>
</body>
</html>
"""

with open("rujuwal_gartner_agentic_ai_prep.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("Successfully generated rujuwal_gartner_agentic_ai_prep.html")
