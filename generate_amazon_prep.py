# -*- coding: utf-8 -*-
"""
Master Generator Script for Ashutosh Rudraksh
Amazon Advertising in Live Events - AI Engineer Technical Interview Preparation Suite
Generates:
1. amazon_live_events_ai_ashutosh_prep.md (Comprehensive Markdown Guide)
2. content/ashutosh-amazon-live-events-prep.mdx (Protected Nextra MDX with <PasswordGate>)
3. amazon_live_events_ai_ashutosh_prep.html (Standalone Protected Web Application)
4. public/amazon_live_events_ai_ashutosh_prep.html (Static Production HTML)
"""

import json
import os
import re
from amazon_prep_dsa import dsa_questions
from amazon_prep_sysde_part1 import sysde_questions_part1
from amazon_prep_sysde_part2 import sysde_questions_part2
from amazon_prep_sysde_part3 import sysde_questions_part3

all_sysde = sysde_questions_part1 + sysde_questions_part2 + sysde_questions_part3

print(f"Total DSA Questions: {len(dsa_questions)}")
print(f"Total System Design Questions: {len(all_sysde)}")

# =========================================================================
# 1. GENERATE MASTER MARKDOWN FILE & NEXTA MDX FILE
# =========================================================================

md_body_lines = []

# Title & Metadata
md_body_lines.append("# Amazon Advertising in Live Events — AI Engineer Technical Interview Master Guide")
md_body_lines.append("**Candidate:** Ashutosh Rudraksh | Software Engineer (4 Years Experience: Uber, Meta Reality Labs, Tekainos, Dell Technologies | M.S. CS Ohio State University)")
md_body_lines.append("**Target Role:** AI Engineer — Amazon Advertising in Live Events (Thursday Night Football, NBA, NASCAR, Prime Video)")
md_body_lines.append("**Core Focus:** Ultra-Low Latency Distributed Systems, Real-Time Ad Decisioning, Server-Side Ad Insertion (SSAI), Agentic Operations (MCP), Multimodal Video AI, and High-Throughput Stream Telemetry\n")
md_body_lines.append("---\n")

# Executive Summary & Interview Roadmap
md_body_lines.append("## Executive Strategy & Role Alignment\n")
md_body_lines.append("This preparation suite is specifically architected for the **AI Engineer - Amazon Advertising in Live Events** technical interview rounds. Amazon live sports broadcasts (such as Thursday Night Football, NBA, and NASCAR) operate at unprecedented concurrency—serving over **15 million concurrent viewers** entering commercial breaks at the exact same split-second.\n")
md_body_lines.append("As an engineer with deep expertise across **FastAPI, Python, Java, Kubernetes, AWS (SageMaker, Bedrock, Lambda), Apache Kafka, Redis, pgvector, and Model Context Protocol (MCP)**, this guide bridges Ashutosh's production background directly with Amazon's core technical challenges:\n")
md_body_lines.append("1. **Broadcast-Grade Reliability & Latency:** Manifest generation in under 50ms, real-time ad auctions in under 40ms, and in-memory edge rewrites in under 10ms.\n")
md_body_lines.append("2. **AI & Agentic Operations:** Autonomous incident remediation using Model Context Protocol (MCP), continuous prompt evaluation pipelines (CI/CD for LLMs), and automated runbook synthesis for on-call engineers.\n")
md_body_lines.append("3. **Multimodal Broadcast AI:** Real-time brand safety classification and commercial break auto-cue prediction using computer vision and audio signals.\n")
md_body_lines.append("4. **High-Frequency Algorithmic Problem Solving:** Top 30 Python DSA implementations covering sliding windows, monotonic deques, priority queues, topological DAGs, and distributed streaming rate limiters.\n\n")
md_body_lines.append("---\n")

# PART 1: Top 30 DSA Questions
md_body_lines.append("# Part 1: Top 30 High-Frequency Amazon DSA Practice Questions in Python\n")
md_body_lines.append("Each problem follows the strict four-step interview cadence: **Problem Statement**, **Complete Thought Process & Intuition**, **Production-Grade Python Code with Inline Comments**, and **Time & Space Complexity Analysis**.\n\n")

for q in dsa_questions:
    md_body_lines.append(f"## Problem {q['id']}: {q['title']}")
    md_body_lines.append(f"**Topic:** {q['topic']} | **Difficulty:** {q['difficulty']}\n")
    
    md_body_lines.append("### 1. Problem Statement")
    md_body_lines.append(q['problem_statement'].strip() + "\n")
    
    md_body_lines.append("### 2. Complete Thought Process & Intuition")
    md_body_lines.append(q['thought_process'].strip() + "\n")
    
    md_body_lines.append("### 3. Python 3 Implementation")
    md_body_lines.append("```python")
    md_body_lines.append(q['code'].strip())
    md_body_lines.append("```\n")
    
    md_body_lines.append("### 4. Complexity Analysis")
    md_body_lines.append(q['complexity'].strip() + "\n")
    md_body_lines.append("---\n")

