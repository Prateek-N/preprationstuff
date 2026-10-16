# -*- coding: utf-8 -*-
"""
Master compiler script to assemble:
1. amazon_wwde_data_scientist_haritha_prep.md
2. content/haritha-amazon-wwde-prep.mdx
3. haritha_amazon_wwde_prep.html & public/haritha_amazon_wwde_prep.html
Reads from haritha_part1.md, haritha_part2.md, and haritha_part3.md directly.
"""

import re
import os

with open('haritha_part1.md', 'r', encoding='utf-8') as f:
    part1 = f.read()

with open('haritha_part2.md', 'r', encoding='utf-8') as f:
    part2 = f.read()

with open('haritha_part3.md', 'r', encoding='utf-8') as f:
    part3 = f.read()

HEADER_MD = """# Amazon Worldwide Design Engineering (WWDE) — Data Scientist II Onsite Loop Preparation Guide
**Candidate**: Haritha Anand | **Role**: Data Scientist II (Job ID: 10521209) | **Org**: Worldwide Fulfillment Design & Engineering (WWDE)
**Location**: Bellevue, WA / Onsite Loop | **Format**: 5 Sessions (Science Depth, Science Application, Coding/Problem Solving, GenAI Fluency, Leadership Principles)

---

## Executive Overview & Interview Blueprint

You are interviewing for the **Data Scientist II** role within Amazon's **Worldwide Design Engineering (WWDE)** organization. WWDE sits at the cross-section of data science, high-performance physical operations, and advanced industrial automation. You are not building detached toy models; you are developing machine learning, mathematical optimization, and statistical systems that govern **Amazon's global fulfillment center network of tomorrow**.

### Interview Loop Architecture (5 One-Hour Rounds)
1. **Round 1: Science Depth**: Deep dive into your past modeling decisions, mathematical formulation, loss functions, custom feature engineering, and trade-offs. (Grounded in your **Honeywell** IoT XGBoost anomaly detection, **Uber** PyTorch demand forecasting, and **KPMG** BERTopic/NER work).
2. **Round 2: Science Application**: End-to-end problem framing under ambiguity. Clarifying questions, metric trees, data pipelines, baseline heuristic vs. ML, offline validation, and production feedback loops. (Focus on warehouse throughput drops, MHE predictive maintenance, and operational dashboards).
3. **Round 3: Coding & Problem Solving (LiveCode)**: Writing clean Python and SQL code in real-time without an IDE or compiler. (SQL window functions, CTEs, lag/lead, numpy ML from scratch, sliding window, heaps, dynamic programming).
4. **Round 4: GenAI Fluency**: Pragmatic application of foundation models, RAG, and multi-agent workflows to physical operations. Ragas evaluation, hallucination guardrails, and when classical ML beats GenAI.
5. **Round 5: Amazon Leadership Principles**: Strict **STAR** behavioral evaluation across 11 key principles with quantified metrics, first-person ownership, and lessons learned.

---
"""

FULL_MARKDOWN = f"""{HEADER_MD}
{part1}

{part2}

{part3}
"""

def sanitize_for_mdx(markdown_text: str) -> str:
    """
    Sanitizes raw markdown to be 100% valid Nextra MDX:
    - Protects code blocks (``` ... ```)
    - Replaces { and } with HTML entities &#123; and &#125; in prose
    - Replaces standalone comparison < with &lt;
    """
    parts = re.split(r'(```[\s\S]*?```)', markdown_text)
    sanitized_parts = []
    
    for i, part in enumerate(parts):
        # Even index: regular prose
        if i % 2 == 0:
            # Replace { and } outside code
            p = part.replace('{', '&#123;').replace('}', '&#125;')
            # Replace standalone < followed by numbers or spaces or comparisons (e.g. < 2s, <10ms, <3.0, < 60)
            p = re.sub(r'<(?=[\s\d=\$\\%])', '&lt;', p)
            # Replace standalone > followed by numbers or comparisons (e.g. > 120, >10%)
            lines = p.split('\n')
            sanitized_lines = []
            for line in lines:
                if line.strip().startswith('>'):
                    sanitized_lines.append(line)
                else:
                    sanitized_lines.append(re.sub(r'(?<=\s)>(?=[\s\d=\$\\%])', '&gt;', line))
            p = '\n'.join(sanitized_lines)
            sanitized_parts.append(p)
        else:
            # Odd index: code block, keep intact
            sanitized_parts.append(part)
            
    return ''.join(sanitized_parts)

# 1. Standalone Markdown file
with open('amazon_wwde_data_scientist_haritha_prep.md', 'w', encoding='utf-8') as f:
    f.write(FULL_MARKDOWN)
print("Successfully generated: amazon_wwde_data_scientist_haritha_prep.md")

