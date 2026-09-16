# -*- coding: utf-8 -*-
"""
Janaki Ashok Kumar - QA Automation 14-Day Roadmap (Days 0 - 4)
Covers:
Day 0: Diagnostic Assessment, Environment Setup & Test Automation Strategy Blueprint
Day 1: Core Java & Object-Oriented Programming (OOP) for Enterprise Frameworks
Day 2: Selenium WebDriver 4 Architecture, W3C Protocol & Advanced Locators
Day 3: Page Object Model (POM), Page Factory Pitfalls & Robust Synchronization
Day 4: TestNG Framework Deep Dive: Parallel Execution, Data-Driven & Listeners
"""

days_part1 = [
    # =========================================================================
    # DAY 0: Diagnostic Assessment, Environment Setup & Test Strategy Blueprint
    # =========================================================================
    {
        "day": 0,
        "title": "Day 0: Diagnostic Assessment, Environment Setup & Test Automation Strategy Blueprint",
        "theme": "Foundation, Toolchain Verification & Agile STLC Alignment",
        "domain_focus": "Enterprise Banking & Transactional Systems (PNC Bank Context)",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: Core Theory & Architectural Philosophy",
                "topic": "The Enterprise Test Automation Pyramid, Shift-Left QA & STLC Lifecycle",
                "content": """Understanding the strategic place of test automation within enterprise banking is fundamental. At **PNC Bank**, applications process over **$2M+ in daily transaction activity**, meaning test automation is not merely a defect-detection tool but a continuous risk-mitigation pipeline.

### The Automation Pyramid in Enterprise Practice
1. **Unit Testing (Base Layer - 70%):** Validates business logic at the class/method level (JUnit/TestNG). Owned primarily by developers, but QA architects define code coverage thresholds (80%+ via **SonarQube**).
2. **API & Service Integration (Middle Layer - 20%):** Validates RESTful microservices, transactional consistency, payload contracts, and error responses using **REST Assured** and **Postman**. Fast execution (sub-second per test), headless, zero UI flakiness.
3. **End-to-End UI Testing (Top Layer - 10%):** Validates critical user journeys (e.g., login, multi-account fund transfer, approval workflow) using **Selenium WebDriver** and **Playwright**. High maintenance cost; kept lean and focused on true E2E flows.

### Shift-Left Testing & Agile Sprint Integration
- **In-Sprint Automation:** Automation is authored during the active sprint, not as an afterthought. QA participates in **Three Amigos** sessions (Product Owner, Developer, QA) to establish acceptance criteria in Gherkin syntax before coding starts.
- **Definition of Done (DoD):** A user story is only complete when automated API and UI smoke tests are integrated into the **Jenkins** / **Azure DevOps** CI/CD pipeline and passing cleanly."""
            },
            {
                "hour": 2,
                "label": "Hour 2: Production Code Lab & Toolchain",
                "topic": "Enterprise Maven Multi-Module `pom.xml` & Repository Architecture",
                "content": """A scalable automation framework requires a clean Maven configuration managing dependencies, compiler plugins, and execution profiles for local, grid, and CI/CD runs.

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.pnc.qa</groupId>
    <artifactId>banking-automation-framework</artifactId>
    <version>1.0.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <selenium.version>4.18.1</selenium.version>
        <testng.version>7.9.0</testng.version>
        <rest-assured.version>5.4.0</rest-assured.version>
        <cucumber.version>7.15.0</cucumber.version>
        <allure.version>2.25.0</allure.version>
        <suiteFile>src/test/resources/suites/testng-regression.xml</suiteFile>
    </properties>

    <dependencies>
        <!-- Selenium WebDriver 4 -->
        <dependency>
            <groupId>org.seleniumhq.selenium</groupId>
            <artifactId>selenium-java</artifactId>
            <version>${selenium.version}</version>
        </dependency>

        <!-- TestNG -->
        <dependency>
            <groupId>org.testng</groupId>
            <artifactId>testng</artifactId>
            <version>${testng.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- REST Assured for API Validation -->
        <dependency>
            <groupId>io.rest-assured</groupId>
            <artifactId>rest-assured</artifactId>
            <version>${rest-assured.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- Cucumber BDD Dependencies -->
        <dependency>
            <groupId>io.cucumber</groupId>
            <artifactId>cucumber-java</artifactId>
            <version>${cucumber.version}</version>
        </dependency>
        <dependency>
            <groupId>io.cucumber</groupId>
            <artifactId>cucumber-testng</artifactId>
            <version>${cucumber.version}</version>
        </dependency>

        <!-- Apache POI for Excel Test Data -->
        <dependency>
            <groupId>org.apache.poi</groupId>
            <artifactId>poi-ooxml</artifactId>
            <version>5.2.5</version>
        </dependency>

        <!-- Oracle JDBC Driver for Database Reconciliation -->
        <dependency>
            <groupId>com.oracle.database.jdbc</groupId>
            <artifactId>ojdbc11</artifactId>
            <version>23.3.0.23.09</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.5</version>
                <configuration>
                    <suiteXmlFiles>
                        <suiteXmlFile>${suiteFile}</suiteXmlFile>
                    </suiteXmlFiles>
                    <parallel>methods</parallel>
                    <threadCount>4</threadCount>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Enterprise Edge Cases & Flaky Test Elimination",
                "topic": "Flaky Test Taxonomy & Strategic Elimination in Financial Workflows",
                "content": """Flakiness destroys confidence in CI/CD pipelines. At **PNC Bank**, where automated tests guard regulatory fund transfers, flakiness is treated as a priority defect.

### Primary Causes of Test Flakiness & Enterprise Solutions:
1. **Asynchronous DOM Mutations & Dynamic Rendering:** Single-page applications (React/Angular) re-render components asynchronously. Solution: Eliminate all `Thread.sleep()` statements. Enforce dynamic explicit waits (`ExpectedConditions.elementToBeClickable` and `ExpectedConditions.visibilityOfElementLocated`) with sensible polling intervals.
2. **Shared State & Test Interdependence:** Tests depending on sequential execution or shared test accounts fail when executed in parallel. Solution: Enforce complete test isolation. Every test provisions its own unique transaction payload or uses test data management APIs to generate fresh customer account profiles.
3. **Environment & Network Latency Spikes:** Backend microservices experiencing momentary database locks cause timeout failures. Solution: Implement an intelligent retry analyzer (`IRetryAnalyzer` in **TestNG**) that retries failed tests once while logging flaky events for telemetry tracking in **Grafana**."""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "Architecting an Enterprise Automation Framework for $2M+ Daily Banking Operations",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Establishing QA Standards Across Multi-Account Approval Workflows",
                "content": """**Situation:** At **PNC Bank**, the HUB corporate banking portal introduced a multi-tier approval workflow for wire transfers exceeding $100,000. Manual regression cycles took 8 hours across 180 test scenarios, causing frequent release bottlenecks and missing critical edge cases in template validations.

**Task:** As the Lead QA Automation Engineer, I was tasked with architecting a robust automation solution to compress the regression window to under 3 hours while ensuring 100% test reliability across 60 complex transfer, template, and approval inbox scenarios.

**Action:** I spearheaded the design of a **Hybrid Java Automation Framework** combining **Selenium WebDriver**, **Cucumber BDD**, and **TestNG**. I structured clean Page Object classes decoupling banking locators from step definitions, integrated **PicoContainer** to manage transactional state across multi-approval steps without static variables, and established **ThreadLocal<WebDriver>** to run 4 concurrent threads in headless Chrome on our Linux CI runners. Furthermore, I integrated **REST Assured** pre-requisite calls to generate wire transfer templates programmatically via APIs before UI verification, eliminating 40 minutes of repetitive UI setup.

**Result:** We successfully compressed the regression execution time from **8 hours down to 3 hours** (a 62.5% reduction), caught 14 high-severity integration defects prior to staging deployment, and maintained stable biweekly releases supporting over **$2M+ in daily transaction volume**."""
            }
        ],
        "master_qa": {
            "question": "How do you design, architect, and scale an enterprise-grade test automation framework from scratch for a mission-critical financial application like PNC Bank?",
            "answer": """Designing an enterprise-grade test automation framework for a financial institution like **PNC Bank** requires a structured, maintainable, and highly resilient architecture capable of validating complex transactional workflows while adhering to strict regulatory compliance and high-availability standards. When architecting such a framework from the ground up, I follow a modular, multi-layered design pattern utilizing **Java**, **Selenium WebDriver 4**, **Cucumber BDD**, **TestNG**, **REST Assured**, and **Apache POI**, orchestrated through **Maven** and **Jenkins** CI/CD pipelines.

The architecture is divided into distinct, decoupled layers to ensure high reusability and maintainability. At the foundational layer, I implement a **Core Utilities and Driver Management Layer**. This utilizes a thread-safe Singleton pattern powered by **ThreadLocal<WebDriver>** to guarantee that parallel test execution across multiple threads or containerized nodes never experiences driver state collisions or race conditions. All browser initialization parameters, headless arguments, and timeouts are abstracted into configurable property files (`config.properties`) managed through an environment reader utility.

Above the driver layer sits the **Page Object Model (POM) Layer**. Here, every banking page (such as TransferFundsPage, AccountSummaryPage, and ApprovalInboxPage) is represented as an independent Java class. To eliminate the notorious `StaleElementReferenceException` often caused by `@FindBy` in legacy PageFactory, I utilize standard `By` locators paired with encapsulated wrapper methods that enforce dynamic explicit waits using **WebDriverWait** and **ExpectedConditions**. This ensures that asynchronous DOM updates in single-page applications are reliably handled without fragile hardcoded pauses.

For test definition, I incorporate a **Cucumber BDD Layer** to bridge technical execution with business logic. Financial analysts, product managers, and QA engineers collaborate on **Gherkin feature files** defining multi-account transfer limits, dual-authorization approval hierarchies, and template validation rules. State sharing across independent step definition classes is managed cleanly using **PicoContainer** dependency injection, avoiding global static variables that corrupt concurrent execution.

To optimize test execution speed, I integrate a **Hybrid API-UI Testing Strategy**. Instead of navigating through repetitive UI screens to set up pre-conditions (such as account creation or funding a balance), the framework invokes backend REST APIs via **REST Assured** to instantaneously provision test data, reserving UI automation strictly for validating user interface rendering, client-side validation, and end-to-end user workflows. Finally, the framework features an automated reporting and failure triage engine integrating **Allure Reports** and **TestNG Listeners**, capturing full-page screenshots and network payload logs on failure, enabling immediate root-cause analysis during continuous deployment cycles."""
        }
    },

    # =========================================================================
    # DAY 1: Core Java & OOP for Enterprise Frameworks
    # =========================================================================
    {
        "day": 1,
        "title": "Day 1: Core Java & Object-Oriented Programming (OOP) for Enterprise Frameworks",
        "theme": "OOP Principles, Thread Safety & Advanced Collections",
        "domain_focus": "Thread-Safe Driver Architecture & Parallel Test Execution",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: Core Architectural Theory",
                "topic": "The Four Pillars of OOP in Test Automation Framework Design",
                "content": """A professional QA automation engineer must treat test automation code with the exact same architectural rigor as production software. The four core principles of Object-Oriented Programming (**OOP**) form the backbone of clean automation architecture:

1. **Encapsulation:** Page Object classes hide web elements (`private By transferAmountField = By.id("amount");`) and expose only public action methods (`public void enterTransferAmount(String amount)`). This prevents test scripts from directly manipulating DOM elements and enforces validation logic at the page level.
2. **Inheritance:** Common setup, teardown, configuration loading, and driver retrieval are centralized in a `BaseTest` or `BasePage` superclass. Child test classes inherit these capabilities, eliminating code duplication across hundreds of test suites.
3. **Polymorphism:**
   - *Static (Compile-time / Overloading):* Custom click or wait methods overloaded to accept either a `By` locator or an existing `WebElement`, or accept variable timeout durations.
   - *Dynamic (Runtime / Overriding):* The `WebDriver` interface dynamically references different browser implementations (`ChromeDriver`, `FirefoxDriver`, `EdgeDriver`, `RemoteWebDriver`) at runtime based on configuration parameters.
4. **Abstraction:** Using Java `Interfaces` (such as `WebDriver`, `WebElement`, or custom `TestListener` contracts) allows the framework to define operational contracts without coupling tests to specific underlying vendor implementations."""
            },
            {
                "hour": 2,
                "label": "Hour 2: Production Code Lab",
                "topic": "Thread-Safe Singleton Driver Manager with `ThreadLocal<WebDriver>`",
                "content": """Below is the production-grade, thread-safe Driver Manager implemented using `ThreadLocal<WebDriver>` to support concurrent multi-threaded execution without cross-thread contamination:

```java
package com.pnc.qa.framework.driver;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import java.time.Duration;

public class DriverManager {

    private static final ThreadLocal<WebDriver> driverThreadLocal = new ThreadLocal<>();

    // Private constructor to enforce Singleton pattern
    private DriverManager() {}

    public static void initDriver(String browser) {
        if (driverThreadLocal.get() == null) {
            WebDriver driver;
            switch (browser.toLowerCase().trim()) {
                case "firefox":
                    FirefoxOptions firefoxOptions = new FirefoxOptions();
                    firefoxOptions.addArguments("--headless");
                    driver = new FirefoxDriver(firefoxOptions);
                    break;
                case "chrome":
                default:
                    ChromeOptions chromeOptions = new ChromeOptions();
                    chromeOptions.addArguments("--headless=new");
                    chromeOptions.addArguments("--disable-gpu");
                    chromeOptions.addArguments("--window-size=1920,1080");
                    chromeOptions.addArguments("--no-sandbox");
                    chromeOptions.addArguments("--disable-dev-shm-usage");
                    driver = new ChromeDriver(chromeOptions);
                    break;
            }
            driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(0)); // Zero implicit wait to favor explicit waits
            driver.manage().window().maximize();
            driverThreadLocal.set(driver);
        }
    }

    public static WebDriver getDriver() {
        WebDriver driver = driverThreadLocal.get();
        if (driver == null) {
            throw new IllegalStateException("WebDriver has not been initialized for the current thread.");
        }
        return driver;
    }

    public static void quitDriver() {
        WebDriver driver = driverThreadLocal.get();
        if (driver != null) {
            try {
                driver.quit();
            } finally {
                driverThreadLocal.remove(); // CRITICAL: Prevent memory leaks in thread pools
            }
        }
    }
}
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Enterprise Edge Cases & Flaky Test Elimination",
                "topic": "ThreadLocal Memory Leaks & Static Variable Pitfalls in Parallel CI/CD",
                "content": """When running 200+ daily tests in **Jenkins** or **Docker** containers using TestNG parallel execution, subtle Java concurrency bugs can completely invalidate test results.

### Critical Edge Cases:
1. **ThreadLocal Memory Leaks (`ThreadLocal.remove()`):** When using thread pools (such as Maven Surefire or executor services), worker threads are reused across tasks. If `driverThreadLocal.remove()` is not invoked in the `@AfterMethod` teardown, subsequent tests assigned to the same thread inherit stale browser sessions, causing `NoSuchSessionException` or severe memory exhaustion on Linux runners.
2. **Static WebElements in Page Objects:** Declaring `public static WebElement submitBtn;` creates a shared reference across all concurrent threads. Thread A navigates to a new page, invalidating the DOM reference for Thread B, resulting in unpredictable `StaleElementReferenceException`.
3. **Collections Concurrency:** When collecting test metrics or failed URLs across parallel tests, using standard `ArrayList` causes `ConcurrentModificationException`. Always use thread-safe collections such as `Collections.synchronizedList(new ArrayList<>())` or `ConcurrentHashMap`."""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "Deep Dive: ThreadLocal<WebDriver> and Thread-Safe Driver Management",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Troubleshooting Parallel Execution Failures at Liberty Mutual",
                "content": """**Situation:** At **Liberty Mutual**, our regression test suite consisted of 160 policy administration scenarios. Running them sequentially took 10 hours, which delayed our monthly release cycle. When the team attempted to enable parallel execution in TestNG, tests started failing randomly with `SessionNotFoundException` and mismatched policy customer data.

**Task:** As the QA Automation Engineer, I was assigned to diagnose the root cause of these parallel test execution failures and re-architect the framework to achieve stable, concurrent execution across 4 parallel browser threads.

**Action:** I conducted a comprehensive code audit of our automation codebase and discovered two fundamental concurrency bugs: first, the `WebDriver` instance was stored in a static global variable inside `BaseTest`; second, the test data reader was utilizing a shared, un-synchronized `HashMap`. I refactored the driver architecture into a thread-safe **ThreadLocal<WebDriver>** implementation, guaranteeing that each parallel execution thread possessed its own completely isolated browser instance. I updated our `@AfterMethod` hooks to explicitly call `ThreadLocal.remove()` to prevent memory leaks across reused threads in our **Jenkins** pipeline. Additionally, I refactored test data loading so each test dynamically instantiated isolated POJO models rather than accessing shared state.

**Result:** The refactored test suite executed in parallel with zero thread collisions, cutting our regression execution time from **10 hours down to 4 hours** (a 60% reduction). Our daily **Jenkins** CI pipeline achieved a 99.2% pass rate across 200+ daily automated executions."""
            }
        ],
        "master_qa": {
            "question": "Why is `ThreadLocal<WebDriver>` essential in parallel test execution, and how do you implement a thread-safe Singleton Driver Manager in Java?",
            "answer": """In modern continuous integration environments, executing automated UI tests sequentially is unsustainable for enterprise applications. At **PNC Bank** and **Liberty Mutual**, running hundreds of complex banking and insurance scenarios sequentially would take between 8 to 10 hours per regression cycle. Enabling parallel execution—whether at the method, class, or test level via **TestNG** or **Maven Surefire**—is required to achieve rapid feedback. However, in Java, standard object references and static variables are shared across all threads within the same JVM process. If a single static `WebDriver driver` instance is utilized, concurrent threads will simultaneously issue commands (such as `driver.get()` or `driver.findElement()`) to the same browser session. This triggers catastrophic race conditions, browser crashes, and `SessionNotCreatedException` or `NoSuchSessionException` errors.

To solve this challenge, **ThreadLocal<WebDriver>** is indispensable. The `ThreadLocal` class in Java provides thread-local variables. Each thread that accesses a `ThreadLocal` instance (via its `.get()` and `.set()` methods) has its own independently initialized copy of the variable. In our automation framework, wrapping the `WebDriver` instance in a `ThreadLocal` container guarantees that Thread-1 (executing an account transfer test in Chrome) and Thread-2 (executing a wire template test in Chrome) operate entirely independent browser instances without any shared memory state or synchronization locks.

Implementing a thread-safe Singleton Driver Manager involves several disciplined design decisions. First, the class constructor is marked `private` to prevent external instantiation. A `private static final ThreadLocal<WebDriver> driverThreadLocal = new ThreadLocal<>();` variable holds the browser references. The `getDriver()` method checks whether the current thread possesses an active driver instance; if not, it invokes an initialization routine that configures headless browser options, disables sandbox restrictions, sets window dimensions, and registers the newly created driver via `driverThreadLocal.set(driver)`. 

Equally vital is the teardown lifecycle. When a test completes, the `@AfterMethod` teardown hook must invoke `driver.quit()` to close the browser process and, crucially, call `driverThreadLocal.remove()`. Failing to call `.remove()` causes severe memory leaks because thread pool workers in CI/CD environments (such as Jenkins slave nodes or Dockerized runners) are kept alive and reused across builds. Retaining stale `ThreadLocal` references prevents garbage collection of large browser session objects and can lead to subsequent tests inheriting corrupted driver states."""
        }
    },

    # =========================================================================
    # DAY 2: Selenium WebDriver 4 Architecture & Advanced Locators
    # =========================================================================
    {
        "day": 2,
        "title": "Day 2: Selenium WebDriver 4 Architecture, W3C Protocol & Advanced Locators",
        "theme": "W3C Compliance, CDP Integration & Complex XPath Axes",
        "domain_focus": "Dynamic Banking Grids, Shadow DOM & iFrames (PNC & Healthcare)",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: Core Architectural Theory",
                "topic": "Selenium 4 Architecture vs. Selenium 3 & W3C Standardization",
                "content": """### Architectural Evolution: Selenium 3 vs. Selenium 4
- **Selenium 3:** Relied on the legacy **JSON Wire Protocol**. Browser interactions required encoding actions into HTTP requests, passing through a browser-specific executable driver (chromedriver, geckodriver) that translated them into internal browser commands. This encoding/decoding overhead introduced latency and intermittent connection dropped errors.
- **Selenium 4:** Fully adopts the **W3C WebDriver Standard**. Both the test client and browser native drivers communicate directly via standardized W3C protocols. No JSON Wire translation is required, resulting in faster, more deterministic execution.

### Key Selenium 4 Innovations:
1. **Chrome DevTools Protocol (CDP):** Direct access to browser internals. Allows capturing network requests, performance metrics, mocking geolocation, emulating network throttling (3G/4G), and listening to console JavaScript errors.
2. **Relative Locators (`with(By...)`):** Finding elements based on their spatial relationship to other elements (`above()`, `below()`, `toLeftOf()`, `toRightOf()`, `near()`).
3. **Native Window & Tab Management:** `driver.switchTo().newWindow(WindowType.TAB)` or `driver.switchTo().newWindow(WindowType.WINDOW)` without relying on JavaScript hacks."""
            },
            {
                "hour": 2,
                "label": "Hour 2: Production Code Lab",
                "topic": "Dynamic XPath Axes, Shadow DOM & Complex Web Table Automation",
                "content": """Financial web applications like **PNC Bank**'s HUB portal frequently render transactional ledgers and approval queues inside dynamic tables with nested checkboxes and approval buttons.

```java
package com.pnc.qa.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.SearchContext;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;

public class TransactionApprovalPage {

    private final WebDriver driver;
    private final WebDriverWait wait;

    public TransactionApprovalPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    // Dynamic XPath locating the approve button for a specific transaction reference ID
    public void approveTransactionByReference(String referenceId) {
        // XPath using following-sibling and ancestor axes
        String xpathExpression = String.format(
            "//table[@id='transfersGrid']//tr[td[normalize-space()='%s']]//td//button[contains(@class,'btn-approve')]",
            referenceId
        );
        WebElement approveBtn = wait.until(ExpectedConditions.elementToBeClickable(By.xpath(xpathExpression)));
        approveBtn.click();
    }

    // Interacting with an element encapsulated inside an open Shadow DOM
    public void enterVerificationPinInsideShadowDOM(String pin) {
        // 1. Locate the Shadow Host element
        WebElement shadowHost = wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("#auth-widget-host")));
        
        // 2. Extract the Shadow Root context (Selenium 4 native API)
        SearchContext shadowRoot = shadowHost.getShadowRoot();
        
        // 3. Find input inside Shadow DOM using CSS selector (XPath not supported in Shadow DOM)
        WebElement pinInput = shadowRoot.findElement(By.cssSelector("input.pin-field"));
        pinInput.clear();
        pinInput.sendKeys(pin);
    }
}
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Enterprise Edge Cases & Flaky Test Elimination",
                "topic": "Handling Stale Elements, Dynamic IDs & Nested iFrames",
                "content": """### Complex UI Automation Challenges:
1. **Dynamic IDs (`id="btn_submit_984372"`):** Financial apps use dynamic GUIDs that change on every page refresh. Solution: Never rely on auto-generated IDs. Construct resilient XPaths using stable attributes (`//button[@data-testid='transfer-submit-btn']` or `//button[normalize-space()='Submit Transfer' and not(@disabled)]`).
2. **Nested iFrames (e.g., Third-Party Payment Gateways):** Elements inside an `<iframe>` cannot be located until the driver context switches to that frame. Solution:
   ```java
   wait.until(ExpectedConditions.frameToBeAvailableAndSwitchToIt(By.id("paymentFrame")));
   // Interact with payment fields
   driver.switchTo().defaultContent(); // Always return to main page
   ```
3. **Custom SVG Elements & Canvas:** SVG elements do not respond to standard XPath syntax `//svg/path`. You must use `//*[local-name()='svg']/*[local-name()='path']`."""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "Locating Complex UI Elements: Dynamic XPath, Shadow DOM & Dynamic Grids",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Automating Complex Financial Grid Approvals at PNC Bank",
                "content": """**Situation:** At **PNC Bank**, the commercial treasury portal displayed pending wire transfers in an asynchronous ag-Grid table with dynamically generated row IDs and virtualized scrolling. Existing automation scripts failed 40% of the time with `NoSuchElementException` because rows off-screen were removed from the DOM.

**Task:** I needed to engineer a reliable locator and synchronization strategy to automate the approval of specific transactions across 60 multi-account transfer workflows supporting $2M+ in daily transaction volume.

**Action:** I analyzed the ag-Grid DOM structure and developed a dynamic locator strategy combining XPath axes (`ancestor` and `following-sibling`) with JavaScript virtual scroll automation. Instead of hardcoding row indexes, I authored a parameterized XPath locating the target transaction by its unique reference number: `//div[@role='row'][.//span[text()='%s']]//button[@aria-label='Approve']`. When transactions were not immediately visible in the virtual viewport, I wrote a reusable utility utilizing `JavascriptExecutor` to scroll the grid viewport until the element satisfied `ExpectedConditions.visibilityOfElementLocated()`.

**Result:** Flakiness on the transaction approval grid dropped to zero. We achieved 100% test pass reliability across 12 sprint releases, preventing wire approval defects from escaping to staging and ensuring smooth compliance sign-offs."""
            }
        ],
        "master_qa": {
            "question": "How do you locate and interact with elements inside closed or open Shadow DOM, nested iframes, and dynamic web tables in financial web portals?",
            "answer": """Interacting with modern web portals in the financial and healthcare domains—such as **PNC Bank**'s HUB portal or **Molina Healthcare**'s enrollment system—frequently demands navigating beyond simple DOM trees into complex UI structures such as **Shadow DOM**, **nested iframes**, and **dynamically virtualized web tables**. Standard locator strategies like `driver.findElement(By.id())` fail completely when confronted with these encapsulated components.

Handling the **Shadow DOM** depends on whether the shadow root is configured as `open` or `closed`. In modern frontend architectures (such as Lit or Web Components), web widgets (e.g., custom authentication pin pads or secure credit card inputs) are encapsulated within a shadow tree to isolate styles. In **Selenium 4**, handling an `open` Shadow DOM has been streamlined: we locate the host element using standard locators, call `WebElement.getShadowRoot()`, which returns a `SearchContext`, and subsequently search within that context using CSS selectors. It is critical to recognize that **XPath is not supported** within Shadow DOM trees by the W3C specification; only CSS selectors can be used. If dealing with a `closed` Shadow DOM, external JavaScript cannot pierce the shadow boundary by design; the test automation strategy requires coordinating with developers to expose test hooks, using Chrome DevTools Protocol (CDP) commands, or injecting JavaScript via `JavascriptExecutor`.

For **nested iframes**—often employed by third-party payment processors or document viewer widgets—the WebDriver context must explicitly traverse each frame hierarchy. I implement explicit waits using `wait.until(ExpectedConditions.frameToBeAvailableAndSwitchToIt(By.id("parentFrame")))`, followed by a secondary wait for the child frame. Once the interactions inside the iframe are concluded, failing to invoke `driver.switchTo().defaultContent()` leaves the driver trapped inside the child frame, causing all subsequent page actions to throw `NoSuchElementException`.

Finally, when automating **dynamic web tables** (such as transactional ledgers with asynchronous data loading), hardcoded row indexes must be strictly avoided. I construct dynamic, relational XPath expressions using axes such as `ancestor`, `following-sibling`, and `preceding-sibling`. For instance, to click an 'Approve' button corresponding to a specific transaction reference number across a multi-column table, I use: `//table[@id='transfersGrid']//tr[td[normalize-space()='TXN-90812']]//td//button[contains(@class,'approve-btn')]`. This dynamic relationship ensures that even if transactions re-order or new rows load asynchronously, the test deterministically binds to the correct record."""
        }
    },

    # =========================================================================
    # DAY 3: Page Object Model (POM), Page Factory Pitfalls & Synchronization
    # =========================================================================
    {
        "day": 3,
        "title": "Day 3: Page Object Model (POM), Page Factory Pitfalls & Robust Synchronization",
        "theme": "Design Patterns, Stale Element Resolution & Dynamic Waits",
        "domain_focus": "Refactoring Legacy Frameworks & Slashing Execution Times",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: Core Architectural Theory",
                "topic": "Why PageFactory is Deprecated in Modern Automation & Clean POM Design",
                "content": """### The Architectural Debate: PageFactory vs. Clean POM
In early Selenium frameworks, the `@FindBy` annotation combined with `PageFactory.initElements(driver, this)` was popular. However, in modern single-page applications (React, Angular, Vue), PageFactory introduces severe stability bottlenecks:

1. **Lazy Initialization & `StaleElementReferenceException`:** PageFactory initializes element proxies. If the DOM re-renders (common during AJAX calls or state updates in modern banking portals), the proxy still points to the old DOM node. Calling `.click()` immediately throws `StaleElementReferenceException`.
2. **Incompatibility with Dynamic Explicit Waits:** You cannot cleanly wrap a `@FindBy` WebElement with `wait.until(ExpectedConditions.elementToBeClickable())` without triggering an underlying lookup that may fail prematurely.
3. **The Clean POM Pattern (Modern Standard):** Store locators as `private final By` variables. Expose public business actions that dynamically query the DOM through a dedicated wait utility right at the moment of interaction. This ensures elements are always fresh and interactable."""
            },
            {
                "hour": 2,
                "label": "Hour 2: Production Code Lab",
                "topic": "Production-Grade BasePage with Resilient FluentWait Utility",
                "content": """Below is the production-grade `BasePage` incorporating `FluentWait` with polling, custom exception handling, and JavaScript click fallbacks:

```java
package com.pnc.qa.framework.base;

import org.openqa.selenium.*;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.FluentWait;
import java.time.Duration;

public abstract class BasePage {

    protected WebDriver driver;
    protected FluentWait<WebDriver> wait;

    public BasePage(WebDriver driver) {
        this.driver = driver;
        this.wait = new FluentWait<>(driver)
                .withTimeout(Duration.ofSeconds(15))
                .pollingEvery(Duration.ofMillis(500))
                .ignoring(NoSuchElementException.class)
                .ignoring(StaleElementReferenceException.class)
                .ignoring(ElementClickInterceptedException.class);
    }

    protected void click(By locator) {
        try {
            WebElement element = wait.until(ExpectedConditions.elementToBeClickable(locator));
            element.click();
        } catch (ElementClickInterceptedException e) {
            // Fallback: Scroll into view and execute click via JavaScript if overlay momentarily intercepted
            WebElement element = driver.findElement(locator);
            ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block: 'center'});", element);
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", element);
        }
    }

    protected void sendKeys(By locator, String text) {
        WebElement element = wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
        element.clear();
        element.sendKeys(text);
    }

    protected String getText(By locator) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).getText().trim();
    }
}
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Enterprise Edge Cases & Flaky Test Elimination",
                "topic": "Implicit Wait vs. Explicit Wait Collisions & Stale Element Triage",
                "content": """### The Golden Rule of Selenium Synchronization:
**NEVER MIX IMPLICIT AND EXPLICIT WAITS.**
According to the official Selenium documentation, mixing `implicitlyWait()` with `WebDriverWait` causes undefined timeout behaviors. For instance, an explicit wait of 10 seconds combined with an implicit wait of 15 seconds can cause tests to sleep for 25 seconds or fail immediately on element absence. Always set `implicitlyWait(Duration.ofSeconds(0))` and rely exclusively on explicit or fluent waits.

### Eliminating `StaleElementReferenceException`:
A stale element reference occurs when:
1. The element has been deleted entirely from the DOM.
2. The element is still in the DOM, but the page was re-rendered (e.g., React component re-mount).
- **Solution:** Wrap actions in an auto-retry loop catching `StaleElementReferenceException` that re-queries the `By` locator from the driver root, or leverage `FluentWait.ignoring(StaleElementReferenceException.class)`."""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "Root Causes of StaleElementReferenceException & FluentWait Architecture",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Refactoring 180 Regression Scenarios at PNC Bank (8 hrs -> 3 hrs)",
                "content": """**Situation:** At **PNC Bank**, our automated regression suite consisted of 180 legacy Selenium scenarios executed via Cucumber. Over several years of feature additions, the suite execution time had ballooned to **8 hours**, plagued by frequent `StaleElementReferenceException` errors and hardcoded `Thread.sleep(5000)` statements introduced to stabilize flaky banking approval screens.

**Task:** I was tasked with leading the architectural overhaul of the regression suite to reduce execution time to under 4 hours while achieving a 98%+ pass rate for biweekly release cycles.

**Action:** I systematically eliminated every single `Thread.sleep()` across all 180 step definition files, replacing them with a centralized `WaitUtils` class built on **FluentWait** that polled every 500ms and ignored stale element exceptions. I refactored the legacy PageFactory classes away from `@FindBy` proxies to clean `By` locators encapsulated in our `BasePage`. Furthermore, I identified 45 scenarios where tests waited through 5 UI screens simply to set up test accounts; I refactored these to use **REST Assured** background API calls to seed test data in milliseconds. Finally, I reconfigured **TestNG** to execute tests concurrently across 4 parallel browser threads.

**Result:** Regression execution time plummeted from **8 hours down to 3 hours** (a 62.5% reduction). Flaky failure rates dropped from 18% to under 1.5%, saving our engineering team approximately 6 hours of manual re-testing during every biweekly release."""
            }
        ],
        "master_qa": {
            "question": "Explain the root cause of `StaleElementReferenceException` and how you build a resilient, custom wait mechanism using FluentWait in Selenium WebDriver.",
            "answer": """In **Selenium WebDriver**, a `StaleElementReferenceException` is one of the most frequent and disruptive exceptions encountered in enterprise automation suites. It occurs when a previously located `WebElement` reference is no longer attached to the active Document Object Model (DOM) of the browser. Specifically, the W3C WebDriver specification defines two primary conditions that trigger this error: first, the referenced element has been completely deleted or destroyed from the DOM; second, the DOM has undergone a re-render or reload (frequently triggered by asynchronous AJAX calls, React virtual DOM updates, or Angular route transitions), meaning that even if an element with identical HTML attributes appears in the exact same visual location, its internal DOM memory reference ID has changed. If the test script attempts to perform an interaction (such as `.click()` or `.sendKeys()`) on the old reference handle, the browser driver rejects the call with a stale reference error.

To eradicate this problem, relying on static sleep timers (`Thread.sleep()`) or naive implicit waits is wholly insufficient. Implicit waits only dictate the duration WebDriver searches for an element when locating it; they provide zero protection when an already located element subsequently goes stale during interaction. The definitive engineering solution is to implement an intelligent, dynamic synchronization layer using **FluentWait**.

`FluentWait` represents an advanced implementation of the `Wait` interface in Java, allowing engineers to configure maximum timeout durations, polling frequencies, and specific exceptions to ignore during the wait evaluation cycle. In our enterprise framework at **PNC Bank**, I construct a custom wait utility that configures a 15-second maximum timeout, a 500-millisecond polling interval, and explicitly ignores both `NoSuchElementException.class` and `StaleElementReferenceException.class`. Within this wait loop, instead of caching raw `WebElement` instances, we pass the underlying `By` locator to `ExpectedConditions.refreshed(ExpectedConditions.elementToBeClickable(locator))`. The `ExpectedConditions.refreshed()` wrapper is critical: if a stale reference is detected during the polling evaluation, it catches the exception and forces WebDriver to re-query the DOM from scratch using the original `By` locator.

Additionally, our base interaction methods incorporate defensive retry logic. If an interaction fails due to a microsecond race condition where an element re-renders immediately between the wait resolution and the click execution, a controlled loop attempts the interaction up to two additional times before failing. This architecture completely insulates the test suite from asynchronous frontend state mutations, transforming an inherently fragile UI suite into an enterprise-grade, deterministic regression pipeline."""
        }
    },

    # =========================================================================
    # DAY 4: TestNG Framework Deep Dive: Parallel Execution, Data-Driven & Listeners
    # =========================================================================
    {
        "day": 4,
        "title": "Day 4: TestNG Framework Deep Dive: Parallel Execution, Data-Driven & Listeners",
        "theme": "Batch Optimization, Dynamic Retries & Test Data Providers",
        "domain_focus": "220+ Automated Tests Optimization (PNC & Liberty Mutual)",
        "hours": [
            {
                "hour": 1,
                "label": "Hour 1: Core Architectural Theory",
                "topic": "TestNG Execution Lifecycle, Annotations & Suite Architecture",
                "content": """### TestNG Lifecycle Hierarchy:
TestNG provides granular execution control unmatched by JUnit 4:
`@BeforeSuite` -> `@BeforeTest` -> `@BeforeClass` -> `@BeforeMethod` -> `@Test` -> `@AfterMethod` -> `@AfterClass` -> `@AfterTest` -> `@AfterSuite`.

### Enterprise Suite Management:
- **Groups:** Tagging tests (`groups = {"smoke", "regression", "p1"}`) allows targeted execution in CI/CD pipelines (e.g., running only `@smoke` on pull requests).
- **Parameterization:** Injecting global parameters (browser, environment, baseURL) directly from `testng.xml` using `@Parameters({"browser", "env"})`.
- **Dependency Management:** `dependsOnMethods` or `dependsOnGroups` ensures dependent tests are skipped rather than failed if a prerequisite step fails (e.g., don't attempt to approve a wire transfer if the creation test failed)."""
            },
            {
                "hour": 2,
                "label": "Hour 2: Production Code Lab",
                "topic": "Automatic Retry Mechanism with `IRetryAnalyzer` & `IAnnotationTransformer`",
                "content": """Manually adding `retryAnalyzer = RetryAnalyzer.class` to hundreds of `@Test` annotations is unmaintainable. We use `IAnnotationTransformer` to inject retry logic dynamically at runtime across the entire suite.

```java
package com.pnc.qa.framework.listeners;

import org.testng.IRetryAnalyzer;
import org.testng.ITestResult;

public class RetryAnalyzer implements IRetryAnalyzer {

    private int count = 0;
    private static final int MAX_RETRY_COUNT = 1; // Retry failed test once

    @Override
    public boolean retry(ITestResult result) {
        if (!result.isSuccess()) {
            if (count < MAX_RETRY_COUNT) {
                count++;
                System.out.println("Retrying test: " + result.getName() + " for attempt " + count);
                return true; // TestNG re-executes the test
            }
        }
        return false;
    }
}
```

```java
package com.pnc.qa.framework.listeners;

import org.testng.IAnnotationTransformer;
import org.testng.annotations.ITestAnnotation;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;

public class AnnotationTransformer implements IAnnotationTransformer {

    @Override
    public void transform(ITestAnnotation annotation, Class testClass, Constructor testConstructor, Method testMethod) {
        // Automatically attach RetryAnalyzer to every @Test in the project
        annotation.setRetryAnalyzer(RetryAnalyzer.class);
    }
}
```

```xml
<!-- testng-regression.xml -->
<suite name="PNC Banking Regression Suite" parallel="methods" thread-count="4">
    <listeners>
        <listener class-name="com.pnc.qa.framework.listeners.AnnotationTransformer"/>
        <listener class-name="com.pnc.qa.framework.listeners.TestListener"/>
    </listeners>
    <test name="Transfer & Reconciliation Tests">
        <classes>
            <class name="com.pnc.qa.tests.FundTransferTests"/>
            <class name="com.pnc.qa.tests.AccountReconciliationTests"/>
        </classes>
    </test>
</suite>
```"""
            },
            {
                "hour": 3,
                "label": "Hour 3: Enterprise Edge Cases & Flaky Test Elimination",
                "topic": "Data-Driven Testing with Apache POI & DataProvider Concurrency",
                "content": """When running data-driven tests in parallel using `@DataProvider(parallel = true)`, Excel reader utilities must be thread-safe. Standard `FileInputStream` operations can throw `FileLockedException` or corrupted byte read errors if multiple threads read the same workbook simultaneously.

### Thread-Safe DataProvider Best Practices:
1. **Load Into Memory Once:** Read the Excel sheet into an in-memory `List<Map<String, String>>` during suite startup or `@BeforeClass`, then feed test iterations from memory.
2. **Dynamic Data Filtering:** Allow tests to filter rows by `Execution_Flag == 'Y'` so testers can run specific subsets without editing code.
3. **Data Isolation:** Ensure test data rows contain unique transactional amounts or account numbers to avoid collisions during parallel database reconciliation."""
            },
            {
                "hour": 4,
                "label": "Hour 4: Master Technical Interview Question",
                "topic": "Dynamic Retries with IRetryAnalyzer & TestNG Listeners in CI/CD",
                "content": """See below for the comprehensive 300+ word master technical answer."""
            },
            {
                "hour": 5,
                "label": "Hour 5: Behavioral STAR Narrative & Agile Alignment",
                "topic": "Optimizing 220 Automated Tests & Slashing Release Effort by 6 Hours",
                "content": """**Situation:** At **PNC Bank**, our biweekly release activities involved executing a batch of 220 automated tests. The test suite took over 7 hours to run and frequently required an additional 3 hours of manual triage due to intermittent network timeouts in our staging environment, creating significant release fatigue.

**Task:** My objective was to optimize our **TestNG** and **Maven** execution architecture to reduce regression execution effort by at least 5 hours while providing clear, automated visibility into test failures.

**Action:** I re-engineered our `testng.xml` configuration, migrating from sequential execution to parallel execution (`parallel="methods"` with a tuned `thread-count="4"`). To eliminate false alarms caused by temporary microservice network latency, I developed an **IRetryAnalyzer** coupled with an **IAnnotationTransformer** to automatically retry failed tests a single time. I also implemented a custom **ITestListener** that captured full DOM source code, active URL, and a timestamped screenshot directly into an **Allure Report** dashboard whenever a test permanently failed.

**Result:** We reduced regression execution effort by **6 hours** during every biweekly release. Release managers gained immediate confidence through real-time test execution dashboards, and our deployment cycle velocity increased significantly across 12 consecutive sprints."""
            }
        ],
        "master_qa": {
            "question": "How do you implement an automatic failed-test rerun mechanism using `IRetryAnalyzer` and `IAnnotationTransformer` in TestNG without modifying every test annotation?",
            "answer": """In enterprise test automation pipelines, transient infrastructure anomalies—such as temporary network latency, database connection pool exhaustion, or slow third-party service responses—can cause automated tests to fail intermittently. When executing suites of 200+ tests in **Jenkins** or **Azure DevOps**, having a single test fail due to an environmental hiccup can falsely block an entire deployment pipeline. Implementing an automatic retry mechanism ensures that transient failures are automatically verified before declaring a test failed, without masking genuine software defects.

In **TestNG**, the standard mechanism for retrying failed tests is the **IRetryAnalyzer** interface. This interface contains a single method: `public boolean retry(ITestResult result)`. Within this method, we maintain an invocation counter and compare it against a configured maximum retry limit (typically set to 1 in enterprise pipelines to avoid masking race conditions). If the test result status indicates failure and the retry count has not exceeded the limit, the method increments the counter and returns `true`, prompting TestNG to immediately re-execute the failed test.

However, the naive approach to applying this analyzer—manually appending `(retryAnalyzer = RetryAnalyzer.class)` to every `@Test` annotation across hundreds of test classes—is anti-architectural, error-prone, and violates the DRY (Don't Repeat Yourself) principle. When new engineers join the team, they frequently forget to annotate their test methods, creating inconsistent retry behaviors.

The enterprise-grade solution is to leverage TestNG's **IAnnotationTransformer** listener interface. The `IAnnotationTransformer` provides a callback method: `transform(ITestAnnotation annotation, Class testClass, Constructor testConstructor, Method testMethod)`. This method is invoked by TestNG's core engine during suite startup for every single `@Test` annotation in the classpath prior to execution. Inside `transform()`, we programmatically invoke `annotation.setRetryAnalyzer(RetryAnalyzer.class)`.

To activate this globally across the entire test suite, we register the `AnnotationTransformer` inside our `testng.xml` configuration file within the `<listeners>` tag, or dynamically via Maven Surefire plugin configuration. Once registered, every current and future `@Test` method automatically inherits retry capabilities with zero manual intervention. Furthermore, in our custom `ITestListener`, we log retried tests with a status of `SKIPPED` or `RETRIED` and aggregate telemetry into our **Grafana** or **Allure** reporting dashboards. This guarantees that flaky tests are not ignored by the engineering team, but rather tracked, analyzed, and permanently resolved in technical debt sprints."""
        }
    }
]
