---
title: Sai Sharath Infosys STG Prep Guide
description: Comprehensive preparation guide for the Specialist Programmer (STG) interview at Infosys, customized for Sai Sharath Chandra Mahankali.
---

# Sai Sharath Chandra Mahankali Prep Guide: Specialist Programmer (Infosys STG)

Welcome to your preparation guide for the Specialist Programmer role within the **Strategic Technology Group (STG)** unit at **Infosys Limited**. This guide is designed around your experience in building production-grade generative AI systems, deep learning models, and high-performance data architectures at **J.P. Morgan Chase** and **Robosoft Technologies**, mapping those competencies directly to the Infosys STG unit requirements (generative AI models development, deep learning frameworks, model lifecycle management, cloud platform scaling, reusable asset creation, and technical leadership).

---

## Resume & Role Alignment

The Specialist Programmer role within the STG unit requires technologist leaders who can analyze use cases, define design specifications, create reusable assets, and deliver optimized code across applications and databases. The role focuses on developing, fine-tuning, and deploying generative AI and deep learning models on cloud platforms while championing responsible AI practices.

Here is how your background directly bridges to these requirements:

*   **Generative AI & LLM Fine-Tuning:** At J.P. Morgan Chase, you automated model evaluation and CI/CD pipelines for LLM fine-tuning workflows, reducing deployment cycles from 5 days to 8 hours across 12 model versions. This directly maps to the requirement to fine-tune pre-trained models.
*   **Large-Scale RAG & Vector Indexing:** You architected a RAG pipeline using **LangChain**, **Pinecone**, and Hugging Face models to process 2.5 million documents, and optimized indexing in Pinecone to support 10 million embeddings, matching the JD's focus on scalable data structures.
*   **Performance Optimization & MLOps:** You optimized LLM inference on GPU clusters using **4-bit/8-bit quantization**, reducing latency from 3s to 400ms across 50 production endpoints, and deployed containers on AWS EKS, aligning with the cloud platform requirement.
*   **Deep Learning & Image Processing:** You developed a **YOLOv5** computer vision system using **PyTorch** and **Apache Spark** for real-time object detection across 20 video streams at Robosoft, demonstrating your proficiency in deep learning frameworks.
*   **AI Safety & Guardrails:** You implemented prompt-injection defense layers and AI guardrails across 15 conversational applications, averting $3M in compliance risk exposure, which directly maps to championing responsible AI.

---

## Part 1: Top 30 Technical & Consulting Questions & Answers

### 1. How do you manage the entire generative AI development lifecycle, from data preprocessing to production deployment and evaluation?
Managing the generative AI development lifecycle requires a structured, multi-phase engineering process. During the data preprocessing phase, we extract unstructured raw text, clean formatting noise using regular expressions, and split the text into semantic paragraphs to prevent context dilution. We then convert these chunks into dense vector representations using embedding models and index them in vector databases like **Pinecone** to support semantic search.

During the model training and fine-tuning phase, we load pre-trained foundation models and apply Parameter-Efficient Fine-Tuning (PEFT) parameters like **LoRA** and **QLoRA** to specialize the model on domain-specific datasets, keeping base weights frozen to minimize GPU computing memory. We evaluate the model using automated **LLM-as-a-Judge** scoring matrices to track correctness, relevance, and compliance before packaging the code inside **Docker** containers.

For production deployment and optimization, we compile the models using **TensorRT-LLM** to run on GPU clusters, utilizing **vLLM** to handle high-throughput inference requests. We deploy these containers on Kubernetes (EKS) clusters, configuring Horizontal Pod Autoscalers to scale resources based on traffic demands. We integrate monitoring tools like **MLflow** to track metrics, feature drift, and latency spikes in real-time, ensuring continuous model improvement.

---

### 2. Can you explain your approach to fine-tuning pre-trained LLMs using parameter-efficient methods like LoRA and QLoRA?
Fine-tuning pre-trained LLMs for domain-specific tasks requires adjusting the model to capture specialized terminology while minimizing compute resource overhead. To achieve this, I use Parameter-Efficient Fine-Tuning (PEFT) with LoRA (Low-Rank Adaptation) and QLoRA (Quantized LoRA). These techniques freeze the original model weights and insert small, trainable low-rank decomposition matrices into the attention projection layers.

