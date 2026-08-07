---
title: Janaki Oracle Prep Guide
description: Comprehensive preparation guide for the QA Automation Engineer interview at Oracle Health, customized for Janaki Ashok Kumar.
---

# Janaki Ashok Kumar Prep Guide: QA Automation Engineer (Oracle Health)

Welcome to your preparation guide for the QA Automation Engineer role at **Oracle Health Applications & Infrastructure**. This guide is designed around your experience in building scalable test automation frameworks, validating UI/API microservices, running database migrations, and automating release quality at **PNC Bank**, **Liberty Mutual**, and **Molina Healthcare**, mapping those competencies to Oracle Health's technical requirements and core values.

---

## Resume & Role Alignment

The QA Automation Engineer role at Oracle Health requires designing, developing, and managing UI, API, database, and end-to-end test automation solutions. It demands candidates who can own the complete QA lifecycle, from scoping to production monitoring, partnering with cross-functional teams to automate workflows and optimize test execution pipelines.

Here is how your background directly bridges to these requirements:

*   **UI Test Automation & Framework Design:** You have 7+ years of QA experience. At PNC Bank, you architected a **Java** automation framework integrating **Selenium WebDriver** and **Cucumber BDD**, reducing regression execution times from 8 hours to 3 hours. At Molina, you engineered **Playwright** automation suites covering 180 enrollment scenarios.
*   **API & Microservices Testing:** You designed **REST Assured** and **Postman** validations for 90 APIs at PNC and 110 policy APIs at Liberty Mutual, validating backend integration, security (JWT/OAuth), and JSON Schema configurations.
*   **Database Reconciliation & SQL:** You authored **SQL** and **Oracle** validation scripts for 75 reconciliation scenarios at PNC and 90 scenarios at Molina, verifying transactional data consistency across database storage layers.
*   **DevOps & CI/CD Pipelines:** You integrated test suites into **Jenkins** and **Azure DevOps** CI/CD pipelines, ran tests in **Docker** container environments, and monitored microservices performance using **Grafana** dashboards.
*   **Agile Defect Triage & Traceability:** You managed requirements, test execution, and defect resolutions using **Jira**, **Xray**, and **ALM** across multiple releases, collaborating with developers to deliver production-ready software.

---

## Part 1: Top 30 Technical & Behavioral Questions & Answers

### 1. How did you validate HUB banking workflows using Selenium and Postman at PNC Bank, and how does this align with Oracle Health's "Put Customers First" value?
At **PNC Bank**, I validated HUB banking workflows across sixty transfer, template, and inbox scenarios using **Selenium WebDriver** and **Postman**, ensuring stable releases for multi-account and approval processes supporting $2M+ in daily transaction activity. HUB banking applications are highly complex, requiring secure authorization, multi-level approvals, and real-time transaction processing. A minor failure in the customer inbox or template validation could block cash transfers, causing immediate financial loss and damaging customer trust. To prevent this, I designed end-to-end automated UI scripts that validated the entire transaction path from the user's dashboard to the ledger.

I used Postman to mock API responses, allowing us to test UI behavior under various network latencies and error states. I validated that transaction confirmation templates loaded correctly across different device configurations. This focus on the end-user's transactional flow maps directly to Oracle Health's value of putting customers first. We exist to satisfy our customers, which means we must test our software through the customer's eyes.

By prioritizing customer outcomes, I ensured that our automation suites targeted the most critical user paths, such as approving multi-account transfers. I verified that error messages were clear and descriptive, preventing user confusion during transaction drops. In this role, I will bring this customer-centric QA approach to Oracle Health's applications, designing rigorous automation checks to ensure that medical providers and patients experience stable, reliable, and frictionless software workflows.

---

### 2. Describe how you architected a Java automation framework integrating Selenium WebDriver and Cucumber BDD at PNC Bank. How did you iterate to reduce execution time?
At **PNC Bank**, I architected a hybrid **Java** test automation framework from scratch, integrating **Selenium WebDriver** and **Cucumber BDD** to manage 180 regression scenarios. Initially, our regression suite took over 8 hours to execute sequentially, which delayed our staging deployment checks and blocked biweekly releases. I applied Oracle Health's value of acting now and iterating: I built a baseline framework to ensure coverage, and then optimized the architecture to improve performance.

I refactored the framework to use the **Page Object Model (POM)** design pattern, which separated the page elements from the test step definitions, reducing code duplication and making maintenance easier. I implemented parallel test execution using **TestNG** and **Maven**, configuring the runners to distribute test scenarios across multiple threads. I also optimized our element locators, replacing slow XPath queries with fast ID and CSS selectors.

These iterations reduced our regression execution time from 8 hours to 3 hours, saving 5 hours per run. I integrated the Maven execution scripts into our **Jenkins** pipelines, providing developers with automated test feedback within hours of a code commit. I will bring this iterative automation mindset to Oracle Health, building reusable Java assets and optimizing test suites to accelerate release velocity.

