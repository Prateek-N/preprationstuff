---
title: Sirisha GenAI Solutions Prep Guide
description: Comprehensive preparation guide for the Advanced GenAI Software Engineer interview, customized for Sirisha Nelapudi.
---

# Sirisha Nelapudi Prep Guide: Advanced GenAI Software Engineer

Welcome to your preparation guide for the Advanced GenAI Software Engineer role. This guide is tailored around your experience in financial microservices, Generative AI agent orchestration, and DevOps at Morgan Stanley, Liberty Mutual, and Dell Technologies, mapping those competencies directly to the job description requirements (LangGraph, LlamaIndex, async FastAPI, PyTorch/TensorFlow fine-tuning, model swapping, and Docker).

---

## Resume & Role Alignment

The Advanced GenAI Software Engineer role requires developing sophisticated multi-agent architectures, maintaining advanced RAG systems, integrating commercial/open-source LLMs, designing async FastAPI backends, and fine-tuning models using PyTorch or TensorFlow.

Here is how your background directly bridges to these requirements:

*   **LangGraph & Multi-Agent Workflows:** At Morgan Stanley, you engineered **Generative AI agents** using **LangChain** and **LangGraph** to automate technical documentation retrieval, reclaiming 14 hours per sprint. This directly maps to the core requirement of orchestrating sophisticated multi-agent architectures.
*   **Data Ingestion & Backend Performance:** Your design of cloud-native data ingestion layers on **Azure Cloud** with **Azure Functions** and your optimization of Spring Boot microservices processing 4 TB of transactional data for 18,000+ users prepare you to build high-performance, asynchronous backends using **FastAPI** and **Async Python**.
*   **Deep Learning & Model Training:** Your research and projects using **TensorFlow**, **Keras**, and **PyTorch** to build GANs/VAEs (achieving 1.8 FID scores) and automate blood classification establish the deep learning foundation required to fine-tune large language models.
*   **Containerization & DevOps:** Your hands-on experience containerizing deployments using **Docker** and **Kubernetes**, deploying IaC with **Terraform**, and automating CI/CD with **GitHub Actions** and **Jenkins** aligns perfectly with the requirement to containerize and deploy AI services to production.

---

## Part 1: Top 30 Technical & Behavioral Questions & Answers

### 1. How does your experience with LangGraph at Morgan Stanley map to the multi-agent architectures required in this role?
At **Morgan Stanley**, I engineered **Generative AI agents** using **LangChain** and **LangGraph** to automate technical documentation retrieval, reclaiming 14 hours per sprint for the senior engineering team. LangGraph is a library designed for building stateful, multi-actor applications with LLMs, making it the ideal framework for sophisticated multi-agent orchestration. In my previous work, I structured the retrieval process as a stateful graph where different nodes represented specialized agents—such as a query parsing agent, a vector search routing agent, and a document summarizing agent. By maintaining a centralized state across nodes, I could implement loop controls, enabling agents to self-correct and re-query the vector index if the retrieved context was deemed low-quality by an evaluation check. This directly maps to the role's core requirement of developing sophisticated multi-agent architectures. At your organization, I will leverage this expertise to build nested, agentic loops that coordinate task execution, manage memory state, and route tasks dynamically. I will design custom state reducers and conditional edges, ensuring that complex business workflows, such as financial audits or customer support triaging, can execute asynchronously and reliably in production environments, fully utilizing LangGraph's capability for cycle management.

### 2. Can you explain how you would design an Advanced RAG system using LlamaIndex and vector databases?
To design an **Advanced RAG** system using **LlamaIndex**, I would implement a multi-stage retrieval and generation pipeline. First, during the ingestion stage, I would use LlamaIndex’s node parsers to segment documents based on semantic boundaries rather than arbitrary token counts, appending metadata tags (such as document type, date, and access controls) to each node. I would index these nodes in a vector database, such as **Pinecone** or **PGVector**. For retrieval, I would build a **RouterQueryEngine** that dynamically chooses between a vector index (for semantic queries) and a structured SQL index (for metadata or numerical filtering), combining results via hybrid search. The retrieved context would pass through a **Re-ranker** model (like Cohere ReRank) to surface the top-K most relevant nodes, minimizing the prompt context size. Finally, the context is formatted into a prompt template and sent to the LLM. Using LlamaIndex's advanced query pipelines, I would implement self-querying and agentic retrieval loops, allowing the system to query the database multiple times if initial context is incomplete. This ensures high-accuracy retrieval, which is critical when extracting data from complex financial or technical documents.

### 3. How do you handle database concurrency and deadlock resolution, drawing on your experience at Morgan Stanley?
At **Morgan Stanley**, I resolved 25 database deadlocks per production cycle in financial microservices, maintaining data consistency across 12 staging clusters. Deadlocks occur when two or more transactions hold locks on different resources and each attempts to acquire a lock on the resource held by the other. To mitigate deadlocks, I first analyzed query execution plans in **PostgreSQL** to identify unindexed foreign keys and slow-running queries. I implemented strict index strategies to ensure database updates executed quickly, reducing lock holding times. I restructured our Spring Boot transaction boundaries to ensure that all services updated database resources in the exact same logical order, preventing cyclic dependency locks. Furthermore, I integrated **Redis** caching to offload read traffic from the primary database, reducing transactional contention. When designing high-performance GenAI backends with **FastAPI** and **asyncpg** in Python, I will apply similar principles. I will configure transaction isolation levels appropriately, utilize optimistic locking where applicable, implement connection pooling, and run non-blocking database queries asynchronously to maximize concurrency while protecting Natera’s databases from deadlock bottlenecks.

### 4. Walk us through how you would integrate and swap diverse LLMs based on performance and cost requirements.
To enable flexible model swapping, I would design a unified model gateway interface using **FastAPI**. I would define a standard abstract class for LLM client wrappers, ensuring that commercial models (like **Azure OpenAI** or Claude API) and self-hosted open-source models (like LLaMA-3 running via **vLLM** on Kubernetes) conform to the same request-response interface. The gateway would utilize a routing controller that reads configuration rules from a **Redis** database. When a request arrives, the router checks the task classification. For high-priority, complex tasks (such as code generation or complex reasoning), the router maps the request to a frontier model like GPT-4. For high-volume, structural extractions (like formatting logs or parsing simple values), the router maps the request to a cheaper, hosted model like LLaMA-3-8B. The router would also monitor latency and cost statistics: if a commercial API experiences a timeout or rate-limit error, the gateway automatically executes a fallback redirect to the self-hosted model. This dynamic swapping abstraction ensures our AI solutions remain cost-effective, high-performing, and resilient to third-party outages.

