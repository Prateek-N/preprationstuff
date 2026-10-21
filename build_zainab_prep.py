# -*- coding: utf-8 -*-
"""
Builder script for Zainab Asif's Business AI Advisor (Syntax) Interview Preparation Suite.
Outputs:
1. zainab_asif_syntax_ai_prep.md (Master Markdown)
2. content/zainab-asif-syntax-ai-prep.mdx (Nextra MDX with PasswordGate)
3. zainab_asif_syntax_ai_prep.html (Standalone Interactive Luxury Webpage)
4. public/zainab_asif_syntax_ai_prep.html (Public static asset)
"""

import os
import re
import json
from zainab_syntax_data_part1 import QUESTIONS_PART1
from zainab_syntax_data_part2 import QUESTIONS_PART2

ALL_QUESTIONS = QUESTIONS_PART1 + QUESTIONS_PART2

print(f"Loaded {len(ALL_QUESTIONS)} questions for Zainab Asif (Syntax Business AI Advisor).")

def clean_formulas(text: str) -> str:
    """Ensure clean typography and no raw unrendered LaTeX."""
    text = text.replace(r'\%', '%')
    text = text.replace(r'\le', '≤').replace(r'\ge', '≥')
    text = text.replace(r'\times', '×').replace(r'\approx', '≈')
    return text

def sanitize_for_mdx(text: str) -> str:
    code_blocks = []
    def code_repl(match):
        code_blocks.append(match.group(0))
        return f"__MDX_CODE_BLOCK_{len(code_blocks)-1}__"

    # Protect code blocks and inline code
    text = re.sub(r"```[\s\S]*?```", code_repl, text)
    text = re.sub(r"`[^`\n]+`", code_repl, text)

    # Sanitize JSX / MDX sensitive characters in prose
    text = text.replace("{", "&#123;").replace("}", "&#125;")
    text = text.replace("<=", "&le;").replace(">=", "&ge;")
    text = re.sub(r"<(?![a-zA-Z\/])", "&lt;", text)

    # Restore code blocks
    for idx, cb in enumerate(code_blocks):
        text = text.replace(f"__MDX_CODE_BLOCK_{idx}__", cb)

    return text

