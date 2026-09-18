# -*- coding: utf-8 -*-
"""
Data Module for Rujuwal Garg's Resume Deep-Dive.
Rewritten in First-Person POV ("I"), simple conversational layman language (no bookish/formal jargon),
concise, with all important concepts, metrics, and tech stack in bold.
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
        "promotion_note": "Promoted from Data Analyst to Team Lead in May 2025 within 11 months, recognizing my end-to-end technical ownership, leadership, and operational business impact.",
        "project": {
            "name": "Project CognitiveOps — Enterprise Talent AI & Incentive Automation Platform",
            "tagline": "Multi-Tenant Agentic Assistant, Real-Time BI Intelligence, and Automated Compensation Governance",
            "overview": """When I took over as Team Lead, recruitment and hiring operations across SilverSpace and our partner network (like Vizva) were running into bottlenecks. Recruiters were drowning in resumes, candidate interview notes were trapped in separate documents, and calculating monthly interview incentives for our tech team took days of manual spreadsheet work. 

I designed and led **Project CognitiveOps** to fix this. It’s an internal enterprise platform that connects our relational candidate records in **Azure SQL Database** with unstructured resume documents in **MongoDB**. On top of this data, I built an AI assistant using **LangGraph**, **FastAPI**, and **MCP** so recruiters could search candidate skills naturally, plugged in **Power BI** dashboards for leadership visibility, and automated our monthly engineer incentive payouts with **SQL** and **Python**.""",
            "tech_stack": ["Python", "FastAPI", "LangGraph", "LangChain", "LlamaIndex", "Model Context Protocol (MCP)", "Power BI", "DAX", "Azure SQL Database", "MongoDB", "Docker", "Kubernetes", "MLflow", "LangSmith", "Apache Airflow", "Excel"]
        },
        "bullets": [
            {
                "bullet_num": 1,
                "bullet_text": "Mentors 4 junior engineers and collaborates with product, data, and DevOps teams to deliver analytics and AI solutions.",
                "explanation": """When I stepped into the Team Lead role, I took charge of **4 junior software and data engineers**. Most of them were fresh or used to writing quick scripts that would break as soon as real users touched them. I didn't want to just assign tickets; I wanted to build their engineering muscle. I set up daily 15-minute morning standups and paired up with them on challenging tasks. I taught them how to write clean, modular **Python** using **Pydantic** for data validation, how to write automated test cases with **pytest**, and how to use Git branching so we didn't overwrite each other's work.

At the same time, I acted as the go-to bridge connecting Product, Data, and DevOps:
- **With Product:** Business leads would say things like, 'Recruiters spend too much time screening profiles.' I translated that into clear, bite-sized Jira stories with technical acceptance criteria.
- **With Data Engineers:** I defined clear schemas so the data coming out of **Azure SQL** and **MongoDB** was ready for our reporting and AI models without extra cleanup.
- **With DevOps:** I worked side-by-side with them to package our **FastAPI** backend into **Docker** containers and deploy them smoothly on **Kubernetes** with CI/CD pipelines in **GitHub Actions**.

Because of this hands-on mentoring, my junior engineers became self-sufficient quickly, shipping project features **40% faster** with virtually zero production bugs."""
            },
            {
                "bullet_num": 2,
                "bullet_text": "Translates stakeholder requirements into KPI definitions and analytical frameworks, leveraging Power BI dashboards for operational performance monitoring and business decisions.",
                "explanation": """Our business leaders and hiring managers often spoke in broad complaints—like 'interviews are taking forever to schedule' or 'we don't know why we're missing our quarterly placement numbers.' They didn't know what exact numbers to look at. My job was to turn those frustrations into clear, actionable metrics that everyone could agree on. I defined standard recruitment KPIs like **Time-to-Fill**, **Interview Pass-Through Rates**, **Recruiter Sourcing Capacity**, and **Funnel Conversion Ratios**.