### 5. What is the difference between synchronous and asynchronous programming in Python? Why is FastAPI preferred for GenAI backends?
Synchronous programming executes instructions sequentially, meaning if a function blocks on a network call (like an LLM API request), the entire thread freezes until the response returns, wasting CPU cycles. Asynchronous programming uses an event loop to run tasks concurrently on a single thread. When an asynchronous function hits an await point, the event loop pauses that task and runs other pending coroutines, resuming the original task once the network response is ready. **FastAPI** is designed from the ground up to support **Async Python**, utilizing Starlette and Uvicorn to handle thousands of concurrent requests with minimal overhead. In GenAI applications, where model API calls or vector database queries can take hundreds of milliseconds to seconds, a synchronous backend would quickly saturate its thread pool and reject new requests. By writing async handlers in FastAPI, we ensure the server remains highly responsive, routing incoming user queries and handling Webhooks concurrently, maximizing throughput without requiring expensive hardware scaling.

### 6. How would you approach fine-tuning a large language model (LLM) using PyTorch or TensorFlow for domain-specific tasks?
To fine-tune an LLM, I would use **PyTorch** paired with Hugging Face's **PEFT** (Parameter-Efficient Fine-Tuning) and **TRL** (Transformer Reinforcement Learning) libraries. First, I would prepare a clean, domain-specific instruction dataset in JSONL format, ensuring it undergoes duplicate checks and length filtering. I would load the base model in 4-bit precision using bitsandbytes to reduce GPU memory requirements. I would then configure **LoRA** (Low-Rank Adaptation), targeting the attention projection matrices (`q_proj`, `v_proj`) to add trainable low-rank adapters while keeping the base model weights frozen. During training, I would monitor the training loss and validation perplexity curves to detect overfitting, adjusting learning rates with a cosine scheduler. Once training completes, I would merge the LoRA weights back into the base model and evaluate its performance against our golden dataset, using tools like MLflow to track parameters and metrics. This efficient approach allows us to specialize models for specific domains (like underwriting calculations or diagnostic coding) with minimal compute overhead.

### 7. How did you design cloud-native data ingestion layers on Azure with Azure Functions at Morgan Stanley?
At **Morgan Stanley**, I designed cloud-native data ingestion layers on **Azure Cloud** utilizing **Azure Functions** and **Azure AI** services. This architecture automated the encryption and processing of sensitive financial transaction records, sustaining 800+ inference requests per hour. I configured Azure Functions to run as event-triggered serverless microservices. When a new transaction record arrived in our Azure Blob Storage, it triggered an Azure Function that decrypted the data, validated the schema, and sent the records to our processing pipeline. To protect sensitive customer details, I integrated Azure Key Vault to manage encryption keys securely, ensuring compliance with strict data security standards. This serverless ingestion pattern is highly applicable to GenAI workflows. I will use Azure Functions or AWS Lambda to build serverless preprocessing workers that ingest raw document uploads, run OCR pipelines, and index text chunks into our vector database asynchronously, ensuring our systems scale dynamically in response to workload spikes.

### 8. Explain how you use Terraform to standardise deployment environments, drawing on your Morgan Stanley experience.
At **Morgan Stanley**, I deployed Infrastructure as Code (IaC) using **Terraform** to standardize deployment environments across our cloud microservices. Before implementing IaC, manual configuration of cloud environments led to system configuration drift, where staging and production clusters had slight differences in permissions, subnets, or resource sizes, causing hard-to-debug deployment failures. By writing Terraform configuration files, I defined all cloud resources—such as virtual networks, Kubernetes clusters, database instances, and IAM access controls—as code. I used Terraform state files to track deployed infrastructure, enabling automated environment provisioning within our CI/CD pipelines. This standardisation reduced deployment-related configuration drift and accelerated our release cycles. For GenAI engineering, I will write Terraform manifests to automate the provisioning of vector database clusters, GPU VM instances, model gateway routing subnets, and API storage backends, ensuring our deployments are reproducible, secure, and easily auditable.

### 9. What cache strategies did you implement with Redis at Morgan Stanley to optimize query performance?
At **Morgan Stanley**, I developed Spring Boot applications with **Redis** caching strategies to optimize query performance for 18,000+ active users. Financial modules frequently query static or slow-changing data, such as market tickers, security configurations, or user profile metadata. Querying the primary PostgreSQL database for every request created performance bottlenecks and database lock contention. I implemented a Cache-Aside pattern: when a request arrived, the microservice first queried the Redis cache. If a cache miss occurred, the service queried the PostgreSQL database, wrote the retrieved data to Redis, and returned it to the client. I configured Time-to-Live (TTL) values for cached keys to ensure data freshness, and implemented cache eviction policies (like Least Recently Used) to prevent memory exhaustion. In GenAI systems, I will use Redis to cache semantic embeddings, common LLM response patterns, and user session states, preventing redundant LLM API calls and reducing system latency.

### 10. How would you containerize and deploy an async FastAPI GenAI service using Docker to Kubernetes?
To containerize a FastAPI GenAI service, I would write a multi-stage **Dockerfile**. In the builder stage, I install the Python dependencies (FastAPI, uvicorn, LlamaIndex, PyTorch) into a virtual environment. In the runner stage, I copy only the built virtual environment into a slim, GPU-enabled CUDA base image, reducing the final container size and security vulnerability footprint. I expose port 8000 and run the service using Uvicorn: `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]`. For deployment, I write a Kubernetes Deployment manifest, specifying resource limits (CPU, memory, and Nvidia GPU allocations) and defining liveness and readiness probes to check our API health endpoint. I configure a Horizontal Pod Autoscaler to scale the pods based on CPU usage or custom latency metrics, ensuring the service remains highly available under load.

### 11. How do you integrate Python-based server environments with Java Spring Boot microservices, referencing your Liberty Mutual experience?
At **Liberty Mutual**, I led the integration of Python-based server environments with **Java Spring Boot** microservices, maintaining high-availability systems for 18,000 active policyholders. Enterprise architectures often use Java for robust, transactional core logic, while Python is preferred for data science, machine learning, and AI workloads. To connect these two environments, I designed a RESTful communication layer where the Spring Boot microservice acted as the primary orchestrator, routing calculation requests to the Python server via HTTP POST payloads. I used JSON schemas to enforce strict data formatting across both systems, and implemented Apache Kafka as an asynchronous event bus to handle long-running, non-blocking calculations without coupling the services. This integration pattern is crucial when inserting new GenAI capabilities into existing enterprise software. I will ensure that Natera's legacy backend systems integrate seamlessly with our new GenAI FastAPI microservices using clean REST APIs, message queues, and robust schema validation.

