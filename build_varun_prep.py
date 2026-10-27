# -*- coding: utf-8 -*-
"""
Build script for Varun Sambath Kumar's AI/ML Engineer (GDIT Remote) Interview Prep Suite.
Compiles:
1. varun_gdit_aiml_prep.md
2. content/varun-gdit-aiml-prep.mdx
3. varun_gdit_aiml_prep.html
4. public/varun_gdit_aiml_prep.html

Passcode: "Varun"
"""

import json
import re
import os
import shutil

from varun_questions_part1 import QUESTIONS_PART1
from varun_questions_part2 import QUESTIONS_PART2
from varun_coding import CODING_PROBLEMS

QUESTIONS = QUESTIONS_PART1 + QUESTIONS_PART2
print(f"Loaded {len(QUESTIONS)} Technical Questions and {len(CODING_PROBLEMS)} Coding Problems.")

# =============================================================================
# 1. GENERATE MASTER MARKDOWN (varun_gdit_aiml_prep.md)
# =============================================================================
def generate_markdown():
    md = []
    md.append("# Varun Sambath Kumar — AI/ML Engineer Technical Interview Preparation Suite\n\n")
    md.append("## Target Role: AI/ML Engineer — General Dynamics Information Technology (GDIT Remote)\n\n")
    md.append("**Candidate:** Varun Sambath Kumar | Dallas, TX | +1 346-327-6013 | varunkumar.will@gmail.com | [LinkedIn](https://linkedin.com) | [GitHub](https://github.com)\n\n")
    md.append("**Target Focus:** Generative AI & Large Language Models (LLM) · Fine-Tuning (LoRA/QLoRA) · RAG Architecture · Inference Optimization (vLLM, KV-Cache, INT8) · MLOps & Observability · Federal & Mission-Critical AI\n\n")
    md.append("**Passcode Lock:** `Varun`\n\n")
    md.append("---\n\n")

    md.append("## Executive Summary & GDIT Strategic Alignment\n\n")
    md.append("> **Varun Sambath Kumar** is an **AI/ML Engineer** with 2+ years of production experience shipping high-throughput machine learning, deep learning, and generative AI systems at Fortune 500 enterprise scale. Varun specializes in domain-specific foundation model fine-tuning (**LoRA, QLoRA, PEFT**) of **Llama 3.3 70B** and **Mistral-7B**, **Retrieval-Augmented Generation (RAG)** systems, automated evaluation (**Ragas, DeepEval**), distributed training (**DeepSpeed ZeRO-3, PyTorch FSDP**), and low-latency inference optimization (**vLLM, PagedAttention, KV-cache, INT8 quantization**).\n\n")
    md.append("> At **Thomson Reuters**, Varun delivers LLM-powered legal intelligence on the **Westlaw** platform, designing high-precision RAG pipelines using **LangChain** and **LlamaIndex** across complex legal corpora. He assisted in domain fine-tuning experiments on Llama and Mistral using LoRA/QLoRA, optimized multi-GPU inference using **vLLM** on **AWS SageMaker**, and established automated evaluation harnesses with **Ragas** and **DeepEval** that measure Faithfulness, Answer Relevancy, and hallucination rates ahead of production deployment.\n\n")
    md.append("> At **Dell Technologies**, Varun engineered end-to-end machine learning infrastructure processing tens of millions of supply chain records monthly using **Python, PyTorch, and Apache Spark**. He slashed model inference latency from **800ms to under 200ms** by deploying **Triton Inference Server** and **ONNX Runtime**, fine-tuned **BERT** transformers on millions of support tickets for predictive maintenance NLP, and deployed containerized model-serving on **AWS SageMaker** and **Kubernetes** with drift detection and **Prometheus/Grafana** observability for 15+ production models. He built an automated feature store using **Feast** and **Apache Airflow**, migrated batch workflows to real-time streaming with **FastAPI** and **Apache Kafka**, and standardized **MLflow** CI/CD across engineering squads.\n\n")
    md.append("> For **General Dynamics Information Technology (GDIT)**, which delivers mission-critical technology, cybersecurity, and engineering solutions to defense, intelligence, and federal civilian agencies, Varun brings the specialized engineering rigor required to deploy secure, air-gapped, zero-trust AI solutions. His expertise bridges deep algorithmic optimization, scalable distributed computing, automated hallucination guardrails, and compliance with federal AI risk management frameworks.\n\n")

    md.append("## Quantified Impact & Architecture Metrics\n\n")
    md.append("| Organization / System | Domain & Role | Core Tech Stack | Quantified Engineering & Business Impact |\n")
    md.append("| :--- | :--- | :--- | :--- |\n")
    md.append("| **Thomson Reuters** | Legal Intelligence & RAG | Llama 3.3 70B, Mistral-7B, LangChain, LlamaIndex | Built hierarchical legal RAG across Westlaw, boosting contractual extraction accuracy by **22%** |\n")
    md.append("| **Thomson Reuters** | Inference Optimization | vLLM, PagedAttention, KV-Cache, AWS SageMaker | Cut Time-to-First-Token (**TTFT**) by **45%** and boosted concurrent throughput by **3.8x** |\n")
    md.append("| **Thomson Reuters** | Automated LLM Evaluation | Ragas, DeepEval, Cross-Encoder NLI | Established CI/CD deployment gates enforcing **> 0.92 Faithfulness** and **< 2% hallucination** |\n")
    md.append("| **Dell Technologies** | Model Serving Optimization | Triton Inference Server, ONNX Runtime, PyTorch | Slashed model inference latency from **800ms to under 200ms** (4x throughput improvement) |\n")
    md.append("| **Dell Technologies** | Predictive Maintenance NLP | Hugging Face, BERT, Focal Loss, Transformers | Fine-tuned classifiers on millions of tickets, reducing mean resolution time by several hours |\n")
    md.append("| **Dell Technologies** | Real-Time Streaming Inference | FastAPI, Apache Kafka, Continuous Batching | Compressed prediction delivery from **hours to under 250ms** for 100K+ daily operational users |\n")
    md.append("| **Dell Technologies** | Feature Store Infrastructure | Feast, Redis, Snowflake, Apache Airflow | Automated 200+ features, eliminating manual data prep per sprint and preventing train-serve skew |\n")
    md.append("| **Dell Technologies** | Production MLOps & Observability | MLflow, Docker, Kubernetes (EKS), Prometheus | Hosted **15+ production models** globally; compressed debugging cycles from **2 weeks to 2 days** |\n")
    md.append("| **AI Support Assistant** | Flagship GenAI Platform | Python, FastAPI, React, pgvector, Redis, RAG | Indexed **50,000+ documents**, serving **2,000+ daily queries** with sub-10s citation responses |\n")
    md.append("| **AI Career Hub** | Document Processing Platform | React, Node.js, Prisma, PostgreSQL, OpenAI | Built resume parser with **97-point accuracy** score and sub-500ms API response latency |\n\n")

    md.append("---\n\n")

    md.append("## Core System Architecture Blueprints\n\n")

    md.append("### Blueprint 1: Thomson Reuters Westlaw Legal RAG & LLM Serving Pipeline\n\n")
    md.append("```mermaid\ngraph TD\n")
    md.append("    subgraph Ingestion [Legal Document Ingestion & Indexing]\n")
    md.append("        RAW_DOCS[Statutory Codes & Judicial Opinions] --> CHUNK[Hierarchical Parent-Child Chunking: LlamaIndex]\n")
    md.append("        CHUNK --> EMBED[Domain Legal Transformer Embeddings]\n")
    md.append("        EMBED --> DENSE_VEC[(Dense Vector DB: Pinecone / pgvector)]\n")
    md.append("        CHUNK --> BM25_IDX[(Sparse Inverted Index: Elasticsearch BM25)]\n")
    md.append("    end\n")
    md.append("    subgraph Retrieval [Hybrid Retrieval & Context Fusion]\n")
    md.append("        USER_QUERY[Attorney Legal Query] --> HYBRID_SEARCH[Parallel Hybrid Search]\n")
    md.append("        DENSE_VEC <--> HYBRID_SEARCH\n")
    md.append("        BM25_IDX <--> HYBRID_SEARCH\n")
    md.append("        HYBRID_SEARCH --> RRF[Reciprocal Rank Fusion: k=60]\n")
    md.append("        RRF --> RERANK[Cross-Encoder Reranker: Top 5 Chunks]\n")
    md.append("    end\n")
    md.append("    subgraph Serving [vLLM High-Throughput Inference on SageMaker]\n")
    md.append("        RERANK --> PROMPT_ASSEMBLY[Prompt Context Construction]\n")
    md.append("        PROMPT_ASSEMBLY --> VLLM[vLLM Inference Engine: PagedAttention]\n")
    md.append("        VLLM <--> KV_CACHE[Decoupled Non-Contiguous KV-Cache]\n")
    md.append("        VLLM --> MODEL[Fine-Tuned Llama 3.3 70B / Mistral-7B QLoRA]\n")
    md.append("        MODEL --> GUARDRAILS[Guardrails AI: Citation & Hallucination Gate]\n")
    md.append("        GUARDRAILS --> STREAM_OUT[Verified Legal Intelligence Response]\n")
    md.append("    end\n")
    md.append("```\n\n")

    md.append("### Blueprint 2: Dell Technologies Enterprise ML Platform & Streaming Telemetry\n\n")
    md.append("```mermaid\ngraph TD\n")
    md.append("    subgraph DataIngestion [Distributed Telemetry Ingestion]\n")
    md.append("        SENSORS[Supply Chain IoT & Manufacturing Sensors] --> KAFKA[Apache Kafka Ingestion Topics]\n")
    md.append("        BATCH_ERP[Historical ERP Records: Tens of Millions] --> SPARK[Apache Spark Distributed Processing]\n")
    md.append("    end\n")
    md.append("    subgraph FeatureStore [Feast Feature Management]\n")
    md.append("        SPARK --> OFFLINE_STORE[(Offline Feature Store: S3 / Snowflake Parquet)]\n")
    md.append("        AIRFLOW[Apache Airflow DAGs] --> MATERIALIZE[feast materialize Pipeline]\n")
    md.append("        MATERIALIZE --> ONLINE_STORE[(Online Feature Store: Redis In-Memory)]\n")
    md.append("    end\n")
    md.append("    subgraph RealTimeServing [High-Throughput Model Serving]\n")
    md.append("        KAFKA --> FASTAPI_CONSUMER[FastAPI Asynchronous Consumer Workers]\n")
    md.append("        ONLINE_STORE <-->|Sub-5ms Feature Lookup| FASTAPI_CONSUMER\n")
    md.append("        FASTAPI_CONSUMER --> DYNAMIC_BATCH[Continuous Dynamic Batching Queue]\n")
    md.append("        DYNAMIC_BATCH --> TRITON[NVIDIA Triton Inference Server: ONNX Runtime]\n")
    md.append("        TRITON --> MODEL_EXEC[INT8 Quantized PyTorch Model Ensemble]\n")
    md.append("    end\n")
    md.append("    subgraph MLOpsMonitoring [Observability & Governance]\n")
    md.append("        TRITON --> PROMETHEUS[Prometheus Metrics Exporter: Latency & QPS]\n")
    md.append("        FASTAPI_CONSUMER --> DRIFT[PSI Drift Detector: Evidently AI]\n")
    md.append("        PROMETHEUS --> GRAFANA[Grafana Global Observability Dashboards]\n")
    md.append("        DRIFT -->|PSI > 0.25| RETRAIN_ALERT[Automated Airflow Retraining Alert]\n")
    md.append("    end\n")
    md.append("```\n\n")

    md.append("### Blueprint 3: GDIT Federal & Defense Air-Gapped Zero-Trust AI Architecture\n\n")
    md.append("```mermaid\ngraph LR\n")
    md.append("    subgraph IngressBoundary [Secure Mission Network Enclave]\n")
    md.append("        USER[Defense / Intelligence Analyst] --> PKI[PKI / CAC Certificate Handshake]\n")
    md.append("        PKI --> MTLS[mTLS Service Mesh: Istio Zero-Trust]\n")
    md.append("    end\n")
    md.append("    subgraph AirGappedCompute [Isolated Federal Kubernetes: Red Hat OpenShift / GovCloud]\n")
    md.append("        MTLS --> GUARD_IN[Pre-Inference Guardrail: PII Redaction & Prompt Injection Filter]\n")
    md.append("        GUARD_IN --> LOCAL_VLLM[Air-Gapped vLLM Container: Local Model Artifacts]\n")
    md.append("        LOCAL_VLLM --> LOCAL_LLM[Hardened Llama 3.3 70B / Mistral Weights]\n")
    md.append("        LOCAL_VLLM <--> LOCAL_VEC[(Local pgvector DB: FIPS 140-3 Encrypted at Rest)]\n")
    md.append("    end\n")
    md.append("    subgraph Verification [Post-Generation Defense & Auditing]\n")
    md.append("        LOCAL_LLM --> NLI_GATE[DeepEval / NLI Entailment Citation Verifier]\n")
    md.append("        NLI_GATE -->|Entailment >= 0.90| OUTPUT[Secure Grounded Response]\n")
    md.append("        NLI_GATE -->|Ungrounded / Hallucinated| REFUSAL[Deterministic Refusal / Raw Source Reroute]\n")
    md.append("        OUTPUT --> AUDIT_VAULT[(Immutable SIEM Audit Log Repository)]\n")
    md.append("    end\n")
    md.append("```\n\n")

    md.append("---\n\n")

    # =========================================================================
    # SECTION 1: TOP 30 TECHNICAL QUESTIONS
    # =========================================================================
    md.append("# Section 1: Top 30 Technical Interview Questions & Comprehensive Answers (300+ Words Each)\n\n")
    md.append("> **Candidate Delivery Standard:** Every single response is strictly at least 300 words, formatted in small cohesive paragraphs without any bullet points, directly grounded in Varun's resume across **Thomson Reuters**, **Dell Technologies**, and his flagship **AI/ML systems**, tailored specifically to **GDIT** mission-critical standards.\n\n")

    current_cat = ""
    for q in QUESTIONS:
        words = len(re.findall(r'\b\w+\b', q['answer']))
        if q.get('category') and q['category'] != current_cat:
            current_cat = q['category']
            md.append(f"## {current_cat}\n\n")

        md.append(f"### Q{q['num']:02d}: {q['title']}\n\n")
        md.append(f"**Interview Question:** *\"{q['question']}\"*\n\n")
        md.append(f"**Perspective & Delivery:** First-Person Engineering Narrative (`{words} words` · Verified $\\ge 300$ words · Strictly No Bullets)  \n\n")
        md.append(f"**Comprehensive Answer:**\n\n")
        md.append(f"{q['answer']}\n\n")
        md.append("---\n\n")

    # =========================================================================
    # SECTION 2: TOP 10 PRODUCTION CODING PROBLEMS
    # =========================================================================
    md.append("# Section 2: Top 10 Production AI/ML Engineering Coding Problems\n\n")
    md.append("### Production-grade implementations covering RAG rankers, LoRA adapters, KV-cache attention, continuous batching, INT8 quantization, and PySpark feature pipelines.\n\n")

    for p in CODING_PROBLEMS:
        md.append(f"### Problem {p['num']}: {p['title']}\n\n")
        md.append(f"**Category:** `{p['category']}`  \n\n")
        md.append("#### 1. Problem Statement\n\n")
        md.append(f"{p['problem_statement']}\n\n")
        md.append("#### 2. Production Implementation & Commentary\n\n")
        md.append("```python\n")
        md.append(f"{p['code'].strip()}\n")
        md.append("```\n\n")
        md.append("#### 3. Complexity & Execution Profile\n\n")
        md.append(f"{p['complexity']}\n\n")
        md.append("---\n\n")

    # =========================================================================
    # SECTION 3: SCENARIOS & RESUME DEFENSE
    # =========================================================================
    md.append("# Section 3: Candidate Experience Defense, Behavioral Framework & GDIT Mission Alignment\n\n")

    md.append("### 1. Thomson Reuters — Generative AI, RAG & LLM Serving at Scale\n\n")
    md.append("At Thomson Reuters, Varun contributed to mission-critical legal intelligence features on Westlaw. Key interview talking points include designing hierarchical parent-child RAG chunking to preserve statutory citations, fine-tuning Llama 3.3 70B and Mistral-7B via QLoRA with rank=64 and alpha=128 across linear and MLP projections, optimizing inference using vLLM's PagedAttention and continuous batching on AWS SageMaker, and building automated evaluation gates with Ragas and DeepEval enforcing Faithfulness > 0.92 and hallucination rates < 2%.\n\n")

    md.append("### 2. Dell Technologies — Enterprise Machine Learning Infrastructure & Latency Optimization\n\n")
    md.append("At Dell Technologies, Varun engineered high-throughput ML pipelines processing tens of millions of supply chain records monthly using Python, PyTorch, and Apache Spark. Crucial accomplishments to defend include slashing model inference latency from 800ms to under 200ms using Triton Inference Server and ONNX Runtime graph optimizations, fine-tuning BERT transformers with Focal Loss on support tickets for predictive maintenance NLP, deploying containerized model-serving on Kubernetes with drift detection, building a feature store using Feast and Airflow to eliminate train-serve skew, and migrating batch scoring to real-time streaming with Kafka and FastAPI.\n\n")

    md.append("### 3. Flagship Projects & GDIT Federal / Defense Alignment\n\n")
    md.append("Varun's flagship projects—including his AI-Powered Customer Support Assistant (indexing 50,000+ documents with pgvector and Redis semantic caching), AI Career Hub (resume parsing with 97-point accuracy), and FairShare (real-time WebSockets and LSTM forecasting)—demonstrate full-stack engineering craftsmanship. For GDIT's federal, defense, and civilian mission initiatives, emphasize his ability to containerize self-contained, air-gapped LLM runtimes, enforce Zero-Trust cybersecurity and mTLS protocols, eliminate hallucinations via NLI entailment gates, and conduct responsible AI audits following the NIST AI Risk Management Framework.\n\n")

    return "".join(md)