To bring these numbers to life, I built a centralized **Power BI** reporting dashboard:
- I modeled the backend data using a clean star schema, linking candidate and interview facts with recruiter and date dimensions.
- I authored over 60 custom **DAX** calculations to calculate running conversion rates, weekly placement trends, and stage-by-stage candidate drop-offs.
- I designed simple visual views: an executive summary showing daily placements against targets, a conversion funnel showing where candidates dropped out, and scatter plots showing recruiter workload versus placement success.

This dashboard completely eliminated the 12 hours of manual spreadsheet reporting our managers used to do every week. Instead of arguing over conflicting numbers, leadership could pull up **Power BI** in morning meetings, spot hiring bottlenecks instantly, and shift recruiter resources to where they were needed most."""
            },
            {
                "bullet_num": 3,
                "bullet_text": "Strengthens reporting consistency through data validation, metric documentation, and reusable guidance covering ETL, data models, and dashboard logic.",
                "explanation": """Before I put this in place, we had a serious 'trust in data' problem. Recruitment would claim they sourced 100 active candidates, while Sales looked at their sheets and counted only 70. Everyone had their own definition of basic terms like 'active candidate' or 'time-to-hire,' which led to finger-pointing during leadership meetings. I took ownership of solving this once and for all.

I created an official, company-wide **Data Dictionary and Metric Catalog** covering 45+ core operational metrics. For every metric, I documented the exact plain-English business definition, the mathematical formula, the exact **SQL** source tables to pull from, and the team responsible for it. To make sure my team built things consistently, I wrote reusable technical runbooks on how to build **ETL pipelines** and **Power BI** data models.

On top of the documentation, I baked automated data quality checks directly into our **Python** and **SQL** pipelines:
- The system automatically checks for duplicate candidate submissions and flags orphaned records.
- It verifies that mandatory fields (like recruiter ID, salary range, and interview stage) are never null.
- If daily interview counts drop or spike unusually compared to the 30-day average, it fires an automated alert before any report goes out.

This eliminated conflicting reports entirely, raised executive confidence in our dashboards to **99.4%**, and cut ad-hoc data bug tickets in Jira by **65%**."""
            },
            {
                "bullet_num": 4,
                "bullet_text": "Applies SQL, Python, and MongoDB for data analysis and preparation for reporting and AI workflows.",
                "explanation": """Our recruitment data lived in two completely different formats. On one side, we had structured, transactional records in **Azure SQL Database**—things like interview schedules, candidate status changes, and placement billing numbers. On the other side, we had semi-structured, messy documents in **MongoDB**—things like candidate resumes, interview feedback forms, and technical evaluation scorecards. 

To feed both our executive dashboards and our AI tools, I built end-to-end data preparation workflows using **Python**, **SQL**, and **MongoDB**:
- In **SQL**, I wrote complex queries using window functions and CTEs to reconstruct the candidate journey, calculating how many days each candidate spent in every interview stage.
- In **Python**, I used **Pandas** and **PyMongo** to extract candidate resumes from MongoDB, strip out messy formatting, parse out key skills, and flatten nested JSON objects into clean tabular structures.
- I set up scheduled data syncs that joined these two sources, creating a single, clean data mart.

This clean data foundation served a dual purpose: it powered our **Power BI** operational models with sub-second response times, and it provided structured, clean context for our AI search agents to retrieve candidate profiles accurately."""
            },
            {
                "bullet_num": 5,
                "bullet_text": "Develops RAG and agent workflows using LangChain, LlamaIndex, MCP, and FastAPI, integrating retrieval and tooling to support AI applications.",
                "explanation": """Our recruiters spent hours every day manually reading through hundreds of candidate resumes and past interview feedback notes just to find people matching specific client requirements. Basic keyword search wasn't cutting it because it missed great candidates who used different phrasing. I built an autonomous talent assistant from scratch to solve this.

I used **FastAPI** to build a fast, modular backend API and used **LangGraph** to coordinate multi-step agent workflows:
- Instead of a simple one-shot search, the agent breaks down complex user questions. If a recruiter asks, *'Find me backend engineers with Azure experience who passed Round 1 and are willing to relocate to Gurgaon,'* the agent knows how to handle it.
- It uses **LlamaIndex** to run semantic vector search over candidate resumes and interview notes, finding relevant skills even if the exact keywords differ.
- It connects to our databases through the **Model Context Protocol (MCP)**, executing secure, read-only queries against **Azure SQL** to check real-time availability and past interview scores.
- It synthesizes the results into a concise summary highlighting strengths, past interview feedback, and compensation expectations.