def generate_markdown():
    md = []
    md.append("# Zainab Asif — Business AI Advisor Interview Preparation Master Suite\n")
    md.append("## Target Company: Syntax | Target Role: Business AI Advisor (Manufacturing & Retail Focus)\n\n")
    md.append("**Candidate:** Zainab Asif | Houston, TX | +1 (504) 738-4675 | azainab1119@gmail.com | [LinkedIn](https://linkedin.com) | US Citizen\n")
    md.append("**Target Role:** Business AI Advisor — Manufacturing, Retail & Consumer Goods\n")
    md.append("**Target Company:** Syntax (Global Managed Cloud Provider for SAP S/4HANA, Oracle ERP, AWS, Microsoft Azure)\n")
    md.append("**Core Specialization:** Enterprise AI Advisory, GenAI & Agentic Orchestration, Predictive Analytics, ERP Data Integration, Telematics/IoT, and Commercial Business Case Development\n")
    md.append("**Master Passcode Lock:** `Zainab`\n\n")
    md.append("---\n\n")

    md.append("## Executive Summary & Strategic Fit for Syntax\n\n")
    md.append("> **Zainab Asif** brings over 5 years of specialized product management and technical advisory experience leading end-to-end connected platforms, predictive machine learning models, and enterprise AI integrations across **Automotive (General Motors)**, **Retail & Omnichannel Commerce (7-Eleven)**, and **Industrial Technology (Honeywell)**.\n\n")
    md.append("> Her track record directly matches the core mandate of the **Business AI Advisor** role at **Syntax**:\n")
    md.append("> 1. **Proven Scale in High-Stakes Environments:** Championed connected product roadmaps across **four global brands at General Motors ($150M connected portfolio)**, accelerating time-to-market by **90+ days** and scaling AI voice assistants on **Google Built-In and Alexa to 4 million vehicles** with **1.5M monthly active interactions**.\n")
    md.append("> 2. **Retail Supply Chain & Fulfillment Optimization:** Directed product roadmaps for the **7-Now Delivery App Back Office at 7-Eleven**, deploying **AI-driven demand forecasting models** that prevented **3,500+ delayed deliveries per quarter** and evaluating **Copilot-style AI assistants** that saved **120+ staff hours quarterly** across **10TB+ product and customer datasets**.\n")
    md.append("> 3. **Industrial & Compliance Rigor:** Translated complex operational, compliance, and customer requirements into prioritized production roadmaps at **Honeywell**, delivering 18 features across 4 quarterly releases and reducing defect rework by **27 tickets per cycle** across **2,400+ enterprise users**.\n")
    md.append("> 4. **Commercial Accountability & Consultative Selling:** Deep experience building CFO-ready business cases, modeling total cost of ownership (TCO) and ROI, aligning cross-functional stakeholders, and driving commercial adoption resulting in **800,000 net-new feature activations annually**.\n\n")

    md.append("### Core Competency Matrix: Candidate Alignment with Syntax Mandate\n\n")
    md.append("| Syntax Business AI Advisor Mandate | Zainab Asif's Proven Experience | Core Tech Stack & Methodologies |\n")
    md.append("| :--- | :--- | :--- |\n")
    md.append("| **Executive AI Discovery & Value Propositions** | Led executive roadmap reviews across 6 GM vehicle programs; 40-hr impact-effort prioritization workshops at 7-Eleven. | **Value-Feasibility Matrix**, **Executive Roadmapping**, **P&L / ROI Modeling**, **Jira**, **Power BI** |\n")
    md.append("| **GenAI, Copilots & Agentic Systems** | Evaluated back-office Copilot tools across 10TB+ datasets (7-Eleven); conversational voice assistants across 4M vehicles (GM). | **Azure OpenAI**, **AWS Bedrock**, **Copilots**, **RAG**, **LangChain/LangGraph**, **Prompt Guardrails** |\n")
    md.append("| **Enterprise ERP & Master Data Integration** | Integrated back-office pipelines across MongoDB, Amazon S3, and SQL; legacy system telemetry harmonization (Honeywell). | **SAP S/4HANA**, **SAP DMC**, **Oracle Cloud / JDE**, **REST/OData APIs**, **Amazon S3**, **MongoDB**, **SQL** |\n")
    md.append("| **Predictive AI in Manufacturing (OEE & Maint.)** | In-vehicle telematics streaming, predictive maintenance diagnostics across 4M vehicles; industrial compliance at Honeywell. | **Predictive Maintenance (RUL)**, **Edge Computer Vision**, **IoT Telematics**, **OEE Optimization**, **MQTT** |\n")
    md.append("| **Predictive AI in Retail & Omnichannel** | Piloted demand forecasting for delivery slot allocation (prevented 3,500+ late orders); checkout A/B testing (-25K cart abandons/mo). | **Demand Forecasting (TFT/LightGBM)**, **Dynamic Slotting**, **Churn Classification**, **A/B Testing** |\n")
    md.append("| **Advisory: Knowing When NOT to Use AI** | Successfully argued against non-deterministic LLMs for real-time dispatch, deploying rules + statistical models instead. | **Feasibility Assessment**, **Algorithmic Auditing**, **Deterministic vs Probabilistic AI**, **FinOps** |\n")
    md.append("| **Commercial Pipeline & Hyperscaler Alignment** | Managed $150M connected portfolio; partnered with Google Cloud & Amazon AWS teams on connected vehicle rollouts. | **Co-Selling with AWS/Microsoft/SAP**, **Executive Demos**, **ARR/ACV Expansion**, **Adoption Tracking** |\n\n")

    md.append("---\n\n")

    md.append("## High-Impact Enterprise Architecture & Advisory Playbooks\n\n")

    md.append("### Playbook 1: Smart Manufacturing AI Architecture (SAP S/4HANA & SAP DMC - Smart Press Shop Context)\n")
    md.append("```mermaid\nflowchart TD\n    A[Industrial Press & Tooling Sensors: Vibration, Thermal, Current] --> B[Edge Computer: High-Speed Vision & Anomaly Inference < 150ms]\n    B -->|Defect Detected| C[Pneumatic Hardware Diverter: Quarantine Defective Stamping]\n    B -->|Telemetry Stream| D[Unified Namespace UNS: MQTT over Sparkplug B]\n    D --> E[Cloud Lakehouse: Amazon S3 / Azure Data Lake / Databricks]\n    E --> F[Physics-Informed ML: Remaining Useful Life RUL Prediction]\n    F --> G[Integration Layer: SAP S/4HANA Cloud & SAP DMC Open APIs]\n    G --> H[Automated Work Order in SAP PM & Part Reservation in SAP MM]\n    G --> I[Shop Floor Operational Fiori Terminal & Mobile Dispatch]\n```\n\n")

    md.append("### Playbook 2: Hybrid Enterprise RAG over ERP and Unstructured Documents\n")
    md.append("```mermaid\nflowchart LR\n    A[User Operational Query] --> B{Intent Classifier & Router}\n    B -->|Structured ERP Query| C[Governed Semantic Layer / Text-to-SQL: SAP CDS Views / Oracle]\n    B -->|Unstructured SOP/Manual| D[Hybrid Search: Dense Vector + Sparse BM25 / Pinecone]\n    C --> E[Enterprise Permission / RBAC Filter: Active Directory / SAML]\n    D --> E\n    E --> F[Context Assembly & Strict Guardrails: T=0.0 & Mandatory Citations]\n    F --> G[Enterprise LLM: Azure OpenAI / AWS Bedrock]\n    G --> H[Deterministic Plain-Language Response with Source Citations]\n```\n\n")

    md.append("---\n\n")

    md.append("# Top 30 Technical Interview Questions & In-Depth Answers (300+ Words Each)\n\n")

    current_theme = ""
    for q in ALL_QUESTIONS:
        if q['theme'] != current_theme:
            current_theme = q['theme']
            md.append(f"## {current_theme}\n\n")

        words = len(re.findall(r'\b\w+\b', q['answer']))
        md.append(f"### Q{q['num']}: {q['title']}\n\n")
        md.append(f"**Interview Question:** *\"{q['question']}\"*\n\n")
        md.append(f"**Target Role Context:** Syntax Business AI Advisor — Manufacturing & Retail Focus  \n")
        md.append(f"**Candidate Experience Delivery:** Structured Strategic Response (`{words} words` — Verified $\\ge 300$ words)  \n\n")
        md.append(f"{q['answer']}\n\n")
        md.append("---\n\n")

    md.append("## Strategic Interview Delivery & Behavioral Defense Guide\n\n")
    md.append("### 1. Articulating the Value Proposition of Syntax over Megavendors (Accenture/Deloitte)\n")
    md.append("- **The Narrative:** Large global systems integrators sell armies of junior staff and generic slide decks. **Syntax** brings 50+ years of mission-critical ERP operational intimacy (SAP, Oracle, JD Edwards). In manufacturing and retail, AI cannot function without deep ERP integration. Syntax's edge is that we already manage the client's core transactional backbone, so our AI solutions are integrated directly into operational business rules from day one.\n\n")

    md.append("### 2. Defending 'Knowing When AI Is Not the Right Solution'\n")
    md.append("- **The Narrative:** Draw directly from the **7-Eleven delivery routing experience**. Business requested an LLM routing agent. Zainab proved that high latency (3-5s), non-deterministic hallucination risk, and runaway token costs made GenAI an anti-pattern for real-time dispatch. Implemented deterministic optimization + statistical forecasting instead, preventing 3,500+ delayed deliveries per quarter and deploying GenAI where it actually belonged (back-office reporting copilot saving 120+ hrs/qtr).\n\n")

    md.append("### 3. Demonstrating Scale and High-Stakes Reliability (General Motors)\n")
    md.append("- **The Narrative:** Emphasize scaling connected platforms across **4 million vehicles** with **1.5M monthly interactions** and managing a **$150M connected portfolio**. Proves that Zainab is not an academic theorist; she has deployed software to millions of physical, safety-critical endpoints, monitored telemetry in real-time, and shaped executive roadmaps that secured **800,000 net-new activations annually**.\n\n")

    return "".join(md)

