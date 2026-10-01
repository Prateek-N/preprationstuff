# -*- coding: utf-8 -*-
"""
Master Generator Script for Karthik Ravula
AdsGency AI - Member of Technical Staff (MTS) - Full Stack / AI Systems
Generates:
1. karthik_adsgency_ai_prep.md (Pure Markdown Guide)
2. content/karthik-adsgency-ai-prep.mdx (Protected Nextra MDX with <PasswordGate>)
3. karthik_adsgency_ai_prep.html (Standalone Protected Web Application)
4. public/karthik_adsgency_ai_prep.html (Static Production HTML)
"""

import json
import os
import re

from karthik_adsgency_data_part1 import verbal_questions
from karthik_adsgency_data_part2 import dsa_questions
from karthik_adsgency_data_part3 import sysde_questions

print(f"Loaded Verbal Questions: {len(verbal_questions)}")
print(f"Loaded DSA Questions: {len(dsa_questions)}")
print(f"Loaded System Design Questions: {len(sysde_questions)}")

# =========================================================================
# 1. GENERATE MASTER MARKDOWN FILE & NEXTA MDX FILE
# =========================================================================

md_lines = []

# Title & Metadata Header
md_lines.append("# AdsGency AI — Member of Technical Staff (Full Stack / AI Systems) Interview Master Guide")
md_lines.append("**Candidate:** Karthik Ravula | Software Developer (3+ Years Experience: Uber, Epsilon, Dell Technologies | M.S. Data Science NYIT)")
md_lines.append("**Target Role:** Member of Technical Staff (MTS) – Full Stack / AI Systems — AdsGency AI (Onsite San Francisco City)")
md_lines.append("**Core Mission:** Building the autonomous multi-agent operating system for digital advertising across Google Ads, Meta Graph API, and TikTok Marketing API.\n")
md_lines.append("---\n")

# Executive Alignment Section
md_lines.append("## Executive Strategy & Role Alignment\n")
md_lines.append("This technical preparation suite is tailored specifically for **Karthik Ravula** interviewing for the **Member of Technical Staff (MTS) – Full Stack / AI Systems** role at **AdsGency AI** in San Francisco.\n")
md_lines.append("AdsGency AI is reimagining the $800B digital advertising industry with an AI-native multi-agent layer that autonomously plans, generates, optimizes, and scales ad campaigns without human marketers. Karthik's background directly solves AdsGency's foundational technical challenges:\n")
md_lines.append("1. **Distributed FastAPI & High-Throughput Microservices:** Engineered FastAPI microservices at **Uber** handling 580K+ monthly trip records and at **Epsilon** routing 2,000,000 daily API requests across 3 external marketing platforms with sub-50ms latency.\n")
md_lines.append("2. **Autonomous Multi-Agent Orchestration (LangGraph / CrewAI):** Designing hierarchical supervisor-worker state machines that execute complex campaign generation workflows with loop detection, deterministic checkpoints, and safety guardrails.\n")
md_lines.append("3. **Real-Time Streaming & Budget Pacing:** Utilizing **Apache Kafka**, **Redis** atomic Lua counters, and PostgreSQL to track live ad spend and trigger sub-500ms emergency circuit breakers against budget overruns.\n")
md_lines.append("4. **Full-Stack Execution with Next.js & React:** Built responsive Next.js and React dashboards at **Uber** supporting 500K+ daily requests, cutting load times by 1.3 seconds and delivering live Server-Sent Events (SSE) telemetry to operators.\n")
md_lines.append("5. **Enterprise Security & AdTech API Integrations:** Authored secure GraphQL/REST APIs with JWT and OAuth 2.0 at **Epsilon**, protecting 500K customer profiles for HIPAA/GDPR compliance, while orchestrating high-concurrency external integrations with Google Ads, Meta Graph, and TikTok APIs.\n\n")
md_lines.append("---\n")

# PART 1: Verbal Technical Q&As
md_lines.append("# Part 1: Top 20 Verbal Technical Interview Questions & Narrative Answers\n")
md_lines.append("Every answer is crafted in an in-depth, cohesive ~300-word narrative format directly rooted in Karthik Ravula's resume accomplishments at Uber, Epsilon, and Dell Technologies, with core technologies and metrics highlighted in bold.\n\n")