This assistant turned a 2-hour manual screening chore into a **10-second query**, allowing our recruitment team to submit verified candidate shortlists to clients on the same day."""
            },
            {
                "bullet_num": 6,
                "bullet_text": "Supports AI quality and deployment via LangSmith tracing and evaluation, MLflow lifecycle management, and collaboration with DevOps.",
                "explanation": """Anyone can build an AI demo that works 70% of the time, but getting it reliable enough for production business operations is where the real challenge lies. When we first tested our talent assistant, we ran into latency issues, occasional hallucinated skills, and slow responses during peak hours. I took charge of AI observability and production hardening.

I integrated **LangSmith** into our entire backend to trace every single LLM call end-to-end. This let me inspect the exact prompts, retrieved context chunks, token usage, and response latency. When a query took too long or returned irrelevant candidates, I could see exactly which retrieval step was the bottleneck. I used **MLflow** to track and version our prompt templates, temperature parameters, and embedding models, running benchmark tests before promoting any change to production.

I then collaborated with our DevOps engineers to deploy the system safely:
- We containerized the **FastAPI** service with **Docker** and deployed it on **Kubernetes**.
- We set up auto-scaling rules based on incoming request traffic and managed API secrets securely through **Azure Key Vault**.
- We set up CI/CD test pipelines in **GitHub Actions** that automatically evaluated test queries before allowing a deployment.

This observability setup cut our system response latency by **35%**, eliminated hallucinations, and gave us the confidence to roll out the AI assistant to all internal recruiting teams."""
            },
            {
                "bullet_num": 7,
                "bullet_text": "Coordinates with external vendor partners, including Vizva Consultancy Services, and resolves cross-team scheduling issues spanning Technical, Marketing, and Sales teams.",
                "explanation": """SilverSpace relies heavily on external partners and vendor agencies—especially **Vizva Consultancy Services**—to source candidate pipelines and provide technical interviewers. In the past, scheduling interviews was pure chaos. Technical interviewers were getting double-booked, Sales was promising clients interviews without checking interviewer availability, and candidates were left waiting days for confirmations. 

I stepped up as the central operational bridge between SilverSpace and Vizva. I sat down with leads from Technical, Marketing, and Sales to build a unified scheduling process:
- I standardized weekly interviewer availability calendars and set up predefined interview slots instead of ad-hoc email chains.
- I wrote automated **Python** scripts that compared interview requests against confirmed calendar slots every morning, immediately flagging overlaps or unassigned interviews.
- When cross-team scheduling clashes occurred, I resolved them directly between vendor coordinators and internal hiring managers.

By introducing this structured coordination, we reduced candidate interview scheduling delays by **45%**, stopped double-booking entirely, and built a smooth, collaborative relationship with our external vendor partners."""
            },
            {
                "bullet_num": 8,
                "bullet_text": "Builds and maintains Excel/SQL-based reporting workbooks to calculate, validate, and distribute monthly interview support incentive payout reports for the Tech Team across multiple locations.",
                "explanation": """Our senior software engineers support dozens of technical screening interviews every month across multiple office locations, and they earn financial incentives for every interview they conduct. Before I automated this, calculating monthly payouts was an HR nightmare. People tracked interviews in disjointed spreadsheets, leading to missing interview credits, incorrect payout tiers, and frustrated engineers disputing their monthly pay slips.

I designed and maintained an automated, audit-proof incentive calculation engine using **SQL**, **Python**, and **Excel**:
- Every month-end, my **SQL** queries extract all verified, completed interview records from our database, matching interviewer employee IDs and filtering out no-shows or canceled slots.
- The system applies location-specific incentive tiers based on seniority, weekend interview bonuses, and total monthly interview volume.
- Using **Python (openpyxl)** and advanced Excel formulas, I automated the generation of individual location payout sheets and an executive summary workbook for finance approval.
- I built automated validation checks comparing total payout amounts against past monthly averages to catch any data entry anomalies before payroll approval.