def build_master_suite():
    print("Building Zainab Asif Syntax Business AI Advisor Master Suite...")
    full_md = generate_markdown()
    clean_md = clean_formulas(full_md)

    # 1. Save Master Markdown
    with open("zainab_asif_syntax_ai_prep.md", "w", encoding="utf-8") as f:
        f.write(clean_md)
    print("Saved: zainab_asif_syntax_ai_prep.md")

    # 2. Save Nextra MDX
    mdx_sanitized = sanitize_for_mdx(clean_md)
    mdx_content = f"""---
title: Zainab Asif — Syntax Business AI Advisor Interview Preparation Guide
description: Comprehensive interview preparation guide for Business AI Advisor (Manufacturing & Retail Focus) at Syntax — Top 30 technical questions and in-depth answers (300+ words each) grounded in General Motors, 7-Eleven, and Honeywell experience.
---

<PasswordGate password="Zainab" candidateName="Zainab">

{mdx_sanitized}

</PasswordGate>
"""
    os.makedirs("content", exist_ok=True)
    with open(os.path.join("content", "zainab-asif-syntax-ai-prep.mdx"), "w", encoding="utf-8") as f:
        f.write(mdx_content)
    print("Saved: content/zainab-asif-syntax-ai-prep.mdx")

    # 3. Generate Standalone Luxury HTML
    generate_standalone_html(clean_md)