# PART 2: 30 System Design Questions
md_body_lines.append("# Part 2: Top 30 System Design Questions (Amazon Live Events & Advertising AI)\n")
md_body_lines.append("Every system design breakdown is presented in a **simple, conversational walkthrough format written in small, clear paragraph chunks WITHOUT ANY BULLET POINTS**, guiding the interviewer naturally through Functional Requirements, Non-Functional Requirements, Core Entities, API Design, Data Flow, High-Level Architecture, and Non-Functional Deep Dives.\n\n")

def svg_to_ascii(svg_html: str) -> str:
    title_m = re.search(r'font-size="15"[^>]*>([^<]+)<', svg_html)
    title = title_m.group(1) if title_m else 'High-Level Architecture'
    
    node_matches = re.findall(r'<g class="node"[^>]*>(.*?)</g>', svg_html, re.DOTALL)
    nodes = []
    for nm in node_matches:
        texts = re.findall(r'<text[^>]*>([^<]+)</text>', nm)
        if len(texts) >= 2:
            nodes.append((texts[0].strip(), texts[1].strip()))
        elif len(texts) == 1:
            nodes.append((texts[0].strip(), ''))
            
    out = ["```", f"=== {title.upper()} ===", ""]
    for i, (n1, n2) in enumerate(nodes):
        node_str = f"[{i+1}] {n1}" + (f" ({n2})" if n2 else "")
        out.append(node_str)
        if i < len(nodes) - 1:
            out.append("        │")
            out.append("        ▼")
    out.append("```\n")
    return "\n".join(out)

for s in all_sysde:
    md_body_lines.append(f"## System Design {s['id']}: {s['title']}")
    md_body_lines.append(f"**Domain Category:** {s['category']}\n")
    
    md_body_lines.append("### 1. Complete Problem Statement")
    md_body_lines.append(s['problem_statement'].strip() + "\n")
    
    md_body_lines.append("### 2. Clarifying Questions & Scope Definition")
    md_body_lines.append(s['clarifying_questions'].strip() + "\n")
    
    md_body_lines.append("### 3. High-Level Architecture Diagram")
    md_body_lines.append(svg_to_ascii(s['svg_diagram']) + "\n")
    
    md_body_lines.append("### 4. Functional Requirements")
    md_body_lines.append(s['functional_requirements'].strip() + "\n")
    
    md_body_lines.append("### 5. Non-Functional Requirements")
    md_body_lines.append(s['non_functional_requirements'].strip() + "\n")
    
    md_body_lines.append("### 6. Core Entities & Data Modeling")
    md_body_lines.append(s['core_entities'].strip() + "\n")
    
    md_body_lines.append("### 7. API & Interface Design")
    md_body_lines.append(s['api_design'].strip() + "\n")
    
    md_body_lines.append("### 8. End-to-End Data Flow")
    md_body_lines.append(s['data_flow'].strip() + "\n")
    
    md_body_lines.append("### 9. High-Level System Architecture (HLD)")
    md_body_lines.append(s['high_level_design'].strip() + "\n")
    
    md_body_lines.append("### 10. Deep Dive into Non-Functional Requirements & Edge Cases")
    md_body_lines.append(s['nfr_deep_dive'].strip() + "\n")
    md_body_lines.append("---\n")

raw_markdown = "\n".join(md_body_lines)

# Write master pure markdown file
with open("amazon_live_events_ai_ashutosh_prep.md", "w", encoding="utf-8") as f:
    f.write(raw_markdown)
print("Wrote amazon_live_events_ai_ashutosh_prep.md successfully.")

