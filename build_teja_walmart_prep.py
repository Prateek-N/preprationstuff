# -*- coding: utf-8 -*-
"""
Master Builder for Teja Talluri's Walmart Inbound Planning and Optimization Interview Prep Suite.
Outputs:
1. walmart_inbound_transportation_teja_prep.md
2. content/teja-walmart-transportation-prep.mdx
3. teja_walmart_transportation_prep.html
4. public/teja_walmart_transportation_prep.html
"""

import os
import re
import json
import html
from teja_walmart_data_part1 import QUESTIONS_PART1
from teja_walmart_data_part2 import QUESTIONS_PART2
from teja_walmart_data_part3 import CODING_PROBLEMS

def clean_formulas(text: str) -> str:
    """
    Cleans LaTeX formulas to modern Unicode mathematical typography.
    Ensures zero unrendered LaTeX artifacts like $\approx$ or $$\text{...}$$.
    """
    block_replacements = [
        (
            r'\$\$\\text\{OTIF Compliant\} = 1 \\iff \(\\text\{Arrival Timestamp\} \\in \[\text\{MABD Start\}, \\text\{MABD End\}\]\) \\land \(\\text\{Received Qty\} \\ge \\text\{Ordered Qty\}\)\$\$',
            '```text\nOTIF Compliant = 1 ⟺ (Arrival Timestamp ∈ [MABD Start, MABD End]) ∧ (Received Qty ≥ Ordered Qty)\n```'
        ),
        (
            r'\$\$\\Delta \\text\{Total Freight Cost\} = \\Delta \\text\{Rate Effect\} \+ \\Delta \\text\{Volume Effect\} \+ \\Delta \\text\{Mode Mix Effect\} \+ \\Delta \\text\{Carrier Compliance Effect\} \+ \\Delta \\text\{Accessorial Surcharge Effect\}\$\$',
            '```text\nΔTotal Freight Cost = ΔRate Effect + ΔVolume Effect + ΔMode Mix Effect + ΔCarrier Compliance Effect + ΔAccessorial Surcharge Effect\n```'
        ),
        (
            r'\$\$\\text\{Leakage Cost\} = \\sum_\{i\} \(\\text\{Actual Paid Spot Rate\}_i - \\text\{Primary Contracted Rate\}_i\) \\times \\text\{Miles\}_i\$\$',
            '```text\nLeakage Cost = Σ (Actual Paid Spot Rate_i - Primary Contracted Rate_i) × Miles_i\n```'
        ),
        (
            r'\$\$\\text\{Leakage Cost\} = \\sum \(\\text\{Billed Spot Rate\} - \\text\{Primary Contracted Rate\}\) \\times \\text\{Miles\}\$\$',
            '```text\nLeakage Cost = Σ (Billed Spot Rate - Primary Contracted Rate) × Miles\n```'
        ),
        (
            r'\$\$\\text\{Waterfall Rank Score\} = \\alpha \\cdot \\text\{Contract Rate\} \+ \\beta \\cdot \(1 - \\text\{Historic Rejection Rate\}\) \+ \\gamma \\cdot \\text\{Historic OTIF Score\}\$\$',
            '```text\nWaterfall Rank Score = α · Contract Rate + β · (1 - Historic Rejection Rate) + γ · Historic OTIF Score\n```'
        ),
        (
            r'\$\$\\text\{SS\} = Z \\times \\sqrt\{\\bar\{L\} \\cdot \\sigma_D\^2 \+ \\bar\{D\}\^2 \\cdot \\sigma_L\^2\}\$\$',
            '```text\nSafety Stock (SS) = Z × √(L̄ · σ_D² + D̄² · σ_L²)\n```'
        ),
        (
            r'\$\$\\text\{UCL/LCL\} = \\bar\{X\} \\pm 3 \\cdot \\frac\{\\bar\{R\}\}\{d_2\}\$\$',
            '```text\nUCL / LCL = X̄ ± 3 · (R̄ / d2)\n```'
        ),
        (
            r'\$\$\\text\{MCEI\}_c = w_1 \\cdot \\text\{FTAR\}_c \+ w_2 \\cdot \\text\{OTIF\}_c \+ w_3 \\cdot \\left\(1 - \\frac\{\\text\{Demurrage Hours\}_c\}\{\\text\{Max Demurrage\}\}\\right\) - w_4 \\cdot \\text\{Overbill Rate\}_c\$\$',
            '```text\nMCEI_c = w1 · FTAR_c + w2 · OTIF_c + w3 · (1 - Demurrage Hours_c / Max Demurrage) - w4 · Overbill Rate_c\n```'
        ),
        (
            r'\$\$\\text\{Cube Utilization Rate\} = \\frac\{\\sum_\{i=1\}\^n \\text\{Length\}_i \\times \\text\{Width\}_i \\times \\text\{Height\}_i\}\{\\text\{Internal Trailer Volume \(3,850 cu ft\)\}\} \\times 100\$\$',
            '```text\nCube Utilization Rate = (Σ Length_i × Width_i × Height_i / Internal Trailer Volume 3,850 cu ft) × 100\n```'
        ),
        (
            r'\$\$\\text\{Payload Weight Utilization Rate\} = \\frac\{\\sum_\{i=1\}\^n \\text\{Weight\}_i\}\{\\text\{Max Legal Payload \(44,000 lbs\)\}\} \\times 100\$\$',
            '```text\nPayload Weight Utilization Rate = (Σ Weight_i / Max Legal Payload 44,000 lbs) × 100\n```'
        ),
        (
            r'\$\$Y_\{ist\} = \\alpha \+ \\beta \(\\text\{Treated\}_s \\times \\text\{Post\}_t\) \+ \\gamma_s \+ \\delta_t \+ \\mathbf\{X\}_\{ist\}\' \\boldsymbol\{\\theta\} \+ \\varepsilon_\{ist\}\$\$',
            '```text\nY_ist = α + β · (Treated_s × Post_t) + γ_s + δ_t + X_ist · θ + ε_ist\n```'
        )
    ]

    for pat, repl in block_replacements:
        text = re.sub(pat, repl, text)

    inline_replacements = [
        (r'\$\\text\{FTAR\} = \\frac\{\\text\{Loads Accepted by Primary Carrier\}\}\{\\text\{Total Loads Tendered to Primary Carrier\}\} \\times 100\$', '`FTAR = (Loads Accepted by Primary Carrier / Total Loads Tendered to Primary Carrier) × 100`'),
        (r'\$S\(t\) = P\(T > t\)\$', '`S(t) = P(T > t)`'),
        (r'\$P_\{50\}\$', '`P50`'),
        (r'\$P_\{90\}\$', '`P90`'),
        (r'\$P_\{10\}\$', '`P10`'),
        (r'\$\\ge 90\.0\\%\$', '`≥ 90.0%`'),
        (r'\$<0\.01\\%\$', '`< 0.01%`'),
        (r'\$>25\\%\$', '`> 25%`'),
        (r'\$FTAR < 60\\%\$', '`FTAR < 60%`'),
        (r'\$<24\$', '`< 24`'),
        (r'\$>72\$', '`> 72`'),
        (r'\$-30\$', '`-30`'),
        (r'\$\+0\$', '`+0`'),
        (r'\$T\$', '`T`'),
        (r'\\times', '×'),
        (r'\\cdot', '·'),
        (r'\\approx', '≈'),
        (r'\\rightarrow', '→'),
        (r'\\ge', '≥'),
        (r'\\le', '≤'),
        (r'\\ne', '≠'),
        (r'\\pm', '±'),
        (r'\\mu', 'μ'),
        (r'\\sigma', 'σ'),
        (r'\\alpha', 'α'),
        (r'\\beta', 'β'),
        (r'\\gamma', 'γ'),
        (r'\\delta', 'δ'),
        (r'\\Delta', 'Δ'),
        (r'\\Sigma', 'Σ'),
        (r'\\theta', 'θ'),
        (r'\\varepsilon', 'ε'),
        (r'\\%', '%'),
    ]

    for pat, repl in inline_replacements:
        text = re.sub(pat, repl, text)

    def clean_generic_inline(match):
        inner = match.group(1).strip()
        if re.match(r'^\d+(\.\d+)?[KMBkmb]?$', inner):
            return match.group(0)
        inner_cleaned = inner.replace('\\text{', '').replace('}', '').replace('\\', '').replace('_', ' ')
        return f"`{inner_cleaned}`"

    text = re.sub(r'(?<!\$)\$(?!\$)([^$\n]+)(?<!\$)\$(?!\$)', clean_generic_inline, text)
    return text

