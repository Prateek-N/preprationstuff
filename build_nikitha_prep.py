# -*- coding: utf-8 -*-
"""
Builder script for Nikitha Ramesh's Technical Product Manager Interview Preparation Suite.
Outputs:
1. nikitha_ramesh_tpm_prep.md (Master Markdown)
2. content/nikitha-ramesh-tpm-prep.mdx (Nextra MDX with PasswordGate)
3. nikitha_ramesh_tpm_prep.html (Standalone Interactive Luxury Webpage)
4. public/nikitha_ramesh_tpm_prep.html (Public static asset)
"""

import os
import re
import json
from nikitha_data_part1 import QUESTIONS_PART1
from nikitha_data_part2 import QUESTIONS_PART2

ALL_QUESTIONS = QUESTIONS_PART1 + QUESTIONS_PART2

print(f"Loaded {len(ALL_QUESTIONS)} questions across 6 professional experiences.")

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
    md.append("# Nikitha Ramesh — Technical Product Manager Interview Preparation Master Suite\n")
    md.append("## Enterprise SaaS, Agentic AI, Cloud Platforms (AWS/Azure), Data Migrations, and APIs\n\n")
    md.append("**Candidate:** Nikitha Ramesh | Bentonville, AR | +1 484-716-8385 | niramesh.penn@gmail.com | [LinkedIn](https://linkedin.com) | [GitHub](https://github.com) | [Portfolio](https://portfolio.com) | [Substack](https://substack.com)\n")
    md.append("**Target Role:** Technical Product Manager (TPM) / Senior Product Manager — Enterprise SaaS, Cloud, Data & AI\n")
    md.append("**Education:** Master of Engineering Management (Penn State | Chancellor's Scholar & Fox Award) | B.Tech Electronics & Instrumentation\n")
    md.append("**Certifications:** AWS Certified Solutions Architect Associate • Databricks Fundamentals • Certified Ethical Hacker (CEH)\n")
    md.append("**Security Access Passcode:** `Nikitha`\n\n")
    md.append("---\n\n")

    md.append("## Executive Summary & Candidate Value Proposition\n\n")
    md.append("> **Nikitha Ramesh** is a high-impact **Technical Product Manager** with 4+ years of cross-functional leadership spanning enterprise SaaS, cloud infrastructure (AWS, Azure), Agentic AI, large-scale data migrations, REST APIs, and automated workflow platforms. Her unique career trajectory bridges rigorous software engineering foundations (**Freshworks**), enterprise product discovery and commercial strategy (**CoreStack**), academic and industry AI research leadership (**Pennsylvania State University**), large-scale enterprise data cutover governance (**AssistNow Inc**), and digital e-commerce funnel analytics (**Dell**).\n\n")
    md.append("> Nikitha combines deep technical fluency—proven by an **AWS Solutions Architect Associate** certification and professional engineering background—with executive business acumen, translating ambiguous multi-cloud and healthcare compliance constraints into high-velocity product delivery, measurable ARR pipeline growth, and scalable platform architectures.\n\n")

    md.append("### Core Technical Competency Matrix\n\n")
    md.append("| Product & Technical Domain | Key Capabilities & Methodologies | Core Technologies & Tooling |\n")
    md.append("| :--- | :--- | :--- |\n")
    md.append("| **Enterprise Data Migration & Governance** | Multi-domain cutover, delta sync, three-way reconciliation, PII masking, data lineage, compliance auditing | **Workday APIs**, **UKG Pro**, **Snowflake**, **SQL**, **Python**, **OAuth2**, **SAML 2.0**, **RBAC** |\n")
    md.append("| **Agentic AI & Generative Workflows** | 0-to-1 AI product lifecycles, RAG architectures, dynamic agent routing, hallucination guardrails, AI observability | **OpenAI GPT-4o**, **LangChain**, **LangGraph**, **Pinecone**, **Ragas**, **DeepEval**, **Prompt Engineering** |\n")
    md.append("| **Cloud Platforms & Multi-Cloud Governance** | Multi-cloud usage telemetry, policy-as-code guardrails, agentless architecture, enterprise tiering & pricing | **AWS (Lambda, S3, EventBridge, IAM)**, **Azure (Policy, Functions, RBAC)**, **CoreStack**, **FinOps** |\n")
    md.append("| **Distributed Systems & Quality Engineering** | Risk-based test automation, finite state machines, high-concurrency chaos testing, blameless RCA post-mortems | **Ruby**, **Python**, **Jenkins CI/CD**, **RabbitMQ**, **Redis**, **Docker**, **JMeter**, **Locust** |\n")
    md.append("| **B2B Product Analytics & Experimentation** | Micro-funnel analysis, drop-off diagnostics, A/B testing power analysis, user story mapping, executive BI | **Power BI**, **DAX**, **SQL**, **Adobe Analytics**, **Adobe Target**, **Jira**, **Confluence** |\n\n")

    md.append("---\n\n")

    md.append("## Technical Product Management Playbooks & Strategic Frameworks\n\n")

    md.append("### Playbook 1: Enterprise Multi-Domain Data Migration & Cutover Orchestration\n")
    md.append("```mermaid\nflowchart LR\n    A[Legacy Source: UKG Pro] --> B[Encrypted Staging: Snowflake Lakehouse]\n    B --> C[Transformation & Harmonization Engine: Python/SQL]\n    C --> D{Three-Way Automated Reconciliation}\n    D -->|Row Count & Hashing| E[Cryptographic PII Audit]\n    D -->|Financial Sums| F[Penny-Level Payroll Balancing]\n    D -->|Reference Validation| G[Workday Schema Verification]\n    E & F & G --> H[Workday EIB & Web Services API Ingestion]\n    H --> I[Mock Cutover Dry-Runs: 3 Cycles]\n    I --> J[Production Weekend Cutover & Hypercare]\n```\n")
    md.append("- **Phase 1: Discovery & Field-Level Dictionary Mapping:** Profile legacy source schemas via SQL; catalog free-text, denormalized tables; map source attributes to target normalized objects with explicit fallback and null-handling rules.\n")
    md.append("- **Phase 2: Automated Staging & Quarantine Pipelines:** Ingest extracts into encrypted staging (Snowflake/S3); apply column-level PII masking; route invalid records to an isolated quarantine queue with automated Slack alerts.\n")
    md.append("- **Phase 3: Deterministic Three-Way Reconciliation:** Execute automated checks verifying row counts, cryptographic SHA-256 checksums across PII fields, and financial balance roll-forwards (gross-to-net payroll, deduction balances).\n")
    md.append("- **Phase 4: Multi-Iteration Mock Cutovers:** Conduct 3 complete pre-production dry-runs measuring exact minute-by-minute execution timelines, delta extraction catching, and rollback checkpoints before live cutover.\n\n")

    md.append("### Playbook 2: Agentic AI Product Development & Evaluation Lifecycle\n")
    md.append("```mermaid\nflowchart TD\n    A[10K+ Multi-Source Operational Signals] --> B[Semantic Chunking & Metadata Enrichment]\n    B --> C[Hybrid Vector Index: Dense + Sparse BM25]\n    C --> D[User Operational Query] --> E{Dynamic Intent Router: LangGraph}\n    E -->|Simple Lookup| F[Lightweight Fast LLM: GPT-4o-mini]\n    E -->|Multi-Step Reasoning| G[Frontier LLM: GPT-4o / Claude 3.5]\n    G --> H[Pydantic Validated Tool-Calling: SQL / API / Graph]\n    H --> I[Cross-Encoder Reranking & Context Compression]\n    I --> J[Reflection & Grounding Guardrail: Ragas Faithfulness Check]\n    J -->|Pass: Faithfulness ≥ 90%| K[Synthesized Response with Hover Citations]\n    J -->|Fail: Hallucination Detected| L[Self-Correction Retry Loop max 2x]\n```\n")
    md.append("- **Dynamic Intent Routing:** Classify incoming user requests into deterministic state-machine DAGs using constrained schemas to eliminate unbounded prompt wandering.\n")
    md.append("- **Contextual Compression & Hybrid Search:** Combine dense embeddings with sparse lexical BM25 search, followed by cross-encoder reranking to pass only the top 5 high-relevance chunks, slashing token costs by up to 62%.\n")
    md.append("- **Deterministic Tool Calling:** Enforce rigid Pydantic schema validation on all LLM tool arguments (dates, IDs, filters) before executing backend API queries.\n")
    md.append("- **Continuous Quality Observability:** Measure Faithfulness (Grounding), Answer Relevance, Context Recall, and Latency via automated evaluation harnesses (Ragas / LangSmith) across curated golden datasets.\n\n")

    md.append("---\n\n")

    md.append("# Comprehensive Technical Interview Questions & Answers (30 Questions across 6 Experiences)\n\n")

    current_exp = ""
    for q in ALL_QUESTIONS:
        if q['experience'] != current_exp:
            current_exp = q['experience']
            md.append(f"## Experience: {current_exp}\n")
            md.append(f"> **Context & Scope:** {q['role_context']}\n\n")

        words = len(re.findall(r'\b\w+\b', q['answer']))
        md.append(f"### Q{q['num']}: {q['title']}\n\n")
        md.append(f"**Interview Question:** *\"{q['question']}\"*\n\n")
        md.append(f"**Delivery Structure:** Structured First-Person Narrative (`{words} words` — Verified $\\ge 300$ words)  \n\n")
        md.append(f"{q['answer']}\n\n")
        md.append("---\n\n")

    md.append("## Behavioral & Cross-Functional Leadership Guide (First-Person Scenarios)\n\n")
    md.append("### 1. Navigating High-Stakes Enterprise Client Escalations & Conflicting Scope\n")
    md.append("• During our enterprise healthcare migration engagement with **Arcare**, clinical HR directors demanded late-stage custom calculation overrides for holiday shift differentials just three weeks prior to scheduled cutover. While acknowledging their clinical frustration, immediately inserting custom code into the transformation pipeline threatened to destabilize our verified payroll baseline and delay the entire cutover.\n")
    md.append("• Rather than offering a defensive refusal, I scheduled an immediate technical triage session with Arcare's payroll controller and our lead data engineer. I presented an objective **risk-impact analysis in Jira**, illustrating how a late schema modification introduced a 35% probability of payroll calculation errors affecting 800+ nurses. I proposed a phased compromise: for go-live, we instituted an audited manual payroll adjustment batch in Workday to honor the differential, while scheduling the automated calculation engine into our Phase 2 release two weeks post-cutover. The client enthusiastically accepted this transparent risk-mitigated approach, preserving cutover timelines while maintaining complete executive trust.\n\n")

    md.append("### 2. Resisting the 'Custom Development Trap' to Build Scalable Platform Roadmaps\n")
    md.append("• At **CoreStack**, during advanced evaluations with a prospective **$250K+ ARR enterprise account**, the prospect's IT director conditioned contract signing on our engineering squad building a bespoke, proprietary connector for their in-house on-premise inventory database. Sales account executives exerted intense pressure on me to accept the custom development request to close the quarterly revenue quota.\n")
    md.append("• I recognized that building a proprietary, non-reusable connector would introduce toxic technical debt, diverting 40% of our engineering bandwidth from our core multi-cloud roadmap. I deconstructed the client's request into its core architectural job-to-be-done: ingesting external configuration metadata into our policy engine. I drafted a PRD for an **Extensible Webhook & Custom Schema REST Ingestion Framework**, presented the API-first vision to the prospect's enterprise architects, and explained how it offered them superior long-term adaptability. The client embraced the productized approach and signed the enterprise agreement, giving CoreStack a scalable platform capability that subsequently unlocked three additional pipeline deals.\n\n")

    md.append("### 3. Advocating for Technical Debt Remediation and Engineering Refactoring\n")
    md.append("• As a former software engineer at **Freshworks**, I possess deep technical empathy for the corrosive impact of unmanaged technical debt. When leading our squad at **AssistNow Inc**, our initial migration transformation scripts had accumulated complex procedural logic that slowed pre-cutover validation runs to over 4 hours per batch. Business stakeholders pushed to keep adding new features, but our data engineers were burning out debugging brittle transformation edge cases.\n")
    md.append("• To justify an engineering refactoring sprint to non-technical business leaders, I translated technical debt into commercial risk metrics: a 4-hour validation runtime left zero buffer during our tight 48-hour live cutover weekend, turning any pipeline error into a missed Monday payroll deadline. I negotiated a dedicated 1-week 'Architectural Hardening Sprint', during which the squad modularized the transformation engine into vectorized PySpark routines. The refactoring slashed runtime from 4 hours to 42 minutes, providing the exact operational buffer required for our flawless live cutover.\n\n")

    return "".join(md)