# Write Nextra MDX with PasswordGate
mdx_frontmatter = """---
title: Ashutosh Rudraksh — Amazon Live Events Advertising AI Engineer Prep
description: Complete technical preparation suite for AI Engineer at Amazon Advertising in Live Events (Thursday Night Football, NBA, NASCAR) — Top 30 Python DSA + Top 30 System Designs.
---

<PasswordGate password="Ashutosh" candidateName="Ashutosh Rudraksh">

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
        import re
        parts[i] = re.sub(r'<(?=[0-9\s])', '&lt;', parts[i])
        # Wrap URL/prose parameters like {job_id} in backticks so MDX does not evaluate them as JS expressions
        parts[i] = re.sub(r'\{([a-zA-Z0-9_-]+)\}', r'`{\1}`', parts[i])
    return '```'.join(parts)

sanitized_md_content = sanitize_mdx(raw_markdown)

with open("content/ashutosh-amazon-live-events-prep.mdx", "w", encoding="utf-8") as f:
    f.write(mdx_frontmatter + sanitized_md_content + mdx_closing)
print("Wrote content/ashutosh-amazon-live-events-prep.mdx successfully with <PasswordGate>.")

# Remove any old .md file in content/ to avoid route collision
if os.path.exists("content/ashutosh-amazon-live-events-prep.md"):
    os.remove("content/ashutosh-amazon-live-events-prep.md")
    print("Cleaned up redundant content/ashutosh-amazon-live-events-prep.md.")


# =========================================================================
# 2. GENERATE PROTECTED STANDALONE HTML APPLICATION
# =========================================================================

items_data = []

# Add DSA questions
for q in dsa_questions:
    items_data.append({
        "num": q["id"],
        "type": "dsa",
        "title": q["title"],
        "category": "DSA (Algorithms & Data Structures)",
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
for s in all_sysde:
    def p_chunks(text: str) -> str:
        paragraphs = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
        return "".join([f'<p class="conv-p">{p.replace(chr(10), " ")}</p>' for p in paragraphs])

    items_data.append({
        "num": s["id"] + 30,
        "sys_id": s["id"],
        "type": "sysde",
        "title": f"System Design {s['id']}: {s['title']}",
        "category": s["category"],
        "subCategory": "System Design & Architecture",
        "difficulty": "Staff / Principal SDE",
        "search_text": f"{s['title']} {s['category']} {s['problem_statement']} {s['functional_requirements']} {s['high_level_design']}".lower(),
        "html_content": f"""
        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-amz">Problem Statement</span></h4>
          <p class="conv-p">{s['problem_statement'].strip()}</p>
        </div>

        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-blue">Clarifying Questions & Conversational Scope</span></h4>
          {p_chunks(s['clarifying_questions'])}
        </div>

        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-purple">High-Level System Architecture Diagram</span></h4>
          {s['svg_diagram']}
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
          <h4 class="sec-title"><span class="badge badge-green">Core Entities & Data Modeling</span></h4>
          {p_chunks(s['core_entities'])}
        </div>

        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-blue">API & Interface Design</span></h4>
          {p_chunks(s['api_design'])}
        </div>

        <div class="section-block">
          <h4 class="sec-title"><span class="badge badge-purple">End-to-End Data Flow</span></h4>
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

