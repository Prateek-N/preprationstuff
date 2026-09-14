# Oscar Health — Senior Fullstack Software Engineer Interview Master Preparation Guide
**Candidate:** Ashutosh Rudraksh  
**Target Role:** Senior Software Engineer, Fullstack — Oscar Health (Hudson Square, NYC / Hybrid)  
**Compensation Benchmark:** $163,944 - $215,176 + Equity + Unlimited PTO  
**Platform Core Mission:** "A doctor in the family" — Building a full-stack, member-centric healthcare platform, scalable claims engines, and provider integrations.

---

# TABLE OF CONTENTS
1. [PART 1: Technical & Behavioral Deep Dive (Top 20 Questions)](#part-1-technical--behavioral-deep-dive-top-20-questions)
2. [PART 2: Top 15 Data Structures & Algorithms (Coding Round)](#part-2-top-15-data-structures--algorithms-coding-round)
3. [PART 3: System Design Masterclass (HLD & LLD with Healthcare Deep Dives)](#part-3-system-design-masterclass-hld--lld-with-healthcare-deep-dives)
   - [3.1 Expanded System Design Interview Guide & Healthcare Nuances](#31-expanded-system-design-interview-guide--healthcare-nuances)
   - [3.2 Top 5 High-Level System Designs (HLD)](#32-top-5-high-level-system-designs-hld)
   - [3.3 Top 5 Low-Level System Designs (LLD / OOD)](#33-top-5-low-level-system-designs-lld--ood)

---

# PART 1: Technical & Behavioral Deep Dive (Top 20 Questions)
*Each answer is structured in the STAR format (~300 words), tailored specifically to Ashutosh's real-world experience at Uber, Meta, Tekainos, and Dell Technologies, highlighting critical competencies required by Oscar Health.*

---

### Q1: Tell me about yourself, your background, and why you are excited about Oscar Health.
**Category:** Background & Fit  
**Situation:** Over the past four years, I have engineered high-throughput distributed systems, fullstack microservices, and AI-enabled infrastructure across hyper-growth environments including **Uber**, **Meta Reality Labs**, **Tekainos**, and **Dell Technologies**, complemented by an M.S. in Computer Science from **The Ohio State University**.  
**Task:** My focus has always centered on bridging robust backend microservices with intuitive consumer-facing interfaces, ensuring strict system reliability, data fidelity, and seamless user experiences.  
**Action:** At **Uber**, I led the development of a fullstack internal query resolution platform utilizing **FastAPI**, **React**, and **TypeScript**, integrating semantic search over **PostgreSQL** and **pgvector** across 180K+ records. At **Dell Technologies**, I modernized legacy banking and enterprise workflows using **Java 17**, **Spring Boot**, and **Kafka**, achieving a 55% query latency drop and 99.9% uptime. At **Tekainos**, I architected automated asynchronous ETL pipelines using **FastAPI**, **AWS Lambda**, and **Redis**, slashing processing times from 24 hours to minutes. Throughout this journey, I prioritized cross-functional collaboration with product managers, clinical/domain stakeholders, and DevOps engineers.  
**Result:** Oscar Health's mission to act like "a doctor in the family" resonates deeply with me. Healthcare in the United States is fraught with opaque pricing, complex insurance claims, and fragmented care pathways. I want to leverage my fullstack expertise in **TypeScript**, **Python**, **FastAPI**, and event-driven **Kafka** architectures to make healthcare transparent, empathetic, and friction-free for millions of Oscar members and providers.

---

### Q2: Oscar emphasizes building reliable systems for members and providers. Tell me about a time you owned a complex technical project from design through release.
**Category:** Technical Ownership & Execution  
**Situation:** At **Uber**, internal operations and employee support specialists faced fragmented workflows when diagnosing member and employee queries across disparate repositories, causing high turnaround times and low resolution accuracy.  
**Task:** I was tasked with leading the end-to-end design, implementation, and deployment of a unified query resolution platform from scratch, capable of handling thousands of multi-modal requests daily with sub-second response times.  
**Action:** I spearheaded the technical architecture by decoupling the presentation layer from the data ingestion pipelines. I implemented the frontend in **React** and **TypeScript**, crafting a modular interface with type-safe state management. On the backend, I built a high-performance **FastAPI** service containerized with **Docker** and orchestrated on **Kubernetes (EKS)**. To solve unstructured search limitations, I engineered a semantic search pipeline using **PostgreSQL** with the **pgvector** extension, indexing 180,000+ complex documents. I set up automated **CI/CD** pipelines via **GitHub Actions**, integrating unit tests, end-to-end integration tests, and **AWS CloudWatch** synthetic monitoring to track p99 latencies.  
**Result:** The platform successfully handled **3,500+ requests** during initial rollout and settled into **6,000+ daily requests** with **99.5% uptime**. Search accuracy improved by **38%**, and resolution relevance surged by **45%**. I delivered this project on time by partnering closely with data science and product teams.

---

### Q3: Oscar requires engineers to perform step-wise technical migrations of legacy services. Describe a time you executed a migration without downtime.
**Category:** System Migration & Legacy Modernization  
**Situation:** At **Dell Technologies**, our core customer service and order tracking modules were running on a legacy monolithic architecture with tightly coupled database transactions. This setup was suffering from locking contentions and high database query latency across 10+ modules.  
**Task:** I owned the technical migration plan to decompose the monolithic data-access layer into decoupled **Spring Boot** microservices backed by **PostgreSQL**, requiring zero downtime for live business operations.  
**Action:** I applied the **Strangler Fig pattern**. First, I introduced an abstraction layer with an API gateway to route traffic incrementally. I implemented the **Outbox Pattern** using **Kafka** to mirror live database writes asynchronously from the old schema into the new PostgreSQL tables. I validated data integrity by writing automated shadow-comparison scripts in **Python** that ran in the background, comparing production responses from both systems without returning the shadow output to the client. Once parity reached 100% over two consecutive weeks, I gradually shifted read traffic using weighted routing (10%, 25%, 50%, 100%). Finally, I migrated write traffic using distributed transactions and idempotency keys.  
**Result:** The migration executed with **zero downtime** and zero data loss. The optimized schema and Hibernate configurations reduced overall database query latency by **55%**, while inter-service communication bottlenecks fell by **35%**, enabling our team to release features 40% faster.

---

### Q4: Tell me about a time you handled a critical production outage or severe performance regression.
**Category:** Production Debugging & Incident Management  
**Situation:** At **Tekainos**, during peak month-end financial reconciliations, our backend services experienced severe latency spikes where API response times degraded from 200ms to over 30 seconds, leading to cascading HTTP 504 Gateway Timeouts across automated accounting workflows.  
**Task:** As the on-call engineer, I had to immediately triage the root cause, mitigate customer impact, restore normal system throughput, and establish safeguards against future recurrences.  
**Action:** I inspected **AWS CloudWatch** metrics and distributed traces, observing an exponential surge in thread starvation across our **FastAPI** worker nodes. Deep analysis of our **PostgreSQL** slow query logs revealed an un-indexed multi-table join executed concurrently by scheduled **Lambda** ETL workers against our primary transactional database. To stop the bleed, I immediately applied a rate-limiting circuit breaker using **Redis** to throttle bulk analytical queries. Next, I spun up an **AWS RDS Read Replica** and redirected all read-heavy reporting and OCR normalization jobs away from the primary transactional instance. Finally, I added compound B-tree indexes on `(tenant_id, transaction_timestamp, status)` and tuned the connection pool sizing using **PgBouncer**.  
**Result:** P99 response times returned to **under 150ms** within 45 minutes of incident declaration. I subsequently authored a blameless post-mortem, mandated read-replica routing for all analytics, and introduced synthetic database load tests into our **GitHub Actions** CI pipeline.

---

### Q5: How do you collaborate with non-technical stakeholders (Product Managers, Clinical Specialists, Operations) to solve ambiguous problems?
**Category:** Cross-Functional Collaboration  
**Situation:** At **Meta (Reality Labs)**, leadership requested an automated evaluation framework to test how spatial agents perceived and interacted with simulated environments. The prompt from research scientists was highly ambiguous: "Make the spatial agent reason accurately without breaking user immersion."  
**Task:** I had to translate broad, exploratory research goals into tangible, testable software engineering specifications and reproducible API contracts.  
**Action:** I scheduled structured discovery workshops with researchers, product managers, and QA specialists. Rather than discussing abstract ML models, I focused on user journeys: What constitutes an unacceptable failure in an AR/VR environment? Together, we defined concrete acceptance criteria: collision avoidance latency, token budget constraints, and tool invocation accuracy. To bridge the gap, I designed modular **MCP (Model Context Protocol)** servers using **FastAPI** and **Node.js** that exposed clear JSON schemas for perception, evaluation, and logging. I provided product managers with an intuitive dashboard where they could inspect live simulation traces and flag edge cases without writing code.  
**Result:** This collaboration eliminated **70% of manual testing efforts** and boosted system test reliability by **28%**. The modular API layer accelerated team feature integration speed by **50%**, enabling Reality Labs leadership to greenlight the project for extended production development.

---

### Q6: How do you design APIs that handle high throughput, maintain sub-second latency, and ensure strict backward compatibility?
**Category:** API Design & Systems Engineering  
**Situation:** At **Tekainos**, our cross-service messaging was initially fragmented across ad-hoc HTTP endpoints, leading to brittle integrations, contract mismatches, and frequent inter-service communication failures when onboarded partners sent divergent payloads.  
**Task:** I needed to architect a robust, backward-compatible API layer capable of handling bursty traffic with strict schema validation and minimal serialization overhead.  
**Action:** I adopted a contract-first API design. For high-volume inter-service synchronous communication, I instituted **gRPC** with **Protocol Buffers**, strictly enforcing backward compatibility rules (never renumbering field tags, using optional fields, and reserving deprecated tags). For external and client integrations, I engineered RESTful endpoints using **FastAPI** and **Pydantic v2**, taking advantage of compiled type validation and automatic OpenAPI documentation. I implemented deterministic versioning in the URI path (`/api/v1/`), integrated **gzip/brotli compression**, and introduced **Redis** cache-aside mechanisms for read-intensive entity lookups with sub-5ms latency. Furthermore, I enforced idempotency keys in HTTP request headers (`Idempotency-Key: <UUID>`) for all state-mutating POST/PUT endpoints.  
**Result:** Inter-service failures dropped by **40%**, average API response latencies stayed below **80ms**, and partner onboarding time plummeted from **6 weeks down to 2 days** due to self-documenting, resilient API contracts.

---

### Q7: Tell me about a time you had a technical disagreement with a team member. How did you resolve it?
**Category:** Conflict Resolution & Technical Influence  
**Situation:** At **Dell Technologies**, during the redesign of our asynchronous event notification pipeline, a senior engineer strongly advocated using synchronous REST calls with aggressive retry policies between our microservices to keep the architecture "simple" and avoid introducing new message broker overhead.  
**Task:** I recognized that synchronous HTTP chaining across five microservices during peak order spikes would create tight coupling, cascading failures, thread pool exhaustion, and unpredictable latency spikes. I needed to advocate for an event-driven architecture using **Kafka** diplomatically and backed by empirical evidence.  
**Action:** Rather than engaging in an ideological debate, I built a quick proof-of-concept simulation using **Python** and **Locust** to load-test both paradigms under 10,000 concurrent requests with simulated network jitter. The test results demonstrated that the REST-based chaining suffered a 28% failure rate due to connection timeouts, whereas the **Kafka** message broker ingested 100% of events asynchronously with zero loss. I presented the findings in a team design review, emphasizing how Kafka's dead-letter queues (DLQ) and consumer group offsets would give us built-in replayability and isolation without complicating the client interface.  
**Result:** The senior engineer appreciated the empirical data and backed the approach. We implemented the **Kafka** event pipeline, which reduced inter-service communication bottlenecks by **35%** and processed over **10,000 daily requests** seamlessly.

---

### Q8: Healthcare requires strict adherence to HIPAA, PHI privacy, and data security. How have you implemented security and compliance in your architectures?
**Category:** Security, Privacy & Compliance  
**Situation:** At **Tekainos**, we extracted, normalized, and stored highly sensitive financial and identity records from over 5,000+ unstructured documents via OCR, requiring strict adherence to data privacy standards equivalent to **SOC 2** and **HIPAA** compliance.  
**Task:** I was responsible for securing the end-to-end data pipeline to ensure that personally identifiable information (PII) was never exposed in logs, leaked across tenants, or stored unencrypted.  
**Action:** I enforced defense-in-depth security principles across the software lifecycle. First, I configured **AES-256** encryption at rest on **PostgreSQL (AWS RDS)** and **S3 buckets**, and mandated **TLS 1.3** for all data in transit. Second, I introduced an automated data-sanitization middleware in **FastAPI** that intercepted incoming payloads and redacting sensitive fields (Social Security numbers, bank account numbers, names) before writing to application log streams in **CloudWatch**. Third, I implemented role-based access control (**RBAC**) and least-privilege policies through **AWS IAM** and JWT claims verification. Finally, I partitioned our database using tenant-isolated schemas to eliminate cross-tenant data leakage risks, and integrated automated dependency vulnerability scanning using **Snyk** in our **GitHub Actions** CI pipeline.  
**Result:** The pipeline normalized over 5,000+ documents with zero security leaks or compliance breaches, while improving data quality by **38%**. This rigorous foundation prepared the company to pass its third-party security audit seamlessly.

---

### Q9: Tell me about a time you experimented with a new or bleeding-edge technology to solve a real business problem.
**Category:** Innovation & Pragmatic Experimentation  
**Situation:** At **Meta Reality Labs**, evaluating vision-language-action (**VLA**) agents across 3D simulation environments was bottlenecked by brittle, ad-hoc Python testing scripts. Engineers were manually inspecting agent trajectories, which delayed deployment cycles and consumed valuable research bandwidth.  
**Task:** I wanted to explore whether the newly emerging **Model Context Protocol (MCP)** and structured LLM tool-calling could be adapted into a standardized, plug-and-play evaluation pipeline for our embodied AI workflows.  
**Action:** Over a two-week sprint, I designed an experimental MCP server architecture using **FastAPI**, **Node.js**, and **Docker**. I encapsulated environmental observation tools, spatial collision detectors, and trajectory verifiers as standardized MCP tools with explicit JSON schemas. This allowed LLMs and VLA models to dynamically query spatial metrics, execute verification actions, and report regression anomalies autonomously. I benchmarked this against our existing test harness, ensuring that the token overhead and latency of LLM calls did not exceed our simulation frame budgets.  
**Result:** The experiment was a resounding success. It slashed manual testing efforts by **70%**, increased automated anomaly detection by **28%**, and supported 6+ simulation configurations. I demoed the working architecture to Reality Labs leadership, who greenlit it as a standard testing harness across our spatial computing division.

---

### Q10: Oscar operates a high-volume platform with real-time eligibility checks and claims. How do you design and scale event-driven microservices using Kafka?
**Category:** Distributed Systems & Event-Driven Architecture  
**Situation:** At **Dell Technologies**, our enterprise order processing system required real-time orchestration across billing, inventory, and notification services. During promotional events, synchronous API calls triggered database thread deadlocks and dropped notifications.  
**Task:** I was tasked with designing and implementing an asynchronous event-driven backbone using **Apache Kafka** and **Spring Boot** to decouple services and guarantee message delivery during traffic spikes.  
**Action:** I designed partitioned Kafka topics with strategic partition keys (such as `account_id` or `order_id`) to ensure strict in-order processing per entity while scaling consumer concurrency horizontally. To prevent dual-write inconsistencies between the local database and Kafka, I implemented the **Transactional Outbox Pattern**: domain mutations and outbound events were written atomically to PostgreSQL in a single database transaction, after which a background worker relayed the events to Kafka. On the consumer side, I enforced **idempotent message processing** by storing processed event IDs in a **Redis** cache with a TTL. I also implemented a **Dead Letter Queue (DLQ)** with exponential backoff retries to isolate poison-pill messages without halting partition consumption.  
**Result:** The event-driven architecture processed **10,000+ daily events** seamlessly, eliminated communication bottlenecks by **35%**, and maintained **99.9% service availability** during peak traffic without a single dropped transaction.

---

### Q11: Tell me about a time you mentored junior engineers or drove engineering best practices across your team.
**Category:** Leadership & Mentorship  
**Situation:** At **Dell Technologies**, our team grew rapidly with the onboarding of four junior software engineers. Code reviews were inconsistent, unit test coverage was hovering below 50%, and merge conflicts in Git were frequently blocking staging deployments.  
**Task:** As an experienced engineer, I took the initiative to establish structured engineering standards, improve automated testing hygiene, and mentor junior colleagues to elevate overall code quality.  
**Action:** I instituted weekly technical lunch-and-learns focusing on **SOLID principles**, clean architecture in **Spring Boot**, and practical test-driven development (**TDD**). I created a comprehensive PR review checklist and configured pre-commit hooks and **GitHub Actions** workflows that enforced code formatting (**Checkstyle/Black**), static analysis (**SonarQube**), and a mandatory **80% code coverage threshold** via **JUnit** and **Mockito**. Furthermore, I set up bi-weekly 1-on-1 pair-programming sessions with junior engineers, teaching them how to profile slow database queries with **EXPLAIN ANALYZE** and how to write clean, modular abstractions rather than monolithic controllers.  
**Result:** Within four months, production defect escape rates dropped by **30%**, test coverage surpassed **85%**, and junior engineers were able to independently own and ship production features with minimal senior oversight.

---

### Q12: How do you approach database performance tuning, indexing strategies, and scaling when query latencies degrade?
**Category:** Database Optimization & Scaling  
**Situation:** At **Dell Technologies**, our analytical and reporting dashboards experienced severe latency degradation (queries taking 8–12 seconds) across 10+ core database modules as our PostgreSQL transaction tables surpassed millions of rows.  
**Task:** I was assigned to diagnose the root causes of the degradation and optimize database performance without restructuring the entire application.  
**Action:** I systematically audited the **PostgreSQL slow query logs** and ran `EXPLAIN (ANALYZE, BUFFERS)` on the slowest queries. I discovered two primary issues: pervasive sequential table scans caused by missing composite indexes, and severe N+1 query patterns generated by misconfigured **Hibernate JPA** entity mappings. I resolved the N+1 queries by rewriting ORM fetches to use explicit `JOIN FETCH` queries and batch fetching (`hibernate.default_batch_fetch_size = 30`). Next, I introduced targeted B-tree composite indexes aligned with query filter cardinalities and created partial indexes for active records (`WHERE status = 'ACTIVE'`). For high-volume audit logs, I implemented range-based table partitioning by month. Finally, I optimized connection pooling settings via **HikariCP**.  
**Result:** Average database query latency dropped by **55%**, CPU utilization on our database instances decreased by **40%**, and downstream dashboard load times plummeted from 10s to sub-800ms.

---

### Q13: In a fast-paced environment, how do you balance paying down technical debt against delivering new product features?
**Category:** Pragmatic Prioritization & Technical Debt  
**Situation:** At **Tekainos**, our startup needed to ship automated scheduling features rapidly to close enterprise client deals, but our core scheduling service was built on brittle, hard-coded rules that made adding new client constraints increasingly prone to regression bugs.  
**Task:** I had to balance the business imperative to ship client-facing features quickly with the technical necessity of refactoring the core scheduling engine to prevent a maintenance deadlock.  
**Action:** Rather than halting feature development for an unrealistic "full rewrite," I proposed an incremental refactoring strategy to the product manager. I quantified the cost of technical debt in terms of delivery velocity: each new constraint was taking twice as long to ship because of legacy bugs. I negotiated a **20% technical debt allocation** into each two-week sprint. During feature work, I applied the **Boy Scout Rule**: whenever we touched a module to add a feature, we refactored that specific path, decoupled business logic into a clean **Strategy Pattern**, and wrapped it in comprehensive unit tests.  
**Result:** Over three sprints, we completely modernized the scheduling engine without missing a single client deadline. As a result, manual data entry was slashed by **85%**, system latency dropped from 24 hours to minutes, and future feature turnaround times accelerated dramatically.

---

### Q14: Describe your experience building fullstack applications. How do you ensure clean contracts between React/TypeScript and Python/FastAPI?
**Category:** Fullstack Architecture & Type Safety  
**Situation:** At **Uber**, our internal employee query resolution system required a responsive, intuitive frontend in **React** and **TypeScript** coupled with a high-performance, asynchronous backend in **Python (FastAPI)** handling vector search and LLM orchestration.  
**Task:** I needed to ensure end-to-end type safety, prevent runtime contract mismatches between frontend and backend, and provide an ultra-responsive UI for employee operations.  
**Action:** I established an automated contract-driven development workflow. In **FastAPI**, I defined strict request and response schemas using **Pydantic v2**. I integrated an automated OpenAPI generation script in our CI pipeline that exported the API specifications as a `schema.json` file on every build. On the frontend, I used `openapi-typescript` to generate strict **TypeScript** interfaces directly from that schema, ensuring that any backend property renaming or type change would immediately trigger compile-time errors on the frontend. In React, I utilized **React Query (TanStack Query)** for optimistic UI updates, background caching, and automatic deduplication of network requests. For real-time updates, I established WebSocket connections managed cleanly through custom React hooks.  
**Result:** The platform rolled out to **3,500+ users** with zero runtime API contract mismatches. The UI delivered instant sub-100ms perceived latency due to client-side caching, achieving high adoption and user satisfaction.

---

### Q15: Tell me about a time a project failed, fell behind schedule, or did not meet expectations. What did you learn?
**Category:** Resilience, Failure & Retrospective  
**Situation:** Early in my time at **Tekainos**, I designed an OCR data extraction pipeline intended to parse complex medical and accounting invoices. I initially selected an off-the-shelf open-source OCR library without sufficiently testing it against highly degraded, skewed, and handwritten scanned PDFs.  
**Task:** When we deployed the pipeline to staging against real customer documents, the extraction accuracy fell below 60%, far below our 90% business acceptance threshold, threatening our release timeline.  
**Action:** I immediately took ownership of the miscalculation and communicated the roadblock transparently to our engineering lead and product manager. Rather than stubbornly trying to patch an inadequate library, I conducted a rapid 48-hour spike evaluating alternative solutions. I redesigned the ingestion pipeline into a multi-stage hybrid architecture: using **OpenCV** for image pre-processing (deskewing, contrast normalization, noise removal), followed by a cloud-based vision model for raw OCR text extraction, and finally a **FastAPI** validation service that used regular expressions and schema heuristics to normalize unstructured entities into **PostgreSQL**.  
**Result:** The revised pipeline successfully normalized data from **5,000+ unstructured documents**, boosting accuracy to **94%** and overall data quality by **38%**. The key takeaway was to validate edge cases against realistic production data early during discovery rather than assuming library benchmarks apply universally.

---

### Q16: Oscar is exploring AI/LLM applications to assist care guides and members. Describe your real-world experience deploying production AI/RAG systems.
**Category:** AI/LLM Systems & Production Engineering  
**Situation:** At **Uber**, employees spent significant time searching through fragmented internal documentation, wikis, and policies to resolve employee inquiries, leading to delayed resolutions.  
**Task:** I was tasked with engineering an accurate, low-latency semantic search and Retrieval-Augmented Generation (**RAG**) pipeline capable of querying 180,000+ institutional records while mitigating hallucinations and maintaining strict access control.  
**Action:** I architected the semantic search pipeline using **FastAPI**, **PostgreSQL**, and the **pgvector** extension. I chunked long documents into semantic paragraphs using sliding-window tokenizers and generated embeddings using sentence-transformer models. To achieve low latency, I implemented an **HNSW (Hierarchical Navigable Small World)** index in pgvector, which enabled sub-50ms approximate nearest neighbor search across 180K+ embeddings. I integrated a hybrid search ranking strategy combining dense vector similarity with traditional **BM25 full-text search** to preserve exact keyword recall (such as policy IDs). Finally, I introduced a cross-encoder reranking step and strict prompt engineering templates that instructed the LLM to ground answers strictly in retrieved source context, citing document URLs.  
**Result:** The system improved response relevance by **45%** and search accuracy by **38%**. It served **6,000+ daily requests** with **99.5% uptime**, drastically reducing support ticket resolution times.

---

### Q17: Why do you want to join Oscar Health specifically at this stage of your career?
**Category:** Company Motivation & Healthcare Mission  
**Situation:** Having engineered high-scale distributed systems at **Dell** and **Uber**, and cutting-edge agentic workflows at **Meta**, I evaluated where my engineering contributions would deliver the highest societal and user impact over the next five years.  
**Task:** I sought a role at a tech-first organization tackling complex, high-stakes human problems where fullstack engineering excellence directly improves people's lives.  
**Action:** Oscar Health stands out as the pioneer in rebuilding health insurance from the ground up as a modern software platform. Unlike legacy payers whose systems are locked in 40-year-old mainframes, Oscar treats technology as its primary differentiator—from consumer-grade member apps to automated provider claim adjudications. The Hudson Square, NYC engineering culture combines fast-paced iteration with rigorous system reliability. My hands-on skills in **Python/FastAPI**, **TypeScript/React**, **Kafka** event pipelines, and **PostgreSQL** align directly with Oscar's tech stack and engineering challenges.  
**Result:** As a Senior Fullstack Engineer at Oscar, I can take end-to-end ownership of critical member-facing features and backend infrastructure, ensuring that navigating health insurance feels as seamless, transparent, and empathetic as consulting a trusted doctor in the family.

---

### Q18: How do you design systems to be fault-tolerant against third-party API outages (e.g., pharmacy benefit managers, clearinghouses)?
**Category:** Distributed Systems Reliability & Fault Tolerance  
**Situation:** In healthcare and financial integrations (such as the market data server I built and the partner APIs at **Tekainos**), external third-party endpoints frequently experience network latency spikes, rate limits, or transient outages.  
**Task:** When downstream vendor APIs fail, our internal consumer-facing applications must remain resilient, avoiding cascading failures, thread pool exhaustion, or data corruption.  
**Action:** I implement a multi-layered resiliency pattern:  
1. **Timeouts & Circuit Breakers:** I wrap all outbound third-party calls in a circuit breaker pattern (using libraries like **Resilience4j** or **Tenacity**). If error rates exceed 50% over a rolling 10-second window, the circuit trips open, immediately returning fallback cached data rather than hanging threads.  
2. **Exponential Backoff with Jitter:** For transient 5xx or network drops, retries are executed with randomized exponential backoff (`t = base * 2^attempt + jitter`) to avoid thundering-herd problems.  
3. **Asynchronous Queuing & Outbox:** Non-critical vendor synchronizations are pushed to a **Kafka** topic or **AWS SQS** queue, decoupling user requests from third-party response times.  
4. **Idempotency Keys:** Every outbound transactional request carries a cryptographically unique idempotency key, ensuring that if a retried request was actually processed downstream, duplicate charges or duplicate claim submissions are physically prevented.  
**Result:** This architecture guarantees graceful degradation: users can still interact with the UI, read cached statuses, and receive notifications once background reconciliation completes, preserving **99.9% application availability**.

---

### Q19: Describe a time you built tools or infrastructure that drastically improved developer velocity or system observability.
**Category:** Developer Productivity & Observability  
**Situation:** At **Meta Reality Labs**, testing multimodal vision and environment integrations across distributed developer machines required engineers to manually spin up multiple container configurations, resulting in environment drift, broken local setups, and long onboarding cycles.  
**Task:** I wanted to streamline the developer experience by standardizing integration tooling, eliminating configuration friction, and automating regression detection across all six supported simulation environments.  
**Action:** I architected a modular **FastAPI** API layer and standardized containerized workflows using **Docker** and **Kubernetes**. I built reusable developer CLI tools and integrated **Model Context Protocol (MCP)** servers that abstracted environment orchestration behind simple declarative commands. To improve observability, I integrated **OpenTelemetry** tracing and structured JSON logging across all microservices, piping metrics into centralized dashboards. Furthermore, I created automated mock servers simulating external vision and environment endpoints, allowing engineers to run full integration test suites locally in under two minutes without connecting to expensive physical hardware rigs.  
**Result:** The new modular architecture accelerated developer integration speed by **50%**, reduced deployment complexity across 6+ configurations, and slashed new engineer environment onboarding from several days to under two hours.

---

### Q20: Oscar processes millions of sensitive member events. How do you design scalable ETL and asynchronous background workers?
**Category:** Scalable ETL & Asynchronous Systems  
**Situation:** At **Tekainos**, client transaction data arrived in irregular, bursty batches throughout the day, requiring heavy validation, OCR extraction, and reconciliation before updating master accounting ledgers. The existing synchronous processing pipeline created massive backlogs, taking up to 24 hours to reflect finalized records.  
**Task:** I was tasked with re-architecting the entire ETL ingestion system into a scalable, near-real-time asynchronous pipeline capable of handling bursty volumes with zero data loss.  
**Action:** I redesigned the architecture using an event-driven, decoupled worker model. Inbound document uploads were immediately stored in **AWS S3**, which published an `ObjectCreated` event to an **AWS SQS** FIFO queue. I deployed serverless **AWS Lambda** functions and containerized **FastAPI** workers to consume tasks concurrently from the queue. To maintain low latency, intermediate state and deduplication hashes were managed in **Redis**. Heavy OCR normalization jobs were executed in parallel worker pools with memory and CPU boundaries. Processed entities were batched using bulk `COPY` operations into **PostgreSQL** rather than single-row inserts, dramatically reducing database I/O contention.  
**Result:** End-to-end processing latency plummeted from **24 hours down to minutes**, achieving true near-real-time processing. The system slashed manual data entry by **85%**, handled 10x traffic spikes smoothly, and provided comprehensive error tracking via dead-letter queues.

---

# PART 2: Top 15 Data Structures & Algorithms (Coding Round)
*Carefully curated for Oscar Health & Top-Tech Fullstack/Backend interviews. Each problem includes Oscar context, intuitive thought process, annotated Python code with edge-case handling, and rigorous Big-O complexity analysis.*

---

### 1. Merge Intervals
**Oscar Context:** Member insurance policies often have overlapping coverage periods, or doctor availability schedules have overlapping shifts. We need to merge all overlapping time intervals into contiguous blocks.

**Thought Process:**
1. If the input list is empty, return an empty list.
2. Sort the intervals by their start time ($O(N \log N)$). This guarantees that any intervals that could potentially overlap are adjacent.
3. Initialize an empty result list `merged`.
4. Iterate through each interval:
   - If `merged` is empty, or the current interval's start is strictly greater than the last merged interval's end (`curr[0] > merged[-1][1]`), there is no overlap. Append the current interval.
   - Otherwise, there is an overlap. Update the end of the last merged interval to be the maximum of its current end and the current interval's end (`merged[-1][1] = max(merged[-1][1], curr[1])`).

```python
from typing import List

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    Merges all overlapping intervals into contiguous intervals.
    Example: [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]]
    """
    if not intervals:
        return []
    
    # Step 1: Sort intervals by start time
    intervals.sort(key=lambda x: x[0])
    
    merged: List[List[int]] = []
    
    for start, end in intervals:
        # If merged list is empty or current interval does not overlap with previous
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            # Overlap detected: merge current interval with previous
            merged[-1][1] = max(merged[-1][1], end)
            
    return merged

# Complexity:
# Time: O(N log N) due to sorting, where N is the number of intervals.
# Space: O(N) in worst case for storing the output (or O(log N) auxiliary space for sorting).
```

---

### 2. Insert Interval
**Oscar Context:** A member adds a new health insurance deductible window or a doctor blocks off a new consultation slot in an already sorted schedule.

**Thought Process:**
1. The given list is already sorted by start time.
2. We can divide the list into three parts relative to `newInterval`:
   - All intervals that end *before* `newInterval` starts: append directly to `result`.
   - All intervals that overlap with `newInterval`: merge them into `newInterval` by taking the `min(start)` and `max(end)`.
   - All intervals that start *after* `newInterval` ends: append `newInterval` first, then append the remaining intervals.

```python
from typing import List

def insert_interval(intervals: List[List[int]], new_interval: List[int]) -> List[List[int]]:
    result: List[List[int]] = []
    i = 0
    n = len(intervals)
    
    # Phase 1: Add all intervals ending before new_interval begins
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1
        
    # Phase 2: Merge all overlapping intervals with new_interval
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)
    
    # Phase 3: Add remaining intervals that start after new_interval ends
    while i < n:
        result.append(intervals[i])
        i += 1
        
    return result

# Complexity:
# Time: O(N) linear scan through intervals.
# Space: O(N) to store the result list.
```

---

### 3. Meeting Rooms II (Minimum Clinicians / Rooms Needed)
**Oscar Context:** Given an array of telemedicine appointment time intervals, find the minimum number of doctors/virtual rooms required to ensure all appointments occur without delay.

**Thought Process:**
1. If no appointments, return 0.
2. Separate start times and end times into two independent arrays, and sort both in ascending order.
3. Use two pointers: `start_ptr` and `end_ptr`.
4. When an appointment starts (`start[start_ptr] < end[end_ptr]`), we need an additional doctor/room (`used_rooms += 1`), and increment `start_ptr`.
5. If an appointment ends (`start[start_ptr] >= end[end_ptr]`), a doctor/room has become free (`used_rooms -= 1`), and increment `end_ptr`.
6. Track the maximum number of rooms used at any one time.

```python
from typing import List

def min_meeting_rooms(intervals: List[List[int]]) -> int:
    if not intervals:
        return 0
        
    start_times = sorted([i[0] for i in intervals])
    end_times = sorted([i[1] for i in intervals])
    
    start_ptr = 0
    end_ptr = 0
    available_rooms = 0
    max_rooms = 0
    
    while start_ptr < len(intervals):
        # A meeting is starting before the earliest meeting ends
        if start_times[start_ptr] < end_times[end_ptr]:
            available_rooms += 1
            start_ptr += 1
        else:
            # A meeting has ended, freeing up a room
            available_rooms -= 1
            end_ptr += 1
        max_rooms = max(max_rooms, available_rooms)
        
    return max_rooms

# Complexity:
# Time: O(N log N) to sort start and end times.
# Space: O(N) to store sorted start and end arrays.
```

---

### 4. LRU Cache (Least Recently Used Cache)
**Oscar Context:** Caching verified member eligibility tokens or provider network lookup records in memory with $O(1)$ read and write.

**Thought Process:**
1. To achieve $O(1)$ `get` and `put`, we combine a Hash Map (key $\rightarrow$ node pointer) with a Doubly Linked List (maintains access recency).
2. The doubly linked list has sentinel `head` (most recently used) and `tail` (least recently used) nodes to eliminate null checks.
3. `get(key)`: If key in map, move corresponding node to `head`, return value; else return -1.
4. `put(key, value)`: If key exists, update value and move to `head`. If key is new, create node, add to head, and add to map. If capacity is exceeded, remove node right before `tail` and delete key from map.

```python
class Node:
    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.prev: 'Node' = None
        self.next: 'Node' = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {} # key -> Node
        # Dummy head (MRU) and dummy tail (LRU)
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_to_front(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove_node(node)
            self._add_to_front(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove_node(node)
            self._add_to_front(node)
        else:
            if len(self.cache) >= self.cap:
                # Evict least recently used (node before dummy tail)
                lru_node = self.tail.prev
                self._remove_node(lru_node)
                del self.cache[lru_node.key]
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)

# Complexity:
# Time: O(1) for both get() and put().
# Space: O(capacity) for hash map and doubly linked list nodes.
```

---

### 5. Design Hit Counter / Sliding Window Rate Limiter
**Oscar Context:** Rate limiting external pharmacy benefit manager (PBM) or provider portal API calls to at most $N$ requests in the past 300 seconds.

**Thought Process:**
1. A simple queue holding timestamps works, but memory grows with request volume.
2. In production, timestamps wrap around in a fixed window. We can maintain a fixed-size bucket array of size 300 (one bucket per second).
3. Each bucket stores a tuple: `(timestamp, hit_count)`.
4. When `hit(timestamp)` is called:
   - Index is `timestamp % 300`.
   - If stored timestamp equals current timestamp, increment `hit_count`.
   - Else, reset stored timestamp to current and set `hit_count = 1`.
5. When `get_hits(timestamp)` is called:
   - Sum all `hit_count` values where `timestamp - stored_timestamp < 300`.

```python
class HitCounter:
    def __init__(self):
        # 300 buckets for a 5-minute sliding window (300 seconds)
        self.window = 300
        self.times = [0] * self.window
        self.hits = [0] * self.window

    def hit(self, timestamp: int) -> None:
        idx = timestamp % self.window
        if self.times[idx] != timestamp:
            # New time window cycle, reset bucket
            self.times[idx] = timestamp
            self.hits[idx] = 1
        else:
            self.hits[idx] += 1

    def get_hits(self, timestamp: int) -> int:
        total = 0
        for i in range(self.window):
            if timestamp - self.times[i] < self.window:
                total += self.hits[i]
        return total

# Complexity:
# Time: O(1) for hit(), O(W) = O(300) = O(1) for get_hits().
# Space: O(W) = O(300) = O(1) constant auxiliary space.
```

---

### 6. Subarray Sum Equals K (Claims Deductible Accumulation)
**Oscar Context:** Financial reconciliation — finding how many contiguous billing or claim sequences sum up exactly to a member's target deductible $K$.

**Thought Process:**
1. A brute-force check of all pairs takes $O(N^2)$.
2. We can optimize using prefix sums and a hash map in $O(N)$ time.
3. Let $PrefixSum[i]$ be the cumulative sum from index 0 to $i$.
4. The sum of subarray from $j+1$ to $i$ is $PrefixSum[i] - PrefixSum[j]$.
5. We want $PrefixSum[i] - PrefixSum[j] = K \implies PrefixSum[j] = PrefixSum[i] - K$.
6. As we iterate, we maintain a frequency map of seen prefix sums. If `(curr_sum - k)` exists in the map, we add its frequency to our total count.

```python
from typing import List
from collections import defaultdict

def subarray_sum(nums: List[int], k: int) -> int:
    prefix_counts = defaultdict(int)
    prefix_counts[0] = 1  # Base case: empty subarray sum is 0
    
    current_sum = 0
    total_subarrays = 0
    
    for num in nums:
        current_sum += num
        # If (current_sum - k) was seen before, it means a valid subarray ending here exists
        if (current_sum - k) in prefix_counts:
            total_subarrays += prefix_counts[current_sum - k]
        prefix_counts[current_sum] += 1
        
    return total_subarrays

# Complexity:
# Time: O(N) single pass through array.
# Space: O(N) hash map storage.
```

---

### 7. Group Anagrams / Medical Code Grouping
**Oscar Context:** Grouping interchangeable medical billing codes or synonym diagnosis descriptions that contain identical character frequencies.

**Thought Process:**
1. Two strings are anagrams if their sorted characters are identical, or if their character frequency tuples (size 26) match.
2. Using a 26-element tuple as the dictionary key avoids the $O(L \log L)$ sorting overhead per word.
3. Map each tuple to a list of original words. Return the map values.

```python
from typing import List
from collections import defaultdict

def group_anagrams(strs: List[str]) -> List[List[str]]:
    groups = defaultdict(list)
    
    for s in strs:
        # 26 lowercase English letter count
        count = [0] * 26
        for char in s:
            count[ord(char) - ord('a')] += 1
        # Tuples are immutable and hashable
        groups[tuple(count)].append(s)
        
    return list(groups.values())

# Complexity:
# Time: O(N * L), where N is number of strings and L is maximum length of a string.
# Space: O(N * L) to store grouped strings in dictionary.
```

---

### 8. Word Break (Parsing Unspaced Clinical Notes)
**Oscar Context:** Clinical NLP: segmenting unpunctuated medical terms or compound pharmaceutical names (`"tylenolextrastrength"`) into valid medical dictionary words.

**Thought Process:**
1. Dynamic Programming: Let `dp[i]` be `True` if the prefix `s[0:i]` can be segmented into dictionary words.
2. Base case: `dp[0] = True` (empty string is always valid).
3. For each index $i$ from 1 to $len(s)$:
   - For each $j$ from 0 to $i$:
     - If `dp[j]` is `True` and the substring `s[j:i]` is in `word_set`, then `dp[i] = True` and we can break the inner loop.
4. Return `dp[len(s)]`.

```python
from typing import List

def word_break(s: str, word_dict: List[str]) -> bool:
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True  # Empty prefix
    
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
                
    return dp[n]

# Complexity:
# Time: O(N^2 * L) where N is length of s, and L is average length of checked substring.
# Space: O(N + M) where N is dp array size, M is dictionary set size.
```

---

### 9. Lowest Common Ancestor (LCA) of a Binary Tree
**Oscar Context:** Finding the most immediate shared category in Oscar's hierarchical clinical taxonomy or medical specialty ontology.

**Thought Process:**
1. Recursive DFS traversal:
   - If the current `root` is `None`, return `None`.
   - If `root` matches either node `p` or `q`, return `root`.
2. Recursively search left and right subtrees:
   - `left = lca(root.left, p, q)`
   - `right = lca(root.right, p, q)`
3. If both `left` and `right` return non-null, `p` and `q` are in different subtrees, so current `root` is their Lowest Common Ancestor.
4. If only one is non-null, pass that non-null node up.

```python
class TreeNode:
    def __init__(self, val: int = 0):
        self.val = val
        self.left: 'TreeNode' = None
        self.right: 'TreeNode' = None

def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    # Base cases
    if not root or root == p or root == q:
        return root
        
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    
    # If both subtrees returned a candidate, root is the LCA
    if left and right:
        return root
        
    # Otherwise return the non-empty candidate
    return left if left else right

# Complexity:
# Time: O(N) where N is the number of nodes in the tree (visits each node at most once).
# Space: O(H) recursion stack where H is the height of tree (O(N) in worst case skewed tree).
```

---

### 10. Course Schedule II / Topological Sort (Clinical Protocol Prerequisites)
**Oscar Context:** Clinical care pathways and insurance pre-authorization rules: Treatment step B cannot be approved until prerequisites A and C have been satisfied.

**Thought Process:**
1. Graph representation: Nodes are steps, directed edges $(u, v)$ mean $u$ must be completed before $v$.
2. Detect cycles: If a cycle exists, the care plan is logically invalid (deadlock).
3. Algorithm: Kahn's Algorithm (BFS with In-degree count):
   - Compute in-degree (number of prerequisites) for each node.
   - Add all nodes with in-degree 0 to a queue (can be started immediately).
   - While queue is not empty, pop node, append to `order`, and for each neighbor, decrement in-degree.
   - If neighbor's in-degree reaches 0, push to queue.
4. If `len(order) == num_steps`, return `order`; otherwise cycle detected, return `[]`.

```python
from typing import List
from collections import deque, defaultdict

def find_order(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
    adj = defaultdict(list)
    in_degree = [0] * num_courses
    
    # [course, prereq] -> edge prereq -> course
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
        
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    order = []
    
    while queue:
        curr = queue.popleft()
        order.append(curr)
        
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    return order if len(order) == num_courses else []

# Complexity:
# Time: O(V + E) where V is num_courses, E is prerequisites length.
# Space: O(V + E) for adjacency list and in-degree tracking.
```

---

### 11. Number of Islands (Cluster Detection in Care Networks)
**Oscar Context:** Mapping connected healthcare provider clusters across an operational regional grid to ensure network adequacy.

**Thought Process:**
1. Standard 2D grid graph traversal.
2. Iterate through every cell `(r, c)`:
   - If cell is `'1'` (provider present), we found a new cluster (`island_count += 1`).
   - Trigger BFS or DFS from `(r, c)` to mark all connected `'1'` cells as visited (mutate to `'0'` in-place to save memory).
3. Return `island_count`.

```python
from typing import List
from collections import deque

def num_islands(grid: List[List[str]]) -> int:
    if not grid or not grid[0]:
        return 0
        
    rows, cols = len(grid), len(grid[0])
    islands = 0
    
    def bfs(start_r: int, start_c: int):
        q = deque([(start_r, start_c)])
        grid[start_r][start_c] = '0' # Mark visited
        
        while q:
            r, c = q.popleft()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    grid[nr][nc] = '0'
                    q.append((nr, nc))
                    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                islands += 1
                bfs(r, c)
                
    return islands

# Complexity:
# Time: O(M * N) where M and N are grid dimensions (each cell visited constant times).
# Space: O(min(M, N)) space for BFS queue in worst case.
```

---

### 12. Kth Largest Element in an Array / Stream (Triage Priority Queue)
**Oscar Context:** Emergency telemedicine triage: dynamically identifying the $K$-th highest priority patient risk score in real time.

**Thought Process:**
1. A full sort takes $O(N \log N)$.
2. We can maintain a Min-Heap of size $K$.
3. As we iterate through numbers:
   - Push number onto heap.
   - If heap size exceeds $K$, pop the smallest element (`heappop`).
4. The root of the heap (`heap[0]`) will always be the $K$-th largest element seen so far.
5. Quickselect also achieves $O(N)$ average time, but Min-Heap is streaming-friendly.

```python
from typing import List
import heapq

def find_kth_largest(nums: List[int], k: int) -> int:
    # Min-heap of size k
    min_heap = []
    
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
            
    return min_heap[0]

# Complexity:
# Time: O(N log K) where N is array length and K is heap capacity.
# Space: O(K) space to maintain the min-heap.
```

---

### 13. Implement Trie (Prefix Tree for Provider & Drug Search Autocomplete)
**Oscar Context:** Oscar member search bar: instant typeahead autocomplete for doctor specialties, medication names, and provider facilities.

**Thought Process:**
1. Each `TrieNode` has a dictionary `children: Dict[char, TrieNode]` and a boolean `is_end_of_word`.
2. `insert(word)`: Traverse character by character, creating nodes if they don't exist, and mark the final node as `is_end_of_word = True`.
3. `search(word)`: Traverse character by character. If a character is missing, return `False`. At the end, return `node.is_end_of_word`.
4. `starts_with(prefix)`: Similar to search, but only requires that all prefix characters exist in the path, regardless of `is_end_of_word`.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_end_of_word = True

    def search(self, word: str) -> bool:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return curr.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        curr = self.root
        for ch in prefix:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return True

# Complexity:
# Time: O(L) for insert, search, and starts_with, where L is string length.
# Space: O(Total characters inserted * alphabet size).
```

---

### 14. Trapping Rain Water (Resource Cushion Modeling)
**Oscar Context:** Hospital bed reservation and resource surge capacity allocation between seasonal peaks.

**Thought Process:**
1. Two-pointer approach in $O(N)$ time and $O(1)$ space.
2. Initialize pointers `left = 0`, `right = len(height) - 1`.
3. Maintain `left_max` and `right_max`.
4. While `left < right`:
   - If `height[left] < height[right]`:
     - If `height[left] >= left_max`, update `left_max`.
     - Else, trapped water at `left` is `left_max - height[left]`.
     - Increment `left`.
   - Else:
     - If `height[right] >= right_max`, update `right_max`.
     - Else, trapped water at `right` is `right_max - height[right]`.
     - Decrement `right`.

```python
from typing import List

def trap_rain_water(height: List[int]) -> int:
    if not height:
        return 0
        
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    total_water = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                total_water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                total_water += right_max - height[right]
            right -= 1
            
    return total_water

# Complexity:
# Time: O(N) single traversal.
# Space: O(1) constant extra space.
```

---

### 15. Longest Substring Without Repeating Characters
**Oscar Context:** Parsing diagnostic claim telemetry tokens and stream verification without duplicate identifiers.

**Thought Process:**
1. Sliding Window with a Hash Map storing the most recent index of each character.
2. Pointers: `left` and `right`.
3. As `right` advances:
   - If character `s[right]` was seen at index $\ge left$, update `left = seen[s[right]] + 1`.
   - Update `seen[s[right]] = right`.
   - Max length is `max(max_len, right - left + 1)`.

```python
def length_of_longest_substring(s: str) -> int:
    char_map = {} # char -> most recent index
    left = 0
    max_len = 0
    
    for right, char in enumerate(s):
        if char in char_map and char_map[char] >= left:
            left = char_map[char] + 1
        char_map[char] = right
        max_len = max(max_len, right - left + 1)
        
    return max_len

# Complexity:
# Time: O(N) single pass.
# Space: O(min(N, M)) where M is character set size.
```

---

# PART 3: System Design Masterclass (HLD & LLD with Healthcare Deep Dives)

## 3.1 Expanded System Design Interview Guide & Healthcare Nuances

### The Core Paradigm: How Healthcare Engineering Differs from Standard Big Tech
When designing systems at **Oscar Health**, you cannot simply replicate Twitter or Uber architectures without accounting for healthcare-specific constraints:

1. **HIPAA & PHI Security:**
   - **PHI (Protected Health Information)** segregation: Member medical records, prescription history, and diagnosis codes must be isolated from basic authentication metadata.
   - **Encryption:** Mandatory **AES-256** at rest, **TLS 1.3** in transit with mTLS between internal microservices.
   - **Audit Logs:** Immutable, append-only audit trail logging every single read or write of patient records (`user_id, timestamp, resource_id, access_type, client_ip`).

2. **Strict Financial & Clinical Consistency:**
   - A social media feed can be eventually consistent. An insurance deductible calculation or pharmacy pre-authorization **must have strong transactional consistency**.
   - Dual writes (e.g. updating a DB and publishing to Kafka) must employ the **Transactional Outbox Pattern** to prevent desynchronization.
   - Every state-mutating endpoint must be **strictly idempotent** via UUID headers.

3. **Standard Healthcare Protocols:**
   - **EDI 837 / 835:** Electronic Data Interchange for healthcare claims submission and payment advice.
   - **FHIR (Fast Healthcare Interoperability Resources) / HL7:** Modern RESTful JSON standards for exchanging electronic health records.

---

## 3.2 Top 5 High-Level System Designs (HLD)

### HLD 1: Real-Time Claims Adjudication & Processing Engine
**Prompt:** Design Oscar's core claims engine that receives medical claims from hospitals/clinics, validates member eligibility and coverage, checks benefits/deductibles, and adjudicates claims in real time.

#### 1. Requirements & Scale
- **Functional:** Ingest EDI 837 / JSON claims, validate policy active status, compute member out-of-pocket vs insurer liability, output EDI 835 remittance.
- **Non-Functional:** Zero data loss, audit logging, p99 latency < 2 seconds for real-time adjudication, 10,000 claims/sec peak throughput, strict idempotency.

#### 2. Architecture Diagram (Inline Flow)
```
[Hospital / Provider Portal]
           │
           │  (HTTPS / REST / EDI 837) + Idempotency-Key
           ▼
   [API Gateway / WAF]
           │ (mTLS, JWT Auth, Token Bucket Rate Limiter)
           ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ Claims Ingestion Service (FastAPI / Golang)                  │
 └──────────────────────┬──────────────────────────────────────┘
                        │
                        │ 1. Atomic Write to Ingestion DB & Outbox
                        ▼
            [Transactional Outbox Table]
                        │
                        │ Debezium / Kafka Connect CDC
                        ▼
           [Kafka Topic: 'claims-submitted']
                        │
                        ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ Claims Orchestrator Engine (State Machine Worker Pool)       │
 └───────┬───────────────────────────────┬─────────────────────┘
         │                               │
         │ 2. Check Eligibility          │ 3. Check Policy Rules
         ▼                               ▼
 [Eligibility Service]          [Policy Rules Engine]
   (Redis Cache -> RDS)           (Drools / Python Rules)
         │                               │
         └───────────────┬───────────────┘
                         │
                         ▼ 4. Deductible & Co-Pay Calculation
               [Accumulator Service]
                 (PostgreSQL Distributed Locking / Redis Redlock)
                         │
                         ▼ 5. Publish Result
           [Kafka Topic: 'claims-adjudicated']
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
 [Notification Service]        [Remittance Service]
  (Push to Member App)          (Generates EDI 835 Payment)
```

#### 3. Key Components & Deep Dive
- **Idempotency Layer:** The `Idempotency-Key` is hashed and checked in Redis with a 24-hour TTL. If present, cached adjudication results are returned immediately without reprocessing.
- **Accumulator Concurrency Control:** When computing how much a claim applies to a member's $3,000 deductible, concurrent claims from multiple providers could cause a race condition. We use **Optimistic Concurrency Control (OCC)** with version numbers on the `member_deductible` table, or partitioned Kafka keys on `member_id` ensuring all claims for a single member are serialized through the same partition.

---

### HLD 2: In-Network Doctor & Provider Search with Geospatial Directory
**Prompt:** Design the search system powering Oscar's member app to find in-network doctors by specialty, distance/location, language, insurance tier, and ratings.

#### 1. Requirements & Scale
- **Functional:** Autocomplete typeahead for doctor name / specialty, geospatial radius search (within 10 miles of NYC), filter by in-network tier, real-time appointment availability.
- **Non-Functional:** Search latency < 100ms, 99.99% read availability, 5 million members, 500,000 nationwide providers, read-to-write ratio 100:1.

#### 2. Architecture Diagram (Inline Flow)
```
[Member Mobile App / Web]
           │
           │ HTTPS / GET /api/v1/providers/search?lat=40.72&lon=-74.00&specialty=cardiology
           ▼
    [Cloudflare CDN] (Caches static metadata & taxonomy)
           │
           ▼
     [API Gateway]
           │
    ┌──────┴─────────────────────────────────┐
    ▼                                        ▼
[Typeahead Autocomplete]            [Provider Search Service]
  (Redis Trie / Memory)               (FastAPI / Python)
                                             │
                       ┌─────────────────────┴──────────────────────┐
                       │ Read Query                                 │ Read Realtime Slots
                       ▼                                            ▼
           [Elasticsearch / OpenSearch]                 [Appointment Service]
            - Geo-distance querying                       (Redis / PostgreSQL)
            - BM25 & Synonyms
            - Filters: tier, language, insurance_plan
                       ▲
                       │ CDC (Change Data Capture) via Debezium
                       │
              [Kafka Topic: 'provider-updates']
                       ▲
                       │
        [Provider Credentialing Master DB]
              (PostgreSQL Primary)
```

#### 3. Deep Dive: Geospatial & Search Indexing
- **Elasticsearch Mapping:** Provider documents contain `geo_point` fields (`location: {lat: 40.72, lon: -74.00}`) and nested objects for `accepted_plans: ["oscar-bronze-2026", "oscar-silver-2026"]`.
- **Geohash & QuadTree:** Queries use Elasticsearch's `geo_distance` filter sorted by combined distance and relevancy score.
- **Cache-Aside Pattern:** High-frequency searches (e.g. "PCP near 10013") are cached in **Redis** with a 15-minute TTL.

---

### HLD 3: "Doctor in the Family" Virtual Telehealth & Member Care Platform
**Prompt:** Design Oscar's virtual urgent care and telehealth platform connecting members directly to virtual doctors within minutes.

#### 1. Requirements & Scale
- **Functional:** Member requests virtual visit, smart triage questionnaire, queue matching doctor by state license, real-time video/audio room, post-visit clinical notes & e-prescriptions.
- **Non-Functional:** Video latency < 200ms, matching latency < 3 minutes, HIPAA-compliant recording storage, WebRTC signaling reliability.

#### 2. Architecture Diagram (Inline Flow)
```
[Member App]                                  [Doctor Web Portal]
     │                                                │
     ├────────────► [API Gateway / WAF] ◄─────────────┤
     │                                                │
     ▼                                                ▼
[Triage & Questionnaire]                     [Provider Session Service]
  (FastAPI + LLM Symptom Triage)               (State License Registry)
     │                                                │
     ▼                                                ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ Matchmaking & Dispatch Engine (Redis Sorted Sets + Pub/Sub)  │
 └──────────────────────────────┬──────────────────────────────┘
                                │ Match Created
                                ▼
                   [WebRTC Signaling Server]
                    (Node.js / WebSockets)
                                │
          ┌─────────────────────┴─────────────────────┐
          │ Peer-to-Peer Encrypted Media Channel      │
          ▼                                           ▼
   [Member Video Feed] <═════════════════════> [Doctor Video Feed]
          │                                           │
          └─────────────────────┬─────────────────────┘
                                │ Video Ended
                                ▼
                     [Care Summary Service]
               (PostgreSQL + S3 Encrypted PHI)
```

#### 3. Deep Dive: Queue Matching & State Licensing
- **Licensing Constraint:** A doctor can only treat a patient located in a state where the doctor holds an active medical license.
- **Redis Priority Queues:** We maintain Redis Sorted Sets (`ZSET`) keyed by state: `queue:waiting_patients:NY`, where the score is the arrival timestamp. When a doctor logs on for NY, they pop the highest priority waiting patient atomically using `ZPOPMIN`.
- **WebRTC Signaling:** WebSockets exchange SDP (Session Description Protocol) and ICE candidates. Video media flows peer-to-peer (P2P) via SRTP (Secure Real-Time Transport Protocol), avoiding media transit through our servers unless STUN/TURN fallback is required.

---

### HLD 4: Real-Time Prescription Benefit & Pharmacy Verification Gateway
**Prompt:** Design the high-throughput system verifying prescription insurance coverage when a member picks up medication at a pharmacy (CVS/Walgreens).

#### 1. Requirements & Scale
- **Functional:** Instant pharmacy benefit verification, formulary tier lookup (generic vs brand), drug-drug interaction warning check, copay determination.
- **Non-Functional:** Hard p99 latency deadline < 800ms (pharmacy terminal timeout), 99.999% availability, peak 5,000 transactions/second, active-active multi-region failover.

#### 2. Architecture Diagram (Inline Flow)
```
[Pharmacy Terminal (CVS / Walgreens)]
           │
           │ NCPDP Telecommunication Protocol / REST
           ▼
     [B2B Partner Gateway] (mTLS + Hardware Security Module)
           │
           ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ Pharmacy Adjudication Service (FastAPI / Go)                 │
 └───────┬───────────────────────────────┬─────────────────────┘
         │                               │
         │ (1) In-Memory Formulary Check │ (2) Member Deductible
         ▼                               ▼
 [Drug Formulary Cache]           [Member Plan Cache]
   (Redis Cluster / Aerospike)      (Redis Read Replica)
         │                               │
         └───────────────┬───────────────┘
                         │
                         ▼ (3) Safety Screening
            [Drug Interaction Service]
              (In-Memory Graph DB / Neo4j)
                         │
                         ▼ (4) Immediate Copay Result (<400ms)
              [NCPDP Response Packet]
                         │
                         ▼ (5) Asynchronous Financial Journaling
           [Kafka Topic: 'rx-claims-committed']
                         │
                         ▼
             [Financial Ledger DB] (PostgreSQL ACID)
```

#### 3. Deep Dive: Sub-800ms SLA & Circuit Breakers
- **Local In-Memory Caching:** Formularies (which drugs are covered and tier levels) change infrequently. They are cached in-memory on the worker instances using an LRU cache with Redis backup, delivering sub-2ms lookup times.
- **Graceful Fallback:** If the external Drug Interaction Service fails or exceeds 200ms, a circuit breaker trips and allows the benefit verification to succeed with a soft warning, ensuring patients are not stranded at the pharmacy counter without life-saving medication.

---

### HLD 5: Member Medical Records Timeline & Automated OCR Document Ingestion
**Prompt:** Design the ingestion pipeline that ingests member-uploaded medical bills, EMR PDFs, and lab results, runs OCR, extracts structured medical entities, and displays an interactive health timeline.

#### 1. Requirements & Scale
- **Functional:** Upload PDFs/Images, run OCR, extract diagnosis codes (ICD-10) and procedures (CPT), index into chronological timeline, member full-text search.
- **Non-Functional:** Process documents within 60 seconds, handle bursty batch uploads, guarantee PHI encryption at rest, 99.9% durability.

#### 2. Architecture Diagram (Inline Flow)
```
[Member App / Web UI]
           │
           │ 1. Request Upload URL
           ▼
  [Upload Service] ──► Generates S3 Pre-Signed URL (Encrypted SSE-KMS)
           │
           │ 2. Direct Upload
           ▼
 [S3 Quarantine Bucket]
           │
           │ S3 Event Notification ('ObjectCreated')
           ▼
     [AWS SQS Queue] (FIFO, Dead Letter Queue attached)
           │
           ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ OCR & Ingestion Worker Fleet (FastAPI / Celery Workers)      │
 │  - Step A: Anti-Virus & File Format Validation              │
 │  - Step B: OpenCV Pre-Processing (Deskew, Denoise)          │
 │  - Step C: Textract / Tesseract OCR Text Extraction         │
 │  - Step D: Medical Named Entity Recognition (NER / LLM)     │
 └──────────────────────────────┬──────────────────────────────┘
                                │
                                │ Extracted Entities & Metadata
                                ▼
           [Kafka Topic: 'medical-records-processed']
                                │
            ┌───────────────────┴───────────────────┐
            ▼                                       ▼
 [PostgreSQL Timeline DB]               [Elasticsearch Index]
   - Normalized ICD-10 codes              - Full-text clinical notes
   - Timestamps & Provider metadata       - Autocomplete timeline search
```

#### 3. Deep Dive: Asynchronous Processing & Security
- **S3 Pre-Signed URLs:** The application server never handles direct multipart file streams; the client streams directly to S3 with cryptographic credentials, preventing backend memory exhaustion.
- **Quarantine & De-identification:** Uploaded files remain in a quarantine bucket until scanned for malware and sanitized. PHI is encrypted with per-tenant KMS keys.

---

## 3.3 Top 5 Low-Level System Designs (LLD / OOD)

### LLD 1: Insurance Policy Deductible, Copay & Out-of-Pocket Max Calculator
**Domain:** Calculating a member's exact financial responsibility for a given healthcare bill using the **Strategy Pattern** and **Chain of Responsibility**.

#### Class Diagram (ASCII)
```
  ┌─────────────────────────────────────────────────────────┐
  │                      ClaimContext                       │
  ├─────────────────────────────────────────────────────────┤
  │ + bill_amount: Decimal                                  │
  │ + service_type: ServiceType                             │
  │ + member_accumulated_deductible: Decimal                │
  │ + deductible_limit: Decimal                             │
  │ + member_accumulated_oop: Decimal                       │
  │ + oop_max_limit: Decimal                                │
  │ + copay_amount: Decimal                                 │
  │ + coinsurance_rate: Decimal (e.g. 0.20)                 │
  │ + insurer_pays: Decimal                                 │
  │ + member_pays: Decimal                                  │
  └─────────────────────────────────────────────────────────┘
                              │
                              ▼
  ┌─────────────────────────────────────────────────────────┐
  │               <<interface>> AdjudicationRule            │
  ├─────────────────────────────────────────────────────────┤
  │ + set_next(rule: AdjudicationRule): AdjudicationRule    │
  │ + apply(context: ClaimContext): void                    │
  └─────────────────────────────────────────────────────────┘
         ▲                          ▲                    ▲
         │                          │                    │
┌───────────────────┐     ┌───────────────────┐ ┌───────────────────┐
│ OutOfPocketMaxRule│     │   CopayRule       │ │ CoinsuranceRule   │
└───────────────────┘     └───────────────────┘ └───────────────────┘
```

#### Implementation Code (Python)
```python
from decimal import Decimal
from abc import ABC, abstractmethod
from enum import Enum

class ServiceType(Enum):
    PRIMARY_CARE = "PRIMARY_CARE"
    SPECIALIST = "SPECIALIST"
    EMERGENCY_ROOM = "EMERGENCY_ROOM"

class ClaimContext:
    def __init__(self, bill_amount: Decimal, service_type: ServiceType,
                 deductible_limit: Decimal, current_deductible: Decimal,
                 oop_max_limit: Decimal, current_oop: Decimal,
                 copay: Decimal, coinsurance_rate: Decimal):
        self.bill_amount = bill_amount
        self.service_type = service_type
        self.deductible_limit = deductible_limit
        self.current_deductible = current_deductible
        self.oop_max_limit = oop_max_limit
        self.current_oop = current_oop
        self.copay = copay
        self.coinsurance_rate = coinsurance_rate
        
        self.member_pays = Decimal("0.00")
        self.insurer_pays = Decimal("0.00")
        self.remaining_bill = bill_amount

class AdjudicationRule(ABC):
    def __init__(self):
        self._next_rule: AdjudicationRule = None

    def set_next(self, rule: 'AdjudicationRule') -> 'AdjudicationRule':
        self._next_rule = rule
        return rule

    @abstractmethod
    def apply(self, ctx: ClaimContext) -> None:
        pass

class OutOfPocketCapCheckRule(AdjudicationRule):
    def apply(self, ctx: ClaimContext) -> None:
        if ctx.current_oop >= ctx.oop_max_limit:
            # Member has already met OOP max; insurer covers 100%
            ctx.insurer_pays = ctx.bill_amount
            ctx.member_pays = Decimal("0.00")
            ctx.remaining_bill = Decimal("0.00")
            return
        if self._next_rule:
            self._next_rule.apply(ctx)

class CopayRule(AdjudicationRule):
    def apply(self, ctx: ClaimContext) -> None:
        if ctx.copay > 0 and ctx.remaining_bill > 0:
            applicable_copay = min(ctx.copay, ctx.remaining_bill)
            # Ensure copay does not exceed remaining OOP limit
            remaining_oop_room = ctx.oop_max_limit - ctx.current_oop - ctx.member_pays
            actual_copay = min(applicable_copay, remaining_oop_room)
            
            ctx.member_pays += actual_copay
            ctx.remaining_bill -= actual_copay
            
        if self._next_rule and ctx.remaining_bill > 0:
            self._next_rule.apply(ctx)

class DeductibleAndCoinsuranceRule(AdjudicationRule):
    def apply(self, ctx: ClaimContext) -> None:
        # Step 1: Apply Deductible
        remaining_deductible = max(Decimal("0.00"), ctx.deductible_limit - ctx.current_deductible)
        deductible_charge = min(ctx.remaining_bill, remaining_deductible)
        
        ctx.member_pays += deductible_charge
        ctx.remaining_bill -= deductible_charge
        
        # Step 2: Apply Coinsurance on remaining balance
        if ctx.remaining_bill > 0:
            coinsurance_member = ctx.remaining_bill * ctx.coinsurance_rate
            remaining_oop_room = ctx.oop_max_limit - ctx.current_oop - ctx.member_pays
            actual_member_coinsurance = min(coinsurance_member, remaining_oop_room)
            
            ctx.member_pays += actual_member_coinsurance
            ctx.insurer_pays += (ctx.remaining_bill - actual_member_coinsurance)
            ctx.remaining_bill = Decimal("0.00")
            
        # Final sanity assertion
        assert ctx.member_pays + ctx.insurer_pays == ctx.bill_amount
```

---

### LLD 2: Sliding Window Counter Rate Limiter (Thread-Safe with Local Fallback)
**Domain:** Protecting Oscar provider portal APIs against brute-force queries using an in-memory sliding window counter.

#### Implementation Code (Python)
```python
import time
import threading
from collections import deque

class SlidingWindowRateLimiter:
    """
    Thread-safe sliding window log rate limiter.
    Permits at most `max_requests` within `window_seconds`.
    """
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.client_windows = {} # client_id -> deque of timestamps
        self.lock = threading.Lock()

    def is_allowed(self, client_id: str) -> bool:
        current_time = time.time()
        with self.lock:
            if client_id not in self.client_windows:
                self.client_windows[client_id] = deque()
                
            window = self.client_windows[client_id]
            
            # Evict timestamps outside current sliding window
            while window and window[0] <= current_time - self.window_seconds:
                window.popleft()
                
            if len(window) < self.max_requests:
                window.append(current_time)
                return True
            else:
                return False
```

---

### LLD 3: Provider Appointment Scheduling & Conflict Resolution Engine
**Domain:** Managing virtual care doctor bookings without double-booking, handling concurrent reservations via optimistic interval checks.

#### Implementation Code (Python)
```python
from datetime import datetime
from typing import List, Optional
import threading

class TimeSlot:
    def __init__(self, start_time: datetime, end_time: datetime):
        if start_time >= end_time:
            raise ValueError("Start time must precede end time.")
        self.start_time = start_time
        self.end_time = end_time

    def overlaps(self, other: 'TimeSlot') -> bool:
        return self.start_time < other.end_time and other.start_time < self.end_time

class Appointment:
    def __init__(self, appointment_id: str, provider_id: str, member_id: str, slot: TimeSlot):
        self.appointment_id = appointment_id
        self.provider_id = provider_id
        self.member_id = member_id
        self.slot = slot

class ScheduleManager:
    def __init__(self):
        self._provider_schedules = {} # provider_id -> List[Appointment]
        self._lock = threading.Lock()

    def book_appointment(self, appointment_id: str, provider_id: str, 
                         member_id: str, new_slot: TimeSlot) -> bool:
        with self._lock:
            if provider_id not in self._provider_schedules:
                self._provider_schedules[provider_id] = []
                
            current_appointments = self._provider_schedules[provider_id]
            
            # Check for conflict
            for appt in current_appointments:
                if appt.slot.overlaps(new_slot):
                    return False # Overlap detected, booking rejected
                    
            # No overlap, book atomically
            new_appt = Appointment(appointment_id, provider_id, member_id, new_slot)
            current_appointments.append(new_appt)
            return True

    def cancel_appointment(self, provider_id: str, appointment_id: str) -> bool:
        with self._lock:
            if provider_id not in self._provider_schedules:
                return False
            schedule = self._provider_schedules[provider_id]
            for i, appt in enumerate(schedule):
                if appt.appointment_id == appointment_id:
                    del schedule[i]
                    return True
            return False
```

---

### LLD 4: Extensible Claims Processing State Machine & Rules Engine
**Domain:** Modeling the lifecycle of a medical claim (`SUBMITTED -> ELIGIBILITY_VERIFIED -> ADJUDICATED -> PAID -> CLOSED`) using the **State Pattern**.

#### Implementation Code (Python)
```python
from abc import ABC, abstractmethod

class ClaimState(ABC):
    @abstractmethod
    def verify_eligibility(self, claim: 'Claim') -> None:
        pass

    @abstractmethod
    def adjudicate(self, claim: 'Claim') -> None:
        pass

    @abstractmethod
    def pay(self, claim: 'Claim') -> None:
        pass

class SubmittedState(ClaimState):
    def verify_eligibility(self, claim: 'Claim') -> None:
        print(f"Claim {claim.claim_id}: Eligibility verified successfully.")
        claim.set_state(EligibilityVerifiedState())

    def adjudicate(self, claim: 'Claim') -> None:
        raise InvalidTransitionError("Cannot adjudicate claim prior to eligibility check.")

    def pay(self, claim: 'Claim') -> None:
        raise InvalidTransitionError("Cannot pay unadjudicated claim.")

class EligibilityVerifiedState(ClaimState):
    def verify_eligibility(self, claim: 'Claim') -> None:
        print("Eligibility already confirmed.")

    def adjudicate(self, claim: 'Claim') -> None:
        print(f"Claim {claim.claim_id}: Adjudicating benefits.")
        claim.set_state(AdjudicatedState())

    def pay(self, claim: 'Claim') -> None:
        raise InvalidTransitionError("Cannot pay claim while in adjudication stage.")

class AdjudicatedState(ClaimState):
    def verify_eligibility(self, claim: 'Claim') -> None:
        print("Already verified.")

    def adjudicate(self, claim: 'Claim') -> None:
        print("Already adjudicated.")

    def pay(self, claim: 'Claim') -> None:
        print(f"Claim {claim.claim_id}: Remittance disbursed.")
        claim.set_state(PaidState())

class PaidState(ClaimState):
    def verify_eligibility(self, claim: 'Claim') -> None:
        raise InvalidTransitionError("Terminal state.")
    def adjudicate(self, claim: 'Claim') -> None:
        raise InvalidTransitionError("Terminal state.")
    def pay(self, claim: 'Claim') -> None:
        print("Claim already paid.")

class InvalidTransitionError(Exception):
    pass

class Claim:
    def __init__(self, claim_id: str):
        self.claim_id = claim_id
        self._state: ClaimState = SubmittedState()

    def set_state(self, state: ClaimState) -> None:
        self._state = state

    def verify_eligibility(self) -> None:
        self._state.verify_eligibility(self)

    def adjudicate(self) -> None:
        self._state.adjudicate(self)

    def pay(self) -> None:
        self._state.pay(self)
```

---

### LLD 5: High-Concurrency Thread-Safe In-Memory Cache with TTL & Eviction
**Domain:** Caching member sessions and provider credentials in-process with concurrent read/write locks, TTL expiration, and LRU eviction.

#### Implementation Code (Python)
```python
import time
import threading
from typing import Any, Optional

class CacheItem:
    def __init__(self, value: Any, ttl_seconds: Optional[float]):
        self.value = value
        self.expires_at = (time.time() + ttl_seconds) if ttl_seconds else None

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at

class ThreadSafeTTLCache:
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._store = {}
        self._lock = threading.RLock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._store:
                return None
            item = self._store[key]
            if item.is_expired():
                del self._store[key]
                return None
            return item.value

    def set(self, key: str, value: Any, ttl_seconds: Optional[float] = None) -> None:
        with self._lock:
            # Active eviction if full
            if len(self._store) >= self.max_size and key not in self._store:
                self._evict_expired_or_oldest()
            self._store[key] = CacheItem(value, ttl_seconds)

    def _evict_expired_or_oldest(self) -> None:
        # First pass: clean expired keys
        expired_keys = [k for k, v in self._store.items() if v.is_expired()]
        for k in expired_keys:
            del self._store[k]
            
        # If still at capacity, evict any arbitrary key
        if len(self._store) >= self.max_size:
            oldest_key = next(iter(self._store))
            del self._store[oldest_key]
```

---
*End of Oscar Health Senior Fullstack Interview Guide.*
