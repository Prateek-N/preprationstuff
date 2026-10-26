# -*- coding: utf-8 -*-
"""
Build script for Fikerete Semma's SQL Database Administrator Interview Prep Suite.
Compiles:
1. fikerete_semma_sql_dba_prep.md
2. content/fikerete-semma-sql-dba-prep.mdx
3. fikerete_semma_sql_dba_prep.html
4. public/fikerete_semma_sql_dba_prep.html

Passcode: "Fikerete"
"""

import json
import re
import os
import shutil

from fikerete_questions_part1 import QUESTIONS_PART1
from fikerete_questions_part2 import QUESTIONS_PART2
from fikerete_coding import CODING_PROBLEMS

QUESTIONS = QUESTIONS_PART1 + QUESTIONS_PART2
print(f"Loaded {len(QUESTIONS)} Technical Questions and {len(CODING_PROBLEMS)} Coding Problems.")

# =============================================================================
# 1. GENERATE MASTER MARKDOWN (fikerete_semma_sql_dba_prep.md)
# =============================================================================
def generate_markdown():
    md = []
    md.append("# Fikerete Semma — SQL Database Administrator Technical Interview Preparation Suite\n\n")
    md.append("## Target Role: Senior / Enterprise SQL Database Administrator (High Availability, Performance Tuning, Security & Cloud Migration)\n\n")
    md.append("**Candidate:** Fikerete Semma | Dallas, TX | US Citizen | (214) 427-6448 | fikerzsemma@gmail.com\n\n")
    md.append("**Target Focus:** Microsoft SQL Server (2016–2022) · Always On Availability Groups · Query Store & Wait Stats · T-SQL Tuning · Azure SQL Managed Instance · HIPAA & SOX Security\n\n")
    md.append("**Passcode Lock:** `Fikerete`\n\n")
    md.append("---\n\n")

    md.append("## Executive Summary & Engineering Profile\n\n")
    md.append("> **Fikerete Semma** is a **SQL Database Administrator** with 5+ years of hands-on production experience designing, administering, tuning, and securing enterprise Microsoft SQL Server environments across healthcare (**Cigna Healthcare**) and financial services (**Morgan Stanley**, **Liberty Mutual Insurance**). Fikerete specializes in high availability, mission-critical disaster recovery, query execution plan optimization, internal engine storage structures, and regulatory compliance.\n\n")
    md.append("> At **Cigna Healthcare**, Fikerete architected and administered **SQL Server 2022 Always On Availability Groups** across a 3-node cluster supporting **110 production databases** with sub-5-minute automatic failover capability. She diagnosed and resolved 18 critical performance escalations within her first 90 days using **Query Store**, wait statistics, and **DMVs**, slashing MTTR from **5 hours to under 90 minutes**. She redesigned 12 high-load T-SQL stored procedures using columnstore and rowstore indexing to cut batch runtimes from **38s to <5s**, deployed **Resource Governor** workload pools, automated enterprise maintenance via **Ola Hallengren** and PowerShell, and enforced **HIPAA** compliance using **TDE**, **Always Encrypted**, and **Row-Level Security (RLS)** across 9 PHI tables, while migrating 3 on-prem instances to **Azure SQL Managed Instance** saving **$38,000 annually**.\n\n")
    md.append("> At **Morgan Stanley**, Fikerete administered **85 SQL Server 2019 instances** supporting equity trading and risk analytics under strict **Tier-1 RTO (< 2 hours)**. She resolved 35 high-severity performance escalations per quarter using **sp_WhoIsActive**, **Extended Events**, and **SolarWinds DPA**, remediated parameter sniffing and cardinality estimation regressions, configured **Transactional Replication** across 5 read-replicas handling 3,500 daily risk queries, automated backup validation via **PowerShell dbatools** compressing restore drills from **4 hours to <50 minutes**, and established an **Azure DevOps CI/CD** pipeline that cut unplanned database changes from 7 to 1 per quarter under **SOX** audit controls.\n\n")
    md.append("> At **Liberty Mutual Insurance**, Fikerete managed **55 SQL Server 2016/2017 databases**, developed 18 actuarial stored procedures, eliminated **TempDB allocation page latch contention (PFS/GAM/SGAM)** by aligning multi-file configurations to CPU cores, built a proactive DMV triage runbook, audited 140 deprecated syntax objects during SQL Server 2012 to 2016 upgrades, and reduced monthly SSIS ETL failure counts from 6 to fewer than 2.\n\n")

    md.append("## Quantified Impact & Architecture Metrics\n\n")
    md.append("| Organization | Domain & Role | Core Tech Stack | Quantified Engineering & Business Impact |\n")
    md.append("| :--- | :--- | :--- | :--- |\n")
    md.append("| **Cigna Healthcare** | Enterprise Healthcare DBA | SQL Server 2022, Always On AG, WSFC | Administered **110 production databases** with sub-5-minute automatic failover across 3-node cluster |\n")
    md.append("| **Cigna Healthcare** | Performance Triage | Query Store, DMVs, Wait Statistics | Resolved **18 critical incidents in 90 days**, slashing average MTTR from **5 hours to < 90 minutes** |\n")
    md.append("| **Cigna Healthcare** | Batch ETL Optimization | T-SQL, Columnstore Indexing, Rewrites | Redesigned 12 procedures, cutting nightly batch runtimes from **38 seconds to < 5 seconds** |\n")
    md.append("| **Cigna Healthcare** | Cloud Migration | Azure Migrate, Azure SQL Managed Instance | Migrated 3 on-prem instances to Azure SQL MI, cutting annual licensing by **$38,000** |\n")
    md.append("| **Cigna Healthcare** | Security & Compliance | TDE, Always Encrypted, DDM, RLS, Defender | Achieved **HIPAA compliance** within 60 days on 9 PHI tables with zero audit discrepancies |\n")
    md.append("| **Morgan Stanley** | High-Frequency Trading DBA | SQL Server 2019, Always On, Replication | Administered **85 instances** supporting equity trading, holding Tier-1 RTO under **2 hours** |\n")
    md.append("| **Morgan Stanley** | Incident Escalations | sp_WhoIsActive, Extended Events, SolarWinds | Resolved **35 high-severity escalations/quarter** with average MTTR under **4 hours** |\n")
    md.append("| **Morgan Stanley** | Analytical Offloading | Transactional Replication, 5 Read Replicas | Offloaded **3,500 daily analytical queries** away from primary OLTP servers with sub-second latency |\n")
    md.append("| **Morgan Stanley** | DR Automation | PowerShell, dbatools, Point-in-Time Restore | Automated weekly restore testing across 25 DBs, cutting validation cycle from **4 hours to < 50 min** |\n")
    md.append("| **Morgan Stanley** | Database DevOps & SOX | Azure DevOps, SSDT, Dacpac, CAB Gates | Slashed unplanned database incidents from **7 to 1 per quarter** under SOX access governance |\n")
    md.append("| **Liberty Mutual** | Property & Casualty DBA | SQL Server 2016/2017, TempDB Tuning | Eliminated **PFS/GAM/SGAM allocation contention** across 55 instances during peak rating periods |\n")
    md.append("| **Liberty Mutual** | Modernization & ETL | T-SQL, SSIS, SQL Agent, Upgrades | Upgraded 4 instances from 2012 to 2016, remediating **140 deprecated syntax objects** with zero downtime |\n\n")

    md.append("---\n\n")

    md.append("## Core System Architecture Blueprints\n\n")

    md.append("### Blueprint 1: Cigna Healthcare 3-Node Always On Availability Group Architecture\n\n")
    md.append("```mermaid\ngraph TD\n")
    md.append("    subgraph DallasDC [Primary Data Center: Dallas, TX]\n")
    md.append("        NODE1[Node 1: Primary Replica\\nSQL Server 2022 Enterprise\\nRead-Write OLTP Transactions] \n")
    md.append("        NODE2[Node 2: Secondary Replica\\nSynchronous-Commit\\nAutomatic Failover Target] \n")
    md.append("    end\n")
    md.append("    subgraph RemoteDC [Secondary Disaster Recovery Site]\n")
    md.append("        NODE3[Node 3: Secondary Replica\\nAsynchronous-Commit\\nManual Failover Target] \n")
    md.append("    end\n")
    md.append("    subgraph CloudWitness [Microsoft Azure]\n")
    md.append("        WITNESS[Azure Cloud Witness\\nBlob Storage Quorum Arbitrator]\n")
    md.append("    end\n")
    md.append("    subgraph ClientConnections [Client Routing & Ingress]\n")
    md.append("        APP_OLTP[Core Member & Claims Web Services] -->|Read-Write Intent| LISTENER[AG Virtual Listener: MultiSubnetFailover=True]\n")
    md.append("        APP_REP[Analytics & Provider Lookups] -->|ApplicationIntent=ReadOnly| LISTENER\n")
    md.append("    end\n")
    md.append("    LISTENER -->|Primary Routing| NODE1\n")
    md.append("    LISTENER -.->|Read-Only Routing List| NODE2\n")
    md.append("    NODE1 ===|Synchronous Redo Stream\\nZero Data Loss| NODE2\n")
    md.append("    NODE1 -.->|Asynchronous Log Stream\\nCross-Datacenter| NODE3\n")
    md.append("    DallasDC <--->|Quorum Voting| WITNESS\n")
    md.append("    RemoteDC <--->|Quorum Voting| WITNESS\n")
    md.append("```\n\n")

    md.append("### Blueprint 2: Morgan Stanley Trading Database Topology & Transactional Replication\n\n")
    md.append("```mermaid\ngraph TD\n")
    md.append("    subgraph TradingOLTP [Primary High-Frequency Trading Tier]\n")
    md.append("        TRADE_PRIMARY[(Primary Equity Trading DB\\n85 SQL Server 2019 Instances\\nSub-Millisecond Write Latency)]\n")
    md.append("    end\n")
    md.append("    subgraph DistributionTier [Dedicated Replication Distributor]\n")
    md.append("        DIST_SERVER[Remote Distributor Server\\nDistribution Database on NVMe\\nLog Reader: ReadBatchSize=5000]\n")
    md.append("    end\n")
    md.append("    subgraph AnalyticalSubscribers [Read-Replica Risk Tier]\n")
    md.append("        SUB1[(Read Replica 1: Risk Analytics)]\n")
    md.append("        SUB2[(Read Replica 2: Portfolio Pricing)]\n")
    md.append("        SUB3[(Read Replica 3: Client Trade Reporting)]\n")
    md.append("        SUB4[(Read Replica 4: Regulatory Auditing)]\n")
    md.append("        SUB5[(Read Replica 5: Ad-Hoc Management Queries)]\n")
    md.append("    end\n")
    md.append("    TRADE_PRIMARY -->|Log Reader Agent\\nContinuous Transaction Scraping| DIST_SERVER\n")
    md.append("    DIST_SERVER -->|Distribution Agent 1: 4 Streams| SUB1\n")
    md.append("    DIST_SERVER -->|Distribution Agent 2: 4 Streams| SUB2\n")
    md.append("    DIST_SERVER -->|Distribution Agent 3: 4 Streams| SUB3\n")
    md.append("    DIST_SERVER -->|Distribution Agent 4: 4 Streams| SUB4\n")
    md.append("    DIST_SERVER -->|Distribution Agent 5: 4 Streams| SUB5\n")
    md.append("```\n\n")

    md.append("### Blueprint 3: Enterprise Database Security & HIPAA/SOX Defense-in-Depth\n\n")
    md.append("```mermaid\ngraph LR\n")
    md.append("    subgraph IngressSecurity [Identity & Surface Area Protection]\n")
    md.append("        USER[Application / DBA Client] --> ENTRA[Microsoft Entra ID / MFA]\n")
    md.append("        ENTRA --> RBAC[Role-Based Access Control: Least Privilege]\n")
    md.append("    end\n")
    md.append("    subgraph QueryExecution [Execution & Privacy Controls]\n")
    md.append("        RBAC --> RLS[Row-Level Security: Territory Predicates]\n")
    md.append("        RLS --> DDM[Dynamic Data Masking: Phone / Email / SSN]\n")
    md.append("        DDM --> AE[Always Encrypted: Column Master Key in Azure Key Vault]\n")
    md.append("    end\n")
    md.append("    subgraph StorageSecurity [Storage & Audit Tier]\n")
    md.append("        AE --> TDE[(TDE Encryption at Rest: AES-256 Key)]\n")
    md.append("        AUDIT[SQL Server Audit Specifications] --> SIEM[(Enterprise SIEM / Splunk Audit Vault)]\n")
    md.append("        DEFENDER[Microsoft Defender for SQL] --> SEC_ALERTS[Vulnerability Reports & Threat Alerts]\n")
    md.append("    end\n")
    md.append("```\n\n")

    md.append("---\n\n")

    # =========================================================================
    # SECTION 1: TOP 30 TECHNICAL QUESTIONS
    # =========================================================================
    md.append("# Section 1: Top 30 Technical Interview Questions & Comprehensive Answers (300+ Words Each)\n\n")
    md.append("> **Candidate Delivery Standard:** Every single response is strictly at least 300 words, formatted in small cohesive paragraphs without any bullet points, directly grounded in Fikerete's resume across **Cigna Healthcare**, **Morgan Stanley**, and **Liberty Mutual Insurance**.\n\n")

    current_cat = ""
    for q in QUESTIONS:
        words = len(re.findall(r'\b\w+\b', q['answer']))
        if q.get('category') and q['category'] != current_cat:
            current_cat = q['category']
            md.append(f"## {current_cat}\n\n")

        md.append(f"### Q{q['num']:02d}: {q['title']}\n\n")
        md.append(f"**Interview Question:** *\"{q['question']}\"*\n\n")
        md.append(f"**Perspective & Delivery:** First-Person Engineering Narrative (`{words} words` · Verified $\\ge 300$ words · Strictly No Bullets)  \n\n")
        md.append(f"**Comprehensive Answer:**\n\n")
        md.append(f"{q['answer']}\n\n")
        md.append("---\n\n")

    # =========================================================================
    # SECTION 2: TOP 15 CODING & SCRIPTING PROBLEMS
    # =========================================================================
    md.append("# Section 2: Top 15 Production DBA Coding & Scripting Problems\n\n")
    md.append("### Production-grade T-SQL diagnostic scripts, internals decoding, PowerShell automation, and security policies.\n\n")

    for p in CODING_PROBLEMS:
        md.append(f"### Problem {p['num']}: {p['title']}\n\n")
        md.append(f"**Category:** `{p['category']}`  \n\n")
        md.append("#### 1. Problem Statement\n\n")
        md.append(f"{p['problem_statement']}\n\n")
        md.append("#### 2. Production-Grade Implementation & Commentary\n\n")
        md.append("```sql\n")
        md.append(f"{p['code'].strip()}\n")
        md.append("```\n\n")
        md.append("#### 3. Execution Profile & Algorithmic Complexity\n\n")
        md.append(f"{p['complexity']}\n\n")
        md.append("---\n\n")

    # =========================================================================
    # SECTION 3: SCENARIOS & RESUME DEFENSE
    # =========================================================================
    md.append("# Section 3: Candidate Experience Defense, Behavioral Framework & Senior DBA Mindset\n\n")

    md.append("### 1. Cigna Healthcare — Enterprise Availability & Compliance Leadership\n\n")
    md.append("At Cigna Healthcare, Fikerete operated as the technical authority across 110 production databases on SQL Server 2022. When defending this experience, emphasize her mastery over Windows Server Failover Clustering, Availability Group quorum with Azure Cloud Witness, and the exact failover threshold settings (HealthCheckTimeout=30000ms, FailureConditionLevel=3). Highlight how she used Query Store and wait statistics to systematically diagnose 18 critical incidents, cutting MTTR from 5 hours to under 90 minutes. Emphasize her multi-layered HIPAA security implementation spanning TDE, Always Encrypted, Row-Level Security, and Dynamic Data Masking, alongside her cloud migration of 3 instances to Azure SQL Managed Instance saving $38,000 annually.\n\n")

    md.append("### 2. Morgan Stanley — High-Throughput Trading & Disaster Recovery Engineering\n\n")
    md.append("At Morgan Stanley, Fikerete managed 85 SQL Server 2019 instances supporting high-frequency equity trading with strict Tier-1 RTO under 2 hours. In interviews, articulate her precision triage methodology using sp_WhoIsActive, Extended Events, and SolarWinds DPA to resolve 35 high-severity escalations quarterly. Defend her remediation of parameter sniffing and Cardinality Estimation regressions using OPTIMIZE FOR hints and plan guides. Discuss how she scaled analytical reporting by engineering Transactional Replication across 5 read-replicas, and how she built a PowerShell dbatools automation framework that reduced weekly restore testing from 4 hours to under 50 minutes under SOX compliance.\n\n")

    md.append("### 3. Liberty Mutual Insurance — Database Internals & Infrastructure Modernization\n\n")
    md.append("At Liberty Mutual, Fikerete laid the foundational bedrock of her database administration career across 55 property and casualty databases. Key interview talking points include resolving TempDB allocation page latch contention (PFS, GAM, SGAM) by aligning multi-file configurations to CPU cores, establishing a proactive DMV monitoring runbook that intercepted 12 critical blocking and disk events, authoring 18 actuarial stored procedures, and remediating 140 deprecated syntax objects during a zero-downtime migration from SQL Server 2012 to 2016.\n\n")

    return "".join(md)