### 12. Explain the concept of vector embeddings and hybrid search in a vector database.
Vector embeddings are mathematical representations of unstructured data (like text, images, or audio) as high-dimensional vectors, where the distance between vectors represents the semantic similarity between the corresponding data points. In a RAG system, user queries and document chunks are converted into embeddings using models like OpenAI's `text-embedding-3-small`. When a query occurs, the vector database performs a cosine similarity or inner product search to retrieve the closest vectors. **Hybrid search** combines this semantic vector search with traditional keyword-based lexical search (like **BM25**). Vector search excels at capturing semantic intent but can miss exact keyword matches (like serial numbers, medical codes, or vendor IDs). Lexical search excels at keyword accuracy but misses context. By running both in parallel and merging their scores using Reciprocal Rank Fusion (RRF), we achieve high-accuracy retrieval that captures both context and exact terms.

### 13. What is the role of an event loop in Async Python? How do you prevent blocking it?
The event loop is the core of **Async Python**'s concurrency model. It manages and distributes the execution of asynchronous tasks, pausing coroutines when they await an external I/O operation and running other tasks in the meantime. Because the event loop runs on a single thread, executing any synchronous, CPU-bound code (such as large matrix operations, heavy data cleaning with Pandas, or image processing) directly inside an async function will block the event loop, freezing all other concurrent tasks. To prevent this, any CPU-bound or blocking synchronous code must be offloaded to a separate thread or process pool using FastAPI's background tasks or Python's `asyncio.to_thread()` wrapper. This ensures the event loop remains free to route incoming network requests and dispatch tasks without latency spikes.

### 14. How would you design a CI/CD pipeline for an LLM application using GitHub Actions and Docker?
I would design a CI/CD pipeline using **GitHub Actions** triggered upon code push or pull requests. First, the workflow runs code formatting checks and executes unit tests using JUnit or pytest, checking prompt templates and parser code. Next, the pipeline triggers security scanners to check for exposed secrets and dependencies vulnerabilities. If tests pass, the pipeline builds the service's **Docker** image, tags it with the git commit SHA, and pushes it to a secure Container Registry (like Azure Container Registry). Finally, the workflow uses Terraform or kubectl configurations to trigger a rolling update on our staging Kubernetes cluster, ensuring zero-downtime deployment. I would integrate automated model evaluation runs in the staging deployment step, running our RAGAS validation suite before promoting the release to production.

### 15. How do you validate generative AI outputs to ensure they conform to structured formats like JSON?
To ensure LLM outputs conform to structured formats, I use **JSON Schema** validation enforced through **Pydantic** models in Python. When making an API call to OpenAI or a self-hosted model, I configure the API request to use structured outputs, passing the target Pydantic schema class directly. This forces the model's token selection path to adhere strictly to the JSON schema. If the model is accessed without built-in structured output support, I write a validator wrapper: when the response arrives, the wrapper parses the string as JSON and attempts to instantiate the Pydantic model. If validation fails due to missing keys or type mismatches, the wrapper captures the error, appends it to a self-correction prompt, and executes a retry loop asking the model to fix its formatting errors, guaranteeing clean JSON delivery.

### 16. Describe the trade-offs between PEFT/LoRA and full fine-tuning of an LLM.
Full fine-tuning updates all parameters of a model, requiring massive GPU memory (roughly 16-24GB of VRAM per billion parameters just for training states) and producing a complete new set of model weights, which is expensive to store and deploy. Parameter-Efficient Fine-Tuning (**PEFT**) via **LoRA** keeps the base model weights frozen and trains a small set of adapter layers inserted into the attention blocks. The trade-offs are:
*   **Compute Cost:** LoRA drastically reduces VRAM requirements (by up to 80%), allowing fine-tuning on consumer-grade GPUs.
*   **Storage:** LoRA adapters are tiny (megabytes instead of gigabytes), enabling us to swap task-specific adapter weights dynamically at runtime while sharing a single base model instance.
*   **Quality:** Full fine-tuning can achieve slightly higher accuracy on highly specialized languages or formatting tasks, but LoRA performs comparably on most classification, extraction, and instruction-following tasks.

### 17. How does a Transformer model work? What is the self-attention mechanism?
A Transformer is a deep learning architecture based on an encoder-decoder structure that processes sequential data in parallel, unlike traditional sequential RNNs. The core innovation is the **self-attention mechanism**. Self-attention calculates a weight score for every word in a sequence relative to every other word, determining how much focus to place on different parts of the sentence. It does this by creating three vectors for each input token: Queries (Q), Keys (K), and Values (V). The attention score is computed as:
$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$.
This calculation allows the model to capture long-range contextual relationships (e.g., matching a pronoun to a noun far earlier in the text) regardless of their distance in the sequence, forming the foundation of modern large language models.

### 18. What is prompt injection? How do you defend against it in multi-agent architectures?
Prompt injection is an exploit where an attacker inputs malicious text designed to override the system instructions of an LLM, forcing the agent to execute unauthorized commands, leak confidential data, or output toxic content. In multi-agent systems, defending against this is critical because a compromised agent could trigger APIs or execute destructive tools. We defend against this by implementing input sanitization filters that check user queries against blocklists, separating system instructions from user variables using clear delimiters, and enforcing strict validation on all agent tool calls. We also apply the principle of least privilege, ensuring that agents only have access to the specific tools and data collections required for their tasks, and run crucial tool executions through human-in-the-loop checkpoints.

### 19. How do you monitor GenAI workflows for latency, cost, and reliability in production?
To monitor GenAI workflows, I instrument our FastAPI endpoints with OpenTelemetry middleware to collect metrics and export them to Prometheus. We track three primary dimensions:
*   **Latency:** We trace time-to-first-token (TTFT) and total generation latency, segmenting these by model provider and routing path.
*   **Cost:** We log token consumption (input, output, and cached tokens) for every request, calculating running costs in real-time.
*   **Reliability:** We monitor model HTTP error rates (like 429 rate limits or 503 timeouts) and output quality metrics. We display these statistics on Grafana dashboards and set up automated Slack alerts to notify the engineering team if error rates exceed one percent or latency exceeds predefined SLAs.