QLoRA improves this process by quantizing the base model weights to a 4-bit NormalFloat (NF4) data type, which drastically reduces the GPU memory required for training. During backpropagation, the gradients are calculated only for the adapter matrices, which represent less than one percent of the total model parameters. This allows us to fine-tune large foundation models (like LLaMA-70B) on consumer-grade GPU clusters, reducing compute costs.

At **J.P. Morgan Chase**, I automated model evaluation and CI/CD pipelines for LLM fine-tuning workflows, reducing our deployment cycle times from 5 days to 8 hours. I wrote Python scripts using Hugging Face's PEFT and TRL libraries to configure the LoRA hyperparameters (such as rank size and alpha scaling). This automated pipeline allowed us to train and evaluate 12 model versions in parallel, ensuring optimal performance and domain alignment.

---

### 3. How did you design a RAG pipeline at J.P. Morgan Chase to process 2.5 million financial documents using LangChain and Pinecone?
At **J.P. Morgan Chase**, I architected a Retrieval-Augmented Generation (RAG) pipeline using **LangChain**, **Pinecone**, and Hugging Face models to process 2.5 million internal documents, reducing analyst research time by 6,000 hours annually. The primary engineering challenge was retrieving relevant context passages from unstructured PDFs and text files without introducing latency or hallucination risks.

I designed the ingestion pipeline using **Apache Spark** to clean the raw text and split it into semantic chunks using recursive splitters. I converted these chunks into dense vector embeddings and stored them in Pinecone. I configured the Pinecone indexes with custom metadata tags (such as file dates and security levels), which allowed us to apply pre-filtering during queries, ensuring sub-200ms semantic search execution.

When an analyst submitted a query, the RAG pipeline performed a hybrid semantic search across Pinecone, retrieved the top-K context chunks, and formatted them into a prompt template for the LLM. I also integrated a re-ranking model to sort the retrieved nodes, ensuring only the most relevant context was sent to the model to compile the final cited response. This system delivered accurate, auditable financial summaries.

---

### 4. How did you optimize LLM inference on GPU clusters using 4-bit and 8-bit model quantization techniques?
Optimizing LLM inference is critical when deploying financial applications, as latency spikes can degrade user experience and increase cloud infrastructure hosting costs. At **J.P. Morgan Chase**, I slashed model inference latency from 3 seconds to 400 milliseconds across 50 production endpoints by implementing 4-bit and 8-bit model quantization on our GPU clusters. Quantization reduces the precision of model weights from float16 to int4/int8.

I utilized quantization frameworks like AWQ (Activation-aware Weight Quantization) and GPTQ, compiling the quantized models using **TensorRT-LLM** to run on our NVIDIA GPU nodes. AWQ is particularly effective because it protects the most important weights (outliers) during the quantization process, maintaining model accuracy while achieving high compression rates. I deployed these compiled models inside **Docker** containers, using **vLLM** as our high-throughput inference engine.

This optimization allowed us to fit larger models onto fewer GPU cards, reducing our hardware requirements and saving cloud costs. The reduction in latency to 400ms enabled our conversational applications and budget variance agents to process user prompts and return answers in near real-time. This high performance is essential when building interactive copilots that support finance leaders during live budgeting sessions.

---

### 5. How did you optimize Pinecone vector database indexing to support 10 million embeddings and sub-200ms semantic search?
Optimizing vector databases at scale requires configuring index parameters and query schemas to minimize search latency and maximize recall accuracy. At **J.P. Morgan Chase**, I optimized our **Pinecone** vector database indexing strategies to support 10 million embeddings, enabling sub-200-millisecond semantic search execution for 500 concurrent users. 