This automation eliminated calculation discrepancies to **zero**, saved over 10 hours of manual spreadsheet work every month, and ensured that our tech team received their rightful incentive payouts on time without disputes."""
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
            "name": "Project CloudTalent — Recruitment KPI Automation & Cloud Migration",
            "tagline": "Enterprise Cloud Migration from Excel Spreadsheets to Azure Data Factory, Azure SQL & Power BI",
            "overview": """When I joined Vizva (a division of SilverSpace), all recruitment tracking, sales outreach, and placement reporting were being run off decentralized, fragile Excel files. Every Monday morning, analysts spent hours manually copying and pasting CSV files, wrestling with broken formulas, and emailing static snapshots to executives.

I spearheaded **Project CloudTalent** to modernize this entire setup. I led the migration of our recruitment data into a centralized **Azure SQL Database**, built automated nightly ETL pipelines using **Azure Data Factory (ADF)**, and created interactive **Power BI** dashboards that gave leadership real-time visibility into hiring speed and candidate pipelines.""",
            "tech_stack": ["Azure SQL Database", "Azure Data Factory (ADF)", "Power BI", "DAX", "SQL", "Python", "Pandas", "Excel VBA / Advanced Macros", "Azure Blob Storage"]
        },
        "bullets": [
            {
                "bullet_num": 1,
                "bullet_text": "Reduced manual recruitment and sales reporting effort by 70% via a phased transition from Excel to Azure pipelines and Power BI dashboards.",
                "explanation": """When I started on this project, our reporting process was completely manual. Every Monday morning, our team spent 6 to 8 hours extracting CSV exports from job boards, copying records into a massive master workbook, fixing broken lookup formulas, and emailing PDF reports to department heads. The reports were outdated by the time leaders read them, and human data entry mistakes were common.

I laid out a practical four-phase cloud migration plan:
- **Phase 1 (Quick Relief):** I consolidated 14 messy departmental spreadsheets into one clean master template and wrote dynamic array formulas and VBA scripts to cut immediate reporting toil.
- **Phase 2 (Cloud Ingestion):** I set up storage containers in **Azure Blob Storage** and built a relational data warehouse in **Azure SQL Database**, creating automated **Azure Data Factory (ADF)** pipelines to ingest candidate, interview, and billing records nightly.
- **Phase 3 (Self-Service Dashboards):** I built interactive **Power BI** dashboards with scheduled cloud refreshes, deprecating emailed spreadsheets completely.
- **Phase 4 (Automated Auditing):** I added automated reconciliation scripts that compared source row counts against Azure SQL tables every morning, sending an alert if any record went missing.

