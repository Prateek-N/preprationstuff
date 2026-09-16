# -*- coding: utf-8 -*-
"""
Janaki Ashok Kumar - QA Automation 14-Day Roadmap (Days 5 - 9)
Covers:
Day 5: Cucumber BDD, Gherkin Syntax & Enterprise Step Definitions
Day 6: Modern Web Automation with Playwright (Java & TypeScript)
Day 7: REST API Automation with REST Assured (Core HTTP, CRUD & Assertions)
Day 8: Advanced REST Assured, JSON Schema Validation & OAuth 2.0 / JWT Security
Day 9: Database Testing, SQL Verification & Transactional Reconciliation
"""

days_part2 = [
    # =========================================================================
    # DAY 5: Cucumber BDD, Gherkin Syntax & Enterprise Step Definitions
    # =========================================================================
    {
        "day": 5,
        "title": "Day 5: Cucumber BDD, Gherkin Syntax & Enterprise Step Definitions",
        "theme": "Business-Readable Specs, PicoContainer DI & Scenario Outlines",
        "domain_focus": "60 Transfer, Template & Approval Scenarios (PNC Bank Context)",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: Core Architectural Theory",
                "topic": "BDD Philosophy, Gherkin Standards & Feature File Decomposition",
                "content": """### Behavior-Driven Development (BDD) in Enterprise Banking
BDD is not merely an automation syntax; it is a collaborative methodology designed to bridge the communication gap between business stakeholders (Product Owners, Business Analysts) and technical teams (Developers, QA Automation Engineers).

### Gherkin Syntax Rules & Best Practices:
1. **Declarative vs. Imperative Scenarios:** Write business-focused declarative scenarios rather than step-by-step UI instructions.
   - *Bad (Imperative):* `When I click on the input with id 'transfer-amt' and I type '500' and I click the button 'Submit'...`
   - *Good (Declarative):* `When the user submits a domestic wire transfer of $500 to account "ACC-9821"...`
2. **Scenario Outline & Examples:** Used for parameterized testing across diverse business conditions (e.g., verifying transfer limits across Standard, Business, and Corporate accounts).
3. **Data Tables:** Injecting tabular records into step definitions without cluttering the Gherkin narrative with repetitive Given statements."""
            },
            {
                "hour": 2,
                "label": "Hour 2: Production Code Lab",
                "topic": "State Sharing with PicoContainer & Gherkin Step Definitions",
                "content": """To avoid static state corruption during parallel Cucumber execution, we use **PicoContainer** to inject a shared `TestContext` across step definition classes.

```gherkin
# src/test/resources/features/fund_transfers.feature
@regression @banking @transfers
Feature: Commercial Wire Transfer and Approval Workflows
  As a PNC corporate client
  I want to submit and approve high-value wire transfers
  So that operational treasury transactions are processed securely

  Background:
    Given the corporate user is authenticated with "CORPORATE_ADMIN" credentials
    And the source account "ACC-CORP-01" has an active balance of $500,000

  @smoke @dual-approval
  Scenario Outline: Verify dual-approval threshold for high-value domestic wires
    When the user initiates a domestic wire of <amount> to beneficiary "<beneficiary>"
    Then the system should assign transaction status "<expected_status>"
    And an approval task should be dispatched to the "<required_approver>" inbox

    Examples:
      | amount   | beneficiary     | expected_status    | required_approver |
      | 25000.00 | Apex Logistics  | AUTO_APPROVED      | NONE              |
      | 150000.00| Global Freight  | PENDING_APPROVAL   | SENIOR_TREASURER  |
      | 600000.00| Titan Holdings  | REJECTED_LIMIT     | SYSTEM_OVERRIDE   |
```

```java
package com.pnc.qa.stepdefs;

import io.cucumber.java.en.*;
import org.testng.Assert;

public class TransferSteps {

    // TestContext injected via PicoContainer
    private final TestContext context;

    public TransferSteps(TestContext context) {
        this.context = context;
    }

    @When("the user initiates a domestic wire of {double} to beneficiary {string}")
    public void initiateWire(double amount, String beneficiary) {
        context.getTransferPage().initiateTransfer(amount, beneficiary);
        context.setTransferAmount(amount);
    }

    @Then("the system should assign transaction status {string}")
    public void verifyStatus(String expectedStatus) {
        String actualStatus = context.getTransferPage().getTransactionStatus();
        Assert.assertEquals(actualStatus, expectedStatus, "Transaction status mismatch!");
    }
}
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Enterprise Edge Cases & Flaky Test Elimination",
                "topic": "PicoContainer Lifecycle, Hooks & Test Runner Configuration",
                "content": """### Managing State in Enterprise Cucumber Frameworks:
1. **Never Use Static Variables for State Sharing:** Storing `public static String transactionId;` fails when running 4 parallel Cucumber threads in TestNG, as threads overwrite each other's IDs. PicoContainer creates a brand new instance of `TestContext` for every individual scenario and disposes of it at scenario completion.
2. **Tagged Hooks (`@Before` / `@After`):** Run browser initialization only for `@ui` tags, while `@api` tagged scenarios bypass browser setup entirely, executing 10x faster.
3. **Allure & Cucumber Reporting Integration:** Capturing screenshot bytes on scenario failure inside `@After` hook:
   ```java
   @After
   public void tearDown(Scenario scenario) {
       if (scenario.isFailed()) {
           byte[] screenshot = ((TakesScreenshot) DriverManager.getDriver()).getScreenshotAs(OutputType.BYTES);
           scenario.attach(screenshot, "image/png", "Failure_Screenshot");
       }
       DriverManager.quitDriver();
   }
   ```"""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "State Management with PicoContainer in Parallel Cucumber BDD Suites",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Bridging Product Owners and QA on Multi-Tier Approvals at PNC Bank",
                "content": """**Situation:** At **PNC Bank**, corporate treasury clients frequently reported discrepancies regarding when dual-authorization approval was triggered for wire transfers. The requirements were buried across 50-page business specifications, leading to misinterpretation between developers and QA engineers.

**Task:** I was tasked with establishing a unified, living documentation testing framework that clearly defined all 60 transfer, template, and approval inbox scenarios for cross-functional alignment.

**Action:** I organized Three Amigos workshops with our Product Owner, Lead Backend Architect, and Senior Business Analyst. I translated ambiguous business rules into structured **Gherkin feature files** utilizing Scenario Outlines with comprehensive Examples tables covering transaction amounts, currencies, user entitlement tiers, and cutoff times. I then implemented the underlying Java step definitions using **Cucumber BDD** and **Selenium WebDriver**, utilizing **PicoContainer** to cleanly pass transaction reference IDs between the transfer creation steps and the subsequent approval inbox verification steps.

**Result:** The BDD feature files became the definitive living documentation for the entire department. Defect leakage into UAT fell to zero, and we successfully validated all 60 complex scenarios, ensuring rock-solid stability for our **$2M+ daily transaction volume**."""
            }
        ],
        "master_qa": {
            "question": "How do you maintain shared state between Cucumber step definitions without static variables, and how do you organize enterprise feature files for complex financial workflows?",
            "answer": """In large-scale enterprise test automation frameworks utilizing **Cucumber BDD**, maintaining state across multiple step definition classes without compromising thread safety during parallel execution is one of the most critical architectural challenges. In complex domain workflows—such as **PNC Bank**'s HUB banking portal, where a user initiates a transfer in `TransferSteps.java`, verifies transactional ledger entries in `AccountSteps.java`, and completes a dual-authorization sign-off in `ApprovalSteps.java`—data such as transaction IDs, confirmation tokens, and dynamic customer balances must be seamlessly passed between steps.

A common anti-pattern in naive automation suites is declaring static global variables (e.g., `public static String txnReferenceId`). When tests are executed in parallel across multiple threads via **TestNG** or **Maven Surefire**, all threads share the same JVM static memory space. Thread A will overwrite Thread B's transaction reference, corrupting assertions and triggering catastrophic flaky test cascades.

The industry-standard architectural solution is to implement **Dependency Injection (DI)** using **PicoContainer** (or alternatively Spring or Guice). PicoContainer is the recommended DI container for Cucumber because it requires zero configuration files or complex annotations. To implement this, we create a centralized, thread-safe state container class, typically named `TestContext`. The `TestContext` class encapsulates all shared scenario state: Page Object instances, API response objects, authentication tokens, and transactional payloads.

Each step definition class declares `TestContext` as a constructor parameter. When Cucumber instantiates step definition classes for an active scenario, PicoContainer automatically scans the constructor signatures, creates a single instance of `TestContext` dedicated solely to that scenario, and injects that identical instance across all step definition classes involved in that scenario's execution. Crucially, when the scenario concludes, PicoContainer tears down and garbage-collects the scenario's `TestContext` instance. When running tests in parallel, each executing thread operates within its own completely isolated PicoContainer scope, ensuring 100% thread safety and zero cross-test data pollution.

In terms of organizing enterprise feature files for complex financial workflows, I adopt a domain-driven package hierarchy under `src/test/resources/features/`. Scenarios are partitioned into high-level domains (e.g., `transfers/`, `approvals/`, `templates/`, `reconciliation/`). Every feature file adheres to strict declarative Gherkin standards, leveraging the `Background` keyword for recurring authentication steps, and using `Scenario Outline` with well-defined `Examples` tables for boundary value testing. Furthermore, we enforce strict tagging conventions (`@smoke`, `@regression`, `@dual-approval`, `@regulatory`) that allow our CI/CD pipelines in **Jenkins** and **Azure DevOps** to dynamically filter and execute targeted test suites on demand."""
        }
    },

    # =========================================================================
    # DAY 6: Modern Web Automation with Playwright (Java & TypeScript)
    # =========================================================================
    {
        "day": 6,
        "title": "Day 6: Modern Web Automation with Playwright (Java & TypeScript)",
        "theme": "Event-Driven Automation, BrowserContext Isolation & Network Mocking",
        "domain_focus": "180 Member Enrollment Scenarios (Molina Healthcare Context)",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: Core Architectural Theory",
                "topic": "Playwright Architecture vs. Selenium WebDriver & The Event-Driven Loop",
                "content": """### Architectural Comparison: Playwright vs. Selenium
- **Communication Protocol:** Selenium communicates via HTTP request-response cycles over the W3C WebDriver standard. Playwright establishes a single, persistent **WebSocket** connection directly to the browser binary. Commands and DOM events stream bi-directionally with near-zero network latency.
- **Browser Process Architecture:** Playwright introduces the concept of **BrowserContext**. A single browser process can host hundreds of completely isolated incognito BrowserContexts in milliseconds, eliminating the heavy OS process overhead of opening and closing whole browser windows.
- **Built-in Auto-Waiting:** Playwright automatically waits for elements to be actionable (attached to DOM, visible, stable, receiving pointer events, enabled) before performing clicks or typing, eliminating 90% of explicit wait boilerplate."""
            },
            {
                "hour": 2,
                "label": "Hour 2: Production Code Lab",
                "topic": "Playwright Java Automation with Network Interception & Routing",
                "content": """At **Molina Healthcare**, member enrollment workflows depend on external third-party eligibility verification APIs. Using Playwright's `Route` API, we mock slow external services for deterministic testing:

```java
package com.molina.qa.tests;

import com.microsoft.playwright.*;
import com.microsoft.playwright.options.AriaRole;
import org.testng.annotations.*;
import static org.testng.Assert.*;

public class MemberEnrollmentPlaywrightTest {

    private Playwright playwright;
    private Browser browser;
    private BrowserContext context;
    private Page page;

    @BeforeClass
    public void setupBrowser() {
        playwright = Playwright.create();
        browser = playwright.chromium().launch(new BrowserType.LaunchOptions().setHeadless(true));
    }

    @BeforeMethod
    public void createContext() {
        // Fast, isolated browser context with video and tracing enabled
        context = browser.newContext(new Browser.NewContextOptions()
                .setViewportSize(1920, 1080)
                .setRecordVideoDir(java.nio.file.Paths.get("target/videos/")));
        page = context.newPage();
    }

    @Test
    public void testMemberEnrollmentWithMockedEligibilityService() {
        // Intercept backend eligibility verification API and mock instant positive response
        page.route("**/api/v1/eligibility/verify/**", route -> {
            String mockResponseBody = "{\"status\": \"ACTIVE\", \"planType\": \"MEDICAID_PREMIUM\", \"verified\": true}";
            route.fulfill(new Route.FulfillOptions()
                    .setStatus(200)
                    .setContentType("application/json")
                    .setBody(mockResponseBody));
        });

        page.navigate("https://portal.molinahealthcare.com/enrollment");

        // Native Playwright locators using accessibility roles
        page.getByRole(AriaRole.TEXTBOX, new Page.GetByRoleOptions().setName("Member First Name")).fill("Janaki");
        page.getByRole(AriaRole.TEXTBOX, new Page.GetByRoleOptions().setName("Member Last Name")).fill("Kumar");
        page.getByRole(AriaRole.TEXTBOX, new Page.GetByRoleOptions().setName("Social Security Number")).fill("999-00-1234");
        
        page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Verify Eligibility")).click();

        // Assert eligibility badge updates instantly from mocked response
        Locator statusBadge = page.locator(".eligibility-status-badge");
        assertEquals(statusBadge.innerText(), "ACTIVE - MEDICAID PREMIUM");
    }

    @AfterMethod
    public void tearDown() {
        context.close(); // Automatically flushes video and traces
    }

    @AfterClass
    public void closeAll() {
        browser.close();
        playwright.close();
    }
}
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Enterprise Edge Cases & Flaky Test Elimination",
                "topic": "Playwright Trace Viewer & Multi-Context Isolation",
                "content": """### Mastering the Playwright Trace Viewer:
When an automated test fails on a remote Linux CI server, screenshots often fail to capture ephemeral DOM state. Playwright's **Trace Viewer** records:
1. Full DOM snapshots before, during, and after every action.
2. Complete network requests, responses, timings, and payloads.
3. Console logs, browser errors, and visual execution filmstrips.
- **Configuration:** Start tracing in `@BeforeMethod` with `context.tracing().start(new Tracing.StartOptions().setScreenshots(true).setSnapshots(true));` and stop on failure with `context.tracing().stop(new Tracing.StopOptions().setPath(Paths.get("trace.zip")));`."""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "Playwright vs. Selenium WebDriver: Architectural Deep Dive",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Slashing Healthcare Enrollment Regressions from 12 hrs to 5 hrs",
                "content": """**Situation:** At **Molina Healthcare**, the member enrollment portal supported 50,000+ active member records. Our legacy Selenium test suite covering 180 enrollment scenarios took **12 hours** to execute. The suite suffered from frequent test failures caused by slow third-party state Medicaid eligibility APIs that frequently timed out in our staging environment.

**Task:** I was tasked with modernizing our UI test automation architecture to reduce execution time by more than 50% and isolate our testing pipeline from third-party vendor downtime.

**Action:** I spearheaded the adoption of **Playwright** for our member enrollment automation. I leveraged Playwright's lightweight **BrowserContext** model to spin up isolated testing sessions in under 50 milliseconds. To eliminate third-party test blockers, I used Playwright's network routing API (`page.route()`) to mock external state Medicaid eligibility responses for functional UI tests, reserving live network calls for dedicated integration test suites. I configured multi-threaded parallel execution across 6 workers on our **Azure DevOps** build agents and integrated Playwright's Trace Viewer for immediate visual debugging of failures.

**Result:** The regression execution time dropped from **12 hours down to 5 hours** (a 58% reduction). Third-party related test flakiness dropped to 0%, and our team achieved reliable monthly release sign-offs supporting over 50K+ member records."""
            }
        ],
        "master_qa": {
            "question": "Compare Playwright with Selenium WebDriver in terms of architecture, execution speed, flaky test handling, and network interception. Why did you choose Playwright at Molina Healthcare?",
            "answer": """When comparing **Playwright** and **Selenium WebDriver**, the fundamental differences emerge from their underlying communication architecture, process management models, and design philosophies regarding browser automation. 

In **Selenium WebDriver**, the architecture relies on the W3C WebDriver standard, where the test script sends individual HTTP request-response commands over a TCP port to an intermediary browser driver (such as ChromeDriver or GeckoDriver), which translates those commands into browser actions. While W3C standardization ensures wide cross-browser compatibility across legacy and modern platforms, the stateless HTTP request-response paradigm introduces noticeable latency for every single interaction and requires explicit polling loops to verify element readiness.

In contrast, **Playwright** (developed by Microsoft) bypasses external driver executables and establishes a single, persistent **WebSocket** connection directly to the browser engine (Chromium, WebKit, Firefox). All control commands, DOM event notifications, and network responses stream bi-directionally in real time. This architectural difference provides Playwright with massive performance advantages, particularly in test environment setup. In Selenium, spinning up a clean test state usually requires launching a brand new OS browser process, which takes 2 to 4 seconds. Playwright introduces **BrowserContexts**—lightweight, incognito browser instances that are fully isolated (with separate cookies, local storage, and cache) but share the same running browser binary. Spinning up a new BrowserContext takes less than 50 milliseconds, allowing hundreds of tests to run in total isolation with minimal memory footprint.

Regarding **flaky test handling**, Playwright features built-in, out-of-the-box **auto-waiting**. Before performing any action (such as a click or fill), Playwright automatically performs a battery of actionability checks: verifying that the target element is attached to the DOM, visible, stable (not animating), enabled, and not covered by another overlaying element. This completely eliminates the need for boilerplate `WebDriverWait` and `ExpectedConditions` code that dominates Selenium frameworks.

Furthermore, Playwright provides native, first-class **network interception and mocking** capabilities (`page.route()`), allowing engineers to intercept HTTP calls, modify headers, and stub out backend microservices or third-party APIs. At **Molina Healthcare**, our member enrollment portal (supporting 50K+ member records) was tightly coupled with third-party state Medicaid eligibility verification services that suffered from frequent latency spikes and weekend maintenance downtime. In Selenium, mocking these external dependencies required spinning up complex HTTP proxy servers like BrowserMob Proxy. With Playwright, I intercepted backend eligibility requests directly in code, returning deterministic JSON mock responses in milliseconds. This eliminated environmental flakiness, reduced our regression execution from 12 hours to 5 hours, and made Playwright the clear strategic choice for modern enterprise testing."""
        }
    },

    # =========================================================================
    # DAY 7: REST API Automation with REST Assured (Core HTTP & BDD Syntax)
    # =========================================================================
    {
        "day": 7,
        "title": "Day 7: REST API Automation with REST Assured (Core HTTP, CRUD & Assertions)",
        "theme": "Backend Validation, Given-When-Then BDD & Spec Builders",
        "domain_focus": "90 Transfer & Notification APIs (PNC Bank Context)",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: Core Architectural Theory",
                "topic": "HTTP Protocol Mechanics, Microservice Architectures & REST Principles",
                "content": """### HTTP Protocol Fundamentals for QA Automation Engineers:
1. **Idempotency & HTTP Verbs:**
   - `GET`: Safe, idempotent (retrieves data, never mutates state).
   - `POST`: Non-idempotent (creates new resource, returns `201 Created` with `Location` header).
   - `PUT`: Idempotent (replaces entire resource representation).
   - `PATCH`: Non-idempotent or idempotent (partial update of specific fields).
   - `DELETE`: Idempotent (removes resource, returns `204 No Content` or `200 OK`).
2. **HTTP Status Code Taxonomies in Financial APIs:**
   - `200 OK` vs. `201 Created` vs. `202 Accepted` (critical for async batch transfers at PNC).
   - `400 Bad Request` (payload syntax error), `401 Unauthorized` (missing/invalid token), `403 Forbidden` (valid token, insufficient RBAC permissions), `404 Not Found`, `409 Conflict` (duplicate idempotency key).
   - `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`."""
            },
            {
                "hour": 2,
                "label": "Hour 2: Production Code Lab",
                "topic": "REST Assured Framework Architecture with `RequestSpecBuilder`",
                "content": """At **PNC Bank**, our 90 automated transfer APIs share base URIs, authorization headers, content-types, and logging configurations. We centralize this using `RequestSpecBuilder`:

```java
package com.pnc.qa.api;

import io.restassured.builder.RequestSpecBuilder;
import io.restassured.builder.ResponseSpecBuilder;
import io.restassured.filter.log.LogDetail;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;
import io.restassured.specification.ResponseSpecification;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class AccountTransferApiTests {

    private RequestSpecification requestSpec;
    private ResponseSpecification responseSpec;

    @BeforeClass
    public void setupSpecifications() {
        requestSpec = new RequestSpecBuilder()
                .setBaseUri("https://api.pnc.com/banking/v2")
                .setContentType(ContentType.JSON)
                .addHeader("X-Channel-Id", "COMMERCIAL_WEB")
                .log(LogDetail.URI)
                .log(LogDetail.BODY)
                .build();

        responseSpec = new ResponseSpecBuilder()
                .expectContentType(ContentType.JSON)
                .log(LogDetail.STATUS)
                .build();
    }

    @Test
    public void testInitiateDomesticTransferSuccess() {
        String transferPayload = "{\n" +
                "  \"sourceAccount\": \"ACC-100293\",\n" +
                "  \"destinationAccount\": \"ACC-499201\",\n" +
                "  \"amount\": 15000.00,\n" +
                "  \"currency\": \"USD\",\n" +
                "  \"memo\": \"Vendor Q3 Invoice Settlement\"\n" +
                "}";

        Response response = given()
                .spec(requestSpec)
                .header("Authorization", "Bearer " + AuthManager.getAuthToken())
                .header("Idempotency-Key", "IDEMP-" + System.currentTimeMillis())
                .body(transferPayload)
        .when()
                .post("/transfers/domestic")
        .then()
                .spec(responseSpec)
                .statusCode(201)
                .body("status", equalTo("PENDING_APPROVAL"))
                .body("transferId", notNullValue())
                .body("amount", equalTo(15000.00f))
                .body("audit.channel", equalTo("COMMERCIAL_WEB"))
                .extract().response();

        String transferId = response.jsonPath().getString("transferId");
        System.out.println("Created Transfer Reference ID: " + transferId);
    }
}
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Enterprise Edge Cases & Flaky Test Elimination",
                "topic": "Validating Complex Nested JSON Arrays & JsonPath Expressions",
                "content": """### Validating Deeply Nested JSON Payloads:
Financial API responses often return paginated arrays with nested objects. Use GPath expressions inside **JsonPath**:
- Extracting all transfer amounts greater than $10,000:
  `List<Float> highValueAmounts = response.jsonPath().getList("transfers.findAll { it.amount > 10000 }.amount");`
- Verifying all items in an array satisfy a condition:
  `response.then().body("transfers.status", everyItem(isOneOf("COMPLETED", "SETTLED")));`
- Checking array size:
  `response.then().body("transfers.size()", greaterThan(0));`"""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "Designing a Reusable API Test Automation Framework with REST Assured",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Catching Critical Integration Defects Across 90 APIs at PNC Bank",
                "content": """**Situation:** At **PNC Bank**, the core banking development team was refactoring backend microservices responsible for account transfers and automated SMS/email customer notifications. During sprint integration testing, manual QA had not yet verified the updated notification payloads.

**Task:** As QA Automation Engineer, I needed to automate regression testing across 90 transfer and notification APIs to intercept breaking contracts before code was deployed into production.

**Action:** I constructed a comprehensive API test suite using **REST Assured** integrated into our **TestNG** framework. I implemented a robust `RequestSpecBuilder` utility enforcing standard enterprise headers, authentication tokens, and payload formats. Within the test suite, I chained dependent API calls: first executing a fund transfer API, capturing the returned `transferId`, and immediately querying the notification microservice endpoint to assert that an outbound message event was queued with the correct recipient phone number, masked account digits, and dollar amount.

**Result:** My automated API suite caught 8 high-severity integration defects—including a defect where notification microservices dropped transfers initiated via mobile channels—prior to production rollout. This averted critical customer communication failures for our **$2M+ daily transaction operations**."""
            }
        ],
        "master_qa": {
            "question": "How do you design a reusable API automation framework with REST Assured using `RequestSpecBuilder`, `ResponseSpecBuilder`, and global logging filters?",
            "answer": """Designing a production-grade API test automation framework with **REST Assured** requires establishing clean structural abstractions that eliminate redundant code, enforce uniform security and header standards, and provide clear debugging telemetry for CI/CD pipelines. In enterprise banking environments like **PNC Bank**, where automated suites validate 90+ microservice endpoints spanning domestic transfers, wire approvals, and customer notification queues, building requests ad-hoc within individual test methods creates severe maintenance liabilities.

The architectural foundation of an enterprise REST Assured framework is built upon **RequestSpecification** and **ResponseSpecification** patterns, orchestrated via `RequestSpecBuilder` and `ResponseSpecBuilder`. In our framework, I create a centralized `ApiSpecificationFactory` class. The `RequestSpecBuilder` encapsulates global configuration properties: setting the environment base URI (`https://api.pnc.com`), setting default `ContentType.JSON`, attaching standard enterprise audit headers (such as `X-Correlation-ID`, `X-Channel-ID`, and dynamic `Idempotency-Key` headers), and registering global authentication filters. Similarly, `ResponseSpecBuilder` defines universal baseline assertions, such as verifying that the response content type matches application JSON and validating that response latencies remain within acceptable service level agreements (e.g., `expectResponseTime(lessThan(3000L))`).

To ensure total visibility during automated test failures without cluttering build logs with megabytes of sensitive financial data, I implement conditional logging filters. Rather than universally enabling `.log().all()`, which logs customer account details and authorization tokens during passing runs, I attach `RequestLoggingFilter.logRequestTo(PrintStream)` and configure `.log().ifValidationFails()`. This ensures that when a test asserts a `200 OK` but the backend returns a `500 Internal Server Error`, the entire HTTP request headers, body payload, query parameters, response headers, and response body are instantly printed to the console and captured within our **Allure** test report.

Furthermore, the framework employs an API client wrapper layer following the **Service Object Model**. Instead of writing raw REST Assured calls inside test classes, endpoints are encapsulated into service classes (e.g., `TransferApiService`, `NotificationApiService`). These service methods accept strongly typed Java POJO payloads and return strongly typed response objects or REST Assured `Response` instances. This complete separation of concerns ensures that if an API path or header schema changes, only a single service class method requires updates, leaving hundreds of automated regression tests completely untouched."""
        }
    },

    # =========================================================================
    # DAY 8: Advanced REST Assured, JSON Schema Validation & OAuth 2.0 / JWT
    # =========================================================================
    {
        "day": 8,
        "title": "Day 8: Advanced REST Assured, JSON Schema Validation & OAuth 2.0 / JWT Security",
        "theme": "POJO Serialization, Contract Testing & Enterprise Authentication",
        "domain_focus": "110 Policy & Claims APIs Security (Liberty Mutual Context)",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: Core Architectural Theory",
                "topic": "OAuth 2.0 Authorization Flows, JWT Claims & Schema Enforcement",
                "content": """### Enterprise Security Mechanics:
1. **OAuth 2.0 Client Credentials vs. Authorization Code:**
   - *Client Credentials:* Machine-to-machine authentication (microservice to microservice). Client ID + Client Secret exchanged directly at `/oauth/v2/token` for an access token.
   - *Authorization Code with PKCE:* User-delegated authentication. Involves browser redirect, authorization code issuance, and code exchange for JWT access token.
2. **JWT Structure (Header.Payload.Signature):**
   - Header: Algorithm (`RS256`, `HS256`) and Token Type (`JWT`).
   - Payload: Registered claims (`iss`, `exp`, `sub`, `iat`), and private claims (`roles: ["UNDERWRITER", "CLAIMS_ADJUSTER"]`, `policyId: "POL-98120"`).
   - Signature: Cryptographic hash verifying payload integrity.
3. **Contract Testing & JSON Schema Validation:**
   - Functional testing verifies values (e.g., `amount == 500`).
   - Schema validation verifies structure, types, mandatory fields, regex patterns, and constraints defined in standard **JSON Schema Draft-07** specifications."""
            },
            {
                "hour": 2,
                "label": "Hour 2: Production Code Lab",
                "topic": "JSON Schema Validation & Automated OAuth Token Management in REST Assured",
                "content": """At **Liberty Mutual**, validating 110 insurance policy APIs requires verifying both schema contract compliance and dynamic OAuth 2.0 token injection:

```java
package com.libertymutual.qa.api;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.module.jsv.JsonSchemaValidator;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import java.io.File;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

public class PolicySchemaAndSecurityTests {

    private static String accessToken;

    @BeforeClass
    public void retrieveOAuthToken() {
        // Obtain OAuth 2.0 JWT token via Client Credentials Flow
        accessToken = given()
                .contentType(ContentType.URLENC)
                .formParam("grant_type", "client_credentials")
                .formParam("client_id", "lm-qa-automation-client")
                .formParam("client_secret", "Secr3t_Token_982!")
                .formParam("scope", "policy:read policy:write claims:read")
        .when()
                .post("https://auth.libertymutual.com/oauth/v2/token")
        .then()
                .statusCode(200)
                .body("access_token", notNullValue())
                .extract().path("access_token");
    }

    @Test
    public void testPolicyDetailsJsonSchemaValidation() {
        // Validate policy details API against strict schema definition file in classpath
        given()
                .baseUri("https://api.libertymutual.com/insurance/v1")
                .header("Authorization", "Bearer " + accessToken)
                .header("Accept", "application/json")
        .when()
                .get("/policies/POL-2026-9901")
        .then()
                .statusCode(200)
                // Strict JSON Schema validation against policy-schema.json in src/test/resources/schemas/
                .body(JsonSchemaValidator.matchesJsonSchemaInClasspath("schemas/policy-schema.json"))
                .body("policyNumber", equalTo("POL-2026-9901"))
                .body("coverage.underwritingStatus", equalTo("APPROVED"));
    }
}
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Enterprise Edge Cases & Flaky Test Elimination",
                "topic": "POJO Modeling with Lombok & Jackson vs. Raw String Payloads",
                "content": """### Why Raw Strings in API Automation are Anti-Patterns:
Hardcoding JSON strings (`String body = "{\"name\": \"John\"}"`) creates brittle tests: escaping quotes is tedious, refactoring fields breaks tests silently, and dynamic mutation is messy.
- **Enterprise POJO Pattern:** Create strongly typed classes using **Lombok** (`@Data`, `@Builder`, `@NoArgsConstructor`, `@AllArgsConstructor`) and **Jackson** annotations (`@JsonProperty`, `@JsonIgnoreProperties(ignoreUnknown = true)`).
- **Dynamic Builder Usage:**
  ```java
  PolicyRequest request = PolicyRequest.builder()
          .policyType(PolicyType.COMMERCIAL_AUTO)
          .premiumAmount(1250.50)
          .effectiveDate(LocalDate.now().plusDays(1))
          .build();
  given().body(request)...
  ```"""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "OAuth 2.0 Token Automation & JSON Schema Validation in REST Assured",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Detecting Security RBAC Flaws Across 110 APIs at Liberty Mutual",
                "content": """**Situation:** At **Liberty Mutual**, our policy administration microservices were being migrated to a fine-grained Role-Based Access Control (**RBAC**) architecture using JWT tokens. During this migration, developers had to ensure that claims adjusters could not access or alter commercial policy underwriting limits.

**Task:** As the QA Automation Engineer responsible for testing 110 policy and claims APIs, I needed to design an automated security testing matrix to verify that authorization rules were enforced across every endpoint and that payload contracts matched schema specifications.

**Action:** I constructed an automated test suite combining **REST Assured** and **JSON Schema Validator**. I created an automated token factory capable of minting tokens for distinct user personas (`CLAIMS_ADJUSTER`, `UNDERWRITER`, `CUSTOMER_SERVICE`, and `ANONYMOUS`). I developed parameterized TestNG data-driven tests that executed every policy modification endpoint against all personas. When invoking underwriting endpoints with a `CLAIMS_ADJUSTER` token, the tests asserted a `403 Forbidden` status code with an explicit security error code, while `UNDERWRITER` tokens returned `200 OK` and conformed 100% to our classpath JSON Schema definitions.

**Result:** The automated security suite uncovered 3 critical authorization bypass defects where claims adjusters could modify policy premium limits. These were resolved prior to deployment, safeguarding sensitive insurance data across **25,000+ policy records**."""
            }
        ],
        "master_qa": {
            "question": "How do you automate testing for OAuth 2.0 secured REST APIs with JWT tokens, and how do you implement JSON Schema validation in REST Assured?",
            "answer": """Automating tests for enterprise APIs secured by **OAuth 2.0** and **JWT (JSON Web Tokens)** requires an automated, lifecycle-aware authentication mechanism integrated into **REST Assured**, coupled with rigorous contract verification via **JSON Schema Validation**. At **Liberty Mutual**, validating 110 policy and claims APIs supporting over 25,000 policy records demanded that tests dynamically authenticate against identity providers (such as Okta or Azure AD) and validate both functional responses and structural payload contracts.

To handle OAuth 2.0 authentication without manual token maintenance or flaky hardcoded credentials, I architect an automated **TokenManager** utility. Depending on the architecture, the TokenManager supports both the **Client Credentials Grant** (for service-to-service calls) and the **Resource Owner Password / Authorization Code flow** (for user persona testing). Prior to test execution, the TokenManager issues a `POST` request to the identity provider's token endpoint (`/oauth/v2/token`), passing encoded client credentials, requested scopes, and grant types. The returned response is parsed using REST Assured's `JsonPath` to extract the `access_token` and `expires_in` values. To optimize performance across hundreds of test executions, the TokenManager caches this token in memory and tracks its expiration timestamp, refreshing it proactively only when expired. In the API framework's `RequestSpecification`, this token is automatically appended as a standard `Authorization: Bearer <token>` header.

Beyond functional field-by-field assertions, enterprise stability requires **JSON Schema Validation** to guarantee that backend API contracts adhere strictly to agreed OpenAPI/Swagger specifications. Individual assertions (such as asserting `status == 200`) frequently miss breaking backend changes, such as a field name being renamed, a string being returned where an integer is expected, or an optional array being removed.

To implement schema validation, we export the standardized JSON Schema (Draft-07 compliant) into our project repository under `src/test/resources/schemas/`. In our REST Assured validation chain, we utilize the `JsonSchemaValidator.matchesJsonSchemaInClasspath()` matcher from the `io.rest-assured:json-schema-validator` library. In a single assertion line: `.then().assertThat().body(JsonSchemaValidator.matchesJsonSchemaInClasspath("schemas/policy-response-schema.json"))`, REST Assured validates every single field's data type, checks minimum/maximum numeric constraints, evaluates regular expression formats (such as ISO date formats or policy GUID patterns), and verifies that all mandatory fields are present. This dual approach—automated OAuth token lifecycle management paired with comprehensive JSON schema validation—ensures that both API security perimeters and contract integrity are continuously enforced in our CI/CD pipelines."""
        }
    },

    # =========================================================================
    # DAY 9: Database Testing, SQL Verification & Transactional Reconciliation
    # =========================================================================
    {
        "day": 9,
        "title": "Day 9: Database Testing, SQL Verification & Transactional Reconciliation",
        "theme": "Backend Data Integrity, Complex Joins & Financial Reconciliation",
        "domain_focus": "85 Reconciliation Scenarios Across Oracle & SQL Server",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: Core Architectural Theory",
                "topic": "Database Testing Mechanics: ACID Properties & Data Reconciliation",
                "content": """### The Role of Database Automation in Regulated Industries:
Testing the UI or API alone is insufficient. In banking (**PNC Bank**) and insurance (**Liberty Mutual**), UI operations must translate into mathematically sound, ACID-compliant database transactions.
- **Atomicity:** A multi-account transfer must debit Account A and credit Account B within a single database transaction. If one fails, the entire transaction must roll back.
- **Consistency:** Database constraints (Foreign Keys, Check Constraints, Unique Indexes) must never be violated.
- **Isolation:** Concurrent transfers executing in parallel must not cause dirty reads or phantom records.
- **Durability:** Committed transactions must survive service restarts.

### Database Reconciliation Strategy:
1. Trigger action via UI or REST Assured API.
2. Capture transaction reference ID.
3. Query the transactional database via **JDBC** (`SELECT ... FROM transfers WHERE txn_ref = ?`).
4. Validate ledger entries, debit/credit parity, balance calculations, and audit logs."""
            },
            {
                "hour": 2,
                "label": "Hour 2: Production Code Lab",
                "topic": "Thread-Safe JDBC Database Utility with HikariCP Connection Pooling",
                "content": """Creating raw JDBC connections per test causes connection starvation on Oracle/PostgreSQL databases. We use **HikariCP** connection pooling:

```java
package com.pnc.qa.database;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.*;

public class DatabaseManager {

    private static HikariDataSource dataSource;

    static {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:oracle:thin:@//oracle-db.pnc.com:1521/FINPNC");
        config.setUsername("QA_AUTOMATION_USER");
        config.setPassword("SecurePncPass_982!");
        config.setMaximumPoolSize(5); // Optimized for 4 parallel test threads
        config.setMinimumIdle(2);
        config.setIdleTimeout(30000);
        config.setConnectionTimeout(10000);
        dataSource = new HikariDataSource(config);
    }

    public static List<Map<String, Object>> executeQuery(String sql, Object... params) {
        List<Map<String, Object>> rows = new ArrayList<>();
        try (Connection conn = dataSource.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            for (int i = 0; i < params.length; i++) {
                stmt.setObject(i + 1, params[i]);
            }

            try (ResultSet rs = stmt.executeQuery()) {
                int columnCount = rs.getMetaData().getColumnCount();
                while (rs.next()) {
                    Map<String, Object> row = new HashMap<>();
                    for (int col = 1; col <= columnCount; col++) {
                        row.put(rs.getMetaData().getColumnLabel(col).toUpperCase(), rs.getObject(col));
                    }
                    rows.add(row);
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException("Database query execution failed: " + sql, e);
        }
        return rows;
    }
}
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Enterprise Edge Cases & Flaky Test Elimination",
                "topic": "Complex Multi-Table Joins & Window Functions for Duplicate Detection",
                "content": """### SQL Mastery for Enterprise QA Interviews:
1. **Reconciliation Multi-Table Join:**
   ```sql
   SELECT 
       t.transaction_id,
       t.source_account,
       t.target_account,
       t.transfer_amount,
       t.status,
       l.ledger_entry_id,
       l.debit_amount,
       l.credit_amount,
       a.approval_status,
       a.approver_user_id
   FROM transactions t
   INNER JOIN ledger_entries l ON t.transaction_id = l.transaction_id
   LEFT JOIN approvals a ON t.transaction_id = a.transaction_id
   WHERE t.transaction_reference = 'TXN-PNC-2026-9812';
   ```
2. **Detecting Orphan Records & Duplicate Deductions (Window Function):**
   ```sql
   SELECT transaction_id, source_account, transfer_amount, COUNT(*) OVER(PARTITION BY transaction_reference) as occurrence_count
   FROM transactions
   WHERE created_at >= TRUNC(SYSDATE);
   ```"""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "End-to-End Automated Database Reconciliation from UI/API to SQL",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Resolving Policy Ledger Discrepancies Across 85 Scenarios at Liberty Mutual",
                "content": """**Situation:** At **Liberty Mutual**, policy premium adjustments performed through our customer portal occasionally resulted in ledger mismatch reports during end-of-month financial reconciliation across 25,000+ policy records. The discrepancy stemmed from asynchronous batch reconciliation jobs failing to commit distributed database updates.

**Task:** I was tasked with authoring automated SQL validation scripts for 85 reconciliation scenarios to ensure data consistency across distributed Oracle and SQL Server databases during regression testing.

**Action:** I designed an automated verification pipeline connecting our Java test framework to our Oracle transactional database using a pooled **HikariCP JDBC** architecture. In our automated tests, immediately after a policy adjustment API was submitted via **REST Assured**, the test executed a parameterized SQL script joining the `policy_master`, `premium_schedules`, and `financial_ledger` tables. The test verified that the sum of debit adjustments matched the calculated credit adjustments to the exact cent, that policy status codes matched `"ACTIVE_MODIFIED"`, and that an audit record with the tester's user ID was recorded in the database ledger.

**Result:** We successfully automated all 85 reconciliation scenarios, catching 4 critical database trigger bugs where cancelation penalties failed to credit customer ledger accounts. This ensured 100% data integrity prior to monthly release deployments."""
            }
        ],
        "master_qa": {
            "question": "Explain how you perform end-to-end database reconciliation in an automated test: from UI/API action to SQL validation against Oracle/PostgreSQL databases.",
            "answer": """In enterprise software systems—particularly within banking at **PNC Bank** and insurance at **Liberty Mutual**—a successful UI response or an API `200 OK` status code provides only superficial confirmation of a transaction. The definitive source of truth resides in the underlying relational databases (**Oracle**, **PostgreSQL**, or **SQL Server**). End-to-end database reconciliation testing ensures that every front-facing action triggers mathematically accurate, constraint-compliant, and auditable data state mutations across distributed database schemas.

To perform end-to-end database reconciliation in an automated test framework, I structure the validation across four synchronized phases: **Pre-condition Capture**, **Transactional Execution**, **Asynchronous Settlement Wait**, and **Multi-Table SQL Assertion**.

First, during the **Pre-condition Capture** phase, the test script establishes a thread-safe connection to the database via **HikariCP** and queries the baseline state of the affected accounts or policy entities. For instance, in an automated fund transfer test between Account A and Account B, the test queries the `current_balance` and `available_balance` for both accounts, storing these values in our `TestContext` model.

Second, in the **Transactional Execution** phase, the test initiates the fund transfer—either by executing user interactions via **Selenium WebDriver** on the banking portal or by dispatching an authenticated `POST` request using **REST Assured**. The test asserts that the application returns an HTTP `201 Created` or a UI confirmation banner displaying a unique transaction reference ID (e.g., `TXN-PNC-98012`). This dynamic reference ID is extracted and stored as the reconciliation key.

Third, in enterprise architectures where transactions are processed asynchronously through event brokers like **Apache Kafka**, database commits do not happen synchronously with the HTTP response. If a test immediately queries the database, it will fail due to a race condition. I utilize the **Awaitility** library to implement a deterministic polling loop: `await().atMost(Duration.ofSeconds(10)).pollInterval(Duration.ofMillis(500)).until(() -> isTransactionCommitted(txnRef))`.

Finally, once committed, the **Multi-Table SQL Assertion** executes parameterized SQL scripts utilizing complex `INNER JOIN` and `LEFT JOIN` operations across the `transactions`, `general_ledger`, and `audit_log` tables. The test programmatically asserts that Account A's balance decreased by the exact transfer amount, Account B's balance increased by the identical amount (enforcing double-entry bookkeeping rules), that ledger debit/credit totals equal zero net difference, and that an audit entry records the exact timestamp, channel ID, and user ID. This comprehensive end-to-end reconciliation guarantees absolute data integrity across critical financial systems."""
        }
    }
]