---

### 3. How do you construct REST Assured validations for APIs, and how does this align with the "Nail the Basics" value?
Nailing the basics means focusing on fundamentals over flash, recognizing that the path to advanced systems runs through clean, stable interfaces. In application QA, APIs are the basic communication layers that connect microservices, databases, and frontends. If the APIs fail, the entire system degrades. At **PNC Bank**, I constructed **REST Assured** validations for 90 APIs handling account transfers and notifications, identifying integration defects before deployment.

I wrote automated test cases in **Java** to validate API endpoints, verifying HTTP response status codes (such as 200 OK or 400 Bad Request), headers, and execution latencies. I used REST Assured's built-in validation methods to perform JSON Schema validations, checking that the response payload matched our API contracts. I also verified API security, passing valid and invalid JWT tokens to check OAuth 2.0 authorization rules.

By testing the APIs in isolation, we identified data type mismatches and serialization errors before they reached the UI layer, preventing complex debugging sessions during integration testing. This focus on backend API validation ensures that the foundational layers of our software are stable, secure, and compliant. I will apply this rigorous API validation approach to Oracle Health's microservices.

---

### 4. How did you coordinate Jira and Xray test management at PNC Bank, and how do you handle changing priorities?
Operating in a fast-paced environment requires adaptability and situational awareness. At **PNC Bank**, I coordinated **Jira** and **Xray** test management for 12 sprint releases, collaborating with developers, product owners, and business analysts to track test coverage and triage defects. In Agile development, requirements and priorities can change quickly due to customer feedback or production issues.

When a priority shift occurred, I did not hang on to outdated test plans. I reviewed our Xray test execution boards, identified which test cases were affected by the scope change, and updated our regression suites. I organized defect triage meetings in Jira, coordinating with developers to retest critical bug fixes and ensure that the most important user paths remained functional.

This adaptability maps directly to Oracle Health's value of expecting and embracing change. I align quickly with current priorities, using Jira and Xray to maintain end-to-end traceability between requirements, test runs, and defects. I will bring this agile coordination to Oracle Health's QA workflows, ensuring our testing is aligned with development sprints and release targets.

---

### 5. How did you partner with developers and business stakeholders to resolve defects during Liberty Mutual's policy releases?
At **Liberty Mutual**, I developed **Selenium** and **TestNG** automation suites covering 160 policy administration scenarios across monthly insurance releases supporting 25K+ records. Managing these releases required close collaboration between QA, developers, and business analysts to resolve defects quickly. I facilitated Jira-based defect triage across 14 release iterations, aligning the team on priority issues.

When our automated regression pipeline flagged a defect in the policy calculation engine, I did not just file a bug report. I collected the diagnostic data, including **REST Assured** API log payloads, SQL database outputs, and Selenium screenshots, and documented the root cause in Jira. I met with the developers to walk them through the execution steps, helping them locate and patch the calculation bug quickly.

I also collaborated with our business analysts to ensure the automated test cases accurately reflected current insurance policies. This collaborative effort maps to Oracle Health's value of innovating together. By practicing empathy, respect, and clear communication, I helped our cross-functional team deliver stable, high-quality releases, reducing our manual regression effort.

---

### 6. Describe a time you faced a major automation script execution failure during release testing and how you resolved it.
During a monthly insurance release at **Liberty Mutual**, our automated regression suite began experiencing widespread failures on our staging environment, with over forty percent of our **Selenium** tests failing due to connection timeouts. The product team was facing a tight deployment window, and the team was under pressure. I remained calm, mapped out a mitigation plan, and started investigating.

I analyzed our **Jenkins** logs and database connections, and discovered that our test databases were locked due to an unindexed migration script that was running in parallel. This migration script was locking the policy tables, causing our Selenium tests to timeout while waiting for database responses. I coordinated with the database administrator to pause the migration script, restoring database performance.

I then re-ran the Selenium suite, and all tests passed. To prevent similar issues, I updated our Jenkins pipelines, scheduling database migrations and automation runs at separate times, and configured explicit wait times in our Selenium scripts. This experience demonstrated my ability to remain calm, locate root causes, and deliver results, which aligns with Oracle Health's value of taking risks and remaining calm.

---

### 7. Tell me about a time you noticed a test coverage gap or a bad process and took ownership to resolve it.
At **Molina Healthcare**, our team was manually verifying member eligibility datasets across different databases, which took over 8 hours of manual effort per sprint and led to inconsistent test results. I realized this manual validation process was a bottleneck and took ownership to automate it, refusing to say "that's not my job."

I developed a suite of **SQL** and **Oracle** validation scripts to automate our data reconciliation workflows across 90 scenarios, checking member, provider, and claims tables for data consistency. I wrote Python scripts that executed these database validations and outputted a clean variance report, reducing our report preparation effort.

This automation simplified our UAT validation checks and improved data accuracy. By taking ownership of this process improvement, I helped our team transition from manual spreadsheet checking to automated, repeatable database validation, demonstrating my commitment to operational excellence. I will bring this proactive ownership to Oracle Health's QA teams.

