# -*- coding: utf-8 -*-
"""
Part 1: Questions 1 to 15 for Pavan Chandramouleswara
Senior Data Engineer Interview Preparation Suite.
Covers:
- Category 1: Distributed Streaming & Real-Time Data Architectures (Kafka, Spark Streaming, BigQuery, Marketplace Events) [Q1 - Q5]
- Category 2: Data Modeling, Warehousing & Modern Data Stack (dbt, BigQuery, Snowflake Tuning, Medallion/Dimensional) [Q6 - Q10]
- Category 3: Big Data Processing & Distributed Compute (Apache Spark, PySpark/Scala, Hadoop, Hive, AWS EMR) [Q11 - Q15]

Every answer:
- Minimum 300 words
- Rich technical depth grounded in Pavan's resume (Uber, Dell, Adani, Projects, IIT Chicago)
- Important keywords and techstack in bold
"""

QUESTIONS_PART1 = [
    # =========================================================================
    # CATEGORY 1: DISTRIBUTED STREAMING & REAL-TIME EVENT ARCHITECTURES (Q1 - Q5)
    # =========================================================================
    {
        "num": 1,
        "category": "Distributed Streaming & Real-Time Event Architectures",
        "title": "Scaling Real-Time Marketplace Ingestion: Kafka, BigQuery, and Sub-16-Hour SLAs",
        "question": "At Uber, how did you architect the end-to-end event streaming pipeline using Apache Kafka, Python, and GCP BigQuery to ingest 5M+ daily marketplace events and slash latency from 24 hours to under 16 hours?",
        "answer": """At **Uber**, the mobility and delivery marketplace generates continuous telemetry streams including driver location pings, rider trip request lifecycles, surge pricing recalculations, and payment transaction events. Previously, these disparate event streams landed in decentralized object storage buckets and were processed via monolithic end-of-day batch jobs. This architecture resulted in a chronic **24-hour delivery latency**, which severely impaired regional operations teams from performing intraday supply-demand rebalancing, real-time fraud mitigation, and dynamic driver incentive allocations.

To resolve this critical operational bottleneck, I took end-to-end ownership of re-architecting our marketplace ingestion topology into an event-driven, decoupled streaming architecture utilizing **Apache Kafka**, **Python**, and **GCP BigQuery**. At the ingestion layer, event producers across microservices published serialized **Avro** payloads onto high-throughput, partitioned **Kafka topics**, keyed strategically by `driver_id`, `trip_id`, and `geographic_hex_id` to guarantee strict in-order message delivery per entity while preventing partition hot-spotting.

I engineered distributed streaming consumer workers in **Python** leveraging asynchronous I/O and consumer group parallelism. Rather than utilizing legacy row-by-row insertion which triggered extreme API quota throttling and cost spikes, I implemented micro-batching with client-side buffer pooling, flushing micro-batches every 10 seconds or upon accumulating 5,000 records. For storage, I leveraged **GCP BigQuery's Storage Write API (Streaming Ingestion with committed mode)**, which delivers exactly-once delivery semantics and allows immediate queryability of incoming records while bypassing legacy streaming buffer constraints. 

To eliminate downstream compute delays, I designed the staging tables in **BigQuery** with day-level **partitioning on `event_timestamp`** and multi-column **clustering on `marketplace_region_id` and `event_type`**. This physical layout ensured that downstream transformation engines scanned only pertinent byte ranges. Furthermore, I integrated automated health-check heartbeats and end-to-end telemetry monitoring to proactively detect backpressure anomalies before message queues backed up. This complete architectural overhaul reliably scaled past **5M+ daily marketplace events**, eliminated data drops via a dead-letter queue (DLQ) automated retry mechanism, and slashed end-to-end data availability latency from **24 hours to under 16 hours**, unlocking timely operational intelligence across cross-functional marketplace teams."""
    },
    {
        "num": 2,
        "category": "Distributed Streaming & Real-Time Event Architectures",
        "title": "Handling Out-of-Order Events, Deduplication, and Exactly-Once Semantics in Kafka Pipelines",
        "question": "How do you guarantee exactly-once processing semantics, handle late-arriving or out-of-order event streams, and manage distributed deduplication across high-velocity Kafka and BigQuery pipelines?",
        "answer": """In high-velocity distributed streaming platforms like **Uber's** marketplace, network partitions, mobile client reconnects, and asynchronous message retries make out-of-order arrivals and duplicate event payloads an inevitable reality. If an event processing pipeline fails to enforce idempotent processing, duplicate trip records corrupt financial revenue reporting, over-calculate driver compensation, and bias machine learning feature stores.

To guarantee **effectively exactly-once processing semantics**, I implement a multi-layered deduplication and watermarking strategy spanning the producer, streaming consumer, and storage layers:

1. **Producer & Broker Level Idempotence**: I enforce `enable.idempotence=true` on all **Apache Kafka producers**, configuring `acks=all` and `max.in.flight.requests.per.connection <= 5`. This ensures that broker-level network retries do not introduce duplicate message sequences on topic partitions, while Kafka assigns monotonically increasing sequence numbers verified by broker partition leaders.
2. **Consumer-Side Sliding Watermarking**: For real-time stateful aggregations (e.g., dynamic surge multipliers computed over rolling 15-minute time windows), I implement **event-time processing with bounded watermarks** using **Python** consumer streams. The watermark defines the allowable lateness threshold (e.g., 20 minutes). Events arriving within the watermark update the open window state, whereas events arriving past the watermark are segregated to a dedicated dead-letter topic for retrospective reconciliation.
3. **Storage-Layer Deduplication in GCP BigQuery**: Since network retries between consumer microservices and the warehouse can still theoretically introduce duplicates, I establish a deterministic deduplication gate in **BigQuery** using **dbt incremental models**. Each event carries an immutable composite primary key: `FARM_FINGERPRINT(CONCAT(event_uuid, CAST(event_timestamp AS STRING)))`. In our daily incremental merge operations, I leverage the `MERGE` statement:
```sql
MERGE INTO curated.marketplace_events AS target
USING (
    SELECT * EXCEPT(row_num)
    FROM (
        SELECT *, ROW_NUMBER() OVER(
            PARTITION BY event_uuid 
            ORDER BY event_timestamp DESC, ingestion_timestamp DESC
        ) AS row_num
        FROM staging.marketplace_events_raw
        WHERE ingestion_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
    ) WHERE row_num = 1
) AS source
ON target.event_uuid = source.event_uuid AND target.event_date = source.event_date
WHEN NOT MATCHED THEN INSERT ROW;
```
This multi-stage architecture isolates late-arriving anomalies, guarantees mathematical idempotency across **5M+ daily records**, and ensures that downstream executive dashboards and ML feature stores operate on pristine, non-duplicated data."""
    },
    {
        "num": 3,
        "category": "Distributed Streaming & Real-Time Event Architectures",
        "title": "Kafka Partitioning Strategies, Consumer Group Rebalancing, and Lag Mitigation",
        "question": "When scaling high-throughput Kafka topics, what partitioning strategies and consumer tuning techniques do you utilize to prevent consumer lag, hot partitions, and costly rebalancing storms?",
        "answer": """Managing high-throughput **Apache Kafka** clusters requires careful tuning of partitioning strategies, serialization overhead, and consumer group threading models. In high-scale architectures like those at **Uber**, consumer lag is not merely an operational inconvenience; a 30-minute lag on marketplace event ingestion cascades into stale driver dispatching, delayed surge pricing signals, and breached customer SLAs.

To prevent and resolve consumer lag and rebalance storms, I focus on four technical pillars:

1. **Deterministic Partitioning Without Hotspots**: The default Murmur2 partitioner hashes message keys. If the key is chosen carelessly (e.g., partitioning strictly by `country_code`), partitions handling high-density markets like New York or Chicago suffer from severe consumer lag while rural partitions sit idle. I design composite synthetic partition keys, combining entity IDs with geographic grid bins: `CONCAT(marketplace_region_id, '_', MOD(FARM_FINGERPRINT(trip_id), 16))`. This guarantees uniform distributed hashing across partitions while ensuring all lifecycle events for an individual trip route to the exact same partition for in-order consumption.
2. **Mitigating Consumer Rebalance Storms**: When consumers process large micro-batches, long-running downstream writes to **GCP BigQuery** or **Snowflake** can cause processing times to exceed `max.poll.interval.ms`. When this occurs, the Kafka coordinator presumes the consumer dead, evicts it from the group, and triggers an aggressive cluster-wide stop-the-world rebalance. To eliminate this anti-pattern, I decouple message consumption from processing by implementing an in-memory worker thread pool inside our **Python** consumer daemons. The main consumer thread continuously invokes `poll()` to maintain heartbeat liveliness, passing batches to a bounded queue processed by asynchronous background workers. I also configure `heartbeat.interval.ms = 3000` and `session.timeout.ms = 45000`.
3. **Optimizing Batch Throughput**: On the producer side, I tune `linger.ms = 20` and `batch.size = 65536` (64KB) paired with **Snappy or Zstandard compression**. This compresses payload size over the wire by over 40%, reducing network I/O and increasing consumer ingestion throughput.
4. **Automated Consumer Lag Observability**: I integrate **Prometheus** and **Datadog** monitoring on consumer offsets via Kafka lag exporters. If offset lag on any partition exceeds an SLA threshold of 10,000 records for three consecutive minutes, automated alerting fires to scale horizontal Kubernetes consumer pods dynamically."""
    },
    {
        "num": 4,
        "category": "Distributed Streaming & Real-Time Event Architectures",
        "title": "Schema Evolution, Data Contracts, and Schema Registry Governance in Event Streaming",
        "question": "How do you enforce Data Contracts and govern schema evolution (Backward, Forward, Full compatibility) in distributed Kafka architectures to prevent upstream breaking changes from crashing downstream pipelines?",
        "answer": """In enterprise engineering organizations with hundreds of microservices, the single most frequent cause of downstream data pipeline failures is unannounced upstream schema mutations—such as renaming a column, altering an integer data type to a string, or removing a field. At **Uber** and **Dell Technologies**, bridging the data contract gap between operational application developers and analytical consumers was essential to maintaining 99.9% pipeline uptime across **tier-1 datasets exceeding 10TB+**.

To institutionalize data contracts and eliminate breaking changes, I implement an enterprise **Schema Governance Architecture** anchored by **Confluent Schema Registry**, **Apache Avro / Protobuf**, and automated **CI/CD validation gates**:

1. **Strict Compatibility Rules**: I enforce **Full Compatibility** (or at minimum **Backward Compatibility**) as a hard constraint in the Schema Registry. Backward compatibility guarantees that consumers running newer schema code can read records written by older producers (e.g., adding an optional field with an explicit default value). Full compatibility guarantees that new code can read old data and old code can read new data, allowing consumers and producers to be deployed in any arbitrary sequence without service interruptions.
2. **CI/CD Schema Validation Gates**: In our **GitHub Actions** and **Jenkins CI/CD pipelines**, I embed automated pre-merge checks using the Schema Registry Maven/Gradle/Python plugin:
```bash
# Automated CI validation before merging producer PR
schema-registry-cli test-compatibility \
  --schema ./schemas/marketplace/rider_trip_event.avsc \
  --subject marketplace-rider-trips-value \
  --compatibility BACKWARD
```
If a developer attempts to delete a non-optional field, alter a primitive data type, or rename an attribute without a transitional alias, the CI build fails immediately, blocking the pull request before bad code can reach staging or production.
3. **Data Contracts as Code**: I formalize data contracts by maintaining schema repositories as version-controlled code artifacts. Upstream service owners must define semantic metadata: field ownership, deprecation schedules, data classification (PII vs. non-sensitive), and nullability constraints.
4. **Schema Evolution in Downstream Warehouses**: Downstream in **GCP BigQuery** and **Snowflake**, I design schema evolution adapters. When an additive schema change occurs in the Kafka payload, our automated ingestion loaders detect the new schema ID, dynamically execute an `ALTER TABLE ADD COLUMN` statement, and seamlessly populate the new field, avoiding pipeline crashes and manual DBA interventions."""
    },
    {
        "num": 5,
        "category": "Distributed Streaming & Real-Time Event Architectures",
        "title": "Lambda vs. Kappa Architecture: Trade-offs, State Management, and Real-Time Decisioning",
        "question": "Compare Lambda and Kappa architectures for real-time analytics. In what scenarios would you choose one over the other, and how did your work at Uber and Dell reflect these paradigms?",
        "answer": """Both **Lambda** and **Kappa** architectures aim to bridge the gap between low-latency operational event processing and deep historical batch analytics, but they approach the problem with fundamentally different trade-offs regarding operational complexity, code duplication, and consistency guarantees:

1. **Lambda Architecture (Dual-Layer)**:
   - *Architecture*: Incoming streams split into two distinct paths: a **Speed Layer** (e.g., Apache Storm, Flink, Spark Streaming) for low-latency view generation, and a **Batch Layer** (e.g., Hadoop, Hive, AWS EMR batch jobs) that stores the immutable master dataset and recomputes pre-aggregated views periodically. A **Serving Layer** merges queries across both views.
   - *Strengths*: Highly fault-tolerant; historical batch jobs act as a natural healing mechanism to correct streaming errors, dropped packets, or algorithmic drift.
   - *Weaknesses*: High architectural complexity; developers must write and maintain identical business logic in two separate codebases (e.g., Java in streaming and SQL/Hive in batch), causing subtle semantic divergence and high maintenance overhead.
   - *Where I Used It*: At **Dell Technologies**, I integrated 50+ heterogeneous enterprise platforms onto **Hadoop, Hive, Spark, and AWS EMR**. Because legacy transaction ledgers arrived via asynchronous daily flat-files while real-time factory floor telemetry arrived via message queues, the Lambda architecture was necessary to reconcile high-throughput streaming signals against audited financial ledgers.

2. **Kappa Architecture (Single-Stream Layer)**:
   - *Architecture*: Eliminates the batch layer entirely. Everything is treated as a continuous event log (e.g., **Apache Kafka** or Apache Pulsar) with long-term retention. A single stream-processing engine (e.g., **Apache Flink**, **Apache Spark Structured Streaming**) processes both real-time events and historical replays using the exact same codebase.
   - *Strengths*: Unified codebase; zero code duplication; single source of truth; re-processing historical data simply requires spinning up a new consumer group and replaying the Kafka topic from offset zero.
   - *Weaknesses*: Highly dependent on the storage capacity and retention economics of the streaming log; complex ad-hoc analytical joins across months of historical event streams can be compute-intensive.
   - *Where I Used It*: At **Uber**, where marketplace telemetry processing needed to scale to **5M+ daily events** under strict SLAs, we shifted toward the Kappa paradigm. Events stream through Kafka into **GCP BigQuery**, where curated **dbt models** execute deterministic transformations. By treating incoming streams as a unified, immutable event ledger, we eliminated dual-codebase maintenance and reduced operational delivery latency from 24 hours to under 16 hours."""
    },

    # =========================================================================
    # CATEGORY 2: DATA MODELING, WAREHOUSING & MODERN DATA STACK (Q6 - Q10)
    # =========================================================================
    {
        "num": 6,
        "category": "Data Modeling, Warehousing & Modern Data Stack",
        "title": "Standardizing Enterprise Data Modeling: dbt, Medallion Architecture, and BigQuery",
        "question": "At Uber, you drove the creation of standardized dbt data models and curated datasets in BigQuery. How do you design a multi-layer Medallion data architecture, eliminate duplicated reporting logic, and enable self-service analytics?",
        "answer": """In hyper-growth enterprise environments, disparate functional teams—such as growth marketing, rider operations, driver operations, and finance—frequently build isolated, ad-hoc queries directly against raw transactional tables. Over time, this leads to chaotic divergence: different departments report conflicting gross bookings, churn numbers, and trip completion rates because business logic, filter conditions (e.g., excluding test trips or canceled rides), and timezone offsets are duplicated and altered across dozens of unversioned scripts.

At **Uber**, I tackled this chronic inconsistency by driving the creation of an enterprise-grade **dbt (data build tool)** modeling framework on top of **GCP BigQuery**, structuring our data warehouse around the modern **Medallion Architecture (Bronze, Silver, Gold)**:

```mermaid
flowchart TD
    A[Raw Streaming Ingestion: Kafka / Webhooks] --> B[Bronze / Staging Layer: Raw Immutable BigQuery Tables]
    B --> C[Silver / Intermediate Layer: Cleaned, Deduplicated, Conformed Models]
    C --> D[Gold / Marts Layer: Dimensional Star Schemas & Curated Business Entities]
    D --> E[Self-Service BI: Power BI / Tableau]
    D --> F[ML Feature Stores & Downstream Services]
```

1. **Bronze Layer (Raw / Ingestion)**: Ingests raw event streams directly from Kafka and ingestion jobs into append-only tables with minimal transformation. Retains raw JSON payloads, ingestion metadata, and extraction timestamps.
2. **Silver Layer (Intermediate / Conformed Entities)**: Implemented in dbt as view or incremental models. I wrote standardized transformation macros to unpack nested JSON attributes, enforce deterministic schema casting, standardize timezone conversions to UTC, and apply strict deduplication filters. Canonical enterprise entities like `int_trips_deduped` and `int_driver_shifts` were created here once, establishing consistent business definitions.
3. **Gold Layer (Curated Data Marts & Dimensional Models)**: Constructed dimensional star schemas containing enriched fact tables (`fct_marketplace_trips_daily`) and slowly changing dimension tables (`dim_drivers`, `dim_riders`, `dim_hex_regions`). These tables are pre-joined, denormalized where appropriate, and physically **partitioned by day** and **clustered on high-cardinality query keys**.

To eliminate duplicated logic across teams, I published reusable **dbt semantic metrics** and modular macros for core calculations (e.g., active trip duration, surge yield, driver earnings net of tolls). I wrapped these models in comprehensive **dbt documentation** and automated lineage graphs, enabling non-technical stakeholders to build self-serve reports in **Power BI** and **Tableau** with complete confidence that all metrics aligned to a certified single source of truth."""
    },
    {
        "num": 7,
        "category": "Data Modeling, Warehousing & Modern Data Stack",
        "title": "Snowflake Performance Optimization: From 45 Minutes to Under 2 Minutes at Scale",
        "question": "At Dell Technologies, you optimized an unmanaged Snowflake data warehouse processing 5TB+ monthly volume, slashing query times from 45 minutes to under 2 minutes. What specific performance tuning and architectural techniques did you implement?",
        "answer": """When managing large-scale cloud data warehouses like **Snowflake**, explosive data growth without proactive architectural governance rapidly causes severe query degradation and astronomical compute billing. At **Dell Technologies**, our enterprise data warehouse was processing **5TB+ monthly volume** across hundreds of complex ETL transformations and analytical queries. Several mission-critical executive reporting pipelines were taking **45 minutes per run**, leading to compute warehouse queuing, high credit burn, and delayed business insights.

I diagnosed the root causes of this degradation and executed a multi-faceted performance optimization strategy:

1. **Eliminating Full Table Scans via Automatic Clustering**: I analyzed query execution profiles via Snowflake's `QUERY_PROFILE` graphical tool, discovering that frequent analytical queries were scanning 100% of micro-partitions (hundreds of gigabytes) due to natural data clustering aligned strictly with ingestion order rather than query filter predicates. I restructured our largest fact tables (storing order items, customer telematics, and inventory transactions) by defining optimal **Clustering Keys**:
```sql
ALTER TABLE enterprise_dw.fct_order_line_items 
CLUSTER BY (order_date, region_id, customer_account_id);
```
By aligning micro-partition boundaries with common `WHERE` and `JOIN` predicates, Snowflake's metadata pruning eliminated over 92% of partition reads, reducing I/O wait times exponentially.
2. **Materialized Views and Search Optimization Service (SOS)**: For high-frequency dashboard queries aggregating multi-billion-row datasets across fixed dimensions, I implemented **Snowflake Materialized Views**. Unlike standard views, materialized views maintain pre-computed aggregation results maintained automatically in the background. For point-lookup queries searching specific serial numbers or order IDs across 5TB+ tables, I enabled Snowflake's **Search Optimization Service**, turning sequential scans into sub-second indexed lookups.
3. **Warehouse Sizing & Multi-Cluster Auto-Scaling**: The existing configuration ran massive `4X-Large` virtual warehouses around the clock, causing resource contention between long-running ETL transformations and interactive ad-hoc BI queries. I separated compute workloads: I assigned dedicated `Medium` warehouses for scheduled ETL, while configuring a separate **Multi-Cluster Warehouse** with `AUTO_SUSPEND = 60` and `AUTO_RESUME = TRUE` for BI reporting. This eliminated queuing during peak business hours while preventing idle credit drain.
4. **Refactoring Query Anti-Patterns**: I audited legacy SQL queries, eliminating non-sargable expressions in `WHERE` clauses (e.g., replacing `WHERE TO_CHAR(order_timestamp, 'YYYY-MM') = '2023-10'` with explicit date boundary checks: `WHERE order_timestamp >= '2023-10-01' AND order_timestamp < '2023-11-01'`). I replaced Cartesian joins and unnecessary `DISTINCT` aggregations with window functions.

Together, these optimizations slashed peak query runtimes from **45 minutes to under 2 minutes**, reduced monthly Snowflake compute credit consumption by over **38%**, and established a sustainable governance framework for Dell's analytics engineering."""
    },
    {
        "num": 8,
        "category": "Data Modeling, Warehousing & Modern Data Stack",
        "title": "Dimensional Modeling Deep-Dive: Slowly Changing Dimensions (SCD Types 1, 2, 3, 4, 6)",
        "question": "Explain the architectural trade-offs between SCD Type 1, Type 2, Type 4, and Type 6. How do you implement SCD Type 2 tracking in modern data warehouses using dbt snapshots or SQL merges?",
        "answer": """In enterprise dimensional data modeling, capturing historical state changes in dimension entities—such as driver status changes at **Uber**, customer address moves at **Dell**, or vendor compliance tier adjustments at **Adani**—is fundamental to maintaining analytical accuracy over time:

1. **SCD Type 1 (Overwrite)**: Overwrites the old value directly. No historical record is preserved.
   - *Trade-off*: Simplest to implement, minimal storage footprint; however, historical attribution is lost forever. If a driver changes their registered home city from Chicago to Austin, all historical 2022 trips will retroactively appear as Austin trips.
2. **SCD Type 2 (Add New Row / Historical Tracking)**: Preserves complete historical context by inserting a new row whenever an tracked attribute mutates.
   - *Trade-off*: Preserves perfect historical truth; requires tracking columns: `valid_from_timestamp`, `valid_to_timestamp`, and `is_current_flag`. Slightly increases storage and requires range-based join conditions (`ON fact.timestamp BETWEEN dim.valid_from AND dim.valid_to`).
3. **SCD Type 4 (History Table / Split Architecture)**: Maintains the current state in a base table, while dumping all historical state mutations into a separate audit/history table.
   - *Trade-off*: Fast queries on current dimension state; historical queries require joining the history log.
4. **SCD Type 6 (Hybrid 1 + 2 + 3)**: Combines Type 1, 2, and 3. The row maintains both the historical row version (Type 2) and an explicit column storing the current active value (Type 1) alongside the prior historical value (Type 3).

**Implementing SCD Type 2 with dbt Snapshots**:
In modern data engineering workflows, implementing SCD Type 2 manually with verbose SQL `MERGE` statements is brittle and prone to concurrency deadlocks. In my projects, I implement SCD Type 2 using **dbt Snapshots**, which automatically detect schema mutations and handle timestamp intervals:
```sql
{% snapshot dim_driver_scd2 %}
{{
    config(
      target_schema='curated_dimensions',
      unique_key='driver_id',
      strategy='check',
      check_cols=['vehicle_license_plate', 'tier_status', 'payout_city'],
      invalidate_hard_deletes=True
    )
}}
SELECT 
    driver_id,
    vehicle_license_plate,
    tier_status,
    payout_city,
    updated_at
FROM {{ source('marketplace_raw', 'drivers') }}
{% endsnapshot %}
```
When dbt executes the snapshot, it computes a cryptographic hash across the monitored `check_cols`. If a hash change is detected, it automatically sets `dbt_valid_to = CURRENT_TIMESTAMP()` on the existing active row and inserts a new active record with `dbt_valid_to = NULL`, establishing a robust, audit-proof historical dimension tracking pipeline."""
    },
    {
        "num": 9,
        "category": "Data Modeling, Warehousing & Modern Data Stack",
        "title": "Partitioning, Clustering, and Sharding: Physical Warehouse Architecture",
        "question": "What are the core differences between partitioning, clustering, and sharding in modern cloud warehouses (BigQuery, Snowflake)? How do you choose the optimal strategy to maximize performance and minimize scan costs?",
        "answer": """In enterprise cloud data platforms like **GCP BigQuery** and **Snowflake**, physical storage layout directly governs both query latency and financial compute cost. Because modern cloud warehouses bill primarily based on compute time (Snowflake credits) or scanned data volume (BigQuery $6.25 per TB on on-demand pricing), understanding the distinct mechanics of **partitioning**, **clustering**, and **sharding** is critical for any Senior Data Engineer:

1. **Partitioning (Coarse-Grained Physical Segmentation)**:
   - *Mechanics*: Physically divides a table into distinct storage segments based on a low-to-medium cardinality column (most commonly date/timestamp, or integer ranges). In BigQuery, partitions are explicit physical blocks (e.g., partitioned by `DATE(event_timestamp)`).
   - *Cost & Performance Impact*: Enables **Partition Pruning**. If a query specifies `WHERE event_date BETWEEN '2026-10-01' AND '2026-10-07'`, BigQuery completely skips scanning partitions for the rest of the year, reducing scanned bytes by over 95%.
   - *Best Practice*: Use for high-frequency time-series filters. Avoid high-cardinality columns (e.g., `user_id`), as BigQuery enforces a hard limit of 10,000 partitions per table.

2. **Clustering (Fine-Grained Colocation Within Partitions)**:
   - *Mechanics*: Within each partition, clustering physically sorts and co-locates rows based on one or more designated clustering columns (e.g., `marketplace_region_id`, `event_type`). 
   - *Cost & Performance Impact*: Enables **Block-Level Pruning**. In both BigQuery and Snowflake (via micro-partitions), metadata stores the minimum and maximum value for each clustered column within each storage block. When a query filters by a clustered column, the execution engine skips reading non-matching blocks within the partition.
   - *Best Practice*: Use for high-cardinality columns frequently utilized in equality filters, range filters, or `GROUP BY` / `JOIN` operations. In BigQuery, up to 4 clustering columns can be specified; order matters (declare highest-priority query filter columns first).

3. **Sharding (Horizontal Distributed Segmentation)**:
   - *Mechanics*: An older architecture (e.g., creating separate tables per day: `table_20261001`, `table_20261002`, or sharding across distinct physical database nodes in PostgreSQL/MySQL).
   - *Trade-off*: Heavily discouraged in modern cloud warehouses because managing table unions degrades metadata performance, complicates schema migrations, and prevents cross-partition query optimizations.

**My Rule of Thumb**: For multi-terabyte transactional tables, implement **Time-Unit Partitioning** on `event_timestamp` for macro-level partition elimination, combined with **Multi-Column Clustering** on high-cardinality join keys (`region_id`, `customer_id`) for micro-level block skipping."""
    },
    {
        "num": 10,
        "category": "Data Modeling, Warehousing & Modern Data Stack",
        "title": "Role-Based Access Control (RBAC), Column-Level Masking, and Security Governance",
        "question": "At Dell, you implemented role-based security across Snowflake at a 5TB+ monthly volume. How do you design and enforce granular data security, dynamic data masking, and row-level access policies without degrading query performance?",
        "answer": """In enterprise healthcare, financial, and technology environments, data engineers must balance broad analytical data democratization with strict compliance standards (GDPR, HIPAA, SOC 2). At **Dell Technologies**, managing **5TB+ monthly volume** across 50+ integrated enterprise source systems required architecting a bulletproof security governance model. We had hundreds of users—ranging from regional sales analysts and third-party contractors to C-suite executives—querying shared Snowflake datasets containing sensitive **Personally Identifiable Information (PII)** and proprietary financial transaction details.

To resolve this challenge, I designed a multi-layered security architecture in **Snowflake** combining **Role-Based Access Control (RBAC)**, **Dynamic Data Masking**, and **Row-Level Access Policies**:

1. **Hierarchical RBAC Architecture**: I established a clean, functional role hierarchy separating object administration from analytical access. Functional roles (e.g., `DATA_ANALYST_US`, `FINANCE_AUDITOR`, `ENGINEERING_PROD`) inherit permissions from underlying access roles (`READ_SILVER_SALES`, `READ_GOLD_FINANCE`). Users are assigned strictly to functional roles, ensuring the principle of least privilege.
2. **Dynamic Column-Level Data Masking**: To protect sensitive columns (credit card numbers, customer email addresses, tax IDs) without duplicating tables or creating separate views, I implemented **Snowflake Masking Policies**:
```sql
CREATE OR REPLACE MASKING POLICY security_governance.mask_pii_string AS (val STRING) 
RETURNS STRING ->
  CASE
    WHEN CURRENT_ROLE() IN ('FINANCE_AUDITOR', 'SECURITY_ADMIN') THEN val
    WHEN CURRENT_ROLE() LIKE '%ANALYST%' THEN REGEXP_REPLACE(val, '(?<=.{2}).(?=.*@)', '*')
    ELSE '***REDACTED***'
  END;

-- Attach masking policy directly to base table column
ALTER TABLE curated.dim_customers 
MODIFY COLUMN email_address SET MASKING POLICY security_governance.mask_pii_string;
```
When an unprivileged analyst queries `dim_customers`, Snowflake automatically evaluates the masking policy at query runtime, masking the email without incurring performance overhead or storage duplication.
3. **Row Access Policies (Row-Level Security)**: For data tenancy isolation, I authored **Row Access Policies** ensuring regional sales managers can view only records where `sales_region = CURRENT_ROLE_REGION()`.
4. **Zero Performance Degradation**: Because Snowflake evaluates masking and row-access policies at the query compilation layer, rewriting predicates before physical execution, query runtimes remain identical to native queries, protecting sub-2-minute query SLAs while ensuring 100% regulatory compliance."""
    },

    # =========================================================================
    # CATEGORY 3: BIG DATA PROCESSING & DISTRIBUTED COMPUTE (Q11 - Q15)
    # =========================================================================
    {
        "num": 11,
        "category": "Big Data Processing & Distributed Compute",
        "title": "Scaling Distributed ETL Pipelines: PySpark, AWS EMR, Hadoop, and Hive",
        "question": "At Dell Technologies, you integrated 50+ enterprise systems using Python, Java, Scala, Apache Spark, and AWS EMR. How do you architect, tune, and scale high-volume distributed compute pipelines across heterogeneous architectures?",
        "answer": """At **Dell Technologies**, our enterprise data infrastructure was fragmented across 50+ heterogeneous enterprise source systems—ranging from on-premises **Oracle** and **SQL Server** relational databases to legacy **Hadoop/Hive clusters**, mainframe flat-files, and cloud object stores. Business units lacked a centralized single pane of glass, resulting in severe data-access silos and high operational latency.

To unify these systems, I architected a distributed big data platform on **AWS EMR (Elastic MapReduce)** running **Apache Spark** (leveraging **Scala** for high-throughput compute-heavy transformations and **Python/PySpark** for analytical transformation pipelines):

```mermaid
flowchart LR
    A[50+ Source Systems: Oracle, Mainframe, SQL Server] --> B[Data Lake Staging: Amazon S3 Bronze]
    B --> C[AWS EMR Cluster: Apache Spark / Hive Compute]
    C --> D[Partition Pruning, Dynamic Allocation & Broadcast Joins]
    D --> E[Curated Parquet Lakehouse: Amazon S3 Gold]
    E --> F[Curated Serving: Snowflake / Power BI]
```

1. **Optimized Ingestion & Cluster Provisioning**: I designed scalable ingestion workflows extracting transactional change logs from source systems into an **Amazon S3** data lake (utilizing the open-source **Parquet** columnar format with **Snappy compression**). For compute, I provisioned transient **AWS EMR clusters** managed via **Apache Airflow**, pairing cost-effective **EC2 Spot Instances** for Spark core/task workers with on-demand instances for the master node. This decoupled compute from storage, slashing infrastructure costs by over 45%.
2. **Spark Performance Optimization**: Processing multi-terabyte datasets across 50+ upstream feeds frequently caused out-of-memory errors and shuffle bottlenecks. I executed deep Spark performance tuning:
   - **Managing Partitions**: Avoided the 'small files problem' by consolidating input files using `spark.sql.files.maxPartitionBytes = 134217728` (128MB) and tuning `spark.sql.shuffle.partitions` dynamically based on data volume.
   - **Broadcast Hash Joins**: When joining multi-billion-row transactional event tables with smaller dimension lookups (e.g., enterprise product catalogs < 50MB), I forced **Broadcast Joins** (`broadcast(dim_df)`), entirely eliminating costly distributed shuffle operations across worker nodes.
   - **Memory Management**: Optimized Spark executor memory configurations: allocating `spark.executor.memory = 16g`, `spark.executor.cores = 4`, and tuning off-heap overhead (`spark.executor.memoryOverhead = 2g`) to eliminate JVM garbage collection pauses.
3. **Unified Cataloging with AWS Glue & Hive Metastore**: I registered all processed Parquet datasets with the **AWS Glue Data Catalog / Hive Metastore**, enabling seamless SQL accessibility across both Athena ad-hoc querying and automated **Snowflake** stage loading.

This unified distributed pipeline consolidated 50+ heterogeneous enterprise feeds, reduced daily data integration latency from days to hours, and established a scalable foundation for enterprise analytics across Dell."""
    },
    {
        "num": 12,
        "category": "Big Data Processing & Distributed Compute",
        "title": "Diagnosing and Resolving Spark Bottlenecks: Data Skew, Salting, and Memory OOMs",
        "question": "What are the primary causes of Apache Spark Out-Of-Memory (OOM) errors and data skew? Walk through the exact techniques you use—such as salting, adaptive query execution, and repartitioning—to debug and resolve them.",
        "answer": """In distributed computing frameworks like **Apache Spark**, the most common cause of job failure or straggling tasks is **Data Skew** and **Memory Allocation Imbalances**. Data skew occurs when a non-uniform distribution of join or grouping keys causes a single worker task to process 80% of the entire dataset while other executor nodes sit idle. Eventually, the saturated executor exhausts its heap or spill storage, throwing `java.lang.OutOfMemoryError: Java heap space` or `FetchFailedException`.

Throughout my work at **Dell Technologies** and **Uber**, I systematically diagnosed and resolved Spark memory and skew bottlenecks using a disciplined debugging playbook:

1. **Diagnosing Skew via Spark UI**: I inspect the **Spark UI Event Timeline** and **Task Metrics**. In the 'Stages' tab, I evaluate task duration histograms. If the 75th percentile task completes in 10 seconds, but the Max task runs for 45 minutes or crashes, this is the classic signature of data skew on the join/shuffle key (e.g., millions of records having a `NULL` or generic default customer ID).
2. **Key Salting Technique**: When joining two large datasets skewed on a specific key (e.g., `account_id = 'DEFAULT_CORP'`), a standard shuffle hash join concentrates all records onto a single partition. I resolve this by implementing **Key Salting**:
```python
import pyspark.sql.functions as F

# Step 1: Add a random salt (e.g., 0 to 9) to the skewed key in the primary large table
skewed_df_salted = large_df.withColumn(
    "salt", F.concat(F.col("account_id"), F.lit("_"), F.floor(F.rand() * 10))
)

# Step 2: Replicate the lookup dimension table 10x with corresponding salt values
lookup_replicated = small_df.withColumn("salt_array", F.array([F.lit(i) for i in range(10)])) \
    .withColumn("salt_suffix", F.explode("salt_array")) \
    .withColumn("salt", F.concat(F.col("account_id"), F.lit("_"), F.col("salt_suffix")))

# Step 3: Execute join on the salted key, distributing work uniformly across 10 executors
balanced_join_df = skewed_df_salted.join(lookup_replicated, on="salt", how="inner")
```
3. **Enabling Adaptive Query Execution (AQE)**: In modern Spark (3.x+), I enable `spark.sql.adaptive.enabled = true` and `spark.sql.adaptive.skewJoin.enabled = true`. AQE automatically monitors shuffle statistics at runtime; when it detects a partition significantly larger than the median, it dynamically splits the skewed partition into smaller sub-partitions.
4. **Resolving Executor OOMs**: For Driver OOMs caused by `df.collect()`, I mandate `take(N)` or export directly to storage. For Executor OOMs caused by memory pressure, I tune `spark.memory.fraction = 0.8`, increase off-heap memory, and eliminate Cartesian joins, stabilizing enterprise pipelines."""
    },
    {
        "num": 13,
        "category": "Big Data Processing & Distributed Compute",
        "title": "Spark Memory Management: Storage vs. Execution Memory and Garbage Collection Tuning",
        "question": "Deep-dive into Apache Spark's Unified Memory Architecture. How do you configure Storage vs. Execution memory, manage spilling to disk, and tune JVM Garbage Collection to prevent job failures?",
        "answer": """Understanding **Apache Spark's Unified Memory Management** model (introduced in Spark 1.6+) is essential for operating high-throughput big data pipelines without unpredictable executor crashes. A Spark executor JVM divides its total heap memory (`spark.executor.memory`) into four distinct regions:

1. **Reserved Memory**: Fixed at 300MB, reserved strictly for Spark internal system processes.
2. **User Memory**: Approximately 25% of remaining heap (calculated as `(Java Heap - 300MB) * (1 - spark.memory.fraction)`). Holds user-defined data structures, custom UDF buffers, and internal metadata.
3. **Spark Memory Pool (Unified Pool)**: Governed by `spark.memory.fraction` (default 0.60). This 60% of available memory is shared dynamically between two critical sub-regions:
   - **Execution Memory**: Allocated for shuffles, joins, aggregations, sorting, and window function calculations.
   - **Storage Memory**: Allocated for cached data (`.persist()`, `.cache()`) and broadcast variables.
   - *Dynamic Borrowing*: If no cached data occupies storage memory, execution can borrow 100% of the storage pool. If execution memory borrows space, cached storage data cannot evict active execution memory; execution always takes precedence to prevent task failure. However, if execution requires space borrowed by storage, cached partitions are evicted to disk or dropped based on the `StorageLevel`.

**Managing Spilling to Disk**:
When combined execution memory is exhausted during heavy shuffles (e.g., multi-way joins), Spark is forced to **spill data to disk** (`Spill (Memory)` vs. `Spill (Disk)` in Spark UI). Disk spilling severely degrades performance due to serialized disk I/O. I mitigate spilling by:
- Increasing `spark.sql.shuffle.partitions` to reduce data volume processed per task.
- Allocating adequate off-heap memory (`spark.memory.offHeap.enabled = true` and `spark.memory.offHeap.size = 4g`), allowing Tungsten to manage raw binary memory outside the JVM garbage collector.

**Tuning JVM Garbage Collection (GC)**:
In heavy Spark workloads, long JVM 'Stop-The-World' GC pauses cause executors to drop heartbeats to the driver, triggering false task failures. In my **AWS EMR** cluster configurations, I replace the legacy ParallelGC with the modern **G1GC (Garbage-First Garbage Collector)**:
```bash
spark.executor.extraJavaOptions=-XX:+UseG1GC -XX:InitiatingHeapOccupancyPercent=35 -XX:G1ReservePercent=15
```
G1GC splits the heap into discrete regions, collecting short-lived objects incrementally. Setting `InitiatingHeapOccupancyPercent=35` initiates background GC cycles before the heap becomes saturated, eliminating multi-minute pause storms and stabilizing long-running big data pipelines."""
    },
    {
        "num": 14,
        "category": "Big Data Processing & Distributed Compute",
        "title": "Apache Spark vs. Trino / Presto vs. BigQuery: Engine Selection for Analytics and ETL",
        "question": "How do you evaluate whether to run transformations in an engine like Apache Spark, an interactive MPP query engine like Trino/Presto, or a cloud-native serverless engine like GCP BigQuery?",
        "answer": """In enterprise data platform architecture, selecting the correct compute engine for a specific workload is the difference between sub-second dashboards and runaway cloud infrastructure costs. During my tenures across **Uber**, **Dell Technologies**, and **Adani**, I operated heterogeneous compute fabrics spanning **Apache Spark on AWS EMR**, **Apache Drill/NiFi**, and **GCP BigQuery**, learning to map workloads to engine strengths based on strict architectural criteria:

| Evaluation Dimension | Apache Spark (PySpark/Scala) | Trino / Presto (MPP Query Engine) | GCP BigQuery (Serverless Cloud DW) |
| :--- | :--- | :--- | :--- |
| **Core Architecture** | General-purpose distributed compute with disk/memory state checkpointing | In-memory distributed Massively Parallel Processing (MPP) query engine | Fully managed serverless distributed columnar warehouse (Dremel/Colossus) |
| **Fault Tolerance & Resilience** | **Highest**. Task-level lineage recovery; can recompute a single failed partition | **Low**. In-memory streaming pipelined; if one node fails, entire query fails | **High**. Serverless slot virtualization managed automatically by Google |
| **Optimal Workload Profile** | Heavy, long-running batch ETL/ELT; complex ML feature engineering; unstructured data | Interactive ad-hoc querying; cross-system federation across heterogeneous DBs | Curated data marts; business intelligence; high-concurrency SQL analytics |
| **Storage Coupling** | Decoupled (reads S3, HDFS, GCS, ADLS) | Decoupled (reads Hive, Cassandra, Iceberg, Postgres) | Decoupled physically (Colossus), but native BigQuery tables optimized |

**Engine Selection Decision Framework**:
1. **Choose Apache Spark when**: Processing heavy, long-running ETL transformations involving complex multi-stage shuffles, custom Python/Java algorithmic logic, machine learning feature engineering, or unstructured/semi-structured file transformations (JSON/XML/Parquet). If a job takes 3 hours and node preemption is common on Spot instances, Spark's task-level fault tolerance is mandatory.
2. **Choose Trino / Presto when**: Analysts require interactive, low-latency ad-hoc SQL querying across federated enterprise data sources (e.g., joining real-time MongoDB customer documents with historical Hive/S3 tables) without moving the data.
3. **Choose GCP BigQuery when**: Building standardized enterprise data marts, powering executive **Power BI / Tableau** dashboards, and executing SQL-centric ELT modeled via **dbt**. BigQuery's serverless scaling requires zero infrastructure provisioning, dynamically assigning thousands of compute slots to handle multi-terabyte aggregations in seconds while offering predictable on-demand or capacity-based slot commitments."""
    },
    {
        "num": 15,
        "category": "Big Data Processing & Distributed Compute",
        "title": "Architecting Scalable File Layouts: Parquet, Delta Lake, Partitioning, and Compaction",
        "question": "Why is file layout critical in data lakehouse design? Compare Parquet, ORC, and Delta Lake, and explain how you address the 'Small Files Problem' through automated compaction pipelines.",
        "answer": """In cloud object storage architectures like **Amazon S3** and **Google Cloud Storage**, file format and file sizing directly determine query throughput and storage cost. Storing raw data as uncompressed row-based CSV or JSON is an enterprise anti-pattern: reading a single column requires scanning 100% of the dataset, while network serialization crushes compute performance.

**Comparing Modern Columnar & Lakehouse Formats**:
1. **Apache Parquet**: Columnar storage format organized into row groups and column chunks. Embeds rich metadata (min/max statistics, dictionary encoding, and run-length encoding) directly in file footers. Ideal for analytical queries scanning subsets of columns.
2. **Apache ORC**: Highly optimized for **Apache Hive** workloads; similar columnar layout with lightweight index structures.
3. **Delta Lake / Apache Iceberg / Hudi**: The modern **Lakehouse Layer**. Built on top of Parquet, Delta Lake adds an ACID transactional log (`_delta_log/`). This provides ACID transactions, time-travel auditing, schema enforcement, and concurrent read/write capabilities that standard Parquet on S3 lacks.

**The 'Small Files Problem' & Compaction Engineering**:
When streaming ingestion engines (like Kafka consumers, AWS Kinesis, or Azure Data Factory) write micro-batches every few seconds to object storage, millions of tiny files (10KB - 500KB) accumulate in S3 buckets. This creates massive metadata overhead:
- The storage system wastes time opening and closing HTTP connections.
- Compute engines spend 90% of execution time reading file headers and footers rather than processing data.

**How I Solved Small Files at Scale**:
At **Dell Technologies** and **Uber**, I architected automated **Compaction Pipelines** scheduled via **Apache Airflow**:
1. **Dynamic Ingestion to Staging**: Streaming workers write raw Parquet micro-batches into an ephemeral staging prefix (`s3://data-lake/staging/events/year=2026/month=10/day=23/`).
2. **Automated Spark Compaction Jobs**: Every 4 hours, an Airflow DAG triggers a lightweight Spark compaction job that reads the staging prefix, coalesces small partitions into target sizes of **128MB to 512MB**, and writes compacted files to the curated production bucket:
```python
# Spark compaction snippet
raw_small_files_df = spark.read.parquet("s3://data-lake/staging/events/...")
# Calculate target partition count: total_bytes / 256MB
target_partitions = max(1, int(raw_small_files_df.count() * estimated_row_size / (256 * 1024 * 1024)))
raw_small_files_df.repartition(target_partitions).write.mode("overwrite").parquet("s3://data-lake/curated/events/...")
```
3. **Delta Lake Auto-Compaction**: Where Delta Lake is deployed, I enable `delta.autoOptimize.optimizeWrite = true` and schedule periodic maintenance:
```sql
OPTIMIZE delta.`s3://data-lake/delta_table` ZORDER BY (event_type, marketplace_region_id);
```
Compacting small files into 256MB Parquet blocks eliminated metadata throttling and slashed downstream Spark and Snowflake query execution times by over **60%**."""
    }
]

print(f"Part 1 questions loaded successfully: {len(QUESTIONS_PART1)}")
