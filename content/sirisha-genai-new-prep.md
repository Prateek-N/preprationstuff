---
title: Sirisha Nelapudi New GenAI Prep Guide
description: Comprehensive preparation guide for the GenAI Application Engineer interview, customized for Sirisha Nelapudi.
---

# Sirisha Nelapudi Prep Guide: GenAI Application Engineer

Welcome to your preparation guide for the GenAI Application Engineer role. This guide is customized around your software engineering experience at **Morgan Stanley**, **Liberty Mutual**, and **Dell Technologies**, combined with your Master of Science in Computer Science from the **University of Florida**, mapping your background directly to the requirements of the new Job Description (LangGraph, LlamaIndex, FastAPI, PyTorch/TensorFlow model fine-tuning, and Docker container deployments).

---

## Part 1: Introductions & Pitch

### 1. Can you walk me through your background and explain how your software engineering experience prepares you for this GenAI Application Engineer role?
I am a Software Engineer with over three years of experience building high-performance backend systems, distributed architectures, and Generative AI applications. I hold a Master of Science in Computer Science from the **University of Florida**, where I specialized in machine learning and deep learning models. My professional career spans roles at **Morgan Stanley**, **Liberty Mutual**, and **Dell Technologies**, where I transitioned from core Java development to cloud-native microservices and GenAI agentic workflows.

At **Morgan Stanley**, I architected financial microservices using **Java** and **Spring Boot** to process 4 TB of weekly transactions. I also engineered GenAI agents using **LangChain**, **LangGraph**, and **OpenAI APIs** to automate technical documentation retrieval, reclaiming 14 hours of manual research time per sprint for our engineering team. Additionally, I designed cloud-native data ingestion layers on **Azure Cloud** with **Azure AI** services, managing sensitive transaction encryption and scaling containerized deployments using **Docker** and **Kubernetes**.

This combination of enterprise software engineering and generative AI application development aligns with the requirements of this role. I have hands-on experience building multi-agent workflows, managing data integration pipelines, and optimizing backend systems. I am proficient in **Python**, **Java**, and SQL, and am comfortable designing high-performance services. I am excited to bring my experience in building scalable, secure, and cost-effective GenAI systems to your engineering team.

---

## Part 2: Technical Questions Related to Projects

### 2. At Morgan Stanley, you engineered Generative AI agents using LangChain and LangGraph. How would you apply this experience to design the LangGraph multi-agent architectures required for this role?
At **Morgan Stanley**, I engineered Generative AI agents using **LangChain** and **LangGraph** to automate technical documentation retrieval, reclaiming 14 hours of research time per sprint. Our primary challenge was ensuring that the agent could accurately route queries between different documentation silos (such as legacy system logs, API schemas, and release notes) without getting stuck in infinite loops. I designed a stateful, graph-based routing architecture to resolve this.

I defined the agent's state as a structured Pydantic object, containing the user query, active search parameters, retrieved passages, and a loop-counter variable to prevent execution overflows. I constructed the graph nodes using **LangGraph**, assigning specialized roles to different agent nodes (such as a Log Analyzer agent and an API schema parser). I wrote conditional routing edges that analyzed the model's output to determine if the agent needed to query external tools or pass the context to a secondary parser.

For this role, I will leverage this stateful agent engineering experience to build sophisticated multi-agent architectures. I am comfortable writing custom state reducers, implementing human-in-the-loop checkpoints to validate agent decisions, and configuring parallel node executions to reduce latency. By separating complex workflows into specialized, communicating agents, I will ensure that our GenAI systems are modular, testable, and scale to support enterprise operations.

---

### 3. How does your experience building high-performance Java/Spring Boot financial microservices at Morgan Stanley prepare you to design scalable backend services using FastAPI and Async Python?
At **Morgan Stanley**, I architected high-performance financial microservices using **Java** and **Spring Boot** to eliminate trading latency, processing 4 TB of weekly transaction data. In enterprise architectures, handling high concurrent workloads without thread blocking is critical to maintain system responsiveness. While Spring Boot uses a thread-per-request model, **FastAPI** leverages Python's asynchronous event loop to handle concurrent connections efficiently.

My experience in concurrency control, database deadlock resolution, and caching is directly applicable to building services in **FastAPI** using **Async Python**. In Spring Boot, I optimized query performance for 18,000 active users using **Redis** caching strategies and resolved 25 database deadlocks per cycle by refactoring transaction boundaries. In FastAPI, I will write non-blocking async handlers, using async database drivers (like asyncpg) and ORMs (like SQLAlchemy) to prevent event loop blocking.

I will design FastAPI routers to serve quantized LLM inference requests, using background tasks to offload heavy calculations. I will configure connection pools, set up rate-limiting middleware, and write custom validation layers. This transition from multi-threaded Java systems to event-driven Async Python allows me to design high-throughput backend services that handle millions of daily API exchanges without resource exhaustion.

---

### 4. You designed cloud-native data ingestion layers on Azure Cloud. How would you transition this to build advanced RAG systems utilizing LlamaIndex and vector databases?
At **Morgan Stanley**, I designed cloud-native data ingestion layers on **Azure Cloud** utilizing **Azure AI** services and Azure Functions, sustaining 800+ inference requests per hour. The ingestion pipeline automated the extraction, cleaning, and encryption of transactional records before writing them to databases. This experience in building secure data pipelines is directly applicable to constructing advanced RAG (Retrieval-Augmented Generation) systems.

To transition this architecture to advanced RAG, I will use **LlamaIndex** to manage the ingestion, chunking, and indexing of raw documents. I will configure hierarchical node parsers to split text into parent-child relationships, ensuring that our models retrieve detailed context while maintaining global document boundaries. I will store the generated embeddings in vector databases like **Pinecone** or **Milvus**, setting up metadata indexes to enable pre-filtering during queries.

I will also implement advanced retrieval strategies, such as hybrid search (combining sparse TF-IDF tokens with dense vector search) and re-ranking models (like Cohere Re-rank) to sort the retrieved context nodes. This pipeline design ensures that our LLM receives only the most relevant, high-fidelity context passages. By combining my cloud ingestion experience with LlamaIndex, I will deliver secure RAG systems that minimize hallucinations.

---