def sanitize_for_mdx(text: str) -> str:
    code_blocks = []
    def code_repl(match):
        code_blocks.append(match.group(0))
        return f"__MDX_CODE_BLOCK_{len(code_blocks)-1}__"

    text = re.sub(r"```[\s\S]*?```", code_repl, text)
    text = re.sub(r"`[^`\n]+`", code_repl, text)

    text = text.replace("{", "&#123;").replace("}", "&#125;")
    text = text.replace("<=", "&le;").replace(">=", "&ge;")
    text = re.sub(r"<(?![a-zA-Z\/])", "&lt;", text)

    for idx, cb in enumerate(code_blocks):
        text = text.replace(f"__MDX_CODE_BLOCK_{idx}__", cb)

    return text

def build_coding_problems_markdown(problems: list) -> str:
    md = []
    md.append("## Part 3: 20 Advanced Technical Coding Problems (SQL & Python)\n\n")
    md.append("> Each coding problem is set within **Walmart's Inbound Transportation & Planning Optimization** environment and includes:  \n")
    md.append("> 1. **Problem Statement** (Production-scale requirements, schemas, edge cases)  \n")
    md.append("> 2. **Complete Thought Process** (Algorithmic reasoning, mathematical formulation, trade-offs)  \n")
    md.append("> 3. **Code with Comments** (Clean, production-grade Python or BigQuery SQL)  \n")
    md.append("> 4. **Time & Space Complexity** (Big-O analysis explained)\n\n---\n\n")

    for p in problems:
        md.append(f"### Problem {p['id']} ({p['type']}): {p['title']}\n\n")
        md.append(f"{p['statement']}\n\n")
        md.append(f"{p['thought_process']}\n\n")
        
        lang = "sql" if p['type'] == "SQL" else "python"
        md.append(f"```{lang}\n{p['code']}\n```\n\n")
        md.append(f"#### Complexity Analysis:\n{p['complexity']}\n\n")
        md.append("---\n\n")

    return "".join(md)

