# -*- coding: utf-8 -*-
"""
Data Module for Rujuwal Garg's Resume Deep-Dive.
Contains 4 companies, 4 comprehensive dummy projects, and 19 in-depth bullet point explanations (each strictly >= 250 words).
"""

companies_data = [
    # =========================================================================
    # COMPANY 1: SilverSpace Inc. | Team Lead (May 2025 - Present)
    # =========================================================================
    {
        "company_id": "silverspace_lead",
        "company_name": "SilverSpace Inc.",
        "role": "Team Lead | Data Analytics and AI Solutions",
        "tenure": "May 2025 – Present",
        "location": "Gurgaon, India",
        "promotion_note": "Accelerated promotion from Data Analyst to Team Lead in May 2025 within 11 months, recognizing end-to-end technical leadership, architectural vision, and cross-functional operational impact.",
        "project": {
            "name": "Project CognitiveOps — Enterprise Agentic Talent Intelligence & Multi-Location Incentive Governance Platform",
            "tagline": "Multi-Tenant Agentic Digital Assistant, Real-Time BI Intelligence, and Automated Compensation Governance",
            "overview": """As Team Lead, Rujuwal architected and spearheaded **Project CognitiveOps**, a centralized, multi-tenant enterprise platform engineered to unify fragmented recruitment operations, candidate intelligence, interviewer allocation, and technical compensation governance across SilverSpace and its global vendor network (including Vizva Consultancy Services). The platform bridges structured relational operational data with unstructured interview transcripts and company policy knowledge. It integrates real-time **Power BI** analytical dashboards, an autonomous multi-agent digital assistant built with **LangGraph**, **FastAPI**, and the **Model Context Protocol (MCP)**, automated polyglot data pipelines spanning **Azure SQL**, **MongoDB**, and **Python**, an **MLflow/LangSmith** observability framework, and an automated multi-location incentive calculation and audit engine.""",
            "tech_stack": ["Python", "FastAPI", "LangGraph", "LangChain", "LlamaIndex", "Model Context Protocol (MCP)", "Power BI", "DAX", "Azure SQL Database", "MongoDB", "Docker", "Kubernetes", "MLflow", "LangSmith", "Apache Airflow", "Excel / openpyxl"]
        },
        "bullets": [
            {
                "bullet_num": 1,
                "bullet_text": "Mentors 4 junior engineers and collaborates with product, data, and DevOps teams to deliver analytics and AI solutions.",
                "explanation": """Within the execution of **Project CognitiveOps**, technical leadership required establishing rigorous engineering standards, continuous mentorship, and seamless cross-functional alignment. Rujuwal instituted daily 15-minute standups, bi-weekly sprint planning, and structured pair-programming sessions for **4 junior software and data engineers**, guiding them from writing isolated analytical scripts to developing scalable, production-grade microservices. He enforced modern software engineering disciplines, including **PEP 8** adherence, strict type hinting with **Pydantic v2**, modular object-oriented architecture, pre-commit Git hooks, and code review standards requiring comprehensive test coverage using **pytest**. 

To deliver the platform's multi-agent digital assistant and real-time dashboards, Rujuwal functioned as the central architectural liaison across three disparate functional groups:
1. **Product Management:** Collaborating closely to translate ambiguous business requirements—such as reducing recruiter screening fatigue and accelerating executive talent reporting—into concrete Jira epics, user stories, acceptance criteria, and system sequence diagrams.
2. **Data Engineering:** Establishing strict data contract specifications and API interface schemas, ensuring that transactional data from **Azure SQL Database** and document collections from **MongoDB** were formatted deterministically for downstream analytics and vector indexing.
3. **DevOps Engineering:** Partnering to containerize **FastAPI** applications and agent worker nodes using **Docker**, configuring environment secret management via **Azure Key Vault**, configuring resource limits (CPU/memory requests), and establishing automated CI/CD deployment pipelines in **GitHub Actions** with automated linting, security scanning, and blue-green rollouts.

Through this proactive mentorship and cross-functional leadership, junior engineers increased their sprint velocity by **40%**, while deployment defect rates fell to near zero across consecutive production release cycles."""
            },
            {
                "bullet_num": 2,
                "bullet_text": "Translates stakeholder requirements into KPI definitions and analytical frameworks, leveraging Power BI dashboards for operational performance monitoring and business decisions.",
                "explanation": """In **Project CognitiveOps**, executive leadership and recruitment operations managers frequently articulated operational bottlenecks in qualitative terms—such as 'interviews are taking too long to schedule,' 'sourcing bandwidth is improperly allocated,' or 'candidate drop-offs are impacting quarterly placement targets.' Rujuwal bridged this communication gap by translating high-level business concerns into precise, mathematically rigorous **Key Performance Indicator (KPI)** definitions and multidimensional analytical frameworks. He established standard enterprise metrics, including **Time-to-Fill (TTF)**, **Funnel Conversion Velocity** across screening stages, **Recruiter Capacity Utilization Rates**, **Interview Pass-Through Ratios**, and **Cost-per-Hire Attribution**.

To operationalize these KPIs, Rujuwal architected an enterprise **Power BI** semantic model utilizing a star schema architecture, composed of normalized dimension tables (`Dim_Candidate`, `Dim_JobRole`, `Dim_Recruiter`, `Dim_Date`) linked to high-volume transactional fact tables (`Fact_InterviewMilestone`, `Fact_CandidateOutreach`). Within **Power BI**, he authored over 60 complex **DAX (Data Analysis Expressions)** measures, leveraging time-intelligence calculations, dynamic cohort segmentations, moving averages, and filter context manipulation via `CALCULATE()`, `KEEPFILTERS()`, `FILTER()`, and `WINDOW()` functions. 

He designed intuitive, multi-page executive dashboards featuring:
- **Executive KPI Scorecards:** Real-time visual cards highlighting daily placement volume, active candidate pipelines, and month-to-date margin deltas against targets with dynamic conditional formatting.
- **Funnel Drop-Off Analytics:** Visual conversion funnels pinpointing exact drop-off percentages between technical rounds, enabling hiring managers to detect evaluation discrepancies across departments.
- **Recruiter Productivity Matrix:** Quadrant scatter plots benchmarking recruiter outreach volume against successful placement ratios.
- **Dynamic Scenario Modeling:** DAX what-if parameter slicers allowing department heads to project required candidate top-of-funnel sourcing volumes based on targeted hiring quotas.

These dashboards replaced 12 hours of weekly manual reporting, providing department heads with real-time operational visibility that directly guided strategic recruiter reallocations and executive business decisions."""
            },
            {
                "bullet_num": 3,
                "bullet_text": "Strengthens reporting consistency through data validation, metric documentation, and reusable guidance covering ETL, data models, and dashboard logic.",
                "explanation": """Prior to Rujuwal's intervention in **Project CognitiveOps**, reporting across technical, marketing, and recruitment departments suffered from metric fragmentation and conflicting numbers—different teams calculated 'Time-to-Hire,' 'Active Sourced Candidate,' and 'Stage Completion' using inconsistent criteria, leading to decision paralysis during leadership meetings. Rujuwal spearheaded a comprehensive **Data Governance and Standardization Initiative** to establish a single source of operational truth across the enterprise.

He authored an authoritative, enterprise-wide **Data Dictionary and Metric Catalog** documenting over 45 core operational metrics. For every metric, the catalog defined the exact business definition, mathematical formula, source-of-truth database tables, update cadences, ownership teams, and standard SQL/DAX implementation logic. To ensure this logic was universally adopted by engineers and analysts, he authored reusable technical guidelines and developer runbooks covering **ETL design patterns**, normalized dimensional modeling, and **Power BI** semantic layer best practices.

Furthermore, Rujuwal embedded automated **Data Quality Assurance (DQA)** validation checks directly within the data transformation pipelines. Implemented via **Python** and **SQL** stored procedures, these checks automatically validated:
- **Referential Integrity:** Ensuring zero orphaned candidate records in fact tables through foreign key assertions.
- **Primary Key Uniqueness:** Flagging duplicate interview entries prior to ingestion using deterministic hashing.
- **Null Value Tolerances:** Rejecting records missing mandatory recruiter IDs, salary expectations, or placement dates.
- **Statistical Anomaly Detection:** Triggering automated Slack alerts if daily logged interview counts deviated by more than $3\\sigma$ from the 30-day rolling moving average.
- **Schema Drift Guards:** Enforcing strict **Pydantic** contract validation to intercept upstream changes in external applicant tracking feeds before data entered staging tables.

This rigorous governance framework eliminated reporting discrepancies, boosted executive trust in data analytics to **99.4%**, and reduced ad-hoc data defect tickets in Jira by **65%**."""
            },
            {
                "bullet_num": 4,
                "bullet_text": "Applies SQL, Python, and MongoDB for data analysis and preparation for reporting and AI workflows.",
                "explanation": """Within **Project CognitiveOps**, enterprise data was fundamentally polyglot, demanding a sophisticated data engineering and analytical strategy. Structured transactional metadata—such as candidate hiring pipelines, recruiter activity logs, client contracts, and financial billing numbers—resided in relational **Azure SQL Database** instances. Conversely, semi-structured and polymorphic artifacts—such as unstructured interview transcripts, resume parsing extracts, multi-turn AI chat histories, and detailed interviewer feedback evaluations—were stored in **MongoDB** collections due to their flexible BSON document model.

Rujuwal engineered high-performance, asynchronous data preparation pipelines using **Python (Pandas, NumPy, Motor, SQLAlchemy)** and optimized **SQL** queries to bridge these disparate repositories for both business intelligence and downstream AI workflows:
- **For BI & Reporting Workflows:** He authored advanced SQL scripts incorporating Common Table Expressions (**CTEs**), window functions (`ROW_NUMBER()`, `DENSE_RANK()`, `LEAD()`, `LAG()`), and complex multi-table joins to aggregate recruitment metrics, clean dirty operational records, and stage dimensional tables for Power BI.
- **For AI & Agentic Retrieval Workflows:** He built Python data preparation workers that extracted unstructured interview transcripts and resume documents from **MongoDB**. Using Python text-processing libraries, the pipeline performed text normalization, stripped sensitive PII (phone numbers, email addresses, personal identifiers), applied sentence tokenization via **spaCy**, and calculated token lengths using `tiktoken`.

He enriched every document with structured metadata tags (candidate seniorities, primary skills, interview stages, timestamps, and interviewer IDs) before outputting clean, vectorized chunks into downstream knowledge stores. Over **50,000+ candidate interaction documents** were normalized and prepared, accelerating analytical query execution by **35%** and ensuring the RAG vector index remained pristine and hallucination-resistant."""
            },
            {
                "bullet_num": 5,
                "bullet_text": "Develops RAG and agent workflows using LangChain, LlamaIndex, MCP, and FastAPI, integrating retrieval and tooling to support AI applications.",
                "explanation": """To empower recruitment managers and technical interviewers with intelligent digital assistance in **Project CognitiveOps**, Rujuwal engineered an advanced **Multi-Agent Retrieval-Augmented Generation (RAG) System**. Rather than relying on naive single-prompt LLM wrappers, he designed an autonomous, tool-augmented multi-agent architecture utilizing **LangChain**, **LlamaIndex**, and **FastAPI**, orchestrated through stateful graph workflows.

The digital assistant was architected with specialized agent personas:
1. **Candidate Profile Specialist:** Queries **MongoDB** to extract historical candidate resumes, technical evaluation transcripts, and assessment scorecards.
2. **Policy & Compliance Specialist:** Performs hybrid search across internal company policy documents, salary band guidelines, and legal compliance manuals using **LlamaIndex** with dense vector retrieval (**HNSW**) and sparse keyword matching (**BM25**) fused via **Reciprocal Rank Fusion (RRF)**.
3. **Operational Scheduling Agent:** Interacts with internal calendaring and availability APIs to evaluate interviewer bandwidth and identify potential scheduling conflicts.

A critical innovation introduced by Rujuwal was the integration of the **Model Context Protocol (MCP)**. By implementing MCP servers, he standardized how the agent core discovered and invoked external operational tools over structured JSON-RPC transports. The agents dynamically invoked verified tools (e.g., `get_candidate_evaluation_summary`, `check_interviewer_capacity`, `query_salary_band`) using strict **Pydantic** JSON schemas, enforcing that the model never executed unauthorized actions.

Rujuwal exposed the entire multi-agent ecosystem through high-throughput, non-blocking asynchronous **FastAPI** microservice endpoints. He implemented **Server-Sent Events (SSE)** to stream intermediate agent reasoning thoughts (*'Searching candidate notes...'*, *'Cross-referencing salary benchmarks...'*) and final markdown responses in real time. Handling over **1,200+ daily employee inquiries**, the system achieved an average end-to-end response time of **under 1.8 seconds**, automating 40% of repetitive operational questions."""
            },
            {
                "bullet_num": 6,
                "bullet_text": "Supports AI quality and deployment via LangSmith tracing and evaluation, MLflow lifecycle management, and collaboration with DevOps.",
                "explanation": """Deploying generative AI into production environments demands rigorous observability, performance benchmarking, and continuous evaluation to prevent model drift, latency regressions, and factual hallucinations. In **Project CognitiveOps**, Rujuwal instituted an enterprise-grade AI evaluation and lifecycle management framework powered by **LangSmith**, **MLflow**, and **Docker**.

Rujuwal deeply instrumented all **FastAPI** agent endpoints with **LangSmith**, creating detailed distributed trace trees for every user interaction. The traces captured the entire cognitive lifecycle of the agents: user prompt inputs, intermediate reasoning chains, tool-call payload arguments, raw tool outputs, token usage counts, and execution latency at each graph node. Using LangSmith, Rujuwal established automated quantitative evaluation suites scoring 10% of daily production traces on core metrics:
- **Faithfulness:** Verifying that synthesized agent recommendations were mathematically grounded in retrieved interview notes.
- **Context Precision:** Measuring the signal-to-noise ratio of retrieved document chunks.
- **Answer Relevance:** Ensuring the assistant directly answered the recruiter's operational question without evasiveness.

Simultaneously, Rujuwal utilized **MLflow** for AI model and prompt lifecycle management. He tracked system prompt versions, temperature settings, chunking hyperparameters, and embedding model versions as tracked experiments, enabling data-driven comparisons before deploying prompt modifications.

Collaborating closely with the DevOps team, Rujuwal containerized the AI microservices using multi-stage **Docker** builds, optimized container image sizes, and implemented health check probes (`/healthz`, `/readyz`). He established automated CI/CD deployment pipelines in **GitHub Actions** that ran headless evaluation benchmarks before promoting new agent configurations to production. This engineering discipline slashed production hallucination rates by **35%**, cut token costs by **22%** through prompt compaction, and maintained **99.8% service uptime**."""
            },
            {
                "bullet_num": 7,
                "bullet_text": "Coordinates with external vendor partners, including Vizva Consultancy Services, and resolves cross-team scheduling issues spanning Technical, Marketing, and Sales teams.",
                "explanation": """Operationalizing **Project CognitiveOps** across a distributed corporate ecosystem required high-stakes stakeholder coordination, vendor management, and cross-functional conflict resolution. Rujuwal served as the primary technical and operational liaison between **SilverSpace** and external vendor partners, most notably **Vizva Consultancy Services**, which provided candidate pipelines and contracted technical interviewers. He established formal Service Level Agreements (**SLAs**), data interchange standards, and automated feedback loops, ensuring external partner feeds met enterprise quality benchmarks.

Internally, cross-functional dependencies frequently generated friction across three core departments with competing operational priorities:
- **Technical Team:** Focused on rigorous technical bar preservation, code review quality, and avoiding interviewer burnout.
- **Marketing Team:** Driving high-velocity candidate acquisition campaigns and demanding real-time conversion reporting.
- **Sales & Client Engagement Team:** Requiring immediate candidate interview availability to satisfy enterprise client staffing contracts.

When interview scheduling bottlenecks emerged—causing high-value client interviews to be delayed or cancelled due to panel shortages—Rujuwal intervened decisively. He developed an automated **Cross-Team Scheduling and Capacity Coordination System**. Built with **Python**, the script integrated with Google Calendar and Microsoft Graph APIs, dynamically monitoring technical interviewer availability across regional branches. 

He established an automated early-warning mechanism that flagged panel deficits 48 hours in advance, automatically alerting marketing to throttle candidate invitations for specific tech stacks while notifying technical leads to open emergency interview slots. Furthermore, Rujuwal chaired weekly cross-departmental alignment standups, resolving inter-team blockers, standardizing sprint priorities, and ensuring **100% of vendor escalation tickets** were resolved within agreed SLA windows. His diplomatic leadership cut interview rescheduling rates by **45%** and unified cross-team operations."""
            },
            {
                "bullet_num": 8,
                "bullet_text": "Builds and maintains Excel/SQL-based reporting workbooks to calculate, validate, and distribute monthly interview support incentive payout reports for the Tech Team across multiple locations.",
                "explanation": """In **Project CognitiveOps**, technical team members who conducted candidate screening interviews outside their standard development hours were entitled to financial performance incentives. Calculating these monthly incentive payouts was historically a high-friction, error-prone manual process: interview records were scattered across multiple geographical locations (Gurgaon, Delhi, and remote teams), with differing hourly compensation rates, weekend multipliers, candidate seniority tiers, and penalty deductions for late submission of evaluation feedback scorecards. Manual spreadsheet calculations caused payroll delays, audit disputes, and employee dissatisfaction.

Rujuwal engineered an end-to-end automated **Incentive Calculation, Validation, and Distribution Engine** combining **Azure SQL Database** stored procedures, **Python**, and dynamic **Excel workbooks**. 

The system operated through a robust four-stage architecture:
1. **Data Ingestion & Reconciliation:** An automated SQL ETL script ingested completed interview records, attendance logs, and interviewer feedback submission timestamps, joining them against the master employee location registry.
2. **Deterministic SQL Computation:** A parameterized stored procedure executed tiered calculation logic: applying base rates, weekend multipliers ($1.5\\times$), tier bonuses for Principal/Staff candidate evaluations, and automated deductions for evaluations submitted after the 24-hour SLA window.
3. **Cryptographic Validation & Quality Check:** An automated validation script reconciled aggregate payout sums against financial ledger allocations, verifying that zero duplicate interview sessions were counted and generating a cryptographic SHA-256 validation hash for auditing.
4. **Automated Workbook Distribution:** A **Python** script using **openpyxl** formatted the audited results into individual, password-protected executive Excel workbooks with clean summary pivot tables, dynamically dispatching them to regional HR and payroll finance teams.

Rujuwal's automated engine slashed incentive computation turnaround time from **5 full business days down to 2 hours**, achieved **100% payout calculation accuracy** across 12 consecutive monthly payroll cycles, and restored complete transparency to technical compensation."""
            }
        ]
    },

    # =========================================================================
    # COMPANY 2: SilverSpace Inc. | Data Analyst (Jun 2024 - May 2025)
    # =========================================================================
    {
        "company_id": "silverspace_analyst",
        "company_name": "SilverSpace Inc.",
        "role": "Data Analyst",
        "tenure": "Jun 2024 – May 2025",
        "location": "Gurgaon, India",
        "promotion_note": "Project: Recruitment KPI Automation & Cloud Migration - Vizva (a part of SilverSpace)",
        "project": {
            "name": "Project CloudTalent — Recruitment KPI Automation, Data Warehousing & Cloud Modernization",
            "tagline": "Enterprise Cloud Migration from Excel Spreadsheets to Azure Data Factory, Azure SQL & Power BI",
            "overview": """When Rujuwal joined Vizva (a division of SilverSpace), recruitment, sales, and candidate pipeline tracking were conducted entirely through decentralized, error-prone Excel spreadsheets. This caused version collisions, broken formulas, and over 15 hours of manual reporting toil every week. Rujuwal designed and executed **Project CloudTalent**, a phased enterprise cloud modernization initiative that migrated decentralized recruitment tracking to a centralized **Azure SQL Database** cloud data mart, automated data integration using **Azure Data Factory (ADF)** pipelines, and delivered interactive, self-service **Power BI** executive dashboards.""",
            "tech_stack": ["Azure SQL Database", "Azure Data Factory (ADF)", "Power BI", "DAX", "SQL", "Python", "Pandas", "Excel VBA / Advanced Macros", "Azure Blob Storage"]
        },
        "bullets": [
            {
                "bullet_num": 1,
                "bullet_text": "Reduced manual recruitment and sales reporting effort by 70% via a phased transition from Excel to Azure pipelines and Power BI dashboards.",
                "explanation": """Prior to Rujuwal's execution of **Project CloudTalent**, recruitment operations and sales performance reporting at Vizva depended heavily on manual spreadsheet compilation. Every Monday morning, analysts spent 6 to 8 hours extracting CSVs from applicant tracking systems, manually copying records into master workbooks, reconciling formula errors, and emailing static snapshot files to executives. This manual workflow introduced substantial reporting latency, human data-entry errors, and zero real-time visibility into hiring velocity.

Rujuwal formulated and executed a disciplined, three-phase cloud modernization roadmap:
- **Phase 1 (Process Stabilization & Formula Optimization):** He consolidated 14 disparate departmental spreadsheets into a standardized master schema, replacing fragile manual calculations with dynamic array formulas and automated VBA scripts to establish an immediate operational baseline.
- **Phase 2 (Cloud Ingestion & Data Warehousing):** He migrated the cleaned recruitment records into **Azure Blob Storage** and architected a relational star-schema data mart in **Azure SQL Database**, establishing automated **Azure Data Factory (ADF)** ETL pipelines that ingested daily candidate applications, interview events, and placement data.
- **Phase 3 (Enterprise BI Visualization):** He constructed self-service **Power BI** dashboards connected via scheduled cloud refreshes, deprecating local spreadsheet distribution entirely.
- **Phase 4 (Automated Auditing & SLA Verification):** He implemented automated data reconciliation checks that compared nightly Azure SQL row counts against source systems, ensuring that any missing records triggered automated email alerts before morning management meetings.

This cloud migration reduced manual recruitment and sales reporting effort by **70%**, freeing up approximately 12 analyst hours per week, while providing leadership with sub-minute, real-time access to operational metrics every morning at 8:00 AM."""
            },
            {
                "bullet_num": 2,
                "bullet_text": "Partnered with recruitment and sales teams to define outreach, interview success, and placement KPIs; automated initial calculations with Excel formulas and macros, decreasing manual updates by >50%.",
                "explanation": """Before engineering cloud data pipelines in **Project CloudTalent**, Rujuwal recognized that building technical infrastructure without domain alignment leads to user adoption failure. He embedded directly with frontline recruitment specialists, sourcing leads, and sales account managers to map their end-to-end candidate lifecycle workflows—from initial cold outreach and resume screening to client interviews, offer negotiations, and final placement confirmation.

Through these cross-functional working sessions, Rujuwal defined standardized, quantifiable operational metrics and governance KPIs:
- **Outreach Responsiveness Rate:** Percentage of sourced candidates who responded to initial outreach across email and LinkedIn channels.
- **Stage-to-Stage Interview Conversion Velocity:** Conversion ratios across Screening $\\to$ Technical Round $\\to$ Client Final Round.
- **Offer-to-Acceptance Ratio:** Percentage of extended job offers converted into signed client placements.
- **Recruiter Throughput:** Normalized monthly placements per active recruiter.
- **Cycle-Time Latency:** Average business days spent by candidates in each recruitment pipeline phase.

To deliver immediate operational relief while the Azure cloud data mart was being constructed, Rujuwal engineered an automated **Excel KPI Tracking Model**. He authored advanced dynamic array formulas using `XLOOKUP`, `INDEX/MATCH`, `LET`, and `LAMBDA` to eliminate repetitive lookups and formula bloating. He developed modular **VBA (Visual Basic for Applications) macros** that automated multi-tab workbook consolidation, validated candidate phone and email formats upon paste, performed automated fuzzy matching to catch duplicate candidate submissions against historical archives, handled runtime error trapping, and generated pre-formatted weekly summary executive tables at the click of a button.

This tactical automation decreased daily manual tracker updates by **>50%**, completely eliminated formula corruptions and broken links, and established the clean, validated data schema necessary for subsequent migration to Azure SQL Database."""
            },
            {
                "bullet_num": 3,
                "bullet_text": "Led recruitment data migration to Azure SQL Database and built Azure Data Factory ETL pipelines integrating candidate applications, interview schedules, and placement records into a centralized reporting source.",
                "explanation": """In the core execution phase of **Project CloudTalent**, Rujuwal took full ownership of data engineering and cloud warehousing. The legacy data landscape consisted of three disconnected operational silos: external job portal application logs, internal technical interview schedules stored in shared calendars, and financial placement billing records maintained by sales operations.

Rujuwal architected the target relational data warehouse in **Azure SQL Database**, designing an optimized dimensional star schema:
- **Dimension Tables:** `Dim_Candidate` (demographics, seniority, primary technical skillset), `Dim_Recruiter` (recruiter tier, branch location), `Dim_ClientCompany` (industry vertical, contract tier), and `Dim_Calendar` (fiscal weeks, quarters, holidays).
- **Fact Tables:** `Fact_CandidateOutreach` (outreach channel, timestamp, response flag), `Fact_InterviewSchedule` (round number, interviewer ID, outcome score), and `Fact_Placement` (placement date, bill rate, fee revenue).

To automate data movement, Rujuwal engineered robust **Azure Data Factory (ADF)** pipelines. Utilizing Mapping Data Flows, the pipelines extracted raw daily data dumps from **Azure Blob Storage**, performed deduplication using MD5 row hash comparisons, executed surrogate key lookups, and loaded clean records into Azure SQL using high-throughput bulk copy (`bcp`) operations. He integrated **Change Data Capture (CDC)** logic to capture status updates (e.g., candidate moving from 'Interview Scheduled' to 'Offer Extended') without full table reloads, and configured automated **Azure Monitor** alerts notifying the team via email if pipeline execution encountered network timeouts or schema validation errors.

Furthermore, he authored automated pre-load validation scripts in **SQL** ensuring foreign key referential integrity across all transactional staging tables. This pipeline unified over **200,000+ historical recruitment transaction records** into a single, high-performance golden source of truth."""
            },
            {
                "bullet_num": 4,
                "bullet_text": "Built interactive Power BI dashboards for daily and weekly outreach, funnel conversion, and recruitment cycle time, enabling managers to compare performance and identify process bottlenecks.",
                "explanation": """With the centralized Azure SQL data warehouse in place, Rujuwal developed an enterprise **Power BI** reporting suite in **Project CloudTalent**, transforming raw transaction tables into dynamic, visual operational intelligence for practice leads, recruitment managers, and C-level executives.

He authored a multi-page dashboard suite featuring:
- **Daily Outreach & Sourcing Command Center:** Visualized daily outreach volume, candidate channel yield, and recruiter activity quotas, enabling team leads to balance daily sourcing workloads.
- **Full-Funnel Conversion Analytics:** Interactive funnel visualizations depicting candidate attrition at each stage of the recruitment process. The report allowed managers to slice data by technology stack (e.g., Java vs. Data Engineering vs. Cloud), candidate seniority, and client account.
- **Recruitment Cycle Time & Velocity Tracker:** Measured the exact duration in days that candidates remained in each hiring stage, highlighting operational stagnation.

To maximize usability and performance, Rujuwal implemented advanced Power BI UX features: bookmark-based navigation, drill-through capabilities allowing managers to click on a high-level branch metric and view the exact list of stalled candidates, and dynamic measure switching using DAX disconnected slicer tables. He optimized model performance by pre-aggregating historical years in Azure SQL and configuring **Composite Storage Mode**, ensuring all dashboard pages rendered in **under 1.2 seconds**.

Critically, the funnel dashboard uncovered a major hidden bottleneck: candidates in technical interview stages experienced an average **9-day latency** between Round 1 and Round 2, during which candidate drop-off spiked by **22%**. Armed with this insight, leadership instituted a 48-hour interview turnaround policy, directly improving placement conversion velocity by **18%**."""
            },
            {
                "bullet_num": 5,
                "bullet_text": "Analyzed recruitment channels, candidate segments, and outreach frequency to identify drop-off patterns and guide targeting and engagement strategies.",
                "explanation": """Beyond building descriptive dashboards in **Project CloudTalent**, Rujuwal conducted rigorous diagnostic and exploratory data analysis using **Python (Pandas, NumPy, Matplotlib, Seaborn)** and **SQL** to uncover the behavioral drivers of candidate engagement and pipeline drop-off. 

He analyzed historical interaction logs across 35,000 candidate records spanning four primary sourcing channels: LinkedIn InMail, direct job board applications, employee referrals, and internal talent pool re-engagement. He segmented the candidate pool across multiple dimensions: years of experience, technical specialization, geographic location, and message outreach cadence.

Using cohort analysis and statistical correlation techniques, Rujuwal evaluated:
- **Channel Yield vs. Quality:** Discovered that while job board postings generated the highest initial volume, employee referral candidates converted to final client placement at **3.2x the rate** of cold applicants and had a 40% shorter recruitment cycle time.
- **Outreach Latency Impact:** Calculated response decay curves, demonstrating that recruiters who followed up with interested candidates within **48 hours** achieved a **64% higher response rate** compared to recruiters who waited 5 days or longer.
- **Candidate Fatigue Thresholds:** Found that exceeding 3 follow-up messages within a 10-day window increased candidate unsubscribe and blocking rates by 300% without increasing conversions.

Rujuwal synthesized these empirical findings into an executive presentation and actionable recruitment playbook. He advised leadership to reallocate 30% of job board ad budgets into an expanded employee referral bonus program, and established automated CRM task reminders enforcing 48-hour candidate follow-up SLAs. These data-driven optimizations compressed the average recruitment cycle time from **42 days down to 28 days**."""
            }
        ]
    },

    # =========================================================================
    # COMPANY 3: Vaco Binary Semantics LLP | Associate Data Analyst (Jul 2022 - Jun 2024)
    # =========================================================================
    {
        "company_id": "vaco_google",
        "company_name": "Vaco Binary Semantics LLP",
        "role": "Associate Data Analyst - Google Hotel Ads Project",
        "tenure": "Jul 2022 – Jun 2024",
        "location": "Gurgaon, India",
        "promotion_note": "High-Frequency Ad Auction Telemetry, Bid Intelligence & Regional Pricing Optimization for Google Hotel Ads",
        "project": {
            "name": "Project BidOptima — High-Frequency Hotel Ad Auction Analytics, BigQuery Optimization & Price Parity Diagnostics",
            "tagline": "Large-Scale SQL Performance Optimization, Serverless GCP Ingestion, and Multi-Market A/B Bid Intelligence",
            "overview": """Working on the global Google Hotel Ads engagement at Vaco Binary Semantics, Rujuwal was responsible for analyzing massive ad auction bid telemetry, inventory pricing feeds, click-through performance, and partner booking conversions across 2,000+ international hotel partners. He optimized complex analytical SQL queries running on multi-million row datasets, engineered automated serverless ingestion pipelines on Google Cloud Platform (GCP) and BigQuery, maintained multi-market executive dashboards in Looker Studio and Tableau across 4 continental regions, and executed statistical A/B tests to optimize ad bid strategies and diagnose pricing discrepancies.""",
            "tech_stack": ["Google BigQuery", "Google Cloud Platform (GCP)", "Google Cloud Storage (GCS)", "Cloud Functions", "Python", "SQL", "Looker Studio", "Tableau", "Pandas", "Statistical A/B Testing"]
        },
        "bullets": [
            {
                "bullet_num": 1,
                "bullet_text": "Reduced query execution time by 40% by optimizing SQL joins, aggregations, and subqueries across hotel and pricing datasets.",
                "explanation": """In **Project BidOptima**, the Google Hotel Ads analytical database processed hundreds of millions of daily ad auction bids, partner price feeds, impression events, and user booking conversions. Analysts and automated reporting jobs frequently executed large, complex SQL queries across tables exceeding 20 million rows. However, legacy queries were plagued by severe performance anti-patterns: correlated subqueries inside `WHERE` clauses, Cartesian product cross-joins, non-SARGable string manipulation functions applied directly to filtered columns, and heavy full table scans. Analytical queries took 8 to 15 minutes to run, exhausting BigQuery execution slots and driving up compute query costs.

Rujuwal conducted systematic query execution profiling using `EXPLAIN ANALYZE` and BigQuery execution plan execution trees. He engineered an enterprise query optimization strategy:
- **Refactoring Query Logic:** Replaced correlated subqueries with modular Common Table Expressions (**CTEs**) and efficient `INNER JOIN` / `LEFT JOIN` operations with explicit join keys.
- **Window Function Optimization:** Replaced multiple self-joins with analytical window functions (`ROW_NUMBER() OVER(PARTITION BY hotel_id, checkin_date ORDER BY crawl_timestamp DESC)`) to extract the latest pricing snapshot in a single pass.
- **Partitioning & Clustering Strategy:** Re-engineered target tables in **Google BigQuery** to utilize day-based partitioning on `auction_date` combined with multi-column clustering on `hotel_id` and `market_region`. This ensured query filters on specific dates and hotels scanned only the target partition blocks rather than the entire 20M+ row dataset.
- **Materialized Pre-Aggregations:** Built incremental scheduled queries that pre-aggregated raw hourly click telemetry into daily summary tables.

These architectural optimizations slashed average query execution times by **40%**, reduced BigQuery scanned data bytes by **55%**, and saved significant cloud compute costs."""
            },
            {
                "bullet_num": 2,
                "bullet_text": "Automated Google Cloud ingestion and validation, reducing turnaround from 3 hours to 40 minutes, saving 8 hours of manual reporting per week.",
                "explanation": """Prior to Rujuwal's automation in **Project BidOptima**, ingesting hotel partner inventory feeds and auction telemetry was a cumbersome, semi-manual process. Every morning, hotel partners uploaded compressed data files (gzip CSVs and nested JSON feeds) into **Google Cloud Storage (GCS)** buckets. Analysts had to manually trigger local download scripts, inspect files for corrupt headers or encoding errors, execute local Python transformation scripts, and upload the processed records into **Google BigQuery**. This manual ritual took **3 hours every morning**, delayed executive reporting, and consumed over 8 hours of manual engineering effort per week.

Rujuwal designed and deployed a serverless, event-driven automated ingestion and validation pipeline on **Google Cloud Platform (GCP)**:
1. **Event-Driven Trigger:** Configured GCS Pub/Sub bucket notifications that automatically published an event whenever a new partner feed landed in the storage bucket.
2. **Serverless Transformation via Cloud Functions:** Deployed an asynchronous **Python Cloud Function** (and Cloud Run container for oversized files) triggered by the Pub/Sub event. The function streamed compressed files directly into memory, unzipped feeds, and executed automated schema validation using **Pandas**.
3. **Automated Data Quality Assurance:** The Python script inspected mandatory columns, validated numerical pricing ranges (flagging impossible values like negative room rates or $0 luxury suites), checked ISO currency codes, and stripped corrupted characters.
4. **Automated BigQuery Loading:** Valid records were streamed directly into partitioned **BigQuery** staging tables, while malformed records were routed into a Dead-Letter quarantine table with automated error alerts dispatched to partner integration teams.

This automated pipeline compressed daily data turnaround time from **3 hours down to 40 minutes** (a 78% reduction), eradicated human data-entry error, and saved the team **8 hours of manual toil per week**."""
            },
            {
                "bullet_num": 3,
                "bullet_text": "Supported 6 reporting streams and built Looker Studio dashboards across 4 regional markets, translating stakeholder requirements into tracked KPIs and Tableau reporting.",
                "explanation": """In **Project BidOptima**, managing analytics for Google Hotel Ads required navigating immense regional diversity across **4 global continental markets**: North America (NA), Europe/Middle East/Africa (EMEA), Asia-Pacific (APAC), and Latin America (LATAM). Each geographic market operated under distinct competitive dynamics, differing currency conversions, and complex tax inclusion regulations (e.g., VAT-inclusive pricing mandated in European markets versus post-tax pricing models prevalent in North America).

Rujuwal served as the analytical owner supporting **6 distinct reporting streams**, collaborating directly with global partner account managers, ad product specialists, and technical leads. He translated regional business goals into tracked digital advertising KPIs:
- **Impression Share & Win Rate:** Percentage of ad auction impressions won against competing Online Travel Agencies (OTAs).
- **Click-to-Book Conversion Rate (CVR):** Efficiency of ad traffic in driving confirmed room reservations.
- **Average Daily Rate (ADR) & RevPAR:** Hotel pricing benchmarks reflecting seasonal revenue yield and room inventory value.
- **Effective Cost-per-Click (eCPC) & Return on Ad Spend (ROAS):** Direct financial efficiency metrics guiding partner marketing budgets.
- **Price Competitiveness Index:** Ratio of partner pricing relative to lowest competitor rates across metasearch results.

To visualize these metrics, Rujuwal architected interactive **Looker Studio** and **Tableau** dashboards connected directly to optimized **BigQuery** analytical views. He built parameter-driven currency toggles allowing global directors to view metrics in normalized USD or local currencies (EUR, GBP, JPY), dynamic date range comparators, and regional drill-downs from continental aggregates down to individual hotel property IDs.

These 6 reporting streams delivered mission-critical visibility to international stakeholders, directly informing weekly ad bid adjustments and multimillion-dollar quarterly partner marketing spend allocations across **4 regional markets**."""
            },
            {
                "bullet_num": 4,
                "bullet_text": "Investigated pricing, tax, and data-quality issues across 2,000+ hotel datasets using segmentation and root-cause analysis; conducted A/B performance analysis to support bid optimization.",
                "explanation": """In Google Hotel Ads, maintaining strict **Price Parity** is paramount. When an ad displays a room rate of $150 on Google search results, but the user clicks through to the partner booking engine and encounters a price of $175 due to hidden fees, tax miscalculations, or stale cache feeds, Google’s auction algorithm penalizes the partner with lower Quality Scores and reduced ad rank. Rujuwal took ownership of investigating pricing accuracy, tax compliance, and data-quality anomalies across **2,000+ partner hotel properties**.

Rujuwal engineered diagnostic **Python** and **SQL** reconciliation scripts that crawled partner landing page APIs and compared displayed rates against Google’s internal auction cache in BigQuery. Performing cohort segmentation across partner technical integration types (API push vs. scheduled pull feeds), geographic regions, and hotel chain tiers, he conducted deep-dive **Root-Cause Analysis (RCA)**. He uncovered two major systemic bugs:
1. European partners were omitting local city tourist occupancy taxes from their base feed payloads, causing systematic checkout price mismatches.
2. High-frequency currency rounding discrepancies between Euro and British Pound conversions in regional payment gateways.

Furthermore, Rujuwal designed, monitored, and evaluated **A/B Performance Testing Experiments** to support algorithmic bid optimization. He partitioned candidate hotel inventories into randomized control groups (bidding with legacy static floor pricing) and experimental treatment groups (utilizing dynamic, automated bidding multipliers based on predicted conversion rates). He evaluated results using two-sample hypothesis testing ($t$-tests, Mann-Whitney $U$ tests), measuring statistically significant improvements in Click-Through Rates (CTR) and ROAS.

His investigations and A/B analyses remediated pricing defects across **150+ major hotel chains**, elevated price accuracy compliance to **99.1%**, and drove a **12% statistically significant increase in partner booking conversions**."""
            }
        ]
    },

    # =========================================================================
    # COMPANY 4: Profitmart | Data Analyst Intern (Jan 2022 - May 2022)
    # =========================================================================
    {
        "company_id": "profitmart_intern",
        "company_name": "Profitmart",
        "role": "Data Analyst Intern",
        "tenure": "Jan 2022 – May 2022",
        "location": "Gurgaon, India",
        "promotion_note": "Financial Brokerage, Customer Trading Telemetry & Account Retention Analytics",
        "project": {
            "name": "Project TradePulse — Customer Trading Telemetry, Account Activity Modeling & Reporting Automation",
            "tagline": "Exploratory Data Analysis, Data Cleaning Pipelines, and Financial Performance Analytics",
            "overview": """During his internship at Profitmart, a retail financial brokerage firm, Rujuwal established his core data engineering and analytical foundations. He worked on Project TradePulse, analyzing customer trading volumes, account churn indicators, margin call occurrences, and brokerage fee revenues across retail investor accounts to uncover behavioral patterns and support executive reporting.""",
            "tech_stack": ["Python", "Pandas", "NumPy", "SQL", "MySQL", "Excel", "Data Cleansing", "Exploratory Data Analysis"]
        },
        "bullets": [
            {
                "bullet_num": 1,
                "bullet_text": "Built Python and SQL data preparation workflows and performed exploratory analysis with Pandas and NumPy to spot trends and performance patterns.",
                "explanation": """In **Project TradePulse**, Profitmart's operational leadership required clear analytical visibility into customer trading behavior, active brokerage account engagement, order fill latencies, and revenue generation patterns across retail equity, commodities, and derivatives traders. Transactional trade records were distributed across production **MySQL** relational databases, containing millions of rows of trade timestamps, client IDs, order types (market vs. limit), traded volume, leverage ratios, and executed commission fees.

Rujuwal engineered robust **Python** and **SQL** data preparation workflows to extract, clean, and analyze this financial telemetry:
- **Data Preparation Pipelines:** He authored parameterized SQL queries extracting customer trading activity over 12-month rolling windows, utilizing inner joins, common table expressions (CTEs), and group-by aggregations across account master tables and trade ledger databases. In Python, he utilized **Pandas** and **NumPy** to vectorize calculations, handle timestamps with timezone normalizations, compute customer-level summary aggregates (average trade frequency, monthly trading turnover, net brokerage fee contribution, win-loss ratios), and stage clean, analysis-ready datasets.
- **Exploratory Data Analysis (EDA):** Rujuwal conducted rigorous EDA to uncover hidden behavioral trends and customer concentration risks. By computing statistical summary distributions (means, medians, standard deviations, interquartile ranges, skewness, and percentiles), he identified that active trading volume followed an extreme Pareto distribution—the top 8% of active intraday traders accounted for **62% of total brokerage commission revenue**.
- **Trend Identification & Churn Signaling:** He analyzed customer retention curves and trading dormancy, discovering a distinct drop-off threshold: accounts that suffered consecutive margin call liquidations within their first 14 days had an **82% probability of abandoning the platform** within 60 days.

Rujuwal compiled these insights into structured executive analytical decks and interactive Jupyter notebooks, recommending personalized risk management notifications and automated stop-loss educational prompts for novice traders to improve platform retention and long-term active trading lifetime value."""
            },
            {
                "bullet_num": 2,
                "bullet_text": "Cleaned missing values and duplicates, validated datasets, and supported stakeholder reporting with SQL and Excel.",
                "explanation": """In financial brokerage databases, raw transactional datasets are frequently afflicted by data hygiene anomalies resulting from network timeouts, duplicate order submissions, and unpopulated demographic fields in legacy account opening forms. In **Project TradePulse**, dirty data distorted executive reporting, leading to miscalculations of customer acquisition costs and net active trading accounts.

Rujuwal took ownership of developing systematic **Data Cleaning and Validation Protocols**:
- **Missing Value Imputation:** Using **Python (Pandas)**, he analyzed missing value patterns across demographic and financial attributes. For non-critical missing numeric features (such as customer annual income brackets), he applied median and mode imputation segmented by age and location cohorts. For critical transactional fields (such as execution trade prices), he authored SQL scripts that reconciled missing entries against exchange master trade logs.
- **Deduplication:** He constructed SQL deduplication logic using window functions (`ROW_NUMBER() OVER(PARTITION BY order_id, client_code, trade_timestamp ORDER BY execution_id DESC)`), safely identifying and excising duplicate transaction records generated during high-concurrency order placement retries.
- **Dataset Validation:** He authored SQL assertion scripts verifying financial reconciliation constraints—asserting that net traded amounts equaled gross volume minus applicable exchange transaction charges and statutory taxes.
- **Stakeholder Reporting Automation:** Rujuwal built dynamic, structured executive summary workbooks in **Microsoft Excel**. Using pivot tables, conditional formatting, dynamic charts, and automated lookup formulas, he provided branch heads and sales managers with daily trading turnover summaries, active trader counts, and commission revenue breakdowns.

His meticulous data cleaning eradicated duplicate trade errors, established verifiable audit trails, and delivered verified, auditable datasets that underpinned all operational reporting at Profitmart."""
            }
        ]
    }
]