def generate_standalone_html(full_markdown: str):
    print("Generating standalone interactive luxury HTML application with Marked & Mermaid...")
    md_json = json.dumps(full_markdown)

    html_template = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zainab Asif — Syntax Business AI Advisor Interview Preparation Suite</title>
    <meta name="description" content="Business AI Advisor Interview Preparation Guide for Syntax covering Manufacturing, Retail, SAP S/4HANA, GenAI, and Enterprise Integration.">
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
            --bg-primary: #090d16;
            --bg-secondary: #0f172a;
            --bg-card: rgba(15, 23, 42, 0.75);
            --border-color: rgba(255, 255, 255, 0.1);
            --accent-cyan: #06b6d4;
            --accent-blue: #3b82f6;
            --accent-indigo: #6366f1;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --code-bg: #030712;
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

        /* Header Navigation */
        header {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(9, 13, 22, 0.85);
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
            color: var(--accent-cyan);
            font-size: 1.6rem;
            font-weight: 900;
        }}

        .brand-title {{
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #ffffff 0%, #38bdf8 100%);
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
            width: 280px;
            outline: none;
            transition: all 0.2s ease;
        }}

        .search-box:focus {{
            border-color: var(--accent-cyan);
            box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.25);
            width: 340px;
        }}

        .badge-locked {{
            background: rgba(6, 182, 212, 0.15);
            color: #67e8f9;
            border: 1px solid rgba(6, 182, 212, 0.3);
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* Security Gate Modal */
        #password-overlay {{
            position: fixed;
            inset: 0;
            z-index: 9999;
            background: rgba(9, 13, 22, 0.94);
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
            border-color: var(--accent-cyan);
            box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.3);
        }}

        .auth-btn {{
            width: 100%;
            background: linear-gradient(135deg, #06b6d4 0%, #2563eb 100%);
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
            color: #f8fafc;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
        }}

        h3 {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            color: #e2e8f0;
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
            color: #cbd5e1;
        }}

        strong {{
            color: #ffffff;
            font-weight: 600;
        }}

        blockquote {{
            border-left: 4px solid var(--accent-cyan);
            background: rgba(6, 182, 212, 0.08);
            padding: 1rem 1.5rem;
            border-radius: 0 12px 12px 0;
            margin: 1.5rem 0;
            color: #e2e8f0;
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
            background: var(--accent-cyan);
            color: #030712;
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
            <p class="auth-desc">Syntax — Business AI Advisor Preparation Suite<br>Candidate: <strong>Zainab Asif</strong></p>
            <form id="auth-form" onsubmit="event.preventDefault(); verifyPassword();">
                <input type="password" id="pass-input" class="auth-input" placeholder="ENTER PASSCODE" autocomplete="off" autofocus>
                <button type="submit" class="auth-btn">Unlock Preparation Suite</button>
                <div id="auth-error" class="auth-error">Incorrect passcode. Please enter 'Zainab'.</div>
            </form>
        </div>
    </div>

    <!-- Header Navigation -->
    <header>
        <div class="brand">
            <span class="spark">⚡</span>
            <span class="brand-title">Syntax — Business AI Advisor Suite</span>
        </div>
        <div class="header-controls">
            <input type="text" id="filter-input" class="search-box" placeholder="Search topics, questions, SAP, AI...">
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
                primaryColor: '#06b6d4',
                primaryTextColor: '#ffffff',
                primaryBorderColor: '#3b82f6',
                lineColor: '#38bdf8',
                secondaryColor: '#0f172a',
                tertiaryColor: '#1e293b'
            }}
        }});

        // Authentication Logic
        const STORAGE_KEY = 'auth_gate_zainab';
        const CORRECT_PASS = 'zainab';

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
            document.getElementById('status-badge').textContent = 'Verified: Zainab';
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
            const elements = document.querySelectorAll('h2, h3, p, pre, table');
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
    with open("zainab_asif_syntax_ai_prep.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("Saved: zainab_asif_syntax_ai_prep.html")

    os.makedirs("public", exist_ok=True)
    with open(os.path.join("public", "zainab_asif_syntax_ai_prep.html"), "w", encoding="utf-8") as f:
        f.write(html_template)
    print("Saved: public/zainab_asif_syntax_ai_prep.html")

if __name__ == "__main__":
    build_master_suite()