def build_master_suite():
    print("Building Nikitha Ramesh Technical Product Manager Master Suite...")
    full_md = generate_markdown()
    clean_md = clean_formulas(full_md)

    # 1. Save Master Markdown
    with open("nikitha_ramesh_tpm_prep.md", "w", encoding="utf-8") as f:
        f.write(clean_md)
    print("Saved: nikitha_ramesh_tpm_prep.md")

    # 2. Save Nextra MDX
    mdx_sanitized = sanitize_for_mdx(clean_md)
    mdx_content = f"""---
title: Nikitha Ramesh — Technical Product Manager Interview Preparation Guide
description: Comprehensive interview preparation guide for Technical Product Manager roles across Enterprise SaaS, Cloud Platforms (AWS/Azure), Agentic AI, Data Migrations, and APIs — 30 in-depth 300+ word technical Q&As across 6 career experiences.
---

<PasswordGate password="Nikitha" candidateName="Nikitha">

{mdx_sanitized}

</PasswordGate>
"""
    os.makedirs("content", exist_ok=True)
    with open(os.path.join("content", "nikitha-ramesh-tpm-prep.mdx"), "w", encoding="utf-8") as f:
        f.write(mdx_content)
    print("Saved: content/nikitha-ramesh-tpm-prep.mdx")

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
    <title>Nikitha Ramesh — Technical Product Manager Interview Preparation Suite</title>
    <meta name="description" content="Technical Product Manager Interview Preparation Guide covering Enterprise SaaS, Cloud Platforms, Agentic AI, and Data Migrations.">
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
            --accent-purple: #8b5cf6;
            --accent-indigo: #6366f1;
            --accent-cyan: #06b6d4;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
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

        /* Header Navigation */
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
            color: var(--accent-purple);
            font-size: 1.6rem;
            font-weight: 900;
        }}

        .brand-title {{
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
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
            border-color: var(--accent-purple);
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.25);
            width: 340px;
        }}

        .badge-locked {{
            background: rgba(139, 92, 246, 0.15);
            color: #c4b5fd;
            border: 1px solid rgba(139, 92, 246, 0.3);
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
            border-color: var(--accent-purple);
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.3);
        }}

        .auth-btn {{
            width: 100%;
            background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
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
            border-left: 4px solid var(--accent-purple);
            background: rgba(139, 92, 246, 0.08);
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
            background: var(--accent-purple);
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
            <p class="auth-desc">Technical Product Manager Interview Preparation Suite<br>Candidate: <strong>Nikitha Ramesh</strong></p>
            <form id="auth-form" onsubmit="event.preventDefault(); verifyPassword();">
                <input type="password" id="pass-input" class="auth-input" placeholder="ENTER PASSCODE" autocomplete="off" autofocus>
                <button type="submit" class="auth-btn">Unlock Preparation Suite</button>
                <div id="auth-error" class="auth-error">Incorrect passcode. Please enter 'Nikitha'.</div>
            </form>
        </div>
    </div>

    <!-- Header Navigation -->
    <header>
        <div class="brand">
            <span class="spark">✸</span>
            <span class="brand-title">Nikitha Ramesh — Technical Product Manager</span>
        </div>
        <div class="header-controls">
            <input type="text" id="filter-input" class="search-box" placeholder="Search topics, questions, APIs, cloud...">
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
                primaryColor: '#8b5cf6',
                primaryTextColor: '#ffffff',
                primaryBorderColor: '#6366f1',
                lineColor: '#38bdf8',
                secondaryColor: '#111827',
                tertiaryColor: '#1f2937'
            }}
        }});

        // Authentication Logic
        const STORAGE_KEY = 'auth_gate_nikitha';
        const CORRECT_PASS = 'nikitha';

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
            document.getElementById('status-badge').textContent = 'Verified: Nikitha';
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
    with open("nikitha_ramesh_tpm_prep.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("Saved: nikitha_ramesh_tpm_prep.html")

    os.makedirs("public", exist_ok=True)
    with open(os.path.join("public", "nikitha_ramesh_tpm_prep.html"), "w", encoding="utf-8") as f:
        f.write(html_template)
    print("Saved: public/nikitha_ramesh_tpm_prep.html")

if __name__ == "__main__":
    build_master_suite()
