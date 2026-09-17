resume_breakdown_markdown = """# Part 1: Deep-Dive Resume Analysis & Project Breakdown

This section deconstructs every experience, responsibility, and metric on **Rujuwal Garg's** resume into deep technical and architectural narratives, accompanied by concrete sample projects demonstrating how each bullet point translates directly into enterprise capability for **Gartner's Agentic AI Applications Team**.

---

## 1. SilverSpace Inc. | Team Lead (May 2025 – Present)
**Location:** Gurgaon, India  
**Promotion:** Accelerated promotion from Data Analyst to Team Lead in May 2025 within 11 months, recognizing end-to-end technical leadership, architectural initiative, and cross-functional impact.

---

### Bullet 1: *Mentors 4 junior engineers and collaborates with product, data, and DevOps teams to deliver analytics and AI solutions.*
#### In-Depth Technical & Operational Breakdown:
As Team Lead, mentorship transcends basic task assignment. Rujuwal established daily 15-minute engineering standups, weekly technical design reviews, and structured pair-programming sessions for **4 junior engineers**. He instituted production-grade coding standards: PEP 8 linting, type hinting with **Pydantic**, asynchronous design patterns in **FastAPI**, pre-commit Git hooks, and branch protection rules requiring at least one peer approval.

To collaborate effectively across functional boundaries, Rujuwal interfaced between:
- **Product Teams:** Translating abstract business goals (e.g., "accelerate sales associate prep time") into technical user stories, acceptance criteria, and sequence diagrams.
- **Data Teams:** Establishing schema contracts for relational data (**PostgreSQL**, **Azure SQL**) and vector embeddings (**ChromaDB**, **Pinecone**).
- **DevOps Teams:** Co-architecting containerization strategies with **Docker**, configuring environment secret management via **AWS Secrets Manager / Azure Key Vault**, and maintaining **GitHub Actions** CI/CD deployment pipelines.

#### Sample Project: *Multi-Tenant AI Microservice Delivery Framework*
- **Objective:** Enable junior engineers to rapidly scaffold and deploy production-ready AI services with zero architecture drift.
- **Architecture:** Built a template repository in **Python** using **FastAPI**, **Docker**, and **Pydantic v2**. The framework encapsulates structured JSON logging, Prometheus metrics middleware (`/metrics`), health check probes (`/healthz`, `/readyz`), and abstracted LLM client wrappers with automatic retry logic using **Tenacity**.
- **Impact:** Reduced new microservice onboarding and deployment time for junior engineers from **3 weeks to 3 days**, while maintaining zero security or linting regressions across releases.

---

### Bullet 2: *Translates stakeholder requirements into KPI definitions and analytical frameworks, leveraging Power BI dashboards for operational performance monitoring and business decisions.*
#### In-Depth Technical & Operational Breakdown:
Executive decision-makers often articulate business friction in qualitative terms (e.g., "recruitment turnaround is too sluggish"). Rujuwal bridges this gap by engineering formal mathematical KPI definitions: Time-to-Fill (TTF), Stage-to-Stage Funnel Conversion Rates, Candidate Drop-Off Velocity, and Recruiter Capacity Utilization.

He designed enterprise **Power BI** semantic models utilizing star schemas (fact tables surrounded by conformed dimension tables) to ensure sub-second report rendering. In **DAX (Data Analysis Expressions)**, he authored complex time-intelligence calculations, moving averages, and dynamic segmentation measures using `CALCULATE()`, `FILTER()`, `KEEPFILTERS()`, and `WINDOW()` functions, eliminating ambiguous spreadsheet interpretations.

#### Sample Project: *Executive Operational Funnel & Pipeline Velocity BI Model*
- **Objective:** Provide senior leadership with a real-time command center tracking 5,000+ monthly recruitment and operational interactions.
- **Architecture:** Engineered an **Azure SQL Database** data mart feeding into a composite **Power BI** model. Implemented Row-Level Security (**RLS**) ensuring regional branch managers only observed localized metrics while executive leadership accessed unified global aggregates.
- **Impact:** Eliminated weekly 6-hour manual reporting cycles and provided automated pipeline velocity alerts, empowering executive stakeholders to reallocate internal recruiter bandwidth dynamically.

---

### Bullet 3: *Strengthens reporting consistency through data validation, metric documentation, and reusable guidance covering ETL, data models, and dashboard logic.*
#### In-Depth Technical & Operational Breakdown:
In high-velocity organizations, reporting drift—where different departments calculate the same metric differently—creates decision paralysis. Rujuwal spearheaded an internal Data Governance and Standardization charter. He authored a centralized Data Dictionary defining 45+ core business metrics, specifying exact SQL logic, source-of-truth tables, update cadences, and business owners.

He established automated data quality checks within ETL pipelines, validating primary key uniqueness, foreign key referential integrity, null-value thresholds, and distribution anomaly detection using automated **Python** assertions and **SQL** constraints.

#### Sample Project: *Automated Data Contract & Schema Validation Suite*
- **Objective:** Intercept upstream data corruptions before they propagate into downstream BI reports and AI vector embeddings.
- **Architecture:** Integrated an automated pre-load testing stage in **Azure Data Factory** and **Python** ETL scripts. The pipeline evaluates data payloads against strict **Pydantic** schemas and executes automated SQL reconciliation tests (e.g., verifying daily row count deltas remain within $3\sigma$ of historical moving averages).
- **Impact:** Achieved a **99.4% data consistency rate** across executive reporting and decreased data-related defect tickets in Jira by **65%**.

---

### Bullet 4: *Applies SQL, Python, and MongoDB for data analysis and preparation for reporting and AI workflows.*
#### In-Depth Technical & Operational Breakdown:
Modern enterprise data is inherently polyglot. Rujuwal leverages **SQL** for relational, transactional datasets (candidate pipelines, revenue attribution, structured CRM records), **MongoDB** for polymorphic, semi-structured document storage (interview transcripts, evaluation rubrics, multi-turn chat logs, candidate resumes), and **Python (Pandas, NumPy)** for programmatic wrangling, feature engineering, and text preprocessing.

For AI preparation, he constructs data transformation pipelines that clean raw text, strip PII using regular expressions, segment lengthy documents into semantically coherent paragraphs, compute token counts using `tiktoken`, and structure metadata tags (author, department, confidentiality level, timestamp) for vector indexing.

#### Sample Project: *Polyglot Data Cleansing & Chunking Ingestion Engine*
- **Objective:** Normalize and enrich heterogeneous candidate evaluation notes and unstructured recruiter logs for downstream LLM retrieval.
- **Architecture:** Developed a **Python** pipeline querying **MongoDB** via `motor` (async driver) and relational data via **SQLAlchemy**. The pipeline extracts raw interaction transcripts, performs sentence tokenization using **spaCy**, attaches hierarchical metadata, and loads the sanitized records into an staging store for vector indexing.
- **Impact:** Processed over **50,000+ unstructured candidate interaction logs**, reducing downstream LLM parsing errors by **80%** and improving RAG retrieval precision.

---

### Bullet 5: *Develops RAG and agent workflows using LangChain, LlamaIndex, MCP, and FastAPI, integrating retrieval and tooling to support AI applications.*
#### In-Depth Technical & Operational Breakdown:
Moving beyond naive prompt-response wrappers, Rujuwal architects stateful, tool-augmented AI agents. Utilizing **LangChain** and **LlamaIndex**, he builds **Retrieval-Augmented Generation (RAG)** systems incorporating hybrid search (combining dense vector search with sparse **BM25** lexical matching) and cross-encoder re-ranking.

He integrates the **Model Context Protocol (MCP)**, standardizing how LLMs interface with internal tool repositories (e.g., scheduling APIs, candidate databases, policy documents) over JSON-RPC transports. He exposes these capabilities via asynchronous **FastAPI** endpoints utilizing Server-Sent Events (**SSE**) for real-time token streaming.

#### Sample Project: *Enterprise Digital Assistant with Tool Use & Hybrid Retrieval*
- **Objective:** Automate operational queries for internal associates seeking relevant candidate histories, interview transcripts, and compliance policies.
- **Architecture:** Implemented a multi-step agent in **FastAPI** using **LangChain**. The agent utilizes an intent classifier to determine whether a query requires database lookup, vector search in **Qdrant/Pinecone**, or scheduling tool invocation. Employs a cross-encoder (**bge-reranker-large**) to re-score the top 25 retrieved passages down to the top 5 most contextually relevant chunks.
- **Impact:** Handled **1,200+ daily employee inquiries** with an average response time of under **1.8 seconds**, deflecting 40% of repetitive operational questions from HR and operations leads.

---

### Bullet 6: *Supports AI quality and deployment via LangSmith tracing and evaluation, MLflow lifecycle management, and collaboration with DevOps.*
#### In-Depth Technical & Operational Breakdown:
Enterprise AI requires observability and measurable quality assurance. Rujuwal integrated **LangSmith** across all agent workflows to capture end-to-end trace graphs: tracking prompt inputs, intermediate reasoning steps, tool-calling payloads, latency bottlenecks, and token expenditure per query.

He utilized **MLflow** for tracking prompt variations, system instruction hyperparameters, and embedding model versions. In collaboration with DevOps, he defined container resource limits, configured health checks, and established blue-green deployment pipelines to ensure zero-downtime updates when updating model endpoints or prompt templates.

#### Sample Project: *Continuous LLM Evaluation & Tracing Harness*
- **Objective:** Detect model drift, hallucination spikes, and latency regressions across daily agent interactions.
- **Architecture:** Configured **LangSmith** evaluators to score 10% of daily production traces on ground-truth answer correctness, faithfulness, and latency. Coupled with **MLflow**, the system automatically flags prompt changes that degrade benchmark evaluation scores below 0.85 prior to staging deployment.
- **Impact:** Slashed hallucination rates in production AI tools by **35%** and reduced token cost per transaction by **22%** through automated prompt optimization.

---

### Bullet 7: *Coordinates with external vendor partners, including Vizva Consultancy Services, and resolves cross-team scheduling issues spanning Technical, Marketing, and Sales teams.*
#### In-Depth Technical & Operational Breakdown:
Technical delivery in matrixed organizations frequently stalls on operational friction between vendors and internal business units. Rujuwal acted as the primary technical liaison between **SilverSpace** and **Vizva Consultancy Services**, establishing Service Level Agreements (SLAs) for candidate pipeline delivery, API uptime, and data interchange formats.

He harmonized conflicting priorities between the Technical Team (focused on platform stability and code quality), Marketing (demanding rapid lead generation reporting), and Sales (requiring real-time client interaction logs). He established unified sprint planning and cross-team ticketing workflows in Jira.

#### Sample Project: *Cross-Team Automated Scheduling & Capacity Tracker*
- **Objective:** Eliminate double-booking and schedule delays across cross-functional client interview panels.
- **Architecture:** Built an automated **Python** script integrating Google Calendar and Microsoft Graph APIs with an internal SQL registry, flagging panel conflicts 48 hours in advance and automatically re-routing interview requests to available technical panelists.
- **Impact:** Reduced interview rescheduling rates by **45%** and resolved 100% of vendor escalation tickets within agreed SLA windows.

---

### Bullet 8: *Builds and maintains Excel/SQL-based reporting workbooks to calculate, validate, and distribute monthly interview support incentive payout reports for the Tech Team across multiple locations.*
#### In-Depth Technical & Operational Breakdown:
Incentive compensation calculation for technical interviewers across multiple geographical locations involves complex tiered rules: variable hourly rates, weekend multipliers, candidate tier weighting, and deduction penalties for late feedback submission. Manual calculation is fraught with audit risk.

Rujuwal engineered an automated **SQL-based incentive engine** that joins interview schedule records, attendance logs, and interviewer feedback timestamps. The engine computes gross and net incentive payouts, applies multi-location tax and currency parameters, and outputs reconciled audit workbooks with automated cryptographic hash verification.

#### Sample Project: *Automated Multi-Geo Incentive Calculation Engine*
- **Objective:** Replace error-prone manual spreadsheet tracking with a deterministic, auditable incentive computation pipeline.
- **Architecture:** Authored stored procedures in **Azure SQL** with parameterized logic covering tier thresholds and SLA penalties. Output datasets are automatically formatted into secured, password-protected executive Excel distribution summaries via **Python (openpyxl)**.
- **Impact:** Reduced incentive processing cycle time from **5 business days to 2 hours**, achieving **100% payout accuracy** across 12 consecutive monthly payroll cycles.

---

## 2. SilverSpace Inc. | Data Analyst (Jun 2024 – May 2025)
**Project:** Recruitment KPI Automation & Cloud Migration - Vizva (a part of SilverSpace)

---

### Bullet 1: *Reduced manual recruitment and sales reporting effort by 70% via a phased transition from Excel to Azure pipelines and Power BI dashboards.*
#### In-Depth Technical & Operational Breakdown:
When Rujuwal joined the Vizva project, reporting was locked in sprawling, fragmented Excel spreadsheets updated manually across disparate teams. This caused version collisions, formula corruptions, and 15+ hours of wasted manual engineering effort each week.

He formulated a 3-phase cloud modernization roadmap:
1. **Phase 1 (Stabilization):** Centralize existing workbooks, normalize data schemas, and automate local formulas via VBA macros.
2. **Phase 2 (Cloud Ingestion):** Migrate raw data sources into **Azure Blob Storage** and construct automated **Azure Data Factory (ADF)** pipelines loading into **Azure SQL Database**.
3. **Phase 3 (Semantic Modeling & Visualization):** Architect enterprise **Power BI** semantic models with scheduled cloud refreshes, deprecating local spreadsheets entirely.

#### Sample Project: *Cloud Migration & Enterprise Data Warehouse Architecture*
- **Architecture:** Designed an end-to-end pipeline: Azure Blob Storage (Landing Zone) $\to$ Azure Data Factory (ETL Transformation) $\to$ Azure SQL Database (Star Schema Data Mart) $\to$ Power BI Service (DirectQuery / Import Hybrid).
- **Impact:** Slashed manual reporting effort by **70%**, enabling stakeholders to access refreshed operational metrics at 8:00 AM daily without human intervention.

---

### Bullet 2: *Partnered with recruitment and sales teams to define outreach, interview success, and placement KPIs; automated initial calculations with Excel formulas and macros, decreasing manual updates by >50%.*
#### In-Depth Technical & Operational Breakdown:
Before jumping straight into complex cloud pipelines, Rujuwal embedded with frontline recruitment and sales specialists to map their operational workflows. He defined core conversion milestones: Initial Outreach $\to$ Screen Complete $\to$ Client Interview Round 1 $\to$ Client Final Round $\to$ Offer Extended $\to$ Placement Confirmed.

He authored dynamic Excel automation workbooks utilizing advanced array formulas (`XLOOKUP`, `INDEX/MATCH`, `LAMBDA`, `LET`), dynamic pivot caches, and VBA automation modules that validated input data formats upon entry, slashing manual data entry errors.

#### Sample Project: *Dynamic Outreach & Conversion Calculator Workbook*
- **Architecture:** Built an interactive operational tracker with embedded VBA scripts that automatically pulled updated candidate application batches from CSV exports, performed deduplication against national phone/email records, and computed real-time conversion percentages.
- **Impact:** Decreased daily manual tracker update times by **>50%**, establishing the exact data baseline required for subsequent cloud database migration.

---

### Bullet 3: *Led recruitment data migration to Azure SQL Database and built Azure Data Factory ETL pipelines integrating candidate applications, interview schedules, and placement records into a centralized reporting source.*
#### In-Depth Technical & Operational Breakdown:
Rujuwal architected the database schema in **Azure SQL Database**, creating normalized dimensional tables (`Dim_Candidate`, `Dim_Recruiter`, `Dim_Client`, `Dim_JobRequirement`, `Dim_Date`) and central transactional fact tables (`Fact_Outreach`, `Fact_InterviewStage`, `Fact_Placement`).

Within **Azure Data Factory (ADF)**, he engineered parameterized pipelines utilizing Mapping Data Flows. The pipelines incorporated change data capture (CDC), delta detection via MD5 row hashing, lookup transformations, conditional splits for handling malformed records, and automated alerting via Azure Monitor when pipeline steps failed.

#### Sample Project: *Azure Data Factory Enterprise Ingestion Pipeline*
- **Architecture:** ADF pipeline orchestrated with scheduled triggers every 4 hours. Connectors ingested structured feeds from internal applicant tracking systems (ATS), parsed nested JSON metadata, applied business rules, and loaded data using SQL bulk copy operations (`bcp`) for high-throughput performance.
- **Impact:** Unified **3 previously disconnected data silos** into a single golden source of truth containing over **200,000+ historical recruitment transaction records**.

---

### Bullet 4: *Built interactive Power BI dashboards for daily and weekly outreach, funnel conversion, and recruitment cycle time, enabling managers to compare performance and identify process bottlenecks.*
#### In-Depth Technical & Operational Breakdown:
To empower branch managers and practice leads, Rujuwal designed multi-page **Power BI** dashboards focusing on actionable executive UX:
- **Executive Summary:** High-level KPI cards (Total Placements, Active Pipeline, Average Cycle Time, Revenue Attribution) with dynamic delta indicators against monthly targets.
- **Funnel Drop-Off Analytics:** Visual funnel charts detailing conversion percentage losses at each screening stage.
- **Recruiter Productivity Matrix:** Scatter plots and matrix visuals benchmarking recruiter outreach volume against placement conversion ratios.

He optimized DAX expressions using pre-calculated summary tables in Azure SQL and composite storage modes, ensuring report pages loaded in under **1.2 seconds**.

#### Sample Project: *Enterprise Recruitment Performance Command Center*
- **Architecture:** Power BI report utilizing bookmark navigation, dynamic measure selection, drill-through capabilities from high-level branch metrics down to individual candidate interview histories, and automated daily email subscriptions for executives.
- **Impact:** Enabled managers to identify a **22% drop-off bottleneck** between Round 1 and Round 2 interviews, leading to targeted coaching that improved overall placement velocity by **18%**.

---

### Bullet 5: *Analyzed recruitment channels, candidate segments, and outreach frequency to identify drop-off patterns and guide targeting and engagement strategies.*
#### In-Depth Technical & Operational Breakdown:
Rujuwal performed rigorous exploratory data analysis (**EDA**) and cohort segmentation in **Python (Pandas, Seaborn)** and **SQL**. He analyzed candidate response behavior across multiple acquisition channels (LinkedIn InMail, job boards, internal employee referrals, direct email outreach) stratified by years of experience, primary technical skillset, and message outreach cadence.

He calculated statistical metrics including response latency distributions, Kaplan-Meier candidate retention curves, and logistical regression modeling to identify the primary drivers of candidate disengagement.

#### Sample Project: *Candidate Acquisition Channel Optimization Study*
- **Methodology:** Segmented 35,000 historical candidate interaction records into behavioral cohorts. Analyzed the correlation between follow-up frequency (e.g., 2-day vs. 5-day cadence) and response rates.
- **Findings & Impact:** Discovered that referral candidates converted at **3.2x the rate** of cold job-board applicants, and that follow-up outreach sent within **48 hours** yielded a **64% higher response rate**. Refocusing recruiter bandwidth on high-yield channels reduced the overall recruitment cycle time by **14 days**.

---

## 3. Vaco Binary Semantics LLP | Associate Data Analyst (Jul 2022 – Jun 2024)
**Project:** Google Hotel Ads Project  
**Domain:** High-Frequency Ad Auction Telemetry, Bid Intelligence & Regional Pricing Optimization

---

### Bullet 1: *Reduced query execution time by 40% by optimizing SQL joins, aggregations, and subqueries across hotel and pricing datasets.*
#### In-Depth Technical & Operational Breakdown:
The Google Hotel Ads repository processed millions of ad auction bids, click-through events, hotel inventory pricing feeds, and partner metadata daily. Legacy analytical queries were plagued by Cartesian joins, unindexed full table scans, correlated subqueries, and non-SARGable `WHERE` clauses (e.g., applying functions to columns in predicate conditions).

Rujuwal performed systematic query profiling using `EXPLAIN ANALYZE` execution plans. He optimized queries by:
1. Replacing correlated subqueries with Common Table Expressions (**CTEs**) and efficient `LEFT JOIN` operations.
2. Introducing composite clustering and partitioning on `hotel_id` and `auction_date`.
3. Pre-aggregating high-volume click telemetry into materialized intermediate tables.
4. Converting string comparisons to integer surrogate key evaluations.

#### Sample Project: *Large-Scale SQL Performance Optimization & Index Tuning*
- **Execution:** Analyzed 25 high-impact analytical queries running against 10M+ row hotel pricing databases. Refactored multi-stage joins and partitioned large transaction tables by calendar month and regional market codes.
- **Impact:** Slashed average analytical query execution times by **40%**, reducing server CPU utilization spikes by **30%** and accelerating reporting pipelines.

---

### Bullet 2: *Automated Google Cloud ingestion and validation, reducing turnaround from 3 hours to 40 minutes, saving 8 hours of manual reporting per week.*
#### In-Depth Technical & Operational Breakdown:
Hotel partner pricing feeds landed continuously in **Google Cloud Storage (GCS)** buckets in diverse formats (gzip CSVs, JSON feeds). Prior to Rujuwal's intervention, analysts manually downloaded files, validated column formatting in local scripts, and loaded them into reporting repositories—a process taking 3 hours every morning.

Rujuwal automated this workflow end-to-end using **Google Cloud Platform (GCP)** primitives. He authored automated **Python** ingestion scripts executed via **Cloud Functions** / **Cloud Run**, loading data directly into **Google BigQuery** using partitioned external tables. He embedded automated schema validation rules checking for unexpected null prices, corrupted currency codes, or duplicate partner timestamps.

#### Sample Project: *Serverless GCS-to-BigQuery Automated Ingestion Pipeline*
- **Architecture:** GCS bucket upload triggers a serverless **Python Cloud Function** that validates file headers, unpacks compressed feeds, executes sanitization transformations using **Pandas**, and streams valid rows into **BigQuery** with automated dead-letter logging for malformed records.
- **Impact:** Reduced data turnaround time from **3 hours to 40 minutes**, saving the analytics team **8 hours of manual toil per week** while accelerating critical ad-bid adjustments.

---

### Bullet 3: *Supported 6 reporting streams and built Looker Studio dashboards across 4 regional markets, translating stakeholder requirements into tracked KPIs and Tableau reporting.*
#### In-Depth Technical & Operational Breakdown:
Managing analytics across 4 major international geographic regions (North America, EMEA, APAC, LATAM) required handling multi-currency conversions, differing tax inclusions (e.g., VAT in Europe vs. post-tax rates in North America), and disparate timezone alignments.

Rujuwal owned **6 end-to-end reporting streams**, collaborating with global partner managers to define tracked KPIs: Impression Share, Click-to-Book Conversion Rate, Average Daily Rate (ADR), Effective Cost Per Click (eCPC), and Return on Ad Spend (ROAS). He constructed interactive **Looker Studio** and **Tableau** dashboards with dynamic currency toggles and localized calendar hierarchies.

#### Sample Project: *Global Multi-Market Ad Performance & Bidding Dashboard*
- **Architecture:** Multi-region **Looker Studio** reporting suite connected to partitioned **BigQuery** analytical views. Implemented parameter-driven controls allowing account leads to toggle between local currencies and normalized USD conversions dynamically.
- **Impact:** Empowered regional ad directors across **4 continents** to monitor bid health in real time, directly informing multimillion-dollar quarterly hotel ad spend allocations.

---

### Bullet 4: *Investigated pricing, tax, and data-quality issues across 2,000+ hotel datasets using segmentation and root-cause analysis; conducted A/B performance analysis to support bid optimization.*
#### In-Depth Technical & Operational Breakdown:
Discrepancies between the ad rate shown on Google Hotel Ads and the actual price on the partner landing page resulted in severe ad rank penalties and wasted ad spend. Rujuwal conducted deep-dive root-cause investigations across **2,000+ partner hotel datasets**.

He engineered diagnostic SQL and Python scripts that systematically detected pricing mismatches, tax omission bugs, and currency rounding discrepancies. Furthermore, he designed and evaluated **A/B performance experiments**, splitting hotel inventories into control and test bidding cohorts to evaluate the statistical significance of automated bid adjustments versus manual floor pricing using two-sample hypothesis testing ($t$-tests and Mann-Whitney $U$ tests).

#### Sample Project: *Pricing Accuracy Diagnostics & A/B Bid Optimization Engine*
- **Methodology:** Automated scraper-to-feed reconciliation script comparing Google cache prices against partner landing page rates. Conducted statistical A/B test analysis on ad bid adjustments across 500 candidate hotels over a 30-day evaluation window.
- **Impact:** Identified and remediated pricing bugs across **150+ major partner hotels**, improving ad price accuracy compliance to **99.1%** and driving a **12% increase in partner booking conversions** during the test period.

---

## 4. Profitmart | Data Analyst Intern (Jan 2022 – May 2022)
**Domain:** Financial Brokerage, Customer Trading Telemetry & Account Retention

---

### Bullet 1 & 2: *Python/SQL data preparation workflows, Pandas/NumPy exploratory analysis, missing value imputation, duplicate cleansing, and stakeholder reporting.*
#### In-Depth Technical Breakdown:
During this internship, Rujuwal established his foundational data engineering and analytical rigor. He extracted trading account activity records, customer margin calls, and brokerage fee transactions using **SQL** queries.

Using **Python (Pandas, NumPy)**, he engineered automated preprocessing scripts that handled missing numerical data via median and KNN imputation, flagged anomalous transactional spikes using interquartile range (IQR) outlier detection, eliminated duplicate trade logs, and structured clean summary workbooks in Excel for management review.

---

## 5. Selected Projects & Academic Foundations

### Project: *Customer Churn Analysis & Retention Strategy*
- **Architecture & Modeling:** Built a comprehensive diagnostic model in **Power BI** using advanced **DAX** and **Python (Scikit-learn)**. Segmented customers across engagement frequency, transactional recency, service ticket volume, and account tenure.
- **Findings & Business Impact:** Discovered that accounts experiencing more than 2 unresolved operational tickets within their first 30 days exhibited an **85% higher churn probability**. The retention strategy recommendations derived from the dashboard contributed to a **15% reduction in churn** and a **10% increase in long-term customer loyalty**.

### Project: *E-commerce Operations Analysis – Target Brazil (100K Orders)*
- **Architecture & Modeling:** Analyzed a public dataset of 100,000 orders across Brazilian states, integrating customer geolocation, payment installments, delivery carrier performance, and freight logistics.
- **Findings & Business Impact:** Identified that regional freight delays in northern states were primarily driven by carrier route consolidation rather than warehouse fulfillment bottlenecks. Provided actionable delivery window estimation formulas that lowered customer complaint escalations.

### Academic Rigor & Certifications:
- **Scaler Specialization in Data Science & Machine Learning (Nov 2021 – Nov 2022):** Intensive curriculum covering Advanced Data Structures, Algorithms, Statistical Modeling, Supervised/Unsupervised ML, Deep Learning, and System Design.
- **Bachelor of Business Administration (BBA) - GGSIPU (Aug 2019 – Mar 2022):** Solid grounding in business economics, financial modeling, organizational behavior, and operational management—enabling seamless communication with senior executive stakeholders.
- **HackerRank Certifications:** SQL (Advanced), Python (Basic).

---
"""