# 2. Nextra MDX file
sanitized_content = sanitize_for_mdx(FULL_MARKDOWN)
mdx_file_content = f"""---
title: Haritha Anand — Amazon WWDE Data Scientist II Preparation
description: Comprehensive 5-session interview preparation suite for Amazon Worldwide Design Engineering (WWDE) Data Scientist II.
---

import {{ PasswordGate }} from '../components/PasswordGate'

<PasswordGate password="Haritha" candidateName="Haritha">

{sanitized_content}

</PasswordGate>
"""

with open('content/haritha-amazon-wwde-prep.mdx', 'w', encoding='utf-8') as f:
    f.write(mdx_file_content)
print("Successfully generated: content/haritha-amazon-wwde-prep.mdx")

# 3. HTML application
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Haritha Anand — Amazon WWDE Data Scientist II Onsite Preparation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-secondary: #111827;
            --bg-card: rgba(17, 24, 39, 0.7);
            --border-color: rgba(255, 255, 255, 0.08);
            --accent-orange: #FF9900; /* Amazon Amber */
            --accent-blue: #00A8E8;
            --accent-purple: #8B5CF6;
            --text-primary: #F3F4F6;
            --text-secondary: #9CA3AF;
            --text-muted: #6B7280;
            --code-bg: #030712;
            --success: #10B981;
            --danger: #EF4444;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.65;
            -webkit-font-smoothing: antialiased;
        }

        /* Password Gate Modal Overlay */
        #auth-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(10, 14, 23, 0.95);
            backdrop-filter: blur(16px);
            z-index: 99999;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
        }

        .auth-card {
            background: linear-gradient(135deg, rgba(31, 41, 55, 0.8), rgba(17, 24, 39, 0.95));
            border: 1px solid rgba(255, 153, 0, 0.3);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 40px rgba(255, 153, 0, 0.15);
            border-radius: 20px;
            padding: 2.75rem 2.25rem;
            max-width: 440px;
            width: 100%;
            text-align: center;
        }

        .auth-badge {
            display: inline-block;
            background: rgba(255, 153, 0, 0.12);
            color: var(--accent-orange);
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 0.35rem 1rem;
            border-radius: 9999px;
            margin-bottom: 1.25rem;
            border: 1px solid rgba(255, 153, 0, 0.25);
        }

        .auth-title {
            font-size: 1.65rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 0.5rem;
            color: #FFFFFF;
        }

        .auth-desc {
            font-size: 0.925rem;
            color: var(--text-secondary);
            margin-bottom: 1.75rem;
        }

        .auth-input-group {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .auth-input {
            width: 100%;
            padding: 0.9rem 1.25rem;
            border-radius: 12px;
            background: rgba(3, 7, 18, 0.6);
            border: 1px solid var(--border-color);
            color: #FFFFFF;
            font-size: 1rem;
            outline: none;
            transition: all 0.2s ease;
        }

        .auth-input:focus {
            border-color: var(--accent-orange);
            box-shadow: 0 0 0 3px rgba(255, 153, 0, 0.25);
        }

        .auth-btn {
            background: linear-gradient(135deg, #FF9900, #F57C00);
            color: #111827;
            font-weight: 700;
            font-size: 1rem;
            padding: 0.9rem;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 14px rgba(255, 153, 0, 0.35);
        }

        .auth-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(255, 153, 0, 0.5);
        }

        .auth-error {
            color: var(--danger);
            font-size: 0.85rem;
            margin-top: 0.75rem;
            display: none;
        }

        /* App Layout */
        .app-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2.5rem 1.5rem 6rem;
        }

        /* Top Hero */
        .top-hero {
            background: linear-gradient(135deg, rgba(31, 41, 55, 0.6), rgba(17, 24, 39, 0.8));
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 2.5rem;
            margin-bottom: 2.5rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        }

        .top-hero::after {
            content: '';
            position: absolute;
            top: -100px;
            right: -100px;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(255, 153, 0, 0.15) 0%, transparent 70%);
            pointer-events: none;
        }

        .hero-tagline {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(255, 153, 0, 0.1);
            color: var(--accent-orange);
            border: 1px solid rgba(255, 153, 0, 0.25);
            padding: 0.3rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }

        .hero-title {
            font-size: 2.4rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 0.75rem;
            color: #FFFFFF;
        }

        .hero-subtitle {
            font-size: 1.05rem;
            color: var(--text-secondary);
            max-width: 850px;
            margin-bottom: 1.5rem;
        }

        .hero-meta-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border-color);
        }

        .meta-pill {
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }

        .meta-pill-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-muted);
            font-weight: 600;
        }

        .meta-pill-value {
            font-size: 0.95rem;
            color: var(--text-primary);
            font-weight: 600;
        }

        /* Search & Filter Bar */
        .controls-bar {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            position: sticky;
            top: 1rem;
            z-index: 100;
            background: rgba(10, 14, 23, 0.85);
            backdrop-filter: blur(12px);
            padding: 0.75rem;
            border-radius: 14px;
            border: 1px solid var(--border-color);
        }

        .search-box {
            flex: 1;
            position: relative;
        }

        .search-input {
            width: 100%;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            color: #FFFFFF;
            padding: 0.75rem 1rem 0.75rem 2.5rem;
            border-radius: 10px;
            font-size: 0.95rem;
            outline: none;
            transition: all 0.2s ease;
        }

        .search-input:focus {
            border-color: var(--accent-orange);
            box-shadow: 0 0 0 2px rgba(255, 153, 0, 0.2);
        }

        .search-icon {
            position: absolute;
            left: 0.85rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
        }

        /* Markdown Render Body */
        .content-body {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 18px;
            padding: 3rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .content-body h1 {
            display: none;
        }

        .content-body h2 {
            font-size: 1.85rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-top: 3.5rem;
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .content-body h2:first-of-type {
            margin-top: 0;
        }

        .content-body h3 {
            font-size: 1.35rem;
            font-weight: 700;
            color: #E5E7EB;
            margin-top: 2.25rem;
            margin-bottom: 1rem;
        }

        .content-body h4 {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--accent-orange);
            margin-top: 1.5rem;
            margin-bottom: 0.6rem;
        }

        .content-body p {
            margin-bottom: 1.25rem;
            color: #D1D5DB;
            font-size: 1rem;
        }

        .content-body strong {
            color: #FFFFFF;
            font-weight: 700;
        }

        .content-body ul, .content-body ol {
            margin-bottom: 1.5rem;
            padding-left: 1.75rem;
            color: #D1D5DB;
        }

        .content-body li {
            margin-bottom: 0.5rem;
        }

        /* Code Blocks */
        pre {
            background: var(--code-bg);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.25rem;
            overflow-x: auto;
            margin: 1.25rem 0 1.75rem;
            position: relative;
        }

        code {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: #E5E7EB;
        }

        p code, li code {
            background: rgba(255, 255, 255, 0.08);
            color: #FBBF24;
            padding: 0.2rem 0.45rem;
            border-radius: 6px;
            font-size: 0.85em;
        }

        .copy-code-btn {
            position: absolute;
            top: 0.75rem;
            right: 0.75rem;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: var(--text-secondary);
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.35rem 0.65rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .copy-code-btn:hover {
            background: rgba(255, 255, 255, 0.2);
            color: #FFFFFF;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.75rem 0;
            font-size: 0.95rem;
        }

        th, td {
            padding: 0.85rem 1.1rem;
            text-align: left;
            border: 1px solid var(--border-color);
        }

        th {
            background: rgba(31, 41, 55, 0.6);
            color: #FFFFFF;
            font-weight: 700;
        }

        tr:nth-child(even) {
            background: rgba(255, 255, 255, 0.02);
        }

        /* Mermaid Diagrams */
        .mermaid {
            background: rgba(3, 7, 18, 0.4);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.75rem 0;
            text-align: center;
        }

        @media (max-width: 768px) {
            .content-body {
                padding: 1.5rem;
            }
            .hero-title {
                font-size: 1.85rem;
            }
            .top-hero {
                padding: 1.5rem;
            }
        }
    </style>
</head>
<body>

<div id="auth-overlay">
    <div class="auth-card">
        <div class="auth-badge">Encrypted Access · Locked Guide</div>
        <h2 class="auth-title">Amazon WWDE Prep Suite</h2>
        <p class="auth-desc">Welcome <strong>Haritha</strong>. Enter your candidate password to unlock your personalized interview loop preparation dossier.</p>
        <form id="auth-form" onsubmit="handleAuth(event)">
            <div class="auth-input-group">
                <input type="password" id="password-input" class="auth-input" placeholder="Enter Access Password..." autofocus autocomplete="off" />
                <button type="submit" class="auth-btn">Unlock Dossier</button>
            </div>
            <div id="auth-error" class="auth-error">Incorrect password. Please try again.</div>
        </form>
    </div>
</div>

<div class="app-container" id="main-content" style="display: none;">
    <div class="top-hero">
        <div class="hero-tagline">
            <span>●</span> Amazon Worldwide Fulfillment Design & Engineering (WWDE)
        </div>
        <h1 class="hero-title">Haritha Anand — Data Scientist II Onsite Loop Dossier</h1>
        <p class="hero-subtitle">
            Comprehensive 5-session interview preparation master guide covering Science Depth, Science Application, 21 LiveCode Coding Solutions, Frontier GenAI Fluency, 11 STAR Leadership Principles, and End-to-End System Design (HLD & LLD).
        </p>
        <div class="hero-meta-grid">
            <div class="meta-pill">
                <span class="meta-pill-label">Candidate</span>
                <span class="meta-pill-value">Haritha Anand</span>
            </div>
            <div class="meta-pill">
                <span class="meta-pill-label">Target Role</span>
                <span class="meta-pill-value">Data Scientist II (Job ID: 10521209)</span>
            </div>
            <div class="meta-pill">
                <span class="meta-pill-label">Organization</span>
                <span class="meta-pill-value">Worldwide Design Engineering (WWDE)</span>
            </div>
            <div class="meta-pill">
                <span class="meta-pill-label">Location / Loop Format</span>
                <span class="meta-pill-value">Bellevue, WA · 5 Virtual Sessions</span>
            </div>
        </div>
    </div>

    <div class="controls-bar">
        <div class="search-box">
            <span class="search-icon">🔍</span>
            <input type="text" id="filter-input" class="search-input" placeholder="Search across 21 coding problems, algorithms, SQL queries, or behavioral stories..." oninput="handleSearch(this.value)" />
        </div>
    </div>

    <main class="content-body" id="render-target">
    </main>
</div>

<script>
    const RAW_MARKDOWN = `MARKDOWN_PAYLOAD_PLACEHOLDER`;

    const VALID_PASSWORDS = ['haritha', 'harithaanand'];
    const STORAGE_KEY = 'auth_gate_haritha';

    function checkAuth() {
        if (sessionStorage.getItem(STORAGE_KEY) === 'unlocked') {
            document.getElementById('auth-overlay').style.display = 'none';
            document.getElementById('main-content').style.display = 'block';
            renderContent();
        }
    }

    function handleAuth(e) {
        e.preventDefault();
        const input = document.getElementById('password-input').value.trim().toLowerCase();
        const errorEl = document.getElementById('auth-error');

        if (VALID_PASSWORDS.includes(input)) {
            sessionStorage.setItem(STORAGE_KEY, 'unlocked');
            document.getElementById('auth-overlay').style.display = 'none';
            document.getElementById('main-content').style.display = 'block';
            renderContent();
        } else {
            errorEl.style.display = 'block';
            document.getElementById('password-input').focus();
        }
    }

    let renderedOnce = false;
    function renderContent() {
        if (renderedOnce) return;
        renderedOnce = true;
        
        const target = document.getElementById('render-target');
        target.innerHTML = marked.parse(RAW_MARKDOWN);

        document.querySelectorAll('pre').forEach((pre) => {
            const btn = document.createElement('button');
            btn.className = 'copy-code-btn';
            btn.innerText = 'Copy Code';
            btn.onclick = () => {
                const code = pre.querySelector('code').innerText;
                navigator.clipboard.writeText(code);
                btn.innerText = 'Copied!';
                setTimeout(() => btn.innerText = 'Copy Code', 2000);
            };
            pre.appendChild(btn);
        });

        mermaid.initialize({
            startOnLoad: false,
            theme: 'dark',
            themeVariables: {
                darkMode: true,
                background: '#030712',
                primaryColor: '#FF9900',
                edgeColor: '#00A8E8'
            }
        });

        document.querySelectorAll('code.language-mermaid').forEach((block) => {
            const container = document.createElement('div');
            container.className = 'mermaid';
            container.textContent = block.textContent;
            block.parentElement.replaceWith(container);
        });

        mermaid.run();
    }

    function handleSearch(query) {
        query = query.toLowerCase().trim();
        const sections = document.querySelectorAll('#render-target h2, #render-target h3, #render-target h4, #render-target p, #render-target pre');
        
        if (!query) {
            document.querySelectorAll('#render-target > *').forEach(el => el.style.display = '');
            return;
        }

        const firstMatch = Array.from(sections).find(el => el.textContent.toLowerCase().includes(query));
        if (firstMatch) {
            firstMatch.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    window.addEventListener('DOMContentLoaded', checkAuth);
</script>
</body>
</html>
"""

escaped_md_for_html = FULL_MARKDOWN.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
complete_html = HTML_TEMPLATE.replace('MARKDOWN_PAYLOAD_PLACEHOLDER', escaped_md_for_html)

with open('haritha_amazon_wwde_prep.html', 'w', encoding='utf-8') as f:
    f.write(complete_html)
print("Successfully generated: haritha_amazon_wwde_prep.html")

os.makedirs('public', exist_ok=True)
with open('public/haritha_amazon_wwde_prep.html', 'w', encoding='utf-8') as f:
    f.write(complete_html)
print("Successfully generated: public/haritha_amazon_wwde_prep.html")

print("All build artifacts generated successfully!")