### 5. At Liberty Mutual, you integrated Python-based server environments with Spring Boot microservices. How would you leverage this to swap and optimize diverse LLMs?
At **Liberty Mutual**, I modernised legacy policy modules and led the integration of **Python-based** server environments with **Java** Spring Boot microservices, maintaining high availability for 18,000 active policyholders. In enterprise GenAI platforms, we must remain model-agnostic, allowing the system to swap commercial models (like OpenAI) and open-source models (like LLaMA-70B) based on latency and cost.

I design this abstraction by building a model gateway service using **FastAPI** and **Python**. The gateway exposes a unified REST API endpoint for downstream applications. Inside the gateway, I write router classes that intercept incoming requests, evaluate the complexity of the prompt, and direct the call to the appropriate LLM provider (such as Azure OpenAI for complex tasks or a self-hosted vLLM engine for extraction).

This gateway abstraction allows us to swap models without modifying client-side code. I will configure automated fallback logic: if a commercial API experiences a timeout, the gateway redirects the request to our self-hosted backup model, maintaining service availability. By tracking API costs and token usage in real-time, I will optimize our model routing to reduce operational expenditures.

---

### 6. Describe your experience standardizing deployment environments using Docker, Kubernetes, and Terraform, and how it maps to containerizing GenAI services.
At **Morgan Stanley** and **Dell Technologies**, I standardized deployment environments by containerizing Java applications using **Docker** and orchestrating them on **Kubernetes**, utilizing **Terraform** for Infrastructure as Code (IaC). In traditional backend systems, configuration drift between local, staging, and production environments is a common cause of deployment failures. Containerization resolves this by packaging the application with its runtime dependencies.

This containerization experience is critical when deploying GenAI applications, which require complex libraries (such as PyTorch, CUDA drivers, and sentence-transformers) to run. I write multi-stage Dockerfiles to package our Python FastAPI services, installing build tools in an initial stage and copying only the compiled virtual environment to a slim base image, reducing the container footprint.

I write Kubernetes deployment manifests, specifying CPU/GPU limits and configuring Horizontal Pod Autoscalers (HPA) to scale pods based on concurrent request counts. I use Terraform to provision our cloud clusters, S3 buckets, and vector database instances. This automation ensures that our GenAI deployments are reproducible, scale to meet traffic spikes, and maintain high availability in production.

---

## Part 3: Top 10 Python Debugging Questions

### 7. Debugging Question 1: Resolving a blocking database call inside an asynchronous FastAPI endpoint.
**Thought Process:**
In **FastAPI**, if I write an asynchronous endpoint using the `async def` syntax but call a synchronous, blocking function (like a standard database query using psycopg2) inside it, I will block the entire event loop. The event loop runs on a single thread, and blocking it prevents FastAPI from processing concurrent incoming requests, destroying performance. To fix this, I must either use an asynchronous database driver (like asyncpg) or run the blocking call in a separate thread pool using FastAPI's background workers.

**Code:**
```python
import asyncio
import time
from fastapi import FastAPI

app = FastAPI()

# Buggy version: This blocking function blocks the single-threaded event loop
def get_db_data_sync():
    time.sleep(2)  # Simulates a slow, blocking SQL database query
    return {"data": "financial_records"}

# Corrected version: I run the blocking database call asynchronously
async def get_db_data_async():
    # In a production system, I would use an async database driver like asyncpg.
    # Here, I simulate the non-blocking await using asyncio.sleep.
    await asyncio.sleep(2)
    return {"data": "financial_records"}

@app.get("/records")
async def read_records():
    # I await the asynchronous, non-blocking database call
    result = await get_db_data_async()
    return result
```

**Complexity:**
The time complexity of the database lookup remains $O(1)$ simulated. The space complexity is $O(1)$ as we store only static records in memory. By resolving the event loop block, we allow FastAPI to process concurrent requests, shifting our system throughput from sequential execution to parallel execution.

---

### 8. Debugging Question 2: Fixing a memory leak caused by mutable default arguments in a LlamaIndex custom node parser.
**Thought Process:**
In **Python**, default arguments are evaluated once when the function is defined, not each time the function is called. If I use a mutable object (like a list) as a default argument in a custom **LlamaIndex** node parser, that list is shared across all function executions. If I append parsed text nodes to this list, the list will grow indefinitely across requests, causing a memory leak and mixing up document context between different users.

**Code:**
```python
class CustomNodeParser:
    # Buggy version: def __init__(self, target_nodes=[]):
    # This shares the same list across all parser instances, causing a memory leak.
    
    # Corrected version: I default to None and instantiate a new list per call
    def __init__(self, target_nodes=None):
        if target_nodes is None:
            self.target_nodes = []
        else:
            self.target_nodes = target_nodes

    def parse_document(self, text_chunk):
        # I append the parsed text chunk to the instance-specific list
        self.target_nodes.append(text_chunk)
        return self.target_nodes
```

**Complexity:**
The time complexity of appending a node to the list is $O(1)$. The space complexity is $O(N)$ where $N$ is the number of text chunks parsed in the active instance. By resolving the default argument issue, we ensure that memory is garbage-collected after each session, preventing memory leaks.

---

### 9. Debugging Question 3: Resolving unawaited coroutines in a LangGraph multi-agent routing loop.
**Thought Process:**
When building multi-agent systems using **LangGraph** and **LangChain**, many tool execution functions are defined as coroutines (`async def`). If I call one of these async tool functions inside a node but forget to write the `await` keyword, Python will return a coroutine object instead of executing the function. This will cause downstream nodes to fail when they attempt to parse the expected string output.

**Code:**
```python
import asyncio

# I define an asynchronous tool to fetch user transaction data
async def fetch_user_balance(user_id):
    await asyncio.sleep(1)
    return "$5,000"

# Buggy version:
# def agent_node(state):
#     balance = fetch_user_balance(state["user_id"])  # Returns a coroutine object
#     return {"output": "User balance is " + balance}

# Corrected version: I define the node as async and await the tool execution
async def agent_node_corrected(state):
    # I write the await keyword to execute the coroutine and get the string result
    balance = await fetch_user_balance(state["user_id"])
    return {"output": "User balance is " + balance}
```

**Complexity:**
The time complexity of the tool execution is $O(1)$ simulated database lookup. The space complexity is $O(1)$ to store the output string. Awaiting the coroutine ensures that the graph state receives the string value, preventing execution errors.

---