# =============================================================================
# 2. GENERATE NEXTJS MDX (content/fikerete-semma-sql-dba-prep.mdx)
# =============================================================================
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

def generate_mdx(master_md):
    escaped_body = sanitize_for_mdx(master_md)

    header = """---
title: Fikerete Semma — SQL Database Administrator Interview Preparation Suite
description: Complete technical interview preparation guide for Senior / Enterprise SQL Server DBA — Top 30 technical questions (300+ words each, narrative paragraphs, no bullets), 15 production T-SQL/PowerShell coding problems, architectural blueprints, and experience defense across Cigna Healthcare, Morgan Stanley, and Liberty Mutual.
---

<PasswordGate password="Fikerete" candidateName="Fikerete Semma">

"""

    footer = """

</PasswordGate>
"""
    return header + escaped_body + footer

# =============================================================================
# 3. GENERATE INTERACTIVE WEBPAGE (fikerete_semma_sql_dba_prep.html)
# =============================================================================
def generate_html():
    items_json = []
    categories = []

    # 1. Add Technical Questions
    for q in QUESTIONS:
        words = len(re.findall(r'\b\w+\b', q['answer']))
        cat = q.get('category', 'Technical Excellence')
        if cat not in categories:
            categories.append(cat)
        items_json.append({
            "type": "question",
            "num": q["num"],
            "category": cat,
            "title": q["title"],
            "question": q["question"],
            "words": words,
            "answer": q["answer"]
        })

    # 2. Add Coding Problems
    coding_cat = "DBA T-SQL & Automation Scripts"
    if coding_cat not in categories:
        categories.append(coding_cat)

    for p in CODING_PROBLEMS:
        full_content = f"### 1. Problem Statement\n{p['problem_statement']}\n\n### 2. Production Implementation & Commentary\n```sql\n{p['code'].strip()}\n```\n\n### 3. Execution Profile & Algorithmic Complexity\n{p['complexity']}"
        words = len(re.findall(r'\b\w+\b', full_content))
        items_json.append({
            "type": "coding",
            "num": p["num"],
            "category": coding_cat,
            "title": f"Script {p['num']}: {p['title']}",
            "question": p["problem_statement"][:175] + "...",
            "words": words,
            "answer": full_content
        })

    items_json_str = json.dumps(items_json, ensure_ascii=False)
    categories_json_str = json.dumps(categories, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SQL Database Administrator Interview Prep Suite · Fikerete Semma</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <style>
    :root {{
      --bg-base: #07090e;
      --bg-surface: #0e121a;
      --bg-card: #141a26;
      --bg-card-hover: #1c2436;
      --border: #222c3f;
      --border-accent: #3b82f6;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --sql-blue: #0284c7;
      --sql-cyan: #06b6d4;
      --sql-emerald: #10b981;
      --sql-amber: #f59e0b;
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg-base);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.65;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }}

    /* LOCK SCREEN */
    #lockScreen {{
      position: fixed; inset: 0;
      background: radial-gradient(circle at center, #0f1d33 0%, #03060a 100%);
      display: flex; align-items: center; justify-content: center;
      z-index: 99999; padding: 1.5rem;
    }}
    .lock-box {{
      background: rgba(14, 18, 26, 0.96);
      backdrop-filter: blur(24px);
      border: 1px solid rgba(59, 130, 246, 0.45);
      border-radius: 22px;
      padding: 2.75rem 2.5rem;
      max-width: 490px;
      width: 100%;
      text-align: center;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.95), 0 0 60px rgba(59, 130, 246, 0.25);
    }}
    .lock-logo-mark {{
      display: inline-flex; align-items: center; justify-content: center;
      margin-bottom: 1.25rem; font-size: 2.3rem; font-weight: 900; letter-spacing: -0.04em;
    }}
    .lock-txt-1 {{ color: #ffffff; }}
    .lock-txt-2 {{ color: #38bdf8; }}
    .lock-badge-pill {{
      background: linear-gradient(135deg, rgba(2, 132, 199, 0.25), rgba(56, 189, 248, 0.25));
      border: 1px solid rgba(56, 189, 248, 0.4);
      padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; color: #7dd3fc;
      font-family: var(--font-mono); margin-left: 8px; font-weight: 700;
    }}
    .lock-box h2 {{ font-size: 1.45rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.02em; }}
    .lock-box p {{ color: var(--text-muted); font-size: 0.88rem; margin-bottom: 1.75rem; }}
    .input-group {{ position: relative; margin-bottom: 1.25rem; }}
    .input-group input {{
      width: 100%;
      background: rgba(7, 9, 14, 0.92);
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
      border-color: var(--sql-cyan);
      box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.25);
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
      letter-spacing: 0.04em;
    }}
    .unlock-btn:hover {{
      transform: translateY(-1px);
      box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.5);
      background: linear-gradient(135deg, #0ea5e9, #0284c7);
    }}
    .error-msg {{
      color: #f87171; font-size: 0.85rem; margin-top: 0.9rem; display: none; font-weight: 500;
    }}

    /* MAIN APP */
    #app {{ display: none; }}
    .page-wrapper {{ max-width: 1400px; margin: 0 auto; padding: 2rem 2.5rem 5rem; }}

    /* HEADER */
    .top-bar {{
      display: flex; align-items: center; justify-content: space-between;
      padding: 1.25rem 0; border-bottom: 1px solid var(--border); margin-bottom: 2.5rem;
    }}
    .brand-mark {{
      display: flex; align-items: center; gap: 14px; font-weight: 800; font-size: 1.35rem; letter-spacing: -0.03em;
    }}
    .brand-badge {{
      background: rgba(2, 132, 199, 0.15); border: 1px solid rgba(56, 189, 248, 0.35);
      color: #7dd3fc; font-family: var(--font-mono); font-size: 0.72rem;
      font-weight: 600; padding: 4px 10px; border-radius: 6px;
    }}
    .header-links {{ display: flex; align-items: center; gap: 1rem; }}
    .header-btn {{
      background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border);
      color: var(--text-muted); padding: 0.55rem 1.1rem; border-radius: 8px;
      font-size: 0.85rem; font-weight: 600; text-decoration: none; transition: all 0.2s;
      cursor: pointer;
    }}
    .header-btn:hover {{ background: rgba(255, 255, 255, 0.1); color: #fff; border-color: var(--border-accent); }}

    /* HERO BANNER */
    .hero-banner {{
      background: linear-gradient(135deg, rgba(14, 29, 51, 0.9) 0%, rgba(10, 15, 24, 0.95) 100%);
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-radius: 20px; padding: 2.75rem; margin-bottom: 2.5rem;
      box-shadow: 0 20px 40px -15px rgba(0,0,0,0.7); position: relative; overflow: hidden;
    }}
    .hero-banner::after {{
      content: ""; position: absolute; right: -80px; top: -80px; width: 320px; height: 320px;
      background: radial-gradient(circle, rgba(56, 189, 248, 0.2) 0%, transparent 70%);
      pointer-events: none; border-radius: 50%;
    }}
    .hero-eyebrow {{
      font-family: var(--font-mono); font-size: 0.8rem; text-transform: uppercase;
      color: #7dd3fc; font-weight: 700; letter-spacing: 0.08em; margin-bottom: 0.75rem;
      display: flex; align-items: center; gap: 8px;
    }}
    .hero-eyebrow::before {{
      content: ""; display: inline-block; width: 8px; height: 8px; background: #38bdf8; border-radius: 50%;
      box-shadow: 0 0 10px #38bdf8;
    }}
    .hero-title {{
      font-size: 2.45rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 1rem; line-height: 1.25;
    }}
    .hero-title span {{
      background: linear-gradient(135deg, #ffffff 40%, #7dd3fc 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .hero-subtitle {{
      color: var(--text-muted); font-size: 1.05rem; max-width: 980px; line-height: 1.7; margin-bottom: 2rem;
    }}
    .hero-stats-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1.25rem;
    }}
    .stat-card {{
      background: rgba(7, 9, 14, 0.75); border: 1px solid var(--border);
      border-radius: 12px; padding: 1.25rem; transition: transform 0.2s;
    }}
    .stat-card:hover {{ transform: translateY(-2px); border-color: var(--border-accent); }}
    .stat-val {{
      font-size: 1.65rem; font-weight: 800; color: #fff; margin-bottom: 0.25rem;
      font-family: var(--font-mono);
    }}
    .stat-val.blue {{ color: #7dd3fc; }}
    .stat-val.emerald {{ color: #34d399; }}
    .stat-val.cyan {{ color: #38bdf8; }}
    .stat-val.amber {{ color: #fbbf24; }}
    .stat-label {{ font-size: 0.8rem; color: var(--text-muted); font-weight: 500; }}

    /* ARCHITECTURE MERMAID SECTION */
    .arch-section {{
      background: var(--bg-surface); border: 1px solid var(--border);
      border-radius: 16px; padding: 2rem; margin-bottom: 2.5rem;
    }}
    .arch-header {{
      display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem;
      padding-bottom: 1rem; border-bottom: 1px solid var(--border);
    }}
    .arch-title {{ font-size: 1.35rem; font-weight: 700; color: #fff; }}
    .arch-badge {{
      font-size: 0.75rem; font-family: var(--font-mono); background: rgba(2, 132, 199, 0.2);
      color: #7dd3fc; padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.4);
    }}
    .mermaid-box {{
      background: rgba(7, 9, 14, 0.8); border: 1px solid var(--border);
      border-radius: 12px; padding: 1.75rem; overflow-x: auto; margin-bottom: 1.5rem;
    }}

    /* CONTROLS & FILTER BAR */
    .controls-panel {{
      background: var(--bg-surface); border: 1px solid var(--border);
      border-radius: 16px; padding: 1.5rem; margin-bottom: 2rem;
      display: flex; flex-direction: column; gap: 1.25rem;
    }}
    .search-row {{ display: flex; gap: 1rem; align-items: center; }}
    .search-input-wrap {{ flex: 1; position: relative; }}
    .search-input-wrap input {{
      width: 100%; background: var(--bg-base); border: 1px solid var(--border);
      padding: 0.85rem 1.2rem; border-radius: 10px; color: #fff; font-size: 0.95rem;
      outline: none; transition: all 0.2s;
    }}
    .search-input-wrap input:focus {{ border-color: var(--sql-cyan); box-shadow: 0 0 0 2px rgba(6, 182, 212, 0.25); }}
    .action-btn-group {{ display: flex; gap: 0.75rem; }}
    .ctrl-btn {{
      background: var(--bg-card); border: 1px solid var(--border); color: var(--text-muted);
      padding: 0.85rem 1.25rem; border-radius: 10px; font-size: 0.88rem; font-weight: 600;
      cursor: pointer; transition: all 0.2s; white-space: nowrap;
    }}
    .ctrl-btn:hover {{ background: var(--bg-card-hover); color: #fff; border-color: var(--border-accent); }}
    .pill-filters {{ display: flex; flex-wrap: wrap; gap: 0.6rem; }}
    .pill-btn {{
      background: var(--bg-card); border: 1px solid var(--border); color: var(--text-muted);
      padding: 0.45rem 1rem; border-radius: 8px; font-size: 0.82rem; font-weight: 600;
      cursor: pointer; transition: all 0.2s;
    }}
    .pill-btn:hover {{ color: #fff; border-color: var(--text-muted); }}
    .pill-btn.active {{
      background: var(--sql-blue); color: #ffffff; border-color: var(--sql-blue);
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
    }}

    /* PROGRESS BAR */
    .progress-bar-wrap {{
      background: var(--bg-base); border: 1px solid var(--border); border-radius: 10px;
      padding: 0.85rem 1.25rem; display: flex; align-items: center; justify-content: space-between; gap: 1.5rem;
    }}
    .progress-text {{ font-size: 0.85rem; font-weight: 600; color: var(--text-muted); font-family: var(--font-mono); }}
    .progress-track {{
      flex: 1; height: 8px; background: rgba(255, 255, 255, 0.08); border-radius: 4px; overflow: hidden;
    }}
    .progress-fill {{
      height: 100%; width: 0%; background: linear-gradient(90deg, #0284c7, #10b981);
      border-radius: 4px; transition: width 0.3s ease;
    }}

    /* QUESTION & CODING CARDS */
    .card-list {{ display: flex; flex-direction: column; gap: 1.25rem; }}
    .q-card {{
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 14px; overflow: hidden; transition: all 0.25s ease;
    }}
    .q-card:hover {{ border-color: rgba(56, 189, 248, 0.4); box-shadow: 0 8px 24px -6px rgba(0,0,0,0.6); }}
    .q-card.completed {{ border-color: rgba(16, 185, 129, 0.45); }}
    .q-card.completed .q-header {{ background: rgba(16, 185, 129, 0.04); }}

    .q-header {{
      padding: 1.25rem 1.5rem; cursor: pointer; display: flex;
      align-items: center; justify-content: space-between; gap: 1rem;
      user-select: none;
    }}
    .q-header-left {{ display: flex; align-items: flex-start; gap: 1rem; flex: 1; }}
    .q-num-badge {{
      background: rgba(2, 132, 199, 0.15); border: 1px solid rgba(56, 189, 248, 0.35);
      color: #7dd3fc; font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700;
      padding: 4px 9px; border-radius: 6px; white-space: nowrap; margin-top: 2px;
    }}
    .q-num-badge.coding-badge {{
      background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35);
      color: #34d399;
    }}
    .q-meta-group {{ display: flex; flex-direction: column; gap: 0.25rem; }}
    .q-cat-tag {{
      font-size: 0.72rem; color: var(--text-dim); text-transform: uppercase;
      font-weight: 700; letter-spacing: 0.05em; font-family: var(--font-mono);
    }}
    .q-title-text {{ font-size: 1.05rem; font-weight: 700; color: #fff; line-height: 1.4; }}
    .q-prompt-sub {{ font-size: 0.88rem; color: var(--text-muted); font-style: italic; margin-top: 2px; }}

    .q-header-right {{ display: flex; align-items: center; gap: 1rem; }}
    .word-badge {{
      font-size: 0.72rem; font-family: var(--font-mono); color: var(--text-dim);
      background: rgba(255, 255, 255, 0.04); padding: 3px 8px; border-radius: 4px;
      white-space: nowrap;
    }}
    .q-checkbox {{
      width: 18px; height: 18px; accent-color: #10b981; cursor: pointer;
    }}
    .chevron {{
      color: var(--text-dim); font-size: 0.85rem; transition: transform 0.25s;
    }}
    .q-card.open .chevron {{ transform: rotate(180deg); color: #fff; }}

    .q-body {{
      display: none; padding: 0 1.5rem 1.75rem; border-top: 1px solid rgba(255, 255, 255, 0.04);
      animation: fadeIn 0.2s ease-in;
    }}
    .q-card.open .q-body {{ display: block; }}
    @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}

    .answer-content {{
      margin-top: 1.25rem; color: #cbd5e1; font-size: 0.96rem; line-height: 1.78;
    }}
    .answer-content p {{ margin-bottom: 1.15rem; }}
    .answer-content p:last-child {{ margin-bottom: 0; }}
    .answer-content strong {{ color: #ffffff; font-weight: 700; }}
    .answer-content h3 {{ color: #e2e8f0; font-size: 1.1rem; margin: 1.25rem 0 0.5rem; }}
    .answer-content h4 {{ color: #cbd5e1; font-size: 1.0rem; margin: 1.0rem 0 0.4rem; }}
    .answer-content pre {{
      background: #04060a; border: 1px solid var(--border); border-radius: 10px;
      padding: 1.25rem; overflow-x: auto; margin: 1.25rem 0;
      font-family: var(--font-mono); font-size: 0.88rem; line-height: 1.6; color: #e2e8f0;
    }}
    .answer-content code {{
      font-family: var(--font-mono); font-size: 0.86rem; background: rgba(2, 132, 199, 0.12);
      color: #7dd3fc; padding: 2px 6px; border-radius: 4px;
    }}
    .answer-content pre code {{
      background: transparent; color: inherit; padding: 0; font-size: 0.88rem;
    }}

    .q-footer-bar {{
      display: flex; align-items: center; justify-content: flex-end; gap: 1rem;
      margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.05);
    }}
    .copy-ans-btn {{
      background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border);
      color: var(--text-muted); padding: 0.45rem 0.95rem; border-radius: 6px;
      font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
    }}
    .copy-ans-btn:hover {{ background: rgba(255, 255, 255, 0.08); color: #fff; }}
    .copy-toast {{
      font-size: 0.78rem; font-family: var(--font-mono); color: #34d399; opacity: 0; transition: opacity 0.2s;
    }}
    .copy-toast.show {{ opacity: 1; }}

    /* FOOTER */
    .page-footer {{
      margin-top: 4rem; padding-top: 2rem; border-top: 1px solid var(--border);
      text-align: center; color: var(--text-dim); font-size: 0.85rem;
    }}

    @media (max-width: 768px) {{
      .page-wrapper {{ padding: 1.25rem 1rem 3rem; }}
      .hero-banner {{ padding: 1.75rem; }}
      .hero-title {{ font-size: 1.75rem; }}
      .search-row {{ flex-direction: column; align-items: stretch; }}
      .action-btn-group {{ justify-content: space-between; }}
    }}
  </style>
</head>
<body>

  <!-- PASSCODE LOCK SCREEN -->
  <div id="lockScreen">
    <div class="lock-box">
      <div class="lock-logo-mark">
        <span class="lock-txt-1">SQL</span><span class="lock-txt-2">DBA</span>
        <span class="lock-badge-pill">PREP PORTAL</span>
      </div>
      <h2>Enterprise Database Administrator Prep</h2>
      <p>Candidate: Fikerete Semma · Enter passcode to unlock</p>
      <div class="input-group">
        <input type="password" id="passInput" placeholder="Enter Access Passcode" autofocus autocomplete="off">
      </div>
      <button class="unlock-btn" onclick="checkPass()">Unlock Master Guide</button>
      <div class="error-msg" id="errMsg">Incorrect passcode. Please verify your credentials.</div>
    </div>
  </div>

  <!-- MAIN INTERACTIVE APP -->
  <div id="app">
    <div class="page-wrapper">

      <!-- TOP BAR -->
      <div class="top-bar">
        <div class="brand-mark">
          <span style="color:#fff;">SQL<span style="color:#38bdf8;">DBA</span></span>
          <span class="brand-badge">ENTERPRISE INTERVIEW PREP</span>
        </div>
        <div class="header-links">
          <button class="header-btn" onclick="lockPage()">🔒 Lock Portal</button>
        </div>
      </div>

      <!-- HERO BANNER -->
      <div class="hero-banner">
        <div class="hero-eyebrow">Enterprise Database Administration Suite</div>
        <div class="hero-title">
          <span>Fikerete Semma</span> · SQL Server DBA
        </div>
        <div class="hero-subtitle">
          Engineered for Senior / Enterprise SQL Database Administrator interviews across Healthcare and Financial Services. Covers SQL Server 2016–2022, Always On Availability Groups, Query Store, Wait Statistics, T-SQL Tuning, Resource Governor, TempDB Allocation, Azure SQL Managed Instance, and HIPAA/SOX Security.
        </div>
        <div class="hero-stats-grid">
          <div class="stat-card">
            <div class="stat-val blue">30 Q&As</div>
            <div class="stat-label">300+ Words Each · No Bullets · Narrative</div>
          </div>
          <div class="stat-card">
            <div class="stat-val emerald">15 Scripts</div>
            <div class="stat-label">Blocking, TempDB, Deadlocks, HA/DR, PowerShell</div>
          </div>
          <div class="stat-card">
            <div class="stat-val cyan">110 DBs / 85 Inst</div>
            <div class="stat-label">Cigna Healthcare & Morgan Stanley Scale</div>
          </div>
          <div class="stat-card">
            <div class="stat-val amber">5h to &lt;90m</div>
            <div class="stat-label">MTTR Incident Resolution Reduction</div>
          </div>
        </div>
      </div>

      <!-- ARCHITECTURAL BLUEPRINTS -->
      <div class="arch-section">
        <div class="arch-header">
          <div class="arch-title">Architecture Blueprint 1: Cigna Healthcare 3-Node Always On Availability Group Topology</div>
          <span class="arch-badge">SQL Server 2022 + Synchronous/Async Commit + Azure Cloud Witness</span>
        </div>
        <div class="mermaid-box">
          <div class="mermaid">
graph TD
    subgraph DallasDC [Primary Data Center: Dallas, TX]
        NODE1[Node 1: Primary Replica\\nSQL Server 2022 Enterprise\\nRead-Write OLTP Transactions] 
        NODE2[Node 2: Secondary Replica\\nSynchronous-Commit\\nAutomatic Failover Target] 
    end
    subgraph RemoteDC [Secondary Disaster Recovery Site]
        NODE3[Node 3: Secondary Replica\\nAsynchronous-Commit\\nManual Failover Target] 
    end
    subgraph CloudWitness [Microsoft Azure]
        WITNESS[Azure Cloud Witness\\nBlob Storage Quorum Arbitrator]
    end
    subgraph ClientConnections [Client Routing & Ingress]
        APP_OLTP[Core Member & Claims Web Services] -->|Read-Write Intent| LISTENER[AG Virtual Listener: MultiSubnetFailover=True]
        APP_REP[Analytics & Provider Lookups] -->|ApplicationIntent=ReadOnly| LISTENER
    end
    LISTENER -->|Primary Routing| NODE1
    LISTENER -.->|Read-Only Routing List| NODE2
    NODE1 ===|Synchronous Redo Stream\\nZero Data Loss| NODE2
    NODE1 -.->|Asynchronous Log Stream\\nCross-Datacenter| NODE3
    DallasDC <--->|Quorum Voting| WITNESS
    RemoteDC <--->|Quorum Voting| WITNESS
          </div>
        </div>
      </div>

      <div class="arch-section">
        <div class="arch-header">
          <div class="arch-title">Architecture Blueprint 2: Morgan Stanley Trading Database Topology & Transactional Replication</div>
          <span class="arch-badge">SQL Server 2019 + Remote Distributor + 5 Analytical Read Replicas</span>
        </div>
        <div class="mermaid-box">
          <div class="mermaid">
graph TD
    subgraph TradingOLTP [Primary High-Frequency Trading Tier]
        TRADE_PRIMARY[(Primary Equity Trading DB\\n85 SQL Server 2019 Instances\\nSub-Millisecond Write Latency)]
    end
    subgraph DistributionTier [Dedicated Replication Distributor]
        DIST_SERVER[Remote Distributor Server\\nDistribution Database on NVMe\\nLog Reader: ReadBatchSize=5000]
    end
    subgraph AnalyticalSubscribers [Read-Replica Risk Tier]
        SUB1[(Read Replica 1: Risk Analytics)]
        SUB2[(Read Replica 2: Portfolio Pricing)]
        SUB3[(Read Replica 3: Client Trade Reporting)]
        SUB4[(Read Replica 4: Regulatory Auditing)]
        SUB5[(Read Replica 5: Ad-Hoc Management Queries)]
    end
    TRADE_PRIMARY -->|Log Reader Agent\\nContinuous Transaction Scraping| DIST_SERVER
    DIST_SERVER -->|Distribution Agent 1: 4 Streams| SUB1
    DIST_SERVER -->|Distribution Agent 2: 4 Streams| SUB2
    DIST_SERVER -->|Distribution Agent 3: 4 Streams| SUB3
    DIST_SERVER -->|Distribution Agent 4: 4 Streams| SUB4
    DIST_SERVER -->|Distribution Agent 5: 4 Streams| SUB5
          </div>
        </div>
      </div>

      <!-- CONTROLS & FILTER PANEL -->
      <div class="controls-panel">
        <div class="search-row">
          <div class="search-input-wrap">
            <input type="text" id="searchInput" placeholder="Search across 30 technical questions and 15 DBA coding scripts (keywords, DMVs, wait types)..." oninput="applyFilters()">
          </div>
          <div class="action-btn-group">
            <button class="ctrl-btn" onclick="expandAll(true)">Expand All</button>
            <button class="ctrl-btn" onclick="expandAll(false)">Collapse All</button>
          </div>
        </div>

        <div class="pill-filters" id="categoryPills">
          <!-- Populated by JS -->
        </div>

        <div class="progress-bar-wrap">
          <div class="progress-text" id="progressText">0 / 45 Reviewed (0%)</div>
          <div class="progress-track">
            <div class="progress-fill" id="progressFill"></div>
          </div>
        </div>
      </div>

      <!-- QUESTIONS AND CODING CONTAINER -->
      <div class="card-list" id="questionList">
        <!-- Rendered via JS -->
      </div>

      <!-- FOOTER -->
      <div class="page-footer">
        SQL Database Administrator Technical Interview Preparation Suite · Fikerete Semma
      </div>

    </div>
  </div>

  <script>
    const CORRECT_PASS = "Fikerete";
    const itemsData = {items_json_str};
    const categoriesList = {categories_json_str};

    let activeCategory = "All";
    let completedSet = new Set();

    document.addEventListener("DOMContentLoaded", () => {{
      mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
      if (sessionStorage.getItem('fikerete_unlocked') === 'true') {{
        unlockApp();
      }}
      initApp();
    }});

    function checkPass() {{
      const val = document.getElementById('passInput').value.trim();
      if (val.toLowerCase() === CORRECT_PASS.toLowerCase()) {{
        sessionStorage.setItem('fikerete_unlocked', 'true');
        unlockApp();
      }} else {{
        document.getElementById('errMsg').style.display = 'block';
      }}
    }}

    document.getElementById('passInput').addEventListener('keydown', (e) => {{
      if (e.key === 'Enter') checkPass();
    }});

    function unlockApp() {{
      document.getElementById('lockScreen').style.display = 'none';
      document.getElementById('app').style.display = 'block';
      window.scrollTo(0, 0);
    }}

    function lockPage() {{
      sessionStorage.removeItem('fikerete_unlocked');
      document.getElementById('app').style.display = 'none';
      document.getElementById('lockScreen').style.display = 'flex';
      document.getElementById('passInput').value = '';
      document.getElementById('errMsg').style.display = 'none';
    }}

    function initApp() {{
      const pillBox = document.getElementById('categoryPills');
      pillBox.innerHTML = '';
      
      const allBtn = document.createElement('button');
      allBtn.className = 'pill-btn active';
      allBtn.textContent = 'All Items (' + itemsData.length + ')';
      allBtn.onclick = () => setCategory('All', allBtn);
      pillBox.appendChild(allBtn);

      categoriesList.forEach(cat => {{
        const btn = document.createElement('button');
        btn.className = 'pill-btn';
        const count = itemsData.filter(q => q.category === cat).length;
        btn.textContent = `${{cat}} (${{count}})`;
        btn.onclick = () => setCategory(cat, btn);
        pillBox.appendChild(btn);
      }});

      renderQuestions();
    }}

    function setCategory(cat, btnElem) {{
      activeCategory = cat;
      document.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
      btnElem.classList.add('active');
      applyFilters();
    }}

    function renderQuestions() {{
      const container = document.getElementById('questionList');
      container.innerHTML = '';

      itemsData.forEach((item, idx) => {{
        const card = document.createElement('div');
        card.className = 'q-card';
        card.id = `qcard-${{idx}}`;
        card.setAttribute('data-category', item.category);

        const renderedMd = marked.parse(item.answer);
        const isCoding = item.type === "coding";
        const badgeClass = isCoding ? "q-num-badge coding-badge" : "q-num-badge";
        const badgeLabel = isCoding ? `Script ${{item.num}}` : `Q${{item.num.toString().padStart(2, '0')}}`;

        card.innerHTML = `
          <div class="q-header" onclick="toggleCard(${{idx}})">
            <div class="q-header-left">
              <span class="${{badgeClass}}">${{badgeLabel}}</span>
              <div class="q-meta-group">
                <span class="q-cat-tag">${{item.category}}</span>
                <div class="q-title-text">${{item.title}}</div>
                <div class="q-prompt-sub">${{item.question}}</div>
              </div>
            </div>
            <div class="q-header-right">
              <span class="word-badge">${{item.words}} words</span>
              <input type="checkbox" class="q-checkbox" onclick="event.stopPropagation(); toggleComplete(${{idx}})" title="Mark completed">
              <span class="chevron">▼</span>
            </div>
          </div>
          <div class="q-body">
            <div class="answer-content">
              ${{renderedMd}}
            </div>
            <div class="q-footer-bar">
              <button class="copy-ans-btn" onclick="copyAnswer(${{idx}}, this)">📋 Copy Answer / Code</button>
              <span class="copy-toast" id="toast-${{idx}}">Copied to clipboard!</span>
            </div>
          </div>
        `;
        container.appendChild(card);
      }});
      updateProgress();
    }}

    function toggleCard(idx) {{
      const card = document.getElementById(`qcard-${{idx}}`);
      card.classList.toggle('open');
    }}

    function expandAll(open) {{
      document.querySelectorAll('.q-card').forEach(c => {{
        if (open) c.classList.add('open');
        else c.classList.remove('open');
      }});
    }}

    function toggleComplete(idx) {{
      const card = document.getElementById(`qcard-${{idx}}`);
      if (completedSet.has(idx)) {{
        completedSet.delete(idx);
        card.classList.remove('completed');
      }} else {{
        completedSet.add(idx);
        card.classList.add('completed');
      }}
      updateProgress();
    }}

    function updateProgress() {{
      const total = itemsData.length;
      const count = completedSet.size;
      const pct = Math.round((count / total) * 100);
      document.getElementById('progressFill').style.width = pct + '%';
      document.getElementById('progressText').textContent = `${{count}} / ${{total}} Reviewed (${{pct}}%)`;
    }}

    function applyFilters() {{
      const query = document.getElementById('searchInput').value.toLowerCase().trim();

      itemsData.forEach((item, idx) => {{
        const card = document.getElementById(`qcard-${{idx}}`);
        const matchesCat = (activeCategory === 'All' || item.category === activeCategory);
        const textContent = (item.title + ' ' + item.question + ' ' + item.answer).toLowerCase();
        const matchesQuery = !query || textContent.includes(query);

        if (matchesCat && matchesQuery) {{
          card.style.display = 'block';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    function copyAnswer(idx, btn) {{
      const item = itemsData[idx];
      if (!item) return;
      navigator.clipboard.writeText(item.answer).then(() => {{
        const toast = document.getElementById(`toast-${{idx}}`);
        toast.classList.add('show');
        setTimeout(() => {{ toast.classList.remove('show'); }}, 2000);
      }});
    }}
  </script>
</body>
</html>
"""
    return html

# =============================================================================
# MAIN BUILD SCRIPT ENTRYPOINT
# =============================================================================
def main():
    print(f"Building Fikerete Semma SQL DBA Prep Suite...")

    # 1. Master Markdown
    master_md = generate_markdown()
    md_path = "fikerete_semma_sql_dba_prep.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(master_md)
    print(f"Master Markdown generated: {md_path} ({len(master_md.split())} words)")

    # 2. Nextra MDX
    mdx_content = generate_mdx(master_md)
    mdx_path = os.path.join("content", "fikerete-semma-sql-dba-prep.mdx")
    with open(mdx_path, "w", encoding="utf-8") as f:
        f.write(mdx_content)
    print(f"Nextra MDX generated: {mdx_path}")

    # 3. Interactive Webpage
    html_content = generate_html()
    html_path = "fikerete_semma_sql_dba_prep.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Interactive Webpage generated: {html_path}")

    # 4. Copy to public/
    os.makedirs("public", exist_ok=True)
    pub_html_path = os.path.join("public", "fikerete_semma_sql_dba_prep.html")
    with open(pub_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Public Webpage generated: {pub_html_path}")

    print("\nAll Fikerete Semma SQL DBA prep assets successfully compiled!")

if __name__ == "__main__":
    main()
