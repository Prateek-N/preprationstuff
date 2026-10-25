# -*- coding: utf-8 -*-
"""
Coding Questions for Priyanka Gantam
Role: Data Engineer at Walmart
Contains: 5 Production-Grade Data Engineering Coding Problems
Format:
- Problem Statement & Retail Context
- Algorithmic Thought Process & Trade-offs
- Commented Production Python / PySpark Implementation
- Complexity & Scalability Analysis
"""

CODING_PROBLEMS = [
    {
        "num": 1,
        "title": "Real-Time Event Deduplication & Watermarking in PySpark Structured Streaming",
        "category": "Streaming & Real-Time Processing",
        "problem_statement": """In Walmart's omnichannel retail ecosystem, thousands of physical store point-of-sale (POS) registers and e-commerce mobile applications emit millions of purchase events per minute into an Apache Kafka topic. Due to intermittent network disconnects, cellular handoffs, and edge retries, events frequently arrive out-of-order and with duplicated payloads.

Design an end-to-end PySpark Structured Streaming pipeline that:
1. Ingests raw JSON transaction events from a Kafka topic.
2. Implements event-time watermarking to tolerate up to 10 minutes of late-arriving data.
3. Performs stateful deduplication on a composite key (`transaction_id`, `store_id`) within the watermark window.
4. Computes rolling 5-minute sales volume and transaction count per store.
5. Writes the aggregated metrics into a Delta Lake table with checkpointing and exactly-once idempotency.""",
        "thought_process": """When designing high-throughput stateful streaming pipelines, managing state store memory while guaranteeing data accuracy is the central engineering challenge. Without watermarking, Spark Structured Streaming would maintain in-memory state for every unique transaction identifier indefinitely, eventually causing JVM heap exhaustion and out-of-memory executor crashes.

My thought process begins by defining the event-time watermark. A 10-minute watermark instructs Spark to track the maximum event time observed so far and discard any records arriving older than that threshold minus 10 minutes. This allows Spark's state store (backed by RocksDB or HDFS) to prune expired state keys safely.

Next, stateful deduplication is achieved via `dropDuplicatesWithinWatermark()`. Using a composite key (`transaction_id`, `store_id`) ensures that even if an edge device resends a batch of receipts, duplicates within the 10-minute horizon are filtered out before stateful window aggregations occur.

For aggregations, we apply tumbling or sliding windows using `window(col("event_timestamp"), "5 minutes")`. To write out to Delta Lake idempotently, we configure checkpointing on cloud storage (e.g., S3 or ADLS) and use Delta's native ACID log to ensure committed micro-batches are never re-applied during failure recoveries.""",
        "code": """from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, sum as _sum, count as _count
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# Initialize Spark Session configured for Delta Lake and Kafka
spark = SparkSession.builder \\
    .appName("Walmart_POS_Streaming_Deduplication") \\
    .config("spark.sql.streaming.stateStore.providerClass", 
            "org.apache.spark.sql.execution.streaming.state.RocksDBStateStoreProvider") \\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \\
    .getOrCreate()

# 1. Define explicit schema for incoming JSON payloads
pos_schema = StructType([
    StructField("transaction_id", StringType(), False),
    StructField("store_id", StringType(), False),
    StructField("customer_id", StringType(), True),
    StructField("product_id", StringType(), False),
    StructField("amount", DoubleType(), False),
    StructField("event_timestamp", TimestampType(), False)
])

# 2. Ingest raw streaming stream from Kafka broker
raw_kafka_df = spark.readStream \\
    .format("kafka") \\
    .option("kafka.bootstrap.servers", "kafka-broker:9092") \\
    .option("subscribe", "walmart.pos.transactions") \\
    .option("startingOffsets", "latest") \\
    .option("failOnDataLoss", "false") \\
    .load()

# 3. Parse JSON payload and project strongly typed columns
parsed_transactions = raw_kafka_df \\
    .select(from_json(col("value").cast("string"), pos_schema).alias("data")) \\
    .select("data.*")

# 4. Enforce Event-Time Watermarking and Stateful Deduplication
deduplicated_stream = parsed_transactions \\
    .withWatermark("event_timestamp", "10 minutes") \\
    .dropDuplicates(["transaction_id", "store_id", "event_timestamp"])

# 5. Compute rolling 5-minute sales aggregations per physical store
windowed_sales_summary = deduplicated_stream \\
    .groupBy(
        window(col("event_timestamp"), "5 minutes", "5 minutes"),
        col("store_id")
    ) \\
    .agg(
        _sum("amount").alias("total_sales_amount"),
        _count("transaction_id").alias("total_transactions")
    ) \\
    .select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("store_id"),
        col("total_sales_amount"),
        col("total_transactions")
    )

# 6. Stream sink to Delta Lake table with checkpointing for exactly-once guarantees
query = windowed_sales_summary.writeStream \\
    .format("delta") \\
    .outputMode("append") \\
    .option("checkpointLocation", "s3://walmart-lakehouse-checkpoints/pos_sales_metrics/") \\
    .option("path", "s3://walmart-lakehouse-gold/pos_sales_summary/") \\
    .trigger(processingTime="1 minute") \\
    .start()

query.awaitTermination()""",
        "complexity": """- **Time Complexity:** O(N) per micro-batch where N is the number of records. Window aggregation executes in linear time across partitions.
- **Space Complexity:** O(U) in the state store, where U is the number of distinct transactions observed within the active 10-minute watermark window. Utilizing RocksDB off-heap storage prevents JVM garbage collection pauses.
- **Fault Tolerance:** End-to-end exactly-once semantics achieved via Kafka committed offsets and Delta Lake atomic write-ahead logs."""
    },
    {
        "num": 2,
        "title": "Idempotent Slowly Changing Dimension (SCD Type 2) Upsert in PySpark & Delta Lake",
        "category": "Data Warehousing & Dimensional Modeling",
        "problem_statement": """Walmart's master product catalog contains over 100 million Stock Keeping Units (SKUs). Product pricing, department categorization, and promotional tags update frequently from multiple regional merchandising feeds.

Write an idempotent PySpark batch transformation that merges incoming product updates into a target Delta Lake dimension table (`dim_product`) using **SCD Type 2** logic:
1. If a product does not exist, insert it as a new active record (`is_current = True`, `end_date = NULL`).
2. If an existing product has changed attributes (e.g. price, department), expire the old record (`is_current = False`, `end_date = update_time`) and insert the new version with `is_current = True`.
3. If the incoming product attributes are identical to the active version, perform no operation (zero redundant writes).
4. Ensure the entire operation is idempotent and atomic.""",
        "thought_process": """SCD Type 2 tracking is the standard pattern for historical auditability in dimensional warehouses. In distributed systems, executing naive row-by-row updates is prohibitively expensive. We must leverage Delta Lake's native `MERGE INTO` API in PySpark to execute atomic, set-based upserts.

My thought process decomposes the problem into a two-pass staging strategy:
First, we compare incoming records against the active dimension records in `dim_product` (where `is_current = True`). We compute an MD5 hash of the tracked business attributes (e.g., `price`, `department`, `brand`). If the natural key matches and the hash has changed, the record represents an 'Update'. If the natural key does not exist, it represents an 'Insert'.

Second, for 'Update' records, we need to perform two distinct actions in the target table: expire the incumbent record and insert the new record. Because a standard SQL `MERGE` statement can only touch each target row once, we perform the classic 'Merge with Staging Union' pattern:
We union the incoming updates with a synthetic null key or use Delta Lake's conditional merge to:
1. Update existing matching active records by setting `is_current = False` and `end_date = current_timestamp`.
2. Insert all net-new records and newly expired counterparts as active rows.

This design guarantees that re-running the job for the same execution window yields the exact same state without creating duplicate active versions.""",
        "code": """from pyspark.sql import SparkSession
from pyspark.sql.functions import col, md5, concat_ws, current_timestamp, lit
from delta.tables import DeltaTable

spark = SparkSession.builder \\
    .appName("Walmart_Product_SCD2_Merge") \\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \\
    .getOrCreate()

# Path to the persistent Delta Lake dimension table
DIM_PRODUCT_PATH = "s3://walmart-lakehouse-gold/dimensions/dim_product/"

def run_scd2_merge(incoming_updates_df):
    target_table = DeltaTable.forPath(spark, DIM_PRODUCT_PATH)
    target_df = target_table.toDF()

    # 1. Compute attribute hash on incoming data for change detection
    incoming_staged = incoming_updates_df \\
        .withColumn("attr_hash", md5(concat_ws("||", col("price"), col("department"), col("brand"))))

    # 2. Isolate active records in target dimension
    active_target = target_df.filter(col("is_current") == True) \\
        .select(
            col("product_id").alias("t_product_id"),
            col("attr_hash").alias("t_attr_hash")
        )

    # 3. Join incoming with active target to classify actions
    joined_df = incoming_staged.join(
        active_target,
        incoming_staged.product_id == active_target.t_product_id,
        "left_outer"
    )

    # Identify records requiring expiration (natural key matches, hash differs)
    records_to_update = joined_df \\
        .filter((col("t_product_id").isNotNull()) & (col("attr_hash") != col("t_attr_hash"))) \\
        .select(incoming_staged["*"])

    # Identify brand new records (natural key does not exist)
    records_to_insert = joined_df \\
        .filter(col("t_product_id").isNull()) \\
        .select(incoming_staged["*"])

    # 4. Prepare Staged Merge Dataset
    # Records to update need two rows: one to expire the old record, one to insert the new record
    staged_updates_expire = records_to_update \\
        .withColumn("merge_key", col("product_id")) \\
        .withColumn("action", lit("EXPIRE"))

    staged_updates_insert = records_to_update \\
        .withColumn("merge_key", lit(None).cast("string")) \\
        .withColumn("action", lit("INSERT"))

    staged_new_inserts = records_to_insert \\
        .withColumn("merge_key", lit(None).cast("string")) \\
        .withColumn("action", lit("INSERT"))

    # Union all staged records together
    staged_merge_df = staged_updates_expire \\
        .unionByName(staged_updates_insert) \\
        .unionByName(staged_new_inserts)

    # 5. Execute Atomic Delta Lake Merge
    target_table.alias("target").merge(
        source=staged_merge_df.alias("source"),
        condition="target.product_id = source.merge_key AND target.is_current = True"
    ).whenMatchedUpdate(
        condition="source.action = 'EXPIRE'",
        set={
            "is_current": lit(False),
            "end_date": current_timestamp()
        }
    ).whenNotMatchedInsert(
        values={
            "product_id": "source.product_id",
            "price": "source.price",
            "department": "source.department",
            "brand": "source.brand",
            "attr_hash": "source.attr_hash",
            "start_date": current_timestamp(),
            "end_date": lit(None),
            "is_current": lit(True)
        }
    ).execute()

    print("SCD Type 2 atomic merge executed successfully.")""",
        "complexity": """- **Time Complexity:** O(M log N) where M is incoming updates and N is target table size. Delta Lake utilizes file pruning on `is_current` and data skipping via min/max statistics.
- **Space Complexity:** O(M) intermediate shuffle storage for staged candidate records.
- **Idempotency:** Re-executing with the same input produces zero redundant updates because identical attribute hashes are automatically filtered out."""
    },
    {
        "num": 3,
        "title": "Mitigating Severe Data Skew in PySpark via Two-Phase Key Salting",
        "category": "Distributed Computing & Performance Optimization",
        "problem_statement": """During peak retail periods like Black Friday, Walmart's store sales transaction table contains hundreds of millions of records. A tiny fraction of store locations (e.g., Flagship Supercenters in Bentonville, Dallas, or Orlando) generate 100x more transaction volume than smaller rural outlets.

When joining this massive fact table (`sales_transactions`) with the store dimensional table (`dim_store`) to compute regional revenue, standard Spark Sort-Merge joins fail due to executor out-of-memory errors on the hot store partitions.

Implement a production PySpark salting algorithm that:
1. Dynamically detects or isolates skewed join keys.
2. Applies a randomized salt factor to distribute hot partition records uniformly across executors.
3. Replicates the corresponding dimensional keys so that all join combinations match correctly.
4. Executes the distributed join without executor data spillage or out-of-memory crashes.""",
        "thought_process": """In distributed computing, data skew creates the dreaded 'straggler effect' where 99% of tasks finish in seconds, but task 199 stalls for 40 minutes processing 50 GB of data on a single executor. Broadcast joins cannot resolve this if the dimensional table is also large or if memory constraints prohibit broadcasting.

My thought process implements **Two-Phase Key Salting**:
1. Fact Table Salting: We take the skewed join key (`store_id`) and append a pseudo-random integer bounded between `0` and `SALT_FACTOR - 1` (e.g., 0 to 19 for a factor of 20). The resulting composite key (`store_id_salted`) disperses what was previously a single giant partition across 20 distinct worker partitions.
2. Dimension Table Expansion: For the join to succeed, the dimension table must contain matching keys for all 20 possible salt values. We use `explode(array([lit(0), lit(1), ..., lit(SALT_FACTOR - 1)]))` to replicate the dimensional records 20 times, each assigned one salt value.
3. Distributed Hash Join: We join on `fact.store_id_salted == dim.store_id_salted`. Spark now shuffles the records evenly across all executor slots.
4. Post-Join Projection: We drop the synthetic salt columns and proceed with downstream aggregations. Memory consumption remains flat, and executor utilization approaches 100% across all cluster nodes.""",
        "code": """from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws, floor, rand, array, lit, explode

spark = SparkSession.builder \\
    .appName("Walmart_Sales_Key_Salting_Join") \\
    .getOrCreate()

def salted_distributed_join(sales_df, dim_store_df, salt_factor=20):
    \"\"\"
    Performs a balanced distributed join between a heavily skewed sales table
    and a store dimension table using randomized key salting.
    
    :param sales_df: Large transactional DataFrame with severe key skew on 'store_id'
    :param dim_store_df: Store dimensional DataFrame
    :param salt_factor: Number of sub-partitions to distribute skewed keys across
    :return: Joined DataFrame free of executor memory bottlenecks
    \"\"\"
    
    # 1. Salt the primary fact table
    # Append random integer between 0 and (salt_factor - 1)
    salted_sales_df = sales_df \\
        .withColumn("salt_val", floor(rand() * salt_factor)) \\
        .withColumn("salted_store_id", concat_ws("_", col("store_id"), col("salt_val")))

    # 2. Replicate the dimension table to match all possible salt keys
    # Create an array of integers [0, 1, ..., salt_factor - 1]
    salt_array = array([lit(i) for i in range(salt_factor)])
    
    # Explode array so each store record is replicated 'salt_factor' times
    replicated_dim_df = dim_store_df \\
        .withColumn("salt_val", explode(salt_array)) \\
        .withColumn("salted_store_id", concat_ws("_", col("store_id"), col("salt_val")))

    # 3. Perform the distributed join on the salted composite key
    # Spark shuffles data uniformly across partitions, avoiding hot executors
    joined_df = salted_sales_df.join(
        replicated_dim_df,
        on="salted_store_id",
        how="inner"
    )

    # 4. Clean up synthetic columns and return clean schema
    final_df = joined_df \\
        .drop("salted_store_id") \\
        .drop(salted_sales_df["salt_val"]) \\
        .drop(replicated_dim_df["salt_val"])

    return final_df

# Demonstration execution
if __name__ == "__main__":
    # Mocking skewed sales data
    raw_sales = spark.createDataFrame([
        ("TX_STORE_101", 125.50, "2026-10-25"),
        ("TX_STORE_101", 45.00, "2026-10-25"),
        ("AR_STORE_001", 89.20, "2026-10-25")
    ], ["store_id", "sale_amount", "sale_date"])

    # Store dimension
    raw_dim = spark.createDataFrame([
        ("TX_STORE_101", "Dallas Supercenter", "Southwest"),
        ("AR_STORE_001", "Bentonville Flagship", "Midwest")
    ], ["store_id", "store_name", "region"])

    result = salted_distributed_join(raw_sales, raw_dim, salt_factor=10)
    result.show()""",
        "complexity": """- **Time Complexity:** O((N + S * M) log P) where N is fact rows, M is dimension rows, S is salt factor, and P is partition count. Eliminates single-thread long-tail bottlenecks.
- **Space Complexity:** Fact table size remains O(N) with 1 added column. Dimension table memory expands by factor S (O(S * M)), which is easily absorbed by distributed worker memory.
- **Operational Scalability:** Ideal for petabyte-scale joins where broadcast joins exceed executor RAM thresholds."""
    },
    {
        "num": 4,
        "title": "Automated Data Quality Contract Firewall using Python & Great Expectations",
        "category": "Data Governance & Quality Engineering",
        "problem_statement": """Walmart partners with over 100,000 third-party marketplace sellers and suppliers. Upstream suppliers submit daily Advance Shipping Notices (ASNs) via CSV and JSON files landing in S3 buckets. Suppliers frequently upload files with missing mandatory columns, invalid negative shipment quantities, corrupted date formats, and duplicate purchase orders.

Implement a modular, production-ready Python data quality firewall using **Great Expectations** and **Pydantic** concepts that:
1. Validates schema integrity, nullable constraints, and data ranges on landing files.
2. Checks cross-column consistency (e.g., `shipped_date <= expected_delivery_date`).
3. Quarantines defective records into an S3 dead-letter bucket while logging validation metrics.
4. Returns an executive pass/fail summary that blocks downstream Airflow DAG execution on critical failures.""",
        "thought_process": """Data contracts must be enforced before untrusted external feeds enter the core Lakehouse. If corrupt data lands in the Bronze or Silver tables, the blast radius expands exponentially, polluting ML feature stores and executive reports.

My thought process structures a four-tier validation firewall:
1. Ingestion Interceptor: As the file lands in the raw S3 bucket, a validation wrapper reads the file using Pandas or PySpark and binds it to a Great Expectations Data Context.
2. Expectation Suite Execution: We define a declarative validation suite enforcing:
   - File-level checks: Column existence and absence of unexpected schema additions.
   - Column-level checks: `purchase_order_id` is unique and non-null; `shipped_quantity` is strictly positive (> 0); `carrier_code` matches valid logistics providers.
   - Multi-column relational checks: `shipped_date` must precede or equal `estimated_arrival_date`.
3. Triage & Segregation: If the overall validation fails critical assertions, the file is moved to an S3 quarantine path (`s3://walmart-quarantine/vendor_asns/`), a structured JSON incident report is generated for supplier remediation, and the function returns an exit code of 1 to fail the orchestrating Airflow task immediately.
4. Clean Ingestion: If validation passes, records move to the Bronze ingestion lake.""",
        "code": """import os
import sys
import json
import pandas as pd
import great_expectations as gx
from datetime import datetime

class VendorASNQualityFirewall:
    def __init__(self, data_context_root="./gx"):
        \"\"\"Initialize Great Expectations ephemeral data context.\"\"\"
        self.context = gx.get_context(project_root_dir=data_context_root)
        self.suite_name = "vendor_asn_quality_contract"

    def create_or_get_suite(self):
        \"\"\"Define programmatic data contract assertions.\"\"\"
        try:
            suite = self.context.get_expectation_suite(self.suite_name)
        except Exception:
            suite = self.context.add_expectation_suite(self.suite_name)

        return suite

    def validate_and_quarantine(self, file_path: str, quarantine_dir: str) -> dict:
        \"\"\"
        Validates vendor ASN file against data contracts.
        Quarantines invalid files and returns detailed execution telemetry.
        \"\"\"
        df = pd.read_csv(file_path)
        validator = self.context.sources.pandas_default.read_dataframe(df)

        # 1. Structural Schema Contract
        validator.expect_table_columns_to_match_ordered_list([
            "po_number", "vendor_id", "sku_id", "quantity", "shipped_date", "estimated_delivery"
        ])

        # 2. Primary Key Completeness & Uniqueness
        validator.expect_column_values_to_not_be_null("po_number")
        validator.expect_column_values_to_be_unique("po_number")

        # 3. Numeric Business Rule Constraints
        validator.expect_column_values_to_be_between(
            column="quantity", min_value=1, max_value=50000
        )

        # 4. Temporal Format and Sequence Assertions
        validator.expect_column_values_to_match_regex(
            "shipped_date", r"^\\d{4}-\\d{2}-\\d{2}$"
        )
        validator.expect_column_pair_values_a_to_be_greater_than_b(
            column_A="estimated_delivery",
            column_B="shipped_date",
            or_equal=True
        )

        # Execute Validation
        validation_result = validator.validate()

        telemetry = {
            "file_name": os.path.basename(file_path),
            "timestamp": datetime.utcnow().isoformat(),
            "success": validation_result.success,
            "evaluated_expectations": len(validation_result.results),
            "successful_expectations": sum(1 for r in validation_result.results if r.success),
            "failed_details": [
                {
                    "expectation": r.expectation_config.expectation_type,
                    "kwargs": r.expectation_config.kwargs,
                    "observed": r.result.get("observed_value")
                }
                for r in validation_result.results if not r.success
            ]
        }

        # Handle Quarantine Routing
        if not validation_result.success:
            os.makedirs(quarantine_dir, exist_ok=True)
            quarantine_path = os.path.join(quarantine_dir, os.path.basename(file_path))
            os.rename(file_path, quarantine_path)
            telemetry["quarantine_path"] = quarantine_path
            print(f"[SECURITY ALERT] Contract breach! File quarantined to: {quarantine_path}")
        else:
            print(f"[SUCCESS] Contract verified! File approved for Bronze ingestion.")

        return telemetry

# Example demonstration
if __name__ == "__main__":
    # Mock invalid vendor file
    mock_data = {
        "po_number": ["PO_1001", "PO_1001", "PO_1003"],  # Duplicate PO
        "vendor_id": ["V_50", "V_50", "V_99"],
        "sku_id": ["SKU_A", "SKU_B", "SKU_C"],
        "quantity": [100, -5, 50],  # Negative quantity violation
        "shipped_date": ["2026-10-25", "2026-10-25", "2026-10-25"],
        "estimated_delivery": ["2026-10-28", "2026-10-20", "2026-10-29"]  # Reverse date order
    }
    sample_csv = "mock_vendor_asn.csv"
    pd.DataFrame(mock_data).to_csv(sample_csv, index=False)

    firewall = VendorASNQualityFirewall()
    summary = firewall.validate_and_quarantine(sample_csv, quarantine_dir="./quarantine")
    print(json.dumps(summary, indent=2))""",
        "complexity": """- **Time Complexity:** O(N * E) where N is row count and E is number of expectations evaluated. Vectorized Pandas evaluations run in sub-second time for files up to 500,000 rows.
- **Space Complexity:** O(N) memory allocation to evaluate the in-memory dataframe.
- **Enterprise Benefit:** Zero corrupted supplier rows reach the Lakehouse; downstream pipelines are protected against schema breaks."""
    },
    {
        "num": 5,
        "title": "Spark SQL / PySpark Window Functions for Sessionization & Fraud Detection",
        "category": "Advanced Analytics & Fraud Detection",
        "problem_statement": """Walmart's financial protection and loss prevention systems monitor omnichannel returns and refund requests in real time. Fraud syndicates exploit return policies by executing rapid bursts of refund requests across multiple accounts within tight time windows before store associate authorization limits trigger.

Given a distributed transactional returns dataset (`customer_id`, `store_id`, `return_amount`, `return_timestamp`), write an optimized PySpark pipeline that:
1. Identifies all instances where a customer initiates 3 or more refund transactions within any rolling 15-minute sliding window.
2. Calculates the cumulative refund sum within that rolling window.
3. Flags anomalous velocity bursts where total refunds exceed $500 in that window.
4. Assigns a persistent fraud risk score without performing expensive multi-pass self-joins.""",
        "thought_process": """Detecting event clustering within rolling time windows is a quintessential stream analytics problem. Naive solutions involve self-joining the table on `t1.customer_id == t2.customer_id AND t2.timestamp BETWEEN t1.timestamp AND t1.timestamp + 15 min`, which incurs an exponential O(N^2) complexity that melts cluster compute on billions of records.

My thought process uses **PySpark Window Functions with Unix Timestamp Range Frames**:
1. Epoch Conversion: We cast `return_timestamp` to integer seconds (`unix_timestamp`).
2. Range-Based Window Specification: We construct a window partitioned by `customer_id`, ordered by `unix_time`, with a frame defined as `rangeBetween(-900, 0)`. The value `-900` represents 900 seconds (15 minutes). This frame dynamically includes all transactions by that customer occurring in the preceding 15 minutes up to the current row.
3. Vectorized Window Aggregations: Within this single window specification, we compute:
   - `count(transaction_id)`: number of returns in the rolling 15 minutes.
   - `sum(return_amount)`: cumulative refund value in that same window.
   - `lag(return_timestamp, 2)`: checks the timestamp of the 2nd preceding return.
4. Conditional Fraud Flagging: A transaction is flagged as suspicious if `rolling_return_count >= 3` and `rolling_refund_sum >= 500.0`.
This executes in a single distributed shuffle stage, achieving linear O(N log N) runtime.""",
        "code": """from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, unix_timestamp, count, sum as _sum, when, lit
)
from pyspark.sql.window import Window

spark = SparkSession.builder \\
    .appName("Walmart_Fraud_Velocity_Detection") \\
    .getOrCreate()

def detect_refund_fraud_velocity(returns_df):
    \"\"\"
    Detects high-frequency, high-value refund bursts using single-pass
    range-based temporal window functions in PySpark.
    
    :param returns_df: DataFrame with ['return_id', 'customer_id', 'store_id', 'return_amount', 'return_timestamp']
    :return: Annotated DataFrame with fraud flags and rolling velocity metrics
    \"\"\"

    # 1. Convert timestamp to epoch seconds for rangeBetween evaluation
    staged_df = returns_df.withColumn(
        "epoch_seconds", unix_timestamp(col("return_timestamp"))
    )

    # 2. Define 15-minute (900 seconds) rolling historical window per customer
    # rangeBetween(-900, 0) evaluates all records from (current_time - 15 mins) to current_time
    rolling_15min_window = Window \\
        .partitionBy("customer_id") \\
        .orderBy("epoch_seconds") \\
        .rangeBetween(-900, 0)

    # 3. Compute window metrics in a single distributed pass
    velocity_metrics_df = staged_df \\
        .withColumn("rolling_return_count", count("return_id").over(rolling_15min_window)) \\
        .withColumn("rolling_refund_total", _sum("return_amount").over(rolling_15min_window))

    # 4. Evaluate fraud detection heuristics
    flagged_df = velocity_metrics_df.withColumn(
        "is_fraud_burst",
        when(
            (col("rolling_return_count") >= 3) & (col("rolling_refund_total") >= 500.0),
            lit(True)
        ).otherwise(lit(False))
    ).withColumn(
        "fraud_risk_level",
        when(col("rolling_refund_total") >= 1500.0, lit("CRITICAL"))
        .when((col("rolling_return_count") >= 3) & (col("rolling_refund_total") >= 500.0), lit("HIGH"))
        .otherwise(lit("LOW"))
    )

    # Clean up intermediate epoch column
    return flagged_df.drop("epoch_seconds")

# Demonstration
if __name__ == "__main__":
    sample_returns = spark.createDataFrame([
        ("RET_1", "CUST_999", "STORE_10", 250.00, "2026-10-25 14:00:00"),
        ("RET_2", "CUST_999", "STORE_10", 180.00, "2026-10-25 14:06:00"),
        ("RET_3", "CUST_999", "STORE_10", 220.00, "2026-10-25 14:11:00"), # 3rd in 11 mins, sum=$650 -> HIGH FRAUD
        ("RET_4", "CUST_111", "STORE_20", 35.00,  "2026-10-25 14:02:00"),
        ("RET_5", "CUST_111", "STORE_20", 40.00,  "2026-10-25 15:30:00")  # >1 hour gap -> LOW
    ], ["return_id", "customer_id", "store_id", "return_amount", "return_timestamp"])

    flagged_output = detect_refund_fraud_velocity(sample_returns)
    flagged_output.select(
        "return_id", "customer_id", "return_amount", "rolling_return_count", 
        "rolling_refund_total", "fraud_risk_level"
    ).show()""",
        "complexity": """- **Time Complexity:** O(N log N) dominated by the initial partition-level sorting along customer_id and timestamp. Range calculations execute in linear time per partition without cartesian product joins.
- **Space Complexity:** O(N) memory overhead for window buffers.
- **Scalability:** Partitions horizontally across Spark cluster executors; effortlessly scales to tens of millions of retail return records daily."""
    }
]