### 10. Debugging Question 4: Preventing a recursion overflow in a LangGraph state transition loop.
**Thought Process:**
In **LangGraph**, agents transition between nodes based on conditional routing edges. If the router logic fails to update the graph state correctly or does not implement a terminate condition, the graph can route back and forth between two nodes indefinitely. This loop will cause a recursion overflow, consuming API tokens and eventually crashing the container. I must implement a loop counter in our state.

**Code:**
```python
# I define our state schema containing a loop counter
class GraphState(dict):
    query: str
    steps_taken: int
    output: str

# Buggy version: This router loops infinitely if it cannot find an answer.
# Corrected version: I check if steps_taken exceeds our safety threshold.
def route_next_node(state: GraphState):
    # If the agent has run more than 5 times, I force a route to the end node
    if state.get("steps_taken", 0) >= 5:
        return "end_node"
        
    if "final_answer" in state.get("output", ""):
        return "end_node"
    
    # Otherwise, I increment the steps count and retry tool execution
    state["steps_taken"] = state.get("steps_taken", 0) + 1
    return "tool_node"
```

**Complexity:**
The time complexity is $O(M)$ where $M$ is the maximum number of steps allowed (5 in this case), ensuring constant-time termination. The space complexity is $O(1)$ as we store only a few counter variables in the state object.

---

### 11. Debugging Question 5: Resolving thread-safety issues when writing agent run logs to a shared file descriptor.
**Thought Process:**
When running asynchronous web apps in **FastAPI**, multiple requests are processed concurrently by the event loop. If these async endpoints write execution logs to a shared file descriptor using standard synchronous write commands (`file.write()`), the file write blocks the event loop. Furthermore, concurrent writes can overlap and corrupt the log formatting. I must use async file utilities like aiofiles.

**Code:**
```python
# Buggy version:
# def log_execution(message):
#     with open("agent_runs.log", "a") as f:
#         f.write(message + "\n")  # Blocks the event loop

# Corrected version: I use an async library or write to an async logging stream
import aiofiles

async def log_execution_async(message):
    # I open the file asynchronously using aiofiles
    async with aiofiles.open("agent_runs.log", "a") as f:
        # I await the write operation, preventing event loop blocking
        await f.write(message + "\n")
```

**Complexity:**
The time complexity of appending a log line is $O(1)$. The space complexity is $O(1)$ as we write the string data directly to disk. Using async file operations prevents thread blocking, maintaining high-throughput performance for downstream microservices.

---

### 12. Debugging Question 6: Fixing a memory exhaustion issue when loading large pandas datasets in Python care coordination tools.
**Thought Process:**
When building care coordination analytics tools in **Python**, we often load patient datasets (like CSV log reports) using **pandas**. If the CSV file is large, loading the entire file into memory using `pd.read_csv()` can exhaust the server's memory, causing the container to be terminated by the OS kernel. To resolve this, I must load and process the dataset in smaller chunks.

**Code:**
```python
import pandas as pd

# Buggy version:
# def process_patient_records(file_path):
#     df = pd.read_csv(file_path)  # Loads the entire file into memory
#     return df[df["status"] == "active"]

# Corrected version: I process the file in chunks to maintain a low memory footprint
def process_patient_records_chunked(file_path, chunk_size=10000):
    active_records = []
    
    # I read the CSV file sequentially in chunks of 10,000 rows
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # I filter active patients within the chunk
        filtered_chunk = chunk[chunk["status"] == "active"]
        active_records.append(filtered_chunk)
        
    # I concatenate the filtered chunks into a single dataframe
    return pd.concat(active_records, ignore_index=True)
```

**Complexity:**
The time complexity of this filtering is $O(R)$ where $R$ is the number of rows in the CSV file. The space complexity is reduced to $O(C)$ where $C$ is the chunk size, preventing memory exhaustion by keeping only a small data segment in memory at any time.

---

### 13. Debugging Question 7: Resolving a connection pool leak in a custom LlamaIndex vector store retriever.
**Thought Process:**
When querying vector databases like **Pinecone** or PostgreSQL within a custom **LlamaIndex** retriever, we must open database connections. If the retriever opens a new database connection for every query but does not close it after execution, the system will eventually run out of available connection slots, causing all subsequent search queries to fail. I must use a connection pool and close connections.

**Code:**
```python
# Buggy version:
# def retrieve_context(query_vector):
#     conn = database.connect()  # Opens a connection per query
#     cursor = conn.cursor()
#     cursor.execute("SELECT text FROM vector_table ...")
#     return cursor.fetchall()  # Connection is never closed

# Corrected version: I use a context manager to ensure the connection is closed
def retrieve_context_corrected(db_connection_pool, query_vector):
    # I get a connection from our pre-allocated connection pool
    with db_connection_pool.getconn() as conn:
        with conn.cursor() as cursor:
            # I execute the vector search query
            cursor.execute("SELECT text FROM vector_table WHERE vector = %s", (query_vector,))
            return cursor.fetchall()
            # The context managers automatically close the cursor and return the connection
```

**Complexity:**
The time complexity of the vector database search is $O(D \log N)$ where $D$ is the vector dimension and $N$ is the number of embeddings. The space complexity is $O(K)$ where $K$ is the number of retrieved context nodes. Using a connection pool prevents connection leaks and stabilizes database access.

---

### 14. Debugging Question 8: Preventing race conditions when updating shared agent state variables in FastAPI.
**Thought Process:**
In **FastAPI**, if multiple async endpoints update a shared global variable (such as an active session count) without synchronization, race conditions can occur. Because async handlers yield execution during await statements, another request can modify the shared variable before the first request completes, leading to inconsistent state calculations. I must use an asynchronous Lock.

**Code:**
```python
import asyncio
from fastapi import FastAPI

app = FastAPI()
session_count = 0
# I initialize an asyncio Lock to synchronize access to the counter
lock = asyncio.Lock()

# Buggy version:
# @app.post("/session")
# async def create_session():
#     global session_count
#     temp = session_count
#     await asyncio.sleep(0.1)  # Yields execution, causing a race condition
#     session_count = temp + 1

# Corrected version: I acquire the lock before modifying the variable
@app.post("/session")
async def create_session_safe():
    global session_count
    # I use a context manager to acquire the lock, blocking other writes
    async with lock:
        temp = session_count
        await asyncio.sleep(0.1)
        session_count = temp + 1
    return {"sessions": session_count}
```

**Complexity:**
The time complexity of acquiring the lock is $O(1)$. The space complexity is $O(1)$. Using a lock ensures that only one request updates the counter at a time, preventing race conditions and maintaining data integrity.