def build_master_suite():
    print("Building master interview preparation suite...")

    clean_p1 = clean_formulas(QUESTIONS_PART1)
    clean_p2 = clean_formulas(QUESTIONS_PART2)
    coding_md = build_coding_problems_markdown(CODING_PROBLEMS)

    header_md = """# Teja Talluri — Walmart Senior Data Analyst Interview Preparation Guide
## Transportation: Inbound Planning and Optimization

**Candidate:** Teja Talluri | Prosper, TX (Dallas Metro) | 972-379-7887 | Tejatalluri11@gmail.com | Green Card  
**Target Organization:** Walmart Inc. (805 Respect, Bentonville, AR / Hybrid)  
**Target Role:** Senior Data Analyst — Transportation (Inbound Planning and Optimization)  
**Core Tech Stack:** SQL (BigQuery, Snowflake, Spark SQL), Python (Pandas, NumPy, Scipy, Scikit-learn), Tableau, Looker, Streamlit, Apache Airflow, dbt, Azure Databricks, Agentic AI (OpenAI, Gemini, LangChain)  
**Security Gate Passcode:** `Teja`  

---

## Executive Summary & Strategic Fit

Walmart operates the world's most sophisticated retail supply chain, moving billions of cases annually through hundreds of Regional Distribution Centers (**RDCs**), High-Velocity Cross-Docks (**HVDCs**), and Consolidation Centers. The **Transportation - Inbound Planning and Optimization team** enhances inbound transportation efficiency, service quality, and cost-effectiveness by optimizing shipment planning, carrier routing, dock door turnaround, and vendor compliance.

**Teja Talluri** brings a specialized combination of enterprise business analytics, transportation network optimization, and data engineering leadership:
1. **Supply Chain & Mobility Foundation:** Bachelor of Business Administration in **Operations & Supply Chain Management** (Univ. of Central Oklahoma) combined with dual Master's degrees in **Business Analytics** (CU Denver & Tulane Freeman School of Business).
2. **High-Frequency Mobility & Experimentation (Uber):** Engineered a large-scale A/B testing and causal inference experimentation platform enabling 120+ concurrent experiments, delivering **$8.7M in quarterly revenue impact**. Led capacity forecasting across 8 metro markets delivering **$4.2M in annualized operational savings**. Implemented real-time anomaly detection preventing **$2.1M in fraudulent claims**.
3. **Data Engineering & Modern Data Stack (Dish Network):** Migrated 14 legacy ETL workflows to modern **dbt** and **Fivetran** pipelines on Medallion Architecture with automated data contracts, eliminating **$1.8M in annual infrastructure costs**. Optimized pipelines processing 180M+ daily records, slashing execution from 6 hours to 47 minutes and saving **$420K in compute spend**.
4. **Pharmaceutical Supply Chain Optimization (Cipla):** Forecasted demand for 300+ SKUs using time-series models in Python, directly contributing to capacity planning and reducing inventory overstock by **$900K** across 3 regional distribution hubs. Automated sales reporting, saving **80 analyst hours per month**.
5. **Agentic AI & Practical Automation:** Deep experience integrating **Google Gemini, OpenAI GPT-4o, and Microsoft Copilot** to automate complex manual operational workflows—including automating 2.3M weekly driver support interactions at Uber to save **$1.6M quarterly**.

---

## Core Competency Matrix & Walmart Domain Alignment

| Walmart Inbound Focus Area | Teja's Proven Experience | Core Technologies & Methodologies |
| :--- | :--- | :--- |
| **Inbound Shipment Planning & Routing** | Dynamic supply-demand capacity balancing across 8 metro markets ($4.2M savings at Uber); 5G network telemetry analysis across 12 markets (Dish Network). | **Python**, **Linear Programming (PuLP/SciPy)**, **BigQuery GIS**, **H3 Hexagonal Indexing**, **Dijkstra Multi-Modal Routing** |
| **Vendor OTIF & Carrier Management** | SLA contract enforcement, trailer detention cost reduction, tender waterfall leak audit ($1.8M savings), and carrier scorecard automation. | **SQL Window Functions**, **APPROX_QUANTILES**, **Kaplan-Meier Survival Analysis**, **SPC Control Charts** |
| **Data Quality & Observability** | Airflow anomaly detection preventing $2.1M quarterly fraud (Uber); automated dbt testing, data contracts, and Great Expectations (Dish Network). | **Apache Airflow**, **dbt Core**, **Great Expectations**, **Z-Score Anomaly Streaming**, **Population Stability Index (PSI)** |
| **Cross-Dock & DC Flow Optimization** | Clinical trial batch flow optimization (Cipla); real-time client risk streaming dashboard for 400K subscribers (Dish Network). | **Bin Packing (FFD/BFD)**, **Sweep-Line Interval Merging**, **Kahn's Conveyor DAG Sort**, **Discrete Event Simulation** |
| **Agentic AI & Workflow Automation** | Automated resolution of 2.3M weekly driver support workflows via Gemini & OpenAI ($1.6M/qtr savings at Uber); prompt engineering & RAG pipelines. | **Google Gemini API**, **OpenAI GPT-4o**, **LangChain**, **Cosine Similarity Vector Search**, **AI Autonomous Agents** |
| **Executive Storytelling & BI** | C-suite Tableau, Looker, and Streamlit dashboards compressing reporting cycles from 12 hrs to 2 hrs; C-suite business case presentations. | **Tableau**, **Power BI**, **Looker (LookML)**, **Streamlit**, **Causal Inference (DiD / Synth Control)** |

---

"""

    resume_defense_md = """
## Part 4: Resume Defense Guide & Behavioral Scenarios (STAR Method)

### 1. Uber — Mobility Capacity Forecasting & $8.7M Experimentation Platform
- **The Story:** Built an experimentation platform supporting 120+ concurrent causal product experiments and led capacity planning across 8 metro markets, delivering $4.2M in annualized savings.
- **Walmart Inbound Tie-in:** Inbound transportation capacity operates under identical supply-demand elasticity. When Walmart plans holiday surges, carrier capacity tightens. Teja applies these exact elasticity models and causal inference frameworks to optimize routing guide tender acceptance and prevent spot-market surge penalties.

### 2. Uber — GenAI Driver Support Automation & $1.6M Quarterly Savings
- **The Story:** Integrated Google Gemini and OpenAI to automate 2.3M weekly manual driver support interactions, cutting operational costs by $1.6M per quarter.
- **Walmart Inbound Tie-in:** Walmart's JD explicitly emphasizes **Agentic AI** for transportation planning. Teja demonstrates how autonomous LLM agents parse unstructured carrier delay notices, EDI 214 exceptions, and blizzard force-majeure claims, instantly updating dock appointment schedules and re-tendering loads without manual planner intervention.

### 3. Dish Network — $1.8M dbt Medallion Pipeline & $420K Compute Optimization
- **The Story:** Modernized 14 legacy ETL workflows into dbt/Fivetran on Snowflake/AWS, cutting query runtimes from 6 hours to 47 minutes ($420K compute savings) and eliminating $1.8M in infrastructure costs.
- **Walmart Inbound Tie-in:** Walmart processes terabytes of GPS breadcrumbs, EDI 204/214/210 freight records, and dock door scans in BigQuery. Teja applies date-partitioning, clustering on `destination_dc_id` and `carrier_scac`, and incremental dbt models to keep executive dashboards sub-second while slashing BigQuery query scan costs by up to 95%.

### 4. Cipla Limited — Pharmaceutical Supply Chain & $900K Overstock Reduction
- **The Story:** Forecasted demand for 300+ SKUs using Python time-series models, cutting inventory overstock by $900K across 3 distribution centers and eliminating 80 monthly manual reporting hours.
- **Walmart Inbound Tie-in:** Directly aligns with Walmart's safety stock buffers, supplier lead time volatility hedging, and DC cross-dock inventory turns.

---
"""

    # 1. Write Master Markdown
    full_md = header_md + clean_p1 + "\n\n" + clean_p2 + "\n\n" + coding_md + "\n\n" + resume_defense_md
    with open("walmart_inbound_transportation_teja_prep.md", "w", encoding="utf-8") as f:
        f.write(full_md)
    print("Saved: walmart_inbound_transportation_teja_prep.md")

    # 2. Write Nextra MDX
    clean_p1_mdx = sanitize_for_mdx(clean_p1)
    clean_p2_mdx = sanitize_for_mdx(clean_p2)
    coding_mdx = sanitize_for_mdx(coding_md)
    header_mdx = sanitize_for_mdx(header_md)
    resume_defense_mdx = sanitize_for_mdx(resume_defense_md)

    mdx_body = f"""---
title: Teja Talluri — Walmart Transportation Inbound Planning Prep Guide
description: Comprehensive interview preparation guide for Senior Data Analyst (Transportation Inbound Planning & Optimization) at Walmart — 30 in-depth 300+ word Q&As, 20 advanced coding problems (SQL & Python), and resume defense.
---

<PasswordGate password="Teja" candidateName="Teja">

{header_mdx}

{clean_p1_mdx}

{clean_p2_mdx}

{coding_mdx}

{resume_defense_mdx}

</PasswordGate>
"""
    with open(os.path.join("content", "teja-walmart-transportation-prep.mdx"), "w", encoding="utf-8") as f:
        f.write(mdx_body)
    print("Saved: content/teja-walmart-transportation-prep.mdx")

    # 3. Generate Standalone Luxury HTML using Marked.js client-side parser
    generate_standalone_html(full_md)

