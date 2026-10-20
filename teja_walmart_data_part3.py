# -*- coding: utf-8 -*-
"""
Part 3: 20 Technical Coding Problems for Teja Talluri
Walmart Senior Data Analyst - Transportation Inbound Planning and Optimization.
Each problem strictly follows:
1. Problem Statement
2. Complete Thought Process
3. Code with Comments
4. Time and Space Complexity
"""

CODING_PROBLEMS = [
    {
        "id": 1,
        "type": "SQL",
        "title": "Supplier On-Time In-Full (OTIF) Compliance & SLA Penalty Billing",
        "statement": """### Problem Statement: Supplier On-Time In-Full (OTIF) Compliance & SLA Penalty Billing

Walmart enforces strict On-Time In-Full (**OTIF**) supplier delivery standards to prevent Distribution Center (RDC) dock congestion and store shelf stockouts. 

You are provided with two tables in **Google BigQuery**:
1. `walmart_supply_chain.purchase_orders`: Contains purchase order metadata (`po_id`, `vendor_id`, `vendor_name`, `destination_dc_id`, `mabd_start_date`, `mabd_end_date`, `ordered_cases`, `po_total_value_usd`).
2. `walmart_supply_chain.inbound_receipts`: Contains physical dock receiving scans (`receipt_id`, `po_id`, `delivery_date`, `received_cases`, `receipt_status`).

**Requirements**:
1. Calculate the monthly OTIF compliance rate for each supplier across all RDCs for the year 2026.
   - **On-Time Criteria**: `delivery_date` must fall within the supplier's Must-Arrive-By-Date window (`delivery_date BETWEEN mabd_start_date AND mabd_end_date`).
   - **In-Full Criteria**: Total received cases for the PO must be at least 98% of ordered cases (`total_received_cases >= 0.98 * ordered_cases`).
   - **OTIF Compliant**: A PO is OTIF-compliant if and only if it is BOTH On-Time AND In-Full.
2. Walmart applies a **3% financial penalty chargeback** on the total purchase order value (`po_total_value_usd`) for every PO that fails OTIF standards.
3. Return the `vendor_id`, `vendor_name`, `delivery_month`, `total_pos`, `ontime_rate_pct`, `infull_rate_pct`, `otif_rate_pct`, and `total_penalty_chargeback_usd`.
4. Filter only for suppliers with at least 20 purchase orders in the month, ordered by `total_penalty_chargeback_usd` descending.""",
        "thought_process": """### Complete Thought Process:

1. **Understand Data Granularity & Potential Duplications**:
   - A single purchase order (`po_id`) can have multiple delivery receipts if the supplier splits shipments across multiple trailers or partial deliveries. Therefore, we must aggregate `inbound_receipts` at the `po_id` level first before joining with `purchase_orders`. Otherwise, joining directly would cause fan-out duplication of PO values and case counts.
   - For delivery date evaluation, if multiple receipts occur, the final delivery receipt date determines whether the order arrived within the MABD window, or each receipt's delivery date must fall within the window. In Walmart's standard practice, the arrival date of the primary trailer determines On-Time status, but any delivery after `mabd_end_date` makes the order Late. Thus, `MAX(delivery_date)` must be `<= mabd_end_date` and `MIN(delivery_date) >= mabd_start_date`.

2. **Metric Definitions & Edge Cases**:
   - **On-Time Flag**: `CASE WHEN min_delivery_date >= po.mabd_start_date AND max_delivery_date <= po.mabd_end_date THEN 1 ELSE 0 END`.
   - **In-Full Flag**: `CASE WHEN COALESCE(rec.total_received_cases, 0) >= 0.98 * po.ordered_cases THEN 1 ELSE 0 END`.
   - **OTIF Flag**: `CASE WHEN (On-Time = 1 AND In-Full = 1) THEN 1 ELSE 0 END`.
   - **Non-Compliant Penalty**: `CASE WHEN OTIF = 0 THEN po.po_total_value_usd * 0.03 ELSE 0.0 END`.
   - Handling missing receipts: If a PO was ordered but never received (`rec.total_received_cases IS NULL`), it is both late and unfulfilled (OTIF = 0), and subject to penalty. We must use a `LEFT JOIN` from `purchase_orders` to `inbound_receipts`.

3. **Query Architecture**:
   - **CTE 1 (`aggregated_receipts`)**: Group by `po_id`, summing `received_cases` and extracting `MIN(delivery_date)` and `MAX(delivery_date)`.
   - **CTE 2 (`po_level_evaluations`)**: Join `purchase_orders` with CTE 1. Compute binary compliance flags and penalty amounts for each PO. Extract month as `DATE_TRUNC(mabd_start_date, MONTH)`.
   - **Final Query**: Group by `vendor_id`, `vendor_name`, `delivery_month`. Compute percentages using `SAFE_DIVIDE`, filter with `HAVING total_pos >= 20`, and sort by total penalty descending.""",
        "code": """-- BigQuery Production SQL: Supplier OTIF Compliance & SLA Penalty Billing
WITH aggregated_receipts AS (
    -- Step 1: Pre-aggregate receipts by PO to prevent row multiplication fan-out
    SELECT 
        po_id,
        MIN(delivery_date) AS first_delivery_date,
        MAX(delivery_date) AS final_delivery_date,
        SUM(CASE WHEN receipt_status = 'ACCEPTED' THEN received_cases ELSE 0 END) AS total_received_cases
    FROM `walmart_supply_chain.inbound_receipts`
    WHERE delivery_date >= '2026-01-01'
    GROUP BY po_id
),

po_evaluations AS (
    -- Step 2: Evaluate individual PO compliance against MABD and 98% case threshold
    SELECT 
        po.po_id,
        po.vendor_id,
        po.vendor_name,
        DATE_TRUNC(po.mabd_start_date, MONTH) AS delivery_month,
        po.po_total_value_usd,
        -- On-time condition: All shipment deliveries must fall within the MABD window
        CASE 
            WHEN rec.first_delivery_date IS NOT NULL
                 AND rec.first_delivery_date >= po.mabd_start_date 
                 AND rec.final_delivery_date <= po.mabd_end_date 
            THEN 1 
            ELSE 0 
        END AS is_on_time,
        -- In-full condition: Total accepted cases >= 98% of ordered quantity
        CASE 
            WHEN COALESCE(rec.total_received_cases, 0) >= (0.98 * po.ordered_cases) 
            THEN 1 
            ELSE 0 
        END AS is_in_full,
        -- OTIF condition: Must satisfy both On-Time AND In-Full simultaneously
        CASE 
            WHEN (rec.first_delivery_date >= po.mabd_start_date AND rec.final_delivery_date <= po.mabd_end_date)
                 AND (COALESCE(rec.total_received_cases, 0) >= 0.98 * po.ordered_cases)
            THEN 1 
            ELSE 0 
        END AS is_otif
    FROM `walmart_supply_chain.purchase_orders` AS po
    LEFT JOIN aggregated_receipts AS rec
        ON po.po_id = rec.po_id
    WHERE po.mabd_start_date >= '2026-01-01' AND po.mabd_start_date < '2027-01-01'
)

-- Step 3: Roll up vendor metrics by month, calculate penalty, and filter for high-volume vendors
SELECT 
    vendor_id,
    vendor_name,
    delivery_month,
    COUNT(po_id) AS total_pos,
    ROUND(100.0 * SAFE_DIVIDE(SUM(is_on_time), COUNT(po_id)), 2) AS ontime_rate_pct,
    ROUND(100.0 * SAFE_DIVIDE(SUM(is_in_full), COUNT(po_id)), 2) AS infull_rate_pct,
    ROUND(100.0 * SAFE_DIVIDE(SUM(is_otif), COUNT(po_id)), 2) AS otif_rate_pct,
    -- 3% penalty applied to total PO value for any failure of OTIF standards
    ROUND(SUM(CASE WHEN is_otif = 0 THEN po_total_value_usd * 0.03 ELSE 0.0 END), 2) AS total_penalty_chargeback_usd
FROM po_evaluations
GROUP BY vendor_id, vendor_name, delivery_month
HAVING total_pos >= 20
ORDER BY total_penalty_chargeback_usd DESC;""",
        "complexity": """- **Time Complexity**: `O(N + M + V log V)` where `N` is the number of receipts, `M` is the number of purchase orders, and `V` is the number of vendor-month groupings. Grouping and hash joining in BigQuery execute in distributed parallel slots in linear time with respect to input rows, followed by a distributed sort on aggregated vendor records.
- **Space Complexity**: `O(M)` intermediate storage required to hold the aggregated receipts CTE and join state across distributed shuffle partitions."""
    },
    {
        "id": 2,
        "type": "SQL",
        "title": "Inbound Trailer Yard Dwell & Tiered Demurrage Fee Acceleration",
        "statement": """### Problem Statement: Inbound Trailer Yard Dwell & Tiered Demurrage Fee Acceleration

When inbound carrier trailers arrive at a Walmart Regional Distribution Center (**RDC**), they are checked into the trailer yard. If an inbound trailer sits idle in the yard before being spotted to an unloading dock door, Walmart incurs demurrage/detention liability or penalizes third-party drop-trailer carriers depending on contractual responsibility.

You are given the table `walmart_supply_chain.yard_trailer_events`:
- `trailer_id` (STRING)
- `carrier_scac` (STRING)
- `destination_dc_id` (STRING)
- `gate_in_timestamp` (TIMESTAMP)
- `dock_spot_timestamp` (TIMESTAMP, NULL if currently dwelling in the yard)
- `trailer_type` (STRING: 'DRY_VAN', 'REEFER', 'FLATBED')
- `trailer_status` (STRING: 'SPOTTED', 'IN_YARD')

**Demurrage Cost Schedule**:
- **0 to 24 hours**: Free grace period ($0/hr).
- **24 to 48 hours**: Standard detention fee of **$50.00/hour** for every hour dwelling beyond 24 hours.
- **48 to 72 hours**: Accelerated detention fee of **$100.00/hour** for every hour dwelling between 48 and 72 hours.
- **72+ hours**: Severe demurrage penalty of **$200.00/hour** for every hour dwelling beyond 72 hours.
- *Refrigerated trailers ('REEFER') incur an additional flat surcharge of $25.00/hour for all dwell hours exceeding 24 hours due to fuel consumption and reefer unit maintenance.*

**Requirements**:
1. For each completed or active trailer visit in October 2026, compute the total dwell duration in hours (if `dock_spot_timestamp` is NULL, calculate dwell duration relative to `'2026-10-31 23:59:59 UTC'`).
2. Calculate the exact cumulative demurrage charge incurred per trailer according to the progressive tiered bracket schedule.
3. Group by `carrier_scac` and `destination_dc_id`, reporting:
   - `total_trailers`
   - `avg_dwell_hours`
   - `trailers_exceeding_24h`
   - `trailers_exceeding_72h`
   - `total_demurrage_charges_usd`
4. Filter for carrier-DC pairs with total demurrage charges > $5,000, ordered by `total_demurrage_charges_usd` DESC.""",
        "thought_process": """### Complete Thought Process:

1. **Calculating Exact Dwell Hours**:
   - Dwell duration is `TIMESTAMP_DIFF(COALESCE(dock_spot_timestamp, TIMESTAMP('2026-10-31 23:59:59 UTC')), gate_in_timestamp, SECOND) / 3600.0`.
   - Using `SECOND` converted to float division avoids integer truncation issues with `HOUR`.

2. **Progressive Bracketed Calculation (Tiered Demurrage)**:
   - Tiered cost calculation must mirror tax brackets. If dwell = 80 hours:
     - Tier 1 (0 to 24h): 24h × $0 = $0.
     - Tier 2 (24 to 48h): 24h × $50 = $1,200.
     - Tier 3 (48 to 72h): 24h × $100 = $2,400.
     - Tier 4 (> 72h): (80 - 72)h × $200 = 8h × $200 = $1,600.
     - Reefer Surcharge: (80 - 24)h × $25 = 56h × $25 = $1,400.
     - Total = 0 + 1200 + 2400 + 1600 + 1400 = $6,600.
   - We implement this cleanly using nested `GREATEST()` and `LEAST()` bounded arithmetic:
     - `tier_2_hrs = GREATEST(0.0, LEAST(dwell_hours - 24.0, 24.0))`
     - `tier_3_hrs = GREATEST(0.0, LEAST(dwell_hours - 48.0, 24.0))`
     - `tier_4_hrs = GREATEST(0.0, dwell_hours - 72.0)`
     - `reefer_hrs = CASE WHEN trailer_type = 'REEFER' THEN GREATEST(0.0, dwell_hours - 24.0) ELSE 0.0 END`

3. **Aggregation & Filtering**:
   - Aggregate by carrier and destination DC.
   - Count trailers exceeding thresholds using `COUNTIF(dwell_hours > 24)`.
   - Apply `HAVING total_demurrage_charges_usd > 5000`.""",
        "code": """-- BigQuery Production SQL: Inbound Trailer Yard Dwell & Tiered Demurrage Calculation
WITH trailer_dwell_base AS (
    SELECT 
        trailer_id,
        carrier_scac,
        destination_dc_id,
        trailer_type,
        gate_in_timestamp,
        dock_spot_timestamp,
        -- Calculate dwell duration in fractional hours, using month-end cutoff for unspotted trailers
        ROUND(
            TIMESTAMP_DIFF(
                COALESCE(dock_spot_timestamp, TIMESTAMP('2026-10-31 23:59:59 UTC')), 
                gate_in_timestamp, 
                SECOND
            ) / 3600.0, 
            2
        ) AS dwell_hours
    FROM `walmart_supply_chain.yard_trailer_events`
    WHERE gate_in_timestamp >= '2026-10-01 00:00:00 UTC'
      AND gate_in_timestamp < '2026-11-01 00:00:00 UTC'
),

bracketed_demurrage AS (
    SELECT 
        trailer_id,
        carrier_scac,
        destination_dc_id,
        trailer_type,
        dwell_hours,
        -- Progressive bracket allocation
        GREATEST(0.0, LEAST(dwell_hours - 24.0, 24.0)) AS hrs_tier_2, -- 24h to 48h
        GREATEST(0.0, LEAST(dwell_hours - 48.0, 24.0)) AS hrs_tier_3, -- 48h to 72h
        GREATEST(0.0, dwell_hours - 72.0) AS hrs_tier_4,              -- 72h+
        -- Reefer temperature monitoring surcharge (applied to all dwell hours beyond 24h)
        CASE 
            WHEN trailer_type = 'REEFER' THEN GREATEST(0.0, dwell_hours - 24.0)
            ELSE 0.0 
        END AS hrs_reefer_surcharge
    FROM trailer_dwell_base
),

trailer_costs AS (
    SELECT 
        trailer_id,
        carrier_scac,
        destination_dc_id,
        dwell_hours,
        -- Compute exact dollar total per trailer
        (hrs_tier_2 * 50.0) + 
        (hrs_tier_3 * 100.0) + 
        (hrs_tier_4 * 200.0) + 
        (hrs_reefer_surcharge * 25.0) AS trailer_demurrage_usd
    FROM bracketed_demurrage
)

-- Rollup by Carrier SCAC and Destination Facility
SELECT 
    carrier_scac,
    destination_dc_id,
    COUNT(trailer_id) AS total_trailers,
    ROUND(AVG(dwell_hours), 2) AS avg_dwell_hours,
    COUNTIF(dwell_hours > 24.0) AS trailers_exceeding_24h,
    COUNTIF(dwell_hours > 72.0) AS trailers_exceeding_72h,
    ROUND(SUM(trailer_demurrage_usd), 2) AS total_demurrage_charges_usd
FROM trailer_costs
GROUP BY carrier_scac, destination_dc_id
HAVING total_demurrage_charges_usd > 5000.0
ORDER BY total_demurrage_charges_usd DESC;""",
        "complexity": """- **Time Complexity**: `O(N log N)` where `N` is the number of trailer gate-in events. Computing timestamps and piecewise arithmetic is `O(1)` per row. The grouping and aggregation operate in `O(N)` parallel BigQuery compute steps, followed by an `O(C log C)` sort on the grouped carrier-DC records.
- **Space Complexity**: `O(N)` temporary memory across compute slots to store individual trailer dwell durations prior to final reduction."""
    },
    {
        "id": 3,
        "type": "SQL",
        "title": "Identifying Chronic Late Inbound Lanes via Percentile Transit Dwell (P90 vs P50)",
        "statement": """### Problem Statement: Identifying Chronic Late Inbound Lanes via Percentile Lead Time Ratio (P90 / P50)

Transportation planners need to identify freight lanes with severe lead time tail risk. Average transit time is misleading because a lane can have an acceptable mean transit time while experiencing extreme, unpredictable delays that disrupt DC cross-dock scheduling.

You are given the table `walmart_supply_chain.linehaul_shipments`:
- `shipment_id` (STRING)
- `origin_vendor_city` (STRING)
- `destination_dc_id` (STRING)
- `carrier_scac` (STRING)
- `dispatched_timestamp` (TIMESTAMP)
- `actual_delivery_timestamp` (TIMESTAMP)
- `planned_transit_hours` (FLOAT64)

**Requirements**:
1. Construct a unique `lane_id` defined as `CONCAT(origin_vendor_city, ' -> ', destination_dc_id)`.
2. Compute actual transit hours as `TIMESTAMP_DIFF(actual_delivery_timestamp, dispatched_timestamp, MINUTE) / 60.0`.
3. For each lane with at least 50 shipments in the past 90 days, calculate:
   - Median transit hours (50th percentile: `P50`)
   - 90th percentile transit hours (`P90`)
   - Planned transit hours baseline (`avg_planned_hours`)
   - Tail Volatility Ratio defined as `P90 / P50`
   - Chronic Delay Rate: Percentage of shipments whose actual transit exceeded planned transit by > 6.0 hours.
4. Filter for "Chronically Unreliable Lanes" where `P90 / P50 >= 1.75` AND `chronic_delay_pct >= 20.0%`.
5. Return the top 10 most volatile lanes ordered by Tail Volatility Ratio descending.""",
        "thought_process": """### Complete Thought Process:

1. **Analytical Percentile Calculation**:
   - In Google BigQuery, exact percentiles across grouped rows can be computed using `PERCENTILE_CONT(actual_transit_hours, 0.50) OVER (PARTITION BY lane_id)` or approximate percentiles using `APPROX_QUANTILES(actual_transit_hours, 100)[OFFSET(50)]`.
   - In standard SQL / PostgreSQL, `PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY actual_transit_hours)` is standard.
   - For BigQuery analytical scale, `APPROX_QUANTILES(actual_transit_hours, 100)` inside a `GROUP BY` is highly performant and avoids window function memory spills.

2. **Metric Definitions**:
   - Actual Transit Hours: `TIMESTAMP_DIFF(actual_delivery_timestamp, dispatched_timestamp, SECOND) / 3600.0`.
   - `P50` = `quantiles[OFFSET(50)]`
   - `P90` = `quantiles[OFFSET(90)]`
   - Tail Volatility Ratio: `SAFE_DIVIDE(P90, P50)`.
   - Chronic Delay Rate: `100.0 * COUNTIF(actual_transit_hours - planned_transit_hours > 6.0) / COUNT(shipment_id)`.

3. **Filtering & Ranking**:
   - Filter `COUNT(shipment_id) >= 50` in the `HAVING` clause.
   - Filter `SAFE_DIVIDE(P90, P50) >= 1.75` and delay pct `>= 20.0%`.
   - Limit to top 10 rows sorted by ratio descending.""",
        "code": """-- BigQuery Production SQL: Chronic Late Inbound Lanes via Percentile Lead Time Ratio
WITH lane_transit_data AS (
    SELECT 
        shipment_id,
        CONCAT(origin_vendor_city, ' -> ', destination_dc_id) AS lane_id,
        planned_transit_hours,
        ROUND(TIMESTAMP_DIFF(actual_delivery_timestamp, dispatched_timestamp, SECOND) / 3600.0, 2) AS actual_transit_hours,
        CASE 
            WHEN (TIMESTAMP_DIFF(actual_delivery_timestamp, dispatched_timestamp, SECOND) / 3600.0) - planned_transit_hours > 6.0 
            THEN 1 
            ELSE 0 
        END AS is_chronically_late
    FROM `walmart_supply_chain.linehaul_shipments`
    WHERE dispatched_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
      AND actual_delivery_timestamp IS NOT NULL
),

lane_quantiles AS (
    SELECT 
        lane_id,
        COUNT(shipment_id) AS total_shipments,
        ROUND(AVG(planned_transit_hours), 2) AS avg_planned_hours,
        ROUND(AVG(actual_transit_hours), 2) AS avg_actual_hours,
        -- Generate 100 equal percentiles (0 to 100) using BigQuery APPROX_QUANTILES
        APPROX_QUANTILES(actual_transit_hours, 100) AS quantiles,
        SUM(is_chronically_late) AS chronic_late_count
    FROM lane_transit_data
    GROUP BY lane_id
    HAVING total_shipments >= 50
)

SELECT 
    lane_id,
    total_shipments,
    avg_planned_hours,
    avg_actual_hours,
    quantiles[OFFSET(50)] AS p50_transit_hours,
    quantiles[OFFSET(90)] AS p90_transit_hours,
    ROUND(SAFE_DIVIDE(quantiles[OFFSET(90)], quantiles[OFFSET(50)]), 2) AS tail_volatility_ratio,
    ROUND(100.0 * SAFE_DIVIDE(chronic_late_count, total_shipments), 2) AS chronic_delay_pct
FROM lane_quantiles
WHERE SAFE_DIVIDE(quantiles[OFFSET(90)], quantiles[OFFSET(50)]) >= 1.75
  AND SAFE_DIVIDE(chronic_late_count, total_shipments) >= 0.20
ORDER BY tail_volatility_ratio DESC
LIMIT 10;""",
        "complexity": """- **Time Complexity**: `O(N log(100))` where `N` is the total number of shipments. `APPROX_QUANTILES` maintains a bounded reservoir digest in memory per group, enabling quasi-linear processing across distributed slots.
- **Space Complexity**: `O(L × 100)` where `L` is the number of distinct transportation lanes, requiring minimal worker memory to hold the quantile arrays."""
    },
    {
        "id": 4,
        "type": "SQL",
        "title": "Cross-Dock Pallet Staging & Peak Inbound Flow Sessionization",
        "statement": """### Problem Statement: Cross-Dock Pallet Staging & Peak Inbound Flow Sessionization

At a Walmart High-Velocity Cross-Dock (**HVDC**), inbound vendor pallets are unloaded onto the staging floor and rapidly sorted into outbound trailers destined for retail stores. The staging floor has a hard physical capacity limit of **600 pallets**. If staging volume exceeds 600 pallets, the facility enters gridlock, forcing inbound trailers to halt unloading.

You are given the table `walmart_supply_chain.pallet_lifecycle_events`:
- `pallet_id` (STRING)
- `dc_id` (STRING)
- `stage_in_timestamp` (TIMESTAMP: Pallet unloaded and placed in staging bay)
- `stage_out_timestamp` (TIMESTAMP: Pallet picked up and loaded onto outbound trailer)

**Requirements**:
1. Treat pallet arrivals (`+1`) and departures (`-1`) as discrete flow events.
2. For facility `'HVDC-8842'` during the peak Black Friday preparation week (`2026-11-15` to `2026-11-22`), compute the concurrent number of active staged pallets across time.
3. Identify all continuous "Congestion Windows" where staged pallet inventory exceeded the 600-pallet buffer capacity.
4. For each congestion window, report:
   - `window_start_time`
   - `window_end_time`
   - `duration_minutes`
   - `peak_pallet_count`
5. Order results by `duration_minutes` descending.""",
        "thought_process": """### Complete Thought Process:

1. **Event Point Transformation (Sweep-Line in SQL)**:
   - Each pallet creates two chronological delta points:
     - Arrival: `event_time = stage_in_timestamp`, `delta = +1`
     - Departure: `event_time = stage_out_timestamp`, `delta = -1`
   - By stacking these events using `UNION ALL`, we can sort by `event_time ASC, delta DESC` (departures before arrivals or vice versa depending on policy; typically departures before arrivals reduces artificial instantaneous spikes).

2. **Running Total via Window Function**:
   - `SUM(delta) OVER (ORDER BY event_time ASC, delta ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS current_staged_pallets`.

3. **Sessionizing Island Windows of Congestion (> 600 pallets)**:
   - Mark rows where `current_staged_pallets > 600` as `in_congestion = 1`.
   - Identify transitions: A new congestion window starts when the current row has `in_congestion = 1` and the previous row (`LAG(in_congestion, 1, 0)`) was 0.
   - Compute a cumulative window group ID: `SUM(is_new_window) OVER (ORDER BY event_time ASC) AS window_id`.
   - Group by `window_id` where `in_congestion = 1` to find `MIN(event_time)`, `MAX(event_time)`, and `MAX(current_staged_pallets)`.""",
        "code": """-- BigQuery Production SQL: Cross-Dock Pallet Staging & Peak Inbound Flow Sessionization
WITH pallet_deltas AS (
    -- Pallet Stage In Event (+1)
    SELECT 
        stage_in_timestamp AS event_time,
        1 AS delta
    FROM `walmart_supply_chain.pallet_lifecycle_events`
    WHERE dc_id = 'HVDC-8842'
      AND stage_in_timestamp >= '2026-11-15 00:00:00 UTC'
      AND stage_in_timestamp <= '2026-11-22 23:59:59 UTC'

    UNION ALL

    -- Pallet Stage Out Event (-1)
    SELECT 
        stage_out_timestamp AS event_time,
        -1 AS delta
    FROM `walmart_supply_chain.pallet_lifecycle_events`
    WHERE dc_id = 'HVDC-8842'
      AND stage_out_timestamp >= '2026-11-15 00:00:00 UTC'
      AND stage_out_timestamp <= '2026-11-22 23:59:59 UTC'
),

running_inventory AS (
    -- Compute cumulative concurrent staged pallets at every timestamp
    SELECT 
        event_time,
        delta,
        SUM(delta) OVER (
            ORDER BY event_time ASC, delta ASC 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS staged_pallet_count
    FROM pallet_deltas
),

congestion_flags AS (
    -- Identify rows exceeding physical capacity and detect window transitions
    SELECT 
        event_time,
        staged_pallet_count,
        CASE WHEN staged_pallet_count > 600 THEN 1 ELSE 0 END AS is_congested,
        CASE 
            WHEN staged_pallet_count > 600 
                 AND COALESCE(LAG(CASE WHEN staged_pallet_count > 600 THEN 1 ELSE 0 END) OVER (ORDER BY event_time ASC), 0) = 0 
            THEN 1 
            ELSE 0 
        END AS is_new_congestion_window
    FROM running_inventory
),

sessionized_windows AS (
    -- Assign a unique session ID to each contiguous overflow episode
    SELECT 
        event_time,
        staged_pallet_count,
        is_congested,
        SUM(is_new_congestion_window) OVER (ORDER BY event_time ASC) AS congestion_session_id
    FROM congestion_flags
)

-- Aggregate each contiguous congestion episode
SELECT 
    congestion_session_id,
    MIN(event_time) AS window_start_time,
    MAX(event_time) AS window_end_time,
    ROUND(TIMESTAMP_DIFF(MAX(event_time), MIN(event_time), SECOND) / 60.0, 1) AS duration_minutes,
    MAX(staged_pallet_count) AS peak_pallet_count
FROM sessionized_windows
WHERE is_congested = 1
GROUP BY congestion_session_id
HAVING duration_minutes > 0
ORDER BY duration_minutes DESC;""",
        "complexity": """- **Time Complexity**: `O(N log N)` where `N` is the number of pallet lifecycle events. The initial sorting by timestamp across the unioned dataset dominates the runtime.
- **Space Complexity**: `O(N)` memory to maintain the sorted window frames and session accumulators."""
    },
    {
        "id": 5,
        "type": "SQL",
        "title": "Carrier Freight Invoice Discrepancy & Fuel Surcharge Audit",
        "statement": """### Problem Statement: Carrier Freight Invoice Discrepancy & Fuel Surcharge Audit

Walmart pays billions of dollars annually in motor freight transportation. Every week, third-party carriers submit electronic invoices (`EDI 210`) for completed inbound shipments. Inbound transportation analysts audit these bills against contractual tariff rates and weekly diesel fuel index tables to prevent overbilling.

You are given three tables:
1. `walmart_supply_chain.carrier_invoices`:
   - `invoice_id` (STRING)
   - `shipment_id` (STRING)
   - `carrier_scac` (STRING)
   - `invoice_date` (DATE)
   - `billed_linehaul_usd` (NUMERIC)
   - `billed_fuel_surcharge_usd` (NUMERIC)
   - `total_billed_usd` (NUMERIC)
2. `walmart_supply_chain.contract_tariffs`:
   - `carrier_scac` (STRING)
   - `origin_zip3` (STRING)
   - `destination_dc_id` (STRING)
   - `effective_start_date` (DATE)
   - `effective_end_date` (DATE)
   - `contract_rate_per_mile` (NUMERIC)
   - `contract_flat_rate` (NUMERIC, NULL if mileage rate applies)
   - `billed_miles` (NUMERIC)
3. `walmart_supply_chain.eia_diesel_fuel_index`:
   - `effective_week_start` (DATE: Monday of each week)
   - `effective_week_end` (DATE: Sunday of each week)
   - `national_avg_diesel_price` (NUMERIC)
   - `fuel_surcharge_per_mile` (NUMERIC: e.g., $0.42/mile based on DOE index pegs)

**Requirements**:
1. Join each invoice with its active contract tariff (matching carrier, origin, destination, and where `invoice_date BETWEEN effective_start_date AND effective_end_date`).
2. Join with the corresponding EIA fuel index week based on `invoice_date`.
3. Compute expected linehaul cost:
   - If `contract_flat_rate` is populated, expected linehaul is `contract_flat_rate`.
   - Otherwise, expected linehaul is `contract_rate_per_mile * billed_miles`.
4. Compute expected fuel surcharge as `fuel_surcharge_per_mile * billed_miles`.
5. Identify billing anomalies where:
   - Linehaul discrepancy: `billed_linehaul_usd - expected_linehaul_usd > $50.00` OR
   - Fuel surcharge discrepancy: `billed_fuel_surcharge_usd - expected_fuel_usd > $15.00`.
6. Return `carrier_scac`, `COUNT(invoice_id)` as `audited_invoices`, `COUNTIF(is_overbilled)` as `overbilled_invoices`, `SUM(overbilled_amount_usd)` as `total_overbilled_leakage_usd`.
7. Order by `total_overbilled_leakage_usd` descending.""",
        "thought_process": """### Complete Thought Process:

1. **Date-Range Joins & Partition Pruning**:
   - Invoices occur on a specific date. Contract tariffs have date range validity (`effective_start_date <= invoice_date <= effective_end_date`).
   - The fuel surcharge table is indexed weekly. We join on `invoice_date BETWEEN effective_week_start AND effective_week_end`.
   - To ensure fast BigQuery execution, we filter invoices on the recent audit quarter (Q3 2026).

2. **Conditional Linehaul Logic**:
   - `expected_linehaul = COALESCE(tariff.contract_flat_rate, tariff.contract_rate_per_mile * tariff.billed_miles)`.
   - `expected_fuel = fuel.fuel_surcharge_per_mile * tariff.billed_miles`.

3. **Discrepancy Flags & Overbill Extraction**:
   - `linehaul_delta = billed_linehaul_usd - expected_linehaul`.
   - `fuel_delta = billed_fuel_surcharge_usd - expected_fuel`.
   - Flag as overbilled if `linehaul_delta > 50.0 OR fuel_delta > 15.0`.
   - Total overbill amount: `GREATEST(0.0, linehaul_delta) + GREATEST(0.0, fuel_delta)`.

4. **Rollup & Summary**:
   - Group by carrier SCAC code to provide sourcing managers with total audit clawback amounts.""",
        "code": """-- BigQuery Production SQL: Freight Invoice Discrepancy & Fuel Surcharge Audit
WITH enriched_invoices AS (
    SELECT 
        inv.invoice_id,
        inv.shipment_id,
        inv.carrier_scac,
        inv.invoice_date,
        inv.billed_linehaul_usd,
        inv.billed_fuel_surcharge_usd,
        inv.total_billed_usd,
        tariff.billed_miles,
        -- Calculate expected linehaul based on contract structure (flat vs per-mile)
        COALESCE(
            tariff.contract_flat_rate, 
            tariff.contract_rate_per_mile * tariff.billed_miles
        ) AS expected_linehaul_usd,
        -- Calculate expected fuel surcharge based on weekly DOE peg
        ROUND(fuel.fuel_surcharge_per_mile * tariff.billed_miles, 2) AS expected_fuel_usd
    FROM `walmart_supply_chain.carrier_invoices` AS inv
    INNER JOIN `walmart_supply_chain.contract_tariffs` AS tariff
        ON inv.carrier_scac = tariff.carrier_scac
       AND inv.origin_zip3 = tariff.origin_zip3
       AND inv.destination_dc_id = tariff.destination_dc_id
       AND inv.invoice_date BETWEEN tariff.effective_start_date AND tariff.effective_end_date
    INNER JOIN `walmart_supply_chain.eia_diesel_fuel_index` AS fuel
        ON inv.invoice_date BETWEEN fuel.effective_week_start AND fuel.effective_week_end
    WHERE inv.invoice_date >= '2026-07-01' AND inv.invoice_date <= '2026-09-30'
),

discrepancy_audit AS (
    SELECT 
        invoice_id,
        carrier_scac,
        billed_linehaul_usd,
        expected_linehaul_usd,
        billed_fuel_surcharge_usd,
        expected_fuel_usd,
        ROUND(billed_linehaul_usd - expected_linehaul_usd, 2) AS linehaul_diff_usd,
        ROUND(billed_fuel_surcharge_usd - expected_fuel_usd, 2) AS fuel_diff_usd,
        -- Flag overbilling thresholds
        CASE 
            WHEN (billed_linehaul_usd - expected_linehaul_usd > 50.00) 
              OR (billed_fuel_surcharge_usd - expected_fuel_usd > 15.00)
            THEN 1 
            ELSE 0 
        END AS is_overbilled,
        -- Calculate net financial leakage
        GREATEST(0.0, billed_linehaul_usd - expected_linehaul_usd) + 
        GREATEST(0.0, billed_fuel_surcharge_usd - expected_fuel_usd) AS net_leakage_usd
    FROM enriched_invoices
)

-- Carrier Audit Summary
SELECT 
    carrier_scac,
    COUNT(invoice_id) AS audited_invoices,
    SUM(is_overbilled) AS overbilled_invoices,
    ROUND(100.0 * SAFE_DIVIDE(SUM(is_overbilled), COUNT(invoice_id)), 2) AS overbill_frequency_pct,
    ROUND(SUM(net_leakage_usd), 2) AS total_overbilled_leakage_usd
FROM discrepancy_audit
GROUP BY carrier_scac
HAVING total_overbilled_leakage_usd > 0
ORDER BY total_overbilled_leakage_usd DESC;""",
        "complexity": """- **Time Complexity**: `O(N log T + N log F)` where `N` is the number of invoices, `T` is tariff records, and `F` is fuel weeks. Range joins with hash partitioning on `carrier_scac` run in linear distributed time.
- **Space Complexity**: `O(N)` storage required to construct the enriched joined CTE across worker nodes."""
    },
    {
        "id": 6,
        "type": "SQL",
        "title": "Dock Door Turnaround Time & Consecutive Idleness Gap Detection",
        "statement": """### Problem Statement: Dock Door Turnaround Time & Consecutive Idleness Gap Detection

Regional Distribution Centers feature dozens of inbound receiving dock doors. Maximizing door productivity requires keeping idle time between consecutive trailer unloads as low as possible. Inbound managers need to audit dock doors to detect abnormal daytime idleness (> 3 consecutive hours without an active trailer) during operational shifts (06:00 to 22:00 UTC).

You are given the table `walmart_supply_chain.dock_door_sessions`:
- `session_id` (STRING)
- `dc_id` (STRING)
- `dock_door_id` (STRING)
- `trailer_id` (STRING)
- `unload_start_timestamp` (TIMESTAMP)
- `unload_end_timestamp` (TIMESTAMP)

**Requirements**:
1. For facility `'RDC-4019'`, use SQL window functions to evaluate consecutive unloading sessions at each individual `dock_door_id`.
2. Compute:
   - `unload_duration_minutes`: Duration the trailer was actively occupying the door.
   - `idle_gap_minutes`: Gap in minutes between the previous trailer's `unload_end_timestamp` and the current trailer's `unload_start_timestamp`.
3. Filter only for daytime idle gaps occurring between 06:00 and 22:00 UTC where `idle_gap_minutes > 180.0` (3 hours).
4. Return `dc_id`, `dock_door_id`, previous trailer ID, current trailer ID, previous unload departure, current unload arrival, and the idle gap duration in minutes.
5. Order by `idle_gap_minutes` descending.""",
        "thought_process": """### Complete Thought Process:

1. **Window Function Partitioning**:
   - We must partition by `dc_id` and `dock_door_id`, and order strictly by `unload_start_timestamp ASC`.
   - To get the previous trailer's finish time, use `LAG(unload_end_timestamp, 1) OVER (PARTITION BY dc_id, dock_door_id ORDER BY unload_start_timestamp ASC)`.
   - To get the previous trailer ID, use `LAG(trailer_id, 1) OVER (...)`.

2. **Computing Idleness & Handling First Session**:
   - For the first session of the period, `LAG` will be NULL. `TIMESTAMP_DIFF` will return NULL, which naturally drops out when filtering `idle_gap_minutes > 180`.
   - Idle gap = `TIMESTAMP_DIFF(unload_start_timestamp, prev_unload_end_timestamp, SECOND) / 60.0`.

3. **Time-of-Day Filtering**:
   - The problem specifies operational daytime shifts (06:00 to 22:00 UTC).
   - Use `EXTRACT(HOUR FROM prev_unload_end_timestamp) BETWEEN 6 AND 21` to ensure we are auditing daytime operational pauses rather than planned graveyard shift closures.""",
        "code": """-- BigQuery Production SQL: Dock Door Idleness Gap Detection
WITH door_session_transitions AS (
    SELECT 
        dc_id,
        dock_door_id,
        trailer_id AS current_trailer_id,
        unload_start_timestamp,
        unload_end_timestamp,
        -- Get previous trailer's departure time and trailer identifier
        LAG(trailer_id, 1) OVER (
            PARTITION BY dc_id, dock_door_id 
            ORDER BY unload_start_timestamp ASC
        ) AS prev_trailer_id,
        LAG(unload_end_timestamp, 1) OVER (
            PARTITION BY dc_id, dock_door_id 
            ORDER BY unload_start_timestamp ASC
        ) AS prev_unload_end_timestamp,
        -- Compute unload duration of current trailer
        ROUND(TIMESTAMP_DIFF(unload_end_timestamp, unload_start_timestamp, SECOND) / 60.0, 1) AS unload_duration_minutes
    FROM `walmart_supply_chain.dock_door_sessions`
    WHERE dc_id = 'RDC-4019'
      AND unload_start_timestamp >= '2026-10-01 00:00:00 UTC'
      AND unload_start_timestamp < '2026-11-01 00:00:00 UTC'
),

gap_analytics AS (
    SELECT 
        dc_id,
        dock_door_id,
        prev_trailer_id,
        prev_unload_end_timestamp,
        current_trailer_id,
        unload_start_timestamp,
        unload_duration_minutes,
        -- Calculate idle gap between consecutive unloads
        ROUND(TIMESTAMP_DIFF(unload_start_timestamp, prev_unload_end_timestamp, SECOND) / 60.0, 1) AS idle_gap_minutes
    FROM door_session_transitions
    WHERE prev_unload_end_timestamp IS NOT NULL
)

-- Filter for daytime operational gaps exceeding 3 hours (180 minutes)
SELECT 
    dc_id,
    dock_door_id,
    prev_trailer_id,
    prev_unload_end_timestamp,
    current_trailer_id,
    unload_start_timestamp,
    idle_gap_minutes
FROM gap_analytics
WHERE idle_gap_minutes > 180.0
  -- Ensure gap commenced during daytime shift (06:00 to 22:00 UTC)
  AND EXTRACT(HOUR FROM prev_unload_end_timestamp) BETWEEN 6 AND 21
ORDER BY idle_gap_minutes DESC;""",
        "complexity": """- **Time Complexity**: `O(N log N)` where `N` is the number of dock door sessions, driven by window function sorting across `dock_door_id` partitions.
- **Space Complexity**: `O(N)` memory required to buffer window partition rows in BigQuery query execution nodes."""
    },
    {
        "id": 7,
        "type": "SQL",
        "title": "Inbound Purchase Order Splitting & Phantom Order Reconciliation",
        "statement": """### Problem Statement: Inbound Purchase Order Splitting & Phantom Order Reconciliation

Suppliers frequently fulfill large Walmart Purchase Orders (**POs**) across multiple shipments, generating separate **Advanced Shipping Notices (ASNs)** and delivery bills. Occasionally, "phantom shipments" occur—where a shipment is created in the TMS but never physically arrives at the DC, or suppliers accidentally over-deliver unauthorized merchandise.

You are given:
1. `walmart_supply_chain.purchase_order_lines`:
   - `po_id` (STRING)
   - `sku_id` (STRING)
   - `ordered_units` (INT64)
   - `unit_cost_usd` (NUMERIC)
2. `walmart_supply_chain.asn_shipment_receipts`:
   - `asn_id` (STRING)
   - `po_id` (STRING)
   - `sku_id` (STRING)
   - `shipped_units` (INT64)
   - `received_units` (INT64, 0 if trailer never arrived)
   - `receiving_status` (STRING: 'RECEIVED', 'DAMAGED', 'NEVER_ARRIVED')

**Requirements**:
1. Perform a full reconciliation of every PO SKU line item across all its associated ASNs.
2. Calculate:
   - `total_ordered_units`
   - `total_shipped_units`
   - `total_received_units`
   - `fulfillment_ratio_pct`: `(total_received_units / total_ordered_units) * 100`
   - `unfulfilled_units`: `GREATEST(0, total_ordered_units - total_received_units)`
   - `over_delivered_units`: `GREATEST(0, total_received_units - total_ordered_units)`
   - `phantom_units`: Units marked as shipped in an ASN but where `receiving_status = 'NEVER_ARRIVED'`.
3. Categorize the PO Line Status into:
   - `'PERFECT_MATCH'` (received = ordered)
   - `'SHORT_SHIPMENT'` (received < ordered)
   - `'OVER_SHIPMENT'` (received > ordered)
   - `'PHANTOM_DISCREPANCY'` (phantom_units > 0)
4. Filter for POs with total variance value (`ABS(total_received_units - total_ordered_units) * unit_cost_usd`) > $2,500.
5. Order by total variance value descending.""",
        "thought_process": """### Complete Thought Process:

1. **Aggregation Level**:
   - The primary grain is `po_id, sku_id`.
   - `asn_shipment_receipts` has multiple rows per `po_id, sku_id` because suppliers split shipments across different ASNs. We must aggregate receipts first before joining to PO lines.

2. **Metric Formulations**:
   - Total Shipped = `SUM(shipped_units)`.
   - Total Received = `SUM(CASE WHEN receiving_status = 'RECEIVED' THEN received_units ELSE 0 END)`.
   - Phantom Units = `SUM(CASE WHEN receiving_status = 'NEVER_ARRIVED' THEN shipped_units ELSE 0 END)`.

3. **Status Classification Logic**:
   - When `phantom_units > 0`, that takes precedence for fraud/audit alerting (`'PHANTOM_DISCREPANCY'`).
   - Otherwise check equality, under-delivery, or over-delivery.

4. **Financial Impact Filtering**:
   - Variance dollar value: `ABS(total_received - total_ordered) * unit_cost_usd`.
   - Filter `> 2500` and order descending.""",
        "code": """-- BigQuery Production SQL: PO Splitting & Phantom Order Reconciliation
WITH aggregated_asn_receipts AS (
    SELECT 
        po_id,
        sku_id,
        SUM(shipped_units) AS total_shipped_units,
        SUM(CASE WHEN receiving_status = 'RECEIVED' THEN received_units ELSE 0 END) AS total_received_units,
        SUM(CASE WHEN receiving_status = 'NEVER_ARRIVED' THEN shipped_units ELSE 0 END) AS phantom_units
    FROM `walmart_supply_chain.asn_shipment_receipts`
    GROUP BY po_id, sku_id
),

po_line_reconciliation AS (
    SELECT 
        po.po_id,
        po.sku_id,
        po.ordered_units,
        po.unit_cost_usd,
        COALESCE(asn.total_shipped_units, 0) AS total_shipped_units,
        COALESCE(asn.total_received_units, 0) AS total_received_units,
        COALESCE(asn.phantom_units, 0) AS phantom_units,
        -- Variance quantities
        GREATEST(0, po.ordered_units - COALESCE(asn.total_received_units, 0)) AS unfulfilled_units,
        GREATEST(0, COALESCE(asn.total_received_units, 0) - po.ordered_units) AS over_delivered_units,
        -- Fulfillment percentage
        ROUND(100.0 * SAFE_DIVIDE(COALESCE(asn.total_received_units, 0), po.ordered_units), 2) AS fulfillment_ratio_pct,
        -- Financial variance impact
        ROUND(ABS(COALESCE(asn.total_received_units, 0) - po.ordered_units) * po.unit_cost_usd, 2) AS variance_value_usd,
        -- Categorization
        CASE 
            WHEN COALESCE(asn.phantom_units, 0) > 0 THEN 'PHANTOM_DISCREPANCY'
            WHEN COALESCE(asn.total_received_units, 0) = po.ordered_units THEN 'PERFECT_MATCH'
            WHEN COALESCE(asn.total_received_units, 0) < po.ordered_units THEN 'SHORT_SHIPMENT'
            ELSE 'OVER_SHIPMENT'
        END AS po_line_reconciliation_status
    FROM `walmart_supply_chain.purchase_order_lines` AS po
    LEFT JOIN aggregated_asn_receipts AS asn
        ON po.po_id = asn.po_id
       AND po.sku_id = asn.sku_id
)

SELECT 
    po_id,
    sku_id,
    ordered_units,
    total_shipped_units,
    total_received_units,
    phantom_units,
    unfulfilled_units,
    over_delivered_units,
    fulfillment_ratio_pct,
    variance_value_usd,
    po_line_reconciliation_status
FROM po_line_reconciliation
WHERE variance_value_usd > 2500.00
ORDER BY variance_value_usd DESC;""",
        "complexity": """- **Time Complexity**: `O(P + A)` where `P` is the number of PO lines and `A` is the number of ASN receipt lines. Grouping ASNs and executing the hash left join operates in linear distributed time.
- **Space Complexity**: `O(P)` memory to maintain the outer join state across worker slots."""
    },
    {
        "id": 8,
        "type": "Python",
        "title": "Inbound Purchase Order Pallet Packing & 3D Container Cube Optimization",
        "statement": """### Problem Statement: Inbound Purchase Order Pallet Packing & 3D Container Cube Optimization

Walmart's Inbound Planning team needs to minimize the total number of 53ft dry van trailers dispatched from vendor consolidation centers. Each trailer has strict physical and legal capacity constraints:
- **Maximum Payload Weight**: `44,000 lbs`
- **Maximum Usable Volume**: `3,850 cubic feet`
- **Maximum Standard Pallet Floor Spots**: `26 pallets` (53ft trailer holds 26 standard 40" x 48" pallets on the floor).

You are given a list of inbound purchase order shipments. Each shipment is represented as a dictionary:
```python
shipment = {
    "shipment_id": "SHP-101",
    "weight_lbs": 2800.0,
    "volume_cuft": 210.0,
    "pallet_spots": 2,
    "is_stackable": True  # If True, can be stacked, consuming only 1 floor spot per 2 pallets
}
```

**Requirements**:
1. Implement a Python function `pack_inbound_trailers(shipments: list[dict]) -> dict` that packs all shipments into trailers using the **First-Fit Decreasing (FFD)** heuristic with multi-dimensional constraint checks (weight, volume, floor spots).
2. For stackable items, every pair of 2 pallets consumes only `1.0` effective floor spot (an odd single pallet consumes `1.0` spot).
3. The function must return:
   - `total_trailers_required`: Integer count of trailers used.
   - `trailers`: A list of trailer assignments with loaded shipment IDs, total weight, total volume, floor spots used, and percent weight/cube utilization.
   - `overall_cube_utilization_pct`: Average cube utilization across all dispatched trailers.
4. Provide complete type annotations, docstrings, and robust handling of oversize single items that exceed trailer maximums.""",
        "thought_process": """### Complete Thought Process:

1. **Problem Classification**:
   - This is an instance of the **Multi-Dimensional Vector Bin Packing Problem** (NP-hard). In real-world transportation logistics, exact integer linear programming (MILP) solvers like Gurobi are used, but for high-throughput streaming heuristics, **First-Fit Decreasing (FFD)** provides provably robust approximations (within 11/9 OPT + 1).

2. **Sorting Heuristic for Multi-Dimensional Constraints**:
   - To order items for FFD, we compute a normalized "bottleneck score" for each shipment:
     `score = max(weight / MAX_WEIGHT, volume / MAX_VOLUME, floor_spots / MAX_SPOTS)`.
   - Sorting shipments descending by this normalized bottleneck score ensures that the largest, most constrained shipments are packed first.

3. **Effective Floor Spot Calculation**:
   - If `is_stackable` is True: `effective_spots = math.ceil(pallet_spots / 2.0)`.
   - If False: `effective_spots = pallet_spots`.

4. **Greedy First-Fit Placement**:
   - Iterate through each sorted shipment.
   - Check existing trailers in order. If a trailer has sufficient remaining weight capacity (`rem_wt >= item_wt`), remaining volume capacity (`rem_vol >= item_vol`), and remaining floor spots (`rem_spots >= item_spots`), place the item in that trailer.
   - If no existing trailer can fit the shipment, open a new trailer.

5. **Edge Cases**:
   - An individual shipment exceeding max weight, volume, or floor spots raises a `ValueError("Shipment exceeds maximum trailer capacity")`.""",
        "code": """import math
from typing import Any

MAX_WEIGHT_LBS = 44000.0
MAX_VOLUME_CUFT = 3850.0
MAX_FLOOR_SPOTS = 26.0

def calculate_effective_floor_spots(pallet_spots: int, is_stackable: bool) -> float:
    \"\"\"Calculates effective floor spots considering vertical pallet stackability.\"\"\"
    if is_stackable:
        return float(math.ceil(pallet_spots / 2.0))
    return float(pallet_spots)

def pack_inbound_trailers(shipments: list[dict[str, Any]]) -> dict[str, Any]:
    \"\"\"
    Packs inbound PO shipments into 53ft trailers using multi-dimensional First-Fit Decreasing (FFD).
    
    Constraints per trailer:
      - Weight <= 44,000 lbs
      - Volume <= 3,850 cu ft
      - Floor spots <= 26
    \"\"\"
    # Pre-validate individual items against hard physical trailer limits
    for s in shipments:
        eff_spots = calculate_effective_floor_spots(s['pallet_spots'], s.get('is_stackable', False))
        if s['weight_lbs'] > MAX_WEIGHT_LBS or s['volume_cuft'] > MAX_VOLUME_CUFT or eff_spots > MAX_FLOOR_SPOTS:
            raise ValueError(f"Shipment {s['shipment_id']} exceeds maximum single-trailer physical limits.")

    # Sort shipments descending by normalized bottleneck consumption ratio
    def bottleneck_ratio(item: dict[str, Any]) -> float:
        eff_spots = calculate_effective_floor_spots(item['pallet_spots'], item.get('is_stackable', False))
        return max(
            item['weight_lbs'] / MAX_WEIGHT_LBS,
            item['volume_cuft'] / MAX_VOLUME_CUFT,
            eff_spots / MAX_FLOOR_SPOTS
        )

    sorted_shipments = sorted(shipments, key=bottleneck_ratio, reverse=True)

    # List of open trailers
    # Each trailer: dict with accumulated metrics and list of shipment IDs
    trailers: list[dict[str, Any]] = []

    for item in sorted_shipments:
        item_wt = item['weight_lbs']
        item_vol = item['volume_cuft']
        item_spots = calculate_effective_floor_spots(item['pallet_spots'], item.get('is_stackable', False))
        placed = False

        # Attempt to fit into existing open trailers (First-Fit)
        for t in trailers:
            if (t['total_weight_lbs'] + item_wt <= MAX_WEIGHT_LBS and
                t['total_volume_cuft'] + item_vol <= MAX_VOLUME_CUFT and
                t['total_floor_spots'] + item_spots <= MAX_FLOOR_SPOTS):
                
                t['shipment_ids'].append(item['shipment_id'])
                t['total_weight_lbs'] += item_wt
                t['total_volume_cuft'] += item_vol
                t['total_floor_spots'] += item_spots
                placed = True
                break

        # If it doesn't fit in any existing trailer, dispatch a new trailer
        if not placed:
            new_trailer = {
                'trailer_index': len(trailers) + 1,
                'shipment_ids': [item['shipment_id']],
                'total_weight_lbs': item_wt,
                'total_volume_cuft': item_vol,
                'total_floor_spots': item_spots
            }
            trailers.append(new_trailer)

    # Post-process trailers to compute final utilization percentages
    total_cube_util_sum = 0.0
    for t in trailers:
        t['weight_utilization_pct'] = round((t['total_weight_lbs'] / MAX_WEIGHT_LBS) * 100.0, 2)
        t['cube_utilization_pct'] = round((t['total_volume_cuft'] / MAX_VOLUME_CUFT) * 100.0, 2)
        t['floor_spot_utilization_pct'] = round((t['total_floor_spots'] / MAX_FLOOR_SPOTS) * 100.0, 2)
        total_cube_util_sum += t['cube_utilization_pct']

    avg_cube_util = round(total_cube_util_sum / len(trailers), 2) if trailers else 0.0

    return {
        'total_trailers_required': len(trailers),
        'trailers': trailers,
        'overall_cube_utilization_pct': avg_cube_util
    }""",
        "complexity": """- **Time Complexity**: `O(N log N + N × K)` where `N` is the number of shipments and `K` is the number of trailers created (`K <= N`). Sorting takes `O(N log N)`. In the worst case, each item inspects all `K` open trailers, yielding `O(N × K)`.
- **Space Complexity**: `O(N)` auxiliary memory required to store the sorted shipment copies and trailer packing allocations."""
    },
    {
        "id": 9,
        "type": "Python",
        "title": "Rolling Z-Score Anomaly Detection on Carrier Transit Lead Times",
        "statement": """### Problem Statement: Rolling Z-Score Anomaly Detection on Carrier Transit Lead Times

Inbound planners receive continuous GPS and EDI 214 transit updates for motor carrier trailers. To detect acute corridor disruptions (e.g., severe snowstorms, highway closures, carrier breakdowns) without waiting for end-of-month reporting, you must implement a real-time streaming anomaly detector.

**Requirements**:
Implement a Python class `StreamingTransitAnomalyDetector`:
1. Initialized with:
   - `window_size` (int): Number of historical deliveries to maintain in the rolling baseline (e.g., `W = 30`).
   - `z_threshold` (float): Z-score threshold for anomaly classification (e.g., `Z = 2.5`).
   - `warmup_periods` (int): Minimum number of observations required before triggering anomalies (e.g., `10`).
2. Method `process_observation(shipment_id: str, transit_hours: float) -> dict`:
   - Evaluates the incoming shipment's transit lead time against the current sliding window baseline.
   - Calculates the rolling mean and sample standard deviation using **only historical observations** (no lookahead bias).
   - Computes the Z-Score: `Z = (transit_hours - mean) / std`.
   - Returns a dictionary:
     ```python
     {
         "shipment_id": shipment_id,
         "transit_hours": transit_hours,
         "rolling_mean": float,
         "rolling_std": float,
         "z_score": float,
         "is_anomaly": bool,
         "anomaly_type": str  # 'NORMAL', 'SEVERE_DELAY', or 'WARMUP'
     }
     ```
   - **Contamination Guard**: If an observation is flagged as a `SEVERE_DELAY` (`Z >= z_threshold`), it must **not** be appended to the rolling baseline window to prevent contaminating future normal baselines. Normal observations are appended, maintaining at most `window_size` elements in FIFO order.
   - Operates in strict `O(1)` amortized time per incoming observation using Welford's algorithm or sliding window rolling sums.""",
        "thought_process": """### Complete Thought Process:

1. **Strict Lookahead Guard**:
   - The anomaly evaluation for shipment `i` must rely strictly on the window computed from shipments `0` to `i-1`.
   - If the current window has fewer observations than `warmup_periods`, we output `anomaly_type = 'WARMUP'` and `is_anomaly = False`, but we append the value to build the baseline.

2. **O(1) Rolling Sum and Sum of Squares**:
   - Maintaining rolling mean and variance can be done by tracking:
     - `sum_x = sum(x)`
     - `sum_x2 = sum(x^2)`
     - Using a double-ended queue `collections.deque(maxlen=window_size)`.
   - When an old element is popped from the left of the deque:
     - `sum_x -= old_val`
     - `sum_x2 -= old_val ** 2`
   - When a new element is appended:
     - `sum_x += new_val`
     - `sum_x2 += new_val ** 2`
   - Sample Variance: `s^2 = (sum_x2 - (sum_x^2 / n)) / (n - 1)`.
   - Standard Deviation: `s = sqrt(max(0.0, s^2))`.

3. **Contamination Guard**:
   - If `is_anomaly` is True (`z_score >= z_threshold`), we reject the data point from entering the sliding window baseline. This prevents a 5-day snowstorm from skewing the mean lead time upwards and normalizing future delays.

4. **Numerical Stability**:
   - When all observations are identical (`std == 0.0`), set `z_score = 0.0` if `transit_hours == mean`, else a large value (or float('inf')). We handle `std < 1e-6` safely.""",
        "code": """import collections
import math
from typing import Any

class StreamingTransitAnomalyDetector:
    \"\"\"
    Detects transit lead time anomalies in streaming telemetry using an O(1) rolling Z-score.
    Includes a contamination guard to prevent anomalous delays from skewing the baseline.
    \"\"\"
    def __init__(self, window_size: int = 30, z_threshold: float = 2.5, warmup_periods: int = 10):
        if window_size < 2:
            raise ValueError("window_size must be at least 2.")
        self.window_size = window_size
        self.z_threshold = z_threshold
        self.warmup_periods = warmup_periods

        self.window: collections.deque[float] = collections.deque()
        self.sum_x: float = 0.0
        self.sum_x2: float = 0.0

    def process_observation(self, shipment_id: str, transit_hours: float) -> dict[str, Any]:
        n = len(self.window)

        # Warmup phase: insufficient history to establish statistical baseline
        if n < self.warmup_periods:
            self._append_to_baseline(transit_hours)
            return {
                "shipment_id": shipment_id,
                "transit_hours": transit_hours,
                "rolling_mean": round(self.sum_x / len(self.window), 2),
                "rolling_std": 0.0,
                "z_score": 0.0,
                "is_anomaly": False,
                "anomaly_type": "WARMUP"
            }

        # Calculate baseline statistics from existing window (prior to adding current observation)
        mean = self.sum_x / n
        variance = (self.sum_x2 - (self.sum_x ** 2) / n) / (n - 1)
        variance = max(0.0, variance)  # Prevent floating point precision negative zero
        std = math.sqrt(variance)

        # Compute Z-score with zero-variance protection
        if std < 1e-6:
            z_score = 0.0 if abs(transit_hours - mean) < 1e-6 else 999.0
        else:
            z_score = (transit_hours - mean) / std

        is_severe_delay = z_score >= self.z_threshold

        # Contamination Guard: Only append normal observations to baseline window
        if not is_severe_delay:
            self._append_to_baseline(transit_hours)
            anomaly_type = "NORMAL"
        else:
            anomaly_type = "SEVERE_DELAY"

        return {
            "shipment_id": shipment_id,
            "transit_hours": round(transit_hours, 2),
            "rolling_mean": round(mean, 2),
            "rolling_std": round(std, 2),
            "z_score": round(z_score, 2),
            "is_anomaly": is_severe_delay,
            "anomaly_type": anomaly_type
        }

    def _append_to_baseline(self, val: float) -> None:
        \"\"\"Maintains rolling sum and sum-of-squares in O(1) time.\"\"\"
        if len(self.window) == self.window_size:
            old_val = self.window.popleft()
            self.sum_x -= old_val
            self.sum_x2 -= (old_val ** 2)

        self.window.append(val)
        self.sum_x += val
        self.sum_x2 += (val ** 2)""",
        "complexity": """- **Time Complexity**: `O(1)` per observation. All deque operations, rolling sum adjustments, and statistical calculations execute in constant time.
- **Space Complexity**: `O(W)` where `W` is the `window_size` (e.g., 30 floats stored in the deque)."""
    },
    {
        "id": 10,
        "type": "Python",
        "title": "Carrier Lead Time Survival Analysis & Hazard Rate Estimation from Scratch",
        "statement": """### Problem Statement: Carrier Lead Time Survival Analysis & Hazard Rate Estimation from Scratch

In transportation planning, evaluating carrier reliability strictly on completed shipments introduces severe **survivorship bias**. Shipments that are still in-transit have not yet arrived; ignoring them underestimates the true transit delay probability.

To resolve this, we model shipment transit duration using **Survival Analysis with Right-Censoring**:
- Each shipment has an elapsed transit time `T_i` (hours).
- An event indicator `E_i`:
  - `E_i = 1` if the shipment arrived at the dock (uncensored delivery event).
  - `E_i = 0` if the shipment is currently in-transit at the snapshot cutoff time (right-censored).

**Requirements**:
Implement a Python function `kaplan_meier_estimator(records: list[dict]) -> dict` from scratch (using only Python standard library):
1. Input records: `[{"shipment_id": "S1", "transit_hours": 36.5, "event": 1}, ...]`.
2. Compute the **Kaplan-Meier survival function** `S(t) = P(Transit > t)` for all unique delivery event times.
3. Compute the **cumulative hazard rate** `H(t) = -ln(S(t))`.
4. Calculate key summary metrics:
   - Median Transit Time (`P50` where `S(t) <= 0.50`).
   - 90th percentile arrival time (`P90` where `S(t) <= 0.10`).
   - Probability that a shipment takes longer than 48 hours: `P(T > 48)`.
5. Return a structured dictionary with timeline steps and calculated percentile metrics.""",
        "thought_process": """### Complete Thought Process:

1. **Kaplan-Meier Mathematical Formulation**:
   - Let distinct uncensored event times be `t_1 < t_2 < ... < t_k`.
   - At each event time `t_i`:
     - `n_i`: Number of shipments "at risk" (in transit or arriving at `>= t_i`).
     - `d_i`: Number of completed delivery events at exactly `t_i`.
   - The conditional survival probability at step `i` is `(1 - d_i / n_i)`.
   - The cumulative survival probability is `S(t_i) = S(t_{i-1}) * (1 - d_i / n_i)` with `S(0) = 1.0`.

2. **Handling Right-Censoring**:
   - Right-censored observations (`event = 0`) contribute to the risk set `n_i` for all event times `t_k <= T_censored`. Once the timeline passes `T_censored`, they exit the risk set without being counted in `d_i`.

3. **Step-by-Step Algorithm**:
   - Sort all observations ascending by `transit_hours`. If times are tied, uncensored events (`event = 1`) should precede censored events (`event = 0`).
   - Identify unique uncensored event times.
   - For each unique event time `t`:
     - Count total items with `transit_hours >= t` (risk set `n`).
     - Count completed deliveries with `transit_hours == t` and `event == 1` (`d`).
     - Compute survival step: `S = S * (1 - d / n)`.
     - Cumulative hazard: `H = -math.log(max(S, 1e-9))`.

4. **Extracting Percentiles**:
   - Median time `P50`: Smallest `t` where `S(t) <= 0.50`.
   - `P90`: Smallest `t` where `S(t) <= 0.10`.""",
        "code": """import math
from typing import Any

def kaplan_meier_estimator(records: list[dict[str, Any]]) -> dict[str, Any]:
    \"\"\"
    Computes the non-parametric Kaplan-Meier survival curve and cumulative hazard from scratch.
    Correctly accounts for right-censored in-transit shipments.
    \"\"\"
    if not records:
        return {"error": "Empty dataset provided."}

    # Sort records ascending by transit duration; events before censored if tied
    sorted_records = sorted(records, key=lambda x: (x['transit_hours'], -x['event']))

    # Extract all distinct times where an actual arrival occurred (event == 1)
    event_times = sorted(list(set(r['transit_hours'] for r in sorted_records if r['event'] == 1)))

    timeline = []
    current_survival = 1.0
    p50_median = None
    p90_tail = None
    p_gt_48 = 1.0

    total_records = len(sorted_records)

    for t in event_times:
        # Number at risk: shipments with duration >= t
        at_risk = sum(1 for r in sorted_records if r['transit_hours'] >= t)
        # Number of observed delivery events at this exact timestamp
        events_occurred = sum(1 for r in sorted_records if r['transit_hours'] == t and r['event'] == 1)

        if at_risk > 0:
            current_survival *= (1.0 - (events_occurred / at_risk))
            current_hazard = -math.log(max(current_survival, 1e-9))
        else:
            current_hazard = float('inf')

        step_data = {
            "time_hours": round(t, 2),
            "at_risk": at_risk,
            "events": events_occurred,
            "survival_prob": round(current_survival, 4),
            "cumulative_hazard": round(current_hazard, 4)
        }
        timeline.append(step_data)

        # Track P50 median lead time
        if p50_median is None and current_survival <= 0.50:
            p50_median = round(t, 2)

        # Track P90 tail delivery time
        if p90_tail is None and current_survival <= 0.10:
            p90_tail = round(t, 2)

        # Track survival past 48 hours
        if t <= 48.0:
            p_gt_48 = round(current_survival, 4)

    return {
        "total_sample_size": total_records,
        "completed_deliveries": sum(1 for r in records if r['event'] == 1),
        "in_transit_censored": sum(1 for r in records if r['event'] == 0),
        "median_transit_p50_hours": p50_median,
        "tail_transit_p90_hours": p90_tail,
        "prob_transit_exceeds_48h": p_gt_48,
        "survival_curve_sample": timeline[:10]  # First 10 discrete steps
    }""",
        "complexity": """- **Time Complexity**: `O(N log N + K × N)` where `N` is the number of shipment records and `K` is the number of unique delivery event times (`K <= N`). Sorting takes `O(N log N)`. Iterating through unique times to count risk sets takes `O(K × N)`. (Can be optimized to `O(N log N)` using two pointers or prefix counts).
- **Space Complexity**: `O(N)` auxiliary memory to store sorted records and survival step points."""
    },
    {
        "id": 11,
        "type": "Python",
        "title": "Multi-Modal Inbound Freight Routing with Transshipment Hubs (Dijkstra)",
        "statement": """### Problem Statement: Multi-Modal Inbound Freight Routing with Transshipment Hubs (Dijkstra)

Walmart's inbound freight moves across a complex multi-modal transportation network comprising:
- Direct Over-the-Road (**OTR**) Truckload
- Intermodal Rail (drayage to ramp -> rail linehaul -> destination drayage)
- Regional Consolidation Centers (**RCC**)

Each directed edge between two logistics nodes (e.g., `'Supplier_Factory'`, `'Rail_Ramp_Chicago'`, `'RCC_Dallas'`, `'RDC_6021'`) has:
- `cost_usd`: Financial freight cost of moving the container across that link.
- `transit_hours`: Physical transit time on that link.
- `mode`: `'RAIL'`, `'OTR'`, or `'TRANSFER'`.

**Requirements**:
Implement a Python function `optimize_freight_route(network_graph: dict, origin: str, destination: str, max_transit_hours: float) -> dict`:
1. Find the path that **minimizes total freight cost** while strictly guaranteeing that the total path transit hours do not exceed `max_transit_hours`.
2. If multiple paths meet the time constraint, return the path with the lowest dollar cost.
3. If no path can reach the destination within `max_transit_hours`, return `{"feasible": False, "message": "No route satisfies maximum transit time SLA."}`.
4. Return:
   - `feasible`: True
   - `total_cost_usd`: float
   - `total_transit_hours`: float
   - `path_nodes`: list of nodes from origin to destination
   - `modes_used`: list of modes along the chosen path.""",
        "thought_process": """### Complete Thought Process:

1. **Problem Classification**:
   - This is the **Constrained Shortest Path Problem (CSPP)** (min cost subject to time <= T_max), which is weakly NP-hard.
   - For practical logistics graphs where node counts are moderate (hundreds of hubs and ramps), **Constrained Dijkstra / Priority Queue Branch and Bound** provides fast, exact solutions.

2. **Algorithm Design (Modified Dijkstra with State Pruning)**:
   - State representation in min-heap: `(accumulated_cost, accumulated_time, current_node, path_nodes, modes_used)`.
   - The min-heap prioritizes by `cost`. The first time we pop the destination node with `accumulated_time <= max_transit_hours`, we are guaranteed to have the optimal minimum-cost path because edge costs are non-negative.
   - **Dominance Pruning**:
     - Maintain a dictionary `min_time_at_node[node]` that records the best (lowest) transit time seen so far for that node at this or a lower cost.
     - If we reach `neighbor` with both `new_time >= min_time_at_node[neighbor]` and higher cost, we can prune that search branch immediately.

3. **Edge Cases**:
   - Origin equals destination (zero cost, zero time).
   - Disconnected graph or unreachable destination.
   - No path meeting the `max_transit_hours` SLA.""",
        "code": """import heapq
from typing import Any

def optimize_freight_route(
    network_graph: dict[str, list[dict[str, Any]]], 
    origin: str, 
    destination: str, 
    max_transit_hours: float
) -> dict[str, Any]:
    \"\"\"
    Finds the minimum-cost multi-modal freight path meeting maximum transit time constraint.
    Uses Constrained Dijkstra with priority-queue branch and dominance pruning.
    \"\"\"
    if origin not in network_graph:
        return {"feasible": False, "message": f"Origin node '{origin}' not found in network."}
    
    if origin == destination:
        return {
            "feasible": True,
            "total_cost_usd": 0.0,
            "total_transit_hours": 0.0,
            "path_nodes": [origin],
            "modes_used": []
        }

    # Min-Heap stores tuples: (cost, time, current_node, path_list, modes_list)
    # Heap orders strictly by lowest cost first
    pq = [(0.0, 0.0, origin, [origin], [])]

    # Best observed arrival time at each node for pruning suboptimal dominated states
    best_time_to_node: dict[str, float] = {}

    while pq:
        cost, time, u, path, modes = heapq.heappop(pq)

        # Reached destination: Since priority queue pops by minimum cost, this is guaranteed optimal
        if u == destination:
            return {
                "feasible": True,
                "total_cost_usd": round(cost, 2),
                "total_transit_hours": round(time, 2),
                "path_nodes": path,
                "modes_used": modes
            }

        # Dominance check: If we previously reached node 'u' with strictly lower or equal time at lower cost, prune
        if u in best_time_to_node and best_time_to_node[u] <= time:
            continue
        best_time_to_node[u] = time

        # Explore outgoing connections
        for edge in network_graph.get(u, []):
            v = edge['to_node']
            edge_cost = edge['cost_usd']
            edge_time = edge['transit_hours']
            edge_mode = edge['mode']

            new_cost = cost + edge_cost
            new_time = time + edge_time

            # Prune paths that violate maximum allowable transit SLA
            if new_time > max_transit_hours:
                continue

            # Cycle prevention: avoid revisiting nodes already in current path
            if v in path:
                continue

            heapq.heappush(pq, (new_cost, new_time, v, path + [v], modes + [edge_mode]))

    return {
        "feasible": False,
        "message": f"No feasible route exists from '{origin}' to '{destination}' within {max_transit_hours} hours."
    }""",
        "complexity": """- **Time Complexity**: `O((V + E) log V)` in standard cases, expanding up to `O(B × E log V)` in worst-case constrained path searches where `B` is the number of non-dominated Pareto paths. Dominance pruning keeps average execution under a few milliseconds.
- **Space Complexity**: `O(V + E)` to maintain the network graph adjacency list and priority queue search frontiers."""
    },
    {
        "id": 12,
        "type": "Python",
        "title": "Automated Freight Rate Benchmarking & Outlier Trimming (IQR & MAD)",
        "statement": """### Problem Statement: Automated Freight Rate Benchmarking & Outlier Trimming (IQR & MAD)

Walmart procurement managers analyze spot and contracted freight invoices across hundreds of corridors. Before calculating the baseline fair-market contract rate ($/mile) for the annual carrier RFP, raw transaction data must be cleansed. The raw data frequently contains data-entry typos (e.g., $25,000 instead of $2,500), erroneous accessorial charges, or canceled dummy bookings.

**Requirements**:
Implement a Python function `cleanse_freight_rates(rates: list[float], method: str = 'MAD', threshold: float = 3.0) -> dict`:
1. Support two robust statistical outlier filtering techniques:
   - **`'IQR'` (Interquartile Range)**:
     - Compute `Q1` (25th percentile), `Q3` (75th percentile), and `IQR = Q3 - Q1`.
     - Lower bound = `Q1 - (1.5 * IQR)`.
     - Upper bound = `Q3 + (1.5 * IQR)`.
   - **`'MAD'` (Median Absolute Deviation - more robust against high-leverage outliers)**:
     - Compute median `M = median(rates)`.
     - Compute `MAD = median(|x_i - M|)`.
     - Modified Z-Score: `M_i = 0.6745 * |x_i - M| / MAD`.
     - Flag as outlier if `M_i > threshold`.
2. Compute descriptive metrics on both the **raw** and **cleansed** datasets:
   - `mean_rate`, `median_rate`, `std_rate`, `outlier_count`, `outliers_detected`.
3. Handle edge cases gracefully: empty lists, lists with zero variance (all identical rates), and invalid method strings.""",
        "thought_process": """### Complete Thought Process:

1. **Why Median Absolute Deviation (MAD) Over Standard Deviation**:
   - Sample mean and standard deviation are notoriously vulnerable to extreme outliers. A single $50,000 invoice typo distorts the mean and artificially inflates the standard deviation, masking other true anomalies.
   - MAD has a breakdown point of 50%, meaning half the data can be contaminated before the statistic breaks down. The constant `0.6745` normalizes MAD to match standard deviation for a Gaussian distribution.

2. **Interquartile Range (IQR)**:
   - Standard Tukey fence method: `[Q1 - 1.5 * IQR, Q3 + 1.5 * IQR]`.
   - Percentiles computed cleanly via Python `statistics.quantiles(rates, n=4)`.

3. **Handling Zero-Variance & Edge Cases**:
   - If all rates are identical, `IQR == 0.0` and `MAD == 0.0`. In this scenario, no points are outliers. We must check `if mad == 0.0:` or `if iqr == 0.0:` to prevent division by zero.
   - For `len(rates) < 4`, return the raw dataset without filtering (insufficient statistical support).""",
        "code": """import statistics
from typing import Any

def cleanse_freight_rates(
    rates: list[float], 
    method: str = 'MAD', 
    threshold: float = 3.0
) -> dict[str, Any]:
    \"\"\"
    Cleanses transportation freight transaction rates using IQR or Median Absolute Deviation (MAD).
    Returns comparative statistical metrics before and after outlier removal.
    \"\"\"
    if not rates:
        return {"error": "Empty rates list provided."}

    n = len(rates)
    if n < 4:
        return {
            "message": "Sample size too small for robust outlier trimming (n < 4).",
            "clean_rates": rates,
            "raw_mean": round(statistics.mean(rates), 2)
        }

    raw_mean = statistics.mean(rates)
    raw_median = statistics.median(rates)
    raw_std = statistics.stdev(rates) if n > 1 else 0.0

    clean_rates: list[float] = []
    outliers: list[float] = []

    if method.upper() == 'IQR':
        # Calculate Q1 and Q3 using 4 equal quantiles
        q1, median_val, q3 = statistics.quantiles(rates, n=4)
        iqr = q3 - q1

        if iqr == 0.0:
            clean_rates = list(rates)
        else:
            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)
            for r in rates:
                if lower_bound <= r <= upper_bound:
                    clean_rates.append(r)
                else:
                    outliers.append(r)

    elif method.upper() == 'MAD':
        med = statistics.median(rates)
        abs_deviations = [abs(x - med) for x in rates]
        mad = statistics.median(abs_deviations)

        if mad == 0.0:
            # If MAD is zero, points differing from median are evaluated against mean absolute deviation
            clean_rates = list(rates)
        else:
            for r in rates:
                # Modified Z-score using Boris Iglewicz and David Hoaglin standard
                mod_z = 0.6745 * abs(r - med) / mad
                if mod_z <= threshold:
                    clean_rates.append(r)
                else:
                    outliers.append(r)
    else:
        raise ValueError(f"Unknown outlier cleansing method: '{method}'. Choose 'IQR' or 'MAD'.")

    # Post-cleansing metrics
    clean_mean = statistics.mean(clean_rates) if clean_rates else 0.0
    clean_median = statistics.median(clean_rates) if clean_rates else 0.0
    clean_std = statistics.stdev(clean_rates) if len(clean_rates) > 1 else 0.0

    return {
        "method_applied": method.upper(),
        "total_raw_records": n,
        "outliers_removed_count": len(outliers),
        "outliers_detected": outliers,
        "raw_metrics": {
            "mean": round(raw_mean, 2),
            "median": round(raw_median, 2),
            "std": round(raw_std, 2)
        },
        "clean_metrics": {
            "mean": round(clean_mean, 2),
            "median": round(clean_median, 2),
            "std": round(clean_std, 2)
        },
        "variance_reduction_pct": round((1.0 - (clean_std / raw_std)) * 100.0, 2) if raw_std > 0 else 0.0
    }""",
        "complexity": """- **Time Complexity**: `O(N log N)` where `N` is the number of rates, governed by median/quantile sorting operations.
- **Space Complexity**: `O(N)` auxiliary memory to hold the sorted quantile arrays and filtered lists."""
    },
    {
        "id": 13,
        "type": "Python",
        "title": "Population Stability Index (PSI) Drift Calculation for Inbound Demand Forecast Models",
        "statement": """### Problem Statement: Population Stability Index (PSI) Drift Calculation for Inbound Demand Forecast Models

Walmart utilizes machine learning models to forecast inbound trailer volume arriving at Regional Distribution Centers. Over time, macro-economic shifts, supplier network re-alignments, and holiday seasonality cause the distribution of inbound trailer volumes to shift (**feature drift**).

Data analysts must monitor model stability by computing the **Population Stability Index (PSI)** between the baseline training distribution (`expected`) and the current month's production inference distribution (`actual`).

**PSI Formula**:
`PSI = sum((Actual_pct_i - Expected_pct_i) * ln(Actual_pct_i / Expected_pct_i))` across all `K` quantile bins.

**Industry Standard Interpretation**:
- `PSI < 0.10`: No significant distribution change; model is stable.
- `0.10 <= PSI < 0.25`: Moderate drift; investigate features and retrain soon.
- `PSI >= 0.25`: Severe distribution shift; model forecast is degraded, retrain immediately.

**Requirements**:
Implement a Python function `calculate_psi(expected_vals: list[float], actual_vals: list[float], num_bins: int = 10) -> dict`:
1. Use the `expected` dataset to define `num_bins` equal-frequency bin boundaries (quantiles).
2. Bin both `expected` and `actual` data into these fixed boundaries.
3. Apply Laplace epsilon smoothing (`epsilon = 1e-4`) to prevent zero division or log of zero if an actual bucket has zero occurrences.
4. Calculate per-bucket drift contributions and total PSI score.
5. Return the PSI score, drift classification status, and bucket-by-bucket breakdown.""",
        "thought_process": """### Complete Thought Process:

1. **Defining Bin Cutoffs from Baseline (Expected)**:
   - To compute PSI properly, bin edges must be established strictly from the `expected` (training) population so that each expected bucket contains roughly `10%` of the data (for 10 bins).
   - In Python, compute quantile breakpoints: `cutoffs = [min] + [quantiles(expected, n=num_bins)] + [max]`.

2. **Bucket Counting**:
   - For each bucket `[lower, upper]`, count how many values fall into it for both `expected` and `actual`.
   - Ensure the first bucket is left-closed and right-closed: `lower <= x <= upper`.
   - Upper buckets are left-open and right-closed: `lower < x <= upper`.

3. **Percentage Normalization & Epsilon Smoothing**:
   - `expected_pct = (count_expected + eps) / (total_expected + num_bins * eps)`
   - `actual_pct = (count_actual + eps) / (total_actual + num_bins * eps)`
   - `bucket_psi = (actual_pct - expected_pct) * math.log(actual_pct / expected_pct)`

4. **Summation & Status Assignment**:
   - Sum `bucket_psi` across all bins.
   - Categorize based on standard thresholds (`< 0.10`, `0.10 - 0.25`, `>= 0.25`).""",
        "code": """import math
import statistics
from typing import Any

def calculate_psi(
    expected_vals: list[float], 
    actual_vals: list[float], 
    num_bins: int = 10
) -> dict[str, Any]:
    \"\"\"
    Calculates Population Stability Index (PSI) between baseline and production distributions.
    Bins are defined using expected dataset quantiles with Laplace smoothing.
    \"\"\"
    if not expected_vals or not actual_vals:
        return {"error": "Both expected and actual datasets must be non-empty."}

    # Generate quantile breakpoints from expected baseline
    # statistics.quantiles generates num_bins - 1 cut points
    quantiles = statistics.quantiles(expected_vals, n=num_bins)
    
    # Establish full bin intervals [-inf, q1, q2, ..., q9, +inf]
    bin_edges = [-float('inf')] + quantiles + [float('inf')]

    n_exp = len(expected_vals)
    n_act = len(actual_vals)
    eps = 1e-4  # Epsilon smoothing to prevent log(0) or division by zero

    total_psi = 0.0
    bucket_breakdown = []

    for i in range(num_bins):
        lower = bin_edges[i]
        upper = bin_edges[i + 1]

        # Count occurrences in bucket
        if i == 0:
            count_exp = sum(1 for x in expected_vals if x <= upper)
            count_act = sum(1 for x in actual_vals if x <= upper)
        elif i == num_bins - 1:
            count_exp = sum(1 for x in expected_vals if x > lower)
            count_act = sum(1 for x in actual_vals if x > lower)
        else:
            count_exp = sum(1 for x in expected_vals if lower < x <= upper)
            count_act = sum(1 for x in actual_vals if lower < x <= upper)

        # Smooth percentage calculation
        pct_exp = (count_exp + eps) / (n_exp + (num_bins * eps))
        pct_act = (count_act + eps) / (n_act + (num_bins * eps))

        # Bucket PSI contribution
        bucket_psi = (pct_act - pct_exp) * math.log(pct_act / pct_exp)
        total_psi += bucket_psi

        bucket_breakdown.append({
            "bucket_index": i + 1,
            "lower_edge": round(lower, 2) if lower != -float('inf') else "-INF",
            "upper_edge": round(upper, 2) if upper != float('inf') else "+INF",
            "expected_count": count_exp,
            "actual_count": count_act,
            "expected_pct": round(pct_exp * 100.0, 2),
            "actual_pct": round(pct_act * 100.0, 2),
            "bucket_psi": round(bucket_psi, 4)
        })

    total_psi = round(total_psi, 4)

    # Classify drift severity
    if total_psi < 0.10:
        drift_status = "STABLE: No significant distribution change"
        action_required = "None. Continue normal automated inference."
    elif total_psi < 0.25:
        drift_status = "MODERATE_DRIFT: Observable distribution shift"
        action_required = "Flag for review. Monitor downstream forecast accuracy."
    else:
        drift_status = "SIGNIFICANT_DRIFT: Severe feature drift detected"
        action_required = "Trigger model retraining pipeline immediately."

    return {
        "psi_score": total_psi,
        "drift_classification": drift_status,
        "action_required": action_required,
        "bucket_breakdown": bucket_breakdown
    }""",
        "complexity": """- **Time Complexity**: `O(E log E + B × (E + A))` where `E` is length of expected array, `A` is length of actual array, and `B` is `num_bins`. Quantiles take `O(E log E)`. Counting takes linear passes across both datasets.
- **Space Complexity**: `O(B)` auxiliary memory to store bin edges and per-bucket output results."""
    },
    {
        "id": 14,
        "type": "Python",
        "title": "Merge Overlapping Trailer Unloading Windows & Dock Door Conflict Resolution",
        "statement": """### Problem Statement: Merge Overlapping Trailer Unloading Windows & Dock Door Conflict Resolution

At an inbound Regional Distribution Center, carrier trailers book dock appointment time intervals `[start_time, end_time]` (represented in integer minutes from midnight). 

Due to early arrivals and unannounced carrier delays, appointments frequently overlap on the same dock door or across shared receiving areas. 

**Requirements**:
Implement a Python function `resolve_dock_appointments(intervals: list[tuple[int, int]]) -> dict`:
1. **Part A (Merge Overlapping Sessions)**:
   - Given a list of appointment intervals `(start_time, end_time)`, merge all overlapping or touching intervals into consolidated continuous dock occupancy blocks (analogous to LeetCode 56).
2. **Part B (Peak Concurrent Trailer Demand)**:
   - Find the maximum number of trailers actively unloading simultaneously at any single minute across the day (analogous to LeetCode 253 / Sweep-Line algorithm).
   - Find the exact time window `[peak_start, peak_end]` where this maximum concurrency occurred.
3. Return:
   - `merged_occupancy_blocks`: list of merged `[start, end]` intervals.
   - `total_occupied_minutes`: total minutes during which at least one trailer was unloading.
   - `max_concurrent_trailers`: peak concurrency integer.
   - `peak_time_window`: tuple of `(start, end)` representing the peak concurrency period.""",
        "thought_process": """### Complete Thought Process:

1. **Part A: Interval Merging (LeetCode 56 Variant)**:
   - Sort intervals ascending by start time.
   - Maintain a list `merged`.
   - For each interval `[start, end]`:
     - If `merged` is empty or `start > merged[-1][1]`, append `[start, end]`.
     - Else (they overlap or touch, `start <= merged[-1][1]`), extend the current interval: `merged[-1][1] = max(merged[-1][1], end)`.

2. **Part B: Peak Concurrency via Sweep-Line**:
   - For each interval `(start, end)`, create two chronological boundary events:
     - `(start, +1)`
     - `(end, -1)`
   - Sort events by `time ASC, delta ASC` (departures before arrivals if dock door immediately frees up, or arrivals before departures if handover overlap occurs; typically in trailer docking, departure at minute 60 allows another to start at minute 60, so `-1` before `+1`).
   - Iterate through events tracking `current_active`. If `current_active > max_active`, update `max_active` and track peak intervals.

3. **Total Occupied Minutes**:
   - Sum `(end - start)` across all intervals in `merged_occupancy_blocks`.""",
        "code": """from typing import Any

def resolve_dock_appointments(intervals: list[tuple[int, int]]) -> dict[str, Any]:
    \"\"\"
    Merges overlapping trailer dock appointments and calculates peak concurrent trailer demand.
    Times are represented as integer minutes from midnight (0 to 1440).
    \"\"\"
    if not intervals:
        return {
            "merged_occupancy_blocks": [],
            "total_occupied_minutes": 0,
            "max_concurrent_trailers": 0,
            "peak_time_window": None
        }

    # ==========================================
    # PART A: Merge Overlapping Intervals
    # ==========================================
    # Sort intervals by start time ascending
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged: list[list[int]] = []

    for start, end in sorted_intervals:
        if not merged or start > merged[-1][1]:
            # Disjoint interval: start a new occupancy block
            merged.append([start, end])
        else:
            # Overlapping or contiguous interval: extend previous end time
            merged[-1][1] = max(merged[-1][1], end)

    total_occupied_minutes = sum(block[1] - block[0] for block in merged)

    # ==========================================
    # PART B: Peak Concurrency Sweep-Line
    # ==========================================
    # Create start (+1) and end (-1) point events
    # If end touches start (e.g., [10, 20] and [20, 30]), departure (-1) precedes arrival (+1)
    events: list[tuple[int, int]] = []
    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))

    # Sort primarily by time ASC, secondarily by delta ASC (-1 before +1)
    events.sort(key=lambda x: (x[0], x[1]))

    max_concurrent = 0
    current_concurrent = 0
    peak_start = None
    peak_end = None

    for time, delta in events:
        current_concurrent += delta
        if current_concurrent > max_concurrent:
            max_concurrent = current_concurrent
            peak_start = time
            peak_end = None  # Will be locked when concurrency drops below peak
        elif current_concurrent < max_concurrent and peak_end is None and peak_start is not None:
            peak_end = time

    return {
        "merged_occupancy_blocks": [tuple(block) for block in merged],
        "total_occupied_minutes": total_occupied_minutes,
        "max_concurrent_trailers": max_concurrent,
        "peak_time_window": (peak_start, peak_end) if peak_start is not None else None
    }""",
        "complexity": """- **Time Complexity**: `O(N log N)` where `N` is the number of appointment intervals. The runtime is dominated by sorting the intervals and sweep-line event points.
- **Space Complexity**: `O(N)` auxiliary memory to store the merged interval list and event points."""
    },
    {
        "id": 15,
        "type": "Python",
        "title": "Inbound Less-Than-Truckload (LTL) Consolidation into Full Truckloads (Bin Packing)",
        "statement": """### Problem Statement: Inbound Less-Than-Truckload (LTL) Consolidation into Full Truckloads (Bin Packing)

Suppliers with small order volumes dispatch **Less-Than-Truckload (LTL)** shipments. LTL freight is extremely expensive on a per-hundredweight ($/CWT) basis compared to **Full Truckload (FTL)** freight. Walmart routes regional LTL orders to regional consolidation centers (RCCs) where cross-dock planners consolidate them into multi-stop full truckloads.

Each FTL trailer has two hard constraints:
- **Max Weight Capacity**: `42,000 lbs`
- **Max Pallet Capacity**: `26 pallets`

**Requirements**:
Implement a Python function `consolidate_ltl_shipments(shipments: list[dict], method: str = 'BFD') -> dict`:
1. Each shipment has `shipment_id`, `vendor_id`, `weight_lbs`, and `pallets`.
2. Implement **Best-Fit Decreasing (BFD)**:
   - Sort shipments descending by a normalized density score: `weight / 42000 + pallets / 26`.
   - For each shipment, place it into the existing open trailer that has the **tightest remaining capacity** (minimizes remaining unused volume/weight) without exceeding either constraint.
   - If no open trailer can accommodate the shipment, open a new trailer.
3. Compare against financial baseline:
   - Standalone LTL freight cost: `$150 base + $0.18 per lb + $45 per pallet`.
   - Consolidated FTL trailer cost: Flat `$2,400 per trailer dispatched`.
4. Return:
   - `trailers_dispatched_count`
   - `total_ftl_cost_usd`
   - `standalone_ltl_baseline_cost_usd`
   - `net_consolidation_savings_usd`
   - `savings_pct`
   - `trailer_manifest`: list of trailer assignments with loaded shipments and utilization percentages.""",
        "thought_process": """### Complete Thought Process:

1. **Best-Fit Decreasing (BFD) Algorithm**:
   - In FFD, we pick the *first* trailer that fits.
   - In BFD, we inspect *all* open trailers that can fit the item, and select the one that leaves the *minimum residual capacity*. This tightly packs trailers and prevents fragmentation.
   - Residual capacity metric: `rem_wt = MAX_WT - (curr_wt + item_wt)` and `rem_pallets = MAX_PALLETS - (curr_pallets + item_pallets)`.
   - Combined residual score: `(rem_wt / MAX_WT) + (rem_pallets / MAX_PALLETS)`. Pick the trailer that minimizes this residual score.

2. **Financial Cost Modeling**:
   - For each LTL shipment: `cost = 150.0 + (0.18 * wt) + (45.0 * pallets)`.
   - Total standalone LTL cost = sum of individual shipment costs.
   - Total FTL cost = `num_trailers * 2400.0`.
   - Net Savings = `Total LTL - Total FTL`.

3. **Validation & Edge Cases**:
   - Individual shipment exceeding 42,000 lbs or 26 pallets cannot fit into any standard FTL trailer and raises a `ValueError`.""",
        "code": """from typing import Any

MAX_WEIGHT_FTL = 42000.0
MAX_PALLETS_FTL = 26

def calculate_standalone_ltl_cost(weight: float, pallets: int) -> float:
    \"\"\"Calculates baseline tariff cost if shipped standalone via commercial LTL.\"\"\"
    return 150.0 + (0.18 * weight) + (45.0 * pallets)

def consolidate_ltl_shipments(shipments: list[dict[str, Any]], method: str = 'BFD') -> dict[str, Any]:
    \"\"\"
    Consolidates small vendor LTL shipments into Full Truckloads (FTL) using Best-Fit Decreasing.
    Quantifies net transportation procurement savings against commercial LTL tariffs.
    \"\"\"
    if not shipments:
        return {"error": "No shipments provided."}

    # Validate items and compute standalone LTL cost
    standalone_ltl_total = 0.0
    for s in shipments:
        if s['weight_lbs'] > MAX_WEIGHT_FTL or s['pallets'] > MAX_PALLETS_FTL:
            raise ValueError(f"Shipment {s['shipment_id']} exceeds standard FTL limits.")
        standalone_ltl_total += calculate_standalone_ltl_cost(s['weight_lbs'], s['pallets'])

    # Sort descending by normalized capacity consumption
    sorted_shipments = sorted(
        shipments, 
        key=lambda x: (x['weight_lbs'] / MAX_WEIGHT_FTL) + (x['pallets'] / MAX_PALLETS_FTL), 
        reverse=True
    )

    trailers: list[dict[str, Any]] = []

    for item in sorted_shipments:
        item_wt = item['weight_lbs']
        item_pallets = item['pallets']
        
        best_trailer_idx = -1
        min_residual_score = float('inf')

        # Best-Fit: Find open trailer that fits item with minimum leftover slack
        for idx, t in enumerate(trailers):
            if (t['loaded_weight'] + item_wt <= MAX_WEIGHT_FTL and 
                t['loaded_pallets'] + item_pallets <= MAX_PALLETS_FTL):
                
                rem_wt = MAX_WEIGHT_FTL - (t['loaded_weight'] + item_wt)
                rem_pal = MAX_PALLETS_FTL - (t['loaded_pallets'] + item_pallets)
                residual_score = (rem_wt / MAX_WEIGHT_FTL) + (rem_pal / MAX_PALLETS_FTL)

                if residual_score < min_residual_score:
                    min_residual_score = residual_score
                    best_trailer_idx = idx

        if best_trailer_idx != -1:
            # Place in best fitting trailer
            t = trailers[best_trailer_idx]
            t['shipment_ids'].append(item['shipment_id'])
            t['loaded_weight'] += item_wt
            t['loaded_pallets'] += item_pallets
        else:
            # Open new FTL trailer
            new_trailer = {
                "trailer_id": f"FTL-TR-{len(trailers) + 1:03d}",
                "shipment_ids": [item['shipment_id']],
                "loaded_weight": item_wt,
                "loaded_pallets": item_pallets
            }
            trailers.append(new_trailer)

    # Post-process trailers
    for t in trailers:
        t['weight_util_pct'] = round((t['loaded_weight'] / MAX_WEIGHT_FTL) * 100.0, 2)
        t['pallet_util_pct'] = round((t['loaded_pallets'] / MAX_PALLETS_FTL) * 100.0, 2)

    total_ftl_cost = len(trailers) * 2400.0
    net_savings = standalone_ltl_total - total_ftl_cost
    savings_pct = (net_savings / standalone_ltl_total) * 100.0 if standalone_ltl_total > 0 else 0.0

    return {
        "trailers_dispatched_count": len(trailers),
        "total_ftl_cost_usd": round(total_ftl_cost, 2),
        "standalone_ltl_baseline_cost_usd": round(standalone_ltl_total, 2),
        "net_consolidation_savings_usd": round(net_savings, 2),
        "savings_pct": round(savings_pct, 2),
        "trailer_manifest": trailers
    }""",
        "complexity": """- **Time Complexity**: `O(N log N + N × K)` where `N` is the number of LTL shipments and `K` is the number of FTL trailers instantiated. In the worst case, each shipment evaluates all open trailers to find the minimum residual score.
- **Space Complexity**: `O(N)` memory required to store the sorted shipments and consolidated trailer manifest."""
    },
    {
        "id": 16,
        "type": "Python",
        "title": "Top K Most Volatile Transportation Lanes by Freight Variance (Min-Heap)",
        "statement": """### Problem Statement: Top K Most Volatile Transportation Lanes by Freight Variance (Min-Heap)

Walmart manages thousands of active inbound freight corridors. Transportation planners need to track the **Top K most volatile lanes** in real-time based on the variance of carrier transit lead times. Because the streaming telemetry processes millions of events per hour, storing all historical lead times in memory is infeasible.

**Requirements**:
Implement a Python class `StreamingTopKVolatileLanes`:
1. Initialized with `k: int` (e.g., `k = 10`) and `min_shipments: int` (minimum completed shipments required before a lane is eligible, e.g., `min_shipments = 20`).
2. Method `add_shipment(lane_id: str, transit_hours: float) -> None`:
   - Uses **Welford's algorithm** to maintain running count, mean, and sample variance of transit hours in strict `O(1)` time and `O(1)` memory per lane.
3. Method `get_top_k_volatile_lanes() -> list[dict]`:
   - Uses a **min-heap of size K** to extract the Top K lanes with the highest transit lead time variance.
   - Runs in `O(L log K)` time where `L` is the number of unique lanes, avoiding a full `O(L log L)` sort.
   - Returns a list of dictionaries ordered by variance descending:
     ```python
     [
         {
             "lane_id": "Atlanta -> Bentonville",
             "shipments_count": 84,
             "mean_transit_hours": 24.2,
             "variance_hours2": 38.6,
             "std_dev_hours": 6.21
         },
         ...
     ]
     ```""",
        "thought_process": """### Complete Thought Process:

1. **Welford's Algorithm for Single-Pass Variance**:
   - To compute sample variance `s^2` without storing raw observations:
     - For each incoming value `x`:
       - `count += 1`
       - `delta = x - mean`
       - `mean += delta / count`
       - `delta2 = x - mean`
       - `M2 += delta * delta2`
     - Sample Variance: `s^2 = M2 / (count - 1)` (for `count >= 2`).
   - This provides numerically stable variance with zero catastrophic cancellation and strict `O(1)` memory.

2. **Extracting Top K via Min-Heap**:
   - If we have `L` total lanes, sorting all lanes takes `O(L log L)`.
   - By pushing elements into a min-heap of maximum size `K`:
     - Maintain heap elements as `(variance, lane_id)`.
     - For each eligible lane (`count >= min_shipments`):
       - If heap size `< K`: `heappush(heap, (variance, lane_id))`
       - Else if `variance > heap[0][0]`: `heappushpop(heap, (variance, lane_id))`
   - Heap extraction takes `O(L log K)`. For `L = 50,000` and `K = 10`, `50,000 * log(10) ≈ 166,000` operations vs `50,000 * log(50,000) ≈ 780,000` operations.

3. **Final Formatting**:
   - Extract from heap and sort the K items descending to present the highest variance at the top.""",
        "code": """import heapq
import math
from typing import Any

class StreamingTopKVolatileLanes:
    \"\"\"
    Tracks the Top K most volatile transportation lanes by transit lead time variance.
    Maintains online running variance using Welford's algorithm (O(1) memory per lane).
    Uses a min-heap of size K for O(L log K) top-k retrieval.
    \"\"\"
    def __init__(self, k: int = 10, min_shipments: int = 20):
        self.k = k
        self.min_shipments = min_shipments
        # Dictionary storing lane stats: {lane_id: {'count': n, 'mean': m, 'M2': M2}}
        self.lane_stats: dict[str, dict[str, float]] = {}

    def add_shipment(self, lane_id: str, transit_hours: float) -> None:
        \"\"\"Updates running mean and M2 using Welford's algorithm in O(1) time.\"\"\"
        if lane_id not in self.lane_stats:
            self.lane_stats[lane_id] = {'count': 1.0, 'mean': transit_hours, 'M2': 0.0}
            return

        stats = self.lane_stats[lane_id]
        stats['count'] += 1.0
        n = stats['count']
        
        delta = transit_hours - stats['mean']
        stats['mean'] += delta / n
        delta2 = transit_hours - stats['mean']
        stats['M2'] += delta * delta2

    def get_top_k_volatile_lanes(self) -> list[dict[str, Any]]:
        \"\"\"
        Returns Top K lanes by sample variance using a bounded min-heap of size K.
        Complexity: O(L log K).
        \"\"\"
        # Min-heap holds tuples: (variance, lane_id)
        heap: list[tuple[float, str]] = []

        for lane_id, stats in self.lane_stats.items():
            count = int(stats['count'])
            if count < self.min_shipments:
                continue

            # Sample variance: M2 / (n - 1)
            variance = stats['M2'] / (count - 1) if count > 1 else 0.0

            if len(heap) < self.k:
                heapq.heappush(heap, (variance, lane_id))
            else:
                if variance > heap[0][0]:
                    heapq.heappushpop(heap, (variance, lane_id))

        # Extract items from heap and sort descending by variance
        result = []
        for var, lane_id in sorted(heap, key=lambda x: x[0], reverse=True):
            stats = self.lane_stats[lane_id]
            std_dev = math.sqrt(max(0.0, var))
            result.append({
                "lane_id": lane_id,
                "shipments_count": int(stats['count']),
                "mean_transit_hours": round(stats['mean'], 2),
                "variance_hours2": round(var, 2),
                "std_dev_hours": round(std_dev, 2)
            })

        return result""",
        "complexity": """- **Time Complexity**:
  - `add_shipment`: `O(1)` constant time.
  - `get_top_k_volatile_lanes`: `O(L log K)` where `L` is the number of distinct lanes and `K` is the number of top items requested.
- **Space Complexity**: `O(L)` memory to store running accumulator dictionaries for each unique transportation lane."""
    },
    {
        "id": 17,
        "type": "Python",
        "title": "Cycle Detection & Bottleneck Search in Cross-Dock Conveyor Network",
        "statement": """### Problem Statement: Cycle Detection & Bottleneck Search in Cross-Dock Conveyor Network

High-velocity automated cross-dock facilities use conveyor systems to transfer incoming vendor cartons from inbound unloading docks to outbound shipping doors. Conveyor transfer intersections are modeled as a **Directed Graph**:
- Nodes represent conveyor diverters, scan tunnels, and transfer spurs.
- Directed edges represent physical motorized roller conveyors moving freight in one direction.

If a maintenance routing reconfiguration accidentally introduces a **circular dependency (cycle)**, cartons circulate endlessly, creating physical conveyor jams and stopping the entire inbound sortation system.

**Requirements**:
Implement a Python function `audit_conveyor_network(adj_list: dict[str, list[str]]) -> dict`:
1. Use **Kahn's Algorithm (BFS with In-Degree Tracking)** to detect whether the conveyor network contains a deadlock cycle.
2. If the graph is a Directed Acyclic Graph (**DAG**):
   - Return `has_cycle: False`.
   - Return `topological_order`: A valid linear sequence of conveyor segments from inbound intake to outbound spurs.
3. If the graph contains a cycle:
   - Return `has_cycle: True`.
   - Return `deadlock_cycle_nodes`: The specific list of nodes trapped within circular dependencies.
4. Compute the **Critical Path Bottleneck**: Find the longest directed path length (number of conveyor hops) in the DAG representing the maximum latency route.""",
        "thought_process": """### Complete Thought Process:

1. **Cycle Detection via Kahn's Algorithm**:
   - Compute in-degree (number of incoming edges) for every node in the graph.
   - Initialize a queue with all nodes having `in_degree == 0` (inbound entry points).
   - While the queue is non-empty:
     - Dequeue node `u`, append to `topological_order`.
     - For each neighbor `v` of `u`:
       - `in_degree[v] -= 1`
       - If `in_degree[v] == 0`: enqueue `v`.
   - If `len(topological_order) == total_nodes`: Graph is an acyclic DAG.
   - Else: Nodes whose `in_degree > 0` are trapped in one or more circular deadlock cycles.

2. **Critical Path Bottleneck (Longest Path in DAG)**:
   - In a general graph, finding the longest simple path is NP-hard. But in a DAG, longest path can be solved in linear `O(V + E)` time using dynamic programming along the topological sort order.
   - `dist[v] = max(dist[v], dist[u] + 1)`.
   - Max value in `dist` represents the critical path bottleneck length.""",
        "code": """import collections
from typing import Any

def audit_conveyor_network(adj_list: dict[str, list[str]]) -> dict[str, Any]:
    \"\"\"
    Audits an automated cross-dock conveyor network for circular deadlock dependencies.
    Uses Kahn's algorithm for cycle detection and computes critical path conveyor latency.
    \"\"\"
    # Gather all unique nodes across keys and values
    all_nodes: set[str] = set(adj_list.keys())
    for neighbors in adj_list.values():
        all_nodes.update(neighbors)

    total_nodes = len(all_nodes)
    in_degree: dict[str, int] = {node: 0 for node in all_nodes}

    # Compute in-degrees
    for u in adj_list:
        for v in adj_list[u]:
            in_degree[v] += 1

    # Queue of source nodes (in_degree == 0)
    queue = collections.deque([node for node in all_nodes if in_degree[node] == 0])
    topological_order: list[str] = []

    while queue:
        u = queue.popleft()
        topological_order.append(u)

        for v in adj_list.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    # If all nodes processed, graph is a DAG (no cycle)
    if len(topological_order) == total_nodes:
        # Compute critical path length (longest directed path in DAG) using dynamic programming
        dist: dict[str, int] = {node: 0 for node in all_nodes}
        for u in topological_order:
            for v in adj_list.get(u, []):
                if dist[u] + 1 > dist[v]:
                    dist[v] = dist[u] + 1

        max_hops = max(dist.values()) if dist else 0

        return {
            "has_cycle": False,
            "status": "OPERATIONAL: Directed Acyclic Graph (No deadlock)",
            "topological_order": topological_order,
            "deadlock_cycle_nodes": [],
            "critical_path_max_hops": max_hops
        }
    else:
        # Nodes remaining with in_degree > 0 participate in or depend on cycles
        cycle_nodes = [node for node, deg in in_degree.items() if deg > 0]
        return {
            "has_cycle": True,
            "status": "CRITICAL_ERROR: Circular deadlock dependency detected in conveyor layout",
            "topological_order": [],
            "deadlock_cycle_nodes": sorted(cycle_nodes),
            "critical_path_max_hops": None
        }""",
        "complexity": """- **Time Complexity**: `O(V + E)` where `V` is the number of conveyor segments and `E` is the number of conveyor connections. Kahn's algorithm and DAG longest-path DP both operate in linear time.
- **Space Complexity**: `O(V + E)` memory required to store the adjacency list, in-degree lookup tables, and topological order queue."""
    },
    {
        "id": 18,
        "type": "Python",
        "title": "Minimum Number of Yard Spotter Trucks / Hostlers Required (Interval Scheduling)",
        "statement": """### Problem Statement: Minimum Number of Yard Spotter Trucks / Hostlers Required (Interval Scheduling)

At a Walmart Regional Distribution Center yard, specialized yard spotter trucks (hostlers) move trailers between parking slips and dock doors. 

Each planned trailer move has a scheduled time window:
`move = (start_time, end_time)` represented in integer minutes from the beginning of the shift.

A single yard truck can execute at most one trailer move at a time. If move A finishes at minute `45`, that truck cannot start move B until minute `46` (a move ending at `t` requires a truck until `t`).

**Requirements**:
Implement a Python function `min_hostlers_required(moves: list[tuple[int, int]]) -> dict`:
1. Calculate the minimum number of hostler yard trucks required to complete all trailer moves without delaying any move (analogous to LeetCode 253: Meeting Rooms II).
2. Generate an exact schedule assigning each move to a specific hostler truck ID (`"Hostler-1"`, `"Hostler-2"`, etc.).
3. Return:
   - `min_trucks_required`: Integer.
   - `truck_assignments`: Dictionary mapping truck IDs to their allocated list of moves.
   - `utilization_pct`: Average percentage of shift time each hostler truck was actively executing moves across the total shift span.""",
        "thought_process": """### Complete Thought Process:

1. **Greedy Allocation with Min-Heap (LeetCode 253)**:
   - Sort all moves ascending by `start_time`.
   - Maintain a min-heap storing active trucks: `(truck_end_time, truck_id)`.
   - For each move `(start, end)`:
     - Check the truck that frees up earliest (`heap[0]`).
     - If `heap[0][0] < start`:
       - That truck has finished its previous move and is available!
       - Pop `(earliest_end, truck_id)` from heap.
       - Assign the current move to `truck_id`.
       - Push `(end, truck_id)` back onto the heap.
     - Else:
       - No existing truck is free! We must dispatch a new truck: `new_truck_id = f"Hostler-{len(all_trucks) + 1}"`.
       - Push `(end, new_truck_id)` onto the heap.

2. **Tracking Active Move Minutes & Shift Utilization**:
   - Total active minutes for truck `k` = sum of `(end - start)` for all assigned moves.
   - Shift duration = `max(end) - min(start)`.
   - Utilization = `(total_active_minutes) / (num_trucks * shift_duration) * 100`.""",
        "code": """import heapq
from typing import Any

def min_hostlers_required(moves: list[tuple[int, int]]) -> dict[str, Any]:
    \"\"\"
    Computes minimum yard spotter trucks required to execute trailer yard moves.
    Uses a min-heap to generate optimal greedy hostler truck schedules.
    \"\"\"
    if not moves:
        return {
            "min_trucks_required": 0,
            "truck_assignments": {},
            "overall_hostler_utilization_pct": 0.0
        }

    # Sort moves ascending by start time
    sorted_moves = sorted(moves, key=lambda x: (x[0], x[1]))

    # Min-Heap stores tuples: (end_time, truck_id)
    heap: list[tuple[int, str]] = []
    assignments: dict[str, list[tuple[int, int]]] = {}
    truck_counter = 0

    shift_start = min(m[0] for m in moves)
    shift_end = max(m[1] for m in moves)
    shift_duration = max(1, shift_end - shift_start)

    for start, end in sorted_moves:
        # Check if any currently deployed truck is free before this move begins
        if heap and heap[0][0] < start:
            earliest_end, truck_id = heapq.heappop(heap)
            assignments[truck_id].append((start, end))
            heapq.heappush(heap, (end, truck_id))
        else:
            # Need an additional hostler truck
            truck_counter += 1
            new_truck_id = f"Hostler-{truck_counter:02d}"
            assignments[new_truck_id] = [(start, end)]
            heapq.heappush(heap, (end, new_truck_id))

    total_active_minutes = sum(
        sum(m[1] - m[0] for m in move_list) 
        for move_list in assignments.values()
    )

    total_fleet_capacity_minutes = len(assignments) * shift_duration
    fleet_utilization = (total_active_minutes / total_fleet_capacity_minutes) * 100.0 if total_fleet_capacity_minutes > 0 else 0.0

    return {
        "min_trucks_required": len(assignments),
        "truck_assignments": assignments,
        "overall_hostler_utilization_pct": round(fleet_utilization, 2)
    }""",
        "complexity": """- **Time Complexity**: `O(N log N)` where `N` is the number of trailer yard moves. Sorting the moves takes `O(N log N)`. Pushing and popping from the heap of size `K <= N` takes `O(N log K)`.
- **Space Complexity**: `O(N)` memory required to hold the min-heap and truck assignment dictionary."""
    },
    {
        "id": 19,
        "type": "Python",
        "title": "Binary Search for Optimal Order Delivery Window to Minimize Expedited Freight Cost",
        "statement": """### Problem Statement: Binary Search for Optimal Order Delivery Window to Minimize Expedited Freight Cost

When Walmart issues an emergency replenishment purchase order, transportation planners can contract faster, expedited transit (e.g., team-driver team service or air freight) or slower, standard intermodal rail.

The **Expedited Freight Cost** decreases monotonically as the allowable transit window `W` (in days) increases:
`Freight_Cost(W) = Base_Cost * (1.0 + 3.0 / (W ** 0.8))`

Conversely, widening the delivery window delays store shelf replenishment, causing **Inventory Stockout & Buffer Holding Costs** that increase monotonically with `W`:
`Holding_Cost(W) = Daily_Holding_Penalty * (W ** 1.2)`

**Total Logistics Cost**:
`Total_Cost(W) = Freight_Cost(W) + Holding_Cost(W)`

**Requirements**:
Implement a Python function `optimize_delivery_window(base_cost: float, daily_penalty: float, budget: float, max_days: int = 30) -> dict`:
1. Use **Binary Search on the continuous answer space** (or ternary search for convex minimum) to find:
   - The optimal delivery window `W*` (in days, rounded to 2 decimal places) that **minimizes Total Logistics Cost**.
   - The feasibility check: Determine whether the minimum total cost can be achieved within the procurement `budget`.
2. Return:
   - `optimal_window_days`: float
   - `min_total_cost_usd`: float
   - `freight_cost_usd`: float
   - `holding_cost_usd`: float
   - `is_within_budget`: bool
   - `budget_slack_usd`: float (`budget - min_total_cost_usd`)""",
        "thought_process": """### Complete Thought Process:

1. **Mathematical Properties of Total Cost**:
   - `Freight_Cost(W)` is strictly decreasing convex: as `W` increases, freight cost drops.
   - `Holding_Cost(W)` is strictly increasing convex: as `W` increases, inventory holding risk grows.
   - The sum of two convex functions is strictly convex (unimodal with a single global minimum).

2. **Optimization via Ternary Search or Binary Search on Derivative**:
   - Continuous Ternary Search over interval `[low, high] = [1.0, float(max_days)]`:
     - In each iteration, divide the search interval into three equal parts using two points: `m1 = low + (high - low) / 3` and `m2 = high - (high - low) / 3`.
     - Evaluate `cost(m1)` and `cost(m2)`.
     - If `cost(m1) < cost(m2)`, the global minimum cannot lie in `[m2, high]`; set `high = m2`.
     - Else, the minimum cannot lie in `[low, m1]`; set `low = m1`.
     - Repeat for 60 iterations to achieve sub-millimeter mathematical precision (`(2/3)^60 ≈ 10^-11`).

3. **Budget Validation**:
   - Compare `min_total_cost` against `budget`.""",
        "code": """from typing import Any

def optimize_delivery_window(
    base_cost: float, 
    daily_penalty: float, 
    budget: float, 
    max_days: int = 30
) -> dict[str, Any]:
    \"\"\"
    Finds the optimal transit delivery window (in days) minimizing combined freight and holding cost.
    Uses continuous Ternary Search on the strictly convex cost function.
    \"\"\"
    def total_cost(w: float) -> tuple[float, float, float]:
        freight = base_cost * (1.0 + (3.0 / (w ** 0.8)))
        holding = daily_penalty * (w ** 1.2)
        return (freight + holding, freight, holding)

    # Search boundaries in continuous days [1.0, max_days]
    low = 1.0
    high = float(max_days)

    # 60 iterations of ternary search yields 10^-11 precision
    for _ in range(60):
        m1 = low + (high - low) / 3.0
        m2 = high - (high - low) / 3.0

        cost1, _, _ = total_cost(m1)
        cost2, _, _ = total_cost(m2)

        if cost1 < cost2:
            high = m2
        else:
            low = m1

    optimal_w = (low + high) / 2.0
    min_cost, freight_opt, holding_opt = total_cost(optimal_w)

    is_within_budget = min_cost <= budget
    slack = budget - min_cost

    return {
        "optimal_window_days": round(optimal_w, 2),
        "min_total_cost_usd": round(min_cost, 2),
        "freight_cost_usd": round(freight_opt, 2),
        "holding_cost_usd": round(holding_opt, 2),
        "is_within_budget": is_within_budget,
        "budget_slack_usd": round(slack, 2)
    }""",
        "complexity": """- **Time Complexity**: `O(log((high - low) / epsilon))` which takes a fixed 60 iterations (`~O(1)` constant runtime in microseconds).
- **Space Complexity**: `O(1)` constant auxiliary space."""
    },
    {
        "id": 20,
        "type": "Python",
        "title": "Cosine Similarity & Vector Top-K Retrieval for Agentic Carrier Contract & Exception SLA Search",
        "statement": """### Problem Statement: Cosine Similarity & Vector Top-K Retrieval for Agentic Carrier Contract & Exception SLA Search

Walmart is deploying **Agentic AI workflows** to automate inbound carrier exception handling (e.g., evaluating driver delay notices, force majeure claims, and detention fee disputes). 

When an exception occurs, the AI agent receives an unstructured narrative query (e.g., *"Driver delayed due to Interstate 80 closure following severe blizzard in Wyoming pass"*). The query is converted into an embedding vector. 

To determine contractual liability, the agent must perform semantic vector retrieval across a library of carrier SLA contract clauses to retrieve the **Top K most relevant clauses**.

**Requirements**:
Implement a Python function `retrieve_top_k_clauses(query_embedding: list[float], clause_corpus: list[dict], k: int = 3) -> list[dict]`:
1. Each item in `clause_corpus` is a dictionary:
   ```python
   {
       "clause_id": "SLA-FM-04",
       "carrier_scac": "KNIG",
       "clause_title": "Severe Weather Force Majeure",
       "clause_text": "...",
       "embedding": [0.042, -0.118, 0.285, ...]
   }
   ```
2. Compute **Cosine Similarity** from scratch between the query embedding and each clause embedding:
   `Cosine_Similarity(A, B) = (A . B) / (||A|| * ||B||)`
3. Use a bounded **Min-Heap of size K** to retrieve the Top K clauses with the highest cosine similarity in `O(N log K)` time without sorting the entire corpus.
4. Protect against edge cases: zero vectors (avoid division by zero by setting similarity to 0.0) and dimensionality mismatches.
5. Return the top K clauses with their similarity scores rounded to 4 decimal places.""",
        "thought_process": """### Complete Thought Process:

1. **Cosine Similarity Formula**:
   - `dot_product = sum(a_i * b_i for a_i, b_i in zip(A, B))`
   - `norm_a = sqrt(sum(a_i ** 2))`
   - `norm_b = sqrt(sum(b_i ** 2))`
   - `similarity = dot_product / (norm_a * norm_b)`
   - Guard: If `norm_a < 1e-9` or `norm_b < 1e-9`, return `0.0`.

2. **Top-K Retrieval via Min-Heap**:
   - Instead of computing all scores and sorting (`O(N log N)`), maintain a min-heap of size K:
     - Heap element: `(similarity, clause_dict)`
     - When heap size `< K`: `heappush`
     - When `similarity > heap[0][0]`: `heappushpop`
   - Yields `O(N * D + N log K)` where `D` is the embedding dimension.

3. **Output Sorting**:
   - Sort the extracted K elements descending by similarity score for final response presentation.""",
        "code": """import heapq
import math
from typing import Any

def compute_cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    \"\"\"Computes cosine similarity between two float vectors with zero-norm protection.\"\"\"
    if len(vec_a) != len(vec_b):
        raise ValueError("Embedding dimension mismatch.")

    dot_product = 0.0
    norm_a_sq = 0.0
    norm_b_sq = 0.0

    for a, b in zip(vec_a, vec_b):
        dot_product += a * b
        norm_a_sq += a * a
        norm_b_sq += b * b

    norm_a = math.sqrt(norm_a_sq)
    norm_b = math.sqrt(norm_b_sq)

    if norm_a < 1e-9 or norm_b < 1e-9:
        return 0.0

    return dot_product / (norm_a * norm_b)

def retrieve_top_k_clauses(
    query_embedding: list[float], 
    clause_corpus: list[dict[str, Any]], 
    k: int = 3
) -> list[dict[str, Any]]:
    \"\"\"
    Retrieves Top K most semantically relevant carrier SLA clauses using cosine similarity.
    Maintains a min-heap of size K for optimal O(N log K) retrieval.
    \"\"\"
    if not query_embedding or not clause_corpus:
        return []

    # Min-heap stores tuples: (similarity_score, unique_index, clause_data)
    # unique_index prevents comparison between dictionaries if scores are tied
    heap: list[tuple[float, int, dict[str, Any]]] = []

    for idx, clause in enumerate(clause_corpus):
        similarity = compute_cosine_similarity(query_embedding, clause['embedding'])

        if len(heap) < k:
            heapq.heappush(heap, (similarity, idx, clause))
        else:
            if similarity > heap[0][0]:
                heapq.heappushpop(heap, (similarity, idx, clause))

    # Extract from heap and sort descending
    top_k_results = []
    for score, _, clause in sorted(heap, key=lambda x: x[0], reverse=True):
        result_entry = {
            "clause_id": clause.get("clause_id"),
            "carrier_scac": clause.get("carrier_scac"),
            "clause_title": clause.get("clause_title"),
            "clause_text": clause.get("clause_text"),
            "cosine_similarity": round(score, 4)
        }
        top_k_results.append(result_entry)

    return top_k_results""",
        "complexity": """- **Time Complexity**: `O(N × D + N log K)` where `N` is the number of contract clauses in the corpus, `D` is the embedding vector dimension (e.g., 768 or 1536), and `K` is the number of retrieved clauses. Cosine similarity takes `O(D)`, and heap operations take `O(log K)`.
- **Space Complexity**: `O(K)` auxiliary memory to maintain the min-heap."""
    }
]

print(f"Loaded {len(CODING_PROBLEMS)} coding problems successfully.")