---

### 15. Debugging Question 9: Fixing a type error when passing raw JSON payloads to a PyTorch tensor construction function.
**Thought Process:**
When building model inference endpoints in **FastAPI**, the raw inputs arrive as JSON objects. If I attempt to convert a list of strings directly into a **PyTorch** tensor using `torch.tensor()`, the code will throw a TypeError. PyTorch tensors can only be constructed from numerical data types. I must convert the text tokens to their corresponding numerical IDs first.

**Code:**
```python
import torch

# I simulate a simple token-to-ID vocabulary mapping
vocab = {"heart": 1, "rate": 2, "normal": 3}

# Buggy version:
# def predict_sentiment(token_list):
#     tensor = torch.tensor(token_list)  # Throws TypeError if token_list contains strings

# Corrected version: I convert the text tokens to numerical IDs first
def predict_sentiment_corrected(token_list):
    # I map each string token to its vocabulary ID, defaulting to zero
    numerical_ids = [vocab.get(token, 0) for token in token_list]
    
    # I construct the PyTorch tensor from the numerical list
    tensor = torch.tensor(numerical_ids, dtype=torch.long)
    return tensor
```

**Complexity:**
The time complexity of this vocabulary mapping is $O(T)$ where $T$ is the number of tokens in the input list. The space complexity is $O(T)$ to allocate memory for the numerical IDs and the output PyTorch tensor. This conversion resolves the type error, allowing our model to run inference.

---

### 16. Debugging Question 10: Resolving memory leaks caused by uncleaned LangChain callback handlers in FastAPI routers.
**Thought Process:**
In **FastAPI**, if I register custom callback handlers in **LangChain** or **LangGraph** nodes to monitor prompt execution metrics (such as logging API call tokens to an external collector), these handler objects can remain in memory after the request completes. If the handler references a global list or database client, the memory allocated for these handlers will leak across requests, eventually crashing the container.

**Code:**
```python
from fastapi import FastAPI
from langchain.callbacks.base import BaseCallbackHandler

# I define a custom logging callback handler
class IngestionCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        pass

app = FastAPI()

# Buggy version: I append the handler to a global list, causing a memory leak
# global_handlers = []

# Corrected version: I instantiate the callback handler within the request scope
@app.post("/agent")
async def run_agent(query: str):
    # I instantiate the handler locally so it is garbage-collected after the request
    handler = IngestionCallbackHandler()
    
    # In a production system, I would pass the handler directly to the LangChain run config
    # run_result = await agent.arun(query, callbacks=[handler])
    return {"status": "completed"}
```

**Complexity:**
The time complexity of instantiating the handler is $O(1)$. The space complexity is $O(1)$ local reference. Keeping the callback handlers within the request scope ensures that all allocated resources are released after the response is sent, preventing memory leaks in production.

---

## Part 4: Top 20 Coding Questions

### 17. Coding Question 1: Design a stateful multi-agent orchestrator loop using Python.
**Thought Process:**
To build a stateful multi-agent orchestrator loop in **Python** that manages graph transitions without dependencies, I would implement a custom graph coordinator class. I would define our state using a dictionary. The coordinator class will hold the graph nodes (which are Python functions) and conditional transition rules.

I would loop through the execution steps, calling the current node function, updating the state, and using the transition rules to determine the next node. I would add a step counter to terminate the loop if it exceeds a threshold, preventing infinite cycles. This logic replicates the core behavior of **LangGraph** in pure Python.

**Code:**
```python
class AgentOrchestrator:
    def __init__(self):
        # I initialize dictionaries to hold our node functions and routing rules
        self.nodes = {}
        self.edges = {}
        
    def add_node(self, name, node_func):
        self.nodes[name] = node_func
        
    def add_conditional_edge(self, source, routing_func):
        self.edges[source] = routing_func
        
    def execute(self, initial_state, max_steps=5):
        state = initial_state
        current_node = "start"
        steps = 0
        
        # I loop through the execution path until we reach the end node
        while current_node != "end" and steps < max_steps:
            # I execute the current node function, updating our state
            state = self.nodes[current_node](state)
            steps += 1
            
            # I determine the next node using our routing rules
            router = self.edges.get(current_node)
            if router:
                current_node = router(state)
            else:
                break
                
        return state
```

**Complexity:**
The time complexity of this orchestration loop is $O(S)$ where $S$ is the number of steps executed, running in linear time. The space complexity is $O(1)$ as we reuse the same state dictionary in memory.

---

### 18. Coding Question 2: Implement a custom cosine similarity function for vector search matching.
**Thought Process:**
To implement a custom cosine similarity function in **Python** without importing external vector database libraries, I would calculate the dot product of the two vectors and divide it by the product of their L2 norms. This is the mathematical basis for checking semantic relevance in **RAG** systems.

I would write a loop to calculate the dot product, summing the products of the corresponding vector elements. In parallel, I would calculate the sum of squares for each vector, taking the square root of the sums to determine the L2 norms. If either norm is zero, I return zero similarity to prevent division by zero errors.

**Code:**
```python
import math

def calculate_cosine_similarity(vector_a, vector_b):
    # I check if the vectors have matching dimensions
    if len(vector_a) != len(vector_b):
        return 0.0
        
    dot_product = 0.0
    norm_a = 0.0
    norm_b = 0.0
    
    # I loop through the elements to calculate our dot product and norms
    for val_a, val_b in zip(vector_a, vector_b):
        dot_product += val_a * val_b
        norm_a += val_a ** 2
        norm_b += val_b ** 2
        
    # I verify that neither vector has a norm of zero
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
        
    # I calculate and return the cosine similarity score
    return dot_product / (math.sqrt(norm_a) * math.sqrt(norm_b))
```

**Complexity:**
The time complexity of this calculation is $O(D)$ where $D$ represents the dimension of the input vectors. The space complexity is $O(1)$ because we store only scalar sum values in memory during the execution.

---

### 19. Coding Question 3: Build an asynchronous rate-limiting middleware in FastAPI.
**Thought Process:**
To protect our **FastAPI** backend services from resource exhaustion, I would implement an asynchronous rate-limiting middleware. The middleware will intercept incoming HTTP requests, extract the client IP address, and check request frequencies.