---

### 8. How did you earn the trust of your development team when migrating legacy test cases to modern frameworks?
Earning trust requires transparent communication, technical credibility, and collaborative execution. At **Molina Healthcare**, when we decided to migrate our legacy member enrollment tests from Selenium to **Playwright**, the development team was skeptical, concerned that the migration would disrupt their sprint velocities and generate flaky test alerts in their pipelines.

To earn their trust, I did not implement the migration in isolation. I built a lightweight Playwright prototype covering a small set of enrollment scenarios, showing how Playwright's auto-waiting and shadow DOM support eliminated the flaky timeouts we experienced in Selenium. I demonstrated that the new suite was faster, reducing regression runtimes significantly.

I collaborated with the developers to integrate the Playwright tests into their **Azure DevOps** CI/CD pipelines, configuring the runner to only alert on actual code failures. This technical proof convinced the team of the migration's value. By communicating openly and delivering a reliable system, I earned their trust, aligning with Oracle Health's value of earning and giving trust.

---

### 9. How do you ensure the Java frameworks you build are modular, maintainable, and scalable for long-term use?
Building scalable automation frameworks requires a focus on software engineering fundamentals, utilizing design patterns like the **Page Object Model (POM)** and BDD frameworks like **Cucumber**. At **PNC Bank**, I architected a Java framework integrating Selenium WebDriver, TestNG, and Maven, ensuring code reusability and clean separation of concerns.

I structured the framework by separating our page elements, step definitions, utility scripts, and test runner configurations into distinct packages. I used **Maven** to manage our dependencies and **TestNG** to configure parallel execution rules. I wrote modular helper classes in Java (using Apache POI for Excel data parsing and JDBC for SQL database connections), allowing analysts to write tests without writing raw helper code.

I enforce code quality standards, writing clean comments and structuring test cases to be easily readable. This attention to detail ensures that the framework can be maintained and scaled by other QA engineers as the application grows, demonstrating my pride in my work. I will apply these software engineering principles to Oracle Health's automation suites.

---

### 10. Give an example of when you challenged an existing manual testing methodology and successfully championed automated testing.
At **Molina Healthcare**, the QA team was manually executing 120 payroll processing scenarios for every recurring software release. This manual verification was slow, taking several days, and increased the risk of missing bugs in our payroll calculations. I challenged this manual methodology, proposing that we automate the entire payroll regression suite.

I faced skepticism regarding the feasibility of automating complex payroll calculations, but I championed the execution. I built **Selenium** and **TestNG** automation scripts to validate the payroll scenarios, covering tax deductions, direct deposits, and salary calculations. I wrote SQL scripts to verify the outputs against our database records.

This automation suite reduced our manual regression effort across recurring releases, ensuring error-free payroll operations. By challenging the manual process and delivering a working solution, I demonstrated the value of automation, helping our team shift our resources to exploratory testing. I will bring this challenge-and-execute mindset to Oracle Health.

---

### 11. Compare your experience using Playwright at Molina Healthcare and Selenium at PNC/Liberty Mutual. When would you choose each for healthcare apps?
At **Molina Healthcare**, I engineered **Playwright** automation suites covering 180 member enrollment scenarios, reducing regression execution from 12 hours to 5 hours. At **PNC Bank** and **Liberty Mutual**, I built **Selenium WebDriver** and Cucumber frameworks in **Java**. Both tools are excellent for UI validation, but they have different execution architectures.

Selenium is a mature tool that uses the W3C WebDriver protocol to communicate with browsers, which supports a wide array of browsers and legacy systems, but can introduce latency and flaky tests if element waits are not configured correctly. Playwright is a modern framework that connects directly to browsers via WebSocket, enabling faster test execution, auto-waiting, and native browser tracing, which reduces flaky test failures.

For modern, cloud-native healthcare applications that utilize single-page architectures (like React or Angular), I would choose Playwright because its auto-waiting and browser context isolation make tests fast and stable. For legacy enterprise systems that require testing across older Internet Explorer versions or complex third-party integrations, I would choose Selenium for its browser compatibility.

---

### 12. How did you design REST Assured and Postman validations for 110 policy and claims APIs at Liberty Mutual?
At **Liberty Mutual**, I designed **REST Assured** and **Postman** validations for 110 policy and claims APIs, improving defect detection during backend integration and service orchestration testing. Financial and insurance APIs must process complex payloads, validate business rules, and connect to downstream databases securely.

I structured our REST Assured test suites using the Given-When-Then BDD syntax in Java. I wrote scripts to send HTTP POST requests containing policy details, validated the HTTP response codes, and verified the returned JSON parameters. I implemented JSON Schema validations to confirm that the response payloads conformed to our API schemas, and checked authentication tokens (JWT) against our security rules.