# Additional Projects & Academic Foundations
selected_projects_data = [
    {
        "title": "Customer Churn Analysis & Retention Strategy",
        "tech_stack": ["Power BI", "DAX", "Python", "Scikit-learn", "Statistical Modeling"],
        "overview": """Engineered an end-to-end diagnostic churn prediction and root-cause analysis model in **Power BI** and **Python**. Analyzed customer behavioral telemetry across service ticket history, transactional frequency, contract tenure, and net promoter scores. Identified that clients experiencing more than 2 unresolved technical support tickets within their first 30 days exhibited an **85% higher churn probability**. Developed dynamic DAX measures and executive retention dashboards that enabled customer success teams to deploy proactive retention interventions, contributing to a **15% reduction in customer churn** and a **10% increase in long-term customer loyalty**."""
    },
    {
        "title": "E-commerce Operations Analysis – Target Brazil (100K Orders)",
        "tech_stack": ["Python", "Pandas", "NumPy", "SQL", "Logistics Optimization", "Seaborn"],
        "overview": """Conducted a comprehensive operational analytics study on a public dataset of 100,000 e-commerce orders across Brazilian states, integrating customer geolocation, installment payment methods, delivery carrier routes, and freight costs. Discovered that delivery delays in northern and northeastern regions were primarily driven by carrier route consolidation rather than warehouse fulfillment bottlenecks. Provided predictive delivery window estimation models and freight pricing optimization frameworks that reduced customer delivery complaint escalations by **25%**."""
    }
]