I achieved this by structuring our vector indexes using Cosine similarity and configuring metadata indexes. By indexing key fields (such as document date, region, and security classification) in Pinecone, we could apply metadata pre-filtering to our queries. This narrowed down the vector search space, preventing full-index scans and reducing query processing times.

I also optimized the client-side query logic, executing vector lookups in parallel batches and caching common search results in Redis. This caching layer bypassed vector database queries for repeated questions, cutting average response latencies. By combining metadata pre-filtering, batch querying, and caching, I guaranteed that our RAG applications delivered fast semantic search results, even under heavy concurrent user loads.

---

### 6. What prompt-injection defense layers did you deploy across 15 conversational applications to mitigate compliance risks?
Prompt injection is an exploit where an attacker inputs malicious text designed to override the system instructions of an LLM, forcing the agent to execute unauthorized commands or leak confidential data. In financial applications, this is a critical risk, as an injected prompt could command the agent to bypass credit rules, expose PII, or execute unauthorized transactions. At **J.P. Morgan Chase**, I deployed prompt-injection defense layers across 15 conversational applications.

I implemented a multi-layered guardrail architecture. The first layer is an input validation filter that evaluates the user prompt using classification models (like Guardrails AI or NeMo Guardrails) to detect adversarial text patterns. The second layer uses strict XML delimiter separation in our prompt templates, defining the system instructions, context variables, and user input fields in distinct blocks, preventing the LLM from executing user text as instructions.

The final layer is output validation, where we run Pydantic schema validation on the model's response. If the agent's output contains system code or does not conform to the expected JSON schema, the response is blocked and logged. I also applied the principle of least privilege, ensuring that our agents only had read access to specific databases, preventing destructive commands. This defense architecture averted an estimated $3M in compliance risk exposure.

---

### 7. How did you automate model evaluation and CI/CD pipelines for LLM fine-tuning workflows, reducing cycle time to 8 hours?
Automating LLM evaluation and CI/CD pipelines is essential to prevent manual errors and configuration drift, enabling rapid deployment of optimized models. At **J.P. Morgan Chase**, I built an automated pipeline that reduced deployment cycle times from 5 days to just 8 hours. The pipeline is triggered automatically when a developer updates a model configuration or a training dataset.

The workflow begins by running code validation and unit tests using pytest. Next, the pipeline triggers a distributed fine-tuning job on our GPU clusters, training the adapter layers using **LoRA** and **QLoRA** parameters to minimize compute usage. Once training completes, the model is evaluated against our golden validation dataset using an automated **LLM-as-a-Judge** framework to measure correctness, relevance, and toxicity.

If the model's evaluation scores pass our quality gates, the runner packages the fine-tuned adapter weights inside a **Docker** container and pushes the image to our container registry. The pipeline then executes a rolling deployment to our staging EKS cluster, running integration checks before promoting the model to production, ensuring a fast, secure release cycle.

---

### 8. Explain how you built distributed ETL pipelines using PySpark and Apache Spark to process 8 terabytes of data daily at Robosoft.
At **Robosoft Technologies**, I designed and launched distributed ETL pipelines using **PySpark** and **Apache Spark** that processed 8 terabytes of data daily, cutting our batch processing time by 4 hours. In large-scale machine learning and financial modeling applications, raw data is often fragmented across multiple databases, requiring scalable processing engines to perform joins and aggregations without memory issues.

I wrote PySpark scripts to perform data cleaning, schema validation, and feature engineering in a distributed environment. I optimized our Spark configurations by adjusting executor memory, tuning shuffle partitions, and implementing broadcasting joins for our lookup tables. This partitioning prevented data skew and bottleneck issues on our cluster nodes, accelerating our ETL runs.

This data engineering foundation is directly applicable to training and fine-tuning LLMs. When preparing training datasets or context archives for RAG pipelines, we must process millions of document records. By leveraging PySpark and Apache Spark, we can clean, join, and format these massive datasets in parallel, feeding clean inputs to our vector databases and fine-tuning engines.

---