For exploratory API testing, I built collections in Postman, configuring environment variables and pre-request scripts to manage authorization tokens dynamically. This API testing allowed us to identify serialization errors and backend connection failures early, ensuring our microservices operated reliably. I will bring this API testing capability to Oracle Health.

---

### 13. Describe your experience authoring SQL and Oracle validation scripts to ensure data consistency across distributed systems.
In transactional banking and insurance systems, data must remain consistent as it moves from the user interface, through APIs, and into backend databases. At **Liberty Mutual** and **Molina Healthcare**, I implemented **SQL** and **Oracle** validation scripts for 85 and 90 reconciliation scenarios, ensuring accurate policy, claims, and member records.

I wrote complex SQL queries (using joins, group by, and subqueries) to compare records across distributed tables. For example, I wrote validation scripts that joined our claims processing tables with our member enrollment tables, verifying that the member ID and claim status matched across both systems. I checked for data type truncation, missing keys, and duplicate records.

By running these database validation scripts, we identified data sync defects where API write operations failed to update the relational tables, preventing reporting errors. This database testing ensures that our data pipelines are reliable and secure, directly matching the data validation focus of the Oracle Health JD.

---

### 14. How did you optimize Jenkins-driven regression pipelines to provide continuous quality feedback?
Continuous integration requires executing automated tests as part of the build pipeline, providing developers with fast feedback on code changes. At **Liberty Mutual**, I optimized **Jenkins-driven** regression pipelines executing 200+ tests daily, integrating our Selenium and TestNG automation suites with build triggers.

I configured the Jenkinsfiles using declarative syntax, defining stages for checkouts, dependency installation, test execution, and report generation. To optimize execution time, I configured the pipeline to run tests in parallel across multiple Jenkins agent nodes and set up build triggers to execute smoke tests on every pull request, saving the full regression run for nightly builds.

I integrated the build status with automated Slack notifications and email alerts, ensuring the team was immediately notified if a test failed. This pipeline optimization reduced our feedback loops from days to minutes, allowing developers to catch and fix regressions early, aligning with MLOps and CI/CD best practices.

---

### 15. How did you establish Docker execution environments running 220 automated tests daily at Molina Healthcare?
Running tests in consistent environments is critical to prevent the "it works on my machine" problem, where tests fail in the CI/CD pipeline due to dependency mismatches or browser configurations. At **Molina Healthcare**, I established **Docker** execution environments running 220 automated tests daily, maintaining consistent execution across development, QA, and staging.

I wrote Dockerfiles to define our test execution images, specifying the Java runtime, Chrome/Firefox browsers, and Maven dependencies. I built a Docker Compose configuration that spun up a Selenium Grid, containing a hub node and multiple browser worker containers. The automation tests executed inside these isolated containers, using virtual framebuffers to run headless browser sessions.

This containerization eliminated browser dependency issues and allowed us to run tests in parallel without resource contention on our host machines. The Docker execution environment was integrated with our Azure DevOps pipelines, ensuring that our test execution was reproducible. I will apply this containerization experience to scale Oracle Health's test environments.

---

### 16. How did you integrate Azure DevOps pipelines with regression suites executing 350 test cases at Molina Healthcare?
At **Molina Healthcare**, I integrated **Azure DevOps** pipelines with our regression suites, executing 350 automated test cases and delivering continuous quality feedback throughout our monthly release activities. Integrating test automation with Azure DevOps ensures that release managers have a clear view of software quality before promoting code.

I wrote YAML pipeline definitions in Azure DevOps, configuring triggers to execute our Playwright and Selenium suites after staging deployments. The pipeline ran the test containers, executed the Maven builds, and published the test results (.xml) directly to the Azure Test Plans dashboard. This dashboard provided the release team with a visual summary of pass/fail rates.

I also configured automated bug creation: if a critical test failed in the pipeline, the task automatically created a linked bug in Jira, attaching the execution logs and stack traces. This pipeline integration reduced our manual release verification effort and ensured that our production deployments were validated against our regression suites.

---

### 17. How did you monitor Grafana dashboards during performance testing of microservices supporting 8K daily transactions?
Performance testing ensures that microservices handle peak transaction volumes without latency spikes or memory leaks. At **Molina Healthcare**, I monitored **Grafana** dashboards during performance testing of microservices supporting approximately 8K daily transactions, identifying service degradation before production rollouts.

I worked with our DevOps team to configure Prometheus metrics, capturing CPU utilization, memory allocations, garbage collection latencies, and API response times across our Kubernetes pods. During load testing runs (using JMeter), I monitored these metrics in Grafana, looking for trends like memory leaks (where memory usage steadily increased without dropping) or connection pool exhaustion.

In one instance, I identified that our member validation microservice experienced a latency spike when concurrent transactions exceeded 100 requests per second. The Grafana dashboards showed that database connection wait times were rising, indicating a pool bottleneck. We resolved this by increasing the connection pool size, ensuring the service operated reliably under load.

---

