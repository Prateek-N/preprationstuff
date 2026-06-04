---
title: TCS Sandeep Prep Guide
description: PySpark, SQL, cloud & data quality interview Q&A notes
---

# 🔧 Technical — PySpark \& Apache Spark

## Q1. What is the difference between RDD, DataFrame, and Dataset in PySpark?

**RDD (Resilient Distributed Dataset)** is the fundamental data structure in **Apache Spark** — a low-level, immutable distributed collection of objects. It offers full control but lacks optimization because Spark's **Catalyst optimizer** cannot introspect into it. You need to write explicit transformations using **map**, **filter**, and **reduceByKey**, making it verbose and slower for complex pipelines.

**DataFrame** is a higher-level abstraction built on top of RDD. It organizes data into named columns, similar to a table in a relational database. DataFrames are optimized by the **Catalyst query optimizer** and the **Tungsten execution engine**, enabling efficient physical execution plans. This makes DataFrames significantly faster than raw RDDs for most use cases involving structured or semi-structured data. In **PySpark**, DataFrames are the most commonly used abstraction for ETL work.

**Dataset** is available in **Scala** and **Java** but not natively in **Python**. It combines the benefits of RDD's type safety with the optimization of DataFrames. Since Python is dynamically typed, **PySpark** doesn't expose the Dataset API separately — you work primarily with DataFrames.

In practice at **JPMC** or **Accenture**, when building pipelines on **Azure Databricks** or **AWS EMR**, DataFrames are preferred. They integrate seamlessly with **Apache Spark SQL**, support schema enforcement, and allow reading from diverse sources like **AWS S3**, **ADLS Gen2**, or **Amazon Redshift**. For unstructured or schema-less transformations, RDDs can still be useful as a fallback. Understanding the trade-offs between these three helps you choose the right level of abstraction based on performance, maintainability, and complexity of your business transformation logic.

***

## Q2. Explain Lazy Evaluation in PySpark and why it matters.

**Lazy evaluation** is a core design principle of **Apache Spark** where transformations on a **DataFrame** or **RDD** are not executed immediately. When you call a transformation like **filter()**, **groupBy()**, or **join()**, Spark records the operation in a **DAG (Directed Acyclic Graph)** but does not actually execute it. Execution is triggered only when an **action** such as **count()**, **collect()**, **show()**, or **write()** is called.[^2]

This is powerful because Spark's **Catalyst optimizer** can analyze the entire DAG before execution and apply optimizations such as **predicate pushdown**, **column pruning**, and **broadcast join decisions**. Without lazy evaluation, each transformation would execute immediately, preventing any global optimization across the pipeline.

In real-world data pipelines, this means if you chain 10 transformations — reading from **AWS S3**, filtering, joining with reference data, aggregating — Spark builds the plan first, then picks the optimal physical execution strategy across distributed **AWS EMR** or **Azure Databricks** clusters.

A common mistake is calling too many **actions** unnecessarily — for example, calling **count()** mid-pipeline to debug. Each action triggers a full job execution, which is expensive at scale. Instead, use **explain()** to inspect the logical and physical execution plan without actually running the job. Also, calling **cache()** or **persist()** before a frequently reused DataFrame ensures it's computed once and stored in memory, avoiding recomputation across multiple downstream actions.

Understanding lazy evaluation is critical when you're building pipelines that process **500K+ daily transaction records** or managing multi-TB datasets, as it directly impacts **cluster resource utilization**, **job latency**, and **cost efficiency** on cloud platforms.

***

## Q3. How do you handle Data Skewness in PySpark?

**Data skewness** occurs when data is unevenly distributed across partitions in a **Spark** cluster. A few partitions receive a disproportionately large amount of data — for example, when joining on a column like `customer_id` where one customer has millions of records while others have only a few. This leads to some **executors** being overloaded while others sit idle, causing **OOM (Out of Memory)** errors and dramatically increasing job execution time.[^1]

The first approach is **salting** — you artificially add a random prefix or suffix to the skewed key to spread the data across multiple partitions. After the operation, you strip the salt and aggregate the results. This is effective for heavily skewed **groupBy** or **join** operations.

The second approach is **broadcast join** — if one DataFrame is small enough (typically under **10MB by default**, configurable via `spark.sql.autoBroadcastJoinThreshold`), you broadcast it to all worker nodes instead of shuffling the large DataFrame. This avoids expensive **shuffle operations** entirely. In **PySpark**, you use `broadcast()` from `pyspark.sql.functions`.

Third, **repartitioning** using `repartition()` or `coalesce()` helps redistribute data more evenly. Use `repartition(n, col)` when you want to shuffle data based on a specific column to ensure even distribution before a join or aggregation.

Fourth, **AQE (Adaptive Query Execution)** in **Spark 3.x** automatically detects skew at runtime and splits skewed partitions. Enabling `spark.sql.adaptive.enabled=true` and `spark.sql.adaptive.skewJoin.enabled=true` allows Spark to handle skew dynamically without manual intervention.

At **JPMC**, when processing large-scale risk data across **12 upstream sources**, understanding and mitigating skewness is critical to ensuring pipeline **SLA adherence** and cost-efficient processing on **Azure Databricks** or **AWS EMR**.

***

## Q4. What is the difference between `cache()` and `persist()` in PySpark?

Both **`cache()`** and **`persist()`** in **PySpark** are used to store a **DataFrame** or **RDD** in memory to avoid recomputation when the same data is accessed multiple times in a pipeline. The key difference lies in the **storage level** they use.[^2]

**`cache()`** is a shorthand that uses the default storage level of **MEMORY\_AND\_DISK**. This means Spark first tries to store the data in memory. If memory is insufficient, it spills the remainder to disk. It's quick to use but doesn't give you control over storage behavior.