for q in verbal_questions:
    md_lines.append(f"## Question {q['id']}: {q['question']}")
    md_lines.append(f"**Domain:** {q['category']}\n")
    md_lines.append(q['answer'].strip() + "\n")
    md_lines.append("---\n")

# PART 2: DSA Coding Questions
md_lines.append("# Part 2: Top 15 Coding & Algorithm Challenges in Python\n")
md_lines.append("Each problem follows the strict four-step interview cadence: **Problem Statement**, **Complete Thought Process & Intuition**, **Production-Grade Python Code with Inline Comments**, and **Time & Space Complexity Analysis**.\n\n")

for q in dsa_questions:
    md_lines.append(f"## Problem {q['id']}: {q['title']}")
    md_lines.append(f"**Topic:** {q['topic']} | **Difficulty:** {q['difficulty']}\n")
    
    md_lines.append("### 1. Problem Statement")
    md_lines.append(q['problem_statement'].strip() + "\n")
    
    md_lines.append("### 2. Complete Thought Process & Intuition")
    md_lines.append(q['thought_process'].strip() + "\n")
    
    md_lines.append("### 3. Python 3 Implementation")
    md_lines.append("```python")
    md_lines.append(q['code'].strip())
    md_lines.append("```\n")
    
    md_lines.append("### 4. Complexity Analysis")
    md_lines.append(q['complexity'].strip() + "\n")
    md_lines.append("---\n")

# PART 3: System Design Questions
md_lines.append("# Part 3: Top 10 System Designs (AdsGency AI Infrastructure)\n")
md_lines.append("Every system design breakdown is presented in a **simple, conversational walkthrough format written in small, clear paragraph chunks WITHOUT ANY BULLET POINTS**, guiding the interviewer naturally through Functional Requirements, Non-Functional Requirements, Core Entities, API Design, Data Flow, High-Level Architecture, and Non-Functional Deep Dives.\n\n")

for s in sysde_questions:
    md_lines.append(f"## System Design {s['id']}: {s['title']}")
    md_lines.append(f"**Domain Category:** {s['category']}\n")
    
    md_lines.append("### 1. Complete Problem Statement")
    md_lines.append(s['problem_statement'].strip() + "\n")
    
    md_lines.append("### 2. High-Level Architecture Diagram")
    md_lines.append(s['diagram'].strip() + "\n")
    
    md_lines.append("### 3. Functional Requirements (Conversational Walkthrough)")
    md_lines.append(s['functional_requirements'].strip() + "\n")
    
    md_lines.append("### 4. Non-Functional Requirements (Conversational Walkthrough)")
    md_lines.append(s['non_functional_requirements'].strip() + "\n")
    
    md_lines.append("### 5. Core Entities & Data Modeling")
    md_lines.append(s['core_entities'].strip() + "\n")
    
    md_lines.append("### 6. API & Interface Design")
    md_lines.append(s['api_design'].strip() + "\n")
    
    md_lines.append("### 7. End-to-End Data Flow")
    md_lines.append(s['data_flow'].strip() + "\n")
    
    md_lines.append("### 8. High-Level System Architecture (HLD)")
    md_lines.append(s['high_level_design'].strip() + "\n")
    
    md_lines.append("### 9. Deep Dive into Non-Functional Requirements & Resilience")
    md_lines.append(s['nfr_deep_dive'].strip() + "\n")
    md_lines.append("---\n")

raw_markdown = "\n".join(md_lines)

# Write master pure markdown file
with open("karthik_adsgency_ai_prep.md", "w", encoding="utf-8") as f:
    f.write(raw_markdown)
print("Wrote karthik_adsgency_ai_prep.md successfully.")