### 18. Describe your experience maintaining end-to-end traceability using ALM, Jira, and Xray test management.
Maintaining end-to-end traceability is critical in regulated domains like healthcare and banking, ensuring that every software requirement is covered by a test case, and every identified defect is linked to a failing test. At **Molina Healthcare** and **PNC Bank**, I managed these traceability matrices using **ALM** and **Jira** with **Xray**.

I mapped our user stories in Jira to corresponding test cases in Xray. When executing our Selenium or Playwright regression suites, the test results were imported back to Jira, updating the status of our requirement coverage. This integration allowed project stakeholders to see which user stories were fully tested and which were blocked by defects.

If a test failed, I created a bug ticket in Jira, linking it directly to the failing test run and the user story. This traceability ensured that when developers deployed a fix, we could identify which test cases to execute for validation. By maintaining these records, I helped our cross-functional teams pass compliance audits and deliver reliable software.

---

### 19. How do you structure Cucumber BDD feature files and step definitions to ensure they are maintainable?
Cucumber BDD (Behavior-Driven Development) feature files use the Gherkin syntax (Given-When-Then) to write test scenarios in plain English, allowing business analysts and developers to collaborate on requirements. However, if not structured correctly, BDD frameworks can suffer from step definition duplication and maintenance bottlenecks.

To ensure maintainability, I write Gherkin steps that are declarative rather than imperative. Instead of writing detailed UI actions (like "Given I click the username input and type my name"), I write high-level business behaviors (like "Given I log in as a banking customer"). This abstraction ensures that if the UI layout changes, we only update the underlying page object class, keeping the feature files unchanged.

I implement the **Page Object Model (POM)** design pattern in our Java step definitions. The step definition classes act as controllers, calling methods from our page classes to interact with the UI. I also use dependency injection (such as Picocontainer) to share state variables between step classes, preventing static variable issues during parallel execution.

---

### 20. How do you validate REST APIs protected by OAuth 2.0 and JWT using REST Assured?
Validating secured APIs requires handling authentication tokens, validating signature headers, and testing authorization rules. Most modern SaaS and healthcare APIs use OAuth 2.0 or OpenID Connect (OIDC) protocols, requiring clients to retrieve a JSON Web Token (JWT) from an authorization server before calling endpoints.

I automate this authentication flow in **REST Assured** using Java helper classes. I write a configuration method that sends an HTTP POST request to our token endpoint, passing the client credentials and retrieving the access token. The script extracts the JWT token from the JSON response and appends it as a Bearer token in the authorization header of our API requests.

```java
String token = RestAssured.given()
    .formParam("grant_type", "client_credentials")
    .post(tokenUrl)
    .jsonPath().getString("access_token");

RestAssured.given()
    .header("Authorization", "Bearer " + token)
    .get(apiUrl);
```

I test security constraints, verifying that calling the API with an expired token returns a 401 Unauthorized code, and calling it with a token lacking the required scope returns a 403 Forbidden code. This validation ensures that our microservices protect sensitive financial and patient data.

---

### 21. How do you configure Selenium Grid and BrowserStack to perform cross-browser validation?
Cross-browser validation ensures that our web applications render and function consistently across different browsers (Chrome, Firefox, Safari, Edge) and operating systems. To automate this at scale, we configure our test runners to run on distributed execution grids, such as a self-hosted **Selenium Grid** or cloud-native platforms like **BrowserStack**.

I configure our **TestNG** suite XML files to pass the target browser and platform parameters to our Java test classes. In our base test class, I write logic to instantiate a `RemoteWebDriver` instead of a local driver, passing the target browser configuration as a `DesiredCapabilities` object to the grid hub or BrowserStack API endpoint.

I manage the Selenium Grid containers using Docker Compose, spinning up worker nodes for Chrome and Firefox. For mobile browser validation, I configure the capabilities to target specific iOS and Android devices on BrowserStack. This grid configuration allows us to run our UI regression suites in parallel across multiple browser environments, ensuring cross-browser compatibility.

---

### 22. What is your approach to managing test data for complex transactional banking and healthcare workflows?
Managing test data is a critical challenge in QA automation, as tests require specific data states (such as active accounts, valid policies, or pending claims) to run successfully. If test data is static or shared across concurrent runs, tests will interfere with each other, causing false failures.

I design our frameworks to use a combination of dynamic test data generation and database cleanup scripts. Before running a test scenario, I write API calls (using **REST Assured**) or database insert scripts (using **SQL** queries) to create the required test entities dynamically, ensuring each test execution has its own data set.

After the test completes, I run teardown scripts to delete or archive the created records, keeping our test databases clean. For read-only configurations, I query our database using parameterized SQL scripts to locate matching records that fit our test constraints, preventing data hardcoding and ensuring test stability.

---

### 25. How do you perform JSON Schema validation in REST Assured to verify API contracts?
JSON Schema validation is an automated check that compares the structure of an API response payload against a predefined JSON schema, verifying that the data fields, types, and constraints conform to our API contract. This validation prevents integration failures caused by schema changes in microservices.

