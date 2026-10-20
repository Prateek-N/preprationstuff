# -*- coding: utf-8 -*-
"""
Module 1: Questions 1 to 15 for Teja Talluri's Walmart Senior Data Analyst (Transportation - Inbound Planning and Optimization) Interview.
Each answer is at least 300 words, highly technical, grounded in Teja's resume (Uber, Dish Network, Cipla, BBA in Supply Chain, MS in Business Analytics),
and mapped directly to Walmart Inbound Transportation and Supply Chain.
Important words and tech stacks are in BOLD.
"""

QUESTIONS_PART1 = """
## Part 1: Technical Questions & Comprehensive Answers (Q1 to Q15)

---

### Question 1: How would you approach analyzing inbound shipment patterns and carrier performance across Walmart's regional distribution centers (DCs) to identify chronic delivery bottlenecks and reduce demurrage costs?

#### Answer:
To analyze inbound shipment patterns and carrier performance across **Walmart's** massive network of Regional Distribution Centers (**RDCs**) and Consolidation Centers (**CCs**), I apply a structured, multi-dimensional analytical framework built upon my experience leading operations and capacity planning at **Uber** and optimizing high-volume telecom data workflows at **Dish Network**. With my academic foundation in **Supply Chain Management** (BBA) and **Business Analytics** (MS), I approach this not merely as descriptive reporting, but as end-to-end variance decomposition and predictive bottleneck mitigation.

First, I establish an automated data pipeline using **GCP BigQuery**, ingesting event streams from Walmart's **Transportation Management System (TMS)**, **Warehouse Management System (WMS)**, and Electronic Data Interchange (**EDI 214** carrier status messages, **EDI 210** freight invoices, and **EDI 856** Advance Ship Notices). Inbound bottlenecks generally manifest at three distinct operational handoffs: linehaul transit delays, yard gate queues, and dock door unloading dwell. I model these timestamps using **SQL window functions** to isolate granular stage durations: Linehaul Transit Time, Gate-to-Yard Dwell, Yard-to-Dock Staging, and Dock Unload Duration. At **Uber**, where I analyzed ride-allocation bottlenecks across millions of trips, I found that aggregate averages hide operational reality; therefore, I evaluate the **90th and 99th percentiles (P90/P99)** rather than simple averages to capture the long-tail friction that triggers detention and demurrage penalties.

Second, I engineer a standardized **Carrier Scorecard** in **Tableau** and **Streamlit** tracking primary logistics KPIs: **On-Time In-Full (OTIF)** compliance, **Appointment Window Adherence** (within a ±30 minute tolerance), **Tender Acceptance Rate**, and **Trailer Detention Hours**. To isolate chronic bottlenecks from transient external shocks (such as severe weather or interstate highway closures), I apply a **Difference-in-Differences (DiD)** and **Causal Inference** methodology, similar to the causal experimentation framework I built at **Uber** that attributed **$8.7M in quarterly revenue impact**. By benchmarking carrier performance on specific lanes against peer carriers operating on identical origin-destination (**OD**) pairs during the same shift, I eliminate macro-environmental noise and isolate true carrier-controllable inefficiencies.

Third, to directly curtail **demurrage and detention costs**, I develop an automated anomaly detection system deployed via **Apache Airflow**. When a carrier trailer’s yard dwell approaches 75% of the contractual free-time threshold (typically 2 hours for live unloads or 24 hours for drop-and-hook trailers), an automated alert is routed to yard operations via webhooks. At **Uber**, my **SQL-based anomaly detection platform** flagged fraudulent patterns across 6 markets and prevented **$2.1M in losses per quarter**; applying this same operational rigor to Walmart's inbound yard management prevents detention penalties before they materialize, optimizes hostler/spotter truck movements, and ensures high-priority seasonal inventory flows seamlessly from dock to stock.

---

### Question 2: Inbound transportation relies heavily on On-Time In-Full (OTIF) compliance. How do you define, calculate, and diagnose OTIF failures across suppliers and carriers using SQL and Python?

#### Answer:
**On-Time In-Full (OTIF)** is the foundational supply chain health metric governing **Walmart's** retail availability and omnichannel fulfillment. Having managed inventory capacity for 300+ pharmaceutical SKUs at **Cipla** and high-scale operational metrics at **Uber**, I understand that OTIF failures directly degrade distribution center throughput, create safety stock bloating, and result in retail out-of-stocks.

Mathematically, **OTIF** is defined as the intersection of two distinct operational SLAs:
1. **On-Time (OT)**: The shipment arrives at the designated Walmart facility within the approved Scheduled Delivery Appointment window (typically between appointment time $-30$ minutes and $+0$ minutes for appointment adherence, or within the designated MABD—Must Arrive By Date).
2. **In-Full (IF)**: The quantity of units or cases received and scanned at the receiving dock matches 100% of the Purchase Order (**PO**) ordered quantity (or falls within a tight contractual tolerance, such as 98.0% to 100.0%).
$$\\text{OTIF Compliant} = 1 \\iff (\\text{Arrival Timestamp} \\in [\\text{MABD Start}, \\text{MABD End}]) \\land (\\text{Received Qty} \\ge \\text{Ordered Qty})$$

In **GCP BigQuery** and **Snowflake**, I construct an enterprise-grade query that joins `purchase_orders`, `asn_line_items` (EDI 856), `carrier_shipments` (EDI 214), and `wms_receiving_receipts`. The SQL implementation utilizes **CTEs** and **window functions** to handle multiple partial deliveries per PO:
```sql
WITH PO_Summary AS (
    SELECT 
        po.po_number,
        po.supplier_id,
        po.destination_dc_id,
        po.mabd_start_date,
        po.mabd_end_date,
        SUM(po.ordered_cases) AS total_ordered_cases
    FROM `walmart_supply_chain.purchase_orders` po
    GROUP BY 1, 2, 3, 4, 5
),
Receipt_Summary AS (
    SELECT 
        rec.po_number,
        rec.carrier_id,
        MIN(rec.dock_arrival_timestamp) AS first_arrival_ts,
        MAX(rec.dock_arrival_timestamp) AS last_arrival_ts,
        SUM(rec.received_cases) AS total_received_cases
    FROM `walmart_supply_chain.wms_receiving` rec
    GROUP BY 1, 2
)
SELECT 
    p.supplier_id,
    r.carrier_id,
    COUNT(p.po_number) AS total_pos,
    -- On-Time Metric: Arrival within MABD window
    ROUND(COUNTIF(DATE(r.first_arrival_ts) BETWEEN p.mabd_start_date AND p.mabd_end_date) * 100.0 / COUNT(p.po_number), 2) AS on_time_pct,
    -- In-Full Metric: Received >= Ordered
    ROUND(COUNTIF(r.total_received_cases >= p.total_ordered_cases) * 100.0 / COUNT(p.po_number), 2) AS in_full_pct,
    -- Combined OTIF Metric
    ROUND(COUNTIF(
        DATE(r.first_arrival_ts) BETWEEN p.mabd_start_date AND p.mabd_end_date 
        AND r.total_received_cases >= p.total_ordered_cases
    ) * 100.0 / COUNT(p.po_number), 2) AS otif_compliance_pct
FROM PO_Summary p
LEFT JOIN Receipt_Summary r ON p.po_number = r.po_number
GROUP BY 1, 2;
```

To diagnose the root cause of failures, I ingest this processed dataset into **Python (Pandas / Statsmodels)**. I perform **Variance Decomposition** and a **Decision Tree Classifier (Scikit-Learn)** to categorize failures into three actionable buckets:
- **Supplier-Driven Failures**: Order fill-rate shortages, delayed tender creation, or late origin release.
- **Carrier-Driven Failures**: In-transit breakdowns, missed appointment slots, driver hours-of-service (HOS) violations, or transit lane congestion.
- **Facility-Driven Failures**: Yard congestion, gate check-in delays, or dock labor shortages forcing carrier appointment push-backs.
At **Dish Network**, where I automated data pipelines across **180M+ daily subscriber records**, optimizing queries and delivering root-cause visibility slashed compute costs by **$420K**. In Walmart's inbound operations, this diagnostic engine directly informs automated supplier chargebacks and carrier procurement negotiations.

---

### Question 3: How would you design a scalable data quality and data observability framework for streaming inbound logistics data using dbt, Great Expectations, and Apache Airflow?

#### Answer:
In a retail supply chain of **Walmart's** scale, inbound planning decisions—such as dynamic cross-dock allocation, automated dock scheduling, and labor planning—depend entirely on the integrity, timeliness, and consistency of high-velocity streaming data. If an Advance Ship Notice (**EDI 856**) arrives with corrupted pallet counts or missing SKU identifiers, warehouse sorters jam, trailers sit idle, and downstream inventory replenishment is compromised. Drawing from my work at **Dish Network**, where I led the migration of 14 legacy ETL workflows to modern **dbt** and **Fivetran** pipelines on a structured **Medallion Architecture**, I design a comprehensive data observability framework across three layers: Ingestion Contracts, Transformational Quality Tests, and Automated Anomaly Observability.

```mermaid
flowchart LR
    A[Kafka / Streaming IoT & EDI] --> B[Bronze Lake: Raw JSON / Parquet]
    B --> C{Data Contract Validation}
    C -->|Pass| D[Silver: Cleaned & Conformed dbt Models]
    C -->|Fail| E[Dead-Letter Queue & Slack Alert]
    D --> F[Great Expectations: Statistical Testing]
    F --> G[Gold: Semantic Aggregates / BigQuery]
    G --> H[Airflow DQ Monitor & Lineage Tracking]
```

At the **Bronze Layer** (raw landing in **GCP Cloud Storage** / BigQuery), I enforce **Data Contracts** using **Protocol Buffers** or strict **JSON Schemas**. Inbound logistics event streams (trailer GPS pings, RFID gate scans, and barcode receipts) must conform to contract specifications: non-null mandatory keys (`shipment_id`, `carrier_id`, `destination_dc_id`), monotonic timestamp progression (`gate_in_ts <= dock_door_assigned_ts <= unload_start_ts <= unload_complete_ts`), and validated coordinate geofences. Payloads violating schema contracts are immediately isolated to a **Dead-Letter Queue (DLQ)** in BigQuery for inspection, preventing pipeline crashes.

At the **Silver Layer** (cleansed, conformed transactional tables), I orchestrate **dbt (data build tool)** test suites. I implement both generic tests (`unique`, `not_null`, `relationships` referencing master vendor/carrier dimension tables) and custom domain-specific singular tests:
- **Volumetric Plausibility**: Verifying that total reported pallet cube does not exceed standard 53-foot dry van trailer capacity ($3,800$ to $4,000$ cubic feet) or maximum legal gross vehicle weight ($80,000$ lbs).
- **Temporal Consistency**: Ensuring shipment transit lead time is positive and within physically feasible transit bounds (e.g., verifying a linehaul from Chicago to Atlanta is physically greater than 10 hours).

At the **Gold Layer** (reporting models, carrier scorecards, and capacity forecast features), I integrate **Great Expectations** into **Apache Airflow** DAGs as automated quality gates. I implement distribution checks tracking feature drift:
- Null percentage thresholding ($<0.01\%$).
- Volume anomaly detection using historical rolling medians (alerting if daily received PO volume drops by $>25\%$, indicating upstream EDI ingestion outages).
- Category set validation (ensuring carrier codes match registered SCAC codes).

At **Uber**, where I implemented an Airflow-driven **SQL anomaly detection system** standardizing data across 6 markets and preventing **$2.1M in quarterly losses**, automated observability was the key differentiator between proactive operational resolution and reactive fire-fighting. By integrating **Monte Carlo** or open-source data observability tools, Walmart engineers receive instant PagerDuty alerts with root-cause lineage before corrupted shipment records reach executive Tableau dashboards or automated dock scheduling systems.

---

### Question 4: How would you leverage Agentic AI and Large Language Models (LLMs) to streamline inbound exception management, carrier contract compliance, and automated communication?

#### Answer:
In traditional logistics environments, inbound exception management—such as handling damaged freight, resolving detention fee disputes, re-routing trailers during weather disruptions, or parsing non-standard carrier bills of lading (**BOL**)—involves hours of manual analyst intervention. Operations teams spend their shifts reading disparate emails, cross-referencing contractual tariff tables, and manually writing status updates. At **Uber**, I spearheaded the AI integration of support workflows utilizing **Google Gemini** and **OpenAI GPT-4o**, automating the resolution of **2.3M weekly manual support interactions** and delivering **$1.6M in quarterly operational savings**. Applying **Agentic AI** to **Walmart's Inbound Transportation** represents a transformative productivity leap.

I architect an **Agentic Inbound Operations Assistant** utilizing **LangChain / LangGraph**, **Google Gemini API / Vertex AI**, and the **Model Context Protocol (MCP)**, connecting four specialized autonomous sub-agents:

```mermaid
flowchart TD
    A[Incoming Carrier Exception: Email / PDF BOL / EDI 214 Delay] --> B[Orchestrator Agent: Gemini 1.5 Pro]
    B --> C[Document Parser Agent: OCR + Schema Extraction]
    B --> D[Contract Compliance Agent: RAG over Carrier SLAs]
    B --> E[WMS/TMS Execution Agent: BigQuery Tool Call]
    C --> F[Structured JSON Payload]
    D --> G[Liability & Penalty Determination]
    E --> H[Dynamic Dock Reschedule in TMS]
    B --> I[Automated Response & Audit Trail Log]
```

1. **Document Ingestion & Extraction Agent**: Ingests unstructured documents (scanned PDF Bills of Lading, driver inspection reports, and lumper fee receipts). Utilizing **Gemini 1.5 Pro's** multimodal vision capabilities and few-shot prompt engineering, it extracts structured JSON entities: `PO_Number`, `Carrier_SCAC`, `Reported_Damage_Units`, `National_Motor_Freight_Classification_Code (NMFC)`, and `Detention_Start_Timestamp`.
2. **Contract Compliance & RAG Agent**: When a carrier submits a detention surcharge invoice, the agent performs **Retrieval-Augmented Generation (RAG)** over indexed carrier master service agreements (**MSAs**) stored in a vector database (**ChromaDB / Pinecone**). It queries the specific free-time clauses (e.g., *"Carrier XYZ is entitled to $75/hour detention only after 2 hours of verified live-unload dock staging, provided the driver arrived within the appointment window"*).
3. **TMS/WMS Integration Agent (Tool Calling)**: The agent issues structured API/SQL calls to **GCP BigQuery** and Walmart's TMS to cross-reference ground-truth telemetry: Did the trailer’s GPS geofence timestamp confirm arrival on time? Did the driver check in at the guard shack prior to the scheduled slot?
4. **Action & Resolution Agent**: If the audit validates that the delay was Walmart facility-driven (e.g., unloader shortage), the agent auto-approves the invoice up to a pre-authorized limit ($500) and writes the approval record to SAP. If the delay was carrier-driven (driver arrived 90 minutes late, forfeiting free-time protections), the agent autonomously drafts a polite, legally substantiated rejection email citing the specific contract clause, GPS entry timestamp, and appointment log.

To guarantee zero hallucination in financial auditing, I incorporate **NeMo Guardrails** and deterministic programmatic validators. By automating tier-1 carrier communication and invoice audits, Walmart eliminates hundreds of manual analyst hours weekly, compresses dispute resolution cycles from weeks to minutes, and enforces 100% contract compliance across thousands of freight carriers.

---

### Question 5: How do you perform root-cause analysis when inbound freight costs surge on specific lanes, and how would you separate base rate increases from operational inefficiencies?

#### Answer:
A sudden surge in inbound freight expenditure is rarely driven by a single macroeconomic factor; it is typically an intricate combination of contractual rate escalations, operational inefficiencies, suboptimal routing, and accessorial penalty creep. To perform a rigorous root-cause analysis for **Walmart Inbound Transportation**, I apply a mathematical **Variance Decomposition Model** (similar to Price-Volume-Mix analysis in financial analytics) implemented in **Python** and **GCP BigQuery**, separating controllable operational failures from uncontrollable contract or market shifts.

I decompose total freight expenditure variance into five orthogonal components:
$$\\Delta \\text{Total Freight Cost} = \\Delta \\text{Rate Effect} + \\Delta \\text{Volume Effect} + \\Delta \\text{Mode Mix Effect} + \\Delta \\text{Carrier Compliance Effect} + \\Delta \\text{Accessorial Surcharge Effect}$$

1. **Rate Effect (Market & Contractual Shift)**: Isolates changes in the baseline linehaul rate per mile ($/mile) negotiated in the annual Request for Proposal (**RFP**) or indexed against diesel fuel surcharges (**DOE Fuel Index**). If contractual linehaul rates increase from $2.10 to $2.35 per mile due to contractual fuel indexation, this is quantified as an external market cost.
2. **Volume Effect (Demand Surge)**: Measures cost increases resulting purely from shipping higher inventory units or tonnage into the DC due to seasonal inventory build-ups (e.g., Back-to-School or Q4 Holiday Peak).
3. **Mode Mix Effect (FTL vs. LTL vs. Intermodal)**: Evaluates whether shipments that should have moved via economical Full Truckload (**FTL**) or Intermodal rail were fragmented into expensive Less-Than-Truckload (**LTL**) or expedited spot freight due to poor supplier consolidation or emergency store replenishment.
4. **Carrier Routing Guide Compliance Effect (Routing Leakage)**: Primary carrier compliance is critical. If primary contracted carriers (who offer low committed rates) reject tenders, shipments roll to secondary or tertiary carriers, or onto the open **spot market** at a 25% to 50% premium. I calculate **Routing Guide Leakage Cost**:
   $$\\text{Leakage Cost} = \\sum_{i} (\\text{Actual Paid Spot Rate}_i - \\text{Primary Contracted Rate}_i) \\times \\text{Miles}_i$$
5. **Accessorial Surcharge Creep**: Measures the inflation of non-linehaul penalties: Trailer Detention, Driver Demurrage, Lumper Unloading Fees, Redelivery Fees, and Layover charges.

At **Uber**, where I analyzed mobility records and identified operational bottlenecks that reduced MAPE by **4.2%** and saved **$4.2M**, I applied this exact analytical rigor to identify why specific regional markets were hemorrhaging dispatch incentives. Translating this to Walmart, I construct an executive **Waterfall Chart** in **Tableau** that visually explains to supply chain VPs exactly why a lane surged: e.g., *"Lane Atlanta DC to Dallas DC surged $480K this quarter: +$120K was macro fuel inflation (Rate Effect), +$210K was supplier tender rejection forcing spot market booking (Carrier Compliance), and +$150K was trailer detention caused by dock door congestion (Operational Accessorial)"*. This provides engineering and procurement leaders with the exact levers required to fix the operational bottleneck rather than blaming general market inflation.

---

### Question 6: Describe how you would formulate and execute a capacity planning and demand forecasting model for inbound trailer volume during Walmart's Q4 peak holiday season.

#### Answer:
Inbound capacity planning for **Walmart's Q4 holiday peak** is a high-stakes operational mandate. Underestimating inbound trailer volume leads to catastrophic yard gridlock, gate turnaways, missed dock appointments, and empty retail shelves. Overestimating capacity results in millions wasted on idle contracted carrier retainers, empty overflow yard leases, and overstaffed third-party lumper labor. Drawing from my experience at **Uber**, where I led demand forecasting and capacity planning across 8 metro markets using **Python** and **Azure Databricks** to deliver **$4.2M in annualized operational savings**, and at **Cipla**, where I forecasted demand for 300+ SKUs cutting **$900K in inventory overstock**, I design a hierarchical, multi-horizon forecasting architecture.

```mermaid
flowchart TD
    A[Upstream Data: Merchant POs, Promotional Calendars, Supplier EDI 856] --> B[Data Prep & Feature Store: GCP BigQuery]
    B --> C[Feature Engineering: Lead Times, SKU Velocity, Seasonality]
    C --> D[Baseline: SARIMAX & Prophet Decomposition]
    C --> E[Advanced ML: LightGBM / XGBoost Regressor]
    D & E --> F[Ensemble Evaluation & Spatial Hierarchical Reconciliation]
    F --> G[Trailer Forecast by DC / Day: P10, P50, P90]
    G --> H[Operational Capacity Allocation: Dock Labor & Yard Slots]
```

First, I establish the data ingestion and feature engineering pipeline in **GCP BigQuery** and **Databricks**. Inbound volume is not a simple autoregressive time series of historical gate arrivals; it is a downstream function of upstream merchant purchasing decisions. Key features include:
- **Active Purchase Order Pipeline**: Open PO line items, confirmed supplier ship dates, and contractual supplier lead times.
- **Promotional & Event Calendars**: Black Friday, Cyber Week, Rollbacks, and holiday seasonal promotional schedules.
- **Historical Seasonality**: Day-of-week, week-of-year, and holiday lag indicators.
- **Supplier Volumetric Profile**: Historic ratio of pallet cube to weight per supplier category (e.g., Electronics high weight/compact vs. Toys high volume/lightweight).
- **Macro Logistics Covariates**: Port container clearance dwell times, rail intermodal ramp congestion, and weather forecast indices.

Second, I deploy a two-tiered modeling methodology:
1. **Macro Strategic Model (12-Week Horizon)**: Utilizes **SARIMAX** and **Hierarchical Time Series (HTS)** reconciliation (using the `scikit-hts` package). This forecasts aggregate weekly trailer volumes at the National and Regional DC network level, ensuring that regional sub-forecasts sum coherently to the enterprise forecast. This informs long-term carrier volume commitments and auxiliary yard leasing.
2. **Micro Operational Model (1 to 14-Day Horizon)**: Deploys a **LightGBM / XGBoost Regressor** trained on daily sliding windows, forecasting trailer arrivals per specific DC by equipment type (53' Dry Van, Refrigerated Reefer, Flatbed, Intermodal Box).

Third, I emphasize **Probabilistic Forecasting** rather than single-point estimates. Supply chain operations cannot plan solely on the median ($P_{50}$). I generate quantile loss predictions ($P_{10}$, $P_{50}$, $P_{90}$). The **$P_{90}$ forecast** represents the high-volume stress scenario: if the $P_{90}$ inbound trailer count exceeds a DC's physical dock door throughput capacity, the planning engine automatically flags the bottleneck 7 days in advance. This allows the inbound optimization team to dynamically divert inbound POs to adjacent under-utilized facilities or schedule secondary weekend unloading shifts, guaranteeing 100% network flow continuity throughout the holiday surge.

---

### Question 7: How do you design and implement a dynamic trailer routing and dock door assignment optimization model to maximize DC throughput and minimize yard congestion?

#### Answer:
Efficient inbound transportation does not terminate when a trailer arrives at the facility perimeter; the transition from facility gate check-in to yard staging, dock door spotting, and unloading represents a critical operational frontier. In a high-velocity **Walmart Distribution Center** receiving 300+ trailers daily, assigning trailers to random dock doors creates internal congestion, long forklift travel distances, and severe cross-dock transfer delays. To solve this, I formulate the problem as an operational optimization model using **Mixed-Integer Linear Programming (MILP)** implemented in **Python** with libraries such as **PuLP** or **Google OR-Tools**.

The mathematical formulation optimizes trailer-to-door assignments to minimize total operational handling cost, subject to physical constraints:

**Objective Function**:
$$\\min \\sum_{i \\in \\text{Trailers}} \\sum_{j \\in \\text{Dock Doors}} \\left( C_{ij}^{\\text{Travel}} \\cdot X_{ij} + C_i^{\\text{Dwell}} \\cdot (T_i^{\\text{Unload}} - T_i^{\\text{Arrival}}) + P_i^{\\text{Demurrage}} \\right)$$
Where:
- $X_{ij} \\in \\{0, 1\\}$ is a binary decision variable indicating whether trailer $i$ is assigned to dock door $j$.
- $C_{ij}^{\\text{Travel}}$ represents the internal forklift transit distance/time between dock door $j$ and the staging/stowage bays required for the specific SKU mix inside trailer $i$. For cross-dock trailers, this represents the direct distance to the outbound shipping doors.
- $C_i^{\\text{Dwell}}$ is the cost penalty associated with trailer waiting time.
- $P_i^{\\text{Demurrage}}$ is the non-linear penalty applied if the trailer exceeds free-time detention limits.

**Operational Constraints**:
1. **Single Door Assignment**: Each trailer is assigned to at most one dock door during any given time slot:
   $$\\sum_{j} X_{ij} = 1, \\quad \\forall i$$
2. **Door Capacity & Compatibility**: A door cannot host multiple trailers simultaneously, and refrigerated reefers can only dock at doors equipped with cold-chain seals and temperature-controlled pre-coolers.
3. **Priority & SLA Constraints**: Trailers containing high-velocity cross-dock inventory or critical promotional stock are assigned higher priority weights, guaranteeing they are spotted and unloaded before general non-perishable freight.

In production, I wrap this optimization engine inside an asynchronous microservice using **FastAPI** containerized with **Docker** on **GCP Cloud Run**. The model executes dynamically every 15 minutes, ingesting live yard state from the **WMS** via **Kafka** streams. At **Uber**, where I designed algorithms that resolved **12 ride-allocation bottlenecks** and compressed operational reporting cycles from **12 hours to 2 hours**, I proved that mathematical optimization combined with low-latency execution yields massive efficiency gains. In Walmart’s inbound operations, this system minimizes yard hostler moves by 25%, slashes forklift transit travel by up to 30%, and accelerates trailer turn times, directly boosting overall DC throughput.

---

### Question 8: How do you identify, measure, and optimize Less-Than-Truckload (LTL) to Full-Truckload (FTL) consolidation opportunities across inbound vendor shipments?

#### Answer:
Shipping freight via **Less-Than-Truckload (LTL)** is inherently expensive, inefficient, and prone to transit damage compared to **Full Truckload (FTL)**. In LTL shipping, carriers transport freight through complex hub-and-spoke breakbulk terminals, resulting in higher linehaul rates per hundredweight ($/cwt), extended transit lead times, and multiple touchpoints that increase damage risk. For **Walmart**, consolidating disparate vendor shipments into scheduled, high-density FTL movements—either directly to Regional DCs or through Inbound Consolidation Centers (**CCs**)—represents one of the single largest transportation cost-reduction opportunities.

To identify and quantify these consolidation opportunities, I develop an end-to-end analytical pipeline using **SQL (BigQuery)** and **Python**:

```mermaid
flowchart LR
    A[Historical Inbound LTL POs: Origin, Destination, Weight, Cube, Ready Date] --> B[Spatial-Temporal Clustering: DBSCAN / H3 Geospatial]
    B --> C[Bin Packing Algorithm: 53ft Trailer Weight & Cube Constraints]
    C --> D[Cost-Benefit Arbitrage Engine: LTL Tariff vs FTL Contract Rate]
    D --> E[Consolidation Recommendations to Merchant & TMS Planners]
```

1. **Spatial-Temporal Clustering**: Disparate supplier purchase orders cannot be consolidated unless they share temporal compatibility and geographical proximity. In Python, I execute spatial-temporal clustering using **DBSCAN** or **Uber H3 hexagonal indexing** (which I used extensively at **Uber** to optimize spatial mobility clusters). I cluster shipments where:
   - Origin shipping facilities lie within a 50-mile radius (enabling multi-stop milk runs).
   - Destination is the same Walmart Regional DC or Consolidation Hub.
   - Supplier Ship-Ready Dates fall within a 48-hour consolidation window.
2. **3D Bin Packing Optimization (Heuristic Knapsack)**: Once clusters are formed, I pass the shipments into a **3D Bin Packing Algorithm** implemented in Python. The algorithm validates both weight constraints (maximum legal payload of $44,000$ lbs for a standard tandem-axle trailer) and volumetric cube constraints ($3,800$ cubic feet), while respecting stacking rules (e.g., non-stackable pallets or hazmat segregation).
3. **Cost-Benefit Financial Arbitrage**: For every viable consolidated pool, I compute the net financial savings:
   $$\\text{Net Savings} = \\sum_{k \\in \\text{Pool}} \\text{LTL Baseline Cost}_k - \\left( \\text{FTL Linehaul Rate} + \\text{Multi-Stop Pickup Surcharges} + \\text{Consolidation Handling Fee} \\right)$$
4. **Execution & Process Improvement**: At **Dish Network**, where I standardized data transformation pipelines processing **180M+ daily records** and slashed execution time from **6 hours to 47 minutes**, I learned that analytics must seamlessly bridge into daily operations. I automate the delivery of weekly consolidation opportunities directly into the **TMS routing guide**, allowing logistics planners to convert recurring LTL pools into scheduled multi-stop FTL contracts. This reduces linehaul freight spend by 18% to 28% across consolidated lanes, cuts carbon emissions, and streamlines dock receiving throughput.

---

### Question 9: Explain how you would conduct an A/B test or quasi-experiment to evaluate a new inbound appointment scheduling algorithm without disrupting live distribution center operations.

#### Answer:
Evaluating algorithmic innovations in physical logistics environments—such as a new dynamic appointment scheduling algorithm designed to reduce truck turn time—presents unique challenges compared to digital software experimentation. In a digital app, traffic can be randomized at the user session level with zero physical spillover. In a physical Walmart Distribution Center, you cannot easily randomize incoming trucks at the same dock door: trucks share the same physical gate, yard hostlers, and unloading labor. Introducing an untested algorithm into a live building risks operational paralysis, gate backups onto public highways, and supply chain delays.

Drawing from my experience at **Uber**, where I built a large-scale **A/B testing and statistical experimentation platform** enabling **120+ concurrent product experiments** with causal inference controls attributing **$8.7M in quarterly revenue**, I design a robust **Quasi-Experimental Framework** utilizing **Synthetic Control Methods (SCM)** or a **Cluster-Randomized Stepped-Wedge Design**.

```mermaid
flowchart TD
    A[Select Test Facilities: 6 Treatment RDCs] --> B[Construct Synthetic Controls from 40+ Non-Treated RDCs]
    B --> C[Pre-Intervention Baseline Validation: Parallel Trends Check]
    C --> D[Deploy Dynamic Scheduling in Treatment RDCs for 8 Weeks]
    D --> E[Difference-in-Differences DiD Regression with Fixed Effects]
    E --> F[Statistical Significance: Cluster-Robust Standard Errors]
    F --> G[Executive ROI Presentation & Phased Rollout Decision]
```

1. **Selection & Cluster Randomization**: Rather than randomizing individual trucks, I randomize at the facility cluster level. I select 6 treatment RDCs exhibiting diverse operational profiles (high-volume, regional cross-dock, rural vs. urban) and maintain 40+ comparable facilities as donor control candidates.
2. **Synthetic Control Methodology (SCM)**: For each treatment DC, I construct a **Synthetic Twin**—a convex combination of control DCs weighted to match the treatment DC's pre-intervention operational behavior over the preceding 6 months. Metrics matched include daily trailer volume, average gate-to-gate dwell time, OTIF compliance, SKU velocity mix, and unloader labor hours.
3. **Hypothesis Testing & Metrics**:
   - **Primary Metric**: Gate-to-Gate Dwell Time (minutes from security gate check-in to empty trailer gate check-out).
   - **Guardrail Metrics**: Unloader Labor Overtime Hours, On-Time In-Full (OTIF) receiving percentage, and carrier appointment compliance.
4. **Causal Estimation via Difference-in-Differences (DiD)**:
   $$Y_{it} = \\alpha + \\beta \\cdot (\\text{Treatment}_i \\times \\text{Post}_t) + \\gamma_i + \\lambda_t + \\epsilon_{it}$$
   Where $\\gamma_i$ represents facility fixed effects, $\\lambda_t$ represents week/time fixed effects, and $\\beta$ captures the true causal impact of the new scheduling algorithm. I compute **Cluster-Robust Standard Errors** clustered at the facility level to prevent false-positive inflation caused by serial correlation.

At **Uber**, presenting rigorous experimentation results to executive leadership was essential to driving algorithmic adoption. By demonstrating a statistically significant 14-minute reduction in trailer dwell time with zero degradation in guardrail labor costs ($p < 0.01$), I provide Walmart executive leadership with the empirical confidence required to scale the scheduling algorithm across all 150+ distribution centers nationwide.

---

### Question 10: How do you handle missing, corrupted, or asynchronous timestamps in streaming telemetry (GPS, RFID, EDI) when constructing end-to-end transportation visibility pipelines?

#### Answer:
In global supply chain systems, raw physical telemetry is notoriously messy. Carrier GPS devices travel through cellular dead zones; RFID gate readers experience antenna interference; drivers fail to log app status updates; and Electronic Data Interchange messages (**EDI 214**) frequently arrive out of order, hours or days after the physical event occurred. If an analytics pipeline naively computes duration metrics on raw timestamps, it introduces massive data corruption: negative lead times, infinite dwell times, and skewed carrier scorecards. Having engineered large-scale data transformation pipelines processing **180M+ daily records** at **Dish Network** and automated anomaly detection at **Uber**, I implement a multi-layered data cleansing and reconciliation framework in **GCP BigQuery** and **Python**.

1. **Handling Out-of-Order & Asynchronous Event Arrival**:
   Streaming events must be processed using **Event Time** (the exact physical UTC moment the event occurred) rather than **Processing Time** (the time the message landed in Kafka or BigQuery). In BigQuery or Spark Structured Streaming, I enforce a **Watermarking Window** (e.g., 48 hours). For late-arriving EDI messages, the pipeline recalculates the state of open shipments using window functions with **`QUALIFY ROW_NUMBER() OVER (PARTITION BY shipment_id, event_type ORDER BY event_timestamp DESC, ingestion_timestamp DESC) = 1`**, guaranteeing deterministic idempotency.

2. **Temporal Imputation & Monotonicity Enforcement**:
   A physical shipment must adhere to strict physical causality:
   $$\\text{Order Placed} \\le \\text{Tender Accepted} \\le \\text{Origin Departed} \\le \\text{Destination Arrived} \\le \\text{Dock Staged} \\le \\text{Unload Completed}$$
   If `dock_staged_ts` is missing due to an RFID scanner failure, I apply a **constrained imputation algorithm**:
   - If adjacent timestamps exist, I interpolate using historical median stage duration for that specific facility and carrier type:
     $$\\widehat{T}_{\\text{dock}} = T_{\\text{arrival}} + \\text{Median}(\\text{Gate-to-Dock Dwell})_{\\text{Facility}, \\text{Shift}}$$
   - If an impossible timestamp occurs ($T_{\\text{depart}} < T_{\\text{arrive}}$), I flag the record with a `data_quality_anomaly_code = 'CHRONO_INVERSION'`, isolate it from operational dashboards, and route it to an automated data reconciliation queue.

3. **Geofence Spatial Validation for Telemetry Drift**:
   At **Uber**, where I dove deep into raw GPS coordinates across 180K+ mobility records to resolve ride-allocation bottlenecks, I discovered that multipath GPS drift caused false arrival triggers. To prevent carrier GPS pings from triggering premature arrival timestamps outside Walmart RDCs, I implement **Geospatial Polygon Verification** in **BigQuery GIS**:
   ```sql
   ST_CONTAINS(
       ST_GEOGFROMTEXT(rdc_perimeter_polygon), 
       ST_GEOGPOINT(carrier_gps_longitude, carrier_gps_latitude)
   )
   ```
   A trailer is marked as physically arrived only when three consecutive GPS pings over a 5-minute interval fall within the verified geofence polygon. This eliminates false dwell spikes and ensures that Walmart's transportation analytics reflect ground-truth operational reality.

---

### Question 11: Describe your approach to designing an executive C-suite dashboard in Tableau or Power BI that monitors transportation network health and drives operational decision-making.

#### Answer:
An executive dashboard for C-suite supply chain leadership—such as the Senior Vice President of Transportation and Logistics at **Walmart**—must never be a cluttered data dump of operational tables. Executives do not have time to parse through thousands of individual PO rows or decipher complex technical schemas. The dashboard must provide **immediate cognitive clarity**: highlighting high-level financial and operational health in 5 seconds, enabling drill-down into regional variance in 30 seconds, and prescribing root-cause operational levers within 60 seconds. At **Uber**, I constructed C-suite **Tableau**, **Looker**, and **Streamlit** self-serve analytics dashboards that compressed executive reporting cycles from **12 hours to 2 hours per cycle**; at **Dish Network**, I built real-time client-risk dashboards connected to live **Snowflake** semantic layers that directed executive retention strategies.

I structure the executive dashboard using the **Three-Tier Visual Hierarchy**:

```mermaid
flowchart TD
    A[Tier 1: Strategic North Star KPIs - Cost per Case, OTIF %, Fleet Utilization] --> B[Tier 2: Tactical Variance Diagnostics - Regional Heatmaps, Lane Decomposition]
    B --> C[Tier 3: Prescriptive Exception Queue - Critical DC Bottlenecks & At-Risk POs]
```

1. **Tier 1: Strategic North Star Metrics (Executive Summary Strip)**:
   - **Total Inbound Freight Spend vs. Budget** (with % variance and run-rate forecast).
   - **Network On-Time In-Full (OTIF)** compliance against the enterprise target ($95.0\\%$).
   - **Cost Per Case Inbounded** ($/case trended over 13 rolling weeks).
   - **Demurrage & Detention Leakage** (total dollars spent on avoidable carrier waiting fees).
   Each metric features a prominent sparkline, week-over-week delta indicator (colored with accessible muted green/red hues), and a target trajectory band.
2. **Tier 2: Tactical Diagnostics (Variance Exploration)**:
   - **Interactive Geospatial Flow Map**: Visualizing major inbound freight corridors. Line width encodes trailer volume, while color encodes transit time variance or OTIF degradation, instantly highlighting congested lanes into specific DCs.
   - **Carrier Performance Matrix (Four-Quadrant Scatter Plot)**: X-axis represents Volume Share; Y-axis represents OTIF Compliance; bubble size encodes average freight rate ($/mile). This immediately separates dependable core carriers from high-risk, expensive carriers.
   - **Waterfall Variance Decomposition**: Explaining weekly cost fluctuations across Fuel, Rate, Volume, Mode Mix, and Accessorials.
3. **Tier 3: Prescriptive Operational Exceptions (Action Center)**:
   - Filterable list of the **Top 5 Bottleneck DCs** experiencing yard dwell $>P_{90}$, complete with root-cause flags (e.g., *"Chicago RDC: 42 trailers pending live-unload; lumper staffing deficit"*).
   - Automated export functionality into Slack/Teams, allowing executives to assign follow-up action items directly to regional logistics directors with a single click.

To ensure sub-second page performance across billions of historical records, I connect the dashboard to a **Semantic Layer** in **BigQuery / Snowflake** using pre-aggregated materialized views partitioned by `shipment_date` and clustered by `destination_dc_id`. This architecture eliminates dashboard latency, providing Walmart leadership with a responsive, trustworthy compass for daily transportation management.

---

### Question 12: How would you design a predictive model in Python to estimate Inbound Transit Lead Times and forecast arrival dates dynamically as weather and traffic events unfold?

#### Answer:
Static supplier lead times (e.g., *"Supplier ABC requires 5 days to deliver to DC 6021"*) are a major source of stockouts and dock congestion in modern retail supply chains. A snowstorm in the Midwest, an interstate closure on I-80, or a congested rail interchange in Kansas City immediately invalidates static lead times, causing unexpected delivery surges or empty inventory buffers. To solve this, I develop an end-to-end **Dynamic Estimated Time of Arrival (ETA)** and **Lead Time Forecasting Model** in **Python**, moving from static master data to continuous real-time predictions.

1. **Problem Formulation & Target Variable**:
   I formulate the problem as a supervised regression task: predicting the continuous remaining transit duration (in hours) from origin release to final gate arrival.
   $$\\widehat{Y} = \\text{Remaining Transit Time} = f(X_{\\text{Static}}, X_{\\text{Dynamic}}, X_{\\text{Spatial}}, X_{\\text{Weather}})$$

2. **Feature Engineering Pipeline**:
   - **Static Attributes**: Origin-Destination linehaul road mileage, equipment type (Reefer vs Dry Van), team driver vs single driver flag, carrier historic reliability rating.
   - **Dynamic Telemetry Features**: Current distance-to-go (computed via Haversine / Open Source Routing Machine OSRM), cumulative hours driven since last 10-hour mandatory driver reset (Hours of Service HOS modeling), current vehicle speed profile.
   - **Spatial-Temporal Features**: Origin departure hour-of-day, day-of-week, historical congestion index along intermediate highway corridors.
   - **Exogenous Environmental Features**: Live weather alerts from the **National Weather Service API** mapped to highway route polygons (precipitation intensity, snowfall depth, wind gust advisories), and Department of Transportation (DOT) construction zone alerts.

3. **Model Selection & Architecture**:
   I implement an ensemble approach using **LightGBM / XGBoost Regressor** combined with a **Temporal Multi-Layer Perceptron (MLP)**. Gradient boosted decision trees excel on heterogeneous tabular transportation features, handle missing data naturally, and provide fast inference ($<5$ms).
   - **Objective Function**: To penalize severe delays more heavily than early arrivals (since late freight causes stockouts, whereas early freight merely waits in the yard), I utilize an **Asymmetric Huber Loss Function**:
     $$L_\\tau(y, \\hat{y}) = \\begin{cases} \\tau |y - \\hat{y}| - \\frac{1}{2}\\delta \\tau^2 & \\text{if } y - \\hat{y} > \\delta \\\\ (1 - \\tau) |y - \\hat{y}| - \\frac{1}{2}\\delta (1 - \\tau)^2 & \\text{if } y - \\hat{y} < -\\delta \\end{cases}$$
     Setting quantile $\\tau = 0.75$ forces the model to deliver conservative, delay-averse ETA estimates.

4. **Production Deployment & Continuous Re-Scoring**:
   The model is containerized in **Docker** and deployed on **GCP Vertex AI / Cloud Run**. As in-transit trailers emit GPS pings every 15 minutes via EDI 214 or telematics APIs, an **Apache Airflow / Pub-Sub** pipeline streams the updated coordinates to the model endpoint, recalculating the predicted arrival timestamp. If the updated ETA drifts past the scheduled appointment window, an automated alert triggers in Walmart's TMS to proactively reschedule dock unloader labor, guaranteeing smooth cross-dock coordination.

---

### Question 13: How do you identify carrier freight invoice discrepancies and overbilling using SQL and automated audit rules?

#### Answer:
Inbound freight bill auditing is a multi-million-dollar financial recovery channel for enterprise retailers. In a network operating thousands of daily loads across hundreds of third-party motor carriers, invoice errors—such as incorrect base mileage calculations, unauthorized accessorial surcharges, inflated fuel surcharges, and duplicate billings—routinely account for 2.0% to 5.5% of total billed freight spend. At **Uber**, my SQL-based monitoring and anomaly detection pipelines flagged fraudulent patterns and prevented **$2.1M in fraudulent claims per quarter**; applying this rigor to **Walmart Inbound Transportation** ensures complete contractual financial integrity.

To automate freight invoice auditing, I architect a scalable audit reconciliation engine in **GCP BigQuery** that matches carrier billing invoices (**EDI 210**) against contractual tender rate cards and ground-truth execution records (**EDI 214** and WMS logs):

```mermaid
flowchart LR
    A[Carrier Invoice: EDI 210] --> C{Reconciliation Engine: 3-Way Match}
    B[TMS Tender Contract: EDI 204] --> C
    D[WMS Execution: Gate/Dock Logs] --> C
    C -->|Zero Discrepancy| E[Auto-Approve to SAP Accounts Payable]
    C -->|Variance > Tolerance| F[Automated Chargeback & Rejection Notice]
```

The automated audit engine enforces five automated validation rules:
1. **Three-Way Document Match**: The invoice must match an authorized TMS Load Tender (`EDI 204`) and a verified WMS Receiving Receipt. Invoices lacking a corresponding WMS gate check-in are rejected as phantom billings.
2. **Contractual Linehaul Rate Audit**: Recalculates linehaul cost based on contractual lane tariffs:
   $$\\text{Contract Cost} = \\text{Contract Base Rate} + (\\text{Contract Miles} \\times \\text{Rate/Mile})$$
   Any invoice where billed linehaul exceeds contracted tariff by more than $0.00 is flagged for overcharge recovery.
3. **Automated Fuel Surcharge (FSC) Recalculation**: Fuel surcharges are pegged to the weekly **Department of Energy (DOE) National Average Diesel Fuel Price**. The audit query dynamically looks up the exact fuel index published on the day the load was dispatched and computes the contractual FSC percentage:
   $$\\text{Allowed FSC} = \\text{Billed Miles} \\times \\left( \\frac{\\text{DOE Diesel Price} - \\text{Contract Peg Price}}{\\text{Fuel Efficiency Factor}} \\right)$$
   Carriers frequently bill based on current fuel rates rather than dispatch-date rates; the query flags discrepancies greater than $1.00.
4. **Accessorial Fee Ground-Truth Validation**:
   - **Detention**: Verified against WMS gate-in and gate-out timestamps. If a carrier bills for 4 hours of detention ($300), but WMS logs prove the trailer turned around in 90 minutes (within the 2-hour free time), the detention line item is automatically stripped.
   - **Stop-Off Charges**: Verified against GPS geofences and bill-of-lading drop manifests.
5. **Duplicate Invoice & Hash Key Detection**: Computes an MD5 hash of `(carrier_id, bol_number, origin_zip, destination_zip, amount)` to instantly catch carriers resubmitting identical invoices across multiple billing cycles.

By automating these audits in BigQuery, Walmart recovers millions in freight overbilling annually, eliminates manual third-party audit agency fees, and accelerates payment cycles for compliant transportation partners.

---

### Question 14: How would you evaluate the trade-offs between holding safety stock at Regional DCs versus utilizing fast-flow cross-docking for high-velocity grocery and consumable products?

#### Answer:
The strategic tension between holding localized buffer inventory (safety stock at Regional Distribution Centers) versus operating dynamic, zero-inventory **Cross-Docking** (direct transshipment from inbound trailer to outbound store delivery trailer) is at the core of **Walmart's** low-cost retail dominance. With my educational background in **Operations & Supply Chain Management** and analytics experience at **Cipla** where I forecasted demand across 300+ SKUs cutting **$900K in inventory overstock**, I analyze this through a total-cost-to-serve optimization framework.

| Evaluation Criterion | Regional DC Safety Stocking | High-Velocity Cross-Docking |
| :--- | :--- | :--- |
| **Primary Advantage** | Decouples supply from demand; high resilience against supplier lead time volatility. | Minimizes inventory holding costs; eliminates warehouse storage and put-away labor. |
| **Primary Vulnerability** | Capital tie-up; warehouse space congestion; higher inventory obsolescence/shrink risk. | Fragile to inbound transit delays; stockouts propagate directly to store shelves. |
| **Handling Labor Touchpoints** | Multiple: Inbound Unload → Put-Away → Storage Rack → Pick → Pack → Stage → Load. | Minimal: Inbound Unload → Conveyor / Sortation → Outbound Door Stage → Load. |
| **Optimal Product Profile** | Long lead-time imported goods; unpredictable demand; high margin/low volume items. | High-velocity staples (milk, paper towels, seasonal produce); predictable demand; fast turnover. |

To mathematically determine the optimal network allocation per SKU category, I build a **Total Supply Chain Cost Optimization Function**:
$$\\min \\left( C_{\\text{Holding}} + C_{\\text{Handling}} + C_{\\text{Transportation}} + C_{\\text{Stockout}} \\right)$$
Where:
- **Inventory Holding Cost ($C_{\\text{Holding}}$)**: $H = I \\times C \\times Q$, where $I$ is annual capital holding rate (typically $18\\%-25\\%$), $C$ is SKU unit cost, and $Q$ is average inventory held. For cross-docking, $Q \\approx 0$, saving millions in working capital.
- **Warehouse Handling Cost ($C_{\\text{Handling}}$)**: Cross-docking reduces internal touchpoints from 7 touches to 2 touches, cutting internal warehouse labor cost per case by $40\\%$ to $60\\%$.
- **Transportation Cost ($C_{\\text{Transportation}}$)**: Cross-docking requires rigorous, synchronized inbound scheduling. If inbound trucks miss their cross-dock wave, downstream store trucks depart half-empty, driving up outbound linehaul cost per unit.
- **Stockout Cost ($C_{\\text{Stockout}}$)**: The cost of lost retail sales and customer churn if inventory is depleted.

In Python, I construct an automated classification model that segments Walmart's product catalog:
- SKUs exhibiting a low **Coefficient of Variation** ($CV = \\sigma / \\mu < 0.20$) and high turnover velocity are assigned to **100% Cross-Docking**.
- SKUs with high demand volatility ($CV > 0.60$) or volatile supplier lead times are routed to **Safety Stock Buffering**.
This data-driven SKU tiering ensures maximum capital efficiency while insulating Walmart retail stores against supply chain stockouts.

---

### Question 15: How would you establish data contracts between upstream supply chain partners (suppliers, 3PLs) and downstream Walmart analytics teams to prevent schema drift and broken dashboards?

#### Answer:
In a sprawling, multi-tiered enterprise architecture, **schema drift** and unannounced data contract breaches represent the primary cause of pipeline downtime and broken executive dashboards. When an upstream logistics partner or internal engineering team renames an EDI field, alters a timestamp format from UTC to local time, or drops a foreign key column without warning, downstream models fail silently, metrics distort, and operations leadership makes decisions on corrupted data. Drawing from my experience at **Dish Network**, where I led the transition of 14 legacy ETL workflows to modern **dbt** on a structured **Medallion Architecture** enforcing **Data Lineage** and **Data Contracts**, I implement an enterprise-grade contract framework for Walmart Inbound Transportation.

A robust **Data Contract** is an explicit, version-controlled agreement between the data producer (upstream vendor, EDI broker, or TMS microservice) and data consumers (the Inbound Planning and Optimization team). It formally defines:
1. **Schema Specifications**: Exact column names, strict data types, nullability constraints, and allowed categorical enum values.
2. **Semantic & Business Invariants**: Mathematical invariants (e.g., `shipped_cases >= 0`, `mabd_start <= mabd_end`, `pallet_weight_lbs <= 45000`).
3. **Service Level Agreements (SLAs)**: Data freshness cadences (e.g., *"Trailer gate scans must land in BigQuery within 5 minutes of physical capture"*), availability ($99.9\%$), and expected batch volume ranges.

I implement this contract framework using a three-stage automated enforcement pipeline:
```mermaid
flowchart LR
    A[Producer Code / API Update] --> B{Pre-Commit CI/CD Schema Check}
    B -->|Breaking Change| C[Block Pull Request & Notify Consumers]
    B -->|Approved Contract| D[Deploy to Production Kafka / BigQuery]
    D --> E[Real-Time BigQuery Streaming Enforcement]
    E -->|Valid Payload| F[Silver / Gold Analytics Tables]
    E -->|Contract Breach| G[Dead-Letter Queue DLQ & PagerDuty Alert]
```

- **Stage 1: Version-Controlled Contract Definitions**: Contracts are maintained as YAML/JSON Schema files in a centralized Git repository. Any modification to an inbound data contract requires an automated review process and notification to consumer analytics teams.
- **Stage 2: CI/CD Schema Validation**: During producer software builds, pre-merge tests validate that producer API payloads conform to the published JSON Schema. Breaking changes (such as dropping `carrier_scac_code`) fail the CI/CD pipeline immediately.
- **Stage 3: Real-Time Ingestion Quarantine**: At ingestion in **GCP BigQuery**, payloads that violate the contract are rejected from production reporting tables and redirected to a **Quarantine Table (DLQ)**. An automated **Airflow** DAG triggers a high-priority Slack/PagerDuty notification with full error lineage: Producer ID, violated schema rule, and sample corrupted payload.

At **Uber**, where I partnered cross-functionally across product, engineering, and operations leadership, I demonstrated that enforcing data standards and clear governance models directly protects business outcomes. Implementing data contracts at Walmart eliminates silent dashboard failures, ensures absolute trust in executive logistics reporting, and fosters seamless collaboration between technology teams and operational stakeholders.
"""

print("Module 1 (Questions 1 to 15) successfully defined.")