### 20. How would you design a test suite for prompt templates to prevent regression during model updates?
To prevent prompt regression, I would build an automated evaluation test suite. First, I would compile a golden dataset of test cases, containing diverse queries, context documents, and expected ground-truth answers. When a developer updates a prompt template, our CI/CD pipeline triggers a test run that runs these queries through the updated template using a test LLM instance. We use evaluation frameworks like RAGAS or custom LLM-as-a-Judge scoring to compare the new outputs against the ground-truth answers, measuring correctness, format adherence, and toxicity. The pipeline blocks the commit if the average evaluation score falls below our quality threshold, ensuring prompt updates never degrade production system quality.

### 21. How do you optimize query latency in LlamaIndex when retrieving from a large vector database?
To optimize retrieval latency, I implement several query optimization techniques:
*   **Pre-filtering:** I apply strict metadata filters (e.g., document ID, creation date) to the database query, narrowing down the vector search space.
*   **Hybrid Search:** I run parallel vector and keyword lookups and limit the initial retrieval to the top-50 results.
*   **Re-ranking:** I pass the initial top-50 nodes through a fast re-ranking model (like Cohere ReRank) to select only the top-5 most relevant nodes for the final prompt context, reducing prompt token processing overhead.
*   **Caching:** I cache semantic query embeddings and common search results in Redis, bypassing vector database lookups for repeated queries.

### 22. What is a stateful agent? How does LangGraph handle agent state across execution cycles?
A stateful agent is an AI workflow that maintains a persistent memory of previous interactions, decisions, and data inputs across multiple execution steps. **LangGraph** manages this state using a centralized state schema (often defined as a Pydantic model or TypedDict) that is passed to every node in the graph. When a node (an agent or tool) executes, it returns an update dictionary. LangGraph uses pre-defined reducer functions to merge these updates back into the central state (e.g., appending new messages to a message list). This state is stored in a durable checkpoint saver (like Postgres or Redis), allowing workflows to pause, wait for external inputs or human approvals, and resume execution without losing their history.

### 23. What are the security risks of allowing AI agents to call database execution tools? How do you mitigate them?
Allowing agents to call database tools introduces SQL injection risks, unauthorized data access, and potential database corruption if an agent runs a destructive query (like `DROP TABLE`). To mitigate these risks, agents must never generate or execute raw SQL directly. Instead, we expose restricted tool APIs that run parameterized SQL queries with strict input validation. The database connection used by the agent must have read-only permissions on a limited set of tables. We also run any data modification commands through human-in-the-loop validation checkpoints, requiring explicit administrator approval before execution.

### 24. Explain how you would implement model fallbacks and retry logic in FastAPI backends.
I would implement fallbacks and retries using Python’s async libraries and the Tenacity retry decorator. When a FastAPI endpoint initiates an LLM call, we wrap the request in a retry handler configured to catch transient errors (such as HTTP 429 rate limits or HTTP 503 service unavailable). The handler attempts the call up to three times with exponential backoff and random jitter. If all retries fail, the handler catches the exception, logs a warning, and automatically swaps the target model to our fallback provider (e.g., falling back from a commercial API to our self-hosted LLaMA model). This ensure that client requests succeed even during model provider outages.

### 25. How do you design and test prompt engineering constraints to enforce output formatting guidelines?
To enforce output formatting, I use strict system instructions, few-shot examples, and structural schema definitions. In the prompt template, I explicitly define the expected output format (such as a structured JSON object) and include examples showing correct and incorrect responses. I test these templates by running batch queries through our test suite, using regex and json parsers to verify that the LLM output can be successfully parsed. If a template fails formatting validation during testing, I iterate on the prompt constraints, making the instructions more explicit and removing ambiguous wording.

### 26. Describe how you would handle long-running, asynchronous LLM workflows in a FastAPI backend.
To handle long-running workflows (which can take minutes to complete), I use an asynchronous queue architecture. When a request arrives, the FastAPI endpoint validates the input, generates a unique task ID, pushes the task to a Celery or RabbitMQ queue, and immediately returns a `202 Accepted` status with the task ID. Background worker processes consume the queue and run the LLM workflow. The client can poll a separate `/status/{task_id}` endpoint to check progress, or configure a webhook URL that our background worker calls with the final results once processing completes, preventing HTTP timeouts.

### 27. What metrics do you track to evaluate GAN and VAE performance, drawing on your projects?
In my image generation project, I engineered hybrid GAN and VAE models in **TensorFlow** and Keras to reconstruct 60,000 images, and evaluated their performance using two key metrics:
*   **Fréchet Inception Distance (FID):** FID measures the similarity between the feature representations of generated images and real images, with lower scores indicating higher visual quality. I achieved an FID score of 1.8.
*   **Structural Similarity Index (SSIM):** SSIM measures the similarity in luminance, contrast, and structure between two images. By tuning our architectures and loss functions, I optimized convergence and improved SSIM across 10,000 test samples, ensuring high structural fidelity.

### 28. How does a token count rate limiter work? Why is it important in LLM systems?
A token count rate limiter tracks the number of tokens processed by LLM requests over time (e.g., tokens per minute, TPM), rather than just the number of raw API calls (requests per minute, RPM). This is crucial because a single LLM request containing a massive document can consume hundreds of thousands of tokens, which can quickly saturate our API quota and trigger rate-limit errors for all other users. The limiter tracks consumed tokens, and if a new request exceeds the remaining TPM quota, it blocks the call until the quota refills, protecting our applications from service degradation.

### 29. How do you ensure least-privilege access to Azure resources when deploying GenAI containers?
We ensure least-privilege access using Azure Managed Identities and strict Role-Based Access Control (RBAC). Instead of embedding database passwords or API keys inside our Docker containers, we assign a User-Assigned Managed Identity to our Kubernetes pod or Container App. We then configure our Azure databases and Key Vaults to grant read-only or limited permissions specifically to this identity. This ensures that even if a container is compromised, the attacker cannot access other Azure resources, maintaining security compliance.

### 30. How would you handle a situation where a business partner requests an AI workflow that violates data privacy regulations?
As an engineer, maintaining security and compliance is my priority. If a stakeholder requests a workflow that violates regulations (such as sending unmasked patient data to a model that trains on customer inputs), I would schedule a meeting to explain the regulatory risks. I would present a safe, compliant alternative: we can implement a preprocessing pipeline to redact PII, route the queries through our self-hosted models running inside Natera's secure virtual network, or sign business associate agreements (BAAs) with compliant model providers. This protects the company from legal liability while still delivering the business value they need.