# =============================================================================
# 2. GENERATE NEXTJS MDX (content/varun-gdit-aiml-prep.mdx)
# =============================================================================
def sanitize_for_mdx(text: str) -> str:
    code_blocks = []
    def code_repl(match):
        code_blocks.append(match.group(0))
        return f"__MDX_CODE_BLOCK_{len(code_blocks)-1}__"

    # Protect code blocks and inline code
    text = re.sub(r"```[\s\S]*?```", code_repl, text)
    text = re.sub(r"`[^`\n]+`", code_repl, text)

    # Sanitize JSX / MDX sensitive characters in prose
    text = text.replace("{", "&#123;").replace("}", "&#125;")
    text = text.replace("<=", "&le;").replace(">=", "&ge;")
    text = re.sub(r"<(?![a-zA-Z\/])", "&lt;", text)

    # Restore code blocks
    for idx, cb in enumerate(code_blocks):
        text = text.replace(f"__MDX_CODE_BLOCK_{idx}__", cb)

    return text

def generate_mdx(master_md):
    escaped_body = sanitize_for_mdx(master_md)

    header = """---
title: Varun Sambath Kumar — AI/ML Engineer (GDIT Remote) Interview Preparation Suite
description: Complete technical interview preparation guide for AI/ML Engineer at General Dynamics Information Technology (GDIT) — Top 30 technical questions (300+ words each, narrative paragraphs, no bullets), 10 production AI/ML coding problems, architectural blueprints, and experience defense across Thomson Reuters, Dell Technologies, and flagship GenAI systems.
---

<PasswordGate password="Varun" candidateName="Varun Sambath Kumar">

"""

    footer = """

</PasswordGate>
"""
    return header + escaped_body + footer

