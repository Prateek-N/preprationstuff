# -*- coding: utf-8 -*-
"""
Janaki Ashok Kumar - QA Automation 14-Day Roadmap (Days 10 - 14)
Covers:
Day 10: Event-Driven Architecture, Messaging & Microservices Testing (Kafka, Awaitility)
Day 11: CI/CD Pipeline Integration with Jenkins & Azure DevOps
Day 12: Dockerization, Selenium Grid & Cross-Browser Cloud Execution
Day 13: Non-Functional Testing, Performance Telemetry & Agile Defect Management
Day 14: Master End-to-End Mock Interview, Resume Defense & Live Coding Drills
"""

days_part3 = [
    # =========================================================================
    # DAY 10: Event-Driven Architecture, Messaging & Microservices Testing
    # =========================================================================
    {
        "day": 10,
        "title": "Day 10: Event-Driven Architecture, Messaging & Microservices Testing (Kafka & Awaitility)",
        "theme": "Asynchronous Event Streams, Kafka Consumers & Deterministic Polling",
        "domain_focus": "Asynchronous Banking Notifications & Claims Orchestration",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: Core Architectural Theory",
                "topic": "Event-Driven Microservices, Apache Kafka Concepts & Eventual Consistency",
                "content": """### Event-Driven Architecture (EDA) Mechanics in Financial Systems:
Modern enterprise systems at **PNC Bank** and **Liberty Mutual** decouple synchronous REST requests from heavy backend processing using event brokers like **Apache Kafka** and **RabbitMQ**.
1. **Core Kafka Primitives:**
   - **Topic:** Partitioned, immutable log of events (e.g., `pnc.transfers.settlement.v1`).
   - **Producer:** Microservice publishing events when a state changes (e.g., when a user initiates a wire transfer).
   - **Consumer & Consumer Groups:** Downstream microservices (e.g., Fraud Detection, General Ledger, Customer Notification) reading from partitions independently.
   - **Offset Management:** Tracking read positions to ensure at-least-once or exactly-once message delivery.
2. **The Challenge of Eventual Consistency in QA:**
   Because messaging is asynchronous, test assertions cannot rely on instantaneous synchronous responses. Using `Thread.sleep()` is anti-pattern; tests must use **Awaitility** to dynamically poll message brokers until conditions are met."""
            },
            {
                "hour": 2,
                "label": "Hour 2: Production Code Lab",
                "topic": "Automated Kafka Event Verification with Java & Awaitility",
                "content": """Below is the automated Kafka consumer verification utility used in our Java test framework:

```java
package com.pnc.qa.messaging;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.awaitility.Awaitility;

import java.time.Duration;
import java.util.*;
import java.util.concurrent.atomic.AtomicReference;

public class KafkaTestVerifier {

    private static final String BOOTSTRAP_SERVERS = "kafka.pnc.internal:9092";

    public static String waitForMessageWithCorrelationId(String topicName, String correlationId, int timeoutSeconds) {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "qa-verifier-group-" + UUID.randomUUID());
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest");

        AtomicReference<String> matchedMessage = new AtomicReference<>(null);

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            consumer.subscribe(Collections.singletonList(topicName));

            // Use Awaitility for deterministic, asynchronous polling
            Awaitility.await()
                    .atMost(Duration.ofSeconds(timeoutSeconds))
                    .pollInterval(Duration.ofMillis(500))
                    .until(() -> {
                        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(200));
                        for (ConsumerRecord<String, String> record : records) {
                            if (record.value() != null && record.value().contains(correlationId)) {
                                matchedMessage.set(record.value());
                                return true;
                            }
                        }
                        return false;
                    });
        }

        return matchedMessage.get();
    }
}
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Enterprise Edge Cases & Flaky Test Elimination",
                "topic": "Idempotency Testing, Poison Pill Messages & Dead Letter Queues (DLQ)",
                "content": """### Critical Edge Cases in Asynchronous Testing:
1. **Idempotency Verification:** In financial transactions, network retries must never cause duplicate wire transfers. In an automated test, replay the identical Kafka event or POST request twice with the same `Idempotency-Key` and assert that the target account is debited exactly once, with the second request returning the cached original response.
2. **Dead Letter Queue (DLQ) Verification:** When a malformed event or corrupted JSON payload is sent to a topic, verify that the consumer microservice does not crash, but routes the poison-pill message to `pnc.transfers.dlq` while alerting monitoring systems.
3. **Consumer Rebalance Timeouts:** Ensure test consumer groups use unique random IDs (`"qa-group-" + UUID.randomUUID()`) to avoid triggering partition rebalancing in active environments."""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "Testing Asynchronous Event-Driven Microservices with Kafka & Awaitility",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Diagnosing Out-of-Order Kafka Processing at Liberty Mutual",
                "content": """**Situation:** At **Liberty Mutual**, during policy cancellation and reinstatement workflows, our claims settlement microservice occasionally processed claims on policies that had already been canceled. The defect occurred intermittently under high concurrent traffic, making it impossible to reproduce manually.

**Task:** As QA Automation Engineer, I took ownership of designing an automated test suite capable of simulating concurrent message streams across our **Apache Kafka** messaging backbone to isolate the root cause.

**Action:** I built a multi-threaded test harness in Java that simultaneously published policy cancellation events and subsequent claim submissions to our Kafka topics. I integrated **Awaitility** to monitor the state transitions across our relational Oracle database and downstream policy status endpoints. The automated tests quickly reproduced the defect and revealed the root cause: the cancellation and claim events were assigned different Kafka partition keys, causing two separate consumer worker threads to process them out of chronological order.

**Result:** Working alongside backend developers, we refactored the message producer to use the `policy_number` as the strict partition key, guaranteeing in-order sequential processing per policy. The automated test suite was integrated into our **Jenkins** regression pipeline, permanently preventing claims processing errors on canceled policies across **25,000+ policy records**."""
            }
        ],
        "master_qa": {
            "question": "How do you test asynchronous, event-driven microservices using Apache Kafka and Awaitility in an automated testing suite?",
            "answer": """Testing asynchronous, event-driven microservices powered by **Apache Kafka** or **RabbitMQ** introduces fundamentally different verification paradigms compared to traditional synchronous REST APIs. In synchronous testing, a client issues an HTTP request and immediately receives the complete final state in the response. In an event-driven architecture—such as the banking transfer and notification pipelines at **PNC Bank** or insurance claims orchestration at **Liberty Mutual**—an HTTP request simply returns an immediate `202 Accepted` status code. The actual business workflow (fraud scoring, balance ledger updates, and notification dispatches) executes asynchronously across decoupled microservices communicating through Kafka topics.

To test these asynchronous workflows with high fidelity and zero flakiness, relying on hardcoded static pauses (`Thread.sleep()`) is an anti-pattern that leads to unstable builds and inflated pipeline execution times. The enterprise-grade testing strategy pairs custom Kafka consumer utilities with **Awaitility**, a domain-specific Java library for synchronizing asynchronous operations.

In our framework, I construct a dedicated messaging test harness utilizing the official `KafkaConsumer` client. When a test initiates a business event—such as submitting a $150,000 corporate wire transfer via **REST Assured** or **Selenium WebDriver**—the test captures the unique `correlationId` or `transactionReferenceId` generated in the request headers. The test then subscribes a test consumer to the downstream Kafka event topic (e.g., `pnc.banking.transfers.settled`). To prevent the test from reading stale messages from previous executions or interfering with active consumer groups, the test dynamically assigns a unique, temporary consumer group ID using `UUID.randomUUID()` and sets `ConsumerConfig.AUTO_OFFSET_RESET_CONFIG` to `"latest"`.

We then wrap the message polling logic inside an **Awaitility** assertion block: `Awaitility.await().atMost(Duration.ofSeconds(10)).pollInterval(Duration.ofMillis(500)).until(() -> pollAndMatch(correlationId))`. Awaitility continuously polls the Kafka topic in non-blocking increments, returning the target event payload the millisecond it arrives. Once captured, the test deserializes the message into a strongly typed POJO, asserting that the payload schema complies with enterprise specifications, that the transaction amount and currency match the original request, and that the calculated settlement timestamp is accurate.

Furthermore, we test critical edge conditions including **idempotency** (replaying the identical Kafka message to ensure downstream consumers do not duplicate financial ledger debits) and **Dead Letter Queue (DLQ)** behavior (publishing deliberately malformed payloads to verify that consumer microservices gracefully isolate bad data without halting partition consumption). This comprehensive approach guarantees end-to-end reliability across asynchronous, distributed microservice ecosystems."""
        }
    },

    # =========================================================================
    # DAY 11: CI/CD Pipeline Integration with Jenkins & Azure DevOps
    # =========================================================================
    {
        "day": 11,
        "title": "Day 11: CI/CD Pipeline Integration with Jenkins & Azure DevOps",
        "theme": "Declarative Pipelines, Parallel Stages & Automated Quality Gates",
        "domain_focus": "Automating 200+ Daily Tests & Multi-Stage Release Gating",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: Core Architectural Theory",
                "topic": "Continuous Integration in Enterprise QA & Quality Gate Architecture",
                "content": """### CI/CD in Modern Enterprise QA:
Automated tests provide zero value if they run only on local developer laptops. They must execute continuously on every Git commit, pull request, and release candidate.
- **Commit Trigger (Smoke Gate):** Runs in under 10 minutes on PR submission. Executes unit tests and fast API smoke tests. Blocks merge if any test fails.
- **Nightly Regression Pipeline:** Executes full regression suite (200+ UI, API, and DB tests) across parallel worker nodes. Generates visual **Allure** reports and sends Slack/Teams notifications.
- **Release Gating:** Quality gates enforce minimum metrics before deployment to staging or production (e.g., 100% pass rate on P1 regression tests, zero high-severity open defects in **Jira/Xray**)."""
            },
            {
                "hour": 2,
                "label": "Hour 2: Production Code Lab",
                "topic": "Production Declarative `Jenkinsfile` with Parallel Multi-Browser Execution",
                "content": """Below is the production-grade declarative `Jenkinsfile` managing parallel test stages and Allure reporting:

```groovy
pipeline {
    agent {
        docker {
            image 'maven:3.9.6-eclipse-temurin-17'
            args '-v /var/run/docker.sock:/var/run/docker.sock -v $HOME/.m2:/root/.m2'
        }
    }

    tools {
        maven 'Maven-3.9.6'
        jdk 'JDK-17'
    }

    environment {
        ALLURE_RESULTS_DIR = 'target/allure-results'
        APP_ENV = 'staging'
    }

    stages {
        stage('Checkout & Compile') {
            steps {
                git branch: 'main', credentialsId: 'github-enterprise-creds', url: 'https://github.com/pnc/banking-automation.git'
                sh 'mvn clean compile test-compile'
            }
        }

        stage('API Smoke Regression') {
            steps {
                sh 'mvn test -DsuiteFile=src/test/resources/suites/testng-api-smoke.xml -Denv=${APP_ENV}'
            }
        }

        stage('Parallel UI Regression Execution') {
            parallel {
                stage('UI Chrome Headless') {
                    steps {
                        sh 'mvn test -DsuiteFile=src/test/resources/suites/testng-chrome.xml -Dbrowser=chrome -Dheadless=true'
                    }
                }
                stage('UI Firefox Headless') {
                    steps {
                        sh 'mvn test -DsuiteFile=src/test/resources/suites/testng-firefox.xml -Dbrowser=firefox -Dheadless=true'
                    }
                }
                stage('Database Reconciliation Tests') {
                    steps {
                        sh 'mvn test -DsuiteFile=src/test/resources/suites/testng-db-reconciliation.xml'
                    }
                }
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'target/allure-results']]
            junit 'target/surefire-reports/*.xml'
        }
        failure {
            slackSend channel: '#qa-automation-alerts',
                      color: '#FF0000',
                      message: "FAILED: Build ${env.BUILD_NUMBER} on ${env.JOB_NAME} failed! Report: ${env.BUILD_URL}allure"
        }
        success {
            slackSend channel: '#qa-automation-alerts',
                      color: '#00FF00',
                      message: "SUCCESS: Build ${env.BUILD_NUMBER} on ${env.JOB_NAME} passed successfully! All 220 tests verified."
        }
    }
}
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Enterprise Edge Cases & Flaky Test Elimination",
                "topic": "Azure DevOps `azure-pipelines.yml` & Pipeline Optimization",
                "content": """### Azure DevOps Multi-Stage Pipeline Patterns:
At **Molina Healthcare**, we executed 350 test cases via **Azure DevOps Pipelines**:
- **Caching Dependencies:** Use `Cache@2` task to cache Maven `.m2` repository, shaving 4 minutes off build initialization.
- **Publishing Test Results:** Use `PublishTestResults@2` to integrate JUnit XML directly into the Azure DevOps Test tab for native pass/fail analytics.
- **Dynamic Artifact Publishing:** Archive failed test screenshots and Playwright trace archives (`trace.zip`) as build artifacts for immediate post-mortem download."""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "Architecting a Production-Grade CI/CD Automation Pipeline",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Optimizing Jenkins Regression Pipelines at Liberty Mutual (200+ Daily Tests)",
                "content": """**Situation:** At **Liberty Mutual**, our nightly regression suite running in **Jenkins** executed 200+ automated tests sequentially on a single bare-metal build agent. The build took over 6 hours, frequently collided with morning code freezes, and when tests failed, testers had to search through 10,000 lines of raw console logs to identify the failed scenarios.

**Task:** My objective was to redesign our CI/CD pipeline architecture to reduce execution time to under 2 hours, establish parallel execution, and automate rich visual reporting.

**Action:** I authored a brand new declarative **Jenkinsfile** leveraging a Docker-in-Docker agent architecture. I partitioned our monolithic test suite into three parallel stages: API Smoke, UI Chrome Headless, and UI Firefox Headless. I configured **Maven Surefire** to run 4 concurrent threads per container, and integrated the **Allure Jenkins Plugin** to automatically compile interactive test reports complete with step-by-step logs, failure screenshots, and test execution duration metrics. I also integrated an automated **Slack** notification hook alerting the on-call QA engineer with direct links to failed test artifacts.

**Result:** We compressed the total pipeline execution time from **6 hours down to 1.5 hours** (a 75% reduction), provided immediate quality feedback to developers before morning standup, and supported continuous daily releases across 14 release iterations."""
            }
        ],
        "master_qa": {
            "question": "Explain how you architect and maintain a production-grade CI/CD automation pipeline in Jenkins or Azure DevOps with parallel execution and automated reporting.",
            "answer": """Architecting and maintaining a production-grade CI/CD test automation pipeline in **Jenkins** or **Azure DevOps** requires building a robust, self-healing, and highly optimized delivery mechanism that provides rapid, actionable feedback to engineering teams. At **Liberty Mutual** and **Molina Healthcare**, where automated suites executed between 200 to 350 tests daily across distributed microservices and multi-page web applications, running tests manually or sequentially on a developer's workstation is unacceptable. The pipeline must serve as an automated, impartial quality gate protecting staging and production environments.

The architecture of our enterprise pipeline is structured as a version-controlled, declarative pipeline (`Jenkinsfile` or `azure-pipelines.yml`) residing directly within the test automation Git repository. This ensures that any change to the testing pipeline undergoes code review alongside framework enhancements.

The execution workflow is segmented into disciplined, sequential and parallel stages. The pipeline initiates with a **Checkout & Environment Validation Stage**, retrieving the latest commit, setting Java 17 and Maven toolchains, and pulling required property files from secure credential stores. Next is the **Fast-Feedback API Smoke Stage**, executing lightweight REST Assured tests against active services. If a critical service returns a `500 Internal Server Error` or authentication endpoint fails, the pipeline fails immediately (in under 3 minutes), terminating execution before spinning up expensive browser nodes.

Upon passing the smoke gate, the pipeline initiates the **Parallel Multi-Browser Regression Stage**. Here, the declarative pipeline utilizes the `parallel` block to spawn concurrent execution tracks across isolated Docker containers. For instance, Track 1 executes Chrome Headless tests, Track 2 executes Firefox Headless tests, and Track 3 executes backend SQL reconciliation scripts. Inside each track, **Maven Surefire** is configured with `parallel=methods` and a `threadCount=4`, maximizing CPU utilization while **ThreadLocal<WebDriver>** guarantees complete thread safety.

Equally vital is the **Reporting and Artifact Management Stage** configured within the `post { always { ... } }` block. Regardless of whether tests pass or fail, the pipeline aggregates JUnit XML test results and compiles an interactive **Allure Report** dashboard. When tests fail, the framework's custom TestNG listeners capture full-page screenshots, DOM source snippets, and network HAR logs, automatically attaching them to the corresponding Allure test step. Finally, conditional post-actions notify the team: in the event of failure, an automated **Slack** or **Microsoft Teams** webhook broadcasts an alert detailing the failed test count, branch name, and a direct clickable link to the Allure failure dashboard. This automated pipeline transforms testing into a continuous, frictionless quality engine."""
        }
    },

    # =========================================================================
    # DAY 12: Dockerization, Selenium Grid & Cross-Browser Cloud Execution
    # =========================================================================
    {
        "day": 12,
        "title": "Day 12: Dockerization, Selenium Grid & Cross-Browser Cloud Execution",
        "theme": "Containerized Test Runners, Grid Scalability & Cloud Infrastructure",
        "domain_focus": "220 Daily Automated Tests in Docker (Molina Healthcare Context)",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: Core Architectural Theory",
                "topic": "Why Containerization is Essential for Modern QA Automation",
                "content": """### Eliminating the "It Works on My Machine" Dilemma:
Different OS environments, browser patch versions, and font rendering engines cause UI tests that pass locally on Windows/macOS to fail on Linux CI agents.
- **Dockerization Benefits:**
  1. **Deterministic Environment:** Exact same Java JDK, Chrome binary version, and display drivers across all machines.
  2. **Zero Host Pollution:** No need to install Chrome, Firefox, or drivers directly on build agents.
  3. **Instant Scalability:** Spin up 10 browser nodes on demand and tear them down immediately upon test completion."""
            },
            {
                "hour": 2,
                "label": "Hour 2: Production Code Lab",
                "topic": "`docker-compose.yml` for Selenium Grid & Test Runner Dockerfile",
                "content": """Below is the `docker-compose.yml` deploying a scalable Selenium 4 Grid with Chrome and Firefox nodes:

```yaml
version: '3.8'

services:
  selenium-hub:
    image: selenium/hub:4.18.1
    container_name: selenium-hub
    ports:
      - "4444:4444"
    environment:
      - GRID_MAX_SESSION=10
      - GRID_TIMEOUT=300

  chrome-node:
    image: selenium/node-chrome:4.18.1
    shm_size: 2gb # Prevent Chrome shared memory crash
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_MAX_SESSIONS=4

  firefox-node:
    image: selenium/node-firefox:4.18.1
    shm_size: 2gb
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
      - SE_NODE_MAX_SESSIONS=4

  test-runner:
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      - chrome-node
      - firefox-node
    environment:
      - GRID_URL=http://selenium-hub:4444/wd/hub
      - BROWSER=chrome
```

```dockerfile
# Dockerfile for Test Runner
FROM maven:3.9.6-eclipse-temurin-17-alpine
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src
CMD ["mvn", "clean", "test", "-DsuiteFile=src/test/resources/suites/testng-regression.xml"]
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Enterprise Edge Cases & Flaky Test Elimination",
                "topic": "Shared Memory Crashes (`/dev/shm`) & Cloud Grid Configuration",
                "content": """### Preventing Containerized Browser Crashes:
1. **The Shared Memory Trap (`shm_size: 2gb`):** By default, Docker allocates 64MB of shared memory to containers. Chrome uses `/dev/shm` to render web pages. In complex banking portals with heavy DOM trees, Chrome exceeds 64MB and crashes silently with `WebDriverException: session deleted because of page crash`. Always set `shm_size: 2gb` or pass `--disable-dev-shm-usage` in ChromeOptions.
2. **Cloud Grid Integration (BrowserStack / SauceLabs):** Using `RemoteWebDriver` with secure capabilities:
   ```java
   MutableCapabilities capabilities = new MutableCapabilities();
   capabilities.setCapability("browserName", "Chrome");
   capabilities.setCapability("browserVersion", "latest");
   HashMap<String, Object> bstackOptions = new HashMap<>();
   bstackOptions.put("os", "Windows");
   bstackOptions.put("osVersion", "11");
   capabilities.setCapability("bstack:options", bstackOptions);
   WebDriver driver = new RemoteWebDriver(new URL("https://hub-cloud.browserstack.com/wd/hub"), capabilities);
   ```"""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "Setting Up a Containerized Test Execution Grid with Docker & Selenium 4",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Deploying Docker Test Environments for 220 Daily Tests at Molina Healthcare",
                "content": """**Situation:** At **Molina Healthcare**, our automated UI tests suffered from environmental inconsistencies. Tests that passed on our development Windows machines consistently failed on Linux build agents due to differing Chrome minor versions, missing OS font libraries, and shared memory exhaustion.

**Task:** As QA Engineer, I was tasked with establishing a completely standardized, containerized test execution infrastructure capable of running 220 automated tests daily with zero environmental flakiness.

**Action:** I containerized our entire automation framework using **Docker** and orchestrated a distributed **Selenium Grid** using `docker-compose`. I configured a dedicated `selenium-hub` container connected to dynamic `node-chrome` and `node-firefox` worker containers, explicitly configuring `shm_size: 2gb` and `--disable-dev-shm-usage` to eradicate browser memory crashes. I authored a multi-stage Dockerfile for our Maven test runner, allowing our **Azure DevOps** pipeline to spin up the entire grid, execute our 220 automated scenarios concurrently across multiple containers, and tear down the infrastructure automatically upon test completion.

**Result:** Environmental test discrepancies dropped from 15% to 0%. Test execution consistency became 100% reproducible across development, QA, and staging environments, saving our team an estimated 10 hours per sprint in false-alarm triage."""
            }
        ],
        "master_qa": {
            "question": "How do you set up a distributed, containerized test execution environment using Docker and Selenium Grid, and what are the primary advantages?",
            "answer": """Setting up a distributed, containerized test execution environment using **Docker** and **Selenium Grid** is one of the most effective strategies for scaling enterprise UI automation, eliminating environmental flakiness, and drastically reducing regression execution time. At **Molina Healthcare** and **PNC Bank**, maintaining physical or virtual machines with manually installed browsers, operating system patches, and driver binaries was plagued by maintenance overhead and the classic 'it works on my machine' syndrome.

The architecture of a containerized **Selenium 4 Grid** centers on decoupling the test execution client from browser execution nodes using container orchestration. We configure this using `docker-compose.yml`. The core coordinator is the **Selenium Hub** container (utilizing the official `selenium/hub` image), which exposes port 4444. The Hub acts as the central router: when an automated test instantiates a `RemoteWebDriver` directed to `http://selenium-hub:4444/wd/hub`, the Hub inspects the requested `Capabilities` (such as browser name, version, and platform) and routes the session request to an available matching browser node.

Connected to the Hub are dynamic worker node containers, specifically `selenium/node-chrome` and `selenium/node-firefox`. These nodes register with the Hub via internal Docker network event buses (ports 4442 and 4443). Crucially, when configuring Chrome containers in Docker, a critical Linux kernel constraint must be addressed: by default, Docker limits container shared memory (`/dev/shm`) to 64 megabytes. When modern web applications render complex DOM structures, high-resolution styles, and JavaScript bundles, Chrome quickly exhausts this memory, triggering sudden browser crashes with `session deleted because of page crash`. In our `docker-compose.yml`, we explicitly assign `shm_size: 2gb` and configure ChromeOptions with `--disable-dev-shm-usage` and `--no-sandbox`.

The primary advantages of this containerized architecture are transformative:
1. **Total Environmental Determinism:** Every test executes against an identical, immutable Linux container image containing known browser versions and system libraries, eradicating OS-level rendering discrepancies.
2. **Horizontal Elastic Scalability:** When regression demand spikes, scaling execution capacity is as simple as executing `docker-compose scale chrome-node=8`, immediately doubling parallel throughput without procuring additional hardware.
3. **Resource Efficiency & Ephemeral Lifecycle:** Build agents in **Azure DevOps** or **Jenkins** spin up the entire grid on-demand at the start of a pipeline run, execute 220+ tests in parallel across headless containers, archive Allure test reports, and immediately tear down the containers, maintaining a lean, pristine CI/CD footprint."""
        }
    },

    # =========================================================================
    # DAY 13: Non-Functional Testing, Performance Telemetry & Defect Management
    # =========================================================================
    {
        "day": 13,
        "title": "Day 13: Non-Functional Testing, Performance Telemetry & Agile Defect Management",
        "theme": "Grafana Telemetry, Microservice Latency & Jira/Xray Defect Lifecycle",
        "domain_focus": "8K Daily Transactions Performance & Defect Triage (Molina & PNC)",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: Core Architectural Theory",
                "topic": "Microservice Performance Telemetry: Latency, Throughput & Error Rates",
                "content": """### Telemetry & Observability for Modern QA Engineers:
In microservices architectures, functional correctness is only half the battle. A test passing functionally while increasing P99 backend response times from 200ms to 4,000ms represents a severe production risk.
- **The Golden Signals of Observability:**
  1. **Latency:** Duration taken to service requests (measured in P50, P90, P95, P99 percentiles).
  2. **Traffic:** Demand placed on the service (Requests Per Second - RPS).
  3. **Errors:** Rate of requests failing explicitly (HTTP 5xx status codes).
  4. **Saturation:** Resource utilization (CPU, memory, database connection pool limits).
- **Tooling Ecosystem:** **Grafana** (dashboards), **Prometheus** (time-series metrics), **Splunk** / **Kibana** (log aggregation and correlation)."""
            },
            {
                "hour": 2,
                "label": "Hour 2: Production Code Lab",
                "topic": "Correlating Test Runs with Telemetry & Enterprise Jira/Xray Bug Logging",
                "content": """At **Molina Healthcare**, we monitor Grafana dashboards during performance tests supporting 8K daily transactions. When microservices degrade, we log detailed Jira defects:

```markdown
### JIRA DEFECT REPORT TEMPLATE (ENTERPRISE STANDARD)

**Issue Key:** PNC-9412
**Issue Type:** Bug
**Summary:** [P1 - Critical] Fund Transfer Microservice P99 Latency Spikes to 4.8s Under 50 Concurrent Users
**Components:** Transfer-Service, Oracle-Database
**Fix Version:** Release-2026.4
**Severity:** High (S2) | **Priority:** High (P1)

#### Environment:
- **Environment:** Staging / QA-Performance-02
- **Build Version:** v2.14.0-RC3
- **Database:** Oracle 19c Enterprise

#### Description:
During execution of the automated payroll regression suite (120 scenarios), monitored via Grafana dashboard (Dashboard ID: `pnc-perf-txns`), the `POST /api/v2/transfers/domestic` endpoint exhibited severe latency degradation. At 50 concurrent transactions, P99 response times degraded from 280ms baseline to 4,820ms, with 6.5% of requests failing with HTTP 504 Gateway Timeout.

#### Steps to Reproduce:
1. Initialize test runner with 50 concurrent threads executing transfer batch requests.
2. Disburse wire transfers exceeding $10,000 with memo tag "PAYROLL_RUN".
3. Observe Splunk logs for trace ID correlation: `index=banking_logs sourcetype=transfer_svc | stats count by status`.
4. Inspect Grafana metric `http_server_requests_seconds_max{uri="/api/v2/transfers/domestic"}`.

#### Expected Result:
P99 response time should remain under 500ms; zero HTTP 504 gateway timeouts.

#### Actual Result:
P99 latency spiked to 4.82s; HikariCP connection pool exhausted (active connections = 50/50, thread wait queue = 142).

#### Root Cause Analysis (Initial QA Triage):
Oracle database query `SELECT ... FROM account_ledger WHERE account_id = ?` missing index on `account_id`, causing full table scans across 1.2M records.

#### Attachments:
- `grafana_latency_spike.png`
- `splunk_error_trace.log`
- `jmeter_aggregate_report.csv`
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Enterprise Edge Cases & Flaky Test Elimination",
                "topic": "Defect Triage Leadership & Handling Developer Pushback",
                "content": """### Navigating Defect Triage Meetings:
When a developer says, *"It works on my machine, this is not a bug"*, an elite QA automation engineer responds with data, not opinions:
1. Provide the exact correlation ID, timestamp, and environment configuration.
2. Provide the recorded video or Playwright trace file showing the failure.
3. Attach backend Splunk logs demonstrating database deadlocks or HTTP 500 traces.
4. Reference the agreed-upon acceptance criteria in the **Jira/Xray** user story."""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "Using Telemetry (Grafana, Splunk) During Test Execution to Catch Degradation",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Identifying Microservice Degradation via Grafana at Molina Healthcare",
                "content": """**Situation:** At **Molina Healthcare**, our automated test suites supported payroll processing operations exceeding $1M+ per processing cycle across microservices handling approximately 8,000 daily transactions. During a pre-release regression cycle, all functional automated tests passed successfully with 100% green status.

**Task:** As the QA Engineer, I was monitoring our non-functional test metrics to ensure that the release satisfied our production Service Level Objectives (SLOs) before sign-off.

**Action:** While reviewing our **Grafana** performance dashboards during the execution of our 120 automated payroll scenarios, I detected an alarming anomaly: while HTTP responses were returning `200 OK`, backend P95 database query latency had quadrupled from 85ms to 420ms, and the connection pool was operating at 94% saturation. Correlating timestamps with **Splunk** logs, I identified that a newly added audit logging interceptor was performing synchronous database writes on every single API call rather than queuing them asynchronously via Kafka.

**Result:** I immediately raised a P1 defect in **Jira**, backed by Grafana metric screenshots and Splunk stack traces, prompting developers to refactor the audit logger to use asynchronous non-blocking event publishing. This preempted a severe production outage during peak payroll processing for our **$1M+ transaction operations**."""
            }
        ],
        "master_qa": {
            "question": "How do you use telemetry tools like Grafana, Splunk, or Datadog during test execution to identify backend microservice degradation before production rollout?",
            "answer": """In modern cloud-native microservice architectures, evaluating software quality solely on functional binary outcomes (pass versus fail) creates a dangerous blind spot. An automated test can assert an HTTP `200 OK` or verify that a UI confirmation badge appears, while masking severe backend degradation—such as memory leaks, thread starvation, unindexed database queries, or downstream connection pool saturation. At **Molina Healthcare** and **PNC Bank**, where systems process thousands of daily transactions supporting millions of dollars in financial activity, integrating telemetry tools like **Grafana**, **Prometheus**, **Splunk**, and **Datadog** into the QA workflow is essential for identifying service degradation before code reaches production.

The methodology begins by establishing clear correlation handles during test execution. In our **REST Assured** and **Selenium** frameworks, every test run injects a standardized, dynamic tracing header—such as `X-Correlation-ID: QA-PERF-<UUID>` and `X-Test-Name: PayrollBatchExecution`—into all outgoing HTTP requests. This correlation token cascades through API gateways, microservices, messaging brokers, and database layers.

During the execution of our automated regression suites (such as the 120 payroll scenarios at Molina Healthcare), I observe real-time **Grafana** dashboards configured to monitor the 'Four Golden Signals': latency, traffic, errors, and saturation. Specifically, I inspect latency distribution curves broken down into P90, P95, and P99 percentiles, rather than relying on misleading arithmetic averages. For example, if a microservice handles 8,000 daily transactions, an average response time of 250ms might appear acceptable, but a P99 latency of 4,800ms indicates that 80 transactions every day are experiencing severe timeouts.

When Grafana alerts indicate a latency spike or connection pool saturation, I transition immediately to **Splunk** or **Datadog** for distributed trace analysis. By querying `index=healthcare_apps correlation_id="QA-PERF-*"`, I isolate the exact microservice span responsible for the delay. In one prominent incident at Molina Healthcare, this telemetry analysis revealed that while payroll APIs were returning functional successes, an un-indexed database foreign key check was forcing Oracle to perform full table scans across 500,000 rows, consuming 92% of available database connections.

Armed with objective telemetry data—including Grafana latency graphs, Splunk stack traces, and database connection pool saturation metrics—I file high-priority defects in **Jira/Xray**. This empowers developers to optimize code, add missing indexes, or implement asynchronous caching before production rollout, transforming QA from a simple verification gate into a proactive driver of system reliability."""
        }
    },

    # =========================================================================
    # DAY 14: Master End-to-End Mock Interview, Resume Defense & Live Coding Drills
    # =========================================================================
    {
        "day": 14,
        "title": "Day 14: Master End-to-End Mock Interview, Resume Defense & Live Coding Drills",
        "theme": "Final Polish, Live Coding Drills, Resume Defense & Interview Mastery",
        "domain_focus": "The Complete QA Automation Engineering Interview Mastery",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: The 90-Second Professional Elevator Pitch & Resume Defense",
                "topic": "Mastering the 'Tell Me About Yourself' & Experience Narrative",
                "content": """### The Perfect 90-Second QA Automation Elevator Pitch:
*"Hi, I'm Janaki Ashok Kumar. I am a QA Automation Engineer with over 7 years of deep, hands-on experience designing and building scalable automation frameworks across banking, insurance, healthcare, and payroll domains. 

Currently, at **PNC Bank**, I specialize in automating complex HUB commercial banking workflows, architecting a Java framework combining **Selenium WebDriver**, **Cucumber BDD**, and **TestNG** that reduced regression execution time from 8 hours down to 3 hours across 180 scenarios. I also validate 90 backend microservice APIs using **REST Assured** and author complex SQL scripts for database reconciliation supporting over **$2M+ in daily transaction activity**.

Prior to PNC, at **Liberty Mutual**, I led automation for 160 policy administration scenarios using Selenium, TestNG, and REST Assured, and optimized **Jenkins** CI/CD pipelines running 200+ tests daily across 25,000+ policy records. Earlier in my career at **Molina Healthcare**, I pioneered the adoption of **Playwright**, cutting member enrollment regression from 12 hours to 5 hours, while establishing **Docker** execution environments and monitoring microservice performance with **Grafana** across 8,000 daily transactions.

I pride myself on strong engineering fundamentals—from thread-safe driver architecture and CI/CD quality gates to collaborating closely with developers and product owners in Agile environments to ensure zero defect leakage into production. I'm excited to be here today to discuss how my automation expertise can drive immediate value for your team."*"""
            },
            {
                "hour": 2,
                "label": "Hour 2: Live Coding Mastery: 5 Core Java Automation Interview Problems",
                "topic": "String Manipulation, Collections & Two-Pointer Algorithms",
                "content": """Below are 5 core coding interview problems frequently asked in senior QA automation interviews:

```java
package com.qa.interview.coding;

import java.util.*;

public class CoreAutomationCodingDrills {

    // 1. Reverse String without using StringBuilder.reverse()
    public static String reverseString(String str) {
        if (str == null) return null;
        char[] chars = str.toCharArray();
        int left = 0, right = chars.length - 1;
        while (left < right) {
            char temp = chars[left];
            chars[left] = chars[right];
            chars[right] = temp;
            left++;
            right--;
        }
        return new String(chars);
    }

    // 2. Find First Non-Repeating Character in a String
    public static Character findFirstNonRepeatingChar(String s) {
        Map<Character, Integer> counts = new LinkedHashMap<>();
        for (char c : s.toCharArray()) {
            counts.put(c, counts.getOrDefault(c, 0) + 1);
        }
        for (Map.Entry<Character, Integer> entry : counts.entrySet()) {
            if (entry.getValue() == 1) {
                return entry.getKey();
            }
        }
        return null;
    }

    // 3. Check for Balanced Parentheses / Brackets (Stack)
    public static boolean isBalanced(String s) {
        Stack<Character> stack = new Stack<>();
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '{' || c == '[') {
                stack.push(c);
            } else if (c == ')' && !stack.isEmpty() && stack.peek() == '(') {
                stack.pop();
            } else if (c == '}' && !stack.isEmpty() && stack.peek() == '{') {
                stack.pop();
            } else if (c == ']' && !stack.isEmpty() && stack.peek() == '[') {
                stack.pop();
            } else {
                return false;
            }
        }
        return stack.isEmpty();
    }

    // 4. Two Sum Problem (Return indexes summing to target)
    public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            map.put(nums[i], i);
        }
        return new int[]{};
    }

    // 5. Count Word Frequencies in a Text (Data Parsing)
    public static Map<String, Integer> countWordFrequency(String text) {
        Map<String, Integer> freq = new HashMap<>();
        String[] words = text.toLowerCase().split("\\W+");
        for (String word : words) {
            if (!word.isEmpty()) {
                freq.put(word, freq.getOrDefault(word, 0) + 1);
            }
        }
        return freq;
    }
}
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Framework Whiteboard Architecture & Live Defense",
                "topic": "Explaining Your Hybrid Framework on a Whiteboard to an Interviewer",
                "content": """### How to Draw & Explain Your Framework on a Whiteboard:
1. **Base Layer:** Java 17, Maven, ThreadLocal Driver Manager (Chrome, Firefox, RemoteWebDriver).
2. **Page Layer:** Page Object Model, BasePage with FluentWait, By locators, dynamic scrolling.
3. **Data Layer:** Apache POI Excel Reader, JSON POJOs, JDBC Database Manager (HikariCP).
4. **Execution Layer:** Cucumber BDD (Feature files, PicoContainer for state sharing), TestNG runner (`parallel="methods"`), Retry Analyzer.
5. **API Layer:** REST Assured with RequestSpecBuilder, JSON Schema Validator, OAuth 2.0 TokenManager.
6. **Infrastructure Layer:** Docker containers, Selenium Grid, Jenkins/Azure DevOps CI/CD pipelines, Allure Reports, Slack alerts."""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "Handling Tricky QA Curveball Questions & Tight Release Deadlines",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Facilitating Defect Triage & Leading Quality Across 14 Releases",
                "content": """**Situation:** Across multiple release cycles at **Liberty Mutual** and **PNC Bank**, tight sprint deadlines frequently created tension between software developers striving to ship features on time and QA engineers identifying defects late in the release candidate phase.

**Task:** As a Senior QA Automation Engineer, I was responsible for facilitating defect triage meetings, aligning developers and product stakeholders on release risk, and driving swift resolution without compromising production stability.

**Action:** I established a structured, transparent **Defect Triage Protocol** integrated into **Jira** and **Xray**. I instituted a daily 15-minute standup during release weeks with the Lead Developer, Product Owner, and Release Manager. For every reported defect, I provided automated reproducible test scripts (REST Assured curl payloads or recorded video traces), categorized defects strictly by business impact (Severity S1–S4 vs. Priority P1–P4), and presented telemetry demonstrating potential user impact. When developers questioned test validity, I walked through the automated logs and database reconciliation scripts demonstrating ledger inconsistencies.

**Result:** We successfully streamlined defect resolution across 14 consecutive release iterations, cut defect resolution cycle times by 35%, and achieved a 99.9% production service availability record across banking and insurance operations."""
            }
        ],
        "master_qa": {
            "question": "How do you handle difficult interview curveballs: testing with incomplete documentation, handling developer pushback on defects, and making release go/no-go decisions under tight deadlines?",
            "answer": """In senior QA automation roles—such as my experience at **PNC Bank**, **Liberty Mutual**, and **Molina Healthcare**—technical proficiency must be matched by high-stakes communication, professional diplomacy, and pragmatic risk management. Interviewers frequently assess how an engineer operates when conditions are imperfect: when specifications are incomplete, when developers contest defect validity, or when release deadlines force difficult trade-offs.

When confronted with **incomplete or missing documentation**, I do not wait passively for documentation to be written. I adopt a proactive, investigative engineering approach. First, I inspect existing backend API contracts through **Swagger/OpenAPI** specifications, review code pull requests directly in **GitHub**, and examine existing database schemas and unit tests to deduce intended functionality. Second, I engage directly with the Product Owner and Lead Architect during sprint planning, leveraging **Behavior-Driven Development (BDD)** and Gherkin syntax to formulate concrete, question-driven scenarios (e.g., 'If a corporate client submits a $150,000 transfer after 5:00 PM EST, does the status default to PENDING or REJECTED?'). Formulating concrete acceptance criteria transforms ambiguity into validated test requirements before coding begins.

When managing **developer pushback on defects**—such as when a developer states 'it works on my machine' or 'this is an edge case that users won't encounter'—I anchor discussions entirely in objective empirical data. I provide an airtight defect report in **Jira/Xray** containing:
1. The automated test execution logs, including the exact HTTP request payload, response status, and correlation ID.
2. A recorded video or **Playwright Trace** showing the exact UI state and network waterfall.
3. Backend **Splunk** stack traces and SQL query results demonstrating database constraint violations.
By demonstrating the defect's concrete business impact (such as financial ledger discrepancies or regulatory compliance risks in PNC's $2M+ daily transactions), I depersonalize the conversation, framing quality as a shared team objective rather than an adversarial critique.

Finally, when evaluating **release go/no-go decisions under tight deadlines**, I rely on a structured risk assessment framework. If non-blocking P3/P4 aesthetic defects remain open, I collaborate with the Product Owner to document known issues, establish release notes, and schedule automated regression coverage for the subsequent sprint. However, if any P1/S1 defect impacts financial data integrity, security authorization, or transactional reconciliation, I maintain the technical integrity to recommend a 'NO-GO', presenting clear telemetry, defect severity matrices, and concrete mitigation options to executive leadership."""
        }
    }
]
