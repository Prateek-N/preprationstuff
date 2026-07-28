---
title: Prathyush Zed Prep Guide
description: Comprehensive preparation guide for the Senior ML Data Scientist interview at Zed, customized for Prathyush Maniyam.
---

# Prathyush Maniyam Prep Guide: Senior ML Data Scientist (Zed Neobank)

Welcome to your preparation guide for the Senior ML Data Scientist role at **Zed**. This guide is designed around your experience in building production machine learning systems, agentic AI workflows, and LLM-powered applications at **JPMorgan Chase**, **KPMG**, and **Dell Technologies**, mapping those competencies directly to the target JD (core credit underwriting with alternative data, transaction text embeddings, transformer-based sequential modeling, agent scaffolding, real-time fraud models, and model drift monitoring).

---

## Resume & Role Alignment

The Senior ML Data Scientist role at Zed requires underwriting credit using foundation models that profile risk from transaction data, financial documents, and other unstructured sources instead of credit scores. This requires building embeddings models, transformer architectures, and LLM-assisted data pipelines alongside classical credit and fraud models.

Here is how your background directly bridges to these requirements:

*   **Credit Risk & Fraud Detection:** You have 7+ years of experience in applied ML. At JPMorgan, you architected **XGBoost** and **Scikit-learn** risk analytics models identifying fraud patterns across 200K+ daily financial records, improving risk flagging accuracy by 18%.
*   **Transaction Embeddings & Transformers:** At JPMorgan, you operationalized **PySpark**, **Databricks**, and **Airflow** ML workflows with **LoRA/QLoRA** fine-tuning on **AWS SageMaker**, and designed **BERT/Transformer** NLP solutions processing 180K+ compliance records. This aligns with Zed's focus on representing transaction data as vector embeddings.
*   **Agentic AI & LLM Scaffolding:** You developed multi-agent AI systems using **LangGraph**, **CrewAI**, and function calling to automate research workflows, and built a tool-use AI agent framework that deflects 200+ requests monthly. This prepares you to build underwriting agent scaffolding.
*   **MLOps & Model Monitoring:** You built MLOps infrastructure with **MLflow**, **Docker**, **FastAPI**, and **RAGAS/TruLens** evaluation, cutting deployment cycles to under 24 hours. This qualifies you to establish robust model monitoring and alerting on performance degradation and concept drift at Zed.

---

## Part 1: Top 30 Technical & Behavioral Questions & Answers

### 1. How can alternative data be used to underwrite credit for thin-file consumers, and how does your experience with Scikit-learn and XGBoost at JPMorgan Chase map to this?
At **JPMorgan Chase**, I architected **XGBoost** and **Scikit-learn** risk analytics models identifying fraud patterns across 200K+ daily financial records, improving risk flagging accuracy by 18%. In emerging markets like the Philippines, traditional credit bureau coverage is low, leaving many young professionals classified as "thin-file" borrowers. To underwrite these consumers, we must look beyond credit scores to alternative data, including transaction histories, spending behavior, utility bills, and device metadata. Using Python libraries, we can engineer features that capture income stability and spending patterns. For example, we can calculate the ratio of essential to non-essential spending, evaluate average balance trends, and assess transaction frequency. We use XGBoost and Scikit-learn to train models on these behavioral features, establishing credit limits based on statistical risk instead of repayment history.

To build these models, we start with feature engineering, using Scikit-learn preprocessing pipelines to scale features and handle missing data. We use XGBoost because it handles sparse datasets and captures non-linear relationships. We optimize hyper-parameters using cross-validation to maximize the Gini coefficient and ensure the model generalizes well to new customer cohorts. This data-driven approach allows us to establish credit lines for young professionals who have high disposable incomes but have been historically excluded from traditional credit card products.

At Zed, I will apply this exact methodology to develop core credit decisioning models. I will extract risk signals from sparse transaction data and write robust preprocessing pipelines that scale. I will configure model evaluation workflows to monitor feature importances, ensuring our credit limits align with borrower risk profiles. This analytical rigor will allow Zed to expand credit access safely, maintaining low default rates while growing our user base.

---

### 2. How do we represent raw transaction logs as vector embeddings for credit underwriting, and how would you build a pipeline using PySpark and Databricks?
Representing raw transaction logs as vector embeddings transforms messy text records into structured numerical vectors that capture spending context. A single transaction log contains unstructured text like merchant names and location codes. To capture this context, we can treat the transaction log as a sentence and run it through a text embedding model, such as a self-hosted **BERT** architecture or **Sentence-Transformers**. This generates a high-dimensional vector for each transaction, mapping similar merchants close together in the vector space. We can then aggregate these individual transaction vectors over a user's history, using time-decayed averaging or pooling, to create a single user behavioral embedding that summarizes their spending profile.