### 9. Describe your computer vision project using YOLOv5 and PyTorch to detect helmet usage across urban monitoring zones.
At **Robosoft Technologies**, I implemented a computer vision analytics system using **YOLOv5** and **PyTorch** to detect helmet usage, triggering real-time compliance alerts for 3 urban monitoring zones. The technical challenge was processing 20 concurrent high-definition video streams in real-time, which required optimizing model inference and data pipelines.

I trained the YOLOv5 object detection model on our custom labeled image datasets using PyTorch. To handle the high-throughput video streams, I architected parallelized model training and data aggregation workflows using **Apache Spark**, shortening end-to-end training cycles by 4 hours. This parallelization allowed us to distribute the video frame processing tasks across our cluster nodes.

I optimized the trained model using TensorRT to reduce parameter size, allowing the system to run on edge GPU nodes. The system processed 20 concurrent video streams, reducing manual monitoring labor by 4,800 hours per year. This project demonstrated my ability to apply deep learning architectures and scale model inference pipelines, which is highly applicable to deploying high-performance AI solutions at Infosys.

---

### 10. How did you train NLP models using SpaCy to process 1 million customer support tickets at Robosoft Technologies?
At **Robosoft Technologies**, I trained NLP models with **SpaCy** for entity extraction and sentiment classification, processing 1 million customer support tickets and reducing manual triage times by 3,200 hours annually. Support tickets are unstructured text records that require fast classification to route critical incidents to the correct engineering teams.

I wrote Python scripts using SpaCy's pipeline utilities, tokenizing ticket descriptions, removing stop words, and extracting key entities (such as customer IDs, product names, and error codes). I trained a custom classifier on these features to assign urgency tags. I used Pandas and NumPy to validate the dataset inputs, ensuring the training records were clean.

I integrated this NLP model with our backend ticketing tools, automating the triage and routing processes. This automated classification reduced manual sorting times and improved our team's response speed. I will bring this NLP and text analytics expertise to Infosys's generative AI projects, designing pipelines that clean, structure, and categorize customer text inputs.

---

### 11. How did you design a JavaScript-based experiment tracking infrastructure to streamline A/B testing across 6 product features?
At **Robosoft Technologies**, I streamlined our A/B testing infrastructure across six product features using **JavaScript-based** experiment tracking, driving $500,000 in incremental revenue through data-driven feature decisions. In digital product environments, running experiments requires a reliable tracking infrastructure to capture user interactions without degrading client-side page load performance.

I designed a lightweight JavaScript SDK that intercepted client-side user events, logged them to our analytics server, and assigned users to control or treatment groups based on hashing algorithms. The client-side script ran asynchronously, preventing page load delays. I configured **Apache Kafka** to ingest these event streams, routing them to our PySpark ETL pipelines for real-time aggregation.

I then built statistical validation dashboards in Power BI, using DAX to calculate statistical significance, p-values, and conversion rate increases. This end-to-end experiment tracking infrastructure allowed our product teams to validate feature rollouts, optimize user experiences, and make data-driven decisions, demonstrating my ability to build scalable, business-focused analytics applications.

---

### 12. Compare your experience using PyTorch and TensorFlow across deep learning projects.
PyTorch and TensorFlow are both popular deep learning frameworks, but they differ in execution paradigms and deployment workflows. PyTorch uses a dynamic computation graph, which allows developers to modify model architectures at runtime and debug code easily using standard Python tools, making it ideal for research and prototyping.

TensorFlow uses a static graph paradigm, compiling the model architecture before execution, which provides optimization and deployment capabilities for enterprise platforms. When building our **YOLOv5** helmet detection system at Robosoft, I used **PyTorch** because its dynamic graph structure allowed us to write custom loss functions and inspect model layers during training.

I am comfortable using both frameworks, having earned Microsoft certifications in deep learning using **TensorFlow**. I select the framework based on project requirements: I use PyTorch when designing novel neural networks or fine-tuning transformer models that require rapid experimentation, and use TensorFlow when integrating models with legacy systems that require static optimizations.

---