---

## Part 2: Top 10 Python Coding Questions

### 1. Async FastAPI Endpoint with Background Tasks for LLM Processing
**Thought Process:**
LLM API calls are slow and can cause HTTP timeouts if executed synchronously. We implement an asynchronous FastAPI endpoint that accepts a query, registers a background task to execute the slow LLM call, and immediately returns a `202 Accepted` status with a task ID, keeping the server highly responsive.

**Python Code:**
```python
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uuid
import asyncio

app = FastAPI()

# Simple task database
tasks = {}

class QueryRequest(BaseModel):
    prompt: str

async def run_llm_inference(task_id: str, prompt: str):
    # Simulate a slow LLM call
    await asyncio.sleep(5)
    tasks[task_id] = {"status": "completed", "result": f"Answer to: {prompt}"}

@app.post("/generate", status_code=202)
async def generate_text(request: QueryRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "pending", "result": None}
    
    # Offload the slow coroutine to background tasks
    background_tasks.add_task(run_llm_inference, task_id, request.prompt)
    return {"task_id": task_id, "status": "pending"}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]
```
*   **Time Complexity:** $O(1)$ endpoint response.
*   **Space Complexity:** $O(T)$ where $T$ is the number of active tasks in memory.

---

### 2. Token Bucket Rate Limiter for LLM Token Counts
**Thought Process:**
LLM providers enforce limits on Tokens Per Minute (TPM). We build an asynchronous token bucket rate limiter to monitor input/output token counts, blocking requests until tokens accumulate.

**Python Code:**
```python
import time
import asyncio

class AsyncTokenRateLimiter:
    def __init__(self, max_tokens: int, refill_rate_per_sec: float):
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate_per_sec
        self.tokens = float(max_tokens)
        self.last_update = time.monotonic()
        self.lock = asyncio.Lock()

    async def acquire(self, tokens_needed: int) -> bool:
        async with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.last_update = now

            # Refill tokens based on elapsed time
            self.tokens = min(self.max_tokens, self.tokens + (elapsed * self.refill_rate))

            if self.tokens >= tokens_needed:
                self.tokens -= tokens_needed
                return True
            return False

    async def wait_and_acquire(self, tokens_needed: int):
        while not await self.acquire(tokens_needed):
            # Back off and wait before checking again
            await asyncio.sleep(0.5)
```
*   **Time Complexity:** $O(1)$ computation.
*   **Space Complexity:** $O(1)$ storage.

---

### 3. Stateful Multi-Agent LangGraph Orchestrator (Mock)
**Thought Process:**
Using LangGraph concepts, we implement a stateful multi-agent system in Python. A central State dictionary stores the query and agent checklist. We define nodes for Risk Analysis and Premium Calculation, and route state transitions based on checklist completion.

**Python Code:**
```python
from typing import Dict, Any, List

class StatefulAgentGraph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name: str, func: callable):
        self.nodes[name] = func

    def execute(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        state = initial_state
        # Run stateful loops based on routing logic
        while "next_node" in state and state["next_node"] is not None:
            node_name = state["next_node"]
            state["next_node"] = None # Reset transition flag
            if node_name in self.nodes:
                state = self.nodes[node_name](state)
            else:
                break
        return state

# Node definitions
def risk_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    state["risk_score"] = 0.35
    state["checklist"].append("risk_checked")
    # Conditional edge logic
    state["next_node"] = "premium_agent"
    return state

def premium_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    if "risk_checked" in state["checklist"]:
        state["premium"] = 1200 * state["risk_score"]
        state["checklist"].append("premium_calculated")
    state["next_node"] = None # Final node
    return state

# Example setup
# graph = StatefulAgentGraph()
# graph.add_node("risk_agent", risk_agent)
# graph.add_node("premium_agent", premium_agent)
# final_state = graph.execute({"checklist": [], "next_node": "risk_agent"})
```
*   **Time Complexity:** $O(N)$ where $N$ is graph nodes visited.
*   **Space Complexity:** $O(S)$ where $S$ is state dictionary storage.

---

### 4. LlamaIndex Custom Router Query Engine (Mock)
**Thought Process:**
A router query engine dynamically forwards a user query to either a relational database index or a vector search index based on semantic classification.

**Python Code:**
```python
class CustomRouterQueryEngine:
    def __init__(self, sql_engine, vector_engine):
        self.sql_engine = sql_engine
        self.vector_engine = vector_engine

    def select_route(self, query: str) -> str:
        # Route logic: if query contains statistics or counts, route to SQL
        keywords = ["how many", "count", "average", "total", "sum", "table"]
        if any(kw in query.lower() for kw in keywords):
            return "sql"
        return "vector"

    def query(self, query_str: str) -> str:
        route = self.select_route(query_str)
        if route == "sql":
            return self.sql_engine.execute_query(query_str)
        else:
            return self.vector_engine.semantic_search(query_str)

# Mock classes for engines
class MockSqlEngine:
    def execute_query(self, q): return f"SQL Result for: {q}"

class MockVectorEngine:
    def semantic_search(self, q): return f"Vector Result for: {q}"
```
*   **Time Complexity:** $O(K \times W)$ where $K$ is keywords and $W$ is words in query.
*   **Space Complexity:** $O(1)$ memory.

---

### 5. Dynamic LLM Gateway with Provider Fallback
**Thought Process:**
To ensure high availability, we build a wrapper client that routes calls to a primary model provider, catching timeouts and switching to a fallback provider dynamically if an error occurs.

**Python Code:**
```python
import asyncio
import random

class LLMGatewayClient:
    def __init__(self, primary_provider: str, fallback_provider: str):
        self.primary = primary_provider
        self.fallback = fallback_provider

    async def _mock_api_call(self, provider: str, prompt: str) -> str:
        # Simulate network failure on primary provider
        if provider == "primary" and random.random() < 0.5:
            raise asyncio.TimeoutError("Primary API timeout")
        await asyncio.sleep(0.5)
        return f"Response from {provider} for: {prompt}"

    async def generate(self, prompt: str) -> str:
        try:
            # Try primary provider first
            return await self._mock_api_call("primary", prompt)
        except asyncio.TimeoutError:
            # Fall back to backup provider immediately
            return await self._mock_api_call("fallback", prompt)
```
*   **Time Complexity:** $O(1)$ call delay.
*   **Space Complexity:** $O(1)$ variables.

