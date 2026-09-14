# System Design Interview — Complete Preparation Guide

## 1. The Two Flavors: HLD vs LLD

| | High-Level Design (HLD) | Low-Level Design (LLD) |
|---|---|---|
| Also called | System Design, Architecture round | Object-Oriented Design (OOD), Machine Coding |
| Scope | Whole system across servers/services | Single component, in code |
| Output | Boxes, arrows, data flow, APIs | Classes, interfaces, methods, design patterns |
| Example prompt | "Design Twitter" | "Design a parking lot system" |
| Tests | Scale, trade-offs, distributed systems thinking | Clean code, SOLID principles, extensibility |

Most companies (Google, Amazon, Uber, Microsoft, etc.) test HLD for senior/mid-senior roles and LLD for roles closer to hands-on coding (or as a separate round entirely). Know which one you're being interviewed for — the prep is different.

---

## 2. HLD: The Framework to Follow in Every Interview

Interviewers care less about your final diagram and more about **how you get there**. Use this repeatable structure:

### Step 1 — Clarify Requirements (5 min)
- **Functional requirements**: What must the system do? (Pick 3-4 core features, don't try to cover everything)
- **Non-functional requirements**: Scale, latency, availability vs consistency, read/write ratio
- **Ask about scale explicitly**: "How many users? How many requests/sec? How much data?"
- Never assume — always ask. This is the #1 signal interviewers watch for.

### Step 2 — Back-of-the-Envelope Estimation (5 min)
- Traffic estimates (QPS, peak vs average)
- Storage estimates (data size × growth over time)
- Bandwidth estimates
- This justifies every architectural decision you make later — don't skip it even if it feels like busywork.

### Step 3 — Define the API / Interface (2-3 min)
- REST/gRPC endpoints for the core use cases
- Request/response shape
- Shows you think about contracts before internals

### Step 4 — High-Level Architecture (10-15 min)
- Draw the major components: client → load balancer → services → databases → caches → queues
- Keep it simple first, then add complexity as you narrate trade-offs
- Explain *why* each box exists, not just what it is

### Step 5 — Deep Dive (15-20 min)
- Interviewer will usually steer you into 1-2 specific areas (e.g., "how does your feed ranking work?" or "what happens on a cache miss?")
- This is where most of your score comes from — go deep, not wide
- Common deep-dive topics: database schema, sharding strategy, consistency model, caching strategy, handling failures

### Step 6 — Identify Bottlenecks & Trade-offs (5 min)
- Single points of failure
- Hot partitions / hot keys
- Trade-offs you made and why (CAP theorem choices, SQL vs NoSQL, sync vs async)

---

## 3. What Interviewers Are Actually Scoring You On

Most rubrics (Google, Meta, Amazon are fairly public about this) boil down to:

1. **Requirement gathering & scoping** — did you ask good questions instead of diving in blind?
2. **Structured communication** — did you drive the conversation, or wait to be led?
3. **Trade-off reasoning** — can you articulate *why* X over Y, not just name-drop technologies?
4. **Depth on request** — when pushed, can you go deeper (not just wider)?
5. **Practical judgment** — do your numbers/estimates make sense? Do you catch your own mistakes?
6. **Handling ambiguity** — do you get flustered when requirements are vague, or do you make reasonable assumptions out loud?

### The biggest red flags interviewers notice
- Jumping straight to "we'll use Kafka and Redis" without justifying why
- Never asking clarifying questions
- Drawing a huge diagram with no narration of trade-offs
- Getting stuck on one component and running out of time
- Buzzword-dropping without being able to explain the buzzword when probed
- Ignoring the interviewer's hints/steering (they usually nudge you on purpose)
- Silence — not thinking out loud

### What impresses interviewers most
- Proactively stating assumptions and trade-offs unprompted
- Correcting yourself ("actually, on second thought, a queue is better here because...")
- Being able to zoom in and zoom out (see the whole system, then drill into one part)
- Knowing 2-3 ways to solve a sub-problem and explaining why you picked one

---

## 4. HLD — Core Building Blocks You MUST Know Cold

You don't need to memorize every technology — you need to deeply understand these concepts and be able to explain trade-offs for each:

- **Load balancing**: L4 vs L7, round robin, consistent hashing
- **Caching**: cache-aside, write-through, write-back, eviction policies, cache invalidation
- **Databases**: SQL vs NoSQL, indexing, replication (leader-follower), sharding strategies, ACID vs BASE
- **CAP theorem**: what it actually means in practice, not just the acronym
- **Message queues**: Kafka vs RabbitMQ vs SQS — when to use pub/sub vs point-to-point
- **CDNs**: static content delivery, edge caching
- **Rate limiting**: token bucket, sliding window
- **Consistent hashing**: for sharding and load distribution
- **Consensus**: basic idea of Paxos/Raft (not implementation, just why it exists)
- **API Gateway & service discovery** (for microservices-style questions)
- **Database scaling**: vertical vs horizontal, read replicas, partitioning
- **Idempotency** and exactly-once vs at-least-once delivery
- **Async processing**: when to move work off the critical path

## 5. Classic HLD Problems to Practice
- URL Shortener (great warm-up — teaches hashing, DB design, scale)
- Rate Limiter
- Chat/Messaging system (WhatsApp)
- News Feed (Twitter/Instagram)
- Video streaming (YouTube/Netflix)
- Ride-sharing (Uber)
- Distributed cache
- Notification system
- E-commerce checkout / inventory system
- Search autocomplete / typeahead

---

## 6. LLD: The Framework to Follow

### Step 1 — Clarify Requirements & Scope
- Same discipline as HLD — ask what entities/actions are in scope, what's out of scope
- Nail down the use cases before writing a single class

### Step 2 — Identify Core Entities/Objects
- Nouns become classes, verbs become methods
- Identify relationships: is-a (inheritance) vs has-a (composition)

### Step 3 — Define Class Diagram
- Classes, interfaces, key attributes and methods
- Decide what's abstract vs concrete early

### Step 4 — Apply Design Principles & Patterns
- **SOLID principles** — this is what's graded most heavily
- Pick design patterns *only where they genuinely fit* (Factory, Strategy, Observer, Singleton, Decorator, State are the most commonly useful ones in interviews)
- Don't force-fit patterns just to show you know them — that's a red flag, not a plus

### Step 5 — Write Clean, Extensible Code
- Actual working code (in whatever language you're comfortable in)
- Favor composition over inheritance
- Handle edge cases and errors explicitly

### Step 6 — Walk Through Extensibility
- Interviewer will ask "how would you add feature X?" — your design should absorb this with minimal changes
- This is the real test of whether your design is good, not just functional

---

## 7. LLD — What Interviewers Notice Most

1. **SOLID adherence** — especially Single Responsibility and Open/Closed
2. **Correct use of OOP** — composition vs inheritance used appropriately, not everything jammed into one class
3. **Naming and readability** — classes/methods that read like the domain, not generic "Manager"/"Helper" soup
4. **Extensibility** — can the design handle a new requirement without a rewrite?
5. **Thread-safety / concurrency awareness** — if relevant (e.g., parking lot with concurrent bookings)
6. **Not over-engineering** — using a pattern where a simple method would do is a real deduction

### Common LLD mistakes
- Starting to code before defining entities/relationships
- One giant class doing everything (violates SRP)
- Overusing inheritance where composition is cleaner
- Ignoring edge cases (concurrency, invalid input, capacity limits)
- Not handling the "what if we add X" follow-up gracefully

## 8. Classic LLD Problems to Practice
- Parking Lot
- Elevator System
- Library Management System
- Tic-Tac-Toe / Chess engine
- Splitwise (expense sharing)
- Movie Ticket Booking System (BookMyShow)
- Vending Machine
- LRU Cache (implementation)
- Rate Limiter (as a class, not distributed)
- Snake and Ladder game

---

## 9. General Prep Strategy (Timeline)

| Phase | Focus |
|---|---|
| Weeks 1-2 | Learn core concepts (caching, databases, queues, CAP, SOLID) — don't skip fundamentals for pattern-memorizing |
| Weeks 3-4 | Practice 8-10 HLD problems out loud, using the 6-step framework every time |
| Weeks 3-4 (parallel) | Practice 5-6 LLD problems, writing actual code, not just diagrams |
| Week 5 | Mock interviews (with a peer or recorded self-practice) — the "thinking out loud" muscle only builds with practice |
| Ongoing | Read real engineering blogs (Uber, Netflix, Airbnb, Meta engineering blogs) to see how actual trade-offs were made |

## 10. Communication Tips That Matter as Much as Technical Knowledge
- **Talk continuously.** Silence reads as "stuck," even if you're thinking productively.
- **Drive the interview.** Treat the interviewer as a collaborator/stakeholder, not an examiner waiting for you to finish.
- **Use a whiteboard/diagram tool fluently** — practice with excalidraw, or plain paper, before the real thing.
- **Timebox yourself.** Don't spend 20 minutes on requirements and leave no time for the deep dive.
- **Say your assumptions out loud** even if no one asks — "I'll assume this needs strong consistency for payments, eventual consistency is fine for the feed."
- **It's OK to not know something** — say "I haven't worked with X, but conceptually I'd expect it to solve Y because Z" rather than bluffing.

## 11. Most Important Single Takeaway
> The interview is graded on your **process and trade-off reasoning**, not on producing the "correct" final architecture. There is no single right answer for "design Twitter." There is a right *way to think* about it — ask questions, quantify scale, start simple, justify every addition, go deep when asked, and know the cost of every decision you make.