I would use a sliding window counter. In this python implementation, I will use a simple dictionary to store request timestamps for each IP. When a request arrives, I clean out old timestamps, check if the active list size exceeds our limit, and raise an HTTP 429 Too Many Requests exception if it does.

**Code:**
```python
import time
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()
request_history = {} # I use a dictionary to track timestamps by IP
LIMIT = 5 # Maximum requests allowed
WINDOW_SIZE = 10 # Sliding window size in seconds

@app.middleware("http")
async def rate_limiter_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()
    
    # I get or initialize the timestamp list for the client IP
    timestamps = request_history.get(client_ip, [])
    
    # I remove any timestamps that fall outside the active sliding window
    timestamps = [t for t in timestamps if current_time - t < WINDOW_SIZE]
    
    # I check if the request limit is reached
    if len(timestamps) >= LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests")
        
    # I add the new request timestamp
    timestamps.append(current_time)
    request_history[client_ip] = timestamps
    
    # I forward the request to the next handler
    response = await call_next(request)
    return response
```

**Complexity:**
The time complexity of the check is $O(W)$ where $W$ is the number of request timestamps stored for the client IP (max 5). The space complexity is $O(I \times L)$ where $I$ is the number of unique IPs and $L$ is the request limit.

---

### 20. Coding Question 4: Create a text chunker with paragraph and overlap boundaries.
**Thought Process:**
When preparing clinical documents for indexing in **LlamaIndex** advanced **RAG** systems, we must split the text into chunks. To prevent losing context at chunk boundaries, I would write a custom Python function that splits text at paragraph boundaries while implementing an overlap window.

I would split the input text by double newlines to isolate paragraphs. I would iterate through these paragraphs, appending them to a chunk buffer. If adding a paragraph exceeds our target chunk size, I save the current chunk and initialize a new chunk, copying the last few paragraphs (overlap window) to maintain context.

**Code:**
```python
def chunk_text_by_paragraphs(raw_text, max_chunk_chars=1000, overlap_paragraphs=1):
    # I split the text by paragraph boundaries
    paragraphs = raw_text.split("\n\n")
    chunks = []
    current_chunk = []
    current_length = 0
    
    for i, para in enumerate(paragraphs):
        para_len = len(para)
        
        # I check if adding the paragraph exceeds our character limit
        if current_length + para_len > max_chunk_chars and current_chunk:
            # I save the completed chunk to our list
            chunks.append("\n\n".join(current_chunk))
            
            # I initialize the new chunk using the configured overlap paragraphs
            overlap_start = max(0, len(current_chunk) - overlap_paragraphs)
            current_chunk = current_chunk[overlap_start:]
            current_length = sum(len(p) for p in current_chunk) + (len(current_chunk) - 1) * 2
            
        current_chunk.append(para)
        current_length += para_len + (2 if current_length > 0 else 0)
        
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
        
    return chunks
```

**Complexity:**
The time complexity of this chunking is $O(P)$ where $P$ is the number of paragraphs in the raw text. The space complexity is $O(T)$ to allocate memory for the output list of chunk strings.

---

### 21. Coding Question 5: Implement a TF-IDF keyword calculator for hybrid search ranking.
**Thought Process:**
To implement a simple Term Frequency-Inverse Document Frequency (TF-IDF) calculator in **Python** for hybrid search ranking, I would calculate term frequencies in a query document and multiply them by the document-level inverse frequencies. This helps rank context nodes before sending them to the LLM.

I would count the occurrences of the search term in the target document to calculate Term Frequency. I would then count how many documents in our corpus contain the term to calculate the Inverse Document Frequency (using a log ratio). The product of these values represents the relevance score.

**Code:**
```python
import math

def calculate_tfidf(term, target_document, corpus_documents):
    # I normalize the casing to ensure matching consistency
    term_lower = term.lower()
    doc_words = [w.lower() for w in target_document.split()]
    
    # I calculate Term Frequency (occurrences divided by total words)
    term_count = doc_words.count(term_lower)
    if not doc_words:
        return 0.0
    tf = term_count / len(doc_words)
    
    # I count how many documents in the corpus contain the term
    matching_docs = sum(1 for doc in corpus_documents if term_lower in doc.lower().split())
    
    # I calculate Inverse Document Frequency using a smoothed log ratio
    total_docs = len(corpus_documents)
    idf = math.log((1 + total_docs) / (1 + matching_docs)) + 1
    
    # I return the final TF-IDF relevance score
    return tf * idf
```

**Complexity:**
The time complexity of this calculation is $O(W + D \times M)$ where $W$ is the number of words in the document, $D$ is the number of documents in the corpus, and $M$ is the average word count in corpus documents. The space complexity is $O(W)$ to store the tokenized words in memory.

---

### 22. Coding Question 6: Build a prompt-routing gateway using FastAPI.
**Thought Process:**
To build a prompt-routing gateway in **FastAPI**, I would write an endpoint that evaluates the complexity of incoming prompts and routes them to different LLM engines. If the prompt contains coding or reasoning keywords, it is routed to a commercial model; otherwise, it goes to a self-hosted open-source model.

I would define a list of complex keywords. When a client calls our route endpoint, I inspect the prompt string. If a keyword is found, I execute a simulated HTTP call to the commercial API. If no keywords match, I route the call to our self-hosted model, optimizing our API usage costs.

**Code:**
```python
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()
# I define keywords that require a complex reasoning model
REASONING_KEYWORDS = ["write code", "analyze schema", "calculate", "optimize"]

@app.post("/route_prompt")
async def route_prompt(prompt: str):
    prompt_lower = prompt.lower()
    
    # I check if the prompt requires a complex model
    use_complex_model = any(kw in prompt_lower for kw in REASONING_KEYWORDS)
    
    # I route the request to the appropriate LLM provider
    if use_complex_model:
        # In production, I would call Azure OpenAI API
        # response = await httpx.post(openai_url, json={"prompt": prompt})
        return {"routed_to": "Azure OpenAI", "result": "complex_response"}
    else:
        # In production, I would call a self-hosted LLaMA model
        # response = await httpx.post(llama_url, json={"prompt": prompt})
        return {"routed_to": "Self-Hosted LLaMA", "result": "simple_response"}
```

**Complexity:**
The time complexity of the keyword inspection is $O(K \times P)$ where $K$ is the number of keywords and $P$ is the prompt length. The space complexity is $O(1)$ as we store only flag variables in memory during the execution.

---