---

### 6. PII Masking Filter for Outgoing LLM Requests
**Thought Process:**
To ensure HIPAA/SOC 2 compliance, we write a preprocessing filter that scans prompts using regular expressions to detect and mask social security numbers, email addresses, and phone numbers.

**Python Code:**
```python
import re

class PiiFilter:
    def __init__(self):
        # Compiled patterns
        self.ssn_pattern = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
        self.email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
        self.phone_pattern = re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b")

    def redact(self, text: str) -> str:
        temp = text
        temp = self.ssn_pattern.sub("[REDACTED_SSN]", temp)
        temp = self.email_pattern.sub("[REDACTED_EMAIL]", temp)
        temp = self.phone_pattern.sub("[REDACTED_PHONE]", temp)
        return temp
```
*   **Time Complexity:** $O(N)$ text scanning.
*   **Space Complexity:** $O(N)$ returned string copy.

---

### 7. JSONL Training Dataset Formatter for LLM Fine-Tuning
**Thought Process:**
Before fine-tuning models in PyTorch, we must format our unstructured data into standard instruction JSONL structures, verifying that all keys are present and parsing correctly.

**Python Code:**
```python
import json
from typing import List, Dict

class FineTuningFormatter:
    @staticmethod
    def format_dataset(raw_samples: List[Dict[str, str]]) -> List[str]:
        formatted_lines = []
        for sample in raw_samples:
            instruction = sample.get("instruction")
            output = sample.get("output")
            
            # Skip invalid records
            if not instruction or not output:
                continue

            # Standard instruction-tuning chat structure
            record = {
                "messages": [
                    {"role": "system", "content": "You are a helpful underwriting assistant."},
                    {"role": "user", "content": instruction},
                    {"role": "assistant", "content": output}
                ]
            }
            formatted_lines.append(json.dumps(record))
        return formatted_lines
```
*   **Time Complexity:** $O(D)$ where $D$ is dataset records.
*   **Space Complexity:** $O(D)$ memory array.

---

### 8. Embedding Cosine Similarity Calculator for Routing
**Thought Process:**
Routing user queries requires calculating the similarity between user query vectors and route vectors. We implement cosine similarity:
$\text{Cosine Similarity} = \frac{A \cdot B}{\|A\| \|B\|}$.

**Python Code:**
```python
import math
from typing import List

def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimension")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))

    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0

    return dot_product / (mag_a * mag_b)
```
*   **Time Complexity:** $O(D)$ where $D$ is vector dimension.
*   **Space Complexity:** $O(1)$ computation storage.

---

### 9. Sliding Window Text Chunking with Overlap
**Thought Process:**
To prepare text for indexing, we chunk the string using a sliding window algorithm, maintaining a character overlap to prevent missing contextual boundaries.

**Python Code:**
```python
from typing import List

def get_sliding_window_chunks(text: str, chunk_size: int, overlap: int) -> List[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap >= chunk_size:
        raise ValueError("overlap must be less than chunk_size")

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunks.append(text[start:end])
        if end == text_len:
            break
        # Shift start point by step size (chunk_size - overlap)
        start += chunk_size - overlap

    return chunks
```
*   **Time Complexity:** $O(T)$ where $T$ is text size.
*   **Space Complexity:** $O(T)$ to hold chunked arrays.

---

### 10. Async API Client with Exponential Backoff Retry
**Thought Process:**
Integrations with third-party LLMs can fail due to network drops. We build an async request wrapper that automatically retries the operation with exponential delay.

**Python Code:**
```python
import asyncio
import random

async def call_api_with_retry(api_func: callable, *args, max_retries: int = 4, base_delay: float = 0.5):
    retries = 0
    delay = base_delay

    while True:
        try:
            # Execute async function
            return await api_func(*args)
        except Exception as e:
            retries += 1
            if retries > max_retries:
                raise e
            
            # Exponential backoff with jitter
            jitter = random.uniform(0, delay)
            await asyncio.sleep(jitter)
            delay *= 2.0
```
*   **Time Complexity:** $O(1)$ wrapper routing overhead.
*   **Space Complexity:** $O(1)$ local states.

---

## Part 3: Top 5 High-Level System Designs

This section breaks down the five core system designs. Each design includes its architecture diagram and is explained step by step in a natural, conversational way (without bullet points) covering all requested design perspectives.

---

### 1. High-Performance Multi-Agent Underwriting System (LangGraph + FastAPI)

![High-Performance Multi-Agent Underwriting System](/sirisha_underwriting_agent.png)

#### Functional Requirements
Let us discuss how we build a high-performance underwriting system for insurance calculations. The application must accept insurance policy applications, process applicant data, and run risk evaluations automatically. The system needs to calculate premium rates based on the determined risk profiles and run compliance checks to ensure parameters conform to local guidelines. We also need to expose an interactive web portal for underwriting coordinators to review flagged policies and manually override premium rates if exceptions apply.

#### Non-Functional Requirements
Our primary performance goal is concurrency and fast response times. The API gateway must handle thousands of active policy queries concurrently, keeping route mapping overhead minimal. The multi-agent calculations must run asynchronously, returning premium summaries within five seconds under normal workloads. We need to implement state persistency across execution cycles, allowing the system to pause when human reviews are pending and resume without data loss.

#### Core Entities
The system architecture revolves around several key entities. We have the Async API Gateway, which manages the client endpoints. We have the Supervisor Agent, which acts as the central coordinator, and the three sub-agents: the Risk Analysis Agent, the Premium Calculation Agent, and the Compliance Auditor Agent. Finally, we have the State Store, managed in Redis, and the Relational Database, which stores the permanent policy records.

#### API Design
The gateway exposes a minimal set of REST endpoints. We have a policy creation endpoint that accepts applicant details and returns a unique tracking token. A policy status endpoint retrieves the current processing state and evaluation scores. Finally, an override endpoint allows underwriting coordinators to submit manual rate updates and mark the policy as approved.

#### Data Flow
When an applicant submits their details, the request hits the Async API Gateway. The gateway validates the payload and triggers a background task, returning a pending status to the client. The Supervisor Agent, orchestrated via LangGraph, initializes the policy state in our Redis store and activates the Risk Analysis Agent. Once the risk assessment is complete, the state updates in Redis, and the Supervisor calls the Premium Calculation Agent. The calculation output is passed to the Compliance Auditor Agent, which verifies guidelines. If a rule is violated, the supervisor marks the state as pending review, notifying the underwriting team. If all checks pass, the record is written to the PostgreSQL database.