I write these contract validations in **REST Assured** using the schema validator library. First, I define the target schema file (.json) based on our API specifications and save it to our project's resource directory. In our Java test class, I configure the validation check using the `matchesJsonSchemaInClasspath` matcher.

```java
RestAssured.given()
    .get("/api/account/123")
    .then()
    .assertThat()
    .body(matchesJsonSchemaInClasspath("schemas/account-schema.json"));
```

This check verifies that the response contains all required fields, that variables are in the correct data types, and that constraints (such as minimum string lengths or formatting rules) are met. If a developer modifies an API payload, this validation will flag the contract violation immediately, preventing staging issues.

---

### 26. The JD mentions a focus on CP-DP interaction and workflows. How do you validate communications between Control Path (CP) and Data Path (DP) in microservices?
In complex microservice architectures, the Control Path (CP) manages configuration, routing, and access rules, while the Data Path (DP) handles the high-throughput processing and transmission of user transaction payloads. Validating the interaction between these two paths requires testing that configuration changes in the CP are correctly applied to the DP.

I validate this interaction by designing automated integration tests that target both paths. First, I send API requests to our CP endpoints to modify a configuration rule (for example, updating a transaction limit policy). I write **REST Assured** scripts to verify that the CP database (such as PostgreSQL) updates correctly and that the event is published to our message brokers (like **Kafka**).

Next, I send a transaction request through the DP. I verify that the DP applies the new configuration rule, checking if it blocks a transaction that exceeds the updated limit. I run SQL scripts to verify that the transactional records are logged correctly, validating the workflow end-to-end and ensuring that the control and data paths remain synchronized.

---

### 27. Describe a time when a test automation project failed to deliver expected results. What lessons did you learn?
At the beginning of my career, our team attempted to automate over ninety percent of our web application's UI scenarios using Selenium, including complex multi-step user registrations and reporting views. We built a large test suite, but it suffered from high execution times and frequent false failures due to minor UI changes, requiring significant maintenance effort.

I realized that automating everything at the UI layer was an unsustainable approach. I learned the principle of the testing pyramid: we must focus our automation efforts on fast, stable API and integration tests, reserving UI automation for critical user journeys and end-to-end workflows. This experience taught me to "nail the basics" before building advanced suites.

I refactored our testing strategy, migrating sixty percent of our validations to **REST Assured** API tests and using Selenium only for core browser flows. This migration reduced our runtime and maintenance overhead. I carry this lesson to Oracle Health, ensuring we build balanced testing strategies that deliver reliable quality feedback.

---

### 28. Explain the differences between implicit, explicit, and fluent waits in Selenium. How does Playwright handle auto-waiting?
Managing element synchronization is critical to prevent flaky test failures in UI automation, as web elements can load at different speeds due to network latencies. In **Selenium WebDriver**, we use wait strategies to synchronize our scripts:
- **Implicit Wait:** Sets a global timeout for the driver instance to wait for elements to appear in the DOM before throwing a `NoSuchElementException`. It is simple but applies to all lookups.
- **Explicit Wait:** Configures the driver to wait for a specific condition (such as visibility or clickability) on a specific element, which is highly targeted and robust.
- **Fluent Wait:** Defines the maximum timeout, the polling interval, and specific exceptions to ignore (such as `NoSuchElementException`) during the element search loop.

**Playwright** handles synchronization using auto-waiting. Before performing any action on an element (such as a click or type), Playwright automatically checks if the element is visible, enabled, stable (not animating), and attached to the DOM. This auto-waiting architecture eliminates the need for manual wait statements, reducing flaky test failures and making scripts cleaner.

---

### 29. How do you use TestNG and Maven test reports to communicate quality metrics to project stakeholders?
Communicating test execution results to project managers and business stakeholders is essential to confirm release readiness. I configure our automation frameworks to generate detailed HTML and XML reports using **TestNG** and **Maven** test runners, integrating them with our build pipelines.

I use TestNG listeners to capture test events, logging pass rates, execution runtimes, and stack traces. I configure Maven plugins (such as Maven Surefire or Extent Reports) to generate visual dashboards that display test execution summaries. If a test fails, the framework captures a screenshot and embeds it in the HTML report.

I publish these reports to our test management dashboards in **Azure DevOps** or **Jira** using Xray. This integration allows stakeholders to see our test coverage, pass/fail trends, and open defects. By providing clear, visual quality metrics, I help our cross-functional team make data-driven release decisions, demonstrating pride in my work.

---

### 30. Describe your experience testing mobile applications using Appium or Android Studio/Xcode Emulators.
Mobile application testing requires validating UI layouts, touch gestures, and API integrations across different device models and operating systems. I use **Appium** in Java to automate mobile test cases, configuring capabilities to target mobile browsers and native applications.

