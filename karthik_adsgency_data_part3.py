# -*- coding: utf-8 -*-
"""
Part 3: Top 10 System Design Walkthroughs for Karthik Ravula
Target Role: Member of Technical Staff (MTS) - Full Stack / AI Systems at AdsGency AI
Format: Conversational walkthrough in small, clear paragraph chunks WITHOUT ANY BULLET POINTS.
Includes ASCII architecture diagram.
"""

sysde_questions = [
    # System Design 1
    {
        "id": 1,
        "title": "Multi-Agent Autonomous Ad Campaign Orchestration Engine",
        "category": "Multi-Agent Systems & AI Infrastructure",
        "problem_statement": "Design an autonomous multi-agent orchestration engine for AdsGency AI that allows marketing operators to input natural language campaign objectives. The system must autonomously plan, generate copy and visual creatives, configure audience targeting, and deploy campaigns across Google Ads, Meta, and TikTok without entering infinite execution loops or conflicting actions.",
        "diagram": """```
=== MULTI-AGENT AUTONOMOUS CAMPAIGN ORCHESTRATOR ===

[1] Operator Dashboard (Next.js / React)
        │
        ▼
[2] API Gateway & Auth (FastAPI / JWT)
        │
        ▼
[3] Supervisor & Planner Agent (LangGraph / State Machine)
        │
        ├──────────────────────┬──────────────────────┐
        ▼                      ▼                      ▼
[4] Creative Copy Agent   [5] Audience Agent    [6] Budget Pacing Agent
 (OpenAI / Claude / RAG)   (Customer Match/DB)   (Redis / Multi-Platform)
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                               ▼
[7] Brand Safety & Verification Agent (Semantic Guardrails)
                               │
                               ▼
[8] Ad Platform Gateway (Meta, Google, TikTok Graph APIs)
```""",
        "functional_requirements": """When we look at what this system needs to accomplish for our users, the core experience begins when a marketing operator enters a natural language prompt specifying a marketing goal, such as launching a summer promotional blitz for an e-commerce brand with a daily budget split across social channels. The system needs to take that broad objective and automatically break it down into concrete, actionable steps across creative generation, audience targeting, and multi-platform deployment.

Once the plan is established, specialized autonomous agents need to execute the individual components of the campaign. A copy agent generates platform-compliant headlines and captions, an audience agent pulls relevant demographic clusters and lookalike segments, and a budget agent configures platform-specific bidding parameters. 

Before any mutation is submitted to external ad platforms, the system must enforce a verification step where safety guardrails inspect the generated copy and budget limits. Finally, the system needs to persist the execution state at every stage so that an operator can inspect the intermediate reasoning traces, pause the workflow, or manually adjust parameters before final deployment.""",
        "non_functional_requirements": """On the non-functional side, reliability and determinism are our highest priorities because we are automating real marketing spend across external financial platforms. The system cannot afford to lose state or trigger duplicate ad creation if an external network connection blinks during deployment.

We need our orchestration engine to maintain high availability with four nines of uptime so that scheduled campaigns launch reliably across global time zones. Latency for the initial planning phase should complete in under ten seconds, giving the operator rapid feedback, while background multi-platform execution can run asynchronously within two minutes.

Data isolation across enterprise tenants is non-negotiable. Every agent execution, context memory, and ad platform token must be strictly segregated by organization so that one customer's proprietary marketing strategy is never leaked or accessible to another tenant's agents.""",
        "core_entities": """The central entity in our data model is the Campaign Workflow, which tracks the overall lifecycle, tenant identity, status, and raw user prompt. Each workflow links to multiple Agent Task Execution records, representing discrete tasks performed by specialized agents such as copy generation, asset formatting, or budget allocation.

Beneath each task, we store Agent Message Traces, which capture the exact prompts, LLM model identifiers, tool calls, and platform responses. This creates an immutable audit trail for observability and debugging.

We also maintain the Campaign Deployment entity, which records external platform identifiers such as the Meta Ad Set ID or Google Campaign ID, alongside status flags, timestamps, and active version numbers to support safe rollbacks and reconciliation.""",
        "api_design": """Our API surface is built using FastAPI and exposes clean RESTful endpoints for workflow creation and real-time streaming. An operator initiates a workflow by sending a POST request to the campaigns endpoint with their prompt, budget, and target platforms, receiving back a unique workflow identifier and an HTTP 202 Accepted status.

To inspect progress without polling, the frontend connects to an SSE streaming endpoint that continuously emits state transition events as individual agents complete their tasks. This delivers live progress updates and reasoning tokens directly into the React user interface.

If an operator wants to modify an active plan, they send a PATCH request to the workflow tasks endpoint with updated parameters. Furthermore, a POST request to the approval endpoint allows human operators to provide final authorization before external ad platform mutations execute.""",
        "data_flow": """The end-to-end data flow begins when the operator submits their campaign prompt through our Nextra and React frontend dashboard. The request enters our FastAPI gateway, where authentication tokens are validated, and a new workflow record is committed to PostgreSQL with a pending state.

The gateway pushes the workflow task into a Redis queue, which is picked up by a LangGraph supervisor worker. The supervisor prompts our primary LLM to construct a deterministic execution graph, decomposing the campaign into sub-tasks for copy generation, audience selection, and budget calculation.

These worker agents execute their tasks in parallel or sequence, pulling brand context and historical exemplars from PostgreSQL using pgvector embeddings. Once all worker outputs are assembled, the payload passes through the Brand Safety Agent for compliance verification. Upon approval, the Ad Platform Gateway dispatches signed requests to Meta, Google, and TikTok, writing back external IDs to our database and streaming a completion notification to the operator.""",
        "high_level_design": """Our high-level architecture is organized into four distinct horizontal tiers: the presentation and edge tier, the API and state machine tier, the agent worker tier, and the external integration tier. The presentation layer is powered by Next.js and React, delivering an interactive operator interface with real-time streaming capabilities.

The API tier runs FastAPI microservices containerized on Kubernetes EKS behind an AWS Application Load Balancer. It handles rate limiting, request validation, and tenant authentication before dispatching jobs to our messaging bus.

The agent worker tier utilizes LangGraph state machines backed by Redis for ephemeral state and distributed locking, with PostgreSQL serving as our source of truth. The external integration tier wraps external advertising APIs behind circuit breakers and idempotent retry queues, ensuring our platform interacts safely with third-party networks.""",
        "nfr_deep_dive": """Let's take a deep dive into how we guarantee loop prevention, fault recovery, and strict tenant isolation. In autonomous agent loops, there is always a risk that an agent encounters ambiguous feedback and repeatedly invokes tools in an infinite recursion, draining LLM token budgets and stalling the system. We eliminate this by enforcing a hard recursion limit inside LangGraph and tracking a state hash in Redis; if the same state hash repeats twice without forward progress, the workflow automatically halts and requests human intervention.

For fault tolerance, every step in our state graph is an idempotent checkpoint persisted in PostgreSQL. If a worker pod crashes mid-execution, a secondary worker immediately recovers the workflow from the last verified checkpoint rather than starting from scratch, preventing duplicate creative generation and wasted API spend.

Tenant isolation is enforced through PostgreSQL Row-Level Security paired with encrypted tenant context in our Redis key namespacing. Furthermore, external platform OAuth tokens are encrypted at rest using AWS KMS envelope encryption, ensuring that agents can only decrypt credentials belonging to the active tenant session."""
    },

    # System Design 2
    {
        "id": 2,
        "title": "Real-Time Ad Spend & Budget Pacing Engine",
        "category": "Real-Time Streaming & Financial Infrastructure",
        "problem_statement": "Design an ultra-low latency, distributed budget pacing engine for AdsGency AI that tracks spend across Google, Meta, and TikTok ad accounts in real time. The system must prevent overspending during viral traffic surges, adjust bids dynamically based on hourly pacing targets, and execute emergency ad pauses within 500 milliseconds of budget exhaustion.",
        "diagram": """```
=== REAL-TIME BUDGET PACING & EMERGENCY CIRCUIT BREAKER ===

[1] Ad Platform Webhooks (Meta, Google, TikTok Clicks/Spend)
        │
        ▼
[2] Ingestion Gateway (FastAPI / Async Buffer)
        │
        ▼
[3] Partitioned Event Log (Apache Kafka / Key: campaign_id)
        │
        ▼
[4] Streaming Processor (Python / Flink / Redis Lua Scripts)
        │
        ├── Atomic Spend Accumulator (Redis In-Memory Counter)
        │
        ▼
[5] Pacing Evaluator (Linear & PID Controller Algorithm)
        │
        ├── Normal Pacing ───> [6] Dynamic Bid Adjustment Queue
        │
        └── Overspend Detected ───> [7] Emergency Kill Switch (HTTP <500ms)
                                          │
                                          ▼
                                   [8] External Ad APIs (Campaign Pause)
```""",
        "functional_requirements": """The functional goal of the budget pacing engine is to ensure that a client's daily marketing capital is distributed intelligently across the day rather than being exhausted in the first few hours of the morning. When impressions and clicks occur on external platforms, raw telemetry and webhook events flow into our system detailing the exact micro-costs incurred.

The engine must continuously aggregate these micro-costs in real time and compare current spend against the scheduled pacing curve. Depending on campaign strategy, the pacing algorithm might follow an even linear pacing model or an accelerated curve that capitalizes on peak conversion hours.

If the pacing curve indicates that a campaign is spending faster than expected, the system must automatically calculate reduced bid values and push them to the ad networks. Conversely, if a campaign breaches its daily budget ceiling due to sudden viral spikes, the engine must trigger an automated emergency pause across all participating platforms to prevent financial overruns.""",
        "non_functional_requirements": """Latency and accuracy are paramount when dealing with live advertising budgets. The emergency kill switch must execute and dispatch pause commands to external ad APIs within five hundred milliseconds of a budget breach to prevent overspend.

Our aggregation counters must guarantee strict consistency and idempotency. Because external webhooks can be retried multiple times during network hiccups, processing the same click event twice would artificially inflate spend calculations, while dropping events would cause real-world overspending.

The system must scale horizontally to handle over fifty thousand incoming webhook events per second during peak holiday shopping surges without backpressure or dropped records, maintaining high availability around the clock.""",
        "core_entities": """The primary data entity is the Campaign Budget Profile, which defines the total budget, daily allocation, pacing strategy, and active status for each ad account. Linked to this is the Hourly Pacing Schedule, which maps target spend percentages to each hour of the day in the client's local time zone.

We maintain the Real-Time Spend Counter entity in our in-memory cache, storing cumulative micro-dollar spend, impression counts, and last-updated timestamps for immediate atomic querying.

Finally, the Budget Adjustment Ledger stores an append-only historical log of all automated bid adjustments, budget alerts, and emergency pause actions, recording the exact telemetry values that triggered each intervention.""",
        "api_design": """For administrative control, the engine exposes a PUT endpoint at campaign budgets allowing operators to set or adjust daily limits and pacing models. This endpoint validates the payload and updates both the relational database and the in-memory cache atomically.

For real-time visibility, an endpoint at campaign budgets pacing returns the current spend, target pacing percentage, projected daily run rate, and current health status of the campaign.

There is also an emergency override endpoint accessible via POST that allows marketing operators to manually trigger an immediate campaign pause or resume across all platforms with a single authenticated call.""",
        "data_flow": """Incoming conversion and spend webhooks from Google, Meta, and TikTok hit our lightweight ingestion gateway, which validates authentication headers and immediately writes the raw payload into a partitioned Kafka topic keyed by campaign ID.

Partitioning by campaign ID ensures that all financial events for a specific campaign are processed in strict chronological order by the downstream streaming workers. The worker consumes the event and executes an atomic Lua script in Redis that checks an event deduplication filter and increments the campaign's active spend accumulator.

Immediately after the accumulator updates, the pacing algorithm evaluates whether the new spend exceeds the hourly or daily limit. If the spend is normal, a bid adjustment task is scheduled; however, if the budget threshold is crossed, the worker immediately dispatches an urgent pause command directly to the ad network APIs via an asynchronous HTTP client pool while alerting operators.""",
        "high_level_design": """The architecture centers around a decoupled streaming and caching topology designed for extreme read and write performance. Ingress is handled by asynchronous FastAPI workers that push directly to an Apache Kafka cluster running across multiple availability zones.

State computation is divided between an in-memory Redis cluster that holds real-time atomic accumulators and a PostgreSQL database that stores long-term campaign rules and settled financial ledgers.

The decisioning layer is powered by background Python streaming workers that read from Kafka and interface with Redis via compiled Lua scripts. This ensures that spend accumulation and limit evaluation happen in a single non-blocking roundtrip. External mutations are handled by an outbound HTTP connection pool tuned with pre-warmed sockets to minimize dispatch latency.""",
        "nfr_deep_dive": """Let's look into how we achieve sub-millisecond atomic consistency and guarantee zero overspend. Redis Lua scripts are executed atomically on the server, meaning no other client can read or modify the spend key between the time we increment the balance and the time we evaluate the ceiling. This completely eliminates race conditions where concurrent webhook threads might both observe an under-budget state and fail to trigger the pause.

To handle transient network failures when communicating with external ad APIs, our outbound client implements an aggressive retry strategy with exponential backoff and circuit breaking. If Meta's API responds with a temporary five-hundred error, the pause request is immediately retried on alternative connections while an emergency webhook is broadcast to our internal Slack alert channel.

For disaster recovery, the streaming worker periodically takes snapshots of in-memory Redis balances and persists them to PostgreSQL. If an entire Redis instance fails, the state can be fully rehydrated in seconds by replaying Kafka offsets from the last verified database checkpoint, ensuring zero data loss."""
    },

    # System Design 3
    {
        "id": 3,
        "title": "High-Throughput Multi-Platform Marketing API Gateway",
        "category": "API Gateway & External Integrations",
        "problem_statement": "Design a resilient, unified Marketing API Gateway for AdsGency AI that abstracts the heterogeneous schemas, dynamic rate limits, and authentication protocols of Google Ads, Meta Graph API, and TikTok Business API into a single standardized internal interface.",
        "diagram": """```
=== UNIFIED MARKETING API GATEWAY ===

[1] Internal Agent Workers & Services
        │
        ▼
[2] Unified API Gateway (FastAPI / Pydantic Domain Model)
        │
        ▼
[3] Distributed Token-Bucket Rate Limiter (Redis)
        │
        ├── Under Quota ───> [4] Platform Adapter Layer
        │                          │
        │                          ├─ Google Ads gRPC Adapter
        │                          ├─ Meta Graph REST Adapter
        │                          └─ TikTok Marketing REST Adapter
        │                                  │
        │                                  ▼
        │                    [5] External Ad Platforms
        │
        └── Rate Limit Approaching ───> [6] Priority Buffer Queue (Kafka)
```""",
        "functional_requirements": """Our marketing API gateway acts as the single bridge between our internal autonomous agent services and the external advertising networks. Internally, our agents should not have to understand the idiosyncratic JSON structures of Meta's Marketing API, the protobuf schemas of Google Ads, or the specific field names of TikTok's Business API.

The gateway must provide a standardized internal domain model for campaigns, ad sets, creatives, and performance metrics. When an internal agent issues a command to create an ad, it sends a single unified payload to the gateway, which translates the request into the appropriate external platform format.

The system must also handle credential management and token refreshes transparently. When OAuth access tokens expire on Meta or Google, the gateway must automatically negotiate fresh tokens using secure refresh credentials without interrupting active agent workflows.""",
        "non_functional_requirements": """Resilience and strict adherence to external platform rate limits are the most vital non-functional requirements. External platforms will ban or throttle accounts that exceed their rate limits, which would halt all client campaigns. The gateway must dynamically throttle outbound traffic based on real-time rate limit headers.

The gateway needs to achieve high throughput, capable of processing millions of outbound requests and incoming webhooks daily with an internal proxy overhead of less than twenty milliseconds.

All outbound mutations must be strictly idempotent. If a network timeout occurs while creating an ad set, retrying the request must never create a duplicate ad set on the external platform, preserving client budget and campaign structure.""",
        "core_entities": """The core entity is the Platform Account Connection, which stores the organization identifier, platform name, external account ID, and encrypted OAuth tokens. Each connection references a Rate Limit Quota Profile that defines the active call allowances and window durations.

We also have the External Resource Mapping entity, which maintains the cross-reference between our internal UUIDs and the external platform identifiers such as Meta Campaign ID or Google Ad Group ID.

Finally, the Gateway Request Audit entity logs every outbound API dispatch, capturing response codes, round-trip latency, payload hashes, and rate limit header states for debugging and compliance.""",
        "api_design": """Internally, the gateway exposes RESTful routes such as POST to api v1 gateway campaigns, accepting a unified campaign schema with standard fields like name, daily budget, objective, target platforms, and flight dates.

For creative uploads, a POST endpoint at api v1 gateway creatives handles asset ingestion, uploads the binary files to our Amazon S3 buckets, and registers the creative across selected ad networks concurrently.

For telemetry, a GET endpoint at api v1 gateway metrics retrieves unified performance data across channels for any date range, normalizing disparate metrics into standard impressions, clicks, spend, and conversion values.""",
        "data_flow": """An autonomous agent submits a campaign deployment request to our gateway via an internal HTTP call. The gateway validates the unified payload using Pydantic and checks the tenant's authorization credentials.

Next, the gateway queries our Redis rate limiter to verify whether the target platform account has available call quota. If quota is available, the request passes into the platform-specific adapter, which formats the parameters and attaches the decrypted OAuth bearer token.

The adapter sends the request over the wire to the external API using pre-warmed HTTP or gRPC client pools. Upon receiving the external response, the adapter extracts the newly generated platform resource IDs, stores the cross-reference mapping in PostgreSQL, updates the rate limit tracker with the returned header values, and returns the unified response to the calling agent.""",
        "high_level_design": """The gateway is architected as an asynchronous modular service built on FastAPI and Python, deployed across multiple pods on AWS EKS. It sits behind an internal load balancer that routes requests from agent workers and frontend services.

The system relies on an in-memory Redis cluster to track distributed rate-limiting tokens across all running gateway instances. A PostgreSQL database stores account credentials, schema mappings, and audit logs.

For requests that cannot be dispatched immediately due to rate limits or external platform downtime, the gateway offloads jobs into a Kafka priority queue. Background consumer workers drain this queue as soon as rate limit windows reset, ensuring zero lost operations.""",
        "nfr_deep_dive": """Let's examine how our rate limiting and idempotency mechanisms prevent external account bans and duplicate mutations. We implement a distributed token-bucket rate limiter in Redis that inspects platform-specific response headers, such as Meta's business use case usage header. When our consumption reaches eighty-five percent of the platform threshold, the gateway automatically downshifts traffic, queuing lower-priority reporting requests and prioritizing high-value campaign mutations.

To guarantee idempotency, every outbound mutation generates a deterministic idempotency key derived from the campaign parameters and step identifier. When calling external APIs that support idempotency keys, such as Meta and Google, we pass this key in the request header. If an external call times out, our retry mechanism resubmits the exact same key; the external network recognizes the duplicate and returns the original result without re-executing the mutation.

For platforms that lack native idempotency support, our gateway checks its internal mapping database before retrying, querying the external platform by name or client reference to verify whether the asset was already created before deciding whether to resubmit."""
    },

    # System Design 4
    {
        "id": 4,
        "title": "Autonomous Creative Generation & Ad Copy A/B Testing Pipeline",
        "category": "AI/LLM Pipelines & Creative Optimization",
        "problem_statement": "Design an autonomous ad creative generation and continuous A/B testing pipeline for AdsGency AI. The system must ingest product catalogs, generate high-converting ad copy and visual concepts using LLMs and diffusion models, deploy multi-variant ad sets, and dynamically reallocate budget toward winning variations using multi-armed bandit algorithms.",
        "diagram": """```
=== AUTONOMOUS CREATIVE GENERATION & MULTI-ARMED BANDIT A/B TESTING ===

[1] Product Catalog & Brief Ingestion (PostgreSQL / S3)
        │
        ▼
[2] Context Retrieval & Exemplars (pgvector / Historical CTR)
        │
        ▼
[3] Multi-Variant Copy Generator (OpenAI / Claude / Pydantic)
        │
        ├──────────────────────┬──────────────────────┐
        ▼                      ▼                      ▼
  Variation A (Urgency)   Variation B (Social)   Variation C (Feature)
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                               ▼
[4] Creative Safety & Compliance Filter (Semantic Distance)
                               │
                               ▼
[5] Automated Ad Deployment (Meta, Google, TikTok APIs)
                               │
                               ▼
[6] Telemetry Stream (Impressions, Clicks, Conversions via Kafka)
                               │
                               ▼
[7] Multi-Armed Bandit Engine (Thompson Sampling / Beta Distribution)
                               │
                               ▼
[8] Automated Budget Reallocation (Dynamic Ad Spend Shift)
```""",
        "functional_requirements": """This pipeline serves as the creative brain of AdsGency AI, responsible for generating, testing, and optimizing ad creatives automatically. The workflow begins when a client uploads their product catalog, brand style guidelines, and historical performance briefs into the platform.

The creative generation engine retrieves top-performing historical ad copy and analyzes the target audience personas. It then uses LLMs to generate dozens of distinct copy variations, each exploring different psychological angles such as urgency, social proof, feature highlights, and curiosity hooks, while ensuring character counts match platform limits.

Once generated and approved, the variations are grouped into multi-variant ad sets and launched across selected advertising channels. The system continuously tracks performance telemetry and automatically shifts budget away from low-converting variants toward top-performing creatives using statistical algorithms.""",
        "non_functional_requirements": """Creative generation must maintain high semantic quality and strict adherence to brand safety guidelines. Generated copy must never include prohibited claims, hallucinations, or offensive phrasing that could jeopardize an advertiser's brand reputation.

The real-time analytics loop that feeds the multi-armed bandit must process incoming conversion signals with a latency of less than five minutes so that budget reallocations occur dynamically while campaigns are live.

The pipeline must support high concurrency, capable of generating hundreds of creative variations simultaneously for multiple enterprise clients without hitting LLM rate limits or exhausting backend memory.""",
        "core_entities": """The Product Asset entity stores product descriptions, price points, imagery URLs, and brand tone guidelines. Linked to this is the Creative Generation Run, which captures the generation prompt, model parameters, and target channels.

Each generated asset is represented by an Ad Creative Variation record, detailing the headline, body text, visual asset references, call-to-action, and unique variation tag.

For tracking performance, we have the Variant Performance Score entity, which stores cumulative impressions, clicks, conversions, current conversion rate, and the alpha and beta parameters used by the Thompson Sampling bandit algorithm.""",
        "api_design": """Marketing operators trigger generation through a POST request to api v1 creatives generate, passing the product identifier, desired number of variations, target platforms, and creative tone. The endpoint initiates an asynchronous job and returns a job identifier.

To preview and manage generated copy, operators query a GET endpoint at api v1 creatives variations with the job ID, returning structured cards with headlines, body text, and predicted engagement scores.

For real-time testing analytics, a GET endpoint at api v1 campaigns ab-test results provides real-time conversion curves, current budget distribution percentages, and statistical confidence intervals for each active variant.""",
        "data_flow": """When an operator requests creative generation, our background worker pulls the product metadata from PostgreSQL and queries pgvector for historical ad creatives in the same industry vertical that achieved a ROAS greater than three.

These top-performing examples are injected into our LLM prompt context as few-shot exemplars. The model generates structured JSON containing multiple distinct angles. The generated copy is passed through a semantic safety validator that checks against banned words and platform compliance policies.

The approved creatives are deployed to external ad networks as an experimental ad set. As real-time impression and conversion webhooks arrive via Kafka, a streaming worker updates the Beta distribution parameters for each variation in Redis. Every hour, the bandit algorithm recalculates allocation weights and adjusts external ad set budgets accordingly.""",
        "high_level_design": """The creative pipeline combines asynchronous generation workers with a streaming optimization engine. Generation is powered by Python workers utilizing LangChain and direct OpenAI and Claude API integrations, orchestrated via Celery and Redis.

Creative assets and historical embeddings are stored in PostgreSQL with pgvector, enabling fast semantic similarity lookups. Visual assets are stored in Amazon S3 and distributed via CloudFront CDN.

The statistical optimization engine runs as a lightweight real-time microservice that reads telemetry from Kafka, updates state in Redis, and issues budget mutation requests to external ad platforms via our marketing API gateway.""",
        "nfr_deep_dive": """Let's look into the mechanics of our Thompson Sampling multi-armed bandit algorithm and how we handle brand safety. Traditional A/B tests split traffic fifty-fifty for weeks, burning substantial money on inferior ads before declaring a winner. In our system, each ad variation is modeled as a Bernoulli bandit with a Beta distribution representing its conversion probability, parameterized by alpha (successes) and beta (failures). Every hour, the system draws random samples from each variant's posterior distribution and allocates budget proportionally to the probability that a variant is optimal. This ensures that winning ads quickly receive the majority of spend while continuing to explore newer variants.

For brand safety, every generated headline is evaluated against a pre-computed vector space of compliance violations and brand restrictions using cosine similarity in pgvector. If an ad's embedding falls within a safety threshold of prohibited themes or hallucinates an unauthorized discount percentage, it is automatically discarded and regenerated before human operators ever see it.

To handle LLM rate limits gracefully, our generation workers utilize an adaptive backoff queue in Redis, distributing prompt requests across multiple API keys and fallback models (such as Claude 3.5 Sonnet and GPT-4o) if an upstream provider experiences elevated latency or outages."""
    },

    # System Design 5
    {
        "id": 5,
        "title": "Agent Long-Term Memory & Context Retrieval System",
        "category": "Vector Databases, RAG & Context Infrastructure",
        "problem_statement": "Design a scalable, low-latency long-term memory and context retrieval system for AdsGency AI. The system must store brand guidelines, past campaign performance logs, audience personas, and operator feedback, enabling autonomous agents to retrieve relevant historical context in under 50 milliseconds to guide campaign strategy.",
        "diagram": """```
=== AGENT LONG-TERM MEMORY & CONTEXT RETRIEVAL SYSTEM ===

[1] Memory Ingestion Pipeline (Campaign Logs, Brand Docs, Feedback)
        │
        ▼
[2] Document Chunking & Embedding Generator (OpenAI text-embedding-3)
        │
        ▼
[3] Hybrid Storage Engine (PostgreSQL + pgvector + HNSW)
        │
        ├── Dense Vector Index (1536-dim HNSW Cosine Distance)
        │
        └── Sparse Keyword Index (PostgreSQL Full-Text Search / GIN)
        │
        ▼
[4] Hybrid Retrieval & Ranker (Reciprocal Rank Fusion / RRF)
        │
        ├── Semantic Distance Filtering
        ├── Metadata Scoping (tenant_id, platform, industry)
        └── Performance Weighting (Historical ROAS Multiplier)
        │
        ▼
[5] Agent Context Assembler (Injected into LLM System Prompt)
```""",
        "functional_requirements": """Autonomous agents are only as smart as the context provided to them. If an agent does not remember that a client's brand strictly avoids aggressive discount language or that visual memes performed poorly for their target demographic last quarter, it will make repetitive, costly mistakes.

The memory system must ingest and index diverse context sources, including brand guidelines, product catalogs, historical campaign performance reports, client feedback notes, and past operator corrections.

When an agent is assigned a task, the memory system must execute a hybrid search to retrieve the most relevant guidelines, historical successes, and negative constraints. The retrieved context must be formatted into clean prompt context windows, enabling the agent to reason from past brand learnings seamlessly.""",
        "non_functional_requirements": """Context retrieval must complete with sub-fifty-millisecond latency so that multi-agent reasoning chains do not suffer compounding delays during interactive planning sessions.

The system must guarantee absolute tenant data isolation. Because memory contains proprietary brand secrets, audience strategies, and performance metrics, under no circumstances can one tenant's memory index be queried or leaked into another tenant's agent prompt.

The storage engine must scale gracefully to millions of memory chunks across thousands of enterprise client organizations while maintaining high vector recall and fast index build times.""",
        "core_entities": """The primary entity is the Memory Item, which represents a chunk of context with its raw text content, tenant identifier, category (such as Brand Rule, Historical Performance, or Audience Persona), and source document reference.

Each memory item has an associated Embedding Record, storing the dense 1536-dimensional vector array indexed using an HNSW index in pgvector.

We also store the Memory Feedback entity, which captures whether an agent's retrieval was helpful or unhelpful based on human operator edits, allowing the system to adjust retrieval weighting over time.""",
        "api_design": """To store new context, the system provides a POST endpoint at api v1 memory items, accepting the raw text, category, metadata tags, and tenant ID, automatically triggering background chunking and embedding generation.

To query memory, agents call a POST endpoint at api v1 memory query, passing their current objective, target platform, and category filters, receiving the top-k most relevant context snippets alongside similarity scores and performance metadata.

For auditability, an operator can inspect an organization's active memory index via a GET endpoint at api v1 memory items, allowing them to review, update, or delete obsolete brand rules and outdated campaign learnings.""",
        "data_flow": """When a new brand document or campaign report is uploaded, an asynchronous ingestion worker splits the text into semantic chunks of roughly three hundred tokens with fifty-token overlaps. The worker calls the embedding API to generate dense vector representations and writes the chunks, metadata, and embeddings into PostgreSQL.

When an autonomous agent prepares to generate an ad campaign, it issues a retrieval query to the memory service containing its prompt and platform scope. The database executes a hybrid search combining dense vector cosine similarity with sparse full-text keyword matching using PostgreSQL's native tsvector.

The results are scored using Reciprocal Rank Fusion, boosted by historical performance multipliers (such as prioritizing chunks associated with high ROAS campaigns). The top five candidate chunks are assembled into a compact context block and injected directly into the agent's prompt context window before inference begins.""",
        "high_level_design": """Our memory architecture is built entirely on PostgreSQL using the pgvector extension, avoiding the operational overhead, synchronization lag, and cost of maintaining a separate external vector database.

The ingestion tier uses FastAPI workers that handle document parsing, semantic chunking, and embedding generation via asynchronous worker queues in Redis.

At the database tier, PostgreSQL hosts both the relational metadata and the high-dimensional vector embeddings, indexed using HNSW for near-instant approximate nearest neighbor searches. A Redis caching layer sits in front of frequent read queries to serve identical context requests in under five milliseconds.""",
        "nfr_deep_dive": """Let's look into how we achieve sub-fifty-millisecond hybrid retrieval and guarantee strict tenant isolation. By leveraging PostgreSQL with HNSW indexes configured with optimized construction parameters (m equals sixteen and ef_construction equals sixty-four), vector similarity lookups execute in roughly fifteen milliseconds even across millions of rows. Combining this with PostgreSQL's native GIN index on full-text search provides robust hybrid retrieval that captures both conceptual meaning and exact keyword matches like brand names and product codes.

Tenant isolation is strictly enforced at the database engine level using Row-Level Security. Every memory query executes within a database transaction where the tenant ID is set in the session context; the query engine physically prunes all rows that do not belong to that tenant before performing the vector distance calculation, mathematically preventing cross-tenant data contamination.

To ensure long-term memory relevance and prevent context pollution from stale data, we implement a memory decay scoring algorithm. Each memory chunk's retrieval score is adjusted by an exponential time-decay factor based on its creation date, while explicit operator feedback applies positive or negative multipliers, ensuring that current brand rules consistently supersede outdated guidelines.""",
    },

    # System Design 6
    {
        "id": 6,
        "title": "Real-Time Campaign Monitoring & Operator Alerting Platform",
        "category": "Observability, Telemetry & Full-Stack Real-Time UI",
        "problem_statement": "Design a real-time campaign observability and alerting platform for AdsGency AI. The system must process real-time click and conversion telemetry, detect performance anomalies (such as sudden CPA spikes or zero-conversion spend), stream live health metrics to a Next.js operator dashboard, and dispatch automated alerts via Slack and email within seconds.",
        "diagram": """```
=== REAL-TIME CAMPAIGN MONITORING & ALERTING PLATFORM ===

[1] Telemetry Stream (Ad Clicks, Spend, Conversions via Kafka)
        │
        ▼
[2] Stream Analytics & Anomaly Detector (Python / Scikit-Learn / Z-Score)
        │
        ├── Normal Metrics ───> [3] In-Memory Time-Series Cache (Redis)
        │                             │
        │                             ▼
        │                       [4] FastAPI Streaming Gateway (SSE / Server-Sent Events)
        │                             │
        │                             ▼
        │                       [5] Operator Live Dashboard (Next.js / React Query)
        │
        └── Anomaly Detected ───> [6] Alert Notification Worker
                                      │
                                      ├─ Slack Webhook Dispatcher
                                      ├─ Email / PagerDuty Dispatcher
                                      └─ Autonomous Agent Mitigation Trigger
```""",
        "functional_requirements": """Marketing operators managing dozens of client campaigns need instant visibility into real-time performance to prevent wasted spend and catch conversion tracking bugs early. The platform must continuously ingest live telemetry from external platforms and compute key operational metrics, including click-through rates, cost per acquisition, and return on ad spend.

The anomaly detection engine must constantly compare incoming performance against expected statistical baselines. If a campaign experiences an abnormal spike in spend without corresponding conversions, or if an ad platform reports widespread delivery drops, the system must flag an anomaly immediately.

The platform must stream live performance metrics and active agent traces directly into an interactive operator dashboard built in Next.js, while dispatching high-priority alerts to external channels like Slack and email so teams can take action immediately.""",
        "non_functional_requirements": """End-to-end alert latency from the moment an anomaly occurs in the telemetry stream to the delivery of a Slack notification must take less than five seconds to protect customer marketing budgets.

The live dashboard streaming connection must maintain low client CPU and memory overhead, supporting hundreds of active operator sessions without server degradation or UI freezing.

The monitoring pipeline must be fault-tolerant and highly available, ensuring that temporary network partitions or worker restarts never miss telemetry events or cause false alarm storms.""",
        "core_entities": """The Campaign Health Metric entity stores aggregated metrics for rolling time windows (one-minute, five-minute, and hourly), including spend, impressions, clicks, conversions, and computed CPA.

The Anomaly Alert Rule entity defines the detection thresholds for each campaign, specifying acceptable variance ranges, baseline metrics, and notification channels.

Finally, the Alert Notification Record logs every triggered alert, the offending metric values, the notification destination, acknowledgment status, and any automated mitigation actions taken by our agents.""",
        "api_design": """The monitoring platform exposes an SSE streaming endpoint at api v1 monitoring campaigns stream, allowing the Next.js frontend to subscribe to live metric updates and agent execution logs using an open HTTP connection.

For alert configuration, an endpoint at api v1 monitoring rules allows operators to create, update, or disable automated alerting thresholds and webhook destinations using standard REST methods.

To acknowledge or resolve an incident, operators issue a POST request to api v1 monitoring alerts resolve with the alert ID and resolution notes, updating the alert status and notifying team members across Slack.""",
        "data_flow": """Raw click and conversion events stream continuously from external webhooks into our Kafka telemetry topic. A stream processing worker consumes events and updates rolling statistical counters in Redis.

Concurrently, an anomaly detection worker evaluates current metric trends against rolling seven-day baselines using statistical z-scores. If a metric deviates beyond three standard deviations, the worker flags an anomaly and pushes an alert event to an internal notification queue.

The alert dispatcher consumes the event and formats structured Slack messages with interactive buttons allowing operators to pause the campaign or approve automated agent mitigation. Simultaneously, the streaming gateway pushes updated metric payloads across open SSE connections to active Next.js dashboard clients.""",
        "high_level_design": """The monitoring architecture is designed around an event-driven streaming pipeline decoupled from our web tier. Ingestion and stream processing are powered by Kafka and Python workers, maintaining hot time-series metrics in Redis.

The frontend communication layer is hosted on FastAPI, using Server-Sent Events to push updates to our Next.js and React dashboard, which leverages React Query and virtualized lists for smooth rendering.

Outbound notifications are managed by asynchronous Celery workers that dispatch messages to external Slack and email APIs, backed by Redis for alert deduplication and rate throttling.""",
        "nfr_deep_dive": """Let's look into how we prevent alert fatigue and maintain smooth UI performance under high event volume. A major risk in real-time monitoring is alert flapping, where an unstable metric repeatedly crosses an alert boundary and floods operators with hundreds of duplicate Slack messages. We resolve this by implementing alert hysteresis and deduplication windows in Redis: once an alert fires for a campaign, subsequent alerts for the same condition are suppressed for thirty minutes unless the severity escalates, while a resolved notification is sent only after the metric remains stable for fifteen consecutive minutes.

On the frontend, streaming thousands of raw telemetry events over WebSockets can quickly degrade browser performance and cause memory leaks. We utilize Server-Sent Events instead of WebSockets because metric monitoring is strictly a unidirectional server-to-client feed, dramatically simplifying connection management across proxies and firewalls. In the React client, updates are throttled using requestAnimationFrame, batching state updates so the UI re-renders at a steady sixty frames per second without stutter.

For anomaly detection, using static thresholds often fails because weekend traffic patterns differ dramatically from weekday peaks. We employ dynamic z-score thresholding based on hour-of-week historical baselines, allowing our anomaly detector to adapt automatically to natural traffic seasonality without triggering false alarms.""",
    },

    # System Design 7
    {
        "id": 7,
        "title": "Distributed Dynamic Bid Optimization & Anomaly Detection Service",
        "category": "Machine Learning & Algorithmic Optimization",
        "problem_statement": "Design an automated, distributed bid optimization service for AdsGency AI that computes optimal cost-per-click (CPC) and target cost-per-acquisition (tCPA) bids across Google, Meta, and TikTok ad auctions in real time, maximizing client ROAS under variable conversion rates and competitive auction dynamics.",
        "diagram": """```
=== DISTRIBUTED DYNAMIC BID OPTIMIZER ===

[1] Campaign Performance Features (CTR, CVR, ROAS, Competitor Density)
        │
        ▼
[2] Feature Engineering Pipeline (Redis Feature Store / PostgreSQL)
        │
        ▼
[3] Bid Optimization Model (Gradient Boosted Trees / Scikit-Learn / PyTorch)
        │
        ├── Predicted CVR & Value Calculation
        │
        ▼
[4] Constraint Solver (Linear Programming / Budget Ceiling & ROAS Target)
        │
        ▼
[5] Anomaly & Guardrail Filter (Max Bid Cap & Rate-of-Change Limit)
        │
        ▼
[6] Dynamic Bid Dispatcher (FastAPI / Outbound Gateway)
        │
        ▼
[7] Ad Platform APIs (Meta, Google, TikTok Ad Set Mutations)
```""",
        "functional_requirements": """In digital advertising auctions, static bidding strategies consistently overpay during low-converting hours and underbid during high-intent conversion spikes. The bid optimization service must analyze real-time and historical campaign signals to determine the mathematically optimal bid for each ad set.

The service must ingest continuous performance features, including device type, placement, geographic location, hour of the day, and historical conversion rates. It calculates expected conversion probability and multiplies it by target transaction value to generate optimal bid recommendations.

Once computed, the service evaluates the proposed bid against client-defined constraints such as maximum CPC caps and minimum ROAS targets. Approved bid adjustments are pushed directly to external ad platform APIs to maintain optimal auction positioning.""",
        "non_functional_requirements": """Bid calculation and mutation dispatch must execute on a scheduled cadence (such as every fifteen minutes per campaign) with high throughput, evaluating thousands of active ad sets within a three-minute execution window.

The system must incorporate strict financial guardrails. Even if a machine learning model predicts an extraordinarily high conversion probability, the service must enforce hard ceilings on bid values and limit the maximum percentage change allowed in a single update to prevent catastrophic spend spikes.

The optimization service must be resilient against missing or delayed telemetry, gracefully falling back to safe historical baseline bids if real-time streaming data is temporarily interrupted.""",
        "core_entities": """The Bid Configuration Profile entity defines the optimization target (such as Maximize Conversions or Target ROAS), allowable bid ranges (minimum and maximum CPC), and pacing aggressiveness.

The Ad Set Feature Vector entity stores the latest computed feature signals, including rolling 24-hour CTR, 7-day CVR, average order value, and competitive auction win rates.

Finally, the Bid Adjustment Event entity records every calculated bid, model confidence score, constraint overrides, external platform response status, and the subsequent change in campaign performance.""",
        "api_design": """Marketing operators configure bidding policies through a PUT endpoint at api v1 bidding campaigns config, specifying target ROAS, maximum bid ceilings, and optimization modes.

To inspect algorithmic decisions, a GET endpoint at api v1 bidding campaigns decisions returns recent bid adjustments, detailing the feature inputs, model predictions, and safety constraints applied to each decision.

An emergency override endpoint accessible via POST at api v1 bidding campaigns reset allows operators to instantly reset all campaign bids back to conservative default values if market conditions behave unpredictably.""",
        "data_flow": """Every fifteen minutes, an orchestration worker queries active campaigns from PostgreSQL and fetches the freshest feature vectors from our Redis feature store.

The feature vectors are passed into our lightweight bid optimization model running in Python using Scikit-Learn and XGBoost. The model predicts the expected conversion rate for the upcoming time window and computes the raw bid value.

The raw bid passes through our constraint solver, which clamps the value within client-specified minimum and maximum limits and restricts the change to no more than twenty percent of the previous bid. The approved bid adjustments are packaged into batch mutation requests and dispatched to Google, Meta, and TikTok APIs via our marketing gateway.""",
        "high_level_design": """The bid optimization architecture utilizes an offline-training and online-inference topology. Model training is executed daily using Apache Airflow pipelines on Amazon EMR or Redshift, training on historical conversion logs and outputting serialized model artifacts to Amazon S3.

Online inference runs inside containerized FastAPI worker pods on AWS EKS, pulling model artifacts from S3 and reading real-time features from a low-latency Redis cluster.

Outbound bid adjustments are distributed across worker pods using Kafka task queues, ensuring parallelized dispatch across hundreds of advertiser accounts without bottlenecking on external network I/O.""",
        "nfr_deep_dive": """Let's look into how we prevent model exploitation and handle cold-start campaigns. Machine learning models in advertising can easily fall victim to feedback loops where an aggressive bid wins more traffic, inflating model confidence and driving bids higher until budgets are exhausted. We prevent this by implementing an exploration-exploitation policy inspired by Upper Confidence Bound algorithms, enforcing a maximum bid change velocity of twenty percent per adjustment cycle. This ensures that bids adjust smoothly and gives the telemetry pipeline ample time to measure the real-world impact of price changes.

For brand new campaigns with zero historical conversion data (the classic cold-start problem), the model cannot accurately predict CVR. In these cases, the service automatically falls back to an industry-vertical benchmark profile derived from aggregated anonymized platform data, applying conservative initial bids until the ad set accumulates at least thirty conversion events.

To guarantee high availability during model service hiccups, the inference workers run behind circuit breakers. If an inference worker experiences latency greater than two seconds or encounters an unhandled exception, the system automatically falls back to deterministic rule-based bidding heuristics stored in Redis, ensuring uninterrupted campaign management.""",
    },

    # System Design 8
    {
        "id": 8,
        "title": "External Ad Platform Webhook Ingestion & Idempotent Sync Pipeline",
        "category": "Event Ingestion, Distributed Queues & Reliability",
        "problem_statement": "Design a bulletproof, high-scale webhook ingestion and reconciliation pipeline for AdsGency AI. The system must ingest millions of webhook notifications from Meta, Google, and TikTok, verify cryptographic signatures, handle bursty traffic surges, deduplicate events, and reconcile internal database state with external platform reality.",
        "diagram": """```
=== WEBHOOK INGESTION & IDEMPOTENT SYNC PIPELINE ===

[1] External Webhooks (Meta, Google, TikTok Events)
        │
        ▼
[2] Serverless Ingestion Edge (AWS Lambda / CloudFront)
        │
        ├── Cryptographic Signature Verification (HMAC-SHA256)
        │
        ▼
[3] Raw Event Buffer (Apache Kafka Topic: 'raw-webhooks')
        │
        ▼
[4] Idempotent Processing Worker Pool (FastAPI / Python)
        │
        ├── Redis Bloom Filter & Deduplication Set (TTL: 24h)
        │
        ▼
[5] State Reconciliation & Mutation (PostgreSQL Ledger)
        │
        ├── Success ───> Update Campaign State & Notify UI
        │
        └── Failure ───> [6] Dead Letter Queue (Kafka DLQ)
                               │
                               ▼
                         [7] Automated Reconciliation Cron (Re-fetch External API)
```""",
        "functional_requirements": """Advertising networks communicate real-time updates—such as ad approvals, policy rejections, budget spend alerts, and billing events—via webhooks. The ingestion pipeline must act as an impenetrable front door that receives, authenticates, and processes these incoming notifications.

The system must verify the cryptographic HMAC signature of every incoming request to guarantee that events originate from legitimate advertising partners and have not been spoofed by malicious actors.

Once validated, the payload must be parsed and processed to update the internal state of campaigns, creatives, and billing records. If an external ad set is rejected due to policy violations, the system must immediately trigger an alert and launch an autonomous agent to remediate the creative copy.""",
        "non_functional_requirements": """The ingestion edge must achieve extreme availability with five nines of uptime and sub-thirty-millisecond response latency. External platforms require webhooks to be acknowledged with an HTTP 200 OK within three seconds; otherwise, they treat the delivery as failed and initiate aggressive retry storms.

The pipeline must handle massive, unpredictable traffic spikes, scaling instantly to absorb tens of thousands of requests per second during major shopping events without dropping payloads or exhausting connection pools.

Data processing must guarantee exactly-once business semantics through robust idempotency, ensuring that duplicated webhook retries never corrupt campaign metrics or trigger repeated downstream actions.""",
        "core_entities": """The Raw Webhook Event entity stores the unparsed JSON payload, platform origin, cryptographic signature header, receipt timestamp, and processing status.

The Event Deduplication Key entity maps the unique platform event ID and entity hash to an expiration timestamp, stored in our Redis caching tier.

The Reconciliation Job entity tracks background consistency audits between internal PostgreSQL state and external platform REST APIs, recording variances, resolved discrepancies, and audit logs.""",
        "api_design": """The ingestion edge exposes public webhook endpoints such as POST at webhooks meta, webhooks google, and webhooks tiktok. Each endpoint verifies signatures and returns an immediate HTTP 200 OK with an empty body within fifteen milliseconds.

For operational visibility, an internal endpoint at api v1 webhooks status provides real-time ingestion rates, consumer lag across Kafka partitions, and dead letter queue depths.

An administrative endpoint at api v1 webhooks redrive allows engineers to re-queue failed events from the Dead Letter Queue back into active processing after resolving downstream bugs.""",
        "data_flow": """An incoming webhook hits our AWS CloudFront distribution and is routed to an AWS Lambda ingestion function. The function calculates the HMAC-SHA256 signature using the platform's secret key and compares it against the request header.

If valid, the Lambda function writes the raw payload directly into an Apache Kafka topic partitioned by advertiser account ID and returns an HTTP 200 OK within twenty milliseconds.

A pool of containerized Python workers on Kubernetes consumes events from Kafka. For each event, the worker checks a Redis Bloom filter and key set for the event ID; if already processed, it drops the duplicate. For new events, the worker applies business logic, updates PostgreSQL records inside a database transaction, and notifies connected clients via Redis Pub/Sub.""",
        "high_level_design": """The architecture utilizes a serverless edge paired with a decoupled event streaming backbone. AWS Lambda provides instant, infinite horizontal scalability for the initial ingestion and signature verification, completely insulating our core servers from external traffic spikes.

Apache Kafka acts as a durable, distributed buffer, decoupling webhook ingestion from downstream database mutations and preventing database connection exhaustion during traffic surges.

Downstream processing is handled by Python workers on AWS EKS that interact with Redis for sub-millisecond deduplication and PostgreSQL for durable state storage, with Kafka Dead Letter Queues catching unparseable payloads.""",
        "nfr_deep_dive": """Let's look into how we achieve zero data loss and resolve eventual consistency discrepancies between our database and external ad networks. Webhooks are inherently unreliable; ad networks occasionally drop events during internal outages or deliver them out of chronological order. We solve this by implementing a two-pronged reconciliation architecture: real-time idempotent stream consumption combined with an asynchronous reconciliation auditor. Every night, an Airflow batch job queries the external ad APIs for the ground-truth state of all active campaigns and compares it against our internal PostgreSQL database. If any discrepancy is detected—such as an ad being paused on Meta directly through their native UI—our system reconciles the local state, logs an audit entry, and notifies operators.

To handle transient failures during stream processing, our workers apply a three-tiered retry policy. If a database deadlock or temporary network glitch occurs, the event is retried with exponential backoff up to three times. If it still fails, the event is routed to a Dead Letter Queue topic in Kafka. An alert is sent to our on-call monitoring channel, and the payload is preserved with full error stack traces for investigation.

Cryptographic verification is performed at the Lambda edge using constant-time string comparison (`hmac.compare_digest`) to prevent timing attacks. Furthermore, our Redis deduplication keys are set with a twenty-four-hour TTL, ensuring bounded memory usage while comfortably covering the maximum retry window used by external advertising platforms.""",
    },

    # System Design 9
    {
        "id": 9,
        "title": "Autonomous Ad Incident Remediation & Self-Healing Agent Pipeline",
        "category": "Autonomous AI Agents & Reliability Engineering",
        "problem_statement": "Design an autonomous incident remediation pipeline for AdsGency AI. When an external platform rejects an ad creative, when tracking pixels fail, or when an ad account encounters a billing error, the system must autonomously diagnose the root cause, synthesize a compliant fix using LLM reasoning agents, and re-deploy the campaign without human intervention.",
        "diagram": """```
=== AUTONOMOUS INCIDENT REMEDIATION PIPELINE ===

[1] Incident Trigger (Ad Disapproval Webhook / Anomaly Detector)
        │
        ▼
[2] Incident Triage Agent (FastAPI / LangGraph)
        │
        ├── Parse Platform Error Code (e.g., Meta Policy 148: Creative Text)
        │
        ▼
[3] Root Cause Diagnosis Agent (Context Retrieval / Policy Database)
        │
        ▼
[4] Creative Remediation Agent (LLM Fix Synthesis & Guardrail Check)
        │
        ├── Generates Compliant Copy Alternative
        │
        ▼
[5] Policy Verification Gate (Semantic Safety Check)
        │
        ├── Safe ───> [6] Auto-Redeployment (Marketing API Gateway)
        │
        └── High-Risk Violation ───> [7] Human-in-the-Loop Escalation (Slack Alert)
```""",
        "functional_requirements": """In digital marketing, ad rejections happen constantly due to strict platform policies regarding wording, capitalization, image text ratios, and prohibited keywords. A human team takes hours or days to notice a rejection, edit the creative, and resubmit it, causing significant missed revenue.

The incident remediation pipeline must automatically ingest rejection notifications from Google, Meta, and TikTok webhooks. It parses the platform-specific error code and policy violation details to classify the root cause.

The remediation agent retrieves the offending ad creative, cross-references our vector policy database, and uses an LLM to synthesize compliant alternatives that preserve the original marketing intent while strictly satisfying platform guidelines. If the fix passes safety checks, the agent automatically redeploys the updated ad set.""",
        "non_functional_requirements": """The autonomous remediation cycle should diagnose, rewrite, and resubmit rejected ad creatives within ninety seconds of receiving the rejection webhook, minimizing lost campaign flight time.

Remediation must be safe and conservative. If an incident involves serious account-level suspensions or ambiguous copyright violations, the agent must recognize its limitations and immediately escalate the issue to a human operator rather than making speculative edits.

Every remediation action must be fully logged and explainable, providing human operators with a clear before-and-after diff and the exact reasoning rationale used by the agent.""",
        "core_entities": """The Incident Record entity stores the campaign identifier, platform name, raw platform error code, violation category, timestamp, and active status (Diagnosing, Remediating, Deployed, or Escalated).

The Remediation Plan entity captures the agent's diagnostic explanation, the original creative text, the proposed compliant alternative, and confidence scores.

The Policy Rule Reference entity contains platform-specific advertising policies and negative constraint patterns indexed in our vector database for fast semantic retrieval.""",
        "api_design": """An operator can view all active and historical incidents via a GET endpoint at api v1 incidents, filtered by status, platform, or severity.

To review an autonomous remediation plan, a GET endpoint at api v1 incidents remediation returns the before-and-after diff, agent rationale, and platform compliance score.

If a human operator wishes to intervene, a POST endpoint at api v1 incidents override allows them to approve, reject, or manually edit the agent's proposed remediation before deployment.""",
        "data_flow": """An ad rejection webhook arrives from Meta indicating that an ad was disapproved under Policy 148 for misleading text claims. The webhook triggers an incident workflow in our FastAPI service, which creates an incident record in PostgreSQL.

The Incident Triage Agent analyzes the rejection code and queries pgvector for specific policy rules and compliant historical examples for that category. The Remediation Agent prompts an LLM with the original text, the specific policy constraint, and instructions to generate an alternative that preserves the marketing value proposition.

The new creative passes through an automated safety verification gate. If the confidence score is above ninety percent, our marketing gateway dispatches a mutation to update the ad creative on Meta and logs the resolution to Slack; if confidence is low, it halts and pings an operator.""",
        "high_level_design": """The remediation engine is built as an asynchronous agentic microservice utilizing LangGraph for stateful multi-step reasoning. It is integrated directly with our webhook ingress tier and our marketing API gateway.

The policy database and historical remediation logs are indexed in PostgreSQL using pgvector, enabling fast semantic matching against obscure platform policy guidelines.

Communication with human operators is facilitated through interactive Slack apps and the Next.js dashboard, allowing operators to oversee autonomous self-healing actions seamlessly.""",
        "nfr_deep_dive": """Let's examine how we enforce safe agent boundaries and prevent remediation thrashing. Remediation thrashing occurs when an agent submits a fix, the platform rejects it for a different policy reason, and the agent enters an infinite submit-and-reject loop that risks triggering account-level penalties. We eliminate this by enforcing a strict maximum retry ceiling: an autonomous agent is permitted a maximum of two automated remediation attempts per ad creative. If the second attempt fails, the workflow immediately locks the ad and escalates the ticket to a human manager.

To guarantee high-quality copy revisions, the remediation prompt uses chain-of-thought reasoning with explicit negative constraints. The agent is forced to explicitly state which words in the original ad triggered the rejection and why the proposed substitute resolves the violation without diluting the call-to-action.

All remediation history is logged into an immutable append-only audit trail in PostgreSQL. This allows engineering and marketing teams to run weekly evaluation benchmarks, identifying recurring rejection patterns across platforms and updating our core prompt guidelines to prevent future rejections before campaigns ever launch.""",
    },

    # System Design 10
    {
        "id": 10,
        "title": "Multi-Tenant Enterprise Security & Audit Vault",
        "category": "Enterprise Security, Auth & Compliance",
        "problem_statement": "Design a zero-trust, multi-tenant enterprise security architecture and audit vault for AdsGency AI. The system must enforce strict data isolation across enterprise clients, secure OAuth credentials and API keys using envelope encryption, manage granular role-based access control (RBAC), and maintain an immutable append-only audit ledger compliant with SOC 2, HIPAA, and GDPR standards.",
        "diagram": """```
=== MULTI-TENANT ENTERPRISE SECURITY & AUDIT VAULT ===

[1] Client Request (Human Operator / Agent Worker)
        │
        ▼
[2] API Gateway & Security Interceptor (FastAPI / OAuth 2.0 / JWT)
        │
        ├── Extract Tenant Context & Role Claims (RS256 JWT)
        │
        ▼
[3] Policy Enforcement Point (Casbin / OPA / RBAC Engine)
        │
        ├── Authorized ───> [4] Database Layer with Row-Level Security (PostgreSQL RLS)
        │                         │
        │                         ├── Tenant Context Injected (`SET LOCAL app.current_tenant_id`)
        │                         └── Envelope Encryption for Secrets (AWS KMS)
        │
        └── Audit Logger ───> [5] Immutable Append-Only Audit Vault (Amazon S3 / WORM / QLDB)
```""",
        "functional_requirements": """As AdsGency AI expands into enterprise marketing accounts, clients demand uncompromising guarantees that their proprietary marketing data, ad budgets, customer audience lists, and API credentials are completely secure and isolated from other tenants.

The security vault must authenticate human operators and automated agents using OAuth 2.0 and cryptographically signed JWT tokens, enforcing granular Role-Based Access Control (RBAC) across roles such as Admin, Marketing Operator, Financial Auditor, and Read-Only Viewer.

The platform must securely store sensitive third-party credentials—such as Google Ads and Meta Graph API refresh tokens—using modern envelope encryption. Furthermore, every single read, write, and agent-driven mutation must be recorded in an immutable, tamper-evident audit ledger.""",
        "non_functional_requirements": """Authentication and authorization checks must introduce less than five milliseconds of latency to every internal and external API request, ensuring zero perceptible performance overhead.

Tenant data isolation must be mathematically guaranteed at the storage engine level, preventing software bugs or omitted WHERE clauses in application queries from ever exposing cross-tenant records.

The audit log must satisfy strict SOC 2 Type II, GDPR, and HIPAA compliance requirements, featuring tamper-evident verification, immutable storage, and automated log retention policies.""",
        "core_entities": """The Tenant Organization entity defines the enterprise client account, subscription tier, active status, and security compliance configuration.

The User & Role Mapping entity associates individual human users or service accounts with specific roles and permission scopes within an organization.

The Encrypted Credential Vault entity stores third-party OAuth tokens, client secrets, and webhook signing keys, referencing the unique AWS KMS Key ID and encrypted data key used for envelope encryption.

Finally, the Immutable Audit Event entity records every system action, capturing timestamp, actor ID, IP address, tenant ID, action type, resource identifier, previous state, and mutated state.""",
        "api_design": """Authentication is managed through standard OAuth routes at auth token, issuing cryptographically signed RS256 JWT tokens containing tenant ID and permission claims.

For user management, administrative endpoints at api v1 orgs users allow administrators to invite team members, assign RBAC roles, and revoke active sessions immediately.

Compliance officers access the audit vault via a GET endpoint at api v1 audit logs, allowing filtered searches by actor, resource, date range, or action type, with export capabilities to signed CSV files.""",
        "data_flow": """When an operator or agent submits an API request, the FastAPI security dependency extracts and verifies the RS256 JWT token using our public signing key. The tenant ID and role claims are verified against the route's required permissions.

Upon authorization, the database connection pool checks out a connection and immediately sets the local tenant context by executing a parameterized query. PostgreSQL Row-Level Security policies automatically apply to all subsequent queries on that connection.

When third-party API credentials are needed, the service calls AWS KMS to decrypt the envelope data key in memory, decrypts the token, and dispatches the external API call. Simultaneously, an asynchronous event worker records the action details into our audit ledger, signing the entry with a cryptographic hash chain.""",
        "high_level_design": """The security architecture follows a zero-trust model implemented across the API gateway, application runtime, and database tiers. FastAPI acts as the Policy Enforcement Point, verifying JWT claims before requests reach business logic.

Data isolation is enforced at the database tier using native PostgreSQL Row-Level Security (RLS), ensuring that isolation does not rely solely on application developers remembering to include tenant filters in SQL queries.

Secrets management leverages AWS Key Management Service (KMS) for envelope encryption, while audit logs are streamed to Amazon S3 Object Lock storage configured in Write Once, Read Many (WORM) compliance mode.""",
        "nfr_deep_dive": """Let's look into how we achieve tamper-evident audit logging and mathematically enforced tenant isolation. In standard web applications, a junior developer forgetting a tenant WHERE clause in a raw SQL query can cause a catastrophic data breach. We eliminate this vulnerability entirely by enabling Row-Level Security on every table in PostgreSQL: policies like `CREATE POLICY tenant_isolation ON campaigns USING (tenant_id = current_setting('app.current_tenant_id'))` ensure that the database engine itself rejects access to any row belonging to a different tenant, regardless of how the application query was constructed.

For secrets storage, storing plaintext credentials in the database or relying on basic environment variables is unacceptable for enterprise compliance. We implement envelope encryption with AWS KMS: each tenant's credentials are encrypted using a unique AES-256 data encryption key, which is itself encrypted under a master customer-managed key in KMS. Decryption occurs only in ephemeral worker memory, and plaintext keys are never written to disk or logs.

Our audit vault uses cryptographic hash chaining similar to a blockchain ledger. Each audit log entry includes the SHA-256 hash of the preceding entry in the chain. These logs are streamed to an Amazon S3 bucket with Object Lock enabled in Compliance Mode, which legally and technologically prevents any user—including AWS root accounts—from altering, overwriting, or deleting log files for a mandated retention period of seven years, effortlessly passing SOC 2 and GDPR compliance audits.""",
    }
]