#### High-Level Design
The system splits the work into a web layer, an orchestration layer, and a storage layer. The web layer is built using FastAPI to maximize non-blocking concurrency. The orchestration layer runs our stateful LangGraph agents, passing the TypedDict state between worker nodes. The storage layer uses Redis for fast, transient state caching and PostgreSQL for long-term database storage, ensuring a clean separation of concerns.

#### Deep Dive into Non-Functional Requirements
To handle the high concurrent request volume without creating system lag, we write our FastAPI handlers using asynchronous programming patterns. We offload any blocking calculations or database calls to a Celery queue, keeping the API gateway event loop completely free. We ensure state safety by configuring optimistic locking on our Redis checkpoints: when an agent attempts to update the policy state, it verifies the state version hash has not changed, preventing concurrent write collisions.

---

### 2. Advanced Enterprise RAG Engine (LlamaIndex + Vector DB)

![Advanced Enterprise RAG Engine](/sirisha_enterprise_rag.png)

#### Functional Requirements
Let us look at how we design an advanced RAG engine for technical document retrieval. The engine must ingest large collections of manuals, policy templates, and wikis, parsing the text and generating search indices. Users should be able to query the engine using natural language to retrieve relevant document passages. The system must synthesize clean summaries based on the retrieved context, citing exact source files to ensure auditability.

#### Non-Functional Requirements
When we evaluate performance, retrieval accuracy and speed are key. The query search latency must remain under two seconds. The system must handle high-volume document ingestion pipelines without saturating vector database connections. We also need to implement metadata filtering at the database query layer, ensuring that search results are restricted based on user access groups.

#### Core Entities
We build this retrieval engine using several modular components. We have the ETL Ingestion Pipeline, which processes raw files. We have the Vector Index, stored in Pinecone, and the SQL Index, stored in PostgreSQL. Finally, we have the LlamaIndex Query Engine, which contains the routing controller, the re-ranker module, and the LLM synthesis wrapper.

#### API Design
The engine exposes clean query and ingestion interfaces. We have a search endpoint that accepts the query string and user credentials, returning the formatted answer and matching nodes. We also expose a document upload endpoint that allows content admins to submit new text files for indexing.

#### Data Flow
During ingestion, raw documents are cleaned, split into semantic paragraphs, embedded using an OpenAI model, and written to Pinecone with associated metadata. When a user submits a query, the LlamaIndex Query Engine routes the text. If the query requires structural calculations, it queries PostgreSQL. If it requires semantic matches, it queries Pinecone. The router merges the retrieved context passages, passes them to our re-ranker to select the top five most relevant nodes, and sends the filtered context to the LLM API to compile the final cited response.

#### High-Level Design
The architecture separates the document indexing pipeline from the query retrieval pipeline. The indexing pipeline runs as an asynchronous ETL queue, preventing document processing spikes from bottlenecking the query engine. The query pipeline is optimized for low-latency retrieval, leveraging parallel vector lookups and rapid re-ranking to deliver answers quickly.

#### Deep Dive into Non-Functional Requirements
To minimize retrieval latency while processing millions of document chunks, we implement semantic cache lookups. We use Redis to cache query embeddings and their corresponding top-K retrieved nodes: if a user query has a high cosine similarity match with a previously cached search, we retrieve the cached results directly, bypassing the vector database completely. We also configure the model with structured output schemas to prevent parsing failures, ensuring the engine remains reliable in production.

---

### 3. Dynamic Model Swapping & Cost-Optimization Gateway

![Dynamic Model Swapping & Cost-Optimization Gateway](/sirisha_model_gateway.png)

#### Functional Requirements
Let us discuss how we manage API costs and reliability when routing queries across different LLMs. The gateway must accept user chat prompts, classify the complexity of each task, and route it to the most cost-effective model that meets quality requirements. The system must detect provider outages or rate-limit errors in real-time, automatically redirecting requests to fallback models. We also need to log token usage and costs for every transaction, presenting these metrics on a live monitoring dashboard.

#### Non-Functional Requirements
Cost optimization and high availability are our primary drivers. The gateway must maintain sub-fifty-millisecond routing overhead, ensuring the routing logic does not add noticeable latency to user queries. The fallback transition must be completely transparent to the client, resolving API errors without returning failures. We also need to track API costs in real-time, enforcing daily budget limits per service.

#### Core Entities
The gateway is structured around several components. We have the API Routing Gateway, built with FastAPI. We have the Model Swapping Controller, which evaluates routing rules. We have the Metrics DB, which logs token consumption. Finally, we have the Model Registry, which maintains connection keys for commercial APIs and our self-hosted Kubernetes vLLM cluster.

#### API Design
The gateway exposes a unified generate endpoint that matches the standard OpenAI completion payload, returning model responses and usage stats. We also expose a rule management endpoint that allows system administrators to adjust model routing mappings and cost limits dynamically.

#### Data Flow
A client sends a completion request to the FastAPI gateway. The Model Swapping Controller checks the prompt complexity. If it is a simple classification query, the controller routes it to a self-hosted LLaMA-3 instance running on our Kubernetes GPU cluster. If it is a complex coding query, it routes it to the Azure OpenAI API. The controller writes the input/output token counts to the Metrics DB. If the Azure OpenAI call fails due to a rate-limit error, the gateway catches the exception, switches the target to the hosted LLaMA instance, and completes the call.

#### High-Level Design
The architecture is structured as a low-latency proxy layer. The routing path uses async HTTP clients to forward requests, minimizing latency. The metrics logging path runs asynchronously, pushing token records to a background queue to ensure logging operations never delay completion responses.

#### Deep Dive into Non-Functional Requirements
To ensure the routing gate remains highly available under load, we configure uvicorn to run with multiple worker processes, utilizing Redis to share routing rules across workers. We implement a token bucket algorithm to monitor our commercial API quotas: if we approach our token-per-minute threshold, the controller preemptively routes non-critical traffic to our Kubernetes cluster, preventing rate-limit blocks and keeping external costs low.

---

### 4. Scalable Asynchronous LLM Fine-tuning & Training Pipeline

![Scalable Asynchronous LLM Fine-tuning & Training Pipeline](/sirisha_finetuning_pipeline.png)