To build a scalable ingestion and processing pipeline, I would use **PySpark** on **Databricks**. First, raw transaction logs are extracted from our storage layers and cleaned. The PySpark job runs text preprocessing, tokenizing merchant names and filtering out noise. We load our embedding model in a distributed environment, using PySpark UDFs to generate vectors in parallel across worker nodes. These embeddings are stored in a centralized vector database or a data lake like Delta Lake, where they can be quickly retrieved by our credit models.

At Zed, this pipeline will allow us to convert millions of daily transaction logs into structured input features for our credit models. I will configure the Databricks pipeline to run as a scheduled **Apache Airflow** workflow, ensuring our customer embeddings are updated daily. By combining these behavioral vectors with traditional demographic variables, we can improve our model's risk profiling accuracy, enabling precise credit decisioning.

---

### 3. How can we model transaction histories as sequences using transformer architectures to forecast credit risk?
Modeling transaction histories as sequences allows us to capture the chronological path of a customer's spending, which provides deeper risk insights than simple aggregate metrics. Transactions are sequential events where the order of purchases matters: a user who suddenly starts cash-advancing at midnight after a series of luxury purchases represents a different risk profile than a user who pays bills in a regular cycle. We can model this by representing a user's transaction history as a sequence of transaction tokens, similar to words in a sentence, and passing them through a **Transformer** model. The self-attention mechanism calculates a weight score for every transaction relative to every other transaction, capturing sequential dependencies and behavioral shifts over time.

To implement this, we write our transformer layers using **PyTorch**, configuring multi-head attention blocks to process the transaction sequences. We represent each transaction using its embedding vector, which combines merchant category, transaction amount, and time elapsed since the previous transaction. The model is trained to forecast credit default risk, optimizing a binary cross-entropy loss function. This architecture allows the model to learn complex, long-range sequential behaviors that classical models like logistic regression or decision trees miss.

At Zed, I will experiment with and deploy transformer-based architectures in the underwriting process. I will write custom PyTorch datasets to format transaction sequences and set up distributed training pipelines on **AWS SageMaker**. By leveraging self-attention, we can identify early signs of credit stress or behavioral changes, allowing us to adjust credit limits proactively and protect our credit portfolio.

---

### 4. How do you design a real-time fraud detection pipeline combining rule-based heuristics and ML (XGBoost/LightGBM) using Kafka?
A real-time fraud detection pipeline must balance rapid response times with analytical accuracy, which we achieve by combining rule-based heuristics and machine learning models. When a transaction request arrives, it must be evaluated in under one hundred milliseconds. We structure this pipeline by running the transaction through a lightweight rule-based engine first, which applies simple checks (such as blocking transactions from blacklisted merchants or flagging duplicate attempts). In parallel, we route the transaction details through a message queue like **Apache Kafka** to our machine learning service, where an **XGBoost** or **LightGBM** model performs advanced anomaly detection.

The ML service is built using **FastAPI** to minimize web proxy overhead. When the transaction hits the API, the service retrieves the customer's historical profile from a **Redis** cache, performs feature engineering, and calculates the fraud probability score. If the ML model's probability score exceeds our threshold, the transaction is flagged for L2 verification. The results of both the rules and the ML model are merged in our decision engine to confirm or reject the transaction.

At Zed, I will design and deploy these real-time fraud models, ensuring they integrate with our banking APIs. I will write Python scripts to configure the Kafka consumers, set up Redis caching strategies to minimize database read latencies, and monitor model calibration in production. This architecture ensures that we block fraudulent transactions in real-time, maintaining high security without introducing latency for our users.

---

### 5. How do you build agentic workflows and tool-calling wrappers using LangGraph or CrewAI for automated credit audits?
Agentic workflows allow us to automate complex credit audit processes by wrapping language models in stateful graph structures that can call external tools. When a credit operations analyst needs to audit a complex business credit application, they must retrieve bank statements, verify business registration files, and run web searches on corporate backgrounds. We can automate this using **LangGraph** or **CrewAI** to build a multi-agent system. We define specialized agents, such as a document parsing agent, a verification agent, and an audit manager agent, which coordinate tasks by updating a shared state.

We write tool-calling wrappers in Python, allowing the agents to interact with our internal databases and external APIs. For example, a database tool uses parameterized SQL queries to pull transaction records, and a web search tool uses search APIs to retrieve company news. The agent receives the user's audit request, determines which tools to call, parses the tool outputs, and updates the graph state. If a verification check fails, a conditional edge routes the task to a human-in-the-loop checkpoint, pausing the graph and notifying the audit team.