def generate_standalone_html(full_markdown: str):
    print("Generating standalone interactive HTML application with client-side Marked & Mermaid...")

    # Safely escape markdown for JSON embedding
    md_json = json.dumps(full_markdown)

    html_template = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teja Talluri — Walmart Transportation Inbound Planning Interview Prep</title>
    <meta name="description" content="Senior Data Analyst Interview Preparation Guide for Walmart Inbound Transportation Planning & Optimization.">
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- Marked.js for fast Markdown parsing -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <!-- Mermaid.js for architectural diagrams -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"></script>
    <style>
        :root {{
            --bg-primary: #0a0e17;
            --bg-secondary: #111827;
            --bg-card: rgba(17, 24, 39, 0.75);
            --border-color: rgba(255, 255, 255, 0.1);
            --accent-blue: #0071dc;
            --accent-yellow: #ffc220;
            --accent-cyan: #06b6d4;
            --accent-emerald: #10b981;
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --text-muted: #6b7280;
            --code-bg: #0f172a;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.7;
            padding: 0;
            margin: 0;
            min-height: 100vh;
        }}

        /* Header */
        header {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(10, 14, 23, 0.85);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .spark {{
            color: var(--accent-yellow);
            font-size: 1.6rem;
            font-weight: 900;
        }}

        .brand-title {{
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #ffffff 0%, #9ca3af 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .header-controls {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .search-box {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 8px 16px;
            border-radius: 9999px;
            font-size: 0.875rem;
            width: 260px;
            outline: none;
            transition: all 0.2s ease;
        }}

        .search-box:focus {{
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 3px rgba(0, 113, 220, 0.25);
            width: 320px;
        }}

        .badge-locked {{
            background: rgba(255, 194, 32, 0.15);
            color: var(--accent-yellow);
            border: 1px solid rgba(255, 194, 32, 0.3);
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* Password Gate Modal */
        #password-overlay {{
            position: fixed;
            inset: 0;
            z-index: 9999;
            background: rgba(10, 14, 23, 0.94);
            backdrop-filter: blur(20px);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
        }}

        .auth-card {{
            background: var(--bg-secondary);
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
            padding: 2.5rem;
            border-radius: 20px;
            width: 100%;
            max-width: 440px;
            text-align: center;
        }}

        .auth-icon {{
            font-size: 2.8rem;
            margin-bottom: 1rem;
        }}

        .auth-title {{
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: #ffffff;
        }}

        .auth-desc {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-bottom: 1.8rem;
        }}

        .auth-input {{
            width: 100%;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            padding: 14px;
            border-radius: 12px;
            color: #ffffff;
            font-size: 1rem;
            text-align: center;
            letter-spacing: 0.1em;
            margin-bottom: 1.2rem;
            outline: none;
            transition: all 0.2s;
        }}

        .auth-input:focus {{
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 3px rgba(0, 113, 220, 0.3);
        }}

        .auth-btn {{
            width: 100%;
            background: linear-gradient(135deg, #0071dc 0%, #004f9a 100%);
            color: #ffffff;
            border: none;
            padding: 14px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .auth-btn:hover {{
            filter: brightness(1.15);
            transform: translateY(-1px);
        }}

        .auth-error {{
            color: #ef4444;
            font-size: 0.825rem;
            margin-top: 10px;
            display: none;
        }}

        /* Content Container */
        .container {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 3rem 2rem 6rem;
        }}

        /* Typography & Markdown Styling */
        h1 {{
            font-size: 2.25rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 1rem;
            line-height: 1.2;
            color: #ffffff;
        }}

        h2 {{
            font-size: 1.6rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-top: 2.5rem;
            margin-bottom: 1.25rem;
            color: #f9fafb;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
        }}

        h3 {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            color: #e5e7eb;
        }}

        h4 {{
            font-size: 1.05rem;
            font-weight: 600;
            margin-top: 1.25rem;
            margin-bottom: 0.5rem;
            color: var(--accent-cyan);
        }}

        p {{
            margin-bottom: 1.25rem;
            color: #d1d5db;
        }}

        strong {{
            color: #ffffff;
            font-weight: 600;
        }}

        blockquote {{
            border-left: 4px solid var(--accent-blue);
            background: rgba(0, 113, 220, 0.08);
            padding: 1rem 1.5rem;
            border-radius: 0 12px 12px 0;
            margin: 1.5rem 0;
            color: #e5e7eb;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            background: var(--bg-secondary);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }}

        th, td {{
            padding: 12px 18px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}

        th {{
            background: rgba(255, 255, 255, 0.04);
            font-weight: 600;
            color: #ffffff;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
        }}

        code {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875em;
            background: rgba(255, 255, 255, 0.08);
            padding: 2px 6px;
            border-radius: 6px;
            color: #38bdf8;
        }}

        pre {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem;
            overflow-x: auto;
            margin: 1.5rem 0;
            position: relative;
        }}

        pre code {{
            background: transparent;
            padding: 0;
            color: #e2e8f0;
            font-size: 0.85rem;
            line-height: 1.6;
        }}

        hr {{
            border: none;
            height: 1px;
            background: var(--border-color);
            margin: 3rem 0;
        }}

        .copy-btn {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: var(--text-secondary);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .copy-btn:hover {{
            background: var(--accent-blue);
            color: #ffffff;
        }}

        .mermaid {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            display: flex;
            justify-content: center;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1.5rem 1rem;
            }}
            .search-box {{
                display: none;
            }}
        }}
    </style>