### 23. Coding Question 7: Write a PyTorch training validation loss check loop.
**Thought Process:**
When fine-tuning open-source LLMs using **PyTorch**, we must write validation loops to monitor training loss and detect overfitting. I would write a standard validation function that disables gradient calculations using `torch.no_grad()`, puts the model in evaluation mode, and iterates through a validation dataloader.

I would loop through the validation batches, passing inputs to the model, and calculating the loss values. I would aggregate these losses and return the average validation loss. If this loss stops decreasing while the training loss continues to fall, it indicates overfitting.

**Code:**
```python
import torch

def validate_model_loss(model, validation_dataloader, loss_function, device):
    # I set the model to evaluation mode, disabling dropout layers
    model.eval()
    total_loss = 0.0
    
    # I disable gradient calculations to save GPU memory and accelerate execution
    with torch.no_grad():
        for batch in validation_dataloader:
            # I transfer our batch data to the active GPU device
            inputs = batch["input_ids"].to(device)
            labels = batch["labels"].to(device)
            
            # I execute the forward pass
            outputs = model(inputs)
            loss = loss_function(outputs, labels)
            
            # I accumulate the validation loss
            total_loss += loss.item()
            
    # I calculate and return the average validation loss
    average_loss = total_loss / len(validation_dataloader)
    return average_loss
```

**Complexity:**
The time complexity of this validation loop is $O(B \times F)$ where $B$ is the number of batches and $F$ is the time complexity of a forward pass through the model layers. The space complexity is $O(M)$ where $M$ is the memory required to store the activation parameters of the batch on the GPU.

---

### 24. Coding Question 8: Create an automated RAG citation verifier.
**Thought Process:**
To implement an automated citation verifier for our **RAG** systems, I would check if the facts generated in the model's response are present in the retrieved source passages. This verification helps identify hallucinations before returning the answer to the user.

I would write a function that takes the generated response and the list of retrieved context nodes. I would split the response into sentences. For each sentence, I would verify if its key terms are present in the context passages. If a sentence has no match, I flag it as unverified.

**Code:**
```python
def verify_rag_citations(generated_response, retrieved_contexts):
    # I split the generated response into individual sentences
    sentences = generated_response.split(".")
    verification_results = []
    
    # I combine all retrieved contexts into a single lowercase text block
    combined_context = " ".join(retrieved_contexts).lower()
    
    for sentence in sentences:
        clean_sentence = sentence.strip()
        if not clean_sentence:
            continue
            
        # I check if the sentence keywords exist in the context block
        words = [w.lower() for w in clean_sentence.split() if len(w) > 4]
        # I consider the sentence verified if at least eighty percent of its keywords exist in the context
        if words:
            match_count = sum(1 for w in words if w in combined_context)
            is_verified = (match_count / len(words)) >= 0.8
        else:
            is_verified = True
            
        verification_results.append({"sentence": clean_sentence, "verified": is_verified})
        
    return verification_results
```

**Complexity:**
The time complexity is $O(S \times W \times C)$ where $S$ is the number of sentences, $W$ is the number of words per sentence, and $C$ is the length of the combined context. The space complexity is $O(S)$ to allocate memory for the validation results list.

---

### 25. Coding Question 9: Implement a thread-safe LlamaIndex document metadata updater.
**Thought Process:**
When multiple ingestion workers update metadata tags (like upload dates and access scopes) for LlamaIndex documents concurrently, we must synchronize access. Without synchronization, concurrent writes can cause index corruption. I would write a thread-safe document manager in **Python** using re-entrant locks.

I would initialize a threading `RLock` in the document manager class. When updating metadata, I would acquire the lock using a context manager. This blocks other threads from modifying the document registry until the current transaction completes.

**Code:**
```python
import threading

class ThreadSafeDocumentRegistry:
    def __init__(self):
        # I initialize our document store and a re-entrant lock
        self.documents = {}
        self.lock = threading.RLock()
        
    def update_document_metadata(self, doc_id, new_metadata):
        # I acquire the lock to block other threads from writing
        with self.lock:
            if doc_id in self.documents:
                doc = self.documents[doc_id]
                # I update the metadata dictionary of the document
                doc["metadata"].update(new_metadata)
                return True
            return False
            # The lock is released automatically when we exit the block
```

**Complexity:**
The time complexity of this update is $O(U)$ where $U$ represents the number of metadata fields updated. The space complexity is $O(1)$ as we modify the document reference in-place.

---

### 26. Coding Question 10: Create a sliding window token bucket rate limiter in Python.
**Thought Process:**
To prevent API token exhaustion when querying commercial LLMs, I would implement a token bucket rate limiter in **Python**. The rate limiter will track available tokens and execute a cooling-off period once the limit is breached, preventing API blockages.

I would initialize our bucket with a maximum capacity and a fill rate. When a request arrives requiring $T$ tokens, I calculate how many tokens have been added since our last request based on the elapsed time, add them to the bucket, and decrement the bucket if sufficient tokens are available.

**Code:**
```python
import time

class TokenBucketRateLimiter:
    def __init__(self, max_tokens, fill_rate_per_sec):
        self.max_tokens = max_tokens
        self.fill_rate = fill_rate_per_sec
        self.available_tokens = max_tokens
        self.last_update_time = time.time()
        
    def consume_tokens(self, tokens_required):
        current_time = time.time()
        elapsed_time = current_time - self.last_update_time
        
        # I calculate refilled tokens and update the bucket level
        refilled_tokens = elapsed_time * self.fill_rate
        self.available_tokens = min(self.max_tokens, self.available_tokens + refilled_tokens)
        self.last_update_time = current_time
        
        # I check if the bucket has enough tokens
        if self.available_tokens >= tokens_required:
            self.available_tokens -= tokens_required
            return True
            
        # I block the request if the bucket is empty
        return False
```

**Complexity:**
The time complexity of this rate-limiting check is $O(1)$ as it involves only basic mathematical calculations. The space complexity is $O(1)$ to store the bucket level and timestamp variables in memory.

---

### 27. Coding Question 11: Write a FastAPI endpoint that swaps LLMs using a router class.
**Thought Process:**
To build a model gateway in **FastAPI** that allows downstream services to swap LLMs dynamically, I would write an endpoint that accepts a target model name in the JSON payload. I would design a router class that selects the appropriate API connector based on this parameter.

I would write the endpoints as asynchronous handlers. If the payload requests "openai", the router executes a call to the OpenAI API wrapper. If it requests "llama", it routes the call to our self-hosted inference engine, returning a unified response model.

