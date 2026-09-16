# -*- coding: utf-8 -*-
"""
Janaki Ashok Kumar - QA Automation Engineer 14-Day Preparation Suite Generator
Generates:
1. janaki_qa_automation_14day_prep.md
2. content/janaki-qa-automation-14day-prep.mdx
3. janaki_qa_automation_14day_prep.html
Passcode: "Janaki"
"""

import json
import os
import re
from janaki_data_part1 import days_part1
from janaki_data_part2 import days_part2
from janaki_data_part3 import days_part3

all_days = days_part1 + days_part2 + days_part3
print(f"Total days loaded: {len(all_days)}")

# Validate word counts for master QA answers
print("\n--- Validating Master Q&A Word Counts (Target >= 300 words) ---")
for d in all_days:
    ans = d["master_qa"]["answer"]
    words = len(re.findall(r'\b\w+\b', ans))
    day_num = d["day"]
    print(f"Day {day_num}: {words} words in Master Q&A")
    if words < 300:
        print(f"WARNING: Day {day_num} master QA answer is under 300 words ({words} words)!")

# =============================================================================
# 1. GENERATE MASTER MARKDOWN FILE (janaki_qa_automation_14day_prep.md)
# =============================================================================
md_lines = []
md_lines.append("# Janaki Ashok Kumar — QA Automation Engineer 14-Day Master Preparation Blueprint")
md_lines.append("## Daily 5-Hour Intensive Study Roadmap (Day 0 to Day 14 · Total 75 Dedicated Study Hours)")
md_lines.append("")
md_lines.append("**Candidate:** Janaki Ashok Kumar  ")
md_lines.append("**Target Role:** Senior QA Automation Engineer / Lead SDET  ")
md_lines.append("**Experience:** 7+ Years Enterprise QA Automation (Banking, Insurance, Healthcare, Payroll)  ")
md_lines.append("**Location & Status:** Dallas, TX · US Citizen  ")
md_lines.append("**Current & Past Organizations:** PNC Bank USA, Liberty Mutual USA, Molina Healthcare USA  ")
md_lines.append("**Core Tech Stack:** **Java 17/21**, **Selenium WebDriver 4**, **Playwright**, **REST Assured**, **Cucumber BDD**, **TestNG**, **Apache POI**, **SQL / Oracle / PostgreSQL**, **Docker**, **Jenkins**, **Azure DevOps**, **Kafka**, **Grafana**, **Jira / Xray**  ")
md_lines.append("**Security Access Passcode:** `Janaki`  ")
md_lines.append("")
md_lines.append("---")
md_lines.append("")
md_lines.append("## 14-DAY CURRICULUM ARCHITECTURE (75 HOURS TOTAL)")
md_lines.append("")
md_lines.append("| Day | Core Topic & Focus Area | Target Domain & Enterprise Tech Stack | Daily Commitment |")
md_lines.append("|---|---|---|---|")
for d in all_days:
    md_lines.append(f"| **Day {d['day']}** | {d['title']} | {d['domain_focus']} | 5 Hours Dedicated |")
md_lines.append("")
md_lines.append("---")
md_lines.append("")

for d in all_days:
    day_num = d["day"]
    md_lines.append(f"# {d['title']}")
    md_lines.append(f"**Theme:** {d['theme']}  ")
    md_lines.append(f"**Domain Focus:** {d['domain_focus']}  ")
    md_lines.append("")
    md_lines.append("### 5-Hour Daily Structured Breakdown")
    md_lines.append("")
    for h in d["hours"]:
        md_lines.append(f"#### {h['label']}: {h['topic']}")
        md_lines.append(h["content"])
        md_lines.append("")

    md_lines.append("---")
    md_lines.append(f"### Master Technical Interview Deep Dive (Day {day_num})")
    md_lines.append(f"**Question:** {d['master_qa']['question']}")
    md_lines.append("")
    md_lines.append(d["master_qa"]["answer"])
    md_lines.append("")
    md_lines.append("---")
    md_lines.append(f"### Resume STAR Narrative & Behavioral Alignment (Day {day_num})")
    md_lines.append(f"**Topic:** {d['hours'][4]['topic']}")
    md_lines.append("")
    md_lines.append(d['hours'][4]['content'])
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