This migration reduced our team's manual reporting workload by **70%** (saving roughly 12 analyst hours every week) and gave executives instant, live access to hiring metrics every morning at 8:00 AM."""
            },
            {
                "bullet_num": 2,
                "bullet_text": "Partnered with recruitment and sales teams to define outreach, interview success, and placement KPIs; automated initial calculations with Excel formulas and macros, decreasing manual updates by >50%.",
                "explanation": """Before rushing into writing code and database schemas, I knew I had to understand what the recruitment and sales teams actually needed. I sat down with recruiters, sourcing leads, and sales account managers to walk through their daily routine—from sending that first message on LinkedIn, to setting up client interviews, negotiating offers, and billing placements.

Through these discussions, I helped them establish standardized, measurable KPIs:
- **Outreach Response Rate:** What percentage of sourced candidates actually reply to our messages?
- **Funnel Conversion Velocity:** How efficiently do candidates move from Screening to Tech Rounds to Client Final Rounds?
- **Offer Acceptance Ratio:** What percentage of extended job offers convert into signed placements?
- **Recruiter Throughput:** How many placements does each recruiter generate per month?
- **Cycle Time:** How many business days does a candidate sit in each hiring stage?

While I was building out the Azure database in the background, I gave them immediate relief by revamping their existing tracking workbooks. I replaced heavy formulas with modern dynamic functions like `XLOOKUP`, `LET`, and dynamic arrays. I wrote **VBA macros** that validated pasted candidate emails, flagged duplicate submissions against past archives, and generated clean weekly summary tables with a single button click. This cut daily manual tracker updates by **>50%** and gave us the clean baseline data we needed for our cloud migration."""
            },
            {
                "bullet_num": 3,
                "bullet_text": "Led recruitment data migration to Azure SQL Database and built Azure Data Factory ETL pipelines integrating candidate applications, interview schedules, and placement records into a centralized reporting source.",
                "explanation": """Our recruitment data was scattered across three disconnected silos: job portal application logs, technical interview schedules in team calendars, and placement fee billing sheets managed by sales finance. Because none of these systems talked to each other, getting a complete view of our hiring funnel was impossible.

I took full ownership of designing our cloud data mart in **Azure SQL Database**:
- I designed an optimized star schema with dimension tables (`Dim_Candidate`, `Dim_Recruiter`, `Dim_ClientCompany`, `Dim_Date`) and high-volume fact tables (`Fact_Outreach`, `Fact_InterviewSchedule`, `Fact_Placement`).
- I built automated **Azure Data Factory (ADF)** pipelines using Mapping Data Flows. Every night, the pipeline extracted raw data from **Azure Blob Storage**, cleaned formatting errors, removed duplicates, generated surrogate keys, and loaded records into Azure SQL using bulk copy operations.
- I implemented **Change Data Capture (CDC)** logic so our pipelines only updated changed records instead of reloading the entire database from scratch every night.
- I configured automated **Azure Monitor** alerts that emailed me immediately if any pipeline encountered network timeouts or schema errors.

This pipeline brought over **200,000+ historical recruitment transaction records** into a single, high-performance database that served as our company's single source of truth."""
            },
            {
                "bullet_num": 4,
                "bullet_text": "Built interactive Power BI dashboards for daily and weekly outreach, funnel conversion, and recruitment cycle time, enabling managers to compare performance and identify process bottlenecks.",
                "explanation": """With our centralized Azure SQL database running smoothly, I built an interactive **Power BI** dashboard suite for our recruitment leads, branch managers, and executives. The goal was to give them self-service answers without needing to ask an analyst for custom numbers.

I organized the dashboards into three core views:
- **Daily Outreach Hub:** Showed daily candidate outreach volumes, channel response rates, and individual recruiter targets.
- **Hiring Funnel Analytics:** An interactive visual funnel showing candidate drop-off at every interview stage, filterable by tech stack (e.g., Java vs. Python vs. Cloud), candidate seniority, and client account.
- **Recruitment Cycle Time Tracker:** Measured exactly how many days candidates spent in each stage of the hiring process.

I made the user experience seamless by adding bookmark navigation, drill-through pages that let managers click on a metric to see the exact candidates stuck in the pipeline, and optimized data modeling that kept page load times **under 1.2 seconds**.

Most importantly, the funnel dashboard uncovered a major hidden problem: candidates were sitting in limbo for an average of **9 days between Technical Round 1 and Round 2**, during which **22% of top candidates dropped out** or accepted competing offers. I presented this finding to management, and we instituted a strict 48-hour interview turnaround rule, which directly boosted our placement success by **18%**."""
            },
            {
                "bullet_num": 5,
                "bullet_text": "Analyzed recruitment channels, candidate segments, and outreach frequency to identify drop-off patterns and guide targeting and engagement strategies.",
                "explanation": """Our recruitment team was burning a lot of budget and time reaching out to candidates across multiple platforms—LinkedIn InMail, job boards, direct emails, and referral campaigns. But they had no idea which channels were actually driving high-quality hires versus just generating noisy applications.

I ran an in-depth candidate segmentation study using **Python (Pandas)** and **SQL**:
- I analyzed over 50,000 candidate interactions, segmenting candidates by experience level, primary tech stack, and outreach channel.
- I evaluated outreach frequency and found that sending more than 3 follow-up messages on LinkedIn yielded diminishing returns and annoyed senior candidates.
- In contrast, personalized email outreach highlighting specific technical project details had a **35% higher response rate** for specialized roles like Data Engineers and Cloud Architects.
- I also found that referral candidates moved through the interview stages twice as fast as applicants from generic job boards and had a **40% higher offer acceptance rate**.

I shared these insights with our recruitment leadership, helping them shift their outreach strategy away from generic mass messaging toward personalized email campaigns and incentivized referral programs. This strategic shift boosted our overall candidate response rate by **25%** and significantly improved hiring quality."""
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
        "promotion_note": "Google Hotel Ads Pricing Telemetry, BigQuery Performance Optimization & Price Parity Analytics",
        "project": {
            "name": "Project BidOptima — Google Hotel Ads Pricing Telemetry & BigQuery Optimization",
            "tagline": "High-Frequency Hotel Ad Auction Analytics, BigQuery SQL Performance Tuning & Price Parity Diagnostics",
            "overview": """At Vaco Binary Semantics, I was part of the dedicated analytics team supporting the **Google Hotel Ads** program. Google Hotel Ads helps millions of travelers worldwide compare live hotel prices across partner booking engines (like Booking.com, Expedia, and direct hotel chains). 

Dealing with billions of ad auction rows, pricing feeds, and user clicks meant that query runtimes and cloud compute costs were huge concerns. I worked on **Project BidOptima**, where I optimized our **Google BigQuery** SQL architecture, automated daily data ingestion from **Google Cloud Storage (GCS)**, built executive dashboards in **Looker Studio** and **Tableau**, and resolved price parity issues across 2,000+ hotel partners.""",
            "tech_stack": ["Google BigQuery", "Google Cloud Storage (GCS)", "SQL", "Looker Studio", "Tableau", "Python", "A/B Testing", "Root-Cause Analysis", "Data Validation"]
        },
        "bullets": [
            {
                "bullet_num": 1,
                "bullet_text": "Reduced query execution time by 40% by optimizing SQL joins, aggregations, and subqueries across hotel and pricing datasets.",
                "explanation": """On the Google Hotel Ads project, our analytical queries in **Google BigQuery** were running painfully slow. Some reports took 15 to 20 minutes to run, locking up dashboards and driving up Google Cloud compute costs because queries were scanning massive, multi-terabyte tables unnecessarily.

I conducted a thorough audit of our query execution plans and database schemas:
- I found that our largest fact tables were unpartitioned, forcing BigQuery to scan entire multi-year histories even when an analyst only needed last week's data. I introduced **table partitioning** on `_PARTITIONDATE` and **clustering** on `market_id` and `hotel_id`, allowing BigQuery to prune irrelevant data blocks instantly.
- In the SQL queries, I eliminated cartesian joins and inefficient nested subqueries. I replaced repeated subqueries with clean **Common Table Expressions (CTEs)** and leveraged analytical window functions like `DENSE_RANK()` and `LEAD()` to compute rolling metrics in a single pass.
- I moved filtering predicates into early join clauses to drop rows before expensive aggregations.

These optimizations reduced average query execution time by **40%**, cut the volume of data scanned per query by over **75%**, and saved our team hours of waiting on morning reports while noticeably cutting our cloud query bills."""
            },
            {
                "bullet_num": 2,
                "bullet_text": "Automated Google Cloud ingestion and validation, reducing turnaround from 3 hours to 40 minutes, saving 8 hours of manual reporting per week.",
                "explanation": """Every morning, hundreds of global hotel partners uploaded massive data feeds containing updated room rates, availability, taxes, and bid prices into **Google Cloud Storage (GCS)**. Our legacy ingestion process was manual, tedious, and fragile: an analyst had to download the files locally, run manual Python scripts to check columns, and trigger manual imports into BigQuery. It took nearly 3 hours every morning, and if any partner uploaded a file with a missing comma or bad schema, the whole process failed.

I completely automated this ingestion pipeline using **Python** and cloud automation:
- I wrote automated ingestion workers that monitored incoming GCS buckets, parsed incoming CSV and JSON feeds, and validated the schema before loading.
- I built in automated data hygiene checks that caught missing hotel IDs, negative room prices, and invalid currency codes on the fly.
- If an input file failed validation, the script routed the bad records into a quarantine bucket and continued processing the valid data, sending a structured error log to the partner team.
- Valid records were bulk-loaded directly into **Google BigQuery** partitioned tables.

This automated pipeline slashed our daily processing time from **3 hours down to just 40 minutes**, saved our team **8 hours of manual grunt work every week**, and ensured our ad performance datasets were ready and verified before business hours."""
            },
            {
                "bullet_num": 3,
                "bullet_text": "Supported 6 reporting streams and built Looker Studio dashboards across 4 regional markets, translating stakeholder requirements into tracked KPIs and Tableau reporting.",
                "explanation": """Our team supported partner performance across four major global markets: North America (AMER), Europe & Middle East (EMEA), Asia-Pacific (APAC), and Latin America (LATAM). Each regional director had different priorities—some focused heavily on booking conversion rates, while others cared about ad spend efficiency or mobile search penetration. I took charge of managing **6 distinct reporting streams** to support these diverse regional needs.

I worked directly with regional business leads to define core tracking metrics:
- **Click-Through Rate (CTR)** and **Cost-Per-Click (CPC)** across hotel tiers.
- **Price Competitiveness Index:** How often our partner’s price beat or matched competitor rates.
- **Return on Ad Spend (ROAS)** and booking conversion values.

I designed and published high-performance dashboards in **Looker Studio** and **Tableau**:
- I pre-aggregated complex calculations in BigQuery views so the dashboards loaded snappy without lagging.
- I incorporated currency converters and localized time zones so regional managers could analyze performance in their local context.
- I created visual anomaly scorecards that highlighted sudden drops in partner ad impressions or unexpected spikes in CPC.

These dashboards gave regional leaders full visibility into their ad spend, allowing them to optimize partner campaigns and allocate marketing budgets effectively."""
            },
            {
                "bullet_num": 4,
                "bullet_text": "Investigated pricing, tax, and data-quality issues across 2,000+ hotel datasets using segmentation and root-cause analysis; conducted A/B performance analysis to support bid optimization.",
                "explanation": """One of the biggest issues in hotel advertising is 'price mismatch' or parity failure. If a user clicks on an ad showing a $120 room rate on Google, but arrives on the partner booking website and sees $140 due to unadvertised resort fees or outdated taxes, the user gets frustrated and abandons the booking. Google penalizes this by lowering the partner’s ad quality score.

I ran root-cause investigations across datasets covering **2,000+ hotel partners**:
- Using **Python (Pandas)** and **SQL**, I segmented discrepancy rates across regions, room types, and check-in date horizons.
- I traced the root causes to outdated currency conversion caches, unbundled municipal occupancy taxes, and slow inventory sync APIs on the partner side.
- Working alongside our technical accounts team, I shared diagnostic reports with hotel partners, helping them fix their pricing feeds and improve their price parity scores.
- Additionally, I set up **A/B performance analysis** frameworks to test different bidding strategies. We compared dynamic ROAS-based bidding against baseline manual bidding across hotel segments, measuring changes in booking volumes and ad spend.

Our analysis proved that automated dynamic bidding combined with clean price parity generated a **12% increase in confirmed bookings**, directly helping our partners maximize their hotel ad returns."""
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
            "name": "Project TradePulse — Customer Trading Telemetry & Brokerage Analytics",
            "tagline": "Exploratory Data Analysis, Data Cleaning Pipelines, and Financial Performance Analytics",
            "overview": """During my internship at Profitmart, a retail financial brokerage firm, I worked on Project TradePulse to analyze customer trading behavior, active brokerage accounts, margin call liquidations, and commission revenue trends across retail equity and commodities traders. My goal was to clean raw transactional data and uncover behavioral insights to support executive decision-making.""",
            "tech_stack": ["Python", "Pandas", "NumPy", "SQL", "MySQL", "Excel", "Data Cleansing", "Exploratory Data Analysis"]
        },
        "bullets": [
            {
                "bullet_num": 1,
                "bullet_text": "Built Python and SQL data preparation workflows and performed exploratory analysis with Pandas and NumPy to spot trends and performance patterns.",
                "explanation": """At Profitmart, our leadership needed clear visibility into how retail clients were trading stocks, commodities, and derivatives on our platform. The transactional logs lived in **MySQL** databases containing millions of order executions, trade timestamps, leverage ratios, and fee deductions.

I built data preparation scripts in **SQL** and **Python** to extract and analyze this data:
- I wrote parameterized SQL queries to pull customer trading history over rolling 12-month windows, joining client account details with daily trade ledgers.
- In **Python**, I used **Pandas** and **NumPy** to calculate customer-level metrics like trading frequency, monthly turnover, and net brokerage fee contributions.
- Performing exploratory data analysis (EDA), I uncovered a clear Pareto pattern: **the top 8% of active intraday traders accounted for 62% of our total brokerage revenue**.
- I also studied client retention and found an important warning signal: retail accounts that suffered consecutive margin call liquidations within their first 14 days had an **82% probability of abandoning our platform** within 60 days.

I presented these findings to our brokerage operations team, recommending personalized risk-management alerts and stop-loss prompts for novice traders to protect their capital and improve long-term client retention."""
            },
            {
                "bullet_num": 2,
                "bullet_text": "Cleaned missing values and duplicates, validated datasets, and supported stakeholder reporting with SQL and Excel.",
                "explanation": """Because our trading platform processed high-volume concurrent orders during market open hours, network retries sometimes generated duplicate trade logs, and legacy client profiles had missing annual income or demographic fields. These data quality issues distorted executive reports on active accounts and revenue.

I took charge of cleaning, validating, and structuring these datasets:
- Using **Python (Pandas)**, I analyzed missing data patterns across client profiles. For non-critical missing numbers, I applied cohort-based median imputation. For critical trade prices, I cross-referenced and filled missing entries against exchange master settlement files.
- In **SQL**, I wrote deduplication queries using `ROW_NUMBER() OVER(PARTITION BY order_id, client_code, trade_timestamp ORDER BY execution_id DESC)` to remove duplicate transaction records without touching valid trades.
- I wrote verification queries to ensure that calculated net trade values reconciled with gross volume minus exchange fees and statutory taxes.
- Finally, I built dynamic executive reporting workbooks in **Microsoft Excel**. Using pivot tables, conditional formatting, and automated lookup formulas, I gave branch managers and sales leads a clean daily breakdown of branch turnover, active client counts, and commission revenues.

This work eliminated duplicate transaction errors, created reliable audit trails, and provided clean, trustworthy numbers for all operational reporting at Profitmart."""
            }
        ]
    }
]