**Code:**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ModelRequest(BaseModel):
    prompt: str
    target_model: str # e.g. 'openai' or 'llama'

@app.post("/generate_text")
async def generate_text(request: ModelRequest):
    # I select the model connector based on the target_model parameter
    model_name = request.target_model.lower()
    
    if model_name == "openai":
        # In production, I would return await call_openai(request.prompt)
        return {"model": "OpenAI", "output": "response_from_openai"}
    elif model_name == "llama":
        # In production, I would return await call_self_hosted_llama(request.prompt)
        return {"model": "LLaMA-70B", "output": "response_from_llama"}
    else:
        # I raise an HTTP 400 bad request if the model name is unsupported
        raise HTTPException(status_code=400, detail="Unsupported model provider")
```

**Complexity:**
The time complexity of the routing logic is $O(1)$ dictionary lookup. The space complexity is $O(1)$ to store the request parameter references in memory during the execution.

---

### 28. Coding Question 12: Implement an automated RAG evaluator using G-Eval metric.
**Thought Process:**
To build an automated **RAG** evaluator that measures answer relevance, I would implement a simple G-Eval metric in **Python**. G-Eval uses a large language model to evaluate generated text based on a set of criteria, returning a score from one to five.

I would write a function that formats a evaluation prompt, containing the user query, retrieved context, generated answer, and evaluation instructions. I would call our LLM API, parse the returned response string to extract the numerical score, and return it.

**Code:**
```python
def evaluate_answer_relevance(query, context, generated_answer):
    # I format our evaluation prompt containing instructions for the evaluator model
    evaluation_prompt = f"""
    Evaluate the relevance of the answer to the query based on the context.
    Query: {query}
    Context: {context}
    Answer: {generated_answer}
    Rate the answer on a scale from 1 (irrelevant) to 5 (highly relevant).
    Output only the score as a single integer.
    """
    
    # In production, I would execute the LLM API call
    # response = await openai_client.chat.completions.create(model="gpt-4", prompt=evaluation_prompt)
    # score = int(response.choices[0].text.strip())
    
    # For simulation, I return a default success score
    score = 5
    return {"relevance_score": score}
```

**Complexity:**
The time complexity of formatting the evaluation prompt is $O(C)$ where $C$ is the total length of the query, context, and answer. The space complexity is $O(C)$ to allocate memory for the prompt string.

---

### 29. Coding Question 13: Create a LlamaIndex custom metadata extractor.
**Thought Process:**
When indexing clinical documents in **LlamaIndex**, we must enrich our text nodes with metadata tags (like patient IDs and dates) to enable pre-filtering during RAG queries. I would write a custom metadata extractor class in **Python** that extends LlamaIndex's base classes.

I would write an extraction method that parses the raw text of each node. I would use regex patterns to locate patient identifiers and date codes. If a pattern matches, I extract the string, clean the spaces, and write it to the node's metadata dictionary.

**Code:**
```python
import re

class PatientMetadataExtractor:
    def __init__(self):
        # I compile regular expressions to locate patient IDs and dates
        self.id_pattern = re.compile(r'Patient\s*ID:\s*([a-zA-Z0-9]+)')
        self.date_pattern = re.compile(r'Date:\s*(\d{2}/\d{2}/\d{4})')
        
    def extract_metadata(self, text_content):
        metadata = {}
        
        # I search for a patient ID match in the text content
        id_match = self.id_pattern.search(text_content)
        if id_match:
            metadata["patient_id"] = id_match.group(1).strip()
            
        # I search for a date match in the text content
        date_match = self.date_pattern.search(text_content)
        if date_match:
            metadata["visit_date"] = date_match.group(1).strip()
            
        return metadata
```

**Complexity:**
The time complexity of this extraction is $O(L)$ where $L$ is the length of the node's text content, as regular expression matching scans the characters. The space complexity is $O(1)$ to store the extracted metadata key-value pairs.

---

### 30. Coding Question 14: Implement a text overlap validation checker.
**Thought Process:**
In **RAG** systems, when splitting text using sliding window splitters, we must verify that the consecutive chunks overlap correctly. If the overlap is too small or missing, we risk losing context at the boundaries. I would write a validation function in **Python** to check the overlap size between two chunks.

I would compare the end of the first chunk with the start of the second chunk. I would write a loop that slices the end of the first chunk and compares it with the prefix of the second chunk, looking for the longest matching substring to determine the overlap size.

**Code:**
```python
def check_chunk_overlap(chunk_a, chunk_b, target_overlap_chars=200):
    len_a = len(chunk_a)
    len_b = len(chunk_b)
    max_check = min(len_a, len_b, target_overlap_chars * 2)
    longest_overlap = 0
    
    # I loop through potential overlap lengths to find matching substrings
    for i in range(1, max_check + 1):
        # I slice the end of chunk A and the start of chunk B
        suffix_a = chunk_a[-i:]
        prefix_b = chunk_b[:i]
        
        if suffix_a == prefix_b:
            longest_overlap = i
            
    # I verify if the longest overlap meets our target size
    is_valid = longest_overlap >= target_overlap_chars
    return {"overlap_chars": longest_overlap, "is_valid": is_valid}
```

**Complexity:**
The time complexity of this comparison is $O(O^2)$ where $O$ is the maximum check window size (target overlap chars * 2), due to string slicing and comparisons in the loop. The space complexity is $O(O)$ to store the sliced substrings.

---

### 31. Coding Question 15: Create an asynchronous health check router in FastAPI.
**Thought Process:**
To support containerized deployments in **Kubernetes**, our **FastAPI** backend services must expose health check endpoints. The cluster manager uses these endpoints to verify if the container is healthy. I would write an asynchronous health check router in FastAPI.

I would write an endpoint that returns a status message. I would also add checks to verify that our external database connections and Redis caches are active. If a check fails, I return an HTTP 500 error, notifying Kubernetes to restart the pod.

**Code:**
```python
from fastapi import FastAPI, Response, status

app = FastAPI()

