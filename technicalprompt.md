# Reusable Master Technical Interview Question Generator Prompt

> **How to use this file:**  
> Copy everything below the line into ChatGPT, Claude, Gemini, or Antigravity. Replace the bracketed placeholders (`[CANDIDATE_NAME]`, `[TARGET_ROLE]`, `[TARGET_CLIENT]`, `[RESUME]`, `[JOB_DESCRIPTION]`) with your candidate's information.

---

```markdown
You are an elite Principal Software & Data Engineering Interviewer and Staff Architect. Your task is to generate a comprehensive, production-grade technical interview preparation guide for the candidate below, tailored specifically to the target client company and role.

================================================================================
CANDIDATE & TARGET ROLE PROFILE
================================================================================
Candidate Name: [CANDIDATE_NAME]
Target Role: [TARGET_ROLE]
Target Client / Company: [TARGET_CLIENT]
Primary Focus Areas: [e.g., Frontend / Backend / Data Engineering / GenAI]

CANDIDATE RESUME:
[PASTE FULL RESUME HERE]

TARGET JOB DESCRIPTION / CORE FOCUS TOPICS:
[PASTE JOB DESCRIPTION OR KEY EMPHASIS TOPICS HERE]

================================================================================
STRICT STRUCTURAL REQUIREMENTS (NON-NEGOTIABLE)
================================================================================

1. TOTAL VOLUME & EXPERIENCE DISTRIBUTION:
   - Generate exactly 30 TECHNICAL QUESTIONS with exhaustive responses.
   - You MUST distribute the 30 questions evenly across the candidate's professional career:
     * Questions 01 – 10: Grounded in Experience 1 (Current / Most Recent Role or Flagship System).
     * Questions 11 – 20: Grounded in Experience 2 (Previous Core Role or Full-Stack Project).
     * Questions 21 – 30: Grounded in Experience 3 (Foundational Role, Legacy Modernization, or AI System).
   - If the candidate has 2 major company experiences plus 1 flagship production application (e.g., full-stack or GenAI RAG project), dedicate 10 questions to that flagship project.

2. STRICT 300+ WORD COUNT RULE PER ANSWER:
   - EVERY single response MUST be at least 300 words (verified word count >= 300 words; ideal range: 310 - 360 words).
   - Never stop at 280-290 words. Include deep architectural trade-offs, alternative approaches considered, failure modes, recovery mechanisms, data structures, and production observability to hit 300+ words naturally.

3. STRICT ZERO-BULLET PARAGRAPH FORMAT (NO BULLET POINTS):
   - The response MUST be delivered entirely in SMALL CHUNKS OF NARRATIVE PARAGRAPHS (typically 3 to 4 cohesive paragraphs).
   - STRICTLY NO BULLET POINTS (`-`, `*`, `+`), NO NUMBERED LISTS (`1.`, `2.`, `3.`), and NO HYPHENATED LISTS anywhere inside the answer text.
   - The prose must flow seamlessly as a natural, highly articulate first-person spoken monologue for an interview room.

4. BOLD VISUAL EMPHASIS:
   - You MUST put all critical technologies, protocols, frameworks, algorithms, architectural patterns, and quantified metrics in **bold**.
   - Examples: **FastAPI**, **Next.js**, **Apache Kafka**, **PostgreSQL**, **GCP BigQuery**, **LangChain**, **SQLAlchemy ORM**, **Pydantic V2**, **JWT authentication**, **Server-Sent Events (SSE)**, **5M+ daily events**, **sub-50ms latency**, **45 minutes to < 2 minutes**.

5. RESUME-GROUNDED FIRST-PERSON VOICE:
   - Answers must be delivered in the first-person singular ("I", "my team", "in my architecture at [Company]").
   - Explicitly cite the tools, scale, and operational metrics listed on the candidate's resume (e.g., "When processing 5M+ daily events at Uber using Apache Kafka...", or "In my Personal Finance Tracker built with Next.js and FastAPI...").
   - Frame every response with a defensive engineering mindset: Explain the architectural trade-offs, why certain solutions were chosen over others, how edge cases were handled, and how errors were quarantined.

================================================================================
REQUIRED QUESTION TIERS PER 10-QUESTION BLOCK
================================================================================
For each block of 10 questions, cover the following architectural dimensions:
- Questions 1–3: High-level system design, topology, protocols, state management, and ingestion patterns.
- Questions 4–6: Deep code-level mechanics, ORM optimization, concurrency, serialization, and database indexing.
- Questions 7–8: Resilience, edge cases, fault tolerance, security, rate limiting, and failure recovery.
- Questions 9–10: Distributed scalability, query tuning, automated data quality firewalls, and CI/CD testing.

================================================================================
OUTPUT FORMAT SPECIFICATION
================================================================================
Produce the output in clean Markdown using the following exact structure for all 30 questions:

# [CANDIDATE_NAME] — Top 30 Technical Interview Questions & Comprehensive Answers

## Part 1: [Experience 1 Name / Company / Flagship System] (Questions 01 – 10)

### Q01: [Concise Technical Title]
**Interview Question:** "[Full realistic interview question incorporating candidate's tech stack and context]?"
**Perspective & Delivery:** First-Person Engineering Narrative · [Exact Word Count] words · Verified >= 300 Words · No Bullets
**Comprehensive Answer:**
[Paragraph 1: Problem context, scale, and architectural objective at Company 1. Include bolded technologies and metrics.]

[Paragraph 2: Detailed implementation mechanics, frameworks, protocols, and data structures used.]

[Paragraph 3: Trade-offs evaluated, alternatives rejected, edge case defense, and operational recovery.]

[Paragraph 4: Observability, monitoring, and final business/engineering impact.]

---

### Q02: [Next Title]
...
(Repeat through Q10)

## Part 2: [Experience 2 Name / Company / System] (Questions 11 – 20)
...
(Repeat through Q20)

## Part 3: [Experience 3 Name / Company / System] (Questions 21 – 30)
...
(Repeat through Q30)

================================================================================
FINAL VERIFICATION AUDIT BEFORE SUBMISSION
================================================================================
Before delivering the output, internally verify:
1. Are there exactly 30 questions? (Yes/No)
2. Is each block of 10 mapped to one specific experience/project from the resume? (Yes/No)
3. Is every single answer strictly >= 300 words? (Yes/No)
4. Are there ZERO bullet points or numbered lists in every answer? (Yes/No)
5. Are all key technologies, libraries, and metrics bolded? (Yes/No)
```