### 13. How do you design and create reusable software assets to enhance developer productivity in AI projects?
Designing reusable software assets requires building modular, well-documented code libraries that abstract complex operations, allowing other developers to implement features without writing code from scratch. In machine learning projects, we look for repetitive tasks (such as database connections, log formatting, or model evaluation) and package them as custom libraries.

I design these assets by writing modular Python packages, defining clean APIs and using Pydantic for input validation. I package the libraries using Docker and distribute them through our team's private container registry. I write comprehensive documentation and few-shot examples in Confluence, making the packages easy for other engineering teams to adopt.

At TCS, I assisted in the creation of reusable assets for our model monitoring and metadata migration pipelines, standardizing deployments across six engineering teams. This standardization reduced release coordination times and improved developer productivity. I will bring this asset-creation discipline to Infosys, building reusable frameworks that accelerate our AI projects.

---

### 14. How do you champion responsible AI practices, focusing on bias mitigation, fairness, and explainability?
Championing responsible AI requires establishing validation checks to ensure our models are fair, unbiased, and explainable. Machine learning models can learn to perpetuate historical bias if the training data is imbalanced. To prevent this, we must audit our datasets and model predictions using fairness metrics.

I use Python libraries like Fairlearn to calculate disparate impact and equalized odds, measuring if our models behave consistently across different demographic groups. If I detect bias, I apply mitigation techniques (such as re-weighting training samples or adjusting model decision thresholds post-prediction). I also use SHAP and LIME to generate local feature explanations, ensuring our models are auditable.

I will advocate for these responsible AI practices at Infosys. I will write validation scripts to test our models for bias, document model cards to describe training parameters, and integrate explainability metrics into our dashboards. This transparency ensures that our AI solutions are compliant, fair, and trusted by stakeholders.

---

### 15. How do you approach debugging complex routines and memory leaks in distributed machine learning systems?
Debugging complex routines and memory leaks in distributed ML systems requires a structured, tool-driven process. When running models on GPU clusters or PySpark nodes, memory issues (like out-of-memory errors) can occur due to uncollected tensors, large data shuffles, or improper garbage collection.