# Write Nextra MDX with PasswordGate
mdx_frontmatter = """---
title: Karthik Ravula — AdsGency AI Member of Technical Staff Prep Guide
description: Complete technical preparation suite for Member of Technical Staff (Full Stack / AI Systems) at AdsGency AI (SF) — 20 Verbal Tech Q&As, 15 Python DSA, and 10 Conversational System Designs.
---

<PasswordGate password="Karthik" candidateName="Karthik Ravula">

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

with open("content/karthik-adsgency-ai-prep.mdx", "w", encoding="utf-8") as f:
    f.write(mdx_frontmatter + sanitized_md_content + mdx_closing)
print("Wrote content/karthik-adsgency-ai-prep.mdx successfully with <PasswordGate>.")


# =========================================================================
# 2. GENERATE PROTECTED STANDALONE HTML APPLICATION
# =========================================================================

items_data = []

# Add Verbal Questions
for q in verbal_questions:
    def format_answer(ans):
        paragraphs = [p.strip() for p in ans.strip().split("\n\n") if p.strip()]
        return "".join([f'<p class="conv-p">{p.replace(chr(10), " ")}</p>' for p in paragraphs])

    items_data.append({
        "num": q["id"],
        "type": "verbal",
        "title": f"Q{q['id']}: {q['question']}",
        "category": "Verbal Technical & Architecture",
        "subCategory": q["category"],
        "difficulty": "Staff / MTS Interview",
        "search_text": f"{q['question']} {q['category']} {q['answer']}".lower(),
        "html_content": f"""
        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-purple">Interview Question</span></h4>
          <p class="body-p" style="font-weight: 600; font-size: 1.05rem; color: #f8fafc;">{q['question']}</p>
        </div>
        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-cyan">In-Depth Technical Response (~300 Words)</span></h4>
          {format_answer(q['answer'])}
        </div>
        """
    })

# Add DSA questions
for q in dsa_questions:
    items_data.append({
        "num": q["id"] + 20,
        "dsa_id": q["id"],
        "type": "dsa",
        "title": f"Problem {q['id']}: {q['title']}",
        "category": "DSA & Algorithms",
        "subCategory": q["topic"],
        "difficulty": q["difficulty"],
        "search_text": f"{q['title']} {q['topic']} {q['problem_statement']} {q['thought_process']}".lower(),
        "html_content": f"""
        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-amz">Problem Statement</span></h4>
          <p class="body-p">{q['problem_statement'].replace(chr(10), '<br>')}</p>
        </div>
        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-purple">Complete Thought Process & Intuition</span></h4>
          <p class="body-p">{q['thought_process'].replace(chr(10), '<br>')}</p>
        </div>
        <div class="section-block">
          <div class="code-header">
            <span>Python 3 Solution</span>
            <button class="btn-copy-code" onclick="copyCode(this)">Copy Code</button>
          </div>
          <pre class="code-box"><code class="language-python">{q['code'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</code></pre>
        </div>
        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-green">Complexity Analysis</span></h4>
          <div class="complexity-box">{q['complexity'].replace(chr(10), '<br>')}</div>
        </div>
        """
    })

# Add System Design questions
for s in sysde_questions:
    def p_chunks(text: str) -> str:
        paragraphs = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
        return "".join([f'<p class="conv-p">{p.replace(chr(10), " ")}</p>' for p in paragraphs])

    items_data.append({
        "num": s["id"] + 35,
        "sys_id": s["id"],
        "type": "sysde",
        "title": f"System Design {s['id']}: {s['title']}",
        "category": "System Design",
        "subCategory": s["category"],
        "difficulty": "MTS / Principal SDE",
        "search_text": f"{s['title']} {s['category']} {s['problem_statement']} {s['functional_requirements']} {s['high_level_design']}".lower(),
        "html_content": f"""
        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-amz">Problem Statement</span></h4>
          <p class="conv-p">{s['problem_statement'].strip()}</p>
        </div>

        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-purple">High-Level Architecture Diagram</span></h4>
          <pre class="code-box" style="color: #38bdf8; font-family: monospace;"><code>{s['diagram'].replace('```', '').strip()}</code></pre>
        </div>

        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-cyan">Functional Requirements (Conversational Walkthrough)</span></h4>
          {p_chunks(s['functional_requirements'])}
        </div>

        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-amber">Non-Functional Requirements (Conversational Walkthrough)</span></h4>
          {p_chunks(s['non_functional_requirements'])}
        </div>

        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-blue">Core Entities & Data Modeling</span></h4>
          {p_chunks(s['core_entities'])}
        </div>

        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-purple">API & Interface Design</span></h4>
          {p_chunks(s['api_design'])}
        </div>

        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-green">End-to-End Data Flow</span></h4>
          {p_chunks(s['data_flow'])}
        </div>

        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-cyan">High-Level System Architecture (HLD)</span></h4>
          {p_chunks(s['high_level_design'])}
        </div>

        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-rose">Deep Dive into Non-Functional Requirements & Resilience</span></h4>
          {p_chunks(s['nfr_deep_dive'])}
        </div>
        """
    })

items_json_str = json.dumps(items_data)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Karthik Ravula — AdsGency AI MTS (Full Stack / AI Systems) Interview Suite</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
  <style>
    :root {{
      --bg-primary: #0b0f19;
      --bg-secondary: #111827;
      --bg-card: #161f33;
      --bg-card-hover: #1e2942;
      --accent-purple: #a855f7;
      --accent-blue: #3b82f6;
      --accent-cyan: #06b6d4;
      --accent-green: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --border-color: rgba(255, 255, 255, 0.08);
      --border-focus: rgba(168, 85, 247, 0.4);
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

    /* Glassmorphism Lock Overlay */
    #lockOverlay {{
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(11, 15, 25, 0.88);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      z-index: 99999;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }}

    .lock-card {{
      background: rgba(22, 31, 51, 0.95);
      border: 1px solid rgba(168, 85, 247, 0.35);
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 40px rgba(168, 85, 247, 0.15);
      border-radius: 24px;
      padding: 3rem 2.5rem;
      max-width: 480px;
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
      background: rgba(168, 85, 247, 0.15);
      border: 1px solid rgba(168, 85, 247, 0.3);
      color: #c084fc;
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
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--accent-cyan);
      margin-bottom: 0.75rem;
    }}

    .lock-sub {{
      color: var(--text-muted);
      font-size: 0.9rem;
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
      background: rgba(11, 15, 25, 0.7);
      border: 1px solid var(--border-color);
      color: #fff;
      font-size: 1rem;
      font-family: var(--font-sans);
      outline: none;
      transition: all 0.2s;
    }}

    .lock-input:focus {{
      border-color: var(--accent-purple);
      box-shadow: 0 0 15px rgba(168, 85, 247, 0.3);
    }}

    .lock-btn {{
      padding: 0.85rem 1.5rem;
      border-radius: 12px;
      background: linear-gradient(135deg, #a855f7, #6366f1);
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

    /* App Header */
    header {{
      background: rgba(17, 24, 39, 0.85);
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
      width: 40px;
      height: 40px;
      border-radius: 10px;
      background: linear-gradient(135deg, #a855f7, #3b82f6);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      font-size: 1.2rem;
      color: #fff;
      box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
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
      background: rgba(22, 31, 51, 0.5);
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
      border-color: var(--accent-purple);
    }}

    .filter-tabs {{
      display: flex;
      gap: 0.4rem;
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border-color);
      background: rgba(11, 15, 25, 0.4);
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
      background: rgba(168, 85, 247, 0.2);
      border-color: rgba(168, 85, 247, 0.4);
      color: #e9d5ff;
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
      background: rgba(168, 85, 247, 0.15);
      border-color: var(--accent-purple);
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

    .badge-verbal {{ background: rgba(59, 130, 246, 0.2); color: #93c5fd; }}
    .badge-dsa {{ background: rgba(16, 185, 129, 0.2); color: #6ee7b7; }}
    .badge-sysde {{ background: rgba(168, 85, 247, 0.2); color: #d8b4fe; }}

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
      padding: 2rem 2.5rem;
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
    }}

    .detail-title {{
      font-size: 1.65rem;
      font-weight: 800;
      color: #fff;
      line-height: 1.3;
      letter-spacing: -0.02em;
    }}

    .section-block {{
      margin-bottom: 2rem;
    }}

    .sec-title {{
      font-size: 0.9rem;
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
    .badge-blue {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }}
    .badge-cyan {{ background: rgba(6, 182, 212, 0.15); color: #22d3ee; border: 1px solid rgba(6, 182, 212, 0.3); }}
    .badge-green {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
    .badge-amber {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }}
    .badge-rose {{ background: rgba(244, 63, 94, 0.15); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.3); }}
    .badge-amz {{ background: rgba(249, 115, 22, 0.15); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.3); }}

    .conv-p {{
      color: #cbd5e1;
      font-size: 0.95rem;
      line-height: 1.75;
      margin-bottom: 1.15rem;
    }}

    .body-p {{
      color: #cbd5e1;
      font-size: 0.95rem;
      line-height: 1.7;
    }}

    .code-header {{
      background: #1e293b;
      padding: 0.5rem 1rem;
      border-radius: 8px 8px 0 0;
      border: 1px solid #334155;
      border-bottom: none;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.8rem;
      font-weight: 600;
      color: #94a3b8;
    }}

    .btn-copy-code {{
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #f1f5f9;
      padding: 0.25rem 0.6rem;
      border-radius: 4px;
      font-size: 0.75rem;
      cursor: pointer;
    }}

    .btn-copy-code:hover {{
      background: rgba(255, 255, 255, 0.2);
    }}

    .code-box {{
      margin: 0 0 1.5rem 0;
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 0 0 8px 8px;
      padding: 1.25rem;
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      line-height: 1.6;
    }}

    .complexity-box {{
      background: #1e293b;
      border: 1px solid #334155;
      border-left: 4px solid var(--accent-green);
      border-radius: 6px;
      padding: 0.85rem 1.25rem;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      color: #a7f3d0;
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
      <div class="lock-title">AdsGency AI Interview Portal</div>
      <div class="lock-candidate">Karthik Ravula</div>
      <div class="lock-sub">Member of Technical Staff – Full Stack / AI Systems<br>(San Francisco City · Onsite)</div>
      
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
        <h1>Karthik Ravula — AdsGency AI Prep Suite</h1>
        <p>Member of Technical Staff (Full Stack / AI Systems) · 20 Verbal · 15 DSA · 10 System Designs</p>
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
        <input type="text" id="searchInput" class="search-input" placeholder="Search questions, algorithms, concepts..." oninput="handleSearch()" />
      </div>
      <div class="filter-tabs">
        <button class="filter-btn active" onclick="setFilter('all', this)">All (45)</button>
        <button class="filter-btn" onclick="setFilter('verbal', this)">Verbal (20)</button>
        <button class="filter-btn" onclick="setFilter('dsa', this)">DSA Coding (15)</button>
        <button class="filter-btn" onclick="setFilter('sysde', this)">System Design (10)</button>
      </div>
      <div class="items-scroll" id="itemsList"></div>
    </div>

    <!-- Detail View -->
    <div class="detail-panel" id="detailPanel">
      <!-- Dynamic Content Injected Here -->
    </div>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
  <script>
    const MASTER_PASS = "Karthik";
    const SESSION_KEY = "karthik_adsgency_unlocked";
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

        let badgeClass = 'badge-verbal';
        let badgeLabel = 'Verbal';
        if (item.type === 'dsa') {{ badgeClass = 'badge-dsa'; badgeLabel = 'DSA'; }}
        else if (item.type === 'sysde') {{ badgeClass = 'badge-sysde'; badgeLabel = 'System Design'; }}

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

      let badgeClass = 'badge-purple';
      if (item.type === 'verbal') badgeClass = 'badge-blue';
      else if (item.type === 'dsa') badgeClass = 'badge-green';

      const panel = document.getElementById("detailPanel");
      panel.innerHTML = `
        <div class="detail-header">
          <span class="detail-tag ${{badgeClass}}">${{item.category}} · ${{item.subCategory}}</span>
          <h2 class="detail-title">${{item.title}}</h2>
        </div>
        ${{item.html_content}}
      `;

      if (window.Prism) {{
        Prism.highlightAllUnder(panel);
      }}
      panel.scrollTop = 0;

      // Update active in sidebar
      const cards = document.querySelectorAll(".item-card");
      cards.forEach(card => {{
        if (card.querySelector(".item-num") && card.querySelector(".item-num").innerText === `#${{num}}`) {{
          card.classList.add("active");
        }}
      }});
    }}

    function copyCode(btn) {{
      const code = btn.closest(".section-block").querySelector("code").innerText;
      navigator.clipboard.writeText(code).then(() => {{
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
with open("karthik_adsgency_ai_prep.html", "w", encoding="utf-8") as f:
    f.write(html_template)
print("Wrote karthik_adsgency_ai_prep.html successfully.")

with open("public/karthik_adsgency_ai_prep.html", "w", encoding="utf-8") as f:
    f.write(html_template)
print("Wrote public/karthik_adsgency_ai_prep.html successfully.")