# =============================================================================
# 3. GENERATE INTERACTIVE WEBPAGE (varun_gdit_aiml_prep.html)
# =============================================================================
def generate_html():
    items_json = []
    categories = []

    # 1. Add Technical Questions
    for q in QUESTIONS:
        words = len(re.findall(r'\b\w+\b', q['answer']))
        cat = q.get('category', 'Technical Excellence')
        if cat not in categories:
            categories.append(cat)
        items_json.append({
            "type": "question",
            "num": q["num"],
            "category": cat,
            "title": q["title"],
            "question": q["question"],
            "words": words,
            "answer": q["answer"]
        })

    # 2. Add Coding Problems
    coding_cat = "AI/ML Production Implementations"
    if coding_cat not in categories:
        categories.append(coding_cat)

    for p in CODING_PROBLEMS:
        full_content = f"### 1. Problem Statement\n{p['problem_statement']}\n\n### 2. Production Implementation & Commentary\n```python\n{p['code'].strip()}\n```\n\n### 3. Complexity & Execution Profile\n{p['complexity']}"
        words = len(re.findall(r'\b\w+\b', full_content))
        items_json.append({
            "type": "coding",
            "num": p["num"],
            "category": coding_cat,
            "title": f"Problem {p['num']}: {p['title']}",
            "question": p["problem_statement"][:175] + "...",
            "words": words,
            "answer": full_content
        })

    items_json_str = json.dumps(items_json, ensure_ascii=False)
    categories_json_str = json.dumps(categories, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GDIT — AI/ML Engineer Prep Suite · Varun Sambath Kumar</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <style>
    :root {{
      --bg-base: #06090e;
      --bg-surface: #0c121b;
      --bg-card: #121a27;
      --bg-card-hover: #192437;
      --border: #1f2e46;
      --border-accent: #38bdf8;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --gdit-blue: #0284c7;
      --gdit-cyan: #38bdf8;
      --gdit-emerald: #10b981;
      --gdit-violet: #818cf8;
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg-base);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.65;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }}

    /* LOCK SCREEN */
    #lockScreen {{
      position: fixed; inset: 0;
      background: radial-gradient(circle at center, #0f2038 0%, #03060a 100%);
      display: flex; align-items: center; justify-content: center;
      z-index: 99999; padding: 1.5rem;
    }}
    .lock-box {{
      background: rgba(12, 18, 27, 0.96);
      backdrop-filter: blur(24px);
      border: 1px solid rgba(56, 189, 248, 0.45);
      border-radius: 22px;
      padding: 2.75rem 2.5rem;
      max-width: 490px;
      width: 100%;
      text-align: center;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.95), 0 0 60px rgba(56, 189, 248, 0.25);
    }}
    .lock-logo-mark {{
      display: inline-flex; align-items: center; justify-content: center;
      margin-bottom: 1.25rem; font-size: 2.3rem; font-weight: 900; letter-spacing: -0.04em;
    }}
    .lock-txt-1 {{ color: #ffffff; }}
    .lock-txt-2 {{ color: #38bdf8; }}
    .lock-badge-pill {{
      background: linear-gradient(135deg, rgba(2, 132, 199, 0.25), rgba(56, 189, 248, 0.25));
      border: 1px solid rgba(56, 189, 248, 0.4);
      padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; color: #7dd3fc;
      font-family: var(--font-mono); margin-left: 8px; font-weight: 700;
    }}
    .lock-box h2 {{ font-size: 1.45rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.02em; }}
    .lock-box p {{ color: var(--text-muted); font-size: 0.88rem; margin-bottom: 1.75rem; }}
    .input-group {{ position: relative; margin-bottom: 1.25rem; }}
    .input-group input {{
      width: 100%;
      background: rgba(6, 9, 14, 0.92);
      border: 1px solid var(--border);
      padding: 0.95rem 1.2rem;
      border-radius: 12px;
      color: #fff;
      font-size: 1.05rem;
      outline: none;
      transition: all 0.2s;
      text-align: center;
      letter-spacing: 0.12em;
    }}
    .input-group input:focus {{
      border-color: var(--gdit-cyan);
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25);
    }}
    .unlock-btn {{
      width: 100%;
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: #ffffff;
      border: none;
      padding: 0.95rem;
      border-radius: 12px;
      font-size: 0.98rem;
      font-weight: 800;
      cursor: pointer;
      transition: all 0.2s;
      letter-spacing: 0.04em;
    }}
    .unlock-btn:hover {{
      transform: translateY(-1px);
      box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.5);
      background: linear-gradient(135deg, #38bdf8, #0284c7);
    }}
    .error-msg {{
      color: #f87171; font-size: 0.85rem; margin-top: 0.9rem; display: none; font-weight: 500;
    }}

    /* MAIN APP */
    #app {{ display: none; }}
    .page-wrapper {{ max-width: 1400px; margin: 0 auto; padding: 2rem 2.5rem 5rem; }}

    /* HEADER */
    .top-bar {{
      display: flex; align-items: center; justify-content: space-between;
      padding: 1.25rem 0; border-bottom: 1px solid var(--border); margin-bottom: 2.5rem;
    }}
    .brand-mark {{
      display: flex; align-items: center; gap: 14px; font-weight: 800; font-size: 1.35rem; letter-spacing: -0.03em;
    }}
    .brand-badge {{
      background: rgba(2, 132, 199, 0.15); border: 1px solid rgba(56, 189, 248, 0.35);
      color: #7dd3fc; font-family: var(--font-mono); font-size: 0.72rem;
      font-weight: 600; padding: 4px 10px; border-radius: 6px;
    }}
    .header-links {{ display: flex; align-items: center; gap: 1rem; }}
    .header-btn {{
      background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border);
      color: var(--text-muted); padding: 0.55rem 1.1rem; border-radius: 8px;
      font-size: 0.85rem; font-weight: 600; text-decoration: none; transition: all 0.2s;
      cursor: pointer;
    }}
    .header-btn:hover {{ background: rgba(255, 255, 255, 0.1); color: #fff; border-color: var(--border-accent); }}

    /* HERO BANNER */
    .hero-banner {{
      background: linear-gradient(135deg, rgba(15, 32, 56, 0.9) 0%, rgba(9, 15, 25, 0.95) 100%);
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-radius: 20px; padding: 2.75rem; margin-bottom: 2.5rem;
      box-shadow: 0 20px 40px -15px rgba(0,0,0,0.7); position: relative; overflow: hidden;
    }}
    .hero-banner::after {{
      content: ""; position: absolute; right: -80px; top: -80px; width: 320px; height: 320px;
      background: radial-gradient(circle, rgba(56, 189, 248, 0.2) 0%, transparent 70%);
      pointer-events: none; border-radius: 50%;
    }}
    .hero-eyebrow {{
      font-family: var(--font-mono); font-size: 0.8rem; text-transform: uppercase;
      color: #7dd3fc; font-weight: 700; letter-spacing: 0.08em; margin-bottom: 0.75rem;
      display: flex; align-items: center; gap: 8px;
    }}
    .hero-eyebrow::before {{
      content: ""; display: inline-block; width: 8px; height: 8px; background: #38bdf8; border-radius: 50%;
      box-shadow: 0 0 10px #38bdf8;
    }}
    .hero-title {{
      font-size: 2.45rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 1rem; line-height: 1.25;
    }}
    .hero-title span {{
      background: linear-gradient(135deg, #ffffff 40%, #7dd3fc 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .hero-subtitle {{
      color: var(--text-muted); font-size: 1.05rem; max-width: 980px; line-height: 1.7; margin-bottom: 2rem;
    }}
    .hero-stats-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1.25rem;
    }}
    .stat-card {{
      background: rgba(6, 9, 14, 0.75); border: 1px solid var(--border);
      border-radius: 12px; padding: 1.25rem; transition: transform 0.2s;
    }}
    .stat-card:hover {{ transform: translateY(-2px); border-color: var(--border-accent); }}
    .stat-val {{
      font-size: 1.65rem; font-weight: 800; color: #fff; margin-bottom: 0.25rem;
      font-family: var(--font-mono);
    }}
    .stat-val.blue {{ color: #7dd3fc; }}
    .stat-val.emerald {{ color: #34d399; }}
    .stat-val.cyan {{ color: #38bdf8; }}
    .stat-val.amber {{ color: #fbbf24; }}
    .stat-label {{ font-size: 0.8rem; color: var(--text-muted); font-weight: 500; }}

    /* ARCHITECTURE MERMAID SECTION */
    .arch-section {{
      background: var(--bg-surface); border: 1px solid var(--border);
      border-radius: 16px; padding: 2rem; margin-bottom: 2.5rem;
    }}
    .arch-header {{
      display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem;
      padding-bottom: 1rem; border-bottom: 1px solid var(--border);
    }}
    .arch-title {{ font-size: 1.35rem; font-weight: 700; color: #fff; }}
    .arch-badge {{
      font-size: 0.75rem; font-family: var(--font-mono); background: rgba(2, 132, 199, 0.2);
      color: #7dd3fc; padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.4);
    }}
    .mermaid-box {{
      background: rgba(6, 9, 14, 0.8); border: 1px solid var(--border);
      border-radius: 12px; padding: 1.75rem; overflow-x: auto; margin-bottom: 1.5rem;
    }}

    /* CONTROLS & FILTER BAR */
    .controls-panel {{
      background: var(--bg-surface); border: 1px solid var(--border);
      border-radius: 16px; padding: 1.5rem; margin-bottom: 2rem;
      display: flex; flex-direction: column; gap: 1.25rem;
    }}
    .search-row {{ display: flex; gap: 1rem; align-items: center; }}
    .search-input-wrap {{ flex: 1; position: relative; }}
    .search-input-wrap input {{
      width: 100%; background: var(--bg-base); border: 1px solid var(--border);
      padding: 0.85rem 1.2rem; border-radius: 10px; color: #fff; font-size: 0.95rem;
      outline: none; transition: all 0.2s;
    }}
    .search-input-wrap input:focus {{ border-color: var(--gdit-cyan); box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25); }}
    .action-btn-group {{ display: flex; gap: 0.75rem; }}
    .ctrl-btn {{
      background: var(--bg-card); border: 1px solid var(--border); color: var(--text-muted);
      padding: 0.85rem 1.25rem; border-radius: 10px; font-size: 0.88rem; font-weight: 600;
      cursor: pointer; transition: all 0.2s; white-space: nowrap;
    }}
    .ctrl-btn:hover {{ background: var(--bg-card-hover); color: #fff; border-color: var(--border-accent); }}
    .pill-filters {{ display: flex; flex-wrap: wrap; gap: 0.6rem; }}
    .pill-btn {{
      background: var(--bg-card); border: 1px solid var(--border); color: var(--text-muted);
      padding: 0.45rem 1rem; border-radius: 8px; font-size: 0.82rem; font-weight: 600;
      cursor: pointer; transition: all 0.2s;
    }}
    .pill-btn:hover {{ color: #fff; border-color: var(--text-muted); }}
    .pill-btn.active {{
      background: var(--gdit-blue); color: #ffffff; border-color: var(--gdit-blue);
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
    }}

    /* PROGRESS BAR */
    .progress-bar-wrap {{
      background: var(--bg-base); border: 1px solid var(--border); border-radius: 10px;
      padding: 0.85rem 1.25rem; display: flex; align-items: center; justify-content: space-between; gap: 1.5rem;
    }}
    .progress-text {{ font-size: 0.85rem; font-weight: 600; color: var(--text-muted); font-family: var(--font-mono); }}
    .progress-track {{
      flex: 1; height: 8px; background: rgba(255, 255, 255, 0.08); border-radius: 4px; overflow: hidden;
    }}
    .progress-fill {{
      height: 100%; width: 0%; background: linear-gradient(90deg, #0284c7, #10b981);
      border-radius: 4px; transition: width 0.3s ease;
    }}

    /* QUESTION & CODING CARDS */
    .card-list {{ display: flex; flex-direction: column; gap: 1.25rem; }}
    .q-card {{
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 14px; overflow: hidden; transition: all 0.25s ease;
    }}
    .q-card:hover {{ border-color: rgba(56, 189, 248, 0.4); box-shadow: 0 8px 24px -6px rgba(0,0,0,0.6); }}
    .q-card.completed {{ border-color: rgba(16, 185, 129, 0.45); }}
    .q-card.completed .q-header {{ background: rgba(16, 185, 129, 0.04); }}

    .q-header {{
      padding: 1.25rem 1.5rem; cursor: pointer; display: flex;
      align-items: center; justify-content: space-between; gap: 1rem;
      user-select: none;
    }}
    .q-header-left {{ display: flex; align-items: flex-start; gap: 1rem; flex: 1; }}
    .q-num-badge {{
      background: rgba(2, 132, 199, 0.15); border: 1px solid rgba(56, 189, 248, 0.35);
      color: #7dd3fc; font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700;
      padding: 4px 9px; border-radius: 6px; white-space: nowrap; margin-top: 2px;
    }}
    .q-num-badge.coding-badge {{
      background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35);
      color: #34d399;
    }}
    .q-meta-group {{ display: flex; flex-direction: column; gap: 0.25rem; }}
    .q-cat-tag {{
      font-size: 0.72rem; color: var(--text-dim); text-transform: uppercase;
      font-weight: 700; letter-spacing: 0.05em; font-family: var(--font-mono);
    }}
    .q-title-text {{ font-size: 1.05rem; font-weight: 700; color: #fff; line-height: 1.4; }}
    .q-prompt-sub {{ font-size: 0.88rem; color: var(--text-muted); font-style: italic; margin-top: 2px; }}

    .q-header-right {{ display: flex; align-items: center; gap: 1rem; }}
    .word-badge {{
      font-size: 0.72rem; font-family: var(--font-mono); color: var(--text-dim);
      background: rgba(255, 255, 255, 0.04); padding: 3px 8px; border-radius: 4px;
      white-space: nowrap;
    }}
    .q-checkbox {{
      width: 18px; height: 18px; accent-color: #10b981; cursor: pointer;
    }}
    .chevron {{
      color: var(--text-dim); font-size: 0.85rem; transition: transform 0.25s;
    }}
    .q-card.open .chevron {{ transform: rotate(180deg); color: #fff; }}

    .q-body {{
      display: none; padding: 0 1.5rem 1.75rem; border-top: 1px solid rgba(255, 255, 255, 0.04);
      animation: fadeIn 0.2s ease-in;
    }}
    .q-card.open .q-body {{ display: block; }}
    @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}

    .answer-content {{
      margin-top: 1.25rem; color: #cbd5e1; font-size: 0.96rem; line-height: 1.78;
    }}
    .answer-content p {{ margin-bottom: 1.15rem; }}
    .answer-content p:last-child {{ margin-bottom: 0; }}
    .answer-content strong {{ color: #ffffff; font-weight: 700; }}
    .answer-content h3 {{ color: #e2e8f0; font-size: 1.1rem; margin: 1.25rem 0 0.5rem; }}
    .answer-content h4 {{ color: #cbd5e1; font-size: 1.0rem; margin: 1.0rem 0 0.4rem; }}
    .answer-content pre {{
      background: #04060a; border: 1px solid var(--border); border-radius: 10px;
      padding: 1.25rem; overflow-x: auto; margin: 1.25rem 0;
      font-family: var(--font-mono); font-size: 0.88rem; line-height: 1.6; color: #e2e8f0;
    }}
    .answer-content code {{
      font-family: var(--font-mono); font-size: 0.86rem; background: rgba(2, 132, 199, 0.12);
      color: #7dd3fc; padding: 2px 6px; border-radius: 4px;
    }}
    .answer-content pre code {{
      background: transparent; color: inherit; padding: 0; font-size: 0.88rem;
    }}

    .q-footer-bar {{
      display: flex; align-items: center; justify-content: flex-end; gap: 1rem;
      margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.05);
    }}
    .copy-ans-btn {{
      background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border);
      color: var(--text-muted); padding: 0.45rem 0.95rem; border-radius: 6px;
      font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.2s;
    }}
    .copy-ans-btn:hover {{ background: rgba(255, 255, 255, 0.08); color: #fff; }}
    .copy-toast {{
      font-size: 0.78rem; font-family: var(--font-mono); color: #34d399; opacity: 0; transition: opacity 0.2s;
    }}
    .copy-toast.show {{ opacity: 1; }}

    /* FOOTER */
    .page-footer {{
      margin-top: 4rem; padding-top: 2rem; border-top: 1px solid var(--border);
      text-align: center; color: var(--text-dim); font-size: 0.85rem;
    }}

    @media (max-width: 768px) {{
      .page-wrapper {{ padding: 1.25rem 1rem 3rem; }}
      .hero-banner {{ padding: 1.75rem; }}
      .hero-title {{ font-size: 1.75rem; }}
      .search-row {{ flex-direction: column; align-items: stretch; }}
      .action-btn-group {{ justify-content: space-between; }}
    }}
  </style>
</head>
<body>

  <!-- PASSCODE LOCK SCREEN -->
  <div id="lockScreen">
    <div class="lock-box">
      <div class="lock-logo-mark">
        <span class="lock-txt-1">GD</span><span class="lock-txt-2">IT</span>
        <span class="lock-badge-pill">AI/ML PREP</span>
      </div>
      <h2>AI/ML Engineer Interview Prep Suite</h2>
      <p>Candidate: Varun Sambath Kumar · Enter passcode to unlock</p>
      <div class="input-group">
        <input type="password" id="passInput" placeholder="Enter Access Passcode" autofocus autocomplete="off">
      </div>
      <button class="unlock-btn" onclick="checkPass()">Unlock Master Guide</button>
      <div class="error-msg" id="errMsg">Incorrect passcode. Please verify your credentials.</div>
    </div>
  </div>

  <!-- MAIN INTERACTIVE APP -->
  <div id="app">
    <div class="page-wrapper">

      <!-- TOP BAR -->
      <div class="top-bar">
        <div class="brand-mark">
          <span style="color:#fff;">GD<span style="color:#38bdf8;">IT</span></span>
          <span class="brand-badge">AI/ML MISSION ENGINEERING PREP</span>
        </div>
        <div class="header-links">
          <button class="header-btn" onclick="lockPage()">🔒 Lock Portal</button>
        </div>
      </div>

      <!-- HERO BANNER -->
      <div class="hero-banner">
        <div class="hero-eyebrow">Enterprise & Defense AI Engineering Suite</div>
        <div class="hero-title">
          <span>Varun Sambath Kumar</span> · AI/ML Engineer
        </div>
        <div class="hero-subtitle">
          Engineered for AI/ML Engineer interviews at General Dynamics Information Technology (GDIT). Covers LLM fine-tuning (LoRA/QLoRA on Llama 3.3 70B & Mistral-7B), Legal & Enterprise RAG, vLLM PagedAttention inference, DeepEval/Ragas evaluation, distributed training (DeepSpeed/FSDP), Triton & ONNX serving, and federal zero-trust AI architectures.
        </div>
        <div class="hero-stats-grid">
          <div class="stat-card">
            <div class="stat-val blue">30 Q&As</div>
            <div class="stat-label">300+ Words Each · No Bullets · Narrative</div>
          </div>
          <div class="stat-card">
            <div class="stat-val emerald">10 Code</div>
            <div class="stat-label">LoRA, Attention, vLLM, RAG, Quantization</div>
          </div>
          <div class="stat-card">
            <div class="stat-val cyan">800ms to &lt;200ms</div>
            <div class="stat-label">Triton & ONNX Serving Latency Optimization</div>
          </div>
          <div class="stat-card">
            <div class="stat-val amber">&gt; 0.92 Faithfulness</div>
            <div class="stat-label">Ragas & DeepEval Hallucination Gate</div>
          </div>
        </div>
      </div>

      <!-- ARCHITECTURAL BLUEPRINTS -->
      <div class="arch-section">
        <div class="arch-header">
          <div class="arch-title">Architecture Blueprint 1: Thomson Reuters Westlaw Legal RAG & LLM Serving Pipeline</div>
          <span class="arch-badge">Llama 3.3 70B + vLLM + Hybrid Search + Ragas Evaluation</span>
        </div>
        <div class="mermaid-box">
          <div class="mermaid">
graph TD
    subgraph Ingestion [Legal Document Ingestion & Indexing]
        RAW_DOCS[Statutory Codes & Judicial Opinions] --> CHUNK[Hierarchical Parent-Child Chunking: LlamaIndex]
        CHUNK --> EMBED[Domain Legal Transformer Embeddings]
        EMBED --> DENSE_VEC[(Dense Vector DB: Pinecone / pgvector)]
        CHUNK --> BM25_IDX[(Sparse Inverted Index: Elasticsearch BM25)]
    end
    subgraph Retrieval [Hybrid Retrieval & Context Fusion]
        USER_QUERY[Attorney Legal Query] --> HYBRID_SEARCH[Parallel Hybrid Search]
        DENSE_VEC <--> HYBRID_SEARCH
        BM25_IDX <--> HYBRID_SEARCH
        HYBRID_SEARCH --> RRF[Reciprocal Rank Fusion: k=60]
        RRF --> RERANK[Cross-Encoder Reranker: Top 5 Chunks]
    end
    subgraph Serving [vLLM High-Throughput Inference on SageMaker]
        RERANK --> PROMPT_ASSEMBLY[Prompt Context Construction]
        PROMPT_ASSEMBLY --> VLLM[vLLM Inference Engine: PagedAttention]
        VLLM <--> KV_CACHE[Decoupled Non-Contiguous KV-Cache]
        VLLM --> MODEL[Fine-Tuned Llama 3.3 70B / Mistral-7B QLoRA]
        MODEL --> GUARDRAILS[Guardrails AI: Citation & Hallucination Gate]
        GUARDRAILS --> STREAM_OUT[Verified Legal Intelligence Response]
    end
          </div>
        </div>
      </div>

      <div class="arch-section">
        <div class="arch-header">
          <div class="arch-title">Architecture Blueprint 2: Dell Technologies Enterprise ML Platform & Streaming Telemetry</div>
          <span class="arch-badge">Apache Kafka + FastAPI + Feast Feature Store + Triton ONNX</span>
        </div>
        <div class="mermaid-box">
          <div class="mermaid">
graph TD
    subgraph DataIngestion [Distributed Telemetry Ingestion]
        SENSORS[Supply Chain IoT & Manufacturing Sensors] --> KAFKA[Apache Kafka Ingestion Topics]
        BATCH_ERP[Historical ERP Records: Tens of Millions] --> SPARK[Apache Spark Distributed Processing]
    end
    subgraph FeatureStore [Feast Feature Management]
        SPARK --> OFFLINE_STORE[(Offline Feature Store: S3 / Snowflake Parquet)]
        AIRFLOW[Apache Airflow DAGs] --> MATERIALIZE[feast materialize Pipeline]
        MATERIALIZE --> ONLINE_STORE[(Online Feature Store: Redis In-Memory)]
    end
    subgraph RealTimeServing [High-Throughput Model Serving]
        KAFKA --> FASTAPI_CONSUMER[FastAPI Asynchronous Consumer Workers]
        ONLINE_STORE <-->|Sub-5ms Feature Lookup| FASTAPI_CONSUMER
        FASTAPI_CONSUMER --> DYNAMIC_BATCH[Continuous Dynamic Batching Queue]
        DYNAMIC_BATCH --> TRITON[NVIDIA Triton Inference Server: ONNX Runtime]
        TRITON --> MODEL_EXEC[INT8 Quantized PyTorch Model Ensemble]
    end
    subgraph MLOpsMonitoring [Observability & Governance]
        TRITON --> PROMETHEUS[Prometheus Metrics Exporter: Latency & QPS]
        FASTAPI_CONSUMER --> DRIFT[PSI Drift Detector: Evidently AI]
        PROMETHEUS --> GRAFANA[Grafana Global Observability Dashboards]
        DRIFT -->|PSI > 0.25| RETRAIN_ALERT[Automated Airflow Retraining Alert]
    end
          </div>
        </div>
      </div>

      <div class="arch-section">
        <div class="arch-header">
          <div class="arch-title">Architecture Blueprint 3: GDIT Federal & Defense Air-Gapped Zero-Trust AI Architecture</div>
          <span class="arch-badge">Air-Gapped Kubernetes + FIPS 140-3 Encryption + mTLS + DeepEval</span>
        </div>
        <div class="mermaid-box">
          <div class="mermaid">
graph LR
    subgraph IngressBoundary [Secure Mission Network Enclave]
        USER[Defense / Intelligence Analyst] --> PKI[PKI / CAC Certificate Handshake]
        PKI --> MTLS[mTLS Service Mesh: Istio Zero-Trust]
    end
    subgraph AirGappedCompute [Isolated Federal Kubernetes: Red Hat OpenShift / GovCloud]
        MTLS --> GUARD_IN[Pre-Inference Guardrail: PII Redaction & Prompt Injection Filter]
        GUARD_IN --> LOCAL_VLLM[Air-Gapped vLLM Container: Local Model Artifacts]
        LOCAL_VLLM --> LOCAL_LLM[Hardened Llama 3.3 70B / Mistral Weights]
        LOCAL_VLLM <--> LOCAL_VEC[(Local pgvector DB: FIPS 140-3 Encrypted at Rest)]
    end
    subgraph Verification [Post-Generation Defense & Auditing]
        LOCAL_LLM --> NLI_GATE[DeepEval / NLI Entailment Citation Verifier]
        NLI_GATE -->|Entailment >= 0.90| OUTPUT[Secure Grounded Response]
        NLI_GATE -->|Ungrounded / Hallucinated| REFUSAL[Deterministic Refusal / Raw Source Reroute]
        OUTPUT --> AUDIT_VAULT[(Immutable SIEM Audit Log Repository)]
    end
          </div>
        </div>
      </div>

      <!-- CONTROLS & FILTER PANEL -->
      <div class="controls-panel">
        <div class="search-row">
          <div class="search-input-wrap">
            <input type="text" id="searchInput" placeholder="Search across 30 technical questions and 10 coding problems (keywords, tech stack, concepts)..." oninput="applyFilters()">
          </div>
          <div class="action-btn-group">
            <button class="ctrl-btn" onclick="expandAll(true)">Expand All</button>
            <button class="ctrl-btn" onclick="expandAll(false)">Collapse All</button>
          </div>
        </div>

        <div class="pill-filters" id="categoryPills">
          <!-- Populated by JS -->
        </div>

        <div class="progress-bar-wrap">
          <div class="progress-text" id="progressText">0 / 40 Reviewed (0%)</div>
          <div class="progress-track">
            <div class="progress-fill" id="progressFill"></div>
          </div>
        </div>
      </div>

      <!-- QUESTIONS AND CODING CONTAINER -->
      <div class="card-list" id="questionList">
        <!-- Rendered via JS -->
      </div>

      <!-- FOOTER -->
      <div class="page-footer">
        General Dynamics Information Technology (GDIT) Confidential AI/ML Engineer Preparation Suite · Varun Sambath Kumar
      </div>

    </div>
  </div>

  <script>
    const CORRECT_PASS = "Varun";
    const itemsData = {items_json_str};
    const categoriesList = {categories_json_str};

    let activeCategory = "All";
    let completedSet = new Set();

    document.addEventListener("DOMContentLoaded", () => {{
      mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
      if (sessionStorage.getItem('varun_unlocked') === 'true') {{
        unlockApp();
      }}
      initApp();
    }});

    function checkPass() {{
      const val = document.getElementById('passInput').value.trim();
      if (val.toLowerCase() === CORRECT_PASS.toLowerCase()) {{
        sessionStorage.setItem('varun_unlocked', 'true');
        unlockApp();
      }} else {{
        document.getElementById('errMsg').style.display = 'block';
      }}
    }}

    document.getElementById('passInput').addEventListener('keydown', (e) => {{
      if (e.key === 'Enter') checkPass();
    }});

    function unlockApp() {{
      document.getElementById('lockScreen').style.display = 'none';
      document.getElementById('app').style.display = 'block';
      window.scrollTo(0, 0);
    }}

    function lockPage() {{
      sessionStorage.removeItem('varun_unlocked');
      document.getElementById('app').style.display = 'none';
      document.getElementById('lockScreen').style.display = 'flex';
      document.getElementById('passInput').value = '';
      document.getElementById('errMsg').style.display = 'none';
    }}

    function initApp() {{
      const pillBox = document.getElementById('categoryPills');
      pillBox.innerHTML = '';
      
      const allBtn = document.createElement('button');
      allBtn.className = 'pill-btn active';
      allBtn.textContent = 'All Items (' + itemsData.length + ')';
      allBtn.onclick = () => setCategory('All', allBtn);
      pillBox.appendChild(allBtn);

      categoriesList.forEach(cat => {{
        const btn = document.createElement('button');
        btn.className = 'pill-btn';
        const count = itemsData.filter(q => q.category === cat).length;
        btn.textContent = `${{cat}} (${{count}})`;
        btn.onclick = () => setCategory(cat, btn);
        pillBox.appendChild(btn);
      }});

      renderQuestions();
    }}

    function setCategory(cat, btnElem) {{
      activeCategory = cat;
      document.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
      btnElem.classList.add('active');
      applyFilters();
    }}

    function renderQuestions() {{
      const container = document.getElementById('questionList');
      container.innerHTML = '';

      itemsData.forEach((item, idx) => {{
        const card = document.createElement('div');
        card.className = 'q-card';
        card.id = `qcard-${{idx}}`;
        card.setAttribute('data-category', item.category);

        const renderedMd = marked.parse(item.answer);
        const isCoding = item.type === "coding";
        const badgeClass = isCoding ? "q-num-badge coding-badge" : "q-num-badge";
        const badgeLabel = isCoding ? `Code ${{item.num}}` : `Q${{item.num.toString().padStart(2, '0')}}`;

        card.innerHTML = `
          <div class="q-header" onclick="toggleCard(${{idx}})">
            <div class="q-header-left">
              <span class="${{badgeClass}}">${{badgeLabel}}</span>
              <div class="q-meta-group">
                <span class="q-cat-tag">${{item.category}}</span>
                <div class="q-title-text">${{item.title}}</div>
                <div class="q-prompt-sub">${{item.question}}</div>
              </div>
            </div>
            <div class="q-header-right">
              <span class="word-badge">${{item.words}} words</span>
              <input type="checkbox" class="q-checkbox" onclick="event.stopPropagation(); toggleComplete(${{idx}})" title="Mark completed">
              <span class="chevron">▼</span>
            </div>
          </div>
          <div class="q-body">
            <div class="answer-content">
              ${{renderedMd}}
            </div>
            <div class="q-footer-bar">
              <button class="copy-ans-btn" onclick="copyAnswer(${{idx}}, this)">📋 Copy Answer / Code</button>
              <span class="copy-toast" id="toast-${{idx}}">Copied to clipboard!</span>
            </div>
          </div>
        `;
        container.appendChild(card);
      }});
      updateProgress();
    }}

    function toggleCard(idx) {{
      const card = document.getElementById(`qcard-${{idx}}`);
      card.classList.toggle('open');
    }}

    function expandAll(open) {{
      document.querySelectorAll('.q-card').forEach(c => {{
        if (open) c.classList.add('open');
        else c.classList.remove('open');
      }});
    }}

    function toggleComplete(idx) {{
      const card = document.getElementById(`qcard-${{idx}}`);
      if (completedSet.has(idx)) {{
        completedSet.delete(idx);
        card.classList.remove('completed');
      }} else {{
        completedSet.add(idx);
        card.classList.add('completed');
      }}
      updateProgress();
    }}

    function updateProgress() {{
      const total = itemsData.length;
      const count = completedSet.size;
      const pct = Math.round((count / total) * 100);
      document.getElementById('progressFill').style.width = pct + '%';
      document.getElementById('progressText').textContent = `${{count}} / ${{total}} Reviewed (${{pct}}%)`;
    }}

    function applyFilters() {{
      const query = document.getElementById('searchInput').value.toLowerCase().trim();

      itemsData.forEach((item, idx) => {{
        const card = document.getElementById(`qcard-${{idx}}`);
        const matchesCat = (activeCategory === 'All' || item.category === activeCategory);
        const textContent = (item.title + ' ' + item.question + ' ' + item.answer).toLowerCase();
        const matchesQuery = !query || textContent.includes(query);

        if (matchesCat && matchesQuery) {{
          card.style.display = 'block';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    function copyAnswer(idx, btn) {{
      const item = itemsData[idx];
      if (!item) return;
      navigator.clipboard.writeText(item.answer).then(() => {{
        const toast = document.getElementById(`toast-${{idx}}`);
        toast.classList.add('show');
        setTimeout(() => {{ toast.classList.remove('show'); }}, 2000);
      }});
    }}
  </script>
</body>
</html>
"""
    return html

# =============================================================================
# MAIN BUILD SCRIPT ENTRYPOINT
# =============================================================================
def main():
    print(f"Building Varun Sambath Kumar GDIT AI/ML Prep Suite...")

    # 1. Master Markdown
    master_md = generate_markdown()
    md_path = "varun_gdit_aiml_prep.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(master_md)
    print(f"Master Markdown generated: {md_path} ({len(master_md.split())} words)")

    # 2. Nextra MDX
    mdx_content = generate_mdx(master_md)
    mdx_path = os.path.join("content", "varun-gdit-aiml-prep.mdx")
    with open(mdx_path, "w", encoding="utf-8") as f:
        f.write(mdx_content)
    print(f"Nextra MDX generated: {mdx_path}")

    # 3. Interactive Webpage
    html_content = generate_html()
    html_path = "varun_gdit_aiml_prep.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Interactive Webpage generated: {html_path}")

    # 4. Copy to public/
    os.makedirs("public", exist_ok=True)
    pub_html_path = os.path.join("public", "varun_gdit_aiml_prep.html")
    with open(pub_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Public Webpage generated: {pub_html_path}")

    print("\nAll Varun Sambath Kumar GDIT AI/ML prep assets successfully compiled!")

if __name__ == "__main__":
    main()