@app.get("/healthz")
async def health_check(response: Response):
    # I simulate checking our database connection status
    database_ok = True 
    # I simulate checking our Redis cache connection status
    redis_ok = True
    
    # I check if all services are online
    if database_ok and redis_ok:
        return {"status": "healthy", "services": "online"}
    else:
        # I set the response status code to 500 Internal Server Error
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "unhealthy", "services": "offline"}
```

**Complexity:**
The time complexity of the health check is $O(1)$ as we check only pre-established connection flags. The space complexity is $O(1)$ to store the status messages in memory.

---

### 32. Coding Question 16: Build a custom metadata-based vector search pre-filter.
**Thought Process:**
To optimize vector search queries in RAG systems, we must pre-filter our document index based on metadata tags (like access scopes or upload dates) before running semantic lookups. I would write a pre-filter function in **Python** that filters list items.

I would write a function that takes a list of document nodes and a filter dictionary. I would loop through the nodes, checking if their metadata dictionary contains all the keys and matching values specified in the filter. I return the list of matching nodes.

**Code:**
```python
def pre_filter_nodes(document_nodes, filter_criteria):
    filtered_nodes = []
    
    for node in document_nodes:
        node_metadata = node.get("metadata", {})
        match = True
        
        # I check if the node metadata matches all filter criteria keys and values
        for key, value in filter_criteria.items():
            if node_metadata.get(key) != value:
                match = False
                break
                
        if match:
            # I append the matching node to our results
            filtered_nodes.append(node)
            
    return filtered_nodes
```

**Complexity:**
The time complexity of this pre-filtering is $O(N \times F)$ where $N$ is the number of nodes in the list and $F$ is the number of filter keys. The space complexity is $O(M)$ where $M$ is the number of matching nodes, representing the size of the output list.

---

### 33. Coding Question 17: Write a LangGraph conditional edge routing function.
**Thought Process:**
In **LangGraph** architectures, conditional edges determine which node to execute next based on the values in the shared state. I would write a routing function in **Python** that inspects our graph state and returns the next target node name.

I would write a function that takes the state dictionary as an argument. I would inspect the model's output string. If the string contains tool-calling commands, I return "execute_tools"; if the output is complete, I return "end_node".

**Code:**
```python
def condition_edge_router(graph_state):
    # I extract the model's output from our graph state
    agent_output = graph_state.get("output", "").lower()
    
    # I determine the routing path based on the content of the output
    if "call_tool:" in agent_output:
        # I route to the execution node if the agent requests a tool call
        return "execute_tools"
    elif "final_answer:" in agent_output:
        # I route to the end node if the agent has compiled the final answer
        return "end_node"
    else:
        # I default to the retry node if the output format is unrecognized
        return "retry_agent"
```

**Complexity:**
The time complexity of this routing check is $O(1)$ as we run only basic string inspections. The space complexity is $O(1)$ to store the node name string in memory.

---

### 34. Coding Question 18: Implement an L2 distance vector retriever.
**Thought Process:**
To implement a custom L2 distance vector retriever in **Python** for a RAG system, I would calculate the Euclidean distance between a query embedding vector and each document embedding in our database, returning the top-K closest matching nodes.

I would write a loop to iterate through our document collection. For each document, I would calculate the sum of squared differences between the query vector and the document vector, taking the square root to determine the L2 distance. I would sort the nodes by distance.

**Code:**
```python
import math

def retrieve_top_k_l2(query_vector, document_database, k=2):
    distances = []
    
    for doc in document_database:
        doc_vector = doc["vector"]
        sum_squared_diff = 0.0
        
        # I calculate the squared difference for each vector dimension
        for q_val, d_val in zip(query_vector, doc_vector):
            sum_squared_diff += (q_val - d_val) ** 2
            
        l2_distance = math.sqrt(sum_squared_diff)
        distances.append({"doc_id": doc["id"], "text": doc["text"], "distance": l2_distance})
        
    # I sort the documents by L2 distance (ascending order) and return the top-K
    distances.sort(key=lambda x: x["distance"])
    return distances[:k]
```

**Complexity:**
The time complexity of this retrieval is $O(N \times D + N \log N)$ where $N$ is the number of documents in the database, $D$ is the vector dimension, and $N \log N$ represents the sorting cost. The space complexity is $O(N)$ to store the distance values in memory.

---

### 35. Coding Question 19: Create a Python decorator to measure API latency.
**Thought Process:**
To monitor the performance of our **FastAPI** routers and database calls in production, I would implement a custom **Python** decorator to measure execution latency. The decorator will record start and end times and write the metrics to a log file.

I would write a decorator function that wraps our async handlers. I would record the timestamp before execution using `time.time()`, await the execution of the wrapped function, and calculate the elapsed time. I would log this latency value before returning the result.

**Code:**
```python
import time
import functools

def log_latency_async(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        
        # I execute the wrapped asynchronous function and capture its response
        result = await func(*args, **kwargs)
        
        # I calculate the execution duration
        latency_sec = time.time() - start_time
        print(f"Function {func.__name__} executed in {latency_sec:.4f} seconds")
        
        return result
    return wrapper
```

**Complexity:**
The time complexity of this decorator is $O(1)$ overhead beyond the execution of the wrapped function itself. The space complexity is $O(1)$ to store the timestamp variables in memory.

---

### 36. Coding Question 20: Build an async pipeline coordinator in Python.
**Thought Process:**
To run multiple independent data retrieval tasks (like querying Pinecone, scraping text, and checking database records) in parallel during a RAG pipeline query, I would use Python's **asyncio** library. This concurrent execution reduces overall API latency.

I would write an asynchronous function that defines our data tasks. I would use `asyncio.gather()` to launch all tasks concurrently, awaiting their completion and collecting the returned results in a single list, ensuring we do not execute tasks sequentially.

**Code:**
```python
import asyncio

async def fetch_vector_matches(query):
    await asyncio.sleep(0.5) # Simulates vector search lookup
    return ["vector_context_node"]

async def fetch_relational_data(user_id):
    await asyncio.sleep(0.3) # Simulates SQL database lookup
    return ["relational_context_node"]

async def execute_rag_pipeline_async(query, user_id):
    # I execute both retrieval tasks concurrently using asyncio.gather
    results = await asyncio.gather(
        fetch_vector_matches(query),
        fetch_relational_data(user_id)
    )
    
    # I unpack and combine the retrieved context nodes
    combined_context = results[0] + results[1]
    return combined_context
```

**Complexity:**
The time complexity is $O(\max(T_1, T_2))$ where $T_1$ and $T_2$ represent the execution times of the individual tasks, running in parallel. The space complexity is $O(C)$ where $C$ is the size of the combined context list in memory.

---
