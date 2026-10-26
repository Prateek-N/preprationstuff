# Technical Interview Preparation — Master Rulebook & Standard

This document defines the strict engineering standards, architectural rules, and formatting guidelines for creating production-grade technical interview preparation Q&As for senior engineering and technical roles.

---

## 1. Core Structure & Allocation Rules

### A. Total Question Volume
- **Total Questions:** Exactly **30 technical interview questions**.
- **Experience-Based Allocation:** Questions must be directly anchored to the candidate's professional career history:
  - If the candidate has **3 core experiences/roles**, allocate **10 questions per experience**:
    - **Questions 01 – 10:** Role 1 (Most Recent / Current Experience)
    - **Questions 11 – 20:** Role 2 (Previous Experience)
    - **Questions 21 – 30:** Role 3 (Earlier Experience / Major Production Systems)
  - If the resume has **2 roles + major end-to-end full-stack/AI production projects**, allocate **10 questions to Role 1**, **10 questions to Role 2**, and **10 questions to the production flagship projects**.
  - If the resume has **4+ experiences**, allocate the 30 questions weighted toward the most senior roles (e.g., 12 for Role 1, 10 for Role 2, 8 for Role 3/4).

### B. Experience Anchoring
- Every single question must test a technology, architectural challenge, or design decision that **explicitly exists in that experience bullet on the resume**.
- Generic textbook questions (e.g., *"What is an index in SQL?"* or *"What is a hook in React?"*) are **strictly forbidden**.
- Questions must be phrased as real-world interview scenarios:
  - *"At [Company], you built [System/Pipeline] handling [Metric/Scale]. How did you architect [Component], what trade-offs did you make, and how did you resolve [Failure Mode]?"*

---

## 2. Response Length & Formatting Constraints

### A. Strict Word Count Constraint
- **Minimum Word Count:** Every answer must be **strictly at least 300 words** ($\ge 300$ words).
- **Recommended Range:** **310 to 360 words** per response.
- Answers that are 280–299 words are non-compliant and must be expanded with deep architectural nuance, edge-case mitigation, or monitoring observability.

### B. Paragraph Structure — STRICTLY NO BULLET POINTS
- **Formatting Style:** Format the response in **small chunks of paragraphs** (typically 3 to 4 concise paragraphs of 3 to 5 sentences each).
- **Zero Bullets Rule:** **DO NOT** use bullet points (`-`, `*`, `+`), numbered lists (`1.`, `2.`, `3.`), or hyphenated lists inside the technical response.
- **Rationale:** Bullet points sound recited from a cheat sheet. Cohesive narrative paragraphs simulate natural, senior-level verbal delivery in an interview room.

### C. Bold Visual Emphasis
- Important concepts, system names, and technical terminology must be rendered in **bold**:
  - **Technologies & Frameworks:** e.g., **FastAPI**, **Next.js**, **Apache Kafka**, **GCP BigQuery**, **SQLAlchemy**, **Redis**, **Pydantic**, **PySpark**.
  - **Architectural Concepts:** e.g., **Server-Sent Events (SSE)**, **Idempotent Consumers**, **Partition Pruning**, **Dead-Letter Queue (DLQ)**, **Sliding Window Counters**, **Row-Level Security (RLS)**.
  - **Metrics & Scale:** e.g., **5M+ daily events**, **45 minutes down to < 2 minutes**, **sub-50ms latency**, **10TB+ datasets**.

---

## 3. Verbal Narrative & Perspective

- **Voice:** First-person singular engineering narrative (**"I"**, **"my architecture"**, **"I designed"**, **"in my pipeline"**).
- **Tone:** Authoritative, pragmatic, defensive, and architecturally mature. Avoid vague platitudes like *"I used best practices"*. Explicitly state the exact mechanism used (e.g., *"I configured the Kafka consumer with `enable.auto.commit=False` and committed offsets only after the atomic BigQuery write completed"*).
- **Structure of Every Answer:**
  1. **Context & Architectural Need:** Set up the problem, scale, and business requirements at that specific employer.
  2. **Technical Implementation:** Walk through the exact tools, protocols, data structures, and algorithms chosen.
  3. **Trade-offs & Resilience:** Explain why alternative approaches were rejected, how edge cases or failures (network partitions, race conditions, schema drift) were defended, and how metrics were observed.

---

## 4. Question Progression Matrix (For Each 10-Question Block)

Within each 10-question experience block, ensure comprehensive coverage across these 4 architectural tiers:

| Tier | Focus Area | Example Topics |
| :--- | :--- | :--- |
| **Tier 1: Core Architecture & Data Flow** (3 Qs) | High-level topology, protocols, state management, ingestion patterns. | Next.js SSR vs ISR, Kafka partitioning, FastAPI async event loops. |
| **Tier 2: Deep Implementation & Mechanics** (3 Qs) | Code-level patterns, ORM tuning, concurrency, schema validation. | SQLAlchemy N+1 queries, Pydantic V2 serializers, Redis token buckets. |
| **Tier 3: Resilience, Edge Cases & Security** (2 Qs) | Failure recovery, fault tolerance, multi-tenancy, rate limiting, auth. | JWT silent refresh, DLQs, distributed locking, row-level isolation. |
| **Tier 4: Observability, Scale & Tuning** (2 Qs) | Performance bottlenecks, memory profiling, query tuning, CI/CD. | BigQuery clustering, Great Expectations firewalls, execution plans. |

---

## 5. Verification & Compliance Checklist

Before publishing any technical prep document, verify each question against this automated checklist:

- [ ] Exactly 30 technical questions generated.
- [ ] 10 questions mapped to Experience 1, 10 to Experience 2, 10 to Experience 3 (or flagship projects).
- [ ] Word count for every question is verified $\ge 300$ words (via regex `\b\w+\b`).
- [ ] Zero bullet points or numbered lists found in the answer body (`^[\s]*[-*+\d\.]`).
- [ ] Formatted in 3–4 short, natural paragraphs.
- [ ] Key frameworks, libraries, protocols, algorithms, and numbers are in **bold**.
- [ ] Aligned 100% with resume claims and targeted client tech stack.