At JPMorgan Chase, I developed multi-agent AI systems using LangGraph to automate research workflows, reducing manual effort by fifty percent. I will bring this expertise to Zed, building automated credit audit pipelines that process unstructured applications. By leveraging agentic orchestration, we can accelerate our underwriting turnaround, reduce manual operational overhead, and ensure that our credit audits are thorough and auditable.

---

### 6. When do we use a rule-based system vs. an ML model in underwriting, and how do we calibrate risk?
In credit underwriting, deciding whether to use a rule-based system or a machine learning model depends on the type of data, explainability requirements, and operational complexity. Rule-based systems are ideal for hard constraints that require clear compliance, such as verifying that the applicant meets the minimum age requirement or resides in an approved region. These rules are easy to audit and modify. However, rules are rigid and fail to capture complex, non-linear correlations across hundreds of variables. For complex risk profiling (such as evaluating a customer's income stability from messy transaction logs), we use machine learning models like **XGBoost** or neural networks.

To calibrate risk in our ML models, we must map our raw prediction probability scores to actual default rates. Machine learning models often produce uncalibrated probabilities, meaning a score of 0.1 does not represent a ten percent default rate. We use calibration techniques like Platt scaling or isotonic regression to align our model outputs with historical default frequencies. This calibration ensures that our credit pricing and risk provisioning calculations are accurate.

At Zed, I will establish the standards for when to apply rules versus models. I will build validation pipelines to calibrate our underwriting models, ensuring that our probability scores represent physical risk. I will partner with our risk operations team to write policy rules that sit alongside our ML models, ensuring our decisioning systems are both compliant and highly predictive.

---

### 7. How can deep learning and neural networks (PyTorch/TensorFlow) be applied to financial document parsing and risk classification?
Financial document parsing is a critical bottleneck in digital underwriting, as applicants submit diverse formats of bank statements, payslips, and tax documents. To automate this, we can apply deep learning models to perform optical character recognition (OCR), layout analysis, and text classification. We use neural network architectures like LayoutLM, which combine visual layout features with text embeddings, to identify and extract key fields (such as salary, total deposits, and transaction dates) from unstructured PDFs.

We build these extraction pipelines using **PyTorch** or **TensorFlow**. Once the document is parsed, the extracted text is processed using recurrent neural networks (RNNs) or transformer layers to identify potential fraud, such as altered transaction lines or inconsistent salary records. The deep learning model acts as a classification filter, assigning a document risk score before the data is sent to our core credit models.

At JPMorgan, I designed **BERT** and Transformer NLP solutions processing 180K+ compliance records monthly. At Zed, I will write PyTorch training scripts to train specialized extraction models on our historical document datasets. I will deploy these models in Docker containers behind FastAPI endpoints, ensuring that when a user uploads a document, we extract their income data in seconds, accelerating the onboarding experience.

---

### 8. How do you adapt credit risk modeling in a data-sparse environment (like the Philippines neobanking market) using transfer learning?
In emerging markets like the Philippines, we often operate in data-sparse environments where historical default records are limited. To build predictive credit models under these constraints, we can leverage **transfer learning** and alternative data features. Transfer learning allows us to train a base model on a large, related dataset (such as consumer credit data from a more mature market) and then fine-tune it on our small local dataset, allowing the model to learn general risk behaviors before adapting to local market conditions.

We also use pre-trained embedding models to extract feature signals from unstructured text. For example, we can load a pre-trained **BERT** model, pass our local merchant text descriptions, and generate transaction embeddings. This allows us to group similar spending behaviors without needing millions of historical transaction records. We combine these embeddings with simple demographic variables, training a supervised model like **LightGBM** with strict regularization parameters to prevent overfitting.

At Zed, I will use my experience in model adaptation to build predictive risk models for our new user segments. I will write Python scripts to set up fine-tuning pipelines, monitor generalization metrics, and design validation checks. This ensures our underwriting models remain accurate and reliable, even as we expand into new, data-sparse consumer markets.

---

### 9. How does your experience deploying BERT/Transformers for compliance record analysis at JPMorgan map to underwriting text inputs?
At **JPMorgan Chase**, I designed **BERT** and Transformer NLP solutions processing 180K+ compliance records monthly, cutting review cycles by 25% and saving 320 analyst-hours quarterly. This experience is directly applicable to credit underwriting, where we must extract risk signals from unstructured text inputs. A transaction log or an applicant's employer description contains text data that traditional credit models ignore. By using transformer models, we can extract semantic meaning from these text records.

We tokenize the transaction descriptions and feed them into a BERT model to generate contextual representations. These text features are then joined with our tabular credit variables. This allows the model to differentiate, for example, between a cash-advance transaction at a casino and a standard purchase at a grocery store, even if the raw merchant codes are similar.

At Zed, I will build similar text processing pipelines to analyze applicant data. I will write PyTorch scripts to fine-tune transformer models on our local text datasets, wrap the models in Docker containers, and integrate them with our FastAPI inference services. This NLP capability will allow us to extract predictive risk signals from unstructured documents, improving our underwriting accuracy.

---

### 10. How do you perform parameter-efficient fine-tuning (LoRA/QLoRA) on AWS SageMaker for financial domain-specific tasks?
Fine-tuning large language models for financial tasks requires adjusting models to capture domain terminology and formatting rules. However, full fine-tuning is compute-intensive. To optimize this process, we use Parameter-Efficient Fine-Tuning (PEFT) via **LoRA** (Low-Rank Adaptation) or **QLoRA** (Quantized LoRA), which freezes the base model weights and trains a small set of adapter layers inserted into the attention blocks, reducing GPU memory requirements.

To implement this on **AWS SageMaker**, we write a Python training script that loads the base model in 4-bit precision using the bitsandbytes library. We configure the LoRA adapters using Hugging Face's PEFT library, targeting the projection layers. We upload our formatted financial dataset to an S3 bucket and launch a SageMaker training job using PySpark and Databricks to manage data scaling. SageMaker spins up a GPU instance, runs the training script, and saves the fine-tuned adapter weights to our model registry.

I have operationalized Databricks and Airflow workflows with LoRA/QLoRA fine-tuning on AWS SageMaker. At Zed, this training pipeline will allow us to specialize foundation models for risk classification and document processing. I will configure the SageMaker container deployment, monitor the validation loss curves in **MLflow**, and deploy the fine-tuned adapters behind our underwriting APIs.

---

### 11. Describe your approach to setting up an MLOps pipeline using MLflow, Docker, and FastAPI for real-time risk inference.
An MLOps pipeline for real-time risk inference must ensure that models are reproducible, testable, and easy to deploy. To achieve this, we containerize our inference services using **Docker** and track our model artifacts and metrics in **MLflow**. The inference API is built using **FastAPI** to handle high-throughput, non-blocking requests, routing incoming customer details to our model runner.

When a developer updates a model, our CI/CD pipeline triggers. The pipeline builds the Docker image containing the model code, retrieves the trained model weights from the MLflow model registry, and runs automated unit tests. These tests verify schema validation, check for null inputs, and run baseline predictions. If all tests pass, the container is deployed to our staging environment for user acceptance testing, before rolling out to production.

At JPMorgan, I built MLOps infrastructure with MLflow, Docker, and FastAPI, cutting deployment cycles from 5 days to under 24 hours. At Zed, I will establish this deployment framework. I will write the Dockerfiles, configure the FastAPI routers, and set up the MLflow registry integration. This automation ensures we deploy new underwriting and fraud models safely and quickly.

---

### 12. How do you monitor production models for concept drift and statistical distribution changes in a dynamic credit environment?
Model monitoring is critical in credit underwriting because customer demographics and macroeconomic conditions change over time, leading to concept drift and performance degradation. If the distribution of our model inputs (like transaction frequency or average balances) shifts, or if the relationship between our predictions and actual default rates changes, the model will lose accuracy. To detect this, we establish a monitoring system that tracks data drift and concept drift in production.

We write automated Python scripts to compare the statistical distributions of our production features against our baseline training datasets, calculating metrics like the Population Stability Index (PSI) and the Wasserstein distance. If the PSI for a key feature exceeds 0.2, the script triggers an alert. We also monitor performance metrics (like the F1 score or the Gini coefficient) in real-time by joining our model predictions with actual repayment data.

At Zed, I will build these automated monitoring pipelines. I will configure metric aggregations in **BigQuery**, set up CloudWatch dashboard alerts, and write fallback procedures. If a model starts to degrade, our monitoring system will flag the drift, allowing us to retrain the model on recent data and maintain stable underwriting performance.

---

### 13. How do you evaluate the reliability and faithfulness of generative AI agent outputs using frameworks like RAGAS or TruLens?
Evaluating generative AI agents is challenging because natural language outputs cannot be validated using simple accuracy metrics. To ensure our underwriting agents are reliable, we use evaluation frameworks like **RAGAS** or **TruLens**, which implement LLM-as-a-judge scoring. These frameworks evaluate three key dimensions of the agentic generation process: faithfulness, answer relevance, and context recall.

Faithfulness measures if the agent's output is derived entirely from the retrieved context documents, ensuring the model does not hallucinate facts. Answer relevance measures if the output directly addresses the user's query, and context recall measures if the retrieval step gathered all the information required. We write automated scripts that pass our test queries, retrieved context, and generated answers to these scoring engines, producing quantitative quality metrics.

At JPMorgan, I utilized RAGAS and TruLens evaluation pipelines, maintaining 92%+ agent accuracy across our research assistants. At Zed, I will establish this evaluation framework to validate our automated underwriting agents. I will write test cases, run evaluation scripts during our CI/CD builds, and log these scores in MLflow, ensuring our agents generate accurate financial summaries.

---

### 14. Describe your project Ask-Aria and how hybrid search (BM25 + Dense) can optimize customer document retrieval.
For my project **Ask-Aria**, I built a production-grade generative AI knowledge assistant using LLaMA 3, Pinecone, and Groq. The core challenge was retrieving relevant context passages from unstructured PDF, DOCX, and TXT files. To optimize retrieval accuracy, I designed a **hybrid search** pipeline that combined keyword-based lexical search with semantic vector search.

Lexical search was implemented using **BM25**, which matches exact terms like serial numbers, tax IDs, or specific dates. Semantic search was implemented using dense vector embeddings stored in **Pinecone**, which captures contextual meaning. When a query occurred, both searches ran in parallel, and their scores were merged using Reciprocal Rank Fusion (RRF). This hybrid approach improved our retrieval hit rate from 55.8% to 70.0%.

This hybrid search architecture is highly applicable to Zed's document parsing workflows. When customers upload financial documents, we can use BM25 to locate specific keywords and dense embeddings to extract overall context. I will write Python scripts to implement this retrieval pipeline, ensuring our models extract accurate financial facts from customer uploads.

---

### 15. How do you extract predictive features from sparse, heterogeneous transaction logs?
Extracting predictive signals from messy, sparse transaction logs requires a combination of rule-based aggregations and embedding models. Raw transaction text often lacks structure. To clean this data, we write Python and SQL pipelines that perform NLP cleaning, removing random character codes, dates, and locations from merchant descriptions, leaving only the clean merchant name.

Once cleaned, we perform feature engineering across different time windows. We calculate rolling aggregations, such as the total amount spent on utilities over the last thirty days, the frequency of cash withdrawals, and the standard deviation of daily spending. We also pass the merchant names through an embedding model, generating high-dimensional vectors that capture semantic intent and grouping similar spending behaviors.

I have built feature engineering pipelines using **Scikit-learn** and **PySpark** across twelve business sectors, reducing model onboarding times by half. At Zed, I will write scalable SQL and PySpark transformations to process raw transaction tables. This feature engineering will convert unstructured transaction records into high-quality, predictive variables for our credit and fraud models.

---

### 16. How do you ensure that ML-driven credit underwriting models do not perpetuate bias against specific demographics?
Enforcing fairness in machine learning credit models is both a regulatory requirement and an ethical responsibility. Machine learning models can learn to perpetuate historical bias if the training data contains disparities. To prevent this, we must audit our models for bias, ensuring they do not use protected attributes (like age, gender, or region) or proxy variables that correlate with these demographics.

We use Python libraries like Fairlearn or AIF360 to calculate fairness metrics, measuring disparate impact and equalized odds. Disparate impact compares the selection rate of different demographic groups, and equalized odds checks if the model's error rates are consistent across groups. If the model exhibits bias, we apply mitigation techniques, such as adversarial debiasing during training or adjusting decision thresholds post-prediction.

At Zed, I will establish our model audit protocols. I will build validation checks in our pipeline to test feature distributions and calculate fairness metrics for every model candidate. By auditing our underwriting and credit decisioning workflows, we ensure that our models are fair, compliant, and base credit limits entirely on financial risk.

---

### 17. How do you use unsupervised anomaly detection for credit limit management?
Unsupervised anomaly detection allows us to identify unusual changes in customer spending behavior that could indicate credit risk or fraud. Unlike supervised models that require historical target labels, unsupervised models learn the baseline distribution of normal behavior and flag any record that deviates from this distribution. We use this to adjust credit limits proactively.

We train models like Isolation Forests or One-Class SVMs on customer features (such as daily transaction counts, average purchase amounts, and location variances) using **Scikit-learn**. The model assigns an anomaly score to each user profile. If a customer's score spikes—for example, due to sudden, high-frequency cash withdrawals—the system flags the account, allowing risk operations to review the credit limit.

I have delivered predictive risk-estimation models that isolate transaction anomalies, accelerating risk review decisions. At Zed, I will build these unsupervised monitoring pipelines, integrating them with our databases. This proactive risk detection will allow us to adjust credit limits dynamically, reducing default rates while maintaining a smooth user experience.

---

### 18. How do you address extreme class imbalance (e.g., fraud rate < 0.1%) when training XGBoost models?
Fraud detection datasets are highly imbalanced, as legitimate transactions outnumber fraudulent ones. If we train an **XGBoost** model on this imbalanced data without adjustments, the model will optimize for accuracy by predicting the majority class (non-fraud) for all records, failing to detect actual fraud. To address this, we apply balance techniques during data prep and model training.

First, during training, we configure the XGBoost hyper-parameter `scale_pos_weight` to scale the gradient updates of the minority class, forcing the model to focus on fraud samples. We also use evaluation metrics like Precision-Recall AUC (PR-AUC) or the F1 score instead of standard accuracy to measure model performance. If needed, we apply SMOTE (Synthetic Minority Over-sampling Technique) using imbalanced-learn to balance the classes.

I have tuned classification models to resolve production prediction discrepancies, improving F1 scores and optimizing performance. At Zed, I will write the training configurations for our fraud models, select the correct evaluation metrics, and tune the classification thresholds to minimize false negatives, protecting the neobank from fraud losses.

---

### 19. How do you design historical backtests to validate changes in credit underwriting models before production rollout?
Before deploying a new credit underwriting model to production, we must validate its performance using historical backtesting. Backtesting simulates how the new model would have performed on past credit cohorts, comparing its predictions against actual historical outcomes. This step verifies that the new model improves risk classification without causing operational regression.

To design a backtest, we extract historical customer data from our data warehouse in **BigQuery**. We apply the new model's preprocessing rules and run predictions on these historical records, calculating credit default and delinquency rates. We compare these results against the actual performance of our legacy model, tracking metrics like the Gini coefficient and default frequencies across risk tiers.

At KPMG, I designed risk-estimation models and backtesting frameworks to validate data migrations and risk decisions. At Zed, I will establish this backtesting protocol, ensuring that every underwriting candidate is validated against historical data before deployment. This validation minimizes risk and ensures our models deliver the expected business results.

---

### 20. How does your experience at KPMG optimizing SQL pipelines across 85K+ records map to Zed's data engineering needs?
At **KPMG India**, I accelerated forensic audit extraction on **BigQuery** from multi-day batch jobs to under 4 hours by optimizing SQL pipelines across 85K+ corporate records, cutting infrastructure compute costs by an estimated 35%. This experience is directly applicable to Zed's data engineering needs, where we must clean, aggregate, and join transaction records from various databases.

To optimize SQL queries, I analyze execution plans, looking for expensive joins, table scans, and Cartesian products. I structure queries using Common Table Expressions (CTEs), implement partition keys, and replace legacy subqueries with window functions. This optimization reduces the compute load on our data warehouses, cutting cloud hosting costs and ensuring dashboards refresh quickly.

At Zed, I will apply this SQL tuning expertise to our data warehousing and ETL pipelines. I will write clean, scalable SQL transformations to consolidate transaction data from ticketing systems and databases into centralized data warehouses, ensuring our support and operations teams have fast, reliable access to operational KPIs.

---

### 21. How do you use SHAP or LIME to explain model-driven credit decisions to credit operations or regulatory auditors?
Explainable AI (XAI) is critical in credit underwriting to ensure our models are auditable and comply with fair lending regulations. When our **XGBoost** model rejects a credit application, we must explain the exact reasons for the decision. We can use SHAP (SHapley Additive exPlanations) or LIME (Local Interpretable Model-agnostic Explanations) to calculate the contribution of each feature to the model's prediction.

SHAP values are calculated using cooperative game theory, assigning a numeric value to each feature that represents how much it shifted the prediction away from the baseline average. For example, a high SHAP value for "late payment counts" shows this feature was the primary driver of the rejection. We generate these explanation metrics in Python and save them to our databases alongside the model predictions.

At Zed, I will integrate SHAP and LIME into our decisioning systems. I will write Python scripts to calculate and save explanation values for every underwriting run, displaying them on our internal dashboards. This transparency allows credit operations to explain decisions to customers and regulatory auditors, ensuring compliance.

---

### 22. How do you balance launching rapid credit prototypes vs. building robust, scalable ML pipelines?
At a startup, balancing speed and quality is a constant challenge. When launching new credit products, we must prototype quickly to validate business value and collect customer feedback. However, we cannot let messy prototype code compromise our production systems. I address this by using a modular, phased development approach.

For the prototype phase, I build lightweight pipelines using Python notebooks and simple rule-based models, utilizing existing database views to deliver dashboards quickly. Once the prototype validates the business need and we collect user feedback, I refactor the code into a scalable ETL pipeline, writing modular PySpark transformations, adding data quality monitoring, and setting up automated UAT scripts.

I have automated data pipelines and dashboarding workflows, saving labor hours while maintaining high data quality. At Zed, I will apply this phased engineering approach, helping the team prototype credit models quickly to support business initiatives while building robust, scalable data architectures for our production systems.

---

### 23. How do you collaborate with engineering teams to integrate ML outputs into real-time decision engines?
Integrating machine learning models into real-time decision engines requires collaboration between data scientists and software engineers. To ensure a smooth integration, we must define clear data contracts and API specifications, ensuring that our model inputs and outputs are formatted using standard JSON schemas.

I build our model services as REST APIs using **FastAPI**, wrapping the logic in Docker containers. I write Pydantic schemas in Python to enforce input data types, and run integration tests using Postman. The software engineering team can call our model endpoints directly, passing user details and receiving the risk score payload, which is then processed by the core decision engine.

I have partnered with DevOps and engineering teams to deploy ML models, reducing deployment cycles. At Zed, I will collaborate with our backend developers to integrate our credit scoring and fraud detection models into our real-time transaction processing layers, ensuring our ML services are secure, fast, and reliable.

---

### 24. How would you set the technical standard for ML practices and help scale the data team at Zed?
Setting the technical standard for machine learning requires establishing best practices for code quality, reproducibility, and model validation. As a senior ML voice, I will advocate for writing modular, testable Python code, enforcing linting checks, and requiring peer reviews for all model modifications. I will configure **MLflow** to track all training parameters and metrics, ensuring our experiments are fully reproducible.

I will also establish automated evaluation pipelines using tools like RAGAS and TruLens to validate generative AI agents, and write data drift checks to monitor model performance in production. To help scale the data team, I will compile technical guides in Confluence and mentor junior analysts, organizing workshops on SQL tuning, PyTorch modeling, and MLOps workflows.

I have mentored cross-functional squads and optimized sprint velocity in my previous roles. At Zed, I will leverage this leadership experience to build a collaborative, high-performing data science culture. By setting high standards and sharing technical knowledge, we ensure our team is capable of building stable, production-grade ML systems that support Zed's growth.

---

### 25. How do you use unsupervised clustering algorithms to identify new, evolving fraud patterns in transaction streams?
Supervised fraud models excel at detecting known fraud patterns that exist in our historical training data. However, fraudsters continuously adapt, creating new techniques that supervised models can miss. To detect these evolving fraud vectors, we use unsupervised clustering algorithms (such as K-Means or DBSCAN) to group transaction data and identify anomalous clusters.

We write Python scripts to extract behavioral features (such as purchase locations, transaction amounts, and merchant categories) from our transaction streams, and run clustering models using **Scikit-learn**. The algorithm groups similar transaction behaviors together. If a new cluster forms that deviates from normal user clusters—for example, a group of accounts showing low-amount transactions at midnight—it indicates a new fraud vector.

I have tuned classification and clustering models to identify anomalies and resolve prediction discrepancies. At Zed, I will establish these clustering pipelines in our data warehouse. By monitoring cluster distributions, we can detect new fraud patterns early, allowing our risk operations team to write preventative rules before the fraud impacts our portfolio.

---

### 26. How do you design database integrations for high-throughput transactional scoring without causing latency spikes?
Designing database integrations for real-time transactional scoring requires maximizing throughput while maintaining low query latency. When a transaction request hits our FastAPI service, querying our primary database directly for customer history would create a performance bottleneck. To prevent latency spikes, we implement a caching layer using **Redis**.

We configure our ETL pipelines to pre-calculate customer features (such as average balances and rolling transaction counts) in **BigQuery** or Snowflake, and write these aggregated variables to our Redis cache. When a transaction occurs, our FastAPI service queries Redis, which returns the features in milliseconds. The model calculates the risk score and writes the prediction log asynchronously to our PostgreSQL database, preventing lock contention.

At Dell and JPMorgan, I optimized database integrations and automated query workflows, reducing data latency. At Zed, I will design this caching and database integration architecture, ensuring our real-time credit decisioning and fraud detection models run quickly and reliably under high transaction volumes.

---

### 27. Describe how you built customer segmentation workflows at Dell and how it applies to account management at Zed.
At **Dell Technologies**, I designed customer segmentation workflows using Python, **Scikit-learn**, and Databricks, generating behavioral datasets supporting 15+ internal analytics use cases and targeted business reporting initiatives. I applied K-Means clustering to segment our user base based on purchase frequency, order values, and product categories, providing our marketing and product teams with detailed user profiles.

This segmentation methodology is directly applicable to credit account management at Zed. We can segment our cardholders based on their utilization rates, spending behaviors, and payment histories. This segmentation allows us to customize our account management policies, such as automatically offering credit limit increases to high-value, low-risk segments, or implementing early-intervention alerts for higher-risk cohorts.

I will write the clustering scripts and ETL transformations to build these segmentation profiles, saving the outputs to our data warehouses. By translating customer behavior into structured segments, we can optimize our credit limits, design targeted marketing campaigns, and improve overall customer retention at Zed.

---

### 28. Compare transformer-based representations and classical TF-IDF for processing unstructured financial documents.
Processing unstructured financial documents (such as bank statements or tax forms) requires converting text records into numerical features that machine learning models can understand. We can achieve this using either classical bag-of-words methods like TF-IDF or transformer-based embedding models like **BERT**.

TF-IDF (Term Frequency-Inverse Document Frequency) measures the frequency of a word in a document relative to its frequency across all documents. It is computationally lightweight and works well for classifying documents based on specific keywords. However, TF-IDF ignores word order and semantic meaning: it cannot identify that "salary payment" and "monthly deposit" represent similar concepts because it only looks for exact keyword matches.

Transformer-based models like BERT process text in parallel, using self-attention to capture context and semantic meaning. This allows the model to map similar financial concepts to close vectors in a high-dimensional space, even if the phrasing is different. At Zed, I will use transformer embeddings to process messy financial text, ensuring our models extract accurate risk signals from unstructured documents.

---

### 29. How do you design randomized controlled experiments to test new credit limit policies in production?
When testing a new credit limit policy or a new underwriting model, we must design a randomized controlled experiment (or A/B test) to evaluate its impact on credit default rates and user spending before rolling it out to our entire customer base. This verification step ensures that our credit policy modifications are statistically valid and do not cause default spikes.

To design the experiment, we randomly split our target customer segment into two groups: the control group (which remains on the legacy credit policy) and the treatment group (which receives the new credit limit policy). We ensure that both groups have similar demographic and risk profiles. We run the experiment over a defined period (such as three months), tracking metrics like the average balance increase, utilization rates, and default frequencies.

I have configured data validation workflows and statistical testing setups in my previous analytics roles. At Zed, I will partner with our risk team to design and validate these credit experiments. I will write SQL and Python scripts to run hypothesis testing, evaluate p-values, and confirm that our new credit policies improve revenue while keeping default risks low.

---

### 30. How do you calibrate ML model probabilities to match credit risk provisioning standards?
In credit risk modeling, predicting the probability of default (PD) is only the first step. For financial planning and regulatory compliance, we must ensure that these predicted probabilities are calibrated, meaning that if our model assigns a PD of five percent to a cohort of cardholders, approximately five percent of those cardholders should default over the defined time window.

Uncalibrated machine learning models (such as deep neural networks or **XGBoost** models) often produce biased probabilities that are pushed toward zero or one. To calibrate these outputs, we use post-processing techniques like Platt scaling (which fits a logistic regression model on the predictions) or isotonic regression (a non-parametric method). We validate the calibration by plotting calibration curves and calculating the Brier score.

At Zed, I will build automated model calibration pipelines. I will write Python validation scripts to evaluate our model outputs against historical default records, applying calibration algorithms to ensure our PD metrics are accurate. This statistical calibration ensures that our credit risk provisioning is compliant and that our credit pricing models are built on mathematically sound risk metrics.

---

## Part 2: Integration with Workspace

We register our new preparation guide in the Nextra navigation configuration.

### File Modifications

#### 1. Add to Navigation Sidebar
We register the guide in [content/_meta.js](file:///f:/rivian%20vaishnavi/preprationstuff/content/_meta.js).

```diff
 export default {
   index: 'Docs Home',
   'qualcomm-prep-material': 'Qualcomm NPU / Embedded Platform Prep',
   'natera-ai-solutions-prep': 'Natera AI Solutions Prep',
   'sirisha-genai-prep': 'Sirisha GenAI Prep',
   'dineesha-support-prep': 'Dineesha Support Prep',
   'manohar-bi-prep': 'Manohar BI Prep',
+  'prathyush-zed-prep': 'Prathyush Zed Prep',
   'torc-prep-guide': 'Torc Prep Guide (Device Drivers)',
   'vaishnavi-torc-mcu-applications-prep': 'Vaishnavi Torc MCU Applications Prep',
```

#### 2. Link on Main Index Page
We link the new document on [content/index.mdx](file:///f:/rivian%20vaishnavi/preprationstuff/content/index.mdx).

```diff
 # Preparation Stuff
 
 This site hosts Markdown documents. Add new files under `content/` and they will appear in the sidebar automatically.
 
 - [Natera Head of AI Solutions Prep Guide](/docs/natera-ai-solutions-prep)
 - [Sirisha GenAI Prep Guide](/docs/sirisha-genai-prep)
 - [Dineesha Support Prep Guide](/docs/dineesha-support-prep)
 - [Manohar BI Prep Guide](/docs/manohar-bi-prep)
+- [Prathyush Zed Prep Guide](/docs/prathyush-zed-prep)
 - [Torc Prep Guide (Device Drivers)](/docs/torc-prep-guide)
```