items_json = json.dumps(items_data)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Amazon Advertising in Live Events — AI Engineer Technical Master Suite · Ashutosh Rudraksh</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-base: #070d18;
      --bg-surface: #0f172a;
      --bg-card: #142036;
      --bg-card-hover: #1c2b48;
      --border: #233452;
      --border-accent: #ff9900;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --amz-orange: #ff9900;
      --amz-gold: #fbbf24;
      --amz-blue: #38bdf8;
      --amz-cyan: #06b6d4;
      --amz-purple: #c084fc;
      --amz-green: #34d399;
      --amz-rose: #fb7185;
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
      background: radial-gradient(circle at center, #142442 0%, #070d18 100%);
      display: flex; align-items: center; justify-content: center;
      z-index: 99999; padding: 1.5rem;
    }}
    .lock-box {{
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(24px);
      border: 1px solid rgba(255, 153, 0, 0.35);
      border-radius: 20px;
      padding: 2.75rem 2.25rem;
      max-width: 460px; width: 100%;
      text-align: center;
      box-shadow: 0 25px 60px -10px rgba(0, 0, 0, 0.8), 0 0 50px rgba(255, 153, 0, 0.15);
    }}
    .lock-icon-wrap {{
      width: 68px; height: 68px; margin: 0 auto 1.25rem;
      background: linear-gradient(135deg, rgba(255, 153, 0, 0.25), rgba(56, 189, 248, 0.2));
      border: 1px solid var(--amz-orange);
      border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      color: var(--amz-orange);
    }}
    .lock-title {{
      font-size: 1.45rem; font-weight: 700; color: #fff;
      margin-bottom: 0.5rem; letter-spacing: -0.02em;
    }}
    .lock-desc {{
      color: var(--text-muted); font-size: 0.88rem; line-height: 1.6;
      margin-bottom: 1.75rem;
    }}
    .lock-desc strong {{
      color: var(--amz-orange); font-weight: 700;
    }}
    .input-wrap {{
      position: relative; margin-bottom: 1.25rem;
    }}
    .lock-input {{
      width: 100%;
      background: rgba(7, 13, 24, 0.9);
      border: 1.5px solid var(--border);
      padding: 0.95rem 1.2rem;
      border-radius: 12px;
      color: #fff;
      font-family: var(--font-sans);
      font-size: 0.95rem;
      outline: none;
      text-align: center;
      letter-spacing: 0.12em;
      transition: all 0.2s;
    }}
    .lock-input:focus {{
      border-color: var(--amz-orange);
      box-shadow: 0 0 0 3px rgba(255, 153, 0, 0.25);
    }}
    .btn-unlock {{
      width: 100%;
      background: linear-gradient(135deg, #ff9900 0%, #ea580c 100%);
      color: #0b1120;
      border: none;
      padding: 0.95rem;
      border-radius: 12px;
      font-size: 0.95rem;
      font-weight: 700;
      cursor: pointer;
      display: flex; align-items: center; justify-content: center; gap: 8px;
      transition: all 0.2s;
    }}
    .btn-unlock:hover {{
      transform: translateY(-1px);
      box-shadow: 0 10px 25px -5px rgba(255, 153, 0, 0.45);
    }}
    .lock-error {{
      color: var(--amz-rose); font-size: 0.82rem; margin-top: 0.75rem;
      display: none; font-weight: 600;
    }}
    .lock-footer {{
      margin-top: 1.75rem; font-size: 0.76rem; color: var(--text-dim);
      display: flex; align-items: center; justify-content: center; gap: 6px;
    }}

    /* APP CONTENT (HIDDEN UNTIL UNLOCKED) */
    #appContent {{
      display: none; opacity: 0; transition: opacity 0.4s ease;
    }}

    /* HEADER & HERO */
    .hero-header {{
      background: linear-gradient(180deg, rgba(255, 153, 0, 0.08) 0%, rgba(15, 23, 42, 0.95) 100%), #070d18;
      border-bottom: 1px solid var(--border);
      padding: 2.5rem 1.5rem 2rem;
      position: sticky; top: 0; z-index: 100;
      backdrop-filter: blur(16px);
    }}
    .hero-container {{
      max-width: 1300px; margin: 0 auto;
      display: flex; flex-direction: column; gap: 1.25rem;
    }}
    .hero-top {{
      display: flex; justify-content: space-between; align-items: flex-start;
      flex-wrap: wrap; gap: 1rem;
    }}
    .brand-tag {{
      display: inline-flex; align-items: center; gap: 8px;
      background: rgba(255, 153, 0, 0.15);
      border: 1px solid rgba(255, 153, 0, 0.4);
      color: var(--amz-orange);
      padding: 6px 14px; border-radius: 999px;
      font-size: 0.8rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;
    }}
    .hero-title {{
      font-size: 2.1rem; font-weight: 800; color: #fff;
      letter-spacing: -0.03em; line-height: 1.2; margin-top: 0.5rem;
    }}
    .hero-title span {{ color: var(--amz-orange); }}
    .hero-subtitle {{
      color: var(--text-muted); font-size: 0.95rem; max-width: 820px; line-height: 1.5; margin-top: 0.35rem;
    }}
    .candidate-pill {{
      background: #111d33; border: 1px solid var(--border);
      padding: 10px 18px; border-radius: 12px;
      display: flex; flex-direction: column; gap: 4px;
      min-width: 260px;
    }}
    .cand-name {{ font-weight: 700; color: #fff; font-size: 0.95rem; }}
    .cand-meta {{ font-size: 0.8rem; color: var(--amz-blue); }}
    .btn-relock {{
      align-self: flex-start; margin-top: 6px;
      background: rgba(255, 255, 255, 0.06); border: 1px solid var(--border);
      color: var(--text-dim); padding: 3px 8px; border-radius: 6px; font-size: 0.72rem;
      cursor: pointer; transition: all 0.2s;
    }}
    .btn-relock:hover {{ color: var(--amz-rose); border-color: var(--amz-rose); }}

    /* PROGRESS BAR */
    .progress-bar-wrap {{
      background: #101c30; border-radius: 8px; height: 8px;
      overflow: hidden; border: 1px solid var(--border);
      position: relative;
    }}
    .progress-fill {{
      height: 100%; width: 0%;
      background: linear-gradient(90deg, var(--amz-orange) 0%, var(--amz-gold) 100%);
      transition: width 0.3s ease;
    }}
    .stats-row {{
      display: flex; justify-content: space-between; align-items: center;
      font-size: 0.82rem; color: var(--text-muted);
    }}

    /* CONTROLS ROW */
    .controls-row {{
      display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; justify-content: space-between;
      margin-top: 0.5rem;
    }}
    .tab-group {{
      display: flex; background: #0c1626; border: 1px solid var(--border); border-radius: 10px; padding: 3px; gap: 4px;
    }}
    .tab-btn {{
      background: transparent; border: none; color: var(--text-muted);
      padding: 8px 18px; font-weight: 600; font-size: 0.88rem; border-radius: 7px;
      cursor: pointer; transition: all 0.2s ease;
    }}
    .tab-btn.active {{
      background: var(--amz-orange); color: #000; font-weight: 700;
    }}
    .search-box-wrap {{
      flex: 1; max-width: 480px; position: relative;
    }}
    .search-input {{
      width: 100%; background: #0f1c30; border: 1px solid var(--border);
      border-radius: 10px; padding: 10px 14px 10px 38px;
      color: #fff; font-family: var(--font-sans); font-size: 0.9rem;
      outline: none; transition: border-color 0.2s;
    }}
    .search-input:focus {{ border-color: var(--amz-orange); }}
    .search-icon {{
      position: absolute; left: 12px; top: 50%; transform: translateY(-50%);
      color: var(--text-dim); pointer-events: none;
    }}

    /* CATEGORY PILLS */
    .filter-pills {{
      display: flex; flex-wrap: wrap; gap: 8px; margin-top: 0.75rem;
    }}
    .cat-pill {{
      background: #0f1c30; border: 1px solid var(--border);
      color: var(--text-muted); padding: 5px 12px; border-radius: 999px;
      font-size: 0.78rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
    }}
    .cat-pill:hover {{ border-color: var(--amz-blue); color: #fff; }}
    .cat-pill.active {{
      background: rgba(56, 189, 248, 0.2); border-color: var(--amz-blue); color: var(--amz-blue);
    }}

    /* MAIN CONTAINER */
    .main-content {{
      max-width: 1300px; margin: 1.5rem auto 4rem; padding: 0 1.5rem;
    }}
    .action-bar {{
      display: flex; justify-content: space-between; align-items: center;
      margin-bottom: 1.5rem; color: var(--text-muted); font-size: 0.85rem;
    }}
    .expand-btn {{
      background: #111d33; border: 1px solid var(--border); color: var(--text-main);
      padding: 6px 14px; border-radius: 8px; font-size: 0.8rem; font-weight: 600;
      cursor: pointer; transition: background 0.2s;
    }}
    .expand-btn:hover {{ background: #1a2a46; }}

    /* QUESTION CARD */
    .q-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      margin-bottom: 1.25rem;
      transition: all 0.25s ease;
      overflow: hidden;
    }}
    .q-card:hover {{
      border-color: rgba(255, 153, 0, 0.4);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }}
    .q-card.completed {{
      opacity: 0.7; border-color: rgba(52, 211, 153, 0.4);
    }}
    .q-header {{
      padding: 1.2rem 1.4rem;
      cursor: pointer;
      display: flex; align-items: flex-start; justify-content: space-between;
      gap: 1rem; user-select: none;
    }}
    .q-title-wrap {{
      display: flex; align-items: flex-start; gap: 12px; flex: 1;
    }}
    .q-checkbox {{
      margin-top: 4px; width: 18px; height: 18px; accent-color: var(--amz-green); cursor: pointer;
    }}
    .q-num {{
      font-family: var(--font-mono); font-size: 0.82rem; font-weight: 700;
      color: var(--amz-orange); background: rgba(255, 153, 0, 0.12);
      padding: 3px 8px; border-radius: 6px; white-space: nowrap; margin-top: 1px;
    }}
    .q-title {{
      font-size: 1.05rem; font-weight: 700; color: #fff; line-height: 1.35;
    }}
    .q-meta {{
      display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; align-items: center;
    }}
    .q-tag {{
      font-size: 0.72rem; padding: 2px 8px; border-radius: 6px; font-weight: 600;
      background: #0d1626; color: var(--text-muted); border: 1px solid var(--border);
    }}
    .q-toggle-icon {{
      font-size: 1.1rem; color: var(--text-dim); transition: transform 0.25s ease;
      padding: 4px;
    }}
    .q-card.open .q-toggle-icon {{ transform: rotate(180deg); color: var(--amz-orange); }}

    /* QUESTION BODY */
    .q-body {{
      display: none;
      padding: 0 1.5rem 1.5rem;
      border-top: 1px solid var(--border);
      background: rgba(11, 18, 32, 0.6);
    }}
    .q-card.open .q-body {{ display: block; }}

    .section-block {{
      margin-top: 1.4rem;
    }}
    .sec-title {{
      display: flex; align-items: center; gap: 8px;
      font-size: 0.88rem; font-weight: 700; text-transform: uppercase;
      letter-spacing: 0.04em; margin-bottom: 0.65rem;
    }}
    .badge {{
      padding: 3px 8px; border-radius: 5px; font-size: 0.72rem; font-weight: 700;
    }}
    .badge-amz {{ background: rgba(255, 153, 0, 0.2); color: var(--amz-orange); }}
    .badge-blue {{ background: rgba(56, 189, 248, 0.2); color: var(--amz-blue); }}
    .badge-cyan {{ background: rgba(6, 182, 212, 0.2); color: var(--amz-cyan); }}
    .badge-purple {{ background: rgba(192, 132, 252, 0.2); color: var(--amz-purple); }}
    .badge-amber {{ background: rgba(251, 191, 36, 0.2); color: var(--amz-gold); }}
    .badge-green {{ background: rgba(52, 211, 153, 0.2); color: var(--amz-green); }}
    .badge-rose {{ background: rgba(251, 113, 133, 0.2); color: var(--amz-rose); }}

    /* CONVERSATIONAL PARAGRAPHS - ZERO BULLETS */
    .conv-p {{
      color: #cbd5e1; font-size: 0.95rem; line-height: 1.7;
      margin-bottom: 0.85rem;
      text-align: justify;
    }}
    .conv-p:last-child {{ margin-bottom: 0; }}

    .body-p {{
      color: #cbd5e1; font-size: 0.95rem; line-height: 1.65;
    }}

    /* CODE BOX */
    .code-header {{
      display: flex; justify-content: space-between; align-items: center;
      background: #090f1d; padding: 6px 14px;
      border-radius: 10px 10px 0 0; border: 1px solid var(--border);
      border-bottom: none; font-size: 0.78rem; font-family: var(--font-mono); color: var(--text-dim);
    }}
    .btn-copy-code {{
      background: #17243c; border: 1px solid var(--border); color: #fff;
      padding: 3px 8px; border-radius: 5px; font-size: 0.72rem; cursor: pointer;
    }}
    .btn-copy-code:hover {{ background: var(--amz-orange); color: #000; }}
    .code-box {{
      background: #090f1d; border: 1px solid var(--border);
      border-radius: 0 0 10px 10px; padding: 1rem;
      overflow-x: auto; font-family: var(--font-mono); font-size: 0.86rem;
      color: #e2e8f0; line-height: 1.5;
    }}
    .complexity-box {{
      background: rgba(52, 211, 153, 0.08); border-left: 3px solid var(--amz-green);
      padding: 10px 14px; border-radius: 0 8px 8px 0; color: #cbd5e1; font-size: 0.9rem;
    }}

    /* TOAST */
    .toast {{
      position: fixed; bottom: 24px; right: 24px;
      background: var(--amz-green); color: #052e16; font-weight: 700;
      padding: 10px 18px; border-radius: 10px; font-size: 0.88rem;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5); z-index: 1000;
      display: none; animation: fadeIn 0.2s ease;
    }}
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  </style>
</head>
<body>

  <!-- LOCK SCREEN OVERLAY -->
  <div id="lockScreen">
    <div class="lock-box">
      <div class="lock-icon-wrap">
        <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="11" width="18" height="11" rx="2.5" ry="2.5"></rect>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          <circle cx="12" cy="16" r="1.5" fill="currentColor"></circle>
          <line x1="12" y1="17.5" x2="12" y2="19.5" stroke="currentColor" stroke-width="2"></line>
        </svg>
      </div>
      <h2 class="lock-title">Protected Guide</h2>
      <p class="lock-desc">
        This material for <strong>Ashutosh Rudraksh</strong> is password-protected.<br>
        Enter your access key to continue.
      </p>
      <div class="input-wrap">
        <input type="password" id="passInput" class="lock-input" placeholder="Enter access password..." onkeydown="if(event.key==='Enter') unlockApp()" autofocus>
      </div>
      <button class="btn-unlock" onclick="unlockApp()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        Unlock Preparation Guide
      </button>
      <div id="lockError" class="lock-error">Incorrect password. Please try again.</div>
      <div class="lock-footer">
        <span>🔒 Protected candidate preparation suite · PrepSuite</span>
      </div>
    </div>
  </div>

  <!-- APPLICATION CONTENT -->
  <div id="appContent">
    <header class="hero-header">
      <div class="hero-container">
        <div class="hero-top">
          <div>
            <div class="brand-tag">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
              Amazon Advertising in Live Events · Technical Master Suite
            </div>
            <h1 class="hero-title">AI Engineer Technical Interview <span>Master Guide</span></h1>
            <p class="hero-subtitle">
              Curated preparation suite for <strong>Ashutosh Rudraksh</strong>. Tailored directly to <strong>Amazon Advertising in Live Events</strong> (Thursday Night Football, NBA, NASCAR, Prime Video). Covers Top 30 High-Frequency Python DSA questions and 30 Conversational System Design questions with zero bullet points.
            </p>
          </div>
          <div class="candidate-pill">
            <div class="cand-name">Ashutosh Rudraksh</div>
            <div class="cand-meta">4 Yrs Exp: Uber · Meta Reality Labs · Tekainos · Dell</div>
            <div class="cand-meta">M.S. CS Ohio State University · LLMs & AI Systems</div>
            <button class="btn-relock" onclick="relockApp()">🔒 Lock Guide</button>
          </div>
        </div>

        <!-- PROGRESS TRACKER -->
        <div class="progress-bar-wrap">
          <div id="topProgress" class="progress-fill"></div>
        </div>
        <div class="stats-row">
          <span id="readCounter">0 / 60 Prepared</span>
          <span>Target: 100% Broadcast Ready</span>
        </div>

        <!-- CONTROLS & SEARCH -->
        <div class="controls-row">
          <div class="tab-group">
            <button class="tab-btn active" onclick="switchTab('all', this)">All (60)</button>
            <button class="tab-btn" onclick="switchTab('dsa', this)">Top 30 DSA (Python)</button>
            <button class="tab-btn" onclick="switchTab('sysde', this)">Top 30 System Design</button>
          </div>
          <div class="search-box-wrap">
            <span class="search-icon">🔍</span>
            <input type="text" id="globalSearch" class="search-input" placeholder="Search algorithms, SSAI, SCTE-35, MCP, Kafka, Redis..." oninput="handleSearch()">
          </div>
        </div>

        <!-- CATEGORY PILLS -->
        <div class="filter-pills">
          <button class="cat-pill active" onclick="filterCategory('all', this)">All Categories</button>
          <button class="cat-pill" onclick="filterCategory('DSA (Algorithms & Data Structures)', this)">Algorithms & Data Structures</button>
          <button class="cat-pill" onclick="filterCategory('Live Video Streaming & Ad Insertion', this)">Live Video & SSAI</button>
          <button class="cat-pill" onclick="filterCategory('Real-Time Bidding & Ad Auctions', this)">Auctions & RTB</button>
          <button class="cat-pill" onclick="filterCategory('AI Agents & Autonomous Operations', this)">AI Agents & MCP</button>
          <button class="cat-pill" onclick="filterCategory('Multimodal AI & Computer Vision', this)">Multimodal & Computer Vision</button>
          <button class="cat-pill" onclick="filterCategory('Telemetry & Observability', this)">Telemetry & Stream ETL</button>
        </div>
      </div>
    </header>

    <!-- MAIN LISTING -->
    <main class="main-content">
      <div class="action-bar">
        <span id="visibleCount">Showing 60 of 60 items</span>
        <div style="display:flex; gap: 8px;">
          <button class="expand-btn" onclick="expandAll()">Expand All</button>
          <button class="expand-btn" onclick="collapseAll()">Collapse All</button>
        </div>
      </div>

      <div id="cardsContainer">
        <!-- Cards rendered via JS -->
      </div>
    </main>
  </div>

  <div id="toast" class="toast">✓ Copied to clipboard!</div>

  <script>
    const itemsData = {items_json};
    const MASTER_PASS = "Ashutosh";
    const AUTH_KEY = "ashutosh_live_events_unlocked";

    function checkAuth() {{
      const isAuth = sessionStorage.getItem(AUTH_KEY) === "true";
      if (isAuth) {{
        document.getElementById("lockScreen").style.display = "none";
        const app = document.getElementById("appContent");
        app.style.display = "block";
        setTimeout(() => app.style.opacity = "1", 30);
      }} else {{
        document.getElementById("lockScreen").style.display = "flex";
        document.getElementById("appContent").style.display = "none";
        setTimeout(() => {{
          const p = document.getElementById("passInput");
          if (p) p.focus();
        }}, 100);
      }}
    }}

    function unlockApp() {{
      const input = document.getElementById("passInput");
      const err = document.getElementById("lockError");
      const entered = input.value.trim();

      if (entered.toLowerCase() === MASTER_PASS.toLowerCase()) {{
        sessionStorage.setItem(AUTH_KEY, "true");
        err.style.display = "none";
        document.getElementById("lockScreen").style.display = "none";
        const app = document.getElementById("appContent");
        app.style.display = "block";
        setTimeout(() => app.style.opacity = "1", 30);
      }} else {{
        err.style.display = "block";
        input.value = "";
        input.focus();
      }}
    }}

    function relockApp() {{
      sessionStorage.removeItem(AUTH_KEY);
      location.reload();
    }}

    let activeTab = 'all';
    let activeCat = 'all';

    function renderCards() {{
      const container = document.getElementById("cardsContainer");
      container.innerHTML = "";

      itemsData.forEach(item => {{
        const isDSA = item.type === 'dsa';
        const numLabel = isDSA ? `DSA #${{item.num}}` : `SYSDE #${{item.sys_id}}`;
        const badgeColor = isDSA ? 'var(--amz-orange)' : 'var(--amz-blue)';

        const card = document.createElement("div");
        card.className = "q-card";
        card.id = `card-${{item.num}}`;
        card.setAttribute("data-num", item.num);
        card.setAttribute("data-type", item.type);
        card.setAttribute("data-cat", item.category);
        card.setAttribute("data-search", item.search_text);

        card.innerHTML = `
          <div class="q-header" onclick="toggleCard(${{item.num}})">
            <div class="q-title-wrap">
              <input type="checkbox" class="q-checkbox" onclick="event.stopPropagation(); toggleComplete(${{item.num}})" title="Mark as Mastered">
              <span class="q-num" style="color: ${{badgeColor}}">${{numLabel}}</span>
              <div>
                <div class="q-title">${{item.title}}</div>
                <div class="q-meta">
                  <span class="q-tag">${{item.subCategory}}</span>
                  <span class="q-tag" style="color: var(--amz-gold);">${{item.difficulty}}</span>
                </div>
              </div>
            </div>
            <div class="q-toggle-icon">▼</div>
          </div>
          <div class="q-body">
            ${{item.html_content}}
          </div>
        `;

        container.appendChild(card);
      }});

      updateProgress();
    }}

    function toggleCard(num) {{
      const card = document.getElementById(`card-${{num}}`);
      card.classList.toggle("open");
    }}

    function expandAll() {{
      document.querySelectorAll(".q-card").forEach(c => {{
        if (c.style.display !== "none") c.classList.add("open");
      }});
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
      document.getElementById("readCounter").innerText = `${{checked}} / ${{total}} Mastered`;
    }}

    function switchTab(tab, btn) {{
      activeTab = tab;
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      if (btn) btn.classList.add("active");
      applyFilters();
    }}

    function filterCategory(cat, btn) {{
      activeCat = cat;
      document.querySelectorAll(".cat-pill").forEach(p => p.classList.remove("active"));
      if (btn) btn.classList.add("active");
      applyFilters();
    }}

    function handleSearch() {{
      applyFilters();
    }}

    function applyFilters() {{
      const query = document.getElementById("globalSearch").value.toLowerCase().trim();
      let visible = 0;

      document.querySelectorAll(".q-card").forEach(card => {{
        const cType = card.getAttribute("data-type");
        const cCat = card.getAttribute("data-cat");
        const cSearch = card.getAttribute("data-search");

        const matchesTab = (activeTab === 'all' || cType === activeTab);
        const matchesCat = (activeCat === 'all' || cCat === activeCat);
        const matchesQuery = (!query || cSearch.includes(query));

        if (matchesTab && matchesCat && matchesQuery) {{
          card.style.display = "block";
          visible++;
        }} else {{
          card.style.display = "none";
        }}
      }});

      document.getElementById("visibleCount").innerText = `Showing ${{visible}} of ${{itemsData.length}} items`;
    }}

    function copyCode(btn) {{
      const codeBlock = btn.closest(".section-block").querySelector("code");
      if (!codeBlock) return;
      navigator.clipboard.writeText(codeBlock.innerText).then(() => {{
        const orig = btn.innerText;
        btn.innerText = "✓ Copied!";
        setTimeout(() => btn.innerText = orig, 1800);
      }});
    }}

    window.addEventListener("DOMContentLoaded", () => {{
      checkAuth();
      renderCards();
    }});
  </script>
</body>
</html>
"""

# Write standalone app
with open("amazon_live_events_ai_ashutosh_prep.html", "w", encoding="utf-8") as f:
    f.write(html_template)
print("Wrote amazon_live_events_ai_ashutosh_prep.html successfully.")

# Write to public/ directory for production serving
with open("public/amazon_live_events_ai_ashutosh_prep.html", "w", encoding="utf-8") as f:
    f.write(html_template)
print("Wrote public/amazon_live_events_ai_ashutosh_prep.html successfully.")