I use **Android Studio** emulators and **Xcode** simulators to run tests in local environments during development. I locate mobile UI elements using Appium Inspector, selecting resource IDs or accessibility labels. I write automated scripts to validate mobile workflows (such as user logins and forms), using TestNG to manage assertions.

For cloud-based mobile testing, I integrate our frameworks with platforms like BrowserStack or Kobiton. This integration allows us to execute our Appium suites in parallel across real iOS and Android devices, verifying that our applications render and function correctly, which is critical to ensure mobile app stability for Oracle Health's users.

---

## Part 2: Top 10 Behavioral Questions & Answers

### 31. Put Customers First: Tell me about a time you’ve had to prioritize your customers’ needs. What was the situation and how did you resolve it?
At **PNC Bank**, we were preparing to deploy a new version of our HUB banking dashboard, which included updated transfer and inbox workflows. Two days before the biweekly release, our QA team completed our automated testing runs, but I noticed that our mobile browser rendering was slightly misaligned on older iOS devices. While the application was functionally correct, the alignment issue made the transfer button hard to locate. The product team proposed proceeding with the release and patching the alignment later, as the functional API tests passed.

I disagreed with this approach. I explained to the product manager that launching a financial dashboard with rendering issues would frustrate our customers, leading to support calls. I prioritized the customer's experience and took immediate action. I set up a dedicated test session using BrowserStack, reproduced the rendering bug, and identified that a CSS media query in our UI layout was causing the misalignment.

I worked with our frontend developer to patch the CSS rules, updated our automated Selenium regression scripts to include responsive design validation, and verified that the dashboard rendered correctly across all mobile models. The release was deployed on schedule with the fix in place. This project demonstrated my commitment to customer-focused quality, ensuring that our software is both functional and easy for customers to use.

---

### 32. Act Now, Iterate: Describe a legacy manual testing process that you simplified by acting quickly and iterating over time.
When I joined **PNC Bank**, our regression testing for our multi-account transfer portal was entirely manual. Analysts spent over 8 hours every sprint manually logging into test accounts, entering transfer details, and checking transactional tables. This manual process was slow and delayed our staging releases. I decided to act quickly to simplify the process.

For our first iteration, I wrote a lightweight Java script using **Selenium WebDriver** to automate the login and transfer data entry steps, which reduced manual testing time by half. Once this baseline script proved reliable, I expanded the automation in a second iteration, integrating BDD Cucumber feature files to allow business analysts to review our test scenarios.

For the final iteration, I added **REST Assured** API validations to verify the transactional outputs, completely eliminating the manual database verification. This iterative development reduced our regression runtime from 8 hours to 3 hours. By acting quickly and continuously refining our automation framework, I simplified our release verification, demonstrating the value of iterative improvement.

---

### 33. Nail the Basics: Describe how you resolved a persistent automation failure by focusing on coding fundamentals.
At **Liberty Mutual**, our automated policy regression pipeline was experiencing intermittent failures, with several **Selenium** tests failing due to element synchronization errors. The previous approach was to add thread sleeps (`Thread.sleep()`) throughout the scripts. This temporary fix made the tests slow and did not solve the root issue, as tests continued to fail during network latencies.

I resolved the issue by refactoring our synchronization logic, focusing on coding fundamentals. I audited our test code and replaced all thread sleeps with targeted **Explicit Waits**, configuring the driver to wait for specific conditions (such as visibility or clickability) on specific elements before executing actions.

I also optimized our element locators. I replaced fragile, absolute XPath queries with unique ID and CSS selectors, which accelerated element search times. This refactoring stabilized our TestNG automation suites, reducing our regression execution runtime from 10 hours to 4 hours and eliminating flaky failures. This project showed that nailing coding basics is essential to build reliable automation systems.

---

### 34. Expect and Embrace Change: Tell me about a time when project priorities changed quickly during a release cycle. How did you adapt?
During a monthly health insurance release at **Molina Healthcare**, our product team decided to pivot and modify our member enrollment workflow to meet a new regulatory requirement, just three days before our scheduled deployment. This late pivot rendered our existing Playwright automation scripts obsolete, and we had to re-validate the entire enrollment pipeline under a tight deadline.

I embraced the change. I immediately paused our current testing activities, met with the business analysts to review the updated requirements, and mapped out a revised test plan. I identified which **Playwright** scenarios needed modification and updated our page object models to reflect the new UI steps.

I worked with our database team to update our SQL verification scripts, ensuring we validated the new member enrollment fields correctly. We ran our updated Playwright suite in our Docker test containers, resolved three deployment bugs, and validated the release on schedule. This experience reinforced my ability to remain adaptable, align quickly with new priorities, and deliver quality results.

---

### 35. Innovate Together: Tell me about a time you collaborated with a cross-functional team to solve a complex integration bug.
At **Liberty Mutual**, during the deployment of our claims processing microservices, our integration testing failed because our claims API was returning unexpected data formatting errors when connecting to our legacy policy database. The QA team and the backend developers were struggling to isolate the root cause, as the services passed their unit tests in isolation.