#### Functional Requirements
Let us analyze how we automate the fine-tuning of LLMs for specialized tasks. The pipeline must ingest raw dataset uploads, clean the files, and format them into structured JSONL training sets. The system needs to schedule training jobs on GPU clusters, track loss metrics and evaluation scores during training, and save the final model weights to a central repository. We must also support model evaluation before deploying the fine-tuned adapter to production.

#### Non-Functional Requirements
Compute resource utilization and pipeline visibility are our primary focus. The fine-tuning jobs must execute asynchronously, managed via a queue to ensure multiple users can submit training runs without overloading the GPUs. The pipeline must capture and log all training metrics to prevent configuration drift. The containerized training jobs must run inside restricted secure environments to protect proprietary training data.

#### Core Entities
We define several entities to manage this pipeline. We have the Data Ingestion Portal, which validates formatting. We have the Training Job Queue, managed with Celery and RabbitMQ. We have the PyTorch/TensorFlow Training Container, which runs the LoRA fine-tuning code. Finally, we have the MLflow Tracking Server and the Model Registry.

#### API Design
The pipeline exposes endpoints to upload datasets, trigger fine-tuning jobs (returning a task ID), query training status and metrics, and promote a validated model to the production registry.

#### Data Flow
A developer uploads a CSV dataset to our storage bucket. The Ingestion Portal triggers a Spark job to clean the data and format it into chat-template JSONL records. The developer triggers the fine-tuning API, which pushes a task into our Celery queue. A background worker claims the task, launches a PyTorch Docker container on our GPU node, and passes the dataset path. During training, the container logs training loss to MLflow. Once training completes, the adapter weights are evaluated against a test suite. If the scores exceed our baseline, the weights are saved to our Model Registry.

#### High-Level Design
The architecture separates the data prep, the compute pipeline, and the monitoring layer. The compute pipeline is built on a distributed queue to decouple job submissions from physical GPU nodes. The monitoring layer utilizes MLflow and Grafana to track experiment metrics, ensuring full observability across all training runs.

#### Deep Dive into Non-Functional Requirements
To optimize GPU memory usage during training, we configure PyTorch to use DeepSpeed ZeRO-3 and parameter-efficient fine-tuning with LoRA. We load the base model in 4-bit precision, training only the low-rank adapter layers, which keeps GPU memory usage below sixteen gigabytes. To protect training datasets containing PII, the data prep pipeline runs a redact filter, ensuring that no sensitive personal data is ever written to the training checkpoints.

---

### 5. Secure Cloud-Native Transaction Ingestion Agent (Azure Functions + Docker)

![Secure Cloud-Native Transaction Ingestion Agent](/sirisha_transaction_agent.png)

#### Functional Requirements
Let us discuss how we ingest and sanitize high-volume transactional logs using serverless agents. The system must accept incoming transaction records from external partners, decrypt the data, and sanitize any sensitive information. The agent needs to use an LLM parser to classify transaction categories and extract structured fields. The verified data must be written to our database, and any anomalous or flagged transactions must trigger alerts.

#### Non-Functional Requirements
Security and scalability are the primary drivers in this architecture. The ingestion endpoints must handle spikes of up to ten thousand transactions per hour, scaling compute resources dynamically. The agent must process each transaction securely under SOC 2 constraints, using managed identities instead of static credentials. We also need to implement Redis caching to optimize database writes and prevent deadlock bottlenecks.

#### Core Entities
The ingestion pipeline is composed of several components. We have Azure API Management, which routes client requests. We have the Azure Functions, which act as the serverless trigger layer. We have the Dockerized LLM Parsing Agent, running on Azure Container Apps. Finally, we have Azure Key Vault, Redis Cache, and the PostgreSQL database.

#### API Design
The ingestion interface exposes a secure POST endpoint that accepts encrypted JSON transaction payloads. We also expose a status API to monitor pipeline throughput, error rates, and decryption latency.

#### Data Flow
An external partner sends an encrypted transaction payload to Azure API Management. This triggers an Azure Function, which retrieves the decryption key from Azure Key Vault and decrypts the payload. The function then forwards the transaction to our Dockerized LLM Parsing Agent. The agent extracts structured fields, sanitizes PII, and categorizes the transaction type. The agent queries Redis to verify matching account metadata, and writes the clean transaction log to our PostgreSQL database, returning a success confirmation to the caller.

#### High-Level Design
The system uses a serverless, event-driven architecture. The Azure Function handles the entry point and decryption, keeping the compute footprint minimal. The containerized parsing agent scales dynamically based on request queue length, ensuring high throughput. The database layer uses connection pools and Redis cache to protect PostgreSQL from concurrent write saturation.

#### Deep Dive into Non-Functional Requirements
To ensure SOC 2 compliance, we run the containerized agents inside a private Azure Virtual Network, restricting external internet access. We configure the Azure Functions and container instances to authenticate with Key Vault and PostgreSQL using Azure Managed Identities, eliminating database passwords from our configuration files. To prevent database deadlock bottlenecks during high write spikes, we write transaction updates in batches, resolving concurrent database locks by executing queries in a strict, sequential order.

---

## Part 4: Integration with Workspace

We register our new preparation guide in the Nextra navigation.

### File Modifications

#### 1. Add to Navigation Sidebar
We register the guide in [content/_meta.js](file:///f:/Personal%20Shit/preprationstuff/content/_meta.js).

```diff
 export default {
   index: 'Docs Home',
   'qualcomm-prep-material': 'Qualcomm NPU / Embedded Platform Prep',
   'natera-ai-solutions-prep': 'Natera AI Solutions Prep',
+  'sirisha-genai-prep': 'Sirisha GenAI Prep',
   'torc-prep-guide': 'Torc Prep Guide (Device Drivers)',
   'vaishnavi-torc-mcu-applications-prep': 'Vaishnavi Torc MCU Applications Prep',
```

#### 2. Link on Main Index Page
We link the new document on [content/index.mdx](file:///f:/Personal%20Shit/preprationstuff/content/index.mdx).

```diff
 # Preparation Stuff
 
 This site hosts Markdown documents. Add new files under `content/` and they will appear in the sidebar automatically.
 
 - [Natera Head of AI Solutions Prep Guide](/docs/natera-ai-solutions-prep)
+- [Sirisha GenAI Prep Guide](/docs/sirisha-genai-prep)
 - [Torc Prep Guide (Device Drivers)](/docs/torc-prep-guide)
```
