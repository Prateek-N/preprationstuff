# Teja Talluri - Data Quality Analyst Interview Preparation (Purpose Financial)
# Questions 1 to 15 (Part 1)

QUESTIONS_PART1 = [
    {
        "num": 1,
        "type": "dq_core",
        "title": "Q1: As a Data Quality Analyst at Purpose Financial, how do you define, measure, and monitor the core dimensions of data quality across enterprise lending and financial datasets?",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Data Quality Dimensions & Frameworks",
        "difficulty": "Senior Data Analyst",
        "answer": """In consumer financial services and specialty lending at **Purpose Financial**, data quality directly governs loan underwriting, credit scoring, regulatory compliance, and customer trust. To ensure integrity across our data ecosystem, I evaluate datasets against the six foundational dimensions of data quality: **Accuracy**, **Completeness**, **Consistency**, **Timeliness**, **Validity**, and **Uniqueness**. At **Dish Network** and **Uber**, I translated these conceptual dimensions into automated, quantifiable metrics evaluated daily within **Snowflake**, **Azure Databricks**, and **Presto**.

For **Completeness**, I implement automated column-level profiling using **Python** and **SQL**, flagging unexpected null rates in mission-critical attributes like borrower annual income, Social Security Numbers, or loan disbursement dates. For **Uniqueness**, I enforce entity integrity constraints and execute automated duplicate detection queries on primary keys such as `loan_application_id` and `customer_id`. For **Validity**, I validate data formats against domain constraints—for instance, ensuring credit scores fall strictly between 300 and 850, phone numbers adhere to E.164 formatting, and state codes match valid USPS postal tables. For **Consistency**, I build cross-system reconciliation jobs between operational transactional systems (**Oracle**, **PostgreSQL**) and our analytical lakehouse, guaranteeing ledger balances reconcile down to the penny. For **Timeliness**, I calculate data freshness and ingestion latency against **Service Level Agreements (SLAs)**, tracking the elapsed time between a customer's loan origination event and its availability in downstream BI marts. Finally, for **Accuracy**, I implement business-rule audits, verifying that calculated loan repayment amortization schedules match contractual interest terms. At **Dish Network**, operationalizing these automated dimensions using **dbt tests** and **Great Expectations** eliminated 92% of downstream reporting anomalies, protecting over **$1.8M** in operational and infrastructure overhead while certifying clean data for executive consumption."""
    },
    {
        "num": 2,
        "type": "dq_core",
        "title": "Q2: Purpose Financial requires hands-on SQL expertise across Oracle, Postgres, SQL Server, and Snowflake. How do you design automated SQL audit scripts to catch data anomalies?",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Advanced SQL Auditing & Multi-Engine Validation",
        "difficulty": "Senior Data Analyst",
        "answer": """Authoring automated **SQL** audit scripts across heterogeneous database engines like **Oracle**, **PostgreSQL**, **SQL Server**, and **Snowflake** requires leveraging both standard ANSI SQL and database-specific dialect optimizations. At **Dish Network** and **Uber**, I managed cross-platform data pipelines that extracted operational records from **Oracle** and **PostgreSQL** OLTP instances and loaded them into **Snowflake** and **Amazon Redshift** data warehouses. To maintain audit-readiness, I created modular, parameter-driven SQL validation test suites orchestrated via **Apache Airflow**.

My automated SQL audits address four critical failure modes: referential integrity breaks, duplicate transactions, distribution shifts, and range violations. For instance, in **Snowflake**, I construct automated verification queries utilizing **Common Table Expressions (CTEs)** and window functions to detect orphaned records in loan transactions:
```sql
WITH OrphanAudit AS (
    SELECT t.transaction_id, t.loan_id, t.transaction_amount, t.transaction_date
    FROM silver_loan_transactions t
    LEFT JOIN gold_loan_master m ON t.loan_id = m.loan_id
    WHERE m.loan_id IS NULL AND t.transaction_date >= CURRENT_DATE() - INTERVAL '1 DAY'
)
SELECT COUNT(*) AS orphan_count, COALESCE(SUM(transaction_amount), 0) AS impacted_exposure
FROM OrphanAudit;
```
For **Oracle** and **PostgreSQL** operational stores, I engineer scheduled stored procedures checking for concurrency anomalies, such as duplicate rapid-fire loan disbursements using `COUNT(*) HAVING COUNT(*) > 1` grouped by customer fingerprint and timestamp windows. In **Snowflake**, I leverage zero-copy cloning and metadata functions (`OBJECT_CONSTRUCT`, `SYSTEM$CLUSTERING_INFORMATION`) to audit schema drift and partition health without incurring heavy compute overhead. Furthermore, I wrap these queries into **dbt singular tests** and automated views that push violation counts directly into an enterprise `DQ_AUDIT_LOG` table. If any audit returns a non-zero count on critical compliance columns, the pipeline automatically aborts downstream **Gold layer** materializations, preventing corrupted data from contaminating financial reporting or credit risk models."""
    },
    {
        "num": 3,
        "type": "dq_core",
        "title": "Q3: How do you build automated Data Quality Scorecards and executive dashboards to certify data for business and BI consumption?",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Data Quality Scorecards & BI Certification",
        "difficulty": "Senior Data Analyst",
        "answer": """Building an enterprise **Data Quality Scorecard** requires transforming raw technical validations into intuitive, risk-weighted business health indicators. At **Dish Network** and **Uber**, I designed and maintained executive data quality scorecards in **Tableau**, **Power BI**, and **Streamlit** that monitored hundreds of production tables, consolidating technical test outputs into actionable certification badges for business and analytics stakeholders.

My architectural approach relies on an automated metadata repository:
1. **Rule Execution Layer:** Every scheduled ETL job running in **dbt**, **Apache Airflow**, or **Python** executes validation assertions (e.g., null checks, referential integrity, range checks, schema validation).
2. **Standardized Telemetry Logging:** The results are logged to a centralized **Snowflake** fact table: `FACT_DATA_QUALITY_RESULTS`, capturing `table_name`, `column_name`, `dimension_type`, `rule_name`, `severity_level` (Critical, High, Medium), `records_evaluated`, `records_failed`, and `execution_timestamp`.
3. **Scoring Algorithm:** I formulate a composite Data Quality Health Index:
$$\\text{DQ Score} = 100 - \\sum \\left( \\frac{\\text{Failed Records}}{\\text{Total Records}} \\times \\text{Weight}_{\\text{Severity}} \\right)$$
Critical financial attributes (e.g., loan balance, interest rate, customer SSN) carry a $5\\times$ weight, whereas non-critical metadata (e.g., secondary phone number) carries a $1\\times$ weight. 

In **Tableau** and **Streamlit**, I visualized these scores across data domains (Originations, Servicing, Collections, Marketing). Tables achieving a score $\\ge 98\\%$ earn a green **"Certified for Production"** badge, signaling to BI analysts and financial reporting teams that the dataset is verified for executive reporting. Tables falling below $95\\%$ trigger an amber warning with automated drill-down capabilities showing exact failing keys, error distributions, and historical trendlines. This transparency reduced executive reporting discrepancies at **Uber** from 12 hours to under 2 hours per cycle and gave leadership complete trust in certified datasets."""
    },
    {
        "num": 4,
        "type": "dq_core",
        "title": "Q4: Describe your experience performing Root Cause Analysis (RCA) on a complex data breakdown. What was the issue, and how did you resolve it?",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Root Cause Analysis & Incident Remediation",
        "difficulty": "Senior Data Analyst",
        "answer": """In enterprise data analytics, identifying a symptom is easy; the real value lies in conducting disciplined **Root Cause Analysis (RCA)** to eliminate recurrence. At **Dish Network**, our executive churn analytics dashboard suddenly reported an unprecedented $18\\%$ spike in voluntary customer cancellations overnight, creating panic among product and finance leadership who feared an impending revenue collapse of millions of dollars.

As the lead analytics engineer on the pipeline, I immediately initiated a 5-step RCA protocol:
1. **Containment & Triage:** I flagged the anomaly to executive stakeholders, placed a temporary hold on automated retention marketing campaigns, and created an isolated investigation branch in our **Git** repository.
2. **Data Lineage Tracing:** Using our **dbt** documentation and **AWS Redshift** query logs, I traced the metric lineage backwards from the **Gold** reporting mart through the **Silver** business logic layer to the **Bronze** ingestion staging tables.
3. **Forensic Hypothesis Testing:** I wrote diagnostic **SQL** scripts comparing partition distributions against the prior 30 days. The raw subscriber count and daily transaction volume were completely normal. However, inspecting the Silver transformation layer revealed that an upstream enterprise billing system migration from legacy **Oracle** to cloud-based billing had modified the status field `SUBSCRIPTION_STATUS_CODE`. The legacy system passed numeric values (`1` for active, `4` for cancelled), whereas the new billing API passed string mnemonics (`ACT`, `CAN`).
4. **Failure Mechanism:** The legacy transformation script contained a fallback conditional: `CASE WHEN status_code = '1' THEN 'Active' ELSE 'Cancelled' END`. Because `'ACT'` did not equal `'1'`, the fallback logic erroneously classified 140,000 active subscribers as cancelled.
5. **Remediation & Permanent Controls:** I refactored the dbt transformation model using explicit **Data Contracts**, replaced the loose fallback with strict enumeration validation, added **Great Expectations** schema tests, and backfilled the historical tables. This restored reporting integrity within 6 hours, prevented millions in misdirected retention discounts, and established permanent regression testing for all future system migrations."""
    },
    {
        "num": 5,
        "type": "dq_core",
        "title": "Q5: How do you use Python for automated data validation, profiling, and anomaly detection? Which libraries do you rely on?",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Python Automation & Data Profiling",
        "difficulty": "Senior Data Analyst",
        "answer": """**Python** is my core programmatic language for automating complex data validation, statistical profiling, and anomaly detection that exceeds standard SQL capabilities. At **Uber** and **Dish Network**, I engineered custom Python validation frameworks leveraging **pandas**, **NumPy**, **Great Expectations**, **SciPy**, and **PySpark** to ingest, profile, and certify multi-gigabyte transactional feeds across distributed cloud environments.

My Python automation architecture operates across three functional modules:
1. **Automated Data Profiling:** Using custom scripts and `pandas-profiling` / `ydata-profiling` integrated into **Azure Data Factory** pipelines, I ingest daily incoming customer and transaction files. The script automatically computes cardinality, null percentages, quantiles ($p25, p50, p75, p99$), skewness, and Kurtosis. It checks whether numeric attributes like loan amounts or credit limits follow expected parametric distributions, writing profiling summaries to our metadata store.
2. **Assertion-Based Validation:** I utilize **Great Expectations** to codify business expectations into reusable JSON expectation suites. In a loan servicing context, my Python scripts assert:
```python
suite.expect_column_values_to_be_between(
    "interest_rate", min_value=3.99, max_value=35.99
)
suite.expect_column_values_to_match_regex(
    "ssn", r"^\\d{3}-\\d{2}-\\d{4}$"
)
suite.expect_table_row_count_to_be_between(
    min_value=prev_day_count * 0.85, max_value=prev_day_count * 1.15
)
```
3. **Statistical Anomaly Detection:** For multi-variate anomalies where rules fall short, I author Python scripts employing rolling statistical filters. I calculate **Z-scores** and **Interquartile Range (IQR)** fences on daily transaction volumes:
$$Z = \\frac{X_t - \\mu_{30}}{\\sigma_{30}}$$
If $|Z| > 3.0$, or if an unsupervised **Isolation Forest** (`scikit-learn`) flags unusual clusters of high-dollar, rapid-succession loan applications from identical IP subnets, the script triggers a webhook alert to **Slack** and **PagerDuty** and logs the anomaly into **DataHub**. This automated Python toolkit reduced manual data auditing by 80 hours per month while catching edge-case pipeline anomalies long before downstream BI consumption."""
    },
    {
        "num": 6,
        "type": "dq_core",
        "title": "Q6: What are Data Contracts, and how do you implement them between operational application teams and enterprise data warehouse platforms?",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Data Contracts & Schema Governance",
        "difficulty": "Senior Data Analyst",
        "answer": """In modern data architecture, a **Data Contract** is a formal, version-controlled agreement between upstream operational application software engineers and downstream enterprise data teams. It explicitly defines the schema, data types, business semantics, update frequency, SLA guarantees, and behavioral expectations of data emitted by production services. Historically, upstream software developers alter application schemas or database tables (such as dropping a column or modifying a status enum) without warning, instantly breaking downstream analytics pipelines.

At **Dish Network** and **Uber**, I championed and implemented enterprise Data Contracts using **JSON Schema**, **YAML**, and **dbt** to safeguard our Medallion data lakehouse architecture. The implementation workflow includes:
1. **Contract Definition:** In collaboration with product and software engineering leads, we draft a contract specification in YAML stored in Git. For a consumer lending platform like **Purpose Financial**, a loan application contract specifies:
```yaml
contract_id: loan_application_event_v2
owner: origination_service_team
sla: near_real_time_15min
schema:
  - name: application_id
    type: string
    nullable: false
    unique: true
  - name: requested_amount
    type: decimal(12,2)
    constraints: { min: 500.00, max: 25000.00 }
  - name: credit_score
    type: integer
    constraints: { min: 300, max: 850 }
```
2. **CI/CD Enforcement Gate:** We integrate contract validation into GitHub Actions CI/CD pipelines. If an upstream engineer attempts to push a microservice change that alters a contracted field type or deletes a required attribute, the automated schema-diff test fails, blocking the pull request before deployment.
3. **Runtime Ingestion Gate:** In our **Azure Databricks** and **Snowflake** streaming pipelines, incoming event payloads are validated against the contract using **Python** and **Pydantic**. Non-compliant records are diverted into a Dead Letter Queue (DLQ) for engineering review rather than crashing production tables. 
Implementing strict Data Contracts eliminated unexpected schema drift, averted over $400K in compute waste from failed pipeline retries, and established accountability across cross-functional teams."""
    },
    {
        "num": 7,
        "type": "tech_sql",
        "title": "Q7: Write a production SQL query in Snowflake/PostgreSQL using window functions to detect duplicate customer records created within a 10-minute window with slightly different email addresses.",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Advanced SQL & Entity Resolution",
        "difficulty": "Senior Data Analyst",
        "answer": """Detecting near-duplicate customer records created within a short time interval is critical in consumer finance to prevent fraudulent loan stacking, identity manipulation, and system ingestion glitches. To solve this, I author a high-performance **SQL** query utilizing window functions (`LAG` / `LEAD`), temporal interval calculations, and string similarity matching.

Here is the production-grade query engineered for **Snowflake** or **PostgreSQL**:

```sql
WITH CustomerLeadOrdered AS (
    SELECT 
        customer_id,
        first_name,
        last_name,
        ssn_hash,
        email,
        phone_number,
        created_at,
        -- Look forward to the immediate next record for the same individual identity fingerprint
        LEAD(customer_id) OVER (
            PARTITION BY ssn_hash, UPPER(TRIM(last_name)) 
            ORDER BY created_at ASC
        ) AS next_customer_id,
        LEAD(email) OVER (
            PARTITION BY ssn_hash, UPPER(TRIM(last_name)) 
            ORDER BY created_at ASC
        ) AS next_email,
        LEAD(created_at) OVER (
            PARTITION BY ssn_hash, UPPER(TRIM(last_name)) 
            ORDER BY created_at ASC
        ) AS next_created_at
    FROM silver_customer_profiles
    WHERE created_at >= CURRENT_DATE() - INTERVAL '7 DAYS'
),
SuspectedDuplicates AS (
    SELECT 
        customer_id AS initial_customer_id,
        next_customer_id AS duplicate_customer_id,
        first_name,
        last_name,
        ssn_hash,
        email AS initial_email,
        next_email AS duplicate_email,
        created_at AS initial_created_at,
        next_created_at AS duplicate_created_at,
        -- Compute exact elapsed difference in minutes
        TIMESTAMPDIFF('minute', created_at, next_created_at) AS elapsed_minutes
    FROM CustomerLeadOrdered
    WHERE next_created_at IS NOT NULL
      AND TIMESTAMPDIFF('minute', created_at, next_created_at) BETWEEN 0 AND 10
      AND LOWER(TRIM(email)) <> LOWER(TRIM(next_email))
)
SELECT 
    initial_customer_id,
    duplicate_customer_id,
    last_name,
    initial_email,
    duplicate_email,
    initial_created_at,
    duplicate_created_at,
    elapsed_minutes,
    'Potential Fraud / Ingestion Duplicate' AS anomaly_classification
FROM SuspectedDuplicates
ORDER BY initial_created_at DESC;
```

**Query Mechanics:**
1. `PARTITION BY ssn_hash, UPPER(TRIM(last_name))`: Groups identical borrower identities regardless of minor typographical case variations.
2. `LEAD(...) OVER (...)`: Retrieves the subsequent record’s attributes without requiring costly $O(N^2)$ cross self-joins.
3. `TIMESTAMPDIFF('minute', ...)`: Filters precisely for records created within the 10-minute fraud/ingestion vulnerability window.
4. `email <> next_email`: Confirms the email attributes diverge, surfacing deceptive application attempts or multi-account creation bugs."""
    },
    {
        "num": 8,
        "type": "tech_sql",
        "title": "Q8: How do you handle schema evolution and schema drift across Snowflake, Oracle, and Postgres when upstream transactional systems alter data types or add columns?",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Schema Evolution & Drift Management",
        "difficulty": "Senior Data Analyst",
        "answer": """In enterprise data architectures bridging transactional RDBMS engines (**Oracle**, **PostgreSQL**) and cloud warehouses (**Snowflake**), unmanaged **schema drift** is the single most common cause of pipeline failure. When an upstream team adds a column, renames an attribute, or alters a precision type (e.g., from `VARCHAR(20)` to `VARCHAR(100)` or `INT` to `BIGINT`), downstream pipelines either crash or silently truncate data.

At **Dish Network** and **Uber**, I instituted a resilient three-tier schema governance framework:
1. **Automated Schema Auditing & Metadata Tracking:** In **Python**, I built daily automated schema-crawling jobs using `SQLAlchemy` and database information schemas (`INFORMATION_SCHEMA.COLUMNS`). The script compares today's live table schema in Oracle/PostgreSQL against our baseline schema repository stored in **Snowflake**. If a new column is detected, an existing column is missing, or a data type has shifted, the system logs the exact delta to an audit table and alerts the data engineering team via Slack.
2. **Adaptive Ingestion in Snowflake:** In our Bronze/staging layer in **Snowflake**, I design ingestion pipelines utilizing semi-structured data types (`VARIANT`) and modern schema evolution capabilities. By leveraging `ENABLE_SCHEMA_EVOLUTION = TRUE` on Snowflake tables and Snowpipe definitions, the target table automatically incorporates newly emitted columns without crashing the ingestion service.
3. **Controlled Silver/Gold Propagation via dbt:** While the Bronze staging layer adapts dynamically, I strictly control the Silver (cleaned business entities) and Gold (reporting) layers through **dbt**. New columns do not automatically flow into financial reporting marts until verified for business semantics and certified for quality. We author comprehensive column assertions; if an upstream column changes to incompatible types, dbt's pre-hook validations halt materialization, ensuring that financial dashboards and underwriting scorecards at **Purpose Financial** never consume unverified structural changes."""
    },
    {
        "num": 9,
        "type": "tech_sql",
        "title": "Q9: How do you audit and validate the Medallion Architecture (Bronze, Silver, Gold) to certify data moving through each layer in a modern cloud lakehouse?",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Medallion Architecture & Data Certification",
        "difficulty": "Senior Data Analyst",
        "answer": """The **Medallion Architecture (Bronze $\\rightarrow$ Silver $\\rightarrow$ Gold)** provides a structured framework for data refinement, but its integrity relies entirely on rigorous, progressive data quality gates between each layer. At **Dish Network** and **Uber**, I architected and audited Medallion data pipelines on **Azure Databricks**, **Snowflake**, and **AWS Redshift**, ensuring data was certified before progressing downstream.

Here is my data quality certification lifecycle across the three tiers:
1. **Bronze Layer (Raw Ingestion Integrity):** The Bronze layer stores raw, immutable append-only event streams and transactional extracts from **Oracle**, **Postgres**, and external APIs. Quality gates here focus on **structural and volumetric integrity**:
   - Verification of file integrity, row counts, and checksums against source transmission logs.
   - Preservation of technical metadata (`_ingested_at`, `_source_file`, `_raw_payload`).
   - Non-blocking validation: Malformed JSON or corrupted rows are flagged and stored rather than discarded, ensuring 100% audit traceability.
2. **Silver Layer (Cleaned, Conformed, & Enriched):** Data moving from Bronze to Silver undergoes heavy data hygiene and business rule transformation via **dbt** and **PySpark**. Quality gates here focus on **entity resolution, validity, and consistency**:
   - Strict schema enforcement, type casting, and deduplication using primary keys.
   - Validation against business rules (e.g., loan amounts $>0$, valid state codes, standardized timestamps in UTC).
   - Referential integrity checks between dimensions and facts (e.g., verifying `customer_id` exists in the master customer dimension).
3. **Gold Layer (Aggregated, Curated, & Certified for BI):** The Gold layer powers executive dashboards, financial reporting, and machine learning feature stores. Quality gates here focus on **financial reconciliation and analytical accuracy**:
   - Ledger balance reconciliation: Verifying that total loan balances across all accounts match general ledger summaries down to the penny.
   - Statistical anomaly checks on KPI aggregations ($p99$ values, day-over-day variance $\\le \\pm 5\\%$).
Only tables passing all automated Silver-to-Gold dbt assertions receive the **"Data Quality Certified"** stamp in **DataHub**, guaranteeing that **Purpose Financial** business leaders consume 100% verified data."""
    },
    {
        "num": 10,
        "type": "tech_sql",
        "title": "Q10: Purpose Financial manages consumer loans and financial transactions. How do you implement automated financial balance reconciliation in SQL to prevent ledger imbalances?",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Financial Balance Reconciliation & Ledger Auditing",
        "difficulty": "Senior Data Analyst",
        "answer": """In consumer lending and financial services at **Purpose Financial**, financial reconciliation is an audit-mandated necessity. Discrepancies between loan origination amounts, cumulative customer repayments, accrued interest, fees, and the current outstanding principal ledger balance can indicate transaction loss, double-posting, or calculation bugs. At **Dish Network** and **Cipla**, I built automated financial reconciliation frameworks in **SQL** and **Python** to verify transactional integrity across accounting cycles.

To audit loan balance integrity, I implement a **Rolling Daily Roll-Forward Reconciliation Model** in **Snowflake/PostgreSQL**:
$$\\text{Ending Balance}_{\\text{Today}} = \\text{Beginning Balance}_{\\text{Today}} + \\text{New Loans Funded} + \\text{Accrued Interest} + \\text{Fees} - \\text{Principal Repayments} - \\text{Charge-offs}$$

The automated SQL reconciliation script runs nightly:
```sql
WITH DailyRollForward AS (
    SELECT 
        l.loan_id,
        l.current_principal_balance AS reported_ending_balance,
        COALESCE(b.prior_ending_balance, 0) AS beginning_balance,
        COALESCE(t.new_disbursements, 0) AS disbursements,
        COALESCE(t.accrued_interest, 0) AS interest_accrued,
        COALESCE(t.fee_assessments, 0) AS fees_assessed,
        COALESCE(t.principal_payments, 0) AS payments_applied,
        COALESCE(t.charge_offs, 0) AS charge_offs,
        -- Calculate mathematically expected ending balance
        (COALESCE(b.prior_ending_balance, 0) + COALESCE(t.new_disbursements, 0) 
         + COALESCE(t.accrued_interest, 0) + COALESCE(t.fee_assessments, 0) 
         - COALESCE(t.principal_payments, 0) - COALESCE(t.charge_offs, 0)) AS calculated_ending_balance
    FROM gold_loan_master l
    LEFT JOIN (
        SELECT loan_id, current_principal_balance AS prior_ending_balance 
        FROM gold_loan_snapshot_daily WHERE snapshot_date = CURRENT_DATE() - INTERVAL '1 DAY'
    ) b ON l.loan_id = b.loan_id
    LEFT JOIN (
        SELECT 
            loan_id,
            SUM(CASE WHEN txn_type = 'DISBURSEMENT' THEN amount ELSE 0 END) AS new_disbursements,
            SUM(CASE WHEN txn_type = 'INTEREST' THEN amount ELSE 0 END) AS interest_accrued,
            SUM(CASE WHEN txn_type = 'FEE' THEN amount ELSE 0 END) AS fees_assessed,
            SUM(CASE WHEN txn_type = 'PAYMENT' THEN amount ELSE 0 END) AS principal_payments,
            SUM(CASE WHEN txn_type = 'CHARGEOFF' THEN amount ELSE 0 END) AS charge_offs
        FROM silver_transactions 
        WHERE txn_date = CURRENT_DATE() - INTERVAL '1 DAY'
        GROUP BY loan_id
    ) t ON l.loan_id = t.loan_id
    WHERE l.is_active = TRUE
)
SELECT 
    loan_id,
    reported_ending_balance,
    calculated_ending_balance,
    ROUND(reported_ending_balance - calculated_ending_balance, 2) AS variance_amount
FROM DailyRollForward
WHERE ABS(reported_ending_balance - calculated_ending_balance) > 0.01;
```
If this audit identifies any loan where variance exceeds $\\$0.01$, the job outputs the exact failing loan ID to our finance ops alert channel, halts automated general ledger journal posting, and triggers an immediate reconciliation review."""
    },
    {
        "num": 11,
        "type": "tech_sql",
        "title": "Q11: How do you design and maintain automated Data Dictionaries and Data Lineage maps across enterprise cloud data warehouses?",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Data Dictionaries & End-to-End Lineage",
        "difficulty": "Senior Data Analyst",
        "answer": """Maintaining accurate, automated **Data Dictionaries** and end-to-end **Data Lineage** is essential for regulatory compliance, impact analysis, and cross-functional self-service analytics. Manual documentation in static spreadsheets becomes obsolete within weeks. At **Dish Network** and **Cipla**, I established automated cataloging and lineage tracking architectures utilizing **DataHub**, **dbt docs**, and **Snowflake Access History / Object Dependencies**.

My approach centers on **Docs-as-Code** and automated metadata scraping:
1. **In-Code Metadata Definition in dbt:** All table models and columns are defined and documented directly in version-controlled `schema.yml` files alongside SQL transformation code. Every column definition includes business descriptions, logical data types, allowed values/enumerations, data sensitivity classifications (e.g., `PII`, `Financial`), and operational owners:
```yaml
models:
  - name: dim_loan_account
    description: "Certified Gold-tier customer loan account dimension."
    columns:
      - name: interest_rate_apr
        description: "Annual Percentage Rate (APR) formatted as a percentage."
        data_tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0.0
              max_value: 36.0
```
2. **Automated Data Lineage Harvesting:** I leverage **dbt** lineage graphs combined with **Snowflake's** metadata views (`SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY` and `OBJECT_DEPENDENCIES`). When queries run, Snowflake records exact column-level read and write interactions. I built Python scripts that extract these access graphs and publish them directly into **DataHub**.
3. **Change Impact Analysis:** When an upstream engineering team proposes modifying a column in an **Oracle** source table, I run an automated lineage trace in DataHub. Within minutes, the trace identifies every downstream Silver table, Gold reporting view, executive **Tableau** dashboard, and regulatory compliance extract impacted by the change. This automated governance compressed regulatory submission preparation at Cipla by 3 weeks and guaranteed full auditability across all data domains."""
    },
    {
        "num": 12,
        "type": "tech_sql",
        "title": "Q12: How do you monitor and optimize query performance, resource consumption, and clustering health on Snowflake when executing massive data quality scans?",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Snowflake Query Optimization & DQ Compute Efficiency",
        "difficulty": "Senior Data Analyst",
        "answer": """Running exhaustive data quality audits and full-table scans across multi-terabyte datasets can easily cause cloud compute costs to skyrocket and saturate warehouse capacity if queries are not rigorously optimized. At **Dish Network** and **Uber**, I optimized **Snowflake** pipelines processing over 180M+ daily records, slashing execution times from 6 hours to 47 minutes and saving **$420K** in annual compute spend.

To execute high-efficiency data quality scans in Snowflake without inflating compute costs, I implement five architectural best practices:
1. **Partition Pruning & Clustering Keys:** I ensure large fact tables (e.g., transactions, clickstreams, loan events) are clustered on high-cardinality, temporal query keys: `CLUSTER BY (DATE_TRUNC('MONTH', transaction_date), customer_region)`. When running daily DQ audits, Snowflake utilizes metadata pruning to scan only the micro-partitions modified within the lookback window, reducing scanned bytes by up to 95%.
2. **Avoiding Full Table Scans via Incremental Testing:** Rather than scanning entire multi-terabyte tables, I configure **dbt incremental models** and audit queries using watermark filters: `WHERE _ingested_at >= CURRENT_DATE() - INTERVAL '1 DAY'`.
3. **Dedicated DQ Virtual Warehouses:** I isolate data quality validation and profiling workloads onto a dedicated virtual warehouse (`DQ_WH`) configured with aggressive auto-suspend (60 seconds) and multi-cluster scaling. This prevents resource contention with user-facing BI tools or mission-critical ingestion pipelines.
4. **Leveraging Snowflake Metadata and Approximation Functions:** For high-level profiling (cardinality, row counts, null counts), I avoid costly `COUNT(DISTINCT ...)` queries. Instead, I utilize hyper-efficient approximate functions like `APPROX_COUNT_DISTINCT()` (HyperLogLog) and inspect the `TABLE_STORAGE_METRICS` view for instant, zero-cost row count validations.
5. **Monitoring Query Profiler & Spilling:** I regularly audit the **Snowflake Query History** using SQL, filtering for queries exhibiting "Bytes Spilled to Local/Remote Storage." Spilling indicates undersized warehouse memory relative to sort/join operations. By tuning join keys, eliminating cartesian products, and right-sizing warehouses, I maintain rapid validation speeds with minimal credit consumption."""
    },
    {
        "num": 13,
        "type": "gov_compliance",
        "title": "Q13: Financial services data requires strict compliance with GLBA, FCRA, and SOC 2. How do you implement PII/NPI data masking, role-based access control (RBAC), and audit logging?",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Regulatory Compliance, PII Masking & Security",
        "difficulty": "Senior Data Analyst",
        "answer": """In consumer financial services, safeguarding **Personally Identifiable Information (PII)** and **Nonpublic Personal Information (NPI)** is mandated under federal regulations such as the **Gramm-Leach-Bliley Act (GLBA)**, the **Fair Credit Reporting Act (FCRA)**, and **SOC 2 Type II** trust principles. Improper exposure of Social Security Numbers, banking account details, or credit scores exposes the enterprise to severe regulatory fines and reputational destruction. At **Dish Network** and **Uber**, I architected HIPAA- and SOC 2-compliant data governance frameworks enforcing least-privilege security controls.

My compliance framework integrates four core pillars:
1. **Dynamic Data Masking (DDM):** In **Snowflake** and **PostgreSQL**, I implement policy-based Dynamic Data Masking. For sensitive columns like `ssn`, `bank_account_number`, and `date_of_birth`, I define masking policies driven by user roles:
```sql
CREATE OR REPLACE MASKING POLICY ssn_mask AS (val STRING) RETURNS STRING ->
    CASE 
        WHEN CURRENT_ROLE() IN ('COMPLIANCE_OFFICER', 'FINANCE_LEAD') THEN val
        WHEN CURRENT_ROLE() IN ('DATA_ANALYST', 'BI_DEVELOPER') THEN CONCAT('XXX-XX-', RIGHT(val, 4))
        ELSE '***-**-****'
    END;
ALTER TABLE gold_customer_master MODIFY COLUMN ssn SET MASKING POLICY ssn_mask;
```
2. **Role-Based Access Control (RBAC):** I structure access into hierarchical functional roles: `ETL_SERVICE_ROLE` (read/write on Bronze/Silver), `ANALYST_ROLE` (read-only on Gold with masking), and `ADMIN_ROLE`. Access is granted strictly at the schema and view level rather than raw database access.
3. **Column-Level and Row-Level Security (RLS):** For regional operations or partner-specific data, I apply row-access policies ensuring analysts only access loan records within their authorized state jurisdiction.
4. **Immutable Audit Logging:** I automate continuous auditing of `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` to monitor who queried sensitive tables, when, and what filters were applied. Any bulk extraction of unmasked records or anomalous query behavior triggers immediate automated alerts to Information Security teams."""
    },
    {
        "num": 14,
        "type": "gov_compliance",
        "title": "Q14: How do you establish Data Governance and Data Stewardship frameworks when partnering with cross-functional teams (Engineering, Finance, BI, Risk)?",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Data Governance & Cross-Functional Stewardship",
        "difficulty": "Senior Data Analyst",
        "answer": """Data governance cannot succeed as an isolated IT function; it must operate as a collaborative partnership between technical custodians (Data Engineering), analytical translators (Data Analysts), and business domain owners (Finance, Underwriting, Product, Risk). At **Dish Network** and **Cipla**, I established and co-chaired cross-functional **Data Governance Councils** that unified data definitions, eliminated metric duplication, and institutionalized data stewardship across the enterprise.

To make governance operational at **Purpose Financial**, I implement a four-part stewardship framework:
1. **Clear Ownership & Accountability (RACI Matrix):** Every core business entity (e.g., `Customer`, `Loan Application`, `Payment Transaction`, `Delinquency`) is assigned a designated **Business Data Owner** (e.g., VP of Credit Risk) and a **Technical Data Steward** (Senior Data Analyst / Engineer). The business owner defines the semantic definition and access policies, while the technical steward enforces schema validation, SLA tracking, and data quality tests.
2. **Standardized KPI Glossaries:** One of the most prevalent operational problems in financial organizations is conflicting metric definitions—for example, Finance defining "Active Customer" as anyone with an open loan balance, while Marketing defines it as anyone who logged in within 90 days. I created centralized, version-controlled metric repositories in **dbt** and **DataHub**, establishing single certified formulas for metrics like **Net Charge-Off Rate**, **Cost Per Origination**, and **Delinquency Aging Buckets**.
3. **Data Quality SLA & Certification Cadence:** We established monthly Data Quality Review Boards with department heads. In these sessions, we review the automated Data Quality Scorecards, examine root causes of failed validations, and prioritize data debt remediation in Jira sprints alongside product feature work.
4. **Self-Service Enablement:** I conduct training workshops for BI analysts and business users on querying certified semantic models, reading data lineage graphs, and utilizing data dictionaries, fostering a culture where data quality is recognized as an enterprise asset."""
    },
    {
        "num": 15,
        "type": "gov_compliance",
        "title": "Q15: When auditing third-party external data feeds (credit bureaus like Experian/Equifax, fraud scores, bank aggregation APIs), how do you validate data quality and handle API schema shifts?",
        "category": "Purpose Financial DQ Interview",
        "subCategory": "Third-Party Data Auditing & External Ingestion",
        "difficulty": "Senior Data Analyst",
        "answer": """In consumer lending organizations like **Purpose Financial**, underwriting and verification depend heavily on third-party data providers: credit bureaus (**Experian**, **Equifax**, **TransUnion**), alternative credit scores, fraud intelligence APIs (**LexisNexis**, **Emailage**), and bank account aggregation feeds (**Plaid**). Ingesting external data introduces substantial risks: vendor API schema changes, delayed file drops, missing score attributes, and silent distribution shifts that can miscalibrate underwriting algorithms.

At **Uber** and **Dish Network**, I designed robust ingestion and validation frameworks for external partner data:
1. **Contractual SLA & Completeness Audits:** For batch drops (SFTP files), automated **Airflow** sensors monitor file landing times against vendor SLAs. Upon arrival, an automated Python task checks file size, header integrity, line counts, and checksums. If a daily bureau file drops with $30\\%$ fewer records than our 30-day moving average, the pipeline pauses processing and alerts vendor operations before incomplete data enters our underwriting datamart.
2. **JSON Schema & Payload Validation:** For real-time REST API webhooks, I implement **Pydantic** validation models in Python. The validator inspects incoming JSON payloads against strict schemas. If an API provider introduces an unannounced schema shift (e.g., renaming `credit_score` to `bureau_score` or passing null values in risk tier indicators), the validator diverts the malformed payload into a **Dead Letter Queue (DLQ)** in **Amazon S3** or **Azure Blob Storage** and fires an alert.
3. **Statistical Distribution Tracking (PSI & Drift):** Vendor credit scores should exhibit stable statistical distributions. I compute the **Population Stability Index (PSI)** on weekly bureau scores:
$$\\text{PSI} = \\sum \\left( (\\text{Actual}\\% - \\text{Expected}\\%) \\times \\ln\\left(\\frac{\\text{Actual}\\%}{\\text{Expected}\\%}\\right) \\right)$$
A $\\text{PSI} > 0.2$ indicates significant drift in external scoring models. Detecting these anomalies prevented underwriting distortions and held external vendors contractually accountable to rigorous quality standards."""
    }
]