I organized a joint debugging session with the backend developer, database administrator, and business analyst. I wrote **REST Assured** scripts to capture the raw JSON payloads and executed database validations using **SQL** to trace the records. We discovered that a data type mismatch in our claims database was truncating policy numbers, causing the API integration to fail.

We worked together to resolve the issue: the developer patched the API serialization code, the database administrator updated the staging tables, and I ran our TestNG validation scripts to confirm the integration was successful. This collaboration solved the bug, reduced our release risk, and demonstrated how working together drives innovation.

---

### 36. Take Risks, Remain Calm: Describe a high-pressure production outage you experienced and how you resolved it.
During a biweekly release deployment at **PNC Bank**, our transaction gateway experienced a critical failure immediately after go-live, with customers unable to approve transfers, affecting our daily transaction activity. The release team was under high pressure, and there was tension. I remained calm, accessed our logs, and joined the incident bridge.

I ran our automated **Postman** API collections against the production endpoints, isolating the failure to our authentication service. The logs showed that the service was returning 401 Unauthorized errors because a security configuration key was missing from our production environment file. I notified the release manager, and we rollbacked the deployment to the previous stable release.

I then worked with the DevOps team to patch the environment configuration and verified the fix in our staging environment using our Selenium regression suite. We redeployed the service successfully later that night. By remaining calm and executing a structured diagnostic plan, I helped restore service and protect our transactional integrity.

---

### 37. Own Without Ego: Tell me about a time you had to admit to a mistake in your testing or framework design.
At **Molina Healthcare**, I designed an automated testing pipeline using Azure DevOps that was configured to run our full Playwright regression suite on every code commit. While the system provided comprehensive quality feedback, it began blocking the developers' deployment pipelines because the full suite took over 5 hours to run, causing developers to wait for build verifications.

I admitted to the mistake during our retrospective, recognizing that configuring the full regression run on every commit was an inefficient design. I welcomed feedback from the development team and worked to optimize the pipeline architecture. I refactored the pipeline to split the regression suite into a lightweight smoke test run for code commits, scheduling the full suite to run nightly.

This adjustment reduced build verification times from 5 hours to 15 minutes, allowing developers to deploy code quickly while maintaining regression coverage. Admitting the design mistake allowed us to build a better, more efficient CI/CD workflow, demonstrating that owning our work without ego improves team productivity.

---

### 38. Earn Trust, Give Trust: Describe a situation where you had to delegate a critical automation task to a colleague.
During a monthly release cycle at **Liberty Mutual**, I was responsible for migrating our policy regression suite to a new Jenkins pipeline. At the same time, we had to validate a new set of claims API endpoints using REST Assured. Both tasks were critical to meet our release deadline, and I realized I could not complete both on my own.

I decided to delegate the REST Assured API validation task to a junior QA engineer on our team. I gave them trust, providing them with our API schemas and Postman collections, and walked them through our framework design. I trusted them to own the task, while making myself available to answer questions and review their code.

The junior engineer completed the API validations on time, identifying two integration defects before our deployment. I reviewed their test scripts and integrated them with our Jenkins pipeline. This delegation allowed us to meet our release deadline and helped the junior engineer grow their automation skills, strengthening trust within our team.

---

### 39. Take Pride in Your Work: How do you demonstrate excellence and attention to detail in your daily automation code?
Demonstrating excellence in test automation means writing clean, maintainable, and well-documented code, treating our test frameworks with the same high standards as production code. I avoid writing quick, hacky scripts that are fragile and hard to maintain. I structure my automation classes using clean coding standards.

I write modular, reusable methods in Java, using descriptive names for our test cases and page objects. I document our framework design, locators, and configuration steps in Confluence, ensuring the documentation is clear for new team members. I write comprehensive assertions for every test scenario, checking both database states and UI elements.

I also optimize our pipelines, configuring parallel execution and setting up clean test environments using Docker. This attention to detail ensures that our automation suites are fast, stable, and deliver accurate quality feedback. I take pride in the reliability of our frameworks, ensuring they support our team's release goals.

---

### 40. Challenge Ideas, Champion Execution: Tell me about a time you proposed a new testing tool or framework that improved quality.
At **Molina Healthcare**, the team was using Selenium for all our UI validation testing. However, our member enrollment portal used a complex single-page application architecture that suffered from frequent timing issues, causing our Selenium tests to fail. I proposed that we transition our enrollment testing suite to **Playwright**.

Some team members were hesitant to adopt a new framework, concerned about the learning curve. I championed the execution: I built a prototype Playwright suite covering ten enrollment scenarios, demonstrating that Playwright's auto-waiting and browser context isolation eliminated the timing issues and reduced test runtimes.

The team was convinced by the prototype results, and we migrated our enrollment suite to Playwright. This migration reduced our regression execution times from 12 hours to 5 hours, improving our release velocity and defect detection. By challenging the status quo and delivering a working solution, I improved our overall software quality.

---