I begin by inspecting our system logs and memory metrics in Grafana or AWS CloudWatch. If a GPU memory leak is suspected, I use Python memory profilers (like PyTorch's `torch.cuda.memory_summary()`) to inspect tensor allocations and identify which objects are remaining in memory. I write scripts to delete unused tensors and force garbage collection.

In PySpark pipelines, I optimize shuffle partitions and use broadcast joins for lookup tables to prevent data skew and out-of-memory errors on worker nodes. By analyzing execution plans and isolating resource bottlenecks, I can resolve performance issues. This debugging skill guarantees that our production AI systems run reliably.

---

### 16. Tell us about your experience building initial prototypes and POCs for emerging AI technologies.
Building prototypes and Proof of Concept (POC) systems is essential to evaluate the feasibility of emerging AI technologies before committing to production development. When a new model architecture or AI framework (like agentic workflows) is released, I build a lightweight sandbox application to test its capabilities on our business data.

I use tools like Jupyter Notebook and Streamlit to design these prototypes, allowing stakeholders to interact with the model early. For example, when testing agentic workflows using **LangGraph** and **CrewAI**, I built a prototype budget variance reporting agent, testing how the model handled tool-calling and graph state transitions.

I evaluate the prototype against baseline metrics (such as latency, API cost, and output correctness). This evaluation provides stakeholders with data-driven insights, helping them decide if the emerging technology is ready for production. I will bring this prototyping agility to Infosys STG, helping you evaluate and adopt emerging AI services.

---

### 17. How do you apply software design patterns to build stateful multi-agent systems using LangGraph or CrewAI?
Building stateful multi-agent systems requires designing architectures that manage state transitions, coordinate agent tasks, and handle exceptions. I use software design patterns (such as the State pattern and the Supervisor-Worker pattern) to structure these agentic workflows using **LangGraph** and **CrewAI**.

The State pattern is implemented by defining a centralized state schema (using Pydantic or TypedDict) that is passed to every node in the graph. As agents and tools execute, they return updates that are merged into the central state. The Supervisor-Worker pattern is used to coordinate tasks: a supervisor agent evaluates the query and routes tasks to specialized worker agents.

I write conditional edges to manage routing logic, checking the state variables to determine the next node. If an agent fails to complete a task, a rollback transition routes the state back to a previous node with a feedback payload. This modular design ensures that our agentic workflows are testable, stateful, and resilient in production.

---

### 18. Explain how you configure Docker containers and Kubernetes (EKS) to deploy and scale AI inference engines.
Deploying AI inference engines in production requires containerizing our services and orchestrating them to scale dynamically based on request traffic. I package our Python inference APIs (built using **FastAPI**) inside **Docker** containers, writing multi-stage Dockerfiles to minimize the final container image size.

I deploy these containers on AWS EKS (Elastic Kubernetes Service), writing Kubernetes manifests to define our deployments, services, and ingress rules. I configure Horizontal Pod Autoscalers (HPA) to scale the number of pods dynamically based on CPU usage or concurrent request metrics. I allocate specific GPU memories to our inference pods.

I use **vLLM** as our high-throughput inference engine, which supports dynamic paging (PagedAttention) to optimize GPU memory utilization. I integrate Prometheus and Grafana to monitor container health and API latencies. This containerization and scaling configuration guarantees high availability and performance for our production AI endpoints.

---

### 19. How do you ensure LLM outputs conform to structured Pydantic schemas for downstream REST API consumption?
In multi-agent systems, ensuring that LLM outputs conform to structured schemas is critical because downstream APIs and databases require typed JSON objects to process transactions. If the model returns unstructured text, the parsing step will fail, causing pipeline errors. I resolve this by using Pydantic schema validation.

I define our target schemas as Pydantic models in Python, specifying data types, required fields, and validation constraints. When calling the OpenAI API or a self-hosted model, I configure the request to use structured outputs, passing the Pydantic schema directly. This forces the model's token selection to adhere to the JSON schema.

If the model is accessed without built-in structured output support, I write a validator wrapper: when the response arrives, the wrapper parses the string as JSON and attempts to instantiate the Pydantic model. If validation fails, the wrapper captures the formatting error and executes a retry loop asking the model to fix its outputs, guaranteeing clean JSON.

---

### 20. Describe your experience writing and optimizing SQL queries for large-scale data warehouses.
Writing and optimizing SQL queries is essential to process large volumes of enterprise data, reduce latency, and minimize cloud warehouse costs. I write clean, structured SQL queries, utilizing Common Table Expressions (CTEs), window functions, and indexing strategies to prepare datasets for modeling.

To optimize SQL performance in databases like Snowflake, I analyze execution plans to identify bottlenecks like full table scans or Cartesian products. I structure my join tables on indexed key columns and partition the target tables, ensuring the query engine only scans the relevant data segments, which cuts execution times.

At TCS, I optimized SQL joins across fifty relational tables in **Snowflake**, eliminating Cartesian products and cutting query execution times from fifteen minutes to forty seconds. This database optimization resolved query bottlenecks, reduced compute costs, and ensured our downstream reporting pipelines had fast access to clean datasets.

---

### 21. How do you apply statistical anomaly detection and machine learning to financial fraud or compliance patterns?
Applying anomaly detection to financial data allows us to identify unusual compliance patterns or fraudulent transactions that deviate from normal behavior. We use a combination of supervised classification models and unsupervised anomaly detection algorithms to monitor transaction streams.

Supervised models like **XGBoost** are trained on historical fraud labels to detect known fraud patterns. For new or evolving fraud vectors, we use unsupervised algorithms (such as Isolation Forests or One-Class SVMs) using **Scikit-learn**. The model analyzes features like transaction amounts, locations, and frequencies, assigning an anomaly score to each record.

At J.P. Morgan Chase, I implemented prompt-injection defense layers and AI guardrails to mitigate compliance risk exposure. I combine statistical checks (like z-score analysis on transaction amounts) with machine learning outputs, routing any anomalous transactions to our risk operations queue for manual review, protecting the organization from compliance exposure.

---

### 22. Describe how you designed a recommendation system using Scikit-learn and collaborative filtering at Robosoft.
At **Robosoft Technologies**, I designed and launched a recommendation system using **Scikit-learn** and collaborative filtering, increasing our average order value by $15 across 200,000 monthly active users. In digital product environments, personalization is key to improving user engagement and driving incremental revenue.

I built the recommendation pipeline by extracting user interaction records (clicks, views, and purchases) from our databases. I cleaned the data and constructed a user-item interaction matrix. I used scikit-learn's truncated SVD (Singular Value Decomposition) and cosine similarity algorithms to calculate the similarity scores between users and items, generating recommendations.

I implemented a hybrid filtering approach, combining collaborative filtering with content-based features (like product tags and descriptions) to resolve the cold-start problem for new users. I integrated this recommendation engine with our backend APIs, ensuring recommendations updated dynamically. This project demonstrated my ability to apply machine learning algorithms to drive business growth.

---

### 23. How do you identify, mitigate, and resolve technical risks to meet quality service (QoS) requirements?
Meeting quality service (QoS) requirements (such as system latency, uptime, and throughput SLAs) requires proactive risk management throughout the software development lifecycle. When designing AI systems, the primary risks are model latency spikes, pipeline failures, and resource exhaustion.

I mitigate these risks by designing redundant, fault-tolerant architectures. I configure load balancers to distribute traffic across EKS nodes and implement caching layers (using Redis) to bypass model lookups. I write automated liveness and readiness probes in Kubernetes to detect container failures and route traffic to healthy pods.

I also set up comprehensive logging and alerting dashboards using Prometheus and Grafana, tracking API latencies and error rates. If a service degrades, the monitoring system triggers alerts, allowing us to investigate and resolve the issue. This risk mitigation framework ensures our production applications meet all QoS requirements.

---

### 24. How do you approach reverse engineering methodologies to support the transition process?
Reverse engineering is a structured methodology used to analyze legacy systems, extract their business logic, and document their data flows to support transition processes (such as migrating a legacy system to a modern cloud database or AI pipeline). It requires analyzing database schemas, stored procedures, and codebase repositories.

I begin by mapping out the data models of the legacy system, identifying the primary tables, keys, and foreign relationships. I analyze the source code (in languages like SQL, Java, or C++) to extract the business rules and calculation formulas. I document these workflows visually using Visio and write source-to-target mappings.

This reverse engineering process ensures that when we transition to a new cloud architecture or AI-driven system, no business rules or logic are lost. It allows us to design new schemas and APIs that replicate the legacy outcomes while optimizing performance and scaling. I will apply this methodology to support Infosys's system transition projects.

---

### 25. How do you mentor junior developers and establish best practices in an Agile development environment?
Mentoring junior developers and establishing technical best practices is a core responsibility for senior technologist leaders in the STG unit. I believe in creating a collaborative, growth-focused engineering culture by organizing regular training workshops, pair-programming sessions, and structured code reviews.

I write detailed technical guides and template configurations in Confluence, covering SQL optimization, PyTorch coding standards, and Docker configurations. During code reviews, I provide constructive feedback, explaining why a specific refactoring improves performance. I help junior developers understand clean coding principles and MLOps workflows.

I coordinate Agile delivery activities, backlog refinement, and sprint planning, helping the team break down complex tasks. By sharing knowledge and establishing coding standards, we reduce technical debt, improve code quality, and ensure the team is capable of delivering high-quality, production-ready AI solutions for Infosys's clients.

---

### 26. Describe a time you worked closely with clients or customers during testing and warranty support to resolve critical production issues.
During a deployment phase at **J.P. Morgan Chase**, we launched a new RAG pipeline for our compliance team. During the warranty support window, the client reported that their search queries were experiencing intermittent timeouts, taking over 5 seconds to load data. I worked closely with the compliance stakeholders to diagnose the issue.

I analyzed our system logs and vector search traces, identifying that the latency spike occurred during the vector lookup step in **Pinecone**. The database was performing full-index scans because the client was query-filtering on unindexed metadata tags. I resolved the issue by modifying our Terraform manifests to index the metadata columns.

I re-ran the automated validation checks, confirming that search latency dropped below 200ms. I walked the compliance team through the updates, verifying they were satisfied with the fix. This close collaboration and quick issue resolution during warranty support rebuilt client confidence and guaranteed a stable, production-ready codebase.

---

### 27. Compare AWQ and GPTQ quantization techniques and explain when to choose each format.
AWQ (Activation-aware Weight Quantization) and GPTQ are both popular post-training quantization methods used to compress LLMs, but they differ in how they calculate weight importance and perform quantization. GPTQ evaluates the model weights layer-by-layer and uses second-order information to adjust the remaining weights to minimize error.

AWQ is based on the observation that not all weights are equal. It identifies that only a small percentage (about one percent) of weights (salient weights) are critical to model performance. AWQ preserves these salient weights in higher precision and only quantizes the remaining weights. This activation-aware approach maintains model accuracy on reasoning tasks.

I use AWQ when deploying models for complex reasoning or compliance tasks, where high accuracy is critical and errors are expensive. I use GPTQ for high-volume, structural classification tasks, where throughput is the primary driver and minor variations in output quality are acceptable. I compile both formats using TensorRT-LLM for GPU deployment.

---

### 28. Explain how you evaluate generative outputs using metrics like faithfulness, relevance, and completeness.
Evaluating generative outputs requires moving beyond manual reviews to automated, continuous evaluation frameworks. I implement an evaluation pipeline using **LLM-as-a-Judge** methodologies, utilizing frameworks like RAGAS or TruLens to score our agent runs automatically.

We evaluate three primary dimensions: faithfulness, answer relevance, and completeness. Faithfulness checks if the agent's output is derived entirely from the retrieved context, preventing hallucinations. Answer relevance measures if the output addresses the user's query, and completeness checks if the agent answered all parts of the question.

We write automated scripts that pass our test queries, retrieved context, and generated answers to these scoring engines, producing quantitative quality metrics. We log these evaluation scores for every model candidate in **MLflow**. This automated validation ensures we deploy reliable models, directly mapping to the evaluation and optimization requirements of the Infosys STG JD.

---

### 29. How do you use Apache Airflow and Kafka to coordinate ETL processes and data streams?
Apache Airflow and Kafka are both used to coordinate data pipelines, but they serve different roles: Kafka is a real-time event streaming platform, while Airflow is a batch workflow orchestrator. We combine them to design event-driven, scalable ETL pipelines.

Kafka is configured to ingest high-volume data feeds, decoupling the ingestion layer from downstream databases. Airflow is used to schedule and orchestrate our batch ETL processing jobs, running data validation checks and model retraining tasks at regular intervals. I write Airflow DAGs using Python operators to trigger Spark processing jobs.

At TCS, I orchestrated automated model deployment CI/CD workflows using **Apache Airflow** and **Kubernetes**, standardizing deployments across six engineering teams. I also built streaming ingestion pipelines using **Kafka** and **PySpark** at TCS. This experience allows me to design hybrid data platforms that handle both real-time streams and batch pipelines.

---

### 30. How do you translate user stories and use cases into technical specifications for production-ready delivery?
Translating user stories and use cases into technical specifications requires a structured process that bridges business goals with software architecture. When a product manager submits a user story (like "as an analyst, I want to search financial documents"), I translate this into a technical design document.

I define the data ingestion schemas, select the vector database index parameters, design the API endpoints (using FastAPI), and specify the security guardrails (like prompt-injection defense). I document these specifications using Source-to-Target Mappings, UML diagrams, and Pydantic validation schemas, publishing the files on **Confluence**.

I break down the technical design into manageable development tasks in Jira, defining clear acceptance criteria and UAT validation checks for each task. This requirements gathering and technical design phase ensures that our cross-functional engineering teams can build and deploy production-ready, optimized solutions that meet the business needs.

---