**`persist()`** gives you explicit control over the **storage level**. Available options include `MEMORY_ONLY`, `MEMORY_AND_DISK`, `DISK_ONLY`, `MEMORY_ONLY_SER` (serialized), and `OFF_HEAP`. For example, `MEMORY_ONLY_SER` stores data in a serialized format, reducing memory usage at the cost of CPU overhead for serialization/deserialization.

In practice, if you have a large **reference dataset** used across multiple join operations — such as a lookup table for product categories or currency exchange rates — you **persist()** it with `MEMORY_AND_DISK` to ensure it's always available without recomputation, even when memory is under pressure on **Azure Databricks** or **AWS EMR** clusters.

Always call **`unpersist()`** explicitly once the cached DataFrame is no longer needed. Failing to do so causes memory pressure and can degrade performance for subsequent stages in long-running pipelines.

In the context of processing **\$1.4B in portfolio risk metrics** at **JPMC**, strategically caching shared reference data across multiple downstream aggregation jobs significantly reduces **job execution time** and **cluster compute costs** on cloud platforms.

***

## Q5. How do you optimize a slow PySpark job in production?

Optimizing a slow **PySpark** job requires a methodical approach. The first step is to use **`explain()`** to inspect the **logical and physical execution plan**, identify expensive operations like **full shuffles**, **Cartesian products**, or **multiple stages** caused by unnecessary wide transformations.[^1]

Next, check **partition count**. Too few partitions means underutilized parallelism; too many means excessive overhead. A good starting point is **2-3x the number of cores** available in the cluster. Use `repartition()` for even distribution and `coalesce()` to reduce partitions without a full shuffle when writing output.

**Broadcast joins** should be used when one DataFrame is small. Large shuffles from **sort-merge joins** are expensive; replacing them with broadcast joins eliminates shuffle entirely. Check `spark.sql.autoBroadcastJoinThreshold` and configure it appropriately.

**Predicate pushdown** and **column pruning** are handled automatically by the **Catalyst optimizer** but only work correctly when reading from optimized formats like **Parquet** or **Delta Lake**. Avoid reading entire datasets when only a few columns are needed. Reading from **AWS S3** or **ADLS Gen2** in columnar **Parquet** format with partition pruning can reduce I/O by over 80%.

Enable **AQE (Adaptive Query Execution)** with `spark.sql.adaptive.enabled=true` for Spark 3.x. AQE dynamically re-optimizes query plans at runtime based on actual data statistics — adjusting join strategies and coalescing shuffle partitions automatically.

Also review **garbage collection (GC) logs** and **executor memory configuration** (`spark.executor.memory`, `spark.memory.fraction`). OOM errors and long GC pauses are common culprits in pipelines processing large-scale data on **AWS EMR** or **Azure Databricks**. At **Accenture**, applying these techniques reduced implementation timelines from **9 months to 6 months** for Fortune 500 supply chain pipelines.

***

# 🛢️ SQL \& Data Modeling

## Q6. What are Window Functions in SQL and when do you use them?

**Window functions** in **SQL** perform calculations across a set of rows related to the current row without collapsing the result set like **GROUP BY** does. They are defined using the **OVER()** clause and are critical for analytical queries in data warehousing environments like **Amazon Redshift**, **Azure Synapse Analytics**, and **Google BigQuery**.[^3]

Common window functions include **ROW\_NUMBER()**, **RANK()**, **DENSE\_RANK()**, **LAG()**, **LEAD()**, **SUM() OVER**, and **AVG() OVER**. For example, `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY transaction_date DESC)` assigns a sequential number to each transaction per customer ordered by date — useful for identifying the latest record per customer.

**LAG()** and **LEAD()** are particularly useful in time-series analysis — for example, comparing a customer's current month spending with the previous month without a self-join. This is far more efficient than traditional approaches using **CTEs** or subqueries.

In a **dimensional data model** built on **Azure Synapse Analytics**, window functions are used extensively for computing **running totals**, **moving averages**, **percentile rankings**, and **period-over-period comparisons** that power executive dashboards. At **JPMC**, enabling **60 senior stakeholders** to access consolidated risk metrics through **Tableau** and **Amazon QuickSight** relied on efficient SQL queries using window functions.

You can partition by multiple columns and define custom window frames using `ROWS BETWEEN` or `RANGE BETWEEN` for sliding window calculations. Always ensure the columns used in `PARTITION BY` and `ORDER BY` are indexed or sorted in the underlying **Redshift** or **Synapse** storage to avoid full scans, improving query performance on multi-billion-row tables.

***

## Q7. Explain Star Schema vs Snowflake Schema in data warehousing.

**Star schema** and **snowflake schema** are both approaches to **dimensional data modeling** used in **data warehouses** built on platforms like **Amazon Redshift**, **Azure Synapse Analytics**, and **Google BigQuery**. The choice between them affects query performance, storage, and maintainability.[^1]

In a **star schema**, a central **fact table** is directly connected to multiple **dimension tables**. Dimension tables are denormalized — meaning all descriptive attributes are stored in a single flat table without further normalization. For example, a `sales_fact` table connected to `date_dim`, `customer_dim`, and `product_dim`. This design results in fewer joins, simpler queries, and faster read performance, making it ideal for **OLAP** reporting and **BI dashboards**.

In a **snowflake schema**, dimension tables are normalized into multiple related tables. For example, `customer_dim` might reference a `city_dim` which references a `country_dim`. This reduces data redundancy and storage footprint but introduces additional joins, which can slow down query performance on large datasets.

