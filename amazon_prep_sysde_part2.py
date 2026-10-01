# -*- coding: utf-8 -*-
"""
Amazon Advertising in Live Events - AI Engineer Preparation
Part 2B: System Design Questions 11 to 20
All sections written in small, conversational paragraph chunks without ANY bullet points.
Candidate: Ashutosh Rudraksh
"""

from amazon_prep_sysde_part1 import generate_svg

sysde_questions_part2 = [
    # Q11: Real-Time Distributed Telemetry & Anomaly Detection
    {
        "id": 11,
        "title": "Real-Time Distributed Telemetry and Anomaly Detection for Live Sports",
        "category": "Telemetry & Observability",
        "problem_statement": """Design a real-time distributed telemetry, health monitoring, and anomaly detection platform for Prime Video live events advertising. The system must ingest over fifty million metrics per second across global edge CDNs, manifest generators, ad decision servers, and player SDKs, detecting microservice degradations and stream stalls within five seconds of onset.""",
        "clarifying_questions": """When clarifying this design, I would first ask about the resolution and aggregation windows required. Are engineers looking at one-second raw metric histograms during live broadcasts, or is a five-second rolling window sufficient to detect anomalies without triggering false alarms from transient network blips? A five-second rolling aggregation strikes the ideal balance.

Next, I would ask about metric dimensions and cardinality. How many distinct dimensions, such as device type, geographic market, ISP, CDN vendor, and operating system, are tagged on each metric? High cardinality requires specialized time-series storage to avoid memory exhaustion.

I would also clarify the alerting mechanism. Do we use static threshold alarms, or do we need unsupervised machine learning algorithms that learn baseline traffic patterns and dynamically adjust alert thresholds for different times of day and game events? Dynamic baselines are essential because traffic naturally surges during halftimes.

Finally, I would ask about retention policies: we need high-resolution data for the duration of the game, followed by downsampled retention for long-term capacity planning.""",
        "svg_diagram": generate_svg(
            "Live Telemetry & Anomaly Detection Platform",
            [
                ["Global Metric Collectors", "Edge & Player Agents"],
                ["Kafka Message Bus", "High-Throughput Partitioning"],
                ["Flink Stream Aggregator", "5-Second Rolling Windows"],
                ["Isolation Forest ML", "Dynamic Anomaly Detector"],
                ["Live Operations Dashboard", "Automated Alert Dispatch"]
            ]
        ),
        "functional_requirements": """Functionally, the platform must collect real-time telemetry from thousands of microservice instances, edge manifest proxies, and millions of active client video players.

The system must aggregate high-frequency metrics like HTTP error rates, P99 manifest latency, ad playback buffer underruns, and auction timeout counts across customizable dimensional slices.

It must feed aggregated time-series streams into an anomaly detection engine that identifies unexpected departures from historical and contextual baselines.

When a severe metric anomaly is detected, the service must trigger automated alert events, notify broadcast incident channels, and wake automated remediation agents.

It must also power real-time live event operations dashboards with sub-second query rendering speeds, allowing engineers to visualize health metrics across all fifty live broadcast event types simultaneously.""",
        "non_functional_requirements": """On the non-functional side, ingestion throughput is massive, requiring the platform to comfortably absorb fifty million metric points per second during major live sporting events.

End-to-end alert latency must be under five seconds from the moment an issue occurs in production to the moment an alarm fires in the broadcast operations center.

The monitoring system must be strictly decoupled from the live streaming and ad delivery path so that an outage in the telemetry pipeline never affects broadcast playback.

System availability must be at least 99.99 percent, ensuring that operations teams never fly blind during high-stakes live games.""",
        "core_entities": """The primary core entity is the Raw Telemetry Data Point, which includes the metric name, floating-point value, high-precision timestamp, and key-value dimension tags.

Next is the Aggregated Metric Window, representing the pre-computed count, sum, average, min, max, and P50 through P99 percentiles for a specific five-second time bucket.

We also have the Anomaly Alert Entity, capturing the anomalous metric identifier, observed deviation score, expected baseline value, affected dimension slice, and timestamp.

Another entity is the Broadcast Event Context, defining the active live game, participating teams, current broadcast stage, and concurrent viewer count.

Finally, the Alert Subscription Rule entity governs escalation paths, pager rotations, and automated remediation webhook targets for different severity tiers.""",
        "api_design": """The ingestion fleet exposes a high-performance gRPC and UDP metric submission API used by server-side daemons to stream telemetry with minimal CPU overhead.

For client video players, a lightweight HTTP batch ingestion endpoint accepts compressed arrays of playback telemetry events every five seconds.

An internal query API provides sub-second time-series data retrieval for operational dashboards using optimized PromQL-like or SQL interfaces.

A webhook notification API delivers structured anomaly payloads to PagerDuty, Slack, and automated MCP remediation agents whenever critical thresholds are breached.""",
        "data_flow": """The data flow begins when edge proxies, ad auction nodes, and player video engines record operational performance metrics and emit them to local collector daemons.

The collector daemons batch and compress the telemetry points, streaming them into a globally distributed Apache Kafka cluster partitioned by metric name and region.

Apache Flink stream processing workers consume the raw metrics, maintaining stateful sliding windows that compute percentile distributions and error rates every five seconds.

The aggregated summaries are forwarded to an online anomaly detection worker running Isolation Forest and seasonal Holt-Winters forecasting algorithms.

If the observed error rate or latency exceeds the dynamic baseline threshold, an anomaly alert is dispatched to the incident response bus, while all aggregates are written to Apache Druid or M3DB for live dashboard rendering.""",
        "high_level_design": """At a high level, the architecture is organized into an edge collection layer, a streaming ingest bus, a stream analytics processing engine, and a time-series storage tier.

Telemetry collection utilizes lightweight OpenTelemetry sidecars and vector daemons deployed across all Kubernetes nodes and edge instances.

The ingestion tier relies on clustered Apache Kafka topics managed across multiple AWS availability zones with automatic partition balancing.

Stream processing and anomaly scoring are handled by Apache Flink jobs running on Amazon EMR, paired with Python-based anomaly microservices.

Persistent analytical queries are served by a distributed Apache Druid or ClickHouse cluster optimized for real-time aggregations across high-cardinality dimensions, backed by Amazon S3 for deep storage.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, achieving a five-second alert detection latency at fifty million metrics per second requires aggressive localized pre-aggregation. Rather than sending individual data points across the network, client and server agents compute T-Digest sketches and histograms locally over one-second intervals, cutting total network ingress volume by over ninety percent.

To eliminate false alarms during natural broadcast transitions like sudden halftime viewership drops, the anomaly detection engine does not rely on static thresholds. Instead, it utilizes contextual awareness by factoring in live game state: an ad request surge that would normally trigger an alarm is recognized as standard behavior when the game enters a commercial break.

High-cardinality dimensions are protected against memory explosion using Count-Min Sketch and HyperLogLog probabilistic data structures within Flink memory, allowing the system to monitor billions of unique user-device combinations with bounded RAM.

The telemetry infrastructure is deployed in dedicated AWS accounts isolated from production ad serving, guaranteeing that network storms or resource exhaustion in production cannot degrade monitoring visibility.""",
    },

    # Q12: AI-Powered Dynamic Ad Creative Personalization & Overlay Synthesis
    {
        "id": 12,
        "title": "AI-Powered Dynamic Ad Creative Personalization and Contextual Overlay Synthesis",
        "category": "GenAI & Creative Personalization",
        "problem_statement": """Design a real-time Generative AI and dynamic creative optimization system for Prime Video live events. The platform must dynamically synthesize customized, contextual video overlay graphics and L-bar advertisements tailored to viewer demographics and live game events (such as celebrating a local team touchdown) within three seconds of a game trigger.""",
        "clarifying_questions": """To properly frame this creative synthesis system, I would first ask whether we are generating full-motion video files from scratch using diffusion models, or dynamically compositing pre-rendered brand assets with personalized text, live game scores, and local retail offers. Generating full generative video in real time is computationally impractical, whereas dynamic graphical compositing with generative LLM copy and localized templates is feasible and broadcast-grade.

Next, I would ask about the delivery format. Are personalized overlays rendered server-side into the video stream, or are they rendered on client devices as interactive HTML5 and graphics overlays? Client-rendered interactive graphics provide greater personalization, lower cloud compute costs, and enable click-to-buy features.

I would also clarify the latency SLA from the triggering game event to overlay display. When a touchdown occurs, the contextual celebration ad must appear on screen within three to five seconds to capitalize on viewer excitement.

Finally, I would ask about advertiser brand safety and approval workflows: all brand logos, color palettes, and generative copy templates must be pre-approved by advertisers before the game begins.""",
        "svg_diagram": generate_svg(
            "Dynamic Creative Personalization & Overlays",
            [
                ["Live Game Trigger", "Touchdown / Home Run"],
                ["Contextual Ad Engine", "Template & Rule Matcher"],
                ["GenAI Copy Synthesizer", "Bedrock Fast LLM"],
                ["Asset Compositor", "Pre-Approved Brand Layers"],
                ["Client Overlay SDK", "Sub-3s Interactive Display"]
            ]
        ),
        "functional_requirements": """Functionally, the system must listen to real-time game event triggers from official sports data feeds, identifying major moments like touchdowns, home runs, or buzzer-beater shots.

It must select an appropriate pre-approved advertiser creative template matching the live context and the target viewer's location and brand affinity.

The system must invoke a generative AI copy synthesizer to generate snappy, contextual ad text tailored to the specific game situation and the viewer's local retail availability.

It must assemble the finalized graphic overlay payload, combining brand vector graphics, generative copy, dynamic game scores, and interactive shopping links into a lightweight render package.

Finally, it must push the overlay instruction payload to viewers' video players, instructing the player SDK to display the graphic overlay at the exact specified presentation timestamp.""",
        "non_functional_requirements": """In terms of non-functional requirements, the end-to-end latency from game event trigger to player overlay display must be under three seconds to maintain emotional relevance.

The system must scale to deliver millions of personalized overlay variations simultaneously across different viewer cohorts without overwhelming client video players.

Visual quality and brand safety must be 100 percent compliant with advertiser guidelines, ensuring zero brand logo distortions or inappropriate generated text.

The client rendering engine must be exceptionally lightweight, consuming less than five percent of device CPU and zero noticeable impact on live video playback smoothness.""",
        "core_entities": """The primary core entity is the Game Trigger Event, capturing the event type, team identifier, player name, current score, and game clock timestamp.

Next is the Advertiser Creative Template, defining acceptable layout zones, typography rules, brand color palettes, approved logo assets, and call-to-action buttons.

We also have the Viewer Personalization Profile, which includes the user's favorite team, geographical market, Prime delivery address eligibility, and past shopping preferences.

Another entity is the Synthesized Overlay Package, containing the resolved image URLs, dynamic text strings, display animation coordinates, and interactive click targets.

Finally, the Overlay Delivery Telemetry entity logs whether the overlay was successfully rendered on the client device and any user engagement interactions.""",
        "api_design": """The service exposes a real-time event trigger API called /triggers/v1/game-event that receives verified sports milestones from the live sports telemetry ingestion engine.

Video player clients maintain an active WebSocket or Server-Sent Events connection to /live/v1/overlay-stream to receive real-time overlay render instructions.

There is a campaign configuration API for advertisers to upload approved SVG and PNG brand assets, specify copy generation guardrails, and set target audience filters.

A tracking API accepts viewability and interaction beacons from the client video player whenever a user views, clicks, or dismisses an interactive overlay.""",
        "data_flow": """The data flow begins when a player scores a touchdown, prompting the sports telemetry engine to publish a Touchdown Event to an Amazon Kinesis stream.

The Contextual Ad Engine consumes the event and queries an in-memory cache to identify all advertisers who purchased situational touchdown sponsorships for that team.

For each viewer cohort, the engine calls a lightweight LLM on Amazon Bedrock using pre-compiled prompt templates with strict output constraints to generate localized celebration ad copy in two hundred milliseconds.

The synthesized copy and pre-cached brand asset URLs are packaged into a compact JSON render instruction.

The instruction is pushed over persistent WebSocket connections to client video players, where the player's graphic layer renders an animated L-bar overlay synchronized with the live celebration.""",
        "high_level_design": """At a high level, the architecture combines a situational trigger listener, an AI copy generation pipeline, an asset distribution layer, and a client-side rendering SDK.

The trigger listener is a low-latency Go microservice that filters and normalizes live sports telemetry feeds.

Generative copy synthesis is handled by Python microservices deployed in AWS Lambda that invoke Amazon Bedrock with Claude 3.5 Haiku or optimized local models to guarantee sub-second text generation.

Static brand assets including high-resolution vector logos and product imagery are pre-cached across Amazon CloudFront global edge caches prior to game kickoff.

Client video players integrate a lightweight WebAssembly and Canvas rendering SDK embedded in the Prime Video player, capable of drawing smooth graphics directly over the video canvas without interrupting stream playback.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, hitting the three-second delivery SLA while leveraging generative AI requires aggressive pre-generation and speculative synthesis. Rather than waiting for the touchdown to occur to start generating ad copy, our system uses speculative generation: as soon as a team enters the red zone, the LLM pre-generates celebratory copy for potential touchdown scenarios across top players, caching the candidates in Redis.

When the touchdown actually happens, the system executes an instantaneous cache lookup taking five milliseconds instead of waiting for a live LLM call, easily beating the three-second broadcast SLA.

To guarantee absolute brand safety and eliminate model hallucinations, the LLM does not generate freeform text; it operates within strict slot-filling grammar constraints where only verified player names, scores, and pre-approved marketing slogans can be populated.

On client devices, the overlay SDK operates in an isolated worker thread using offscreen canvas rendering, guaranteeing that graphics computations can never steal CPU cycles from the core video decoding pipeline and cause frame drops.""",
    },

    # Q13: Global Ad Campaign Inventory Forecasting & Reservation Engine
    {
        "id": 13,
        "title": "Global Ad Campaign Inventory Forecasting and Reservation Engine for Live Sports",
        "category": "Inventory Management & Forecasting",
        "problem_statement": """Design an enterprise-scale ad campaign inventory forecasting and reservation engine for Amazon's live sports portfolio (including Thursday Night Football, NBA, and NASCAR). The system must forecast available ad impressions across hundreds of millions of projected viewer segments months in advance, allowing sales teams to reserve guaranteed high-value sponsorships while preventing inventory overselling or under-delivery.""",
        "clarifying_questions": """When clarifying this system, I would first ask about the time horizon and update frequency of the forecasting model. Are sales teams running ad-hoc what-if inventory scenarios months in advance during upfront advertising negotiations, or does the system need to continuously recalibrate available inventory in real time as game dates approach and team standings change? Both long-term upfront planning and daily recalibration are required.

Next, I would ask about the granularity of audience targeting. Are advertisers reserving broad national broadcast slots, or are they booking hyper-specific demographic slices such as males aged twenty-five to forty-nine living in Chicago streaming on 4K connected televisions? Finer audience slices increase dimensionality and require sophisticated overlap modeling.

I would also clarify the reservation mechanics and consistency model. When a sales executive places a hold on fifty million impressions, how is that capacity locked to prevent another salesperson from selling the exact same audience capacity concurrently? Strong consistency or transactional locking is critical for inventory reservations.

Finally, I would ask how the engine handles uncertain game outcomes like playoff series that may end in four games or stretch to seven games.""",
        "svg_diagram": generate_svg(
            "Ad Inventory Forecasting & Reservation",
            [
                ["Historical Viewership Logs", "Multi-Season S3 Data"],
                ["ML Forecasting Engine", "Time-Series & Team Form"],
                ["Multi-Dimensional HyperCube", "Audience Overlap Matrix"],
                ["Reservation Service", "ACID Allocation Locks"],
                ["Sales Portal & Ad Server", "Guaranteed Booking"]
            ]
        ),
        "functional_requirements": """Functionally, the forecasting engine must ingest historical viewership logs, team popularity indices, matchup rivalries, seasonal broadcast ratings, and television scheduling data to predict audience reach for future live events.

It must construct a multi-dimensional inventory model that projects available ad impressions broken down by geographic market, demographic cohort, device category, and commercial break slot.

The system must support interactive what-if scenario simulations for sales teams, calculating real-time availability and pricing when complex targeting criteria and exclusion rules are applied.

It must enforce guaranteed reservation holds, atomically deducting reserved capacity from the available pool and issuing contractual allocation tokens.

Finally, it must track actual pacing as games air, comparing actual delivered impressions against reserved commitments and automatically suggesting inventory reallocation if a blowout causes viewership to trail projections.""",
        "non_functional_requirements": """From a non-functional perspective, sales availability queries must execute in under two seconds to support smooth, interactive booking experiences on sales portals.

The inventory reservation engine must guarantee strict serializability and strong data consistency, ensuring that zero double-booking or overselling occurs even when hundreds of sales agents book simultaneously.

The machine learning forecasting pipeline must process terabytes of historical viewing data and retrain seasonal models on a daily basis.

The system must scale to manage inventory portfolios spanning thousands of live sports broadcasts, hundreds of thousands of targeting combinations, and billions of potential ad impressions.""",
        "core_entities": """The primary core entity is the Live Broadcast Fixture, defining the scheduled date, teams, venue, expected start time, and historical rating category.

Next is the Audience Segment Forecast, storing predicted concurrent viewer counts, impression capacity, and demographic probability distributions for that fixture.

We also have the Ad Campaign Reservation, capturing the advertiser ID, contract value, requested audience targeting attributes, reserved impression count, and reservation status.

Another entity is the Inventory Hypercube, representing the pre-computed multi-dimensional capacity index across audience slices.

Finally, the Delivery Reconciliation Record tracks the variance between promised reservation numbers and real-world verified impressions after game completion.""",
        "api_design": """The service provides a RESTful query API called /inventory/v1/availability that takes targeting criteria, event IDs, and requested impression counts, returning real-time availability numbers and price quotes.

A transactional booking API called /inventory/v1/reserve allows authorized sales platforms to place hard holds and permanent reservations on specific inventory blocks.

There is a batch forecasting API that triggers retraining of machine learning models and recalculation of seasonal capacity cubes upon receiving updated league schedules.

An internal pacing feedback API consumes real-time delivery telemetry from the impression collector to reconcile reserved balances against actual views in real time.""",
        "data_flow": """The data flow begins as data engineering pipelines ingest years of historical streaming logs from Amazon S3 alongside team rankings, television ratings, and holiday calendars.

A machine learning training cluster runs gradient boosted trees and deep time-series forecasting models to generate audience size and composition predictions for upcoming games.

These predictions are transformed into a compressed multi-dimensional inventory hypercube stored in memory and distributed databases.

When a sales executive queries availability for a target campaign, the query service traverses the hypercube, applying set-intersection mathematics to determine available unreserved capacity.

When the booking is confirmed, the reservation service initiates a distributed transaction that decrements available inventory, records the contract in PostgreSQL, and publishes an allocation update to the ad serving plane.""",
        "high_level_design": """At a high level, the architecture is split into an offline forecasting and model training pipeline, an in-memory inventory indexing tier, and an online transactional reservation service.

Offline forecasting is orchestrated using Apache Airflow and Amazon EMR, processing petabytes of historical viewer logs to output daily forecasted capacity files.

The inventory availability engine is implemented in Java and Spring Boot, utilizing high-performance in-memory bitmap indexing techniques such as Roaring Bitmaps to calculate set intersections across millions of viewer profiles in milliseconds.

Transactional bookings are managed by a dedicated Reservation Service backed by Amazon Aurora PostgreSQL with serializable transaction isolation to eliminate race conditions.

Real-time inventory states and campaign commitments are pushed to downstream ad decision servers via event streams to govern live bid eligibility during game broadcasts.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, resolving complex audience overlap calculations across millions of potential targeting combinations in under two seconds is mathematically challenging. If one advertiser buys sports fans in Texas on mobile and another buys automotive intenders in the US South, their audience pools overlap significantly.

We solve this using Roaring Bitmaps and Maximum Flow Graph modeling: instead of evaluating individual users, the system represents demographic and behavioral cohorts as pre-computed bitsets, allowing union and intersection operations to execute in single-digit milliseconds using CPU vector instructions.

To prevent inventory overselling during high-volume upfront upfront sales seasons, the reservation service uses two-phase locking with short-lived fifteen-minute soft holds: an inventory slice is locked while a sales proposal is being prepared, and automatically released back to the general pool if the contract is not finalized within the window.

To manage the uncertainty of playoff series (where games five, six, and seven are conditional), the forecasting engine assigns probability weights to each potential game, allowing sales teams to sell conditional options contracts that automatically activate only if the series extends.""",
    },

    # Q14: High-Throughput Stream Ingestion & ETL Pipeline for Ad Telemetry
    {
        "id": 14,
        "title": "High-Throughput Stream Ingestion and ETL Pipeline for Viewer Ad Telemetry",
        "category": "Data Engineering & Stream Processing",
        "problem_statement": """Design a fault-tolerant, high-throughput stream ingestion and ETL pipeline for Prime Video ad telemetry. The system must process over one hundred million event records per minute during live commercial breaks, performing real-time schema validation, enrichment with viewer and campaign metadata, multi-stage sessionization, and loading into real-time analytical and batch storage destinations.""",
        "clarifying_questions": """To properly scope this streaming ETL pipeline, I would first ask about the variety and schema stability of incoming telemetry events. Are we processing a homogeneous event stream of standard ad impression beacons, or do we handle diverse schemas including video quality metrics, audio synchronization logs, interactive shopping clicks, and player error events? A unified Avro schema with evolution support is vital.

Next, I would ask about data delivery semantics and ordering guarantees. Does the downstream consumer require strict chronological ordering per viewer session, or is at-least-once delivery with idempotent downstream upserts sufficient? At-least-once delivery with partition-keyed ordering per viewer is standard.

I would also clarify the maximum acceptable processing lag. How quickly must incoming raw telemetry events appear in downstream analytics databases for operational dashboards? Real-time operational dashboards typically require end-to-end data latency under ten seconds.

Finally, I would ask about disaster recovery and data replay capabilities in case a bug in an ETL job corrupts downstream state.""",
        "svg_diagram": generate_svg(
            "High-Throughput Ad Telemetry ETL Pipeline",
            [
                ["Raw Event Ingestion", "Edge Envoy Fleet"],
                ["Kafka Event Buffer", "Partitioned by Session"],
                ["Apache Flink ETL", "Enrichment & Sessionize"],
                ["Real-Time Store", "ClickHouse / Pinot"],
                ["Cold Data Lake", "S3 Parquet via Iceberg"]
            ]
        ),
        "functional_requirements": """Functionally, the ETL pipeline must ingest raw telemetry event streams arriving from edge proxy servers, manifest stitching workers, and client video player SDKs.

It must validate each incoming record against centralized schema registries, quarantining malformed or corrupt payloads into a dead-letter queue for inspection.

The pipeline must enrich raw events with broadcast metadata, advertiser campaign attributes, and geographic lookup information by joining against real-time reference data caches.

It must sessionize related telemetry events across the playback lifecycle, combining ad request, bid win, impression start, quartile milestones, and completion into unified session records.

Finally, it must sink processed data simultaneously to an online analytical processing database for sub-second dashboard queries and to a cloud data lake in columnar formats for historical training and audits.""",
        "non_functional_requirements": """On the non-functional side, extreme throughput is the defining challenge, requiring the system to sustain sustained ingestion loads of over two million events per second with bursts exceeding five million during commercial breaks.

End-to-end data freshness must be under ten seconds from event generation at the edge to queryability in operational dashboards.

Data durability must be 99.999999999 percent, with multi-datacenter replication ensuring zero data loss even during severe cloud availability zone outages.

The pipeline must support full backpressure management, gracefully buffering traffic during downstream database slowdowns without crashing upstream workers.""",
        "core_entities": """The primary core entity is the Raw Telemetry Event, containing the raw JSON or Protobuf payload, client IP, user agent, ingest timestamp, and event type.

Next is the Enriched Ad Record, which adds campaign IDs, brand taxonomy codes, game broadcast IDs, team names, and normalized geographic identifiers.

We also have the Sessionized Ad Lifecycle Entity, aggregating all milestone beacons for a single commercial impression into an end-to-end viewing session record.

Another entity is the Dead Letter Queue Record, capturing rejected payloads along with validation error codes and stack traces.

Finally, the Partition Manifest entity tracks committed streaming offsets, checkpoint files, and written Parquet file metadata in the data lake.""",
        "api_design": """The ingestion layer exposes an internal streaming endpoint accepting batched, snappy-compressed Protocol Buffer records from edge proxies.

A Schema Registry API manages Avro and Protobuf schemas, providing version enforcement and backward compatibility checks for all producers and consumers.

Downstream analytics users interact with the system through standard SQL query APIs exposed by Apache Pinot or ClickHouse.

An operational control API allows data engineers to trigger pipeline replays from specific Kafka offsets, pause specific partition consumers, and inspect dead-letter queues.""",
        "data_flow": """The data flow begins when client video players and edge manifest servers emit telemetry batches to our edge ingestion fleet via HTTP/2.

The ingestion nodes validate the format against the Schema Registry and append the raw events into an Apache Kafka topic partitioned by the hash of the viewer session ID.

Apache Flink consumer applications read events from Kafka, performing real-time lookups against a local RocksDB cache populated with campaign and broadcast metadata to enrich each record.

Flink's stateful operators group related events by impression ID across a fifteen-minute sliding window, emitting a fully reconciled session record when playback completes.

Enriched and sessionized records are written in micro-batches to ClickHouse for live operational dashboards and simultaneously committed to Amazon S3 in Apache Iceberg Parquet tables for long-term machine learning and business intelligence.""",
        "high_level_design": """At a high level, the architecture utilizes a decoupled streaming ingest layer, a stateful stream processing tier, and a bifurcated storage destination pattern.

The ingestion gateway runs as an Auto Scaling fleet of Go microservices behind AWS Network Load Balancers, capable of scaling out dynamically based on live event schedules.

The messaging backbone consists of multi-cluster Apache Kafka deployed on AWS with NVMe storage to sustain massive write I/O.

Stream processing is powered by Apache Flink running on Kubernetes, utilizing RocksDB state backends and asynchronous checkpoints saved to Amazon S3.

The storage tier splits data into a hot path powered by ClickHouse for real-time operations and a cold path powered by Apache Iceberg on Amazon S3 for petabyte-scale historical analytics.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, maintaining sub-ten-second data freshness during sudden five-million-event-per-second surges requires eliminating all external synchronous network lookups in the stream processing path. Flink workers never query external relational databases to enrich telemetry; instead, they maintain localized in-memory broadcast state tables that continuously mirror campaign metadata from low-volume Kafka change-data-capture topics.

To prevent consumer lag from spiraling during game halftimes, Kafka partitions are provisioned with significant headroom: each live event is allocated hundreds of dedicated partitions, allowing Flink to scale out worker tasks across dozens of compute nodes.

Durability is protected through Flink's implementation of the Chandy-Lamport checkpointing algorithm, persisting consistent distributed snapshots to Amazon S3 every thirty seconds.

If an unexpected worker crash occurs, Flink automatically recovers from the latest clean checkpoint, rewinds Kafka consumer offsets, and resumes processing without dropping a single impression record or introducing duplicate financial metrics.""",
    },

    # Q15: Resilient Multi-Region Ad Server Fallback & Slate Delivery Architecture
    {
        "id": 15,
        "title": "Resilient Multi-Region Ad Server Fallback and Slate Content Delivery Architecture",
        "category": "High Availability & Disaster Recovery",
        "problem_statement": """Design a fault-tolerant multi-region ad serving and failover architecture for Prime Video live events. The system must guarantee broadcast continuity during major cloud infrastructure outages, network partitions, or ad decision server crashes, automatically failing over to local edge caches and fallback slate reels within fifty milliseconds so that viewers never see a black screen or video stutter.""",
        "clarifying_questions": """When clarifying this disaster recovery architecture, my first question is about the definition of failure: what exact conditions trigger an automated failover? We should establish thresholds such as a region experiencing more than two percent timeout errors over a five-second window, or complete loss of connectivity to an entire AWS availability zone or region.

Next, I would ask about the fallback content hierarchy. When ad decisioning fails, what should be displayed to the viewer? The typical fallback priority is first to show a pre-cached house ad or Prime Video original promo, and if that is unavailable, to seamlessly transition to a localized broadcast slate reel with ambient stadium audio.

I would also clarify the data synchronization model between active regions. Do all regions operate in an active-active configuration sharing live campaign pacing state, or is there an active-passive setup with asynchronous state replication? An active-active multi-region deployment is necessary for broadcast resilience.

Finally, I would ask about traffic rerouting mechanisms: how do we shift millions of viewer connections between regions without overwhelming the failover region?""",
        "svg_diagram": generate_svg(
            "Multi-Region Ad Server Fallback Architecture",
            [
                ["Global Anycast Route 53", "Latency-Based Health Routing"],
                ["Primary Region Cluster", "Active Ad Decisioning"],
                ["Circuit Breaker Proxy", "50ms Hard Timeout Guard"],
                ["Secondary Region Cluster", "Active-Active Mirror"],
                ["Edge Slate Engine", "Local Pre-Warmed Video Reel"]
            ]
        ),
        "functional_requirements": """Functionally, the architecture must support active-active ad serving across multiple geographically distributed cloud regions such as US-East and US-West.

It must continuously monitor the health of all regional microservices, network links, and dependent ad decision components using high-frequency synthetic probes and real-time error rate trackers.

If a primary region degrades, edge manifest stitchers must automatically reroute requests to an alternate healthy region without disrupting ongoing video playback.

If an ad decision service in any region fails to return a response within a strict fifty-millisecond deadline, an automated circuit breaker must intercept the request and inject a pre-transcoded fallback advertisement.

If the entire ad serving infrastructure becomes completely unreachable, the edge manifest engine must instantly stitch a local, pre-warmed broadcast slate video reel to maintain broadcast continuity.""",
        "non_functional_requirements": """From a non-functional perspective, failover switching must execute in under fifty milliseconds to ensure that video player buffers never stall and live playback remains completely uninterrupted.

Overall system availability must reach 99.999 percent, ensuring fewer than five minutes of total downtime per year across all live sports programming.

The architecture must handle catastrophic regional cloud outages, allowing the entire global viewership load to be absorbed by surviving regions without cascading failure.

Video quality and audio loudness of fallback ads and slates must perfectly match the surrounding live football broadcast to comply with CALM Act broadcast loudness regulations.""",
        "core_entities": """The primary core entity is the Regional Health Status, tracking error rates, P99 response latencies, and circuit breaker trip states across all active serving regions.

Next is the Fallback Content Manifest, which specifies pre-transcoded video segment URLs for house promos and broadcast slates across all required bitrate and resolution ladders.

We also have the Global Routing Policy, defining Anycast IP mappings, DNS failover thresholds, and weighted traffic distribution percentages across regions.

Another entity is the Cross-Region State Replication Log, synchronizing campaign spend balances and frequency capping updates between regions.

Finally, the Disaster Recovery Incident Event entity logs failover triggers, affected viewer percentages, and duration of fallback operation for post-mortem analysis.""",
        "api_design": """The global traffic management layer leverages AWS Route 53 and CloudFront origin request policies with health check endpoints like /health/v1/deep-check returning service status in five milliseconds.

Internal edge proxies communicate with regional ad servers via an internal gRPC client that implements aggressive deadlines, exponential backoff, and automatic connection retries.

A centralized configuration API allows incident commanders to execute manual regional traffic shifts or activate emergency slate mode with a single administrative command.

A broadcast telemetry API publishes real-time failover state changes and circuit breaker engagement metrics to operations center video walls.""",
        "data_flow": """The data flow begins when a viewer's edge manifest proxy attempts to request an ad decision from the primary regional cluster in US-East.

The edge proxy's internal circuit breaker monitors the connection with a strict thirty-five millisecond timeout.

If US-East responds normally, the ad pod is stitched and returned to the viewer as expected.

If the connection times out or returns HTTP 5xx errors, the circuit breaker trips instantly, and the edge proxy attempts a secondary request to the US-West cluster over dedicated internal AWS backbone fibers.

If the secondary region is also unresponsive, the proxy immediately retrieves a pre-cached slate video segment from local edge memory, stitches the slate into the HLS playlist, and returns the valid manifest in under ten milliseconds.""",
        "high_level_design": """At a high level, the architecture is designed as a three-tiered defense-in-depth model spanning global edge points of presence, active-active regional clusters, and a cross-region replication layer.

The first tier is the CDN edge running on AWS CloudFront, where local workers store pre-warmed fallback video slates directly in memory.

The second tier comprises independent, fully functional ad serving stacks deployed in multiple AWS regions, each equipped with dedicated Envoy gateways, Kubernetes worker fleets, and local Redis caches.

The third tier is a cross-region synchronization mesh utilizing Amazon DynamoDB Global Tables and Apache Kafka MirrorMaker 2 to replicate critical campaign budget balances and frequency data asynchronously.

Global traffic routing is orchestrated using AWS Global Accelerator and Route 53 Application Recovery Controller, providing deterministic regional failover in seconds.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, preventing cascading failures during a sudden regional failover requires strict load shedding and capacity reservation. When US-East drops and its entire traffic volume shifts to US-West, the receiving region can experience a doubling of load within seconds.

To protect against this, our regional clusters are provisioned with fifty percent idle headroom during live sports events, and regional proxies implement priority-based load shedding: if CPU utilization exceeds eighty percent, the server sheds non-essential tasks like complex real-time bidding and serves local house ads instead.

To guarantee zero broadcast disruption, fallback video slates are pre-transcoded into identical HLS and DASH segment profiles matching the exact framerate, GOP size, and audio bitrate of the live sports stream, pre-loading them into edge caches hours before the game.

This ensures that when an emergency fallback occurs, the video player experiences seamless playback with zero audio pops, buffering spinners, or visual artifacts, maintaining the broadcast-grade illusion of uninterrupted coverage.""",
    },

    # Q16: AI-Augmented RCA & Broadcast Runbook Automation Assistant
    {
        "id": 16,
        "title": "AI-Augmented Root Cause Analysis and Broadcast Runbook Assistant",
        "category": "AI Operations & Incident Response",
        "problem_statement": """Design an AI-augmented Root Cause Analysis (RCA) and operational runbook automation assistant for on-call engineers supporting Amazon Advertising live events. During high-severity production incidents, the system must synthesize distributed telemetry, error logs, and recent code deployments, diagnosing the primary root cause in under ninety seconds and proposing executable, safety-checked remediation commands.""",
        "clarifying_questions": """To clarify the scope of this AI assistant, I would first ask about the role of the human engineer. Is the assistant designed as an interactive pair-debugging partner in a chat room like Slack, or does it operate headlessly in the background generating automated incident reports? An interactive conversational assistant in Slack that can both answer questions and suggest one-click actions is the most practical and trusted pattern.

Next, I would ask what systems the assistant can query during its diagnostic phase. Can it search git commit histories, AWS CloudTrail deployment events, Kubernetes pod logs, and distributed trace graphs? Broad access across logs, metrics, deployments, and architectural knowledge is essential for accurate diagnosis.

I would also clarify the latency requirement for root cause diagnosis. In a live sporting event, the assistant should provide an initial diagnostic hypothesis within sixty to ninety seconds of an incident declaration.

Finally, I would ask how the assistant verifies the safety of proposed commands to ensure it never suggests destructive actions like dropping a production table or terminating an active cluster.""",
        "svg_diagram": generate_svg(
            "AI Root Cause Analysis & Runbook Assistant",
            [
                ["Incident Declaration", "PagerDuty / Alert Trigger"],
                ["Context Collector", "Logs, Traces & Git Diffs"],
                ["LLM Reasoning Agent", "RCA Diagnostic Engine"],
                ["Runbook Matcher", "Pre-Approved Safe Fixes"],
                ["Interactive Chatbot", "Slack Incident Command"]
            ]
        ),
        "functional_requirements": """Functionally, the assistant must automatically wake whenever a high-severity incident is declared via PagerDuty or an alert in the broadcast operations channel.

It must immediately pull recent operational context from the affected time window, including spike metrics, error logs from OpenSearch, distributed trace spans from AWS X-Ray, and recent deployments from AWS CodePipeline.

The system must run diagnostic reasoning models to correlate anomalies, identifying patterns like a memory leak introduced in the latest release or an exhausted connection pool caused by a slow database dependency.

It must search our internal repository of standard operating runbooks, selecting the appropriate procedure and presenting the diagnostic summary along with executable remediation scripts in Slack.

Finally, upon incident resolution, it must draft a comprehensive post-mortem report detailing the timeline, contributing factors, impact assessment, and recommended prevention items.""",
        "non_functional_requirements": """From a non-functional perspective, time to diagnosis is paramount: the assistant must deliver its initial root-cause hypothesis and runbook recommendation within ninety seconds of incident activation.

Accuracy is critical, requiring the assistant to ground its reasoning strictly in verified telemetry and facts, with zero tolerance for hallucinated log entries or nonexistent service names.

Security and access control must be strictly enforced, ensuring that all proposed runbook commands adhere to least-privilege principles and require two-person authorization for destructive actions.

The assistant platform must be highly available and isolated from the systems it monitors, ensuring it remains fully operational even during major infrastructure outages.""",
        "core_entities": """The primary core entity is the Incident Investigation Session, tracking the incident ticket ID, severity level, affected broadcast service, start timestamp, and assigned incident commander.

Next is the Telemetry Evidence Bundle, containing collected error stack traces, latency graphs, top offending endpoints, and correlated deployment diffs.

We also have the Root Cause Hypothesis entity, storing the diagnosed failure mode, confidence score, supporting evidence links, and identified culprit service.

Another entity is the Runbook Action Step, defining the specific command line instruction or API call, expected output, safety classification, and rollback instructions.

Finally, the Post-Incident Review Document captures the complete chronological timeline, root cause summary, and action items formatted for engineering review.""",
        "api_design": """The assistant provides a conversational Slack integration API that listens to commands like @incident-bot diagnose or @incident-bot run step 2 in war room channels.

There is a diagnostic ingestion API that accepts incident trigger webhooks from PagerDuty and CloudWatch alarms, initializing investigation sessions automatically.

An internal Tool Execution API allows the assistant to execute read-only diagnostic queries against Prometheus, OpenSearch, and Kubernetes clusters via secure MCP servers.

A post-mortem publishing API pushes generated markdown incident reports directly into internal wiki systems like Confluence or GitHub issues for team review.""",
        "data_flow": """The data flow begins when an on-call engineer or automated alarm triggers a P1 incident for SSAI manifest errors during an NBA broadcast.

The incident bot initializes a new investigation session and fans out parallel queries to OpenSearch for 5xx error logs, AWS X-Ray for slow trace spans, and GitHub for commits deployed in the last two hours.

The gathered logs, trace graphs, and deployment diffs are compiled into a structured prompt context and submitted to an advanced reasoning model on Amazon Bedrock.

The model correlates a sudden spike in database connection timeouts with a configuration change deployed thirty minutes earlier that reduced maximum connection pool size.

The assistant posts a concise diagnosis in the incident Slack channel along with a pre-validated runbook command to roll back the configuration change, waiting for the engineer's one-click approval to execute.""",
        "high_level_design": """At a high level, the architecture combines a conversational interface, an autonomous agent orchestration engine, a multi-source data retrieval pipeline, and a secure tool execution environment.

The user interface is powered by a Slack Bolt application running in AWS Lambda, providing real-time chat interactions and interactive action buttons.

The orchestration core is implemented with Python and LangGraph, utilizing retrieval-augmented generation and chain-of-thought prompt architectures powered by Claude 3.5 Sonnet on Amazon Bedrock.

Data retrieval connectors query internal observability backends using pre-authenticated IAM roles and read-only endpoints.

Command execution is managed by a secure, sandboxed execution service that verifies engineer permissions, enforces two-person approval for high-risk commands, and records full audit logs for every executed action.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, ensuring factual accuracy and eliminating hallucinations in high-pressure incident rooms requires strict evidence-grounded prompting techniques. The assistant's reasoning engine is instructed to never speculate; every diagnostic claim must cite a specific log line, metric graph timestamp, or commit hash included in the evidence bundle.

To complete comprehensive diagnostic investigations within ninety seconds, the data retrieval pipeline executes all log, trace, and git queries concurrently using asynchronous Python coroutines, assembling the full evidence bundle in under twenty seconds.

Command safety is enforced through a deterministic Command Validation Proxy: the assistant cannot generate arbitrary shell commands; it can only select from a strict whitelist of pre-approved parameterized runbook scripts that have been vetted by security teams.

All Slack interactions, generated diagnoses, human approvals, and command execution outputs are immutably archived in Amazon S3 with Write-Once-Read-Many policies, providing an audit trail for compliance and post-incident reviews.""",
    },

    # Q17: Real-Time Interactive Shopping & Click-to-Buy Ad Overlay Service
    {
        "id": 17,
        "title": "Real-Time Interactive Shopping and Click-to-Buy Ad Overlay Service",
        "category": "Interactive Commerce & Live Advertising",
        "problem_statement": """Design a low-latency, scalable interactive shopping and click-to-buy ad overlay platform for Prime Video live sports streams. The system must display synchronized, interactive product cards (such as team jerseys or showcased sponsor items) directly over the video stream, allowing millions of concurrent viewers to browse, scan QR codes, or complete one-click purchases via their Amazon accounts without interrupting game playback.""",
        "clarifying_questions": """When clarifying this interactive commerce system, I would first ask about the purchasing flow on different devices. On mobile devices and smart TVs, the experience differs: mobile users can tap directly on the screen to purchase, while living room smart TV users typically prefer scanning a personalized on-screen QR code with their mobile phone or using their television remote for one-click checkout.

Next, I would ask about inventory reservation and cart integration. Does tapping Buy Now immediately charge the customer's default Amazon 1-Click payment method and ship to their primary address, or does it add the item to an Amazon shopping cart for later review? Providing both a frictionless 1-Click purchase option and an Add to Cart option caters to different user preferences.

I would also ask about the scale of concurrent purchase spikes. If a high-profile player scores a spectacular goal and an exclusive limited-edition jersey overlay appears, tens of thousands of orders per second may hit the checkout service simultaneously.

Finally, I would ask about synchronization with the live video feed: the overlay must appear at the exact frame the product is mentioned by commentators.""",
        "svg_diagram": generate_svg(
            "Interactive Shopping & Click-to-Buy Platform",
            [
                ["Broadcast Trigger", "Product Cue & Timestamp"],
                ["Overlay Distribution", "WebSocket & CDN Channel"],
                ["Client Render Engine", "Interactive Overlay Layer"],
                ["QR & 1-Click Purchase", "Amazon Commerce Gateway"],
                ["Order Fulfillment Queue", "High-Throughput Checkout"]
            ]
        ),
        "functional_requirements": """Functionally, the platform must allow broadcast producers and advertisers to schedule interactive shopping overlays tied to specific presentation timestamps or live game milestones.

It must deliver lightweight product metadata packages including product titles, high-resolution imagery, pricing, customer ratings, and Prime delivery estimates to viewers' video players.

The system must dynamically generate individualized on-screen QR codes encoded with signed session tokens that allow viewers to scan the TV screen and complete checkout instantly on their smartphones.

It must integrate with the Amazon Commerce platform to support seamless 1-Click purchasing using the viewer's authenticated Amazon credentials.

Finally, it must track interactive engagement metrics in real time, including overlay impressions, click-through rates, QR code scans, cart additions, and finalized purchases.""",
        "non_functional_requirements": """From a non-functional perspective, the overlay display instruction must synchronize with video playback with sub-second accuracy, ensuring graphics appear precisely when the product is showcased on screen.

The checkout ingestion pipeline must sustain sudden flash-sale purchase surges of over fifty thousand orders per second without dropped transactions or double billing.

The on-screen interactive overlay must maintain silky-smooth sixty-frames-per-second animation performance without causing video frame drops or playback stutter on low-power streaming sticks.

User data privacy and transaction security must comply with PCI-DSS standards, ensuring that payment credentials and shipping addresses are protected end-to-end.""",
        "core_entities": """The primary core entity is the Shoppable Ad Campaign, linking an advertiser, product ASIN, broadcast fixture, target audience segments, and active time windows.

Next is the Product Catalog Snapshot, capturing the item title, hero image URL, current Amazon price, Prime badge status, and real-time inventory count.

We also have the Interactive Viewer Session, mapping the user ID, device type, screen resolution, and active streaming session token.

Another entity is the Personalized QR Code Token, containing an encrypted payload encoding user identity, campaign ID, and a short-lived cryptographic signature.

Finally, the One-Click Purchase Order entity records the transaction ID, ASIN, quantity, billing status, and fulfillment tracking reference.""",
        "api_design": """The client player SDK communicates with an overlay distribution API using WebSockets or Server-Sent Events to receive real-time overlay display and dismiss commands.

A dedicated commerce API endpoint called /commerce/v1/buy-now accepts authenticated purchase requests from client devices, initiating instant 1-Click checkout.

There is a dynamic QR code generator API that returns personalized, short-lived SVG QR codes encoded with cryptographic deep links to the Amazon shopping app.

An advertiser analytics API provides real-time conversion reporting, displaying live impressions, scan rates, and total attributed sales volume to merchant dashboards.""",
        "data_flow": """The data flow begins when the broadcast control room or automated computer vision system triggers a Shoppable Moment linked to a featured product ASIN.

The interactive shopping engine queries an in-memory product cache to retrieve up-to-the-minute pricing, Prime shipping availability, and inventory status.

The engine broadcasts an overlay activation message containing product metadata and animation parameters across persistent WebSocket connections to active player sessions.

The client video player SDK renders the non-intrusive interactive card in the corner of the screen, rendering an individualized QR code for smart TV users.

When a viewer taps the card or scans the QR code on their phone, the request routes to our commerce gateway, which executes a 1-Click purchase against the user's Amazon account and queues the order for fulfillment.""",
        "high_level_design": """At a high level, the architecture combines a broadcast synchronization layer, a real-time messaging gateway, an interactive client SDK, and an elastic commerce integration plane.

Broadcast cues are synchronized using SCTE-35 metadata or WebSocket notification channels powered by AWS AppSync and Amazon API Gateway.

Real-time product metadata and inventory checks are served by a distributed Redis cluster that caches Amazon Retail catalog attributes to avoid hitting core catalog databases during live broadcasts.

The client rendering engine is implemented as a high-performance WebAssembly and HTML5 component embedded in the Prime Video player across FireTV, iOS, Android, and web platforms.

Flash checkout orders are ingested by an Auto Scaling fleet of Go microservices that write order payloads into high-throughput Amazon SQS FIFO queues, decoupling immediate user response from downstream warehouse fulfillment systems.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, handling extreme purchase spikes during high-profile live sports moments requires robust asynchronous checkout architectures. When twenty thousand viewers tap Buy Now within three seconds, attempting synchronous inventory reservation and payment processing in a single HTTP request would cause database connection exhaustion and timeouts.

Instead, our commerce gateway performs instantaneous cryptographic signature verification and account validation in memory, writes the order payload to a durable partitioned Amazon SQS FIFO queue, and immediately returns a Confirmed Order status to the viewer in under eighty milliseconds.

Downstream worker fleets process the queue asynchronously, executing payment authorization and inventory deduction in batches against core Amazon fulfillment services.

To ensure client video playback smoothness on budget streaming sticks like Fire TV Stick Lite, the overlay rendering engine operates on a dedicated hardware-accelerated compositor layer, ensuring that even complex animated graphics and QR code updates consume less than three percent of device CPU and zero memory leaks.""",
    },

    # Q18: Distributed Rate Limiter & Traffic Throttling for Ad Break Surges
    {
        "id": 18,
        "title": "Distributed Rate Limiter and Traffic Throttling Service for Live Ad Break Surges",
        "category": "Traffic Management & Infrastructure Resilience",
        "problem_statement": """Design a distributed, highly performant rate limiting and traffic throttling service for Amazon Advertising in live events. The system must protect core ad decisioning microservices, third-party DSP connections, and database clusters from catastrophic load surges when over fifteen million concurrent viewers enter a commercial break simultaneously, enforcing multi-tier tenant quotas and graceful degradation within one millisecond.""",
        "clarifying_questions": """To clarify the design of this distributed rate limiter, I would first ask about the granularity of rate limiting. Are we limiting traffic globally per microservice, per API route, per third-party DSP partner, or per individual viewer device? In live sports advertising, multi-tier rate limiting is required: protecting downstream DSP partner connections from exceeding agreed queries-per-second limits while simultaneously protecting our own internal database clusters from being overwhelmed.

Next, I would ask about the acceptable latency overhead. Because this rate limiter sits directly in the critical request path of every ad call, the rate limiting decision must execute in under one millisecond.

I would also clarify the rate limiting algorithm preference. Algorithms like Token Bucket, Leaky Bucket, and Sliding Window Counter each offer different trade-offs between burst tolerance and smoothness. For ad traffic surges, a Token Bucket or Sliding Window Counter is typically ideal.

Finally, I would ask how the system behaves during rate limiter infrastructure failure: the rate limiter must fail open to prevent an internal throttling glitch from halting the entire live broadcast.""",
        "svg_diagram": generate_svg(
            "Distributed Rate Limiter & Throttling Fleet",
            [
                ["Incoming Ad Requests", "15M Viewer Spike"],
                ["Envoy Edge Proxy", "Local Token Bucket Cache"],
                ["Distributed Rate Limiter", "Redis Cluster Sync"],
                ["Downstream Services", "Protected Microservices"],
                ["Graceful Shedder", "Default Ad Fallback"]
            ]
        ),
        "functional_requirements": """Functionally, the rate limiting service must evaluate incoming API requests across multiple dimensions, including client IP, viewer session, API route, and downstream target partner.

It must track request volumes against dynamically configured quota rules, enforcing maximum queries-per-second and burst allowances.

When an entity exceeds its rate limit, the service must immediately return an HTTP 429 Too Many Requests response or trigger an internal graceful degradation pathway.

It must support multi-tenant configuration, allowing operations teams to set customized quotas for different third-party DSPs and internal microservices.

Finally, it must provide real-time metrics on dropped requests, quota utilization percentages, and throttling events to operational dashboards.""",
        "non_functional_requirements": """From a non-functional perspective, decision latency must be sub-millisecond, with P99 evaluation times staying strictly under five hundred microseconds.

The rate limiting tier must scale horizontally to handle aggregate throughput exceeding ten million quota evaluations per second during peak commercial break transitions.

The system must adhere to a strict Fail-Open principle: if the rate limiter cluster experiences network partitions or crashes, traffic must be permitted through rather than blocked.

Rate limiting accuracy must remain consistent across globally distributed regions, avoiding significant drift between regional token buckets.""",
        "core_entities": """The primary core entity is the Rate Limit Rule, defining the target resource key, allowable request count, time window duration, burst multiplier, and action on breach.

Next is the Token Bucket State, tracking the current available token count, bucket capacity, refill rate, and timestamp of the last token replenishment.

We also have the Client Quota Identifier, which represents the composite key of tenant ID, client category, and target API endpoint.

Another entity is the Throttling Event Log, capturing dropped request counts, timestamps, offending client keys, and active traffic loads.

Finally, the Dynamic Quota Override entity allows broadcast operations to temporarily expand or restrict specific partner quotas during live games.""",
        "api_design": """The rate limiter implements an ultra-fast gRPC CheckQuota interface integrated directly into Envoy proxies via the standard external authorization and rate limit filter.

An internal REST management API allows automated scaling controllers and operations engineers to update quota rules and bucket capacities in real time.

There is a high-speed telemetry streaming API that publishes real-time rate limit hit metrics and drop counts to Prometheus and CloudWatch.

A bulk check API allows batch services to evaluate rate limits for groups of ad opportunities in a single round-trip call.""",
        "data_flow": """The data flow begins when an incoming ad manifest request reaches an Envoy edge proxy fronting the ad decisioning infrastructure.

The Envoy proxy invokes the local in-memory rate limiting filter via gRPC, passing the client key, target service name, and request weight.

The rate limiter evaluates the key against its local token bucket cache, deducting tokens if available and returning an OK status in under three hundred microseconds.

If the local token bucket is exhausted, the service checks whether global quota headroom exists by querying a clustered Redis instance using atomic Lua scripts.

If the quota is exceeded, the rate limiter returns a THROTTLED response, prompting the edge proxy to immediately bypass complex auction processing and serve a pre-cached default sponsor ad.""",
        "high_level_design": """At a high level, the architecture employs a hierarchical two-tier rate limiting model consisting of local in-process token buckets on Envoy proxies backed by a distributed Redis cluster.

The first tier operates locally within each Envoy proxy instance using thread-safe in-memory token buckets, resolving over ninety percent of rate checks without making any network calls.

The second tier consists of a dedicated Rate Limiting cluster running high-performance C++ or Go workers connected to an Amazon ElastiCache Redis cluster using Redis Cluster sharding.

Redis manages shared global quotas across instances using optimized Lua scripts that execute atomic sliding window evaluations in microseconds.

Dynamic quota rules and tenant configurations are stored in Amazon DynamoDB and synchronized to edge worker memory using change-data-capture streams.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, achieving sub-millisecond evaluation at ten million requests per second requires eliminating Redis network round-trips for the majority of requests. We achieve this using Local Token Batching: instead of incrementing a central Redis counter on every single ad request, each local proxy node reserves a batch of tokens (e.g., five hundred tokens) from Redis asynchronously and satisfies individual incoming requests from its local memory.

Only when the local token pool falls below a safety threshold does the proxy reach out to Redis for another batch, reducing network traffic to Redis by over ninety-five percent.

To guarantee broadcast availability, the system implements a hard Fail-Open circuit breaker: if the rate limiting service fails to respond within eight hundred microseconds, the Envoy proxy automatically assumes the request is allowed and passes it through.

Furthermore, during extreme surges, the rate limiter does not simply discard excess requests; it routes throttled requests to a low-overhead Graceful Degradation Lane, ensuring that even if real-time auctions cannot run, viewers still receive a high-quality default house commercial rather than a playback error.""",
    },

    # Q19: Real-Time Sports Live Data Ingestion & Context-Aware Ad Triggering
    {
        "id": 19,
        "title": "Real-Time Sports Live Data Ingestion and Context-Aware Ad Triggering Engine",
        "category": "Real-Time Telemetry & Contextual Advertising",
        "problem_statement": """Design a real-time live sports telemetry ingestion and contextual ad triggering engine for Prime Video live events. The system must ingest official live play-by-play data feeds with sub-second latency, maintain an in-memory game state machine, and evaluate complex situational ad targeting rules (such as triggering a pizza delivery ad immediately following a team touchdown) within fifty milliseconds of event occurrence.""",
        "clarifying_questions": """When beginning this design, I would first ask about the ingestion latency of upstream sports data providers. Feeds from partners like Sportradar, Genius Sports, or the NFL Next Gen Stats arrive over push WebSockets or HTTP/2 streams; we should clarify the expected network latency and how we handle out-of-order or corrected play events (such as a touchdown that is subsequently overturned by referee review).

Next, I would ask about the rule complexity. Are contextual targeting rules simple condition matches like event == 'touchdown', or do they involve complex stateful aggregations such as team scored three consecutive times, score differential < 7 points, and quarter == 4? The rule engine must support stateful pattern matching.

I would also clarify the output target: does this engine trigger instant on-screen graphics overlays, prepare the upcoming commercial break ad pod, or both? Triggering both interactive overlays and priming upcoming commercial breaks is the standard live sports requirement.

Finally, I would ask about high availability and multi-provider failover: if the primary sports feed drops, the system must seamlessly fail over to a backup provider without missing critical game events.""",
        "svg_diagram": generate_svg(
            "Sports Telemetry Ingest & Contextual Ad Trigger",
            [
                ["Official Sports Feed", "Sportradar / NFL Next Gen"],
                ["State Machine Ingest", "Out-of-Order Play Handler"],
                ["Contextual Rule Engine", "Complex Event Processing"],
                ["Ad Opportunity Bus", "Sub-50ms Event Trigger"],
                ["SSAI & Overlay Fleet", "Contextual Ad Activation"]
            ]
        ),
        "functional_requirements": """Functionally, the engine must establish persistent, redundant streaming connections to official sports data providers to ingest real-time play-by-play events, player tracking coordinates, and game clock updates.

It must maintain an authoritative, in-memory live game state machine tracking score, quarter, possession, field position, player stats, and historical game momentum.

The service must execute a Complex Event Processing (CEP) engine that continuously evaluates incoming game events against active advertiser contextual targeting rules.

When a rule condition is met, the system must formulate a Contextual Ad Opportunity and broadcast it to downstream ad decision engines and video overlay systems within fifty milliseconds.

It must also gracefully handle referee reviews and score corrections, emitting compensation events if a play that triggered an ad action is subsequently nullified.""",
        "non_functional_requirements": """On the non-functional side, end-to-end processing latency is the most critical constraint: the time from receiving a sports play payload to publishing the triggered ad opportunity must be under fifty milliseconds.

System reliability must reach 99.999 percent throughout live broadcasts, with zero downtime during gameplay.

The engine must ensure deterministic state management, handling duplicate play reports and network jitter without corrupting the live game state.

Scalability must support parallel ingestion and rule evaluation across hundreds of concurrent live sporting events worldwide.""",
        "core_entities": """The primary core entity is the Official Sports Telemetry Message, containing the play ID, game ID, play type, participating players, game clock, score, and play description.

Next is the Live Game State Machine, tracking the current quarter, active possession, down and distance, penalty status, and recent momentum metrics.

We also have the Contextual Targeting Rule, specifying trigger conditions, advertiser ID, campaign priority, maximum trigger frequency, and target creative IDs.

Another entity is the Triggered Ad Opportunity, defining the activated campaign, target audience segment, eligible ad slots, and contextual metadata tags.

Finally, the Play Reconciliation Event entity captures retroactive play reversals and adjustments issued by league officials.""",
        "api_design": """The ingestion fleet implements persistent WebSocket and SSE client connectors that maintain authenticated streaming sessions with external sports data providers.

The engine exposes an internal gRPC service called /gamestate/v1/query that allows ad decision servers to query current game context in under two milliseconds.

A rule management REST API allows advertising operations teams to create, test, and activate contextual targeting campaigns before and during the live game.

A real-time trigger publication stream publishes activated ad opportunities into an Amazon Kinesis or Apache Kafka topic for consumption by the ad serving plane.""",
        "data_flow": """The data flow begins when an official sports radar sensor records a touchdown and pushes a structured JSON play payload over a persistent WebSocket connection to our ingest proxy.

The ingest proxy validates the message sequence number, normalizes the provider-specific format into a standard Amazon Sports schema, and passes it to the Game State Engine.

The state engine updates the in-memory game state machine and feeds the new event into an embedded Esper or Flink Complex Event Processing rule engine.

The rule engine matches the touchdown event against active campaigns, identifying that a food delivery brand has purchased a Touchdown Celebration sponsorship.

The engine generates an Ad Opportunity event enriched with the scoring player's name and team colors, publishing it to Redis Pub/Sub within thirty milliseconds to activate on-screen overlays and prime the upcoming commercial break.""",
        "high_level_design": """At a high level, the architecture combines a high-reliability feed ingestion tier, an in-memory stateful processing core, a rule evaluation engine, and an event distribution bus.

Feed ingestion is handled by redundant Go microservices running across multiple availability zones, each maintaining independent connections to primary and secondary sports data vendors.

The game state machine and Complex Event Processing engine are implemented using Apache Flink CEP or embedded in-memory rule engines running within Kubernetes worker pods.

Game state is persisted in an in-memory Redis cluster with active replication, ensuring instantaneous state retrieval for concurrent ad requests.

Triggered opportunities are broadcast via Redis Pub/Sub and Amazon Kinesis to regional SSAI manifest engines and client overlay distribution gateways.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, achieving sub-fifty-millisecond trigger latency requires running the rule evaluation engine entirely in local memory without blocking disk or database I/O. The incoming telemetry stream is processed using zero-allocation memory buffers in Go, parsing JSON payloads into pre-allocated memory structs in single-digit microseconds.

To handle feed failures and network latency spikes from third-party sports data providers, the ingest tier employs an Active-Active Multi-Provider Arbiter: it connects to two independent sports data feeds simultaneously, using monotonically increasing play sequence numbers and timestamps to process the fastest arriving packet while discarding duplicate or slower updates.

To handle referee video reviews that overturn scoring plays, the system maintains a ten-second Reversibility Window: if a touchdown is overturned by a referee challenge within thirty seconds, the engine emits a Compensating Event that cancels any pending commercial break prioritization and adjusts downstream billing logs.

All contextual rules are compiled into abstract syntax trees in memory ahead of game kickoff, allowing millions of rule evaluations to execute across game events in microseconds.""",
    },

    # Q20: Edge-Assisted Audience Cohort Segmentation & Profile Cache
    {
        "id": 20,
        "title": "Edge-Assisted Audience Cohort Segmentation and Real-Time Profile Cache",
        "category": "Targeting & Edge Architecture",
        "problem_statement": """Design an edge-assisted audience cohort segmentation and real-time viewer profile caching platform for Prime Video advertising. The system must maintain and evaluate targeting segments (such as demographic cohorts, behavioral interests, and geographic locations) for over one hundred million viewers, delivering compact targeting tokens to edge SSAI workers in under two milliseconds while preserving viewer privacy.""",
        "clarifying_questions": """When clarifying this edge targeting system, I would first ask about the size and format of viewer targeting profiles. Can a viewer's profile be represented as a compact bitmap or array of integer segment IDs, or does it require rich, unstructured key-value attributes? Storing profiles as compact bitsets or integer arrays is ideal because it minimizes edge memory footprint and network payload sizes.

Next, I would ask how frequently audience profiles are updated. Are segment memberships recalculated offline in daily batch jobs, or do they update in real time based on immediate browsing and shopping actions across Amazon? A hybrid approach is standard: broad demographic segments update daily, while immediate in-stream actions update in real time.

I would also clarify privacy and compliance boundaries. How do we ensure that Personally Identifiable Information (PII) is never pushed to CDN edge caches, and how do we enforce regional privacy laws like GDPR and CCPA? Anonymous hashed tokens and anonymized cohort IDs ensure full privacy compliance.

Finally, I would ask about cache miss behavior at the edge: if a viewer profile is not in the local edge cache, how quickly can the system fetch it without delaying manifest delivery?""",
        "svg_diagram": generate_svg(
            "Edge Audience Cohort Segmentation Platform",
            [
                ["Batch Data Lake & DPo", "Offline Segment Builder"],
                ["Real-Time Event Stream", "Immediate Behavioral Updates"],
                ["Global Profile Store", "DynamoDB Global Tables"],
                ["Edge Cache Sync", "CloudFront KeyValueStore"],
                ["SSAI Manifest Stitcher", "Sub-2ms Token Lookup"]
            ]
        ),
        "functional_requirements": """Functionally, the platform must ingest offline audience segment computations from Amazon's enterprise data lake alongside real-time behavioral events from the streaming app and Amazon retail platform.

It must compile each viewer's active targeting profile into a compact, privacy-preserving token containing hashed cohort IDs, interest tags, and geographic codes.

The system must distribute these compact profiles to CDN edge points of presence worldwide, caching them close to viewers' playback devices.

When an edge SSAI manifest stitcher processes an ad break for a viewer, the profile cache must return the viewer's active targeting tokens in under two milliseconds.

It must also provide an administrative interface for audience planners to create new cohort definitions, test segment reach, and invalidate outdated profile caches dynamically.""",
        "non_functional_requirements": """From a non-functional perspective, lookup latency at the edge must be sub-two-millisecond at the P99 percentile to prevent slowing down manifest generation.

The edge caching layer must support over one hundred million active viewer profiles while keeping memory usage cost-effective.

Privacy by design is essential: zero unencrypted PII, cleartext names, or raw email addresses can ever be stored in edge caches or transmitted across public networks.

Data freshness must allow newly updated behavioral segments to propagate to global edge caches within five minutes of calculation.""",
        "core_entities": """The primary core entity is the Audience Segment Definition, specifying the segment ID, name, classification category, expiration policy, and targeting criteria.

Next is the Compact Viewer Profile, containing the anonymized user hash, an array of 32-bit integer segment IDs, and a regional market code.

We also have the Real-Time Behavioral Signal, capturing immediate in-app actions such as sports genre browsing, search queries, or retail product interactions.

Another entity is the Edge Cache Partition, representing the localized key-value store instance running within a specific CloudFront point of presence.

Finally, the Privacy Consent State entity records the viewer's active privacy preferences and advertising opt-out status.""",
        "api_design": """The edge manifest stitcher accesses the profile cache using a local in-memory C++ or Rust API called GetViewerTargetingTokens(user_hash) that returns the segment array in microseconds.

An internal profile synchronization API accepts batched profile delta updates from central processing pipelines via secure gRPC channels.

There is a segmentation management REST API that allows marketing teams to define new rule-based cohorts and query estimated segment sizes.

A privacy synchronization endpoint consumes global consent updates, instantly purging or anonymizing edge profiles whenever a user opts out of personalized advertising.""",
        "data_flow": """The data flow begins in Amazon's data lake, where batch machine learning jobs process customer viewing history and retail signals to assign users to demographic and interest cohorts.

These cohort assignments are compiled into compact binary vectors and written to Amazon DynamoDB Global Tables.

Concurrently, a real-time streaming pipeline consumes immediate behavioral events from Kafka, updating the active segment bitset in DynamoDB.

DynamoDB Streams publish profile delta changes to an edge synchronization worker that pushes updated compact tokens to CloudFront KeyValueStore and regional ElastiCache nodes.

When a viewer requests a live game manifest, the edge worker hashes the user ID from the session cookie, queries the local edge cache, and passes the retrieved targeting tokens to the ad decision engine in under one millisecond.""",
        "high_level_design": """At a high level, the architecture is split into a centralized segmentation engine, a global database distribution tier, and a distributed edge cache layer.

The centralized segmentation engine is built on Apache Spark and Amazon EMR for batch processing, paired with Apache Flink for real-time behavioral updates.

Central profile storage is anchored by Amazon DynamoDB Global Tables, providing multi-region active-active replication with sub-ten-millisecond cross-region propagation.

Edge caching utilizes Amazon CloudFront KeyValueStore integrated directly into CloudFront edge locations, complemented by regional Redis clusters at major edge hubs.

Privacy enforcement is built into the ingestion gateway, ensuring all profiles are cryptographically anonymized using one-way salted hashes before leaving central data centers.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, storing one hundred million viewer profiles at hundreds of edge locations without incurring massive memory costs requires extreme data compaction. Instead of storing profiles as JSON strings, our platform encodes audience segment memberships as a compressed Roaring Bitmap, packing hundreds of segment memberships into less than one hundred bytes per user.

This compact representation allows millions of profiles to reside in memory at each edge location with a tiny memory footprint.

To achieve sub-two-millisecond lookup latency, the edge manifest worker reads directly from CloudFront KeyValueStore, an in-memory key-value engine co-located with CloudFront servers that delivers single-digit microsecond read latencies.

If an edge cache miss occurs, the worker does not stall the live video manifest request: it immediately returns a default broad demographic profile (e.g., General Sports Enthusiast based on geographic IP), while asynchronously triggering a background fetch to warm the edge cache for the next commercial break."""
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(sysde_questions_part2)} System Design questions (Part 2).")