</head>
<body>

    <!-- Security Gate Modal -->
    <div id="password-overlay">
        <div class="auth-card">
            <div class="auth-icon">🔒</div>
            <h2 class="auth-title">Restricted Access</h2>
            <p class="auth-desc">Walmart Transportation: Inbound Planning & Optimization<br>Candidate: <strong>Teja Talluri</strong></p>
            <form id="auth-form" onsubmit="event.preventDefault(); verifyPassword();">
                <input type="password" id="pass-input" class="auth-input" placeholder="ENTER PASSCODE" autocomplete="off" autofocus>
                <button type="submit" class="auth-btn">Unlock Preparation Suite</button>
                <div id="auth-error" class="auth-error">Incorrect passcode. Please enter 'Teja'.</div>
            </form>
        </div>
    </div>

    <!-- Header Navigation -->
    <header>
        <div class="brand">
            <span class="spark">✸</span>
            <span class="brand-title">Walmart Transportation — Inbound Analytics</span>
        </div>
        <div class="header-controls">
            <input type="text" id="filter-input" class="search-box" placeholder="Search topics, SQL, Python, metrics...">
            <span class="badge-locked" id="status-badge">Locked</span>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="container" id="content-container" style="display: none;"></main>

    <script>
        const RAW_MARKDOWN = {md_json};

        // Initialize Mermaid
        mermaid.initialize({{
            startOnLoad: false,
            theme: 'dark',
            themeVariables: {{
                primaryColor: '#0071dc',
                primaryTextColor: '#ffffff',
                primaryBorderColor: '#004f9a',
                lineColor: '#38bdf8',
                secondaryColor: '#111827',
                tertiaryColor: '#1f2937'
            }}
        }});

        // Authentication Logic
        const STORAGE_KEY = 'auth_gate_teja';
        const CORRECT_PASS = 'teja';

        function checkAuth() {{
            const stored = sessionStorage.getItem(STORAGE_KEY);
            if (stored === 'true') {{
                unlockContent();
            }}
        }}

        function verifyPassword() {{
            const input = document.getElementById('pass-input').value.trim().toLowerCase();
            const errorEl = document.getElementById('auth-error');

            if (input === CORRECT_PASS) {{
                sessionStorage.setItem(STORAGE_KEY, 'true');
                unlockContent();
            }} else {{
                errorEl.style.display = 'block';
                document.getElementById('pass-input').focus();
            }}
        }}

        function unlockContent() {{
            document.getElementById('password-overlay').style.display = 'none';
            const container = document.getElementById('content-container');
            container.style.display = 'block';
            document.getElementById('status-badge').textContent = 'Verified: Teja';
            document.getElementById('status-badge').style.background = 'rgba(16, 185, 129, 0.15)';
            document.getElementById('status-badge').style.color = '#10b981';
            document.getElementById('status-badge').style.borderColor = 'rgba(16, 185, 129, 0.3)';

            // Render Markdown using marked.js
            container.innerHTML = marked.parse(RAW_MARKDOWN);

            // Re-render Mermaid diagrams
            document.querySelectorAll('pre code.language-mermaid').forEach(block => {{
                const pre = block.parentElement;
                const div = document.createElement('div');
                div.className = 'mermaid';
                div.textContent = block.textContent;
                pre.parentElement.replaceChild(div, pre);
            }});
            mermaid.run();

            attachCodeCopyButtons();
        }}

        function attachCodeCopyButtons() {{
            document.querySelectorAll('pre').forEach(pre => {{
                if (pre.querySelector('.copy-btn')) return;
                const btn = document.createElement('button');
                btn.className = 'copy-btn';
                btn.textContent = 'Copy';
                btn.addEventListener('click', () => {{
                    const code = pre.querySelector('code') ? pre.querySelector('code').innerText : pre.innerText;
                    navigator.clipboard.writeText(code).then(() => {{
                        btn.textContent = 'Copied!';
                        setTimeout(() => btn.textContent = 'Copy', 2000);
                    }});
                }});
                pre.appendChild(btn);
            }});
        }}

        // Quick Search Filter
        document.getElementById('filter-input').addEventListener('input', (e) => {{
            const term = e.target.value.toLowerCase();
            const elements = document.querySelectorAll('h3, p, pre, table');
            if (!term) {{
                elements.forEach(el => el.style.opacity = '1');
                return;
            }}
            elements.forEach(el => {{
                if (el.innerText.toLowerCase().includes(term)) {{
                    el.style.opacity = '1';
                }} else {{
                    el.style.opacity = '0.35';
                }}
            }});
        }});

        window.addEventListener('DOMContentLoaded', checkAuth);
    </script>
</body>
</html>
"""

    with open("teja_walmart_transportation_prep.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("Saved: teja_walmart_transportation_prep.html")

    os.makedirs("public", exist_ok=True)
    with open(os.path.join("public", "teja_walmart_transportation_prep.html"), "w", encoding="utf-8") as f:
        f.write(html_template)
    print("Saved: public/teja_walmart_transportation_prep.html")

if __name__ == "__main__":
    build_master_suite()