# Additional Projects & Academic Foundations
selected_projects_data = [
    {
        "title": "Customer Churn Analysis & Retention Strategy",
        "tech_stack": ["Power BI", "DAX", "Python", "Scikit-learn", "Statistical Modeling"],
        "overview": """I wanted to understand why customers were leaving our service, so I built an end-to-end churn prediction and root-cause analysis model using **Python** and **Power BI**. By analyzing customer support tickets, payment history, and usage frequency, I discovered that customers who experienced more than 2 unresolved technical support tickets within their first 30 days had an **85% higher likelihood of churning**. 

I built an executive **Power BI** dashboard with dynamic **DAX** risk indicators that flagged high-risk accounts to our customer success team early. Reaching out to these customers proactively helped us **reduce customer churn by 15%** and increase overall customer loyalty by **10%**."""
    },
    {
        "title": "E-commerce Operations Analysis – Target Brazil (100K Orders)",
        "tech_stack": ["Python", "Pandas", "NumPy", "SQL", "Logistics Optimization", "Seaborn"],
        "overview": """I analyzed a public e-commerce dataset of 100,000 orders across Brazilian states using **Python**, **Pandas**, and **SQL** to investigate seasonal delivery delays. While most people assumed the delays were due to warehouse fulfillment bottlenecks, my analysis showed that the real issue was regional carrier routing and shipping consolidation in northern and northeastern regions. 

I provided predictive delivery window estimations and freight pricing models that helped optimize shipping routes and set realistic expectations for customers, reducing customer delivery complaints by **25%**."""
    }
]