with open("janaki_qa_automation_14day_prep.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))
print("Successfully generated janaki_qa_automation_14day_prep.md")


# =============================================================================
# 2. GENERATE NEXT DATA MDX FILE (content/janaki-qa-automation-14day-prep.mdx)
# =============================================================================
mdx_lines = []
mdx_lines.append("---")
mdx_lines.append("title: Janaki Ashok Kumar — QA Automation Engineer 14-Day Master Roadmap")
mdx_lines.append("description: Intensive Day 0 to Day 14 (5 hours/day) interview preparation guide for Senior QA Automation Engineer / SDET roles — Java, Selenium, Playwright, REST Assured, Cucumber, TestNG, Docker, Jenkins.")
mdx_lines.append("---")
mdx_lines.append("")
mdx_lines.append('<PasswordGate password="Janaki">')
mdx_lines.append("")
mdx_lines.append("# Janaki Ashok Kumar — QA Automation Engineer 14-Day Master Preparation Blueprint")
mdx_lines.append("## Daily 5-Hour Intensive Study Roadmap (Day 0 to Day 14 · Total 75 Dedicated Study Hours)")
mdx_lines.append("")
mdx_lines.append("**Candidate:** Janaki Ashok Kumar  ")
mdx_lines.append("**Target Role:** Senior QA Automation Engineer / Lead SDET  ")
mdx_lines.append("**Experience:** 7+ Years Enterprise QA Automation (Banking, Insurance, Healthcare, Payroll)  ")
mdx_lines.append("**Location & Status:** Dallas, TX · US Citizen  ")
mdx_lines.append("**Current & Past Organizations:** PNC Bank USA, Liberty Mutual USA, Molina Healthcare USA  ")
mdx_lines.append("**Core Tech Stack:** **Java 17/21**, **Selenium WebDriver 4**, **Playwright**, **REST Assured**, **Cucumber BDD**, **TestNG**, **Apache POI**, **SQL / Oracle / PostgreSQL**, **Docker**, **Jenkins**, **Azure DevOps**, **Kafka**, **Grafana**, **Jira / Xray**  ")
mdx_lines.append("**Security Access Passcode:** `Janaki`  ")
mdx_lines.append("")
mdx_lines.append("---")
mdx_lines.append("")
mdx_lines.append("## 14-DAY CURRICULUM ARCHITECTURE (75 HOURS TOTAL)")
mdx_lines.append("")
mdx_lines.append("| Day | Core Topic & Focus Area | Target Domain & Enterprise Tech Stack | Daily Commitment |")
mdx_lines.append("|---|---|---|---|")
for d in all_days:
    mdx_lines.append(f"| **Day {d['day']}** | {d['title']} | {d['domain_focus']} | 5 Hours Dedicated |")
mdx_lines.append("")
mdx_lines.append("---")
mdx_lines.append("")

for d in all_days:
    day_num = d["day"]
    mdx_lines.append(f"# {d['title']}")
    mdx_lines.append(f"**Theme:** {d['theme']}  ")
    mdx_lines.append(f"**Domain Focus:** {d['domain_focus']}  ")
    mdx_lines.append("")
    mdx_lines.append("### 5-Hour Daily Structured Breakdown")
    mdx_lines.append("")
    for h in d["hours"]:
        mdx_lines.append(f"#### {h['label']}: {h['topic']}")
        # Ensure MDX does not contain raw unescaped brackets or invalid characters in text outside code blocks
        content = h["content"]
        mdx_lines.append(content)
        mdx_lines.append("")

    mdx_lines.append("---")
    mdx_lines.append(f"### Master Technical Interview Deep Dive (Day {day_num})")
    mdx_lines.append(f"**Question:** {d['master_qa']['question']}")
    mdx_lines.append("")
    mdx_lines.append(d["master_qa"]["answer"])
    mdx_lines.append("")
    mdx_lines.append("---")
    mdx_lines.append(f"### Resume STAR Narrative & Behavioral Alignment (Day {day_num})")
    mdx_lines.append(f"**Topic:** {d['hours'][4]['topic']}")
    mdx_lines.append("")
    mdx_lines.append(d['hours'][4]['content'])
    mdx_lines.append("")
    mdx_lines.append("---")
    mdx_lines.append("")

mdx_lines.append("</PasswordGate>")

# Clean up any potential MDX formatting clashes outside code fences:
def clean_mdx_content(raw_text):
    # Split by fenced code blocks to only clean outside code
    parts = re.split(r'(```[\s\S]*?```)', raw_text)
    cleaned_parts = []
    for p in parts:
        if p.startswith('```'):
            cleaned_parts.append(p)
        else:
            # Escape raw { and } in text to avoid Acorn JS expression errors
            clean_p = p.replace('{', '&#123;').replace('}', '&#125;')
            # Replace standalone < or > that might be parsed as JSX tags
            clean_p = re.sub(r'<(?!/?PasswordGate|/?span|/?div|/?p|/?strong|/?em|/?a|/?b|/?br|/?pre|/?code)', '&lt;', clean_p)
            cleaned_parts.append(clean_p)
    return "".join(cleaned_parts)

final_mdx = clean_mdx_content("\n".join(mdx_lines))

with open("content/janaki-qa-automation-14day-prep.mdx", "w", encoding="utf-8") as f:
    f.write(final_mdx)
print("Successfully generated content/janaki-qa-automation-14day-prep.mdx")


# =============================================================================
# 3. GENERATE STANDALONE INTERACTIVE HTML (janaki_qa_automation_14day_prep.html)
# =============================================================================
json_days_data = json.dumps(all_days)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Janaki Ashok Kumar — QA Automation Engineer 14-Day Master Roadmap</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-base: #060913;
      --bg-surface: #0d1424;
      --bg-card: #131c31;
      --bg-card-hover: #1a2744;
      --border: #1e2e4f;
      --border-accent: #0284c7;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --brand-blue: #0284c7;
      --brand-cyan: #06b6d4;
      --brand-emerald: #10b981;
      --brand-purple: #a855f7;
      --brand-amber: #f59e0b;
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
      background: radial-gradient(circle at center, #131f38 0%, #04060c 100%);
      display: flex; align-items: center; justify-content: center;
      z-index: 99999; padding: 1.5rem;
    }}
    .lock-box {{
      background: rgba(13, 20, 36, 0.97);
      backdrop-filter: blur(24px);
      border: 1px solid rgba(2, 132, 199, 0.4);
      border-radius: 24px;
      padding: 2.75rem 2.5rem;
      max-width: 500px;
      width: 100%;
      text-align: center;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.9), 0 0 50px rgba(2, 132, 199, 0.25);
    }}
    .lock-logo-mark {{
      display: inline-flex; align-items: center; justify-content: center;
      margin-bottom: 1.5rem; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.03em;
    }}
    .lock-txt-1 {{ color: #ffffff; }}
    .lock-txt-2 {{ color: #0284c7; }}
    .lock-badge-pill {{
      background: linear-gradient(135deg, rgba(2, 132, 199, 0.25), rgba(16, 185, 129, 0.25));
      border: 1px solid rgba(2, 132, 199, 0.5);
      padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; color: #38bdf8;
      font-family: var(--font-mono); margin-left: 8px; font-weight: 700;
    }}
    .lock-box h2 {{ font-size: 1.45rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.02em; }}
    .lock-box p {{ color: var(--text-muted); font-size: 0.88rem; margin-bottom: 1.75rem; }}
    .input-group {{ position: relative; margin-bottom: 1.25rem; }}
    .input-group input {{
      width: 100%;
      background: rgba(6, 9, 19, 0.95);
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
      border-color: var(--brand-blue);
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.25);
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
      display: flex; align-items: center; justify-content: center; gap: 8px;
    }}
    .unlock-btn:hover {{
      background: linear-gradient(135deg, #0369a1, #075985);
      transform: translateY(-1px);
      box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.4);
    }}
    .lock-err {{
      color: #f87171; font-size: 0.82rem; margin-top: 0.85rem; display: none; font-weight: 600;
    }}

    /* MAIN APP CONTENT */
    #appContent {{ display: none; opacity: 0; transition: opacity 0.3s ease; }}

    /* HEADER */
    .top-header {{
      background: linear-gradient(180deg, #0d1424 0%, #060913 100%);
      border-bottom: 1px solid var(--border);
      padding: 2.25rem 2rem 1.75rem 2rem;
      position: relative;
      overflow: hidden;
    }}
    .top-header::after {{
      content: ''; position: absolute; top: 0; left: 15%; width: 550px; height: 180px;
      background: radial-gradient(circle, rgba(2, 132, 199, 0.12) 0%, transparent 70%);
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
    .us-citizen-badge {{
      background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4);
      color: #34d399; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 9999px;
      display: inline-flex; align-items: center; gap: 6px;
    }}
    .role-badge {{
      background: rgba(2, 132, 199, 0.15); border: 1px solid rgba(2, 132, 199, 0.4);
      color: #38bdf8; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 9999px;
      font-family: var(--font-mono);
    }}
    .profile-subtitle {{
      color: var(--text-muted); font-size: 0.95rem; margin-bottom: 1rem; line-height: 1.5;
    }}
    .tags-container {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 0.75rem; }}
    .skill-tag {{
      background: rgba(19, 28, 49, 0.85); border: 1px solid var(--border);
      color: #cbd5e1; font-size: 0.78rem; padding: 3px 10px; border-radius: 6px;
      font-family: var(--font-mono); font-weight: 500;
    }}
    .skill-tag.accent {{ border-color: rgba(2, 132, 199, 0.4); color: #38bdf8; }}

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
      height: 100%; width: 0%; background: linear-gradient(90deg, #0284c7, #10b981);
      transition: width 0.3s ease; border-radius: 9999px;
    }}

    /* NAVIGATION & FILTERS */
    .sticky-nav-bar {{
      position: sticky; top: 0; z-index: 50;
      background: rgba(6, 9, 19, 0.92);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      padding: 0.85rem 2rem;
    }}
    .nav-inner {{
      max-width: 1300px; margin: 0 auto;
      display: flex; justify-content: space-between; align-items: center;
      gap: 1.25rem; flex-wrap: wrap;
    }}
    .days-pill-carousel {{
      display: flex; gap: 8px; overflow-x: auto; padding-bottom: 4px; scrollbar-width: thin;
      max-width: 780px;
    }}
    .day-pill {{
      background: var(--bg-card); border: 1px solid var(--border);
      color: var(--text-muted); font-size: 0.82rem; font-weight: 600;
      padding: 6px 14px; border-radius: 9999px; cursor: pointer;
      white-space: nowrap; transition: all 0.2s; font-family: var(--font-mono);
    }}
    .day-pill:hover {{ border-color: var(--brand-blue); color: #fff; }}
    .day-pill.active {{
      background: linear-gradient(135deg, #0284c7, #0369a1);
      border-color: #38bdf8; color: #fff; font-weight: 700;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
    }}

    .search-box-wrapper {{ position: relative; min-width: 240px; flex: 1; max-width: 380px; }}
    .search-box-wrapper input {{
      width: 100%; background: var(--bg-card); border: 1px solid var(--border);
      padding: 7px 14px 7px 34px; border-radius: 9999px; color: #fff;
      font-size: 0.85rem; outline: none; transition: border-color 0.2s;
    }}
    .search-box-wrapper input:focus {{ border-color: var(--brand-blue); }}
    .search-icon {{
      position: absolute; left: 12px; top: 50%; transform: translateY(-50%);
      font-size: 0.85rem; color: var(--text-dim); pointer-events: none;
    }}

    /* MAIN CONTAINER */
    .main-layout {{
      max-width: 1300px; margin: 0 auto; padding: 2rem 2rem 4rem 2rem;
    }}

    /* DAY CONTAINER */
    .day-section {{
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 2rem;
      margin-bottom: 2.5rem;
      box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    }}
    .day-header-top {{
      display: flex; justify-content: space-between; align-items: flex-start;
      border-bottom: 1px solid var(--border); padding-bottom: 1.25rem; margin-bottom: 1.5rem;
      flex-wrap: wrap; gap: 1rem;
    }}
    .day-header-left {{ flex: 1; }}
    .day-badge-super {{
      font-size: 0.8rem; font-weight: 800; text-transform: uppercase;
      color: #38bdf8; font-family: var(--font-mono); letter-spacing: 0.08em; margin-bottom: 4px;
    }}
    .day-title-main {{ font-size: 1.45rem; font-weight: 800; color: #fff; margin-bottom: 6px; }}
    .day-sub-details {{ font-size: 0.9rem; color: var(--text-muted); }}
    .day-domain-tag {{
      background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35);
      color: #34d399; font-size: 0.76rem; padding: 4px 10px; border-radius: 6px;
      font-weight: 600; display: inline-block; margin-top: 6px;
    }}

    /* 5-HOURS GRID */
    .hours-grid {{
      display: grid; grid-template-columns: 1fr; gap: 1.25rem; margin-bottom: 2rem;
    }}
    .hour-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      transition: all 0.2s;
    }}
    .hour-card:hover {{ border-color: rgba(2, 132, 199, 0.4); }}
    .hour-header {{
      background: rgba(10, 16, 28, 0.7);
      padding: 1rem 1.5rem;
      display: flex; justify-content: space-between; align-items: center;
      cursor: pointer; user-select: none;
      border-bottom: 1px solid rgba(255,255,255,0.04);
    }}
    .hour-title-left {{ display: flex; align-items: center; gap: 12px; flex: 1; }}
    .hour-icon-pill {{
      background: rgba(2, 132, 199, 0.15); color: #38bdf8;
      border: 1px solid rgba(2, 132, 199, 0.3);
      padding: 4px 10px; border-radius: 6px; font-size: 0.76rem;
      font-family: var(--font-mono); font-weight: 700; white-space: nowrap;
    }}
    .hour-topic-text {{ font-size: 1rem; font-weight: 700; color: #f1f5f9; }}
    .hour-header-right {{ display: flex; align-items: center; gap: 12px; }}
    .hour-checkbox {{
      width: 18px; height: 18px; cursor: pointer; accent-color: var(--brand-emerald);
    }}
    .hour-toggle-btn {{
      background: none; border: none; color: var(--text-dim);
      font-size: 0.85rem; cursor: pointer; transition: transform 0.2s;
    }}
    .hour-card.open .hour-toggle-btn {{ transform: rotate(180deg); color: #38bdf8; }}
    .hour-body {{
      display: none; padding: 1.5rem; color: #cbd5e1; font-size: 0.92rem; line-height: 1.65;
    }}
    .hour-card.open .hour-body {{ display: block; }}

    /* MASTER QA CARD */
    .master-qa-box {{
      background: linear-gradient(145deg, #0d172e, #111b33);
      border: 1px solid rgba(2, 132, 199, 0.4);
      border-radius: 16px;
      padding: 1.75rem;
      margin-bottom: 1.5rem;
      box-shadow: 0 10px 25px -5px rgba(0,0,0,0.4);
    }}
    .qa-badge-head {{
      display: inline-flex; align-items: center; gap: 6px;
      background: rgba(2, 132, 199, 0.2); border: 1px solid rgba(2, 132, 199, 0.4);
      color: #38bdf8; font-size: 0.75rem; font-weight: 800; font-family: var(--font-mono);
      padding: 4px 10px; border-radius: 6px; text-transform: uppercase; margin-bottom: 0.75rem;
    }}
    .qa-question-title {{
      font-size: 1.25rem; font-weight: 800; color: #fff; margin-bottom: 1.25rem; line-height: 1.4;
    }}
    .qa-answer-text {{
      color: #cbd5e1; font-size: 0.94rem; line-height: 1.75; margin-bottom: 1.25rem;
    }}
    .qa-answer-text strong {{ color: #ffffff; font-weight: 700; }}
    .qa-footer-bar {{
      display: flex; justify-content: space-between; align-items: center;
      border-top: 1px solid rgba(255,255,255,0.06); padding-top: 1rem;
      font-size: 0.82rem; color: var(--text-dim);
    }}
    .copy-btn {{
      background: rgba(2, 132, 199, 0.15); border: 1px solid rgba(2, 132, 199, 0.35);
      color: #38bdf8; font-size: 0.8rem; font-weight: 600; padding: 6px 14px;
      border-radius: 8px; cursor: pointer; transition: all 0.2s;
    }}
    .copy-btn:hover {{ background: rgba(2, 132, 199, 0.3); color: #fff; }}

    /* STAR STORY CARD */
    .star-story-box {{
      background: rgba(16, 185, 129, 0.05);
      border: 1px solid rgba(16, 185, 129, 0.3);
      border-radius: 14px;
      padding: 1.5rem;
    }}
    .star-badge-head {{
      display: inline-flex; align-items: center; gap: 6px;
      background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35);
      color: #34d399; font-size: 0.75rem; font-weight: 800; font-family: var(--font-mono);
      padding: 4px 10px; border-radius: 6px; text-transform: uppercase; margin-bottom: 0.6rem;
    }}
    .star-title {{ font-size: 1.05rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.75rem; }}
    .star-narrative {{ color: #cbd5e1; font-size: 0.92rem; line-height: 1.65; }}
    .star-narrative strong {{ color: #34d399; }}

    /* CODE STYLING */
    pre {{
      background: #060a14 !important;
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
      background: rgba(2, 132, 199, 0.1);
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
      background: #0284c7; color: #fff;
      padding: 12px 20px; border-radius: 10px;
      font-weight: 700; font-size: 0.88rem;
      box-shadow: 0 10px 25px rgba(0,0,0,0.6);
      display: none; z-index: 100000;
    }}

    @media (max-width: 768px) {{
      .header-container {{ flex-direction: column; }}
      .days-pill-carousel {{ max-width: 100%; }}
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
        <span class="lock-txt-1">QA</span><span class="lock-txt-2">PREP</span>
        <span class="lock-badge-pill">14-DAY ROADMAP</span>
      </div>
      <h2>Enterprise Preparation Suite</h2>
      <p>Candidate: Janaki Ashok Kumar · Senior QA Automation Engineer (PNC, Liberty Mutual, Molina Healthcare)</p>
      
      <form onsubmit="handleUnlock(event)">
        <div class="input-group">
          <input type="password" id="passInput" placeholder="Enter Access Passcode" autofocus autocomplete="off" />
        </div>
        <button type="submit" class="unlock-btn">
          <span>Unlock 14-Day Curriculum</span> ➔
        </button>
      </form>
      <div id="lockError" class="lock-err">Invalid Passcode. Hint: Candidate First Name</div>
    </div>
  </div>

  <!-- MAIN APP CONTAINER -->
  <div id="appContent">

    <!-- TOP HEADER -->
    <header class="top-header">
      <div class="header-container">
        <div class="candidate-profile">
          <div class="title-row">
            <h1 class="candidate-name">Janaki Ashok Kumar</h1>
            <span class="us-citizen-badge">🇺🇸 US Citizen</span>
            <span class="role-badge">QA Automation Engineer (7+ Years)</span>
          </div>
          <p class="profile-subtitle">
            Dallas, TX · Janakiashok01@gmail.com · 407-401-4340 · Specialized in Enterprise Banking, Insurance, Healthcare & Payroll Automation Frameworks
          </p>
          <div class="tags-container">
            <span class="skill-tag accent">Java 17</span>
            <span class="skill-tag accent">Selenium WebDriver 4</span>
            <span class="skill-tag accent">Playwright</span>
            <span class="skill-tag accent">REST Assured</span>
            <span class="skill-tag accent">Cucumber BDD</span>
            <span class="skill-tag">TestNG</span>
            <span class="skill-tag">SQL & Oracle</span>
            <span class="skill-tag">Docker & Grid</span>
            <span class="skill-tag">Jenkins CI/CD</span>
            <span class="skill-tag">Azure DevOps</span>
            <span class="skill-tag">Apache Kafka</span>
            <span class="skill-tag">Grafana</span>
          </div>
        </div>

        <div class="header-stats-card">
          <div class="stat-row">
            <span class="stat-label">Study Duration</span>
            <span class="stat-value">15 Days (Day 0–14)</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Daily Allocation</span>
            <span class="stat-value highlight">5.0 Hours Daily</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Total Time Commitment</span>
            <span class="stat-value">75 Hours Total</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Hours Completed</span>
            <span class="stat-value" id="hoursTrackerText">0 / 75 Hours</span>
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
        <div class="days-pill-carousel" id="daysCarousel">
          <!-- Populated by JS -->
        </div>
        <div class="search-box-wrapper">
          <span class="search-icon">🔍</span>
          <input type="text" id="searchInput" placeholder="Search keywords (e.g. ThreadLocal, Playwright, Kafka)..." oninput="handleSearch()" />
        </div>
      </div>
    </nav>

    <!-- MAIN SECTIONS -->
    <main class="main-layout" id="daysContainer">
      <!-- Populated by JS -->
    </main>

  </div>

  <div id="toast">Copied to Clipboard!</div>

  <script>
    const daysData = {json_days_data};
    const PASSCODE = "Janaki";
    const STORAGE_KEY = "auth_janaki_qa_prep";

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
      renderNavPills();
      renderDays();
      updateProgress();
    }}

    function renderNavPills() {{
      const carousel = document.getElementById("daysCarousel");
      carousel.innerHTML = daysData.map((d, idx) => `
        <button class="day-pill ${{idx === 0 ? 'active' : ''}}" onclick="scrollToDay(${{d.day}}, this)">
          Day ${{d.day}}
        </button>
      `).join("");
    }}

    function scrollToDay(dayNum, btn) {{
      document.querySelectorAll(".day-pill").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      const section = document.getElementById(`day-${{dayNum}}`);
      if (section) {{
        section.scrollIntoView({{ behavior: "smooth", block: "start" }});
      }}
    }}

    function renderDays() {{
      const container = document.getElementById("daysContainer");
      container.innerHTML = daysData.map(d => {{
        return `
          <section class="day-section" id="day-${{d.day}}" data-search="${{(d.title + ' ' + d.theme + ' ' + d.domain_focus).toLowerCase()}}">
            <div class="day-header-top">
              <div class="day-header-left">
                <div class="day-badge-super">DAY ${{d.day}} · 5 HOURS ALLOCATION</div>
                <h2 class="day-title-main">${{d.title}}</h2>
                <div class="day-sub-details"><strong>Theme:</strong> ${{d.theme}}</div>
                <div class="day-domain-tag">${{d.domain_focus}}</div>
              </div>
            </div>

            <!-- 5 HOURS BREAKDOWN -->
            <h3 style="font-size: 1.1rem; color: #fff; margin-bottom: 1rem;">⏱️ Daily 5-Hour Modular Breakdown</h3>
            <div class="hours-grid">
              ${{d.hours.map(h => `
                <div class="hour-card open" id="hour-card-${{d.day}}-${{h.hour}}">
                  <div class="hour-header" onclick="toggleHourCard('hour-card-${{d.day}}-${{h.hour}}')">
                    <div class="hour-title-left">
                      <span class="hour-icon-pill">Hour ${{h.hour}}</span>
                      <span class="hour-topic-text">${{h.topic}}</span>
                    </div>
                    <div class="hour-header-right">
                      <input type="checkbox" class="hour-checkbox" 
                             id="chk-${{d.day}}-${{h.hour}}" 
                             onclick="event.stopPropagation(); toggleHourCheck('${{d.day}}-${{h.hour}}')" 
                             title="Mark hour completed" />
                      <button class="hour-toggle-btn">▼</button>
                    </div>
                  </div>
                  <div class="hour-body">
                    ${{formatMarkdownContent(h.content)}}
                  </div>
                </div>
              `).join("")}}
            </div>

            <!-- MASTER TECHNICAL QA -->
            <div class="master-qa-box">
              <div class="qa-badge-head">🎯 Master Technical Interview Question (Day ${{d.day}})</div>
              <h3 class="qa-question-title">${{d.master_qa.question}}</h3>
              <div class="qa-answer-text">
                ${{formatMarkdownContent(d.master_qa.answer)}}
              </div>
              <div class="qa-footer-bar">
                <span>~${{d.master_qa.answer.split(' ').length}} Words · High-Yield Architectural Deep Dive</span>
                <button class="copy-btn" onclick="copyAnswer(${{d.day}}, this)">📋 Copy Answer</button>
              </div>
            </div>

            <!-- RESUME STAR STORY -->
            <div class="star-story-box">
              <div class="star-badge-head">🤝 Resume STAR Narrative & Behavioral Defense (Day ${{d.day}})</div>
              <h4 class="star-title">${{d.hours[4].topic}}</h4>
              <div class="star-narrative">
                ${{formatMarkdownContent(d.hours[4].content)}}
              </div>
            </div>

          </section>
        `;
      }}).join("");

      // Restore checked states from localStorage
      daysData.forEach(d => {{
        d.hours.forEach(h => {{
          const key = `qa_hour_${{d.day}}_${{h.hour}}`;
          if (localStorage.getItem(key) === "true") {{
            const el = document.getElementById(`chk-${{d.day}}-${{h.hour}}`);
            if (el) el.checked = true;
          }}
        }});
      }});
      updateProgress();
    }}

    function toggleHourCard(id) {{
      const card = document.getElementById(id);
      if (card) card.classList.toggle("open");
    }}

    function toggleHourCheck(idKey) {{
      const [day, hour] = idKey.split("-");
      const key = `qa_hour_${{day}}_${{hour}}`;
      const el = document.getElementById(`chk-${{day}}-${{hour}}`);
      if (el) {{
        localStorage.setItem(key, el.checked ? "true" : "false");
      }}
      updateProgress();
    }}

    function updateProgress() {{
      const totalHours = 15 * 5; // 75 hours
      let completed = 0;
      daysData.forEach(d => {{
        d.hours.forEach(h => {{
          if (localStorage.getItem(`qa_hour_${{d.day}}_${{h.hour}}`) === "true") {{
            completed++;
          }}
        }});
      }});
      const pct = (completed / totalHours) * 100;
      document.getElementById("progressFill").style.width = pct + "%";
      document.getElementById("hoursTrackerText").innerText = `${{completed}} / ${{totalHours}} Hours (${{Math.round(pct)}}%)`;
    }}

    function copyAnswer(dayNum, btn) {{
      const day = daysData.find(d => d.day === dayNum);
      if (!day) return;
      const text = `Q (Day ${{day.day}}): ${{day.master_qa.question}}\\n\\nANSWER:\\n${{day.master_qa.answer}}`;
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
      res = res.replace(/```(xml|java|gherkin|groovy|yaml|dockerfile|markdown|sql)?([\\s\\S]*?)```/g, '<pre><code>$2</code></pre>');
      // Inline code
      res = res.replace(/`([^`]+)`/g, '<code>$1</code>');
      // Bold
      res = res.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
      // Headings
      res = res.replace(/^### (.*$)/gim, '<h4 style="color:#38bdf8; margin: 12px 0 6px 0;">$1</h4>');
      res = res.replace(/^## (.*$)/gim, '<h3 style="color:#fff; margin: 16px 0 8px 0;">$1</h3>');
      // Line breaks
      res = res.replace(/\\n\\n/g, '<br><br>');
      res = res.replace(/\\n/g, '<br>');
      return res;
    }}

    function handleSearch() {{
      const q = document.getElementById("searchInput").value.toLowerCase().trim();
      document.querySelectorAll(".day-section").forEach(sec => {{
        const text = sec.innerText.toLowerCase();
        if (!q || text.includes(q)) {{
          sec.style.display = "block";
        }} else {{
          sec.style.display = "none";
        }}
      }});
    }}

    window.addEventListener("DOMContentLoaded", checkAuth);
  </script>
</body>
</html>
"""

with open("janaki_qa_automation_14day_prep.html", "w", encoding="utf-8") as f:
    f.write(html_template)
print("Successfully generated janaki_qa_automation_14day_prep.html")