**Data Vault 2.0** is a third modeling approach used for enterprise-scale data warehouses. It separates business keys (**Hubs**), relationships (**Links**), and descriptive attributes (**Satellites**), making it highly flexible for integrating data from diverse sources and supporting full historical tracking. At **Accenture**, contributing to a **\$3M enterprise data warehouse** required understanding and implementing these modeling patterns across **8 heterogeneous data sources**.

In practice, most modern **cloud data warehouses** favor **star schemas** for their analytical simplicity. When building **dimensional models** on **Azure Synapse Analytics** for risk reporting at **JPMC**, star schema was the preferred choice to support fast aggregation and reporting for **\$1.4B in portfolio risk metrics** across multiple business units.

***

## Q8. How do you write a query to find the second highest salary without using TOP or LIMIT?

This is a classic **SQL** interview question that tests your knowledge of **subqueries**, **window functions**, and **set-based thinking** — core skills for any data analyst working with large-scale databases like **Amazon Redshift**, **Oracle**, or **Microsoft SQL Server**.[^1]

**Approach 1 — Subquery:**

```sql
SELECT MAX(salary)
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

This finds the maximum salary excluding the highest, effectively returning the second highest. However, it fails if multiple employees share the highest salary value and you want distinct salary ranks.

**Approach 2 — Window Function (preferred):**

```sql
SELECT salary
FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
) ranked
WHERE rnk = 2;
```

Using **`DENSE_RANK()`** ensures that if two employees share the highest salary, the next distinct salary level is still ranked 2. **`ROW_NUMBER()`** would skip rank 2 in case of ties, and **`RANK()`** would leave gaps — so `DENSE_RANK()` is the correct choice here.

**Approach 3 — Correlated Subquery:**

```sql
SELECT DISTINCT salary
FROM employees e1
WHERE 1 = (
  SELECT COUNT(DISTINCT salary) FROM employees e2
  WHERE e2.salary > e1.salary
);
```

This is more flexible and can be generalized to find the **Nth highest salary** by replacing `1` with `N-1`.

In production environments like **Azure Synapse Analytics** or **Amazon Redshift**, window function approaches are preferred as they leverage **Massively Parallel Processing (MPP)** architecture for efficiency. Subquery-based approaches can lead to full table scans on large datasets, causing **query performance degradation** in reporting layers serving executive dashboards.

***

## Q9. What is a CTE (Common Table Expression) and when would you use it over a subquery?

A **CTE (Common Table Expression)** is a temporary named result set defined using the **WITH** clause in **SQL**. It improves code readability and modularity, especially for complex multi-step analytical queries common in **data warehousing** environments like **Amazon Redshift**, **Azure Synapse Analytics**, and **Google BigQuery**.[^3]

The key advantage of a CTE over a subquery is **readability**. When you have deeply nested subqueries, CTEs allow you to break the logic into named, reusable blocks. For example:

```sql
WITH high_value_customers AS (
  SELECT customer_id, SUM(amount) AS total_spend
  FROM transactions
  GROUP BY customer_id
  HAVING SUM(amount) > 10000
)
SELECT c.name, h.total_spend
FROM customers c
JOIN high_value_customers h ON c.id = h.customer_id;
```

**Recursive CTEs** are another powerful feature — they allow hierarchical traversal such as building org charts, category trees, or processing bill-of-materials structures. Using `WITH RECURSIVE` syntax in **PostgreSQL** or `WITH (MAXRECURSION)` in **SQL Server**, you can traverse parent-child relationships without complex procedural logic.

In terms of **performance**, CTEs and subqueries are often treated identically by query optimizers in modern systems like **Amazon Redshift** or **Azure Synapse**. However, in **SQL Server** and some other engines, CTEs can sometimes be materialized, leading to performance differences depending on the query plan.

At **KPMG**, writing **SQL-based ETL workflows** to ingest data from **15 stakeholder systems** into **Amazon Redshift** required organizing multi-step business rules into readable CTEs rather than deeply nested subqueries — reducing review time during **UAT** and making **source-to-target mapping** documentation easier to maintain for compliance audits serving **2M end users**.

***

## Q10. How do you handle NULL values in SQL and Python/PySpark?

Handling **NULL values** is a critical part of **data quality engineering** and affects downstream analytics, aggregations, and join behavior. A clear strategy for managing NULLs demonstrates maturity in building production-grade **data pipelines**.[^3]

In **SQL**, NULL represents an unknown or missing value. Key behaviors to understand: any arithmetic or comparison with NULL returns NULL. For example, `NULL = NULL` is **FALSE** — use `IS NULL` or `IS NOT NULL` for comparisons. Use **`COALESCE(col, default_value)`** to replace NULLs with a fallback, and **`NULLIF(col, value)`** to convert a specific value to NULL. In aggregation functions like `SUM()` and `AVG()`, NULLs are automatically ignored — but `COUNT(*)` counts all rows including NULLs, while `COUNT(column)` excludes them.

In **PySpark**, NULLs can be handled using:

- **`df.fillna(value, subset=[cols])`** — replaces NULLs with a default value
- **`df.dropna(subset=[cols])`** — removes rows with NULLs in specified columns
- **`df.na.replace()`** — replaces specific values including NULLs
- **`when(col.isNull(), replacement).otherwise(col)`** — for conditional logic

For large-scale pipelines processing millions of records, NULL handling must be applied upstream during the **ingestion and transformation layer** before data is loaded into **Amazon Redshift** or **Azure Synapse Analytics**. Unchecked NULLs propagating into **star schema** fact tables can corrupt **KPI calculations** on **Tableau** or **Power BI** dashboards.

At **JPMC**, the **SQL and Python-based data quality frameworks** deployed on **Azure Databricks** explicitly validated NULL percentages per column against defined thresholds before allowing data to flow into downstream **risk reporting** layers — helping reduce **production data defects from 40 incidents per quarter to fewer than 5**.

***

# ☁️ Cloud \& ETL Architecture

## Q11. What is the difference between AWS Glue and Azure Data Factory?

**AWS Glue** and **Azure Data Factory (ADF)** are both managed **ETL and data integration services**, but they differ in architecture, compute model, and best-use scenarios — and both are heavily used across Sandeep's experience at **JPMC** and **Accenture**.[^1]

**AWS Glue** is a serverless **ETL service** that automatically provisions and scales **Apache Spark** compute. It integrates tightly with **AWS S3**, **Amazon Redshift**, **AWS Athena**, and the **AWS Glue Data Catalog** for metadata management. Glue jobs are written in **Python** or **Scala**, leveraging **PySpark** for distributed processing. The **Glue Data Catalog** acts as a centralized metadata repository compatible with **Athena** and **EMR**. Glue also supports **Data Quality checks** natively through **AWS Glue Data Quality**.

**Azure Data Factory (ADF)** is a cloud-based **data integration and orchestration service** in the **Azure** ecosystem. It uses a visual interface with **pipelines**, **datasets**, and **linked services** to define workflows. ADF's **Mapping Data Flows** allow code-free transformations at scale. For heavy processing, ADF integrates with **Azure Databricks** as a compute engine, leveraging **PySpark** for complex transformations. ADF also supports integration with **ADLS Gen2**, **Azure Synapse Analytics**, and **Azure Purview** for lineage tracking.

The key architectural difference is that **AWS Glue** provides integrated Spark compute, while **ADF** is primarily an orchestrator that delegates heavy computation to **Azure Databricks** or **Azure HDInsight**. ADF excels at low-code orchestration with strong native Azure service integration; Glue is better for code-heavy, serverless **Spark-based ETL** on **AWS**.

Both tools support **incremental data loading**, **error handling**, **pipeline monitoring**, and **alerting** — critical for maintaining pipeline reliability in enterprise environments serving multi-billion-dollar financial portfolios.

***

## Q12. How would you design an incremental data pipeline?

An **incremental data pipeline** loads only new or changed records since the last execution rather than reprocessing the entire dataset. This is fundamental for efficiency in large-scale **cloud data warehousing** on **Amazon Redshift**, **Azure Synapse Analytics**, or **Google BigQuery**.[^1]

The most common strategy is **watermark-based incremental loading**. You maintain a **high-watermark** — typically a **timestamp** or **auto-increment ID** — in a **metadata control table** stored in **Amazon RDS** or **Azure SQL**. Each pipeline run reads records where `updated_at > last_run_timestamp`, processes them, then updates the watermark upon successful completion.

For **SCD Type 2 (Slowly Changing Dimensions)**, incremental logic needs to close existing records and insert new versions. In **PySpark**, this is handled using **`MERGE`** statements in **Delta Lake** on **Azure Databricks** or **Amazon Redshift Spectrum**. The `MERGE INTO` command allows upsert logic — matching on a business key and either updating existing rows or inserting new ones in a single atomic operation.

**Event-driven incremental loading** is another approach — using **AWS Lambda** triggered by **S3 file arrival events**, or **Azure Event Grid** triggering **Azure Functions** to kick off **ADF pipelines** or **Glue jobs** as soon as new data lands. **Apache Kafka** or **AWS Kinesis** can be used for near-real-time streaming ingestion into **Delta Lake** or **Redshift**.

At **KPMG**, designing **SQL-based ETL workflows** to ingest data from **15 stakeholder systems** into **Amazon Redshift** used watermark-based incremental logic to process **500K+ daily transaction records** efficiently, ensuring **schema consistency** and **referential integrity** without full reloads — directly supporting **SLA adherence** for compliance platforms serving **2M end users**.

***

## Q13. Explain the difference between ETL and ELT and when to use each.

**ETL (Extract, Transform, Load)** and **ELT (Extract, Load, Transform)** are two architectural patterns for data pipeline design. The key difference is where and when the transformation happens — and modern **cloud data platforms** have significantly shifted industry preference toward **ELT**.[^1]

In **ETL**, raw data is extracted from source systems, transformed in an intermediary compute layer (like **Apache Spark on AWS EMR** or an **on-premise ETL tool**), and only then loaded into the target **data warehouse**. This approach was dominant when data warehouses had limited compute capacity and transformations needed to happen before loading. The downside is that intermediate transformation logic is tightly coupled to pipeline code and harder to iterate on.

In **ELT**, raw data is first loaded as-is into a **data lake** or **data warehouse** — such as **AWS S3**, **ADLS Gen2**, or **Azure Synapse Analytics** — and then transformed using the warehouse's native compute power. Tools like **dbt (Data Build Tool)** are central to ELT — they run **SQL-based transformations** directly inside **Amazon Redshift**, **BigQuery**, or **Snowflake**, creating modular, version-controlled transformation layers.

**ELT is preferred** in modern cloud architectures because cloud warehouses like **Amazon Redshift**, **Azure Synapse**, and **BigQuery** are massively parallel and cost-effective for transformation at scale. It also enables better **data lineage tracking** through **Azure Purview** or **AWS Glue Data Catalog**, since raw data is always preserved.

**ETL** is still used when data needs to be **masked or anonymized** before landing in the warehouse (e.g., PII data), or when transformations are compute-intensive and better suited for **PySpark on Databricks** rather than warehouse SQL. At **Accenture**, both patterns were applied depending on client security and compliance requirements.

***

# 📊 Data Quality \& Governance

## Q14. How do you build a data quality framework in PySpark and SQL?

A robust **data quality framework** is essential for ensuring reliable analytics and regulatory compliance. At **JPMC**, authoring **SQL and Python-based validation frameworks** reduced production data defects from **40 incidents per quarter to fewer than 5** — a concrete benchmark for what a well-designed framework can achieve.[^1]

The framework should cover four dimensions: **completeness** (no unexpected NULLs), **uniqueness** (no duplicate primary keys), **validity** (values within expected ranges or matching reference data), and **consistency** (cross-table referential integrity checks). Each dimension maps to specific checks implemented as **SQL assertions** or **PySpark DataFrame validations**.

In **PySpark**, you can implement checks using:

- **`df.filter(col("amount").isNull()).count()`** for NULL checks
- **`df.groupBy("transaction_id").count().filter("count > 1")`** for duplicate detection
- **`df.filter((col("amount") < 0) | (col("amount") > 1e9)).count()`** for range validation

Results of each check are written to a **data quality log table** in **Amazon Redshift** or **Azure Synapse Analytics**, storing check name, table name, row counts, failure counts, and timestamps. This enables **AWS CloudWatch** or **Azure Monitor** dashboards to surface quality trends over time.

**AWS Glue Data Quality** supports rule-based validation using the **DQDL (Data Quality Definition Language)**, allowing you to define rules like `ColumnValues "amount" > 0` and integrate checks natively into **Glue jobs** without writing custom code.

For **pipeline-level validation**, checks are embedded as a **quality gate stage** — if the failure rate exceeds a configured threshold, the pipeline halts, an alert is sent via **CloudWatch SNS** or **Azure Monitor**, and downstream loads are blocked. This prevents **data defects** from propagating into reporting layers and violating **regulatory compliance** obligations.

***

## Q15. What is Data Lineage and why is it important?

**Data lineage** is the ability to trace the origin, movement, transformation, and consumption of data across the entire **data pipeline** — from source systems through staging, transformation, and into the final **data warehouse** or **reporting layer**. It is a critical component of **data governance**, regulatory compliance, and root-cause analysis for data quality issues.[^1]

In enterprise environments, data lineage answers questions like: "Where did this `revenue` column in the **Tableau** dashboard come from?", "Which upstream source system caused last night's discrepancy in the risk report?", or "Which pipelines will be affected if we change the schema of this **Oracle** source table?" Without lineage, debugging **data incidents** becomes a time-consuming, manual process involving multiple teams.

Tools like **Azure Purview** (now Microsoft Purview) provide automated lineage tracking across **Azure Data Factory pipelines**, **Azure Databricks** notebooks, **ADLS Gen2**, and **Azure Synapse Analytics**. It captures column-level lineage automatically, showing exactly how each field in the output was derived from source fields through specific transformations.

On the **AWS side**, **AWS Glue Data Catalog** and **Amazon DataZone** provide lineage tracking across **Glue ETL jobs**, **Athena** queries, and **Redshift** tables. Integration with **OpenLineage** — an open standard — enables cross-platform lineage visualization.

At **Accenture**, leveraging **Azure Purview** for **metadata management and data lineage tracking** across an **\$800M supply chain data platform** reduced debugging time when schema changes propagated unexpected failures downstream. At **JPMC**, lineage documentation was critical for passing **regulatory audits** on pipelines feeding **\$1.4B in portfolio risk metrics**, demonstrating full traceability of every transformation applied to sensitive financial data.

***

# 🏗️ Scenario-Based Technical Questions

## Q16. Your PySpark job fails with an OOM (Out of Memory) error on the last shuffle step. How do you debug and fix it?

An **OOM (Out of Memory)** error in the **last shuffle step** of a **PySpark** job is one of the most common production issues in large-scale data engineering. The root cause is almost always that a **wide transformation** — like **groupBy**, **join**, or **repartition** — is generating shuffle data that exceeds the available memory of your **executors** on **AWS EMR** or **Azure Databricks**.[^1]

**Step 1 — Inspect the Spark UI.** Check the **Stages tab** to identify which stage is failing and how much shuffle data is being written/read. Look at **spill metrics** — if shuffle spill to disk is high, it means memory is insufficient. Also check executor memory usage and GC time.

**Step 2 — Increase executor memory.** Adjust `spark.executor.memory` and `spark.executor.memoryOverhead`. The overhead allocation (`spark.executor.memoryOverhead`) is often the culprit in shuffle-heavy jobs — increase it to at least **10-15% of executor memory** or a minimum of **384MB**.

**Step 3 — Increase shuffle partitions.** The default `spark.sql.shuffle.partitions` is **200**, which is often too low for large datasets. Increasing it to **500–2000** reduces the amount of data each partition handles, avoiding memory pressure per task.

**Step 4 — Check for data skewness.** If a single partition holds 80% of the data due to a skewed key, no amount of memory tuning will fully solve the problem. Apply **salting** or use **AQE's skew join optimization** with `spark.sql.adaptive.skewJoin.enabled=true`.

**Step 5 — Optimize joins.** Replace **sort-merge joins** with **broadcast joins** where one side is small. Use **`explain()`** to confirm the join strategy being used and validate optimization results before deploying to production pipelines processing millions of financial records.

***

## Q17. You discover a major data quality issue in a production pipeline. What are your steps?

Discovering a **data quality issue** in a production pipeline is a high-stakes scenario that requires a structured, calm, and systematic response — especially in regulated industries like **financial services** where pipelines support **\$1.4B in portfolio risk metrics** or compliance platforms serving **2M end users**.[^3]

**Step 1 — Contain the impact immediately.** Stop downstream loads to **Amazon Redshift**, **Azure Synapse Analytics**, or **reporting dashboards** by disabling the pipeline trigger in **Apache Airflow** or **Azure Data Factory**. Alert stakeholders through **Confluence** or **JIRA** to prevent business decisions being made based on corrupted data.

**Step 2 — Identify the scope.** Determine which records are affected, which time window is impacted, and which downstream tables or dashboards consumed the bad data. Use **AWS Glue Data Catalog** or **Azure Purview** lineage tracking to trace affected datasets. Run SQL queries on the data quality log table to pinpoint the first occurrence of the anomaly.

**Step 3 — Root cause analysis.** Examine source system changes — was there a schema change, a new NULL pattern, or a business rule change in an upstream **Oracle** or **PostgreSQL** system? Check pipeline code changes via **Git** commit history. Review **AWS CloudWatch** or **Azure Monitor** logs for pipeline execution anomalies.

**Step 4 — Fix and reprocess.** Apply the corrective transformation, validate results against expected counts and KPI values, then backfill the affected date range. Use **Delta Lake's time travel** feature if available to restore previous clean versions of affected tables.

**Step 5 — Post-incident review.** Update the **data quality framework** to add a new validation rule that would have caught this issue. Document in **Confluence** and create a **JIRA ticket** to add a **regression test case** to the pipeline validation suite to prevent recurrence.

***

## Q18. How would you design a pipeline to process 100 million daily records efficiently in PySpark?

Designing a pipeline to handle **100 million daily records** requires architectural decisions across **data format**, **partitioning strategy**, **compute configuration**, and **orchestration** — all of which directly impact throughput, cost, and reliability on **AWS EMR** or **Azure Databricks**.[^1]

**Data Format:** Always use **columnar formats** like **Parquet** or **Delta Lake** for storage on **AWS S3** or **ADLS Gen2**. These formats support **predicate pushdown** and **column pruning**, which dramatically reduce I/O when reading subsets of data. Parquet achieves 3-5x compression over CSV and JSON, reducing both storage costs and read times.

**Partitioning Strategy:** Partition data in **S3 or ADLS Gen2** by `year/month/day` or by a high-cardinality business key (e.g., `region`, `product_category`). This ensures that most pipeline runs only read the partitions they need, avoiding full dataset scans. Configure **Spark** to use partition discovery with `spark.sql.hive.convertMetastoreParquet=true`.

**Compute Configuration:** On **AWS EMR**, use **Spot Instances** for cost savings on non-critical batch jobs. Configure `spark.executor.instances`, `spark.executor.cores`, and `spark.executor.memory` based on cluster size. A typical configuration for 100M records might be 20 executors × 4 cores × 8GB memory each.

**Pipeline Orchestration:** Use **Apache Airflow** (or **Cloud Composer on GCP**) to schedule jobs with automatic **retry logic**, **SLA monitoring**, and **alerting via PagerDuty or SNS**. Break the pipeline into modular stages — ingestion, validation, transformation, load — to enable partial reruns without reprocessing the entire dataset.

**Incremental Loading:** Avoid full reloads where possible. Use **watermark timestamps** for incremental extraction and **Delta Lake MERGE** for upserts into the **data warehouse**, ensuring each run processes only the day's new records rather than the full 100M history.

***

# 🔗 Behavioral \& Situational Questions

## Q19. Tell me about a time you reduced data defects significantly in a production environment.

This is a high-impact story drawn from your **JPMC** experience, and you should structure it using the **STAR (Situation, Task, Action, Result)** framework to make it compelling for TCS interviewers evaluating both technical depth and business impact.[^3]

**Situation:** At **JPMorgan Chase**, the consumer banking division was experiencing **40 production data defects per quarter** across pipelines ingesting data from **12 upstream sources** into **Azure Databricks** and **AWS EMR**. These defects were causing incorrect figures in downstream **Tableau** and **Amazon QuickSight** dashboards used by **60 senior stakeholders** to monitor **\$1.4B in portfolio risk metrics**.

**Task:** I was tasked with designing and implementing a comprehensive **data quality framework** to proactively catch defects before they reached the reporting layer, without significantly increasing pipeline runtime or cost.

**Action:** I authored **SQL and Python-based validation frameworks** deployed on **Azure Databricks**, integrating checks for completeness, uniqueness, referential integrity, and business rule compliance. I implemented validation as a **quality gate** stage in **Apache Airflow** DAGs — if failure rates exceeded defined thresholds, pipelines would halt and send alerts via **AWS CloudWatch SNS**. I also set up **AWS Glue Data Quality** rules for serverless validation on the **AWS** side and created a centralized **data quality dashboard** in **Amazon QuickSight** to track defect trends over time.

**Result:** Within two quarters, production data defects dropped from **40 per quarter to fewer than 5** — a **87.5% reduction**. Additionally, the framework eliminated **850 monthly data discrepancies**, directly improving the accuracy of risk reporting. The framework became the standard quality template adopted across **4 enterprise platforms** at **JPMC**.

***

## Q20. Describe a time you translated complex technical requirements into pipeline specifications for non-technical stakeholders.

Bridging the gap between **business stakeholders** and **data engineering teams** is a core competency for a **Data Analyst** role at TCS's end client, and this is a skill explicitly highlighted throughout your career.[^3]

**Situation:** At **Accenture**, I was working on a **\$3M enterprise data warehouse** initiative for a Fortune 500 client. The business team had vague, high-level requirements: "We need real-time visibility into our supply chain performance across regions." Meanwhile, the engineering team needed precise **ETL logic**, **source-to-target mappings**, and **acceptance criteria** to build the pipelines.

**Task:** My role was to serve as the bridge — translating ambiguous business needs into actionable, unambiguous **pipeline specifications** and **BRDs (Business Requirements Documents)** that both sides could execute against.

**Action:** I conducted structured requirements elicitation workshops using **BPMN process diagrams** (created in **Lucidchart**) to visualize current-state data flows and identify gaps. I documented **35 detailed pipeline specifications** covering source system schemas, transformation logic, data types, null handling, SCD logic, and **acceptance criteria** for **UAT**. For each specification, I created a **source-to-target mapping document** registered in **AWS Glue Data Catalog** and **Azure Purview** for lineage tracking.

**Result:** The clarity provided by these documents reduced **development rework by 120 engineering hours per sprint** — engineers no longer had to loop back mid-sprint to clarify ambiguous requirements. The project delivery timeline was cut from **9 months to 6 months**, and the solution successfully ingested data from **8 heterogeneous data sources** including **Oracle**, **SQL Server**, and flat files into **Amazon Redshift** and **Azure Synapse Analytics**, delivering **real-time supply chain visibility** for **\$800M in operations**.

***

## Q21. Tell me about a time you identified a process automation opportunity and delivered measurable savings.

**Process automation** is one of the most valued competencies in modern data engineering teams, and your **JPMC** experience provides a compelling example of turning analytical thinking into **\$600K in annual labor savings**.[^3]

**Situation:** At **JPMorgan Chase**, I observed that multiple data handling workflows across the consumer banking division were still being performed manually — teams were manually triggering **ETL jobs**, performing **data reconciliation** in Excel, and re-running failed pipeline steps through command-line interfaces. This was consuming significant engineering bandwidth and introducing human error risk.

**Task:** I was given ownership to analyze these workflows and identify automation opportunities that could reduce manual labor while improving reliability and auditability.

**Action:** I conducted a formal **BPMN process analysis** across 7 identified workflows, mapping each step, decision point, and handoff to quantify the time and cost involved. I then designed and implemented automated replacements using **AWS Glue jobs** for scheduled data processing and **AWS Step Functions** to orchestrate **serverless workflows** across multiple dependent Lambda functions and Glue steps. Each workflow included automatic retry logic, **CloudWatch alarm** integration for failure alerting, and **audit logging** to **S3** for compliance traceability.

**Result:** The **7 automated workflows** eliminated the equivalent of several full-time engineering roles' worth of manual effort — delivering **\$600K in annual labor savings** through the elimination of repetitive manual data handling. Pipeline execution became deterministic, auditable, and self-healing, directly improving **SLA adherence** and reducing incident tickets logged in **ServiceNow**. This initiative became a reference architecture for automation within the team and was documented in **Confluence** as a reusable pattern for future pipeline automation at the division level.

***

## Q22. How do you prioritize tasks when working on multiple data pipelines and stakeholder demands simultaneously?

Effective **prioritization** under competing demands is a behavioral competency that TCS evaluates heavily for client-facing roles, especially in large-scale data engineering programs where multiple pipelines, deadlines, and stakeholders coexist.[^3]

The approach begins with **impact and urgency assessment**. Not all pipeline failures or enhancement requests carry equal weight. A pipeline failure affecting **regulatory compliance reporting** for **2M end users** takes absolute precedence over a new feature request for an internal analytics dashboard. I use a simple **impact-urgency matrix** — high-impact, time-sensitive items go into the immediate sprint; low-impact requests are backlogged and re-prioritized in planning.

For ongoing delivery, I rely on **Agile ceremonies** — daily standups to flag blockers early, sprint planning to commit only to what's achievable, and retrospectives to refine estimation accuracy over time. Tracking work in **JIRA** with clearly defined **acceptance criteria** per ticket ensures transparency with both technical leads and business stakeholders about what's in progress and what's blocked.

**Stakeholder communication** is equally important. When conflicting priorities arise from different business owners — for example, the risk team and the compliance team both needing urgent pipeline fixes — I surface the conflict immediately to my manager and document the trade-off in **Confluence**, letting leadership make the final call rather than absorbing the conflict silently.

At **JPMC**, managing **4 enterprise platform deliveries simultaneously** while maintaining quality standards required this discipline rigorously. The result was consistently **accelerating project delivery by 3 weeks per release cycle** — achievable only because prioritization decisions were made transparently, early, and collaboratively with all stakeholders. Time-boxing investigation efforts on ambiguous issues (e.g., 2 hours max before escalating) also ensured momentum was maintained across parallel workstreams.

***

## Q23. How do you explain data quality issues or pipeline failures to non-technical stakeholders?

Communicating **technical failures** clearly to business stakeholders is one of the most underrated but heavily evaluated skills in a **Data Analyst** or **BA-heavy data engineering role** like the one at TCS's end client.[^3]

The core principle is **impact-first communication** — lead with what the business cares about (what's broken, who is affected, what decisions cannot be made right now) before explaining the technical root cause. For example, instead of saying "the Glue job failed due to a schema mismatch in the upstream Oracle table," you say: "The daily risk summary report has not been refreshed since last night. The **Tableau** dashboard your team uses for this morning's review is showing yesterday's figures. We have identified the issue and expect it to be resolved in 2 hours."

Use **plain language analogies** when the technical details are necessary. For instance, describing a **data pipeline** as a "series of automated conveyor belts that move and transform data from source systems to dashboards" helps stakeholders visualize the issue without needing to understand **PySpark** or **cloud architecture**.

Provide a **3-part update structure**: what happened, what is the impact, and what is the resolution plan with an ETA. Always include a confidence level on the ETA — "we expect resolution by 11 AM with 80% confidence; we'll confirm or update by 10 AM." This manages expectations without overpromising.

At **JPMC**, briefing **60 senior stakeholders** on pipeline reliability required this approach consistently. Creating a **data quality dashboard** in **Amazon QuickSight** that displayed pipeline health, defect counts, and SLA metrics in business-friendly terms allowed stakeholders to self-serve status updates, reducing ad-hoc interruptions to the engineering team by an estimated **30%** per sprint.

***

# 🧠 Advanced Technical / Miscellaneous

## Q24. What is the difference between `repartition()` and `coalesce()` in PySpark?

Both **`repartition()`** and **`coalesce()`** in **PySpark** change the number of partitions in a **DataFrame**, but they behave very differently in terms of how data is redistributed and what the performance implications are.[^2][^1]

**`repartition(n)`** performs a **full shuffle** of data across the cluster to redistribute records into exactly `n` partitions as evenly as possible. Because it shuffles, it is an **expensive operation** — but it guarantees balanced partition sizes, which is critical before heavy operations like **joins** or **groupBy** on skewed data. You can also repartition by a column: `repartition(200, col("region"))` will ensure all records with the same region land in the same partition, optimizing co-located joins downstream.

**`coalesce(n)`** reduces the number of partitions **without a full shuffle** by merging existing partitions on the same worker node. It is much faster and cheaper than `repartition()` because data movement across the network is minimized. However, it can lead to **uneven partition sizes** since it only combines local partitions. `coalesce()` can only **decrease** the partition count, not increase it.

**When to use which:**

- Use **`repartition()`** before writes to **Parquet** on **S3 or ADLS Gen2** when you want evenly sized output files, or before skew-prone operations.
- Use **`coalesce()`** at the end of a pipeline to reduce output file count (avoiding the "small files problem") before writing to **Amazon Redshift** or **Azure Synapse** — it's faster and avoids unnecessary network shuffles.

The **small files problem** is a common issue when writing to **S3** or **ADLS Gen2** — too many small Parquet files degrade **Athena** and **Databricks** read performance. Using `coalesce(50)` before `.write.parquet()` is a standard optimization pattern in production **data lake** pipelines.

***

## Q25. Where do you see yourself in 3 years, and how does this role at TCS align with your career goals?

This question evaluates your **career clarity**, your **commitment to the role**, and whether your ambitions align with what TCS and the end client can offer. A strong answer demonstrates **self-awareness**, **technical ambition**, and **alignment with the role's growth trajectory**.[^3]

Over the next 3 years, my goal is to evolve from a strong individual contributor in **data pipeline engineering** into a **lead data engineer** or **data architecture** role — someone who shapes the technical direction of large-scale data platforms, mentors junior engineers, and drives platform-wide decisions around **cloud architecture**, **data governance**, and **pipeline scalability**.

This role at TCS aligns directly with that path. The JD's emphasis on **Apache Spark performance optimization**, **complex business-level PySpark transformations**, **scheduling and orchestration**, and **root-cause analysis** of pipeline failures maps exactly to the skills I have built at **JPMC**, **Accenture**, and **KPMG** — and the gaps I'm actively developing further. Working at a major end client through TCS gives me exposure to enterprise-scale challenges and cross-functional collaboration that accelerates that progression faster than most roles.

Specifically, I'm drawn to the challenge of designing **scalable data pipelines** that serve business-critical analytics. My experience reducing **production defects by 87.5%**, delivering **\$600K in annual labor savings** through **serverless automation**, and cutting implementation timelines by **3 months** gives me a strong foundation — and I want to build on that by tackling even more complex distributed systems challenges at scale.

In 3 years, I aim to be the go-to person on the team for **PySpark performance optimization**, **data quality architecture**, and **cloud-native pipeline design** — contributing not just to delivery but to the long-term engineering excellence of the platform.

***

> 💡 **Quick Prep Tips for Sandeep's Onsite:**
> - Brush up on **`MERGE` statements in Delta Lake** and **SCD Type 2** implementation in PySpark — highly likely to be asked
> - Be ready to **whiteboard a pipeline architecture** for an incremental load scenario
> - Prepare a strong **STAR story** around each key metric on the resume (87.5% defect reduction, \$600K savings, 3-week delivery acceleration)
> - Review **Spark UI metrics** — stages, tasks, shuffle read/write, spill — as scenario questions often probe debugging process

⁂

[^1]: https://www.linkedin.com/posts/savarbajiya_power-bi-activity-7328464404260253696-qr4b

[^2]: https://www.youtube.com/watch?v=A2QU5sw6O_M

[^3]: https://www.linkedin.com/posts/savarbajiya_tcs-data-analyst-interview-questions-what-activity-7339275980399697923-bfTH

[^4]: https://www.glassdoor.co.in/Interview/TCS-Data-Engineer-Interview-Questions-EI_IE3211746.0,3_KO4,17.htm

[^5]: https://www.datacamp.com/blog/pyspark-interview-questions

[^6]: https://srinimf.com/2024/01/25/10-python-pyspark-interview-questions-tcs-and-exl/

[^7]: https://www.coursera.org/in/articles/data-analyst-interview-questions-and-answers

[^8]: https://www.slideshare.net/slideshow/sandeep-resume-242624400/242624400

[^9]: https://k21academy.com/ai-ml/pyspark-interview-questions/

[^10]: https://www.glassdoor.co.in/Interview/Tata-Consultancy-Services-Data-Analyst-Interview-Questions-EI_IE13461.0,25_KO26,38.htm

[^11]: https://www.geeksforgeeks.org/data-analysis/data-analyst-interview-questions-and-answers/

[^12]: https://www.overleaf.com/articles/cv-of-sandeep-kumar/qmsgzkdmwdxd

[^13]: https://www.sprintzeal.com/blog/pyspark-interview-questions

[^14]: https://www.youtube.com/shorts/sqVRjgUZRhY

[^15]: https://www.youtube.com/watch?v=prPBBS6wbYA

