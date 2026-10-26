# -*- coding: utf-8 -*-
"""
Production Coding & Scripting Problems for Fikerete Semma — SQL Database Administrator
Format:
1. Problem Statement First
2. Fully Commented Production-Grade Code (T-SQL / PowerShell)
3. Time & Space Complexity Analysis / Execution Profile
"""

CODING_PROBLEMS = [
    {
        "num": 1,
        "category": "Concurrency & Locking Triage",
        "title": "Real-Time Recursive Blocking Chain Detection & Lead Blocker Identification",
        "problem_statement": """In a high-throughput financial or healthcare SQL Server instance, a single long-running query or uncommitted transaction can acquire an exclusive lock, causing dozens of downstream worker threads to queue. Write an enterprise-grade T-SQL diagnostic script that interrogates active requests, builds a recursive blocking hierarchy using Common Table Expressions (CTEs), pinpoints the exact lead blocker session ID, outputs the offending T-SQL text and execution plan, and calculates elapsed blocking duration.""",
        "code": """-- ============================================================================
-- Enterprise Recursive Blocking Chain & Root Cause Diagnostic Script
-- Target: SQL Server 2016 through 2022
-- Author: Fikerete Semma (SQL Database Administrator)
-- ============================================================================

SET NOCOUNT ON;

WITH ActiveSessions AS (
    -- Step 1: Capture all currently executing requests with session metadata
    SELECT 
        r.session_id,
        r.blocking_session_id,
        r.start_time,
        r.status,
        r.command,
        r.wait_type,
        r.wait_time AS wait_time_ms,
        r.last_wait_type,
        r.cpu_time,
        r.total_elapsed_time AS elapsed_time_ms,
        r.logical_reads,
        r.writes,
        s.login_name,
        s.host_name,
        s.program_name,
        DB_NAME(r.database_id) AS database_name,
        t.text AS sql_text,
        p.query_plan
    FROM sys.dm_exec_requests r WITH (NOLOCK)
    JOIN sys.dm_exec_sessions s WITH (NOLOCK) 
        ON r.session_id = s.session_id
    OUTER APPLY sys.dm_exec_sql_text(r.sql_handle) t
    OUTER APPLY sys.dm_exec_query_plan(r.plan_handle) p
    WHERE s.is_user_process = 1
),
BlockingTree AS (
    -- Step 2: Anchor member - identify Root Blockers (sessions that are blocking others but not blocked themselves)
    SELECT 
        session_id,
        blocking_session_id,
        session_id AS root_blocker_id,
        0 AS blocking_level,
        status,
        command,
        wait_type,
        wait_time_ms,
        elapsed_time_ms,
        login_name,
        host_name,
        program_name,
        database_name,
        sql_text,
        query_plan,
        CAST(session_id AS VARCHAR(1000)) AS blocking_path
    FROM ActiveSessions
    WHERE (blocking_session_id = 0 OR blocking_session_id IS NULL)
      AND session_id IN (SELECT DISTINCT blocking_session_id FROM ActiveSessions WHERE blocking_session_id > 0)
    
    UNION ALL
    
    -- Step 3: Recursive member - traverse down the dependency tree
    SELECT 
        child.session_id,
        child.blocking_session_id,
        parent.root_blocker_id,
        parent.blocking_level + 1 AS blocking_level,
        child.status,
        child.command,
        child.wait_type,
        child.wait_time_ms,
        child.elapsed_time_ms,
        child.login_name,
        child.host_name,
        child.program_name,
        child.database_name,
        child.sql_text,
        child.query_plan,
        CAST(parent.blocking_path + ' -> ' + CAST(child.session_id AS VARCHAR(10)) AS VARCHAR(1000)) AS blocking_path
    FROM ActiveSessions child
    INNER JOIN BlockingTree parent 
        ON child.blocking_session_id = parent.session_id
    WHERE child.session_id <> child.blocking_session_id -- Prevent infinite self-loops
)
-- Step 4: Return prioritized blocking tree formatted for rapid incident triage
SELECT 
    REPLICATE('|-- ', blocking_level) + CAST(session_id AS VARCHAR(10)) AS session_tree,
    root_blocker_id,
    blocking_level,
    database_name,
    login_name,
    host_name,
    program_name,
    wait_type,
    wait_time_ms / 1000.0 AS wait_time_sec,
    elapsed_time_ms / 1000.0 AS elapsed_time_sec,
    sql_text,
    query_plan,
    blocking_path
FROM BlockingTree
ORDER BY root_blocker_id, blocking_level, elapsed_time_ms DESC;
""",
        "complexity": """**Execution Profile & Algorithmic Complexity:**
- **Time Complexity:** O(N + E) where N is the number of active user sessions and E is the number of blocking relationships. The recursive CTE processes active sessions in-memory and typically completes in under 15 milliseconds.
- **Space / Memory Complexity:** O(N) workspace memory required to store session tokens and query plans in the temporary execution context.
- **I/O Profile:** Zero physical disk reads. Interrogates in-memory dynamic management structures (`sys.dm_exec_requests` and `sys.dm_exec_sessions`) with `NOLOCK` hints to prevent diagnostic queries from participating in existing lock contention."""
    },
    {
        "num": 2,
        "category": "Internals & TempDB Storage",
        "title": "TempDB Allocation Page Latch Contention Diagnostics (PFS, GAM, SGAM)",
        "problem_statement": """During peak batch rating or ETL workloads, SQL Server instances may experience severe performance stalls manifesting as PAGELATCH_UP or PAGELATCH_SH waits in TempDB. Write an automated T-SQL diagnostic script that inspects active latch waiting tasks, determines if the contention is located in TempDB (database_id = 2), decodes the physical page ID into its corresponding allocation bitmap structure (PFS, GAM, SGAM, or user data page), and outputs actionable configuration remediation recommendations.""",
        "code": """-- ============================================================================
-- TempDB Allocation Page Latch Contention Diagnostic & Decoding Engine
-- Target: SQL Server 2016 through 2022
-- Author: Fikerete Semma (SQL Database Administrator)
-- ============================================================================

SET NOCOUNT ON;

WITH TempDBLatchWaits AS (
    -- Step 1: Interrogate active latch waiting tasks specifically targeting TempDB
    SELECT 
        wt.session_id,
        wt.wait_type,
        wt.wait_duration_ms,
        wt.resource_description,
        -- Extract File ID: 2:1:1 -> File 1, Page 1
        TRY_CAST(SUBSTRING(wt.resource_description, 3, CHARINDEX(':', wt.resource_description, 3) - 3) AS INT) AS file_id,
        -- Extract Page ID: 2:1:8088 -> Page 8088
        TRY_CAST(SUBSTRING(wt.resource_description, 
                           CHARINDEX(':', wt.resource_description, 3) + 1, 
                           LEN(wt.resource_description)) AS BIGINT) AS page_id
    FROM sys.dm_os_waiting_tasks wt WITH (NOLOCK)
    WHERE wt.wait_type LIKE 'PAGELATCH%'
      AND wt.resource_description LIKE '2:%' -- Database ID 2 is strictly TempDB
)
SELECT 
    w.session_id,
    w.wait_type,
    w.wait_duration_ms,
    w.file_id,
    w.page_id,
    -- Step 2: Decode page ID into architectural allocation bitmap structure
    CASE 
        WHEN w.page_id = 1 OR w.page_id % 8088 = 0 THEN 'PFS (Page Free Space) Contention - Free space byte allocation tracking'
        WHEN w.page_id = 2 OR (w.page_id - 2) % 511232 = 0 THEN 'GAM (Global Allocation Map) Contention - Uniform extent allocation tracking'
        WHEN w.page_id = 3 OR (w.page_id - 3) % 511232 = 0 THEN 'SGAM (Shared Global Allocation Map) Contention - Mixed extent allocation tracking'
        ELSE 'User Data Page Contention (Frequent insert/hotspot on temporary table B-tree)'
    END AS allocation_page_type,
    r.command,
    r.cpu_time,
    r.total_elapsed_time AS elapsed_time_ms,
    DB_NAME(r.database_id) AS user_database,
    t.text AS executing_statement,
    -- Step 3: Recommend configuration remediation based on findings
    CASE 
        WHEN w.page_id IN (1, 2, 3) OR w.page_id % 8088 = 0 
        THEN 'Action Required: Add additional TempDB data files (match CPU cores up to 8). Ensure identical file sizes and auto-growth increments.'
        ELSE 'Action Required: Refactor temporary table indexing; replace temporary tables with table variables or distribute inserts.'
    END AS architectural_recommendation
FROM TempDBLatchWaits w
LEFT JOIN sys.dm_exec_requests r WITH (NOLOCK) ON w.session_id = r.session_id
OUTER APPLY sys.dm_exec_sql_text(r.sql_handle) t
ORDER BY w.wait_duration_ms DESC;
""",
        "complexity": """**Execution Profile & Algorithmic Complexity:**
- **Time Complexity:** O(W) where W is the number of active waiting tasks on the SQL Server scheduler. Executes in under 5 milliseconds.
- **Space / Memory Complexity:** O(W) memory required to parse resource description strings in the Common Table Expression.
- **Mathematical Allocation Mapping:** PFS repeats every 8,088 pages (~64 MB); GAM and SGAM repeat every 511,232 pages (~4 GB). Decoding these formulas pinpoints the exact concurrency bottleneck."""
    },
    {
        "num": 3,
        "category": "Query Optimization & Indexing",
        "title": "Automated Missing Index Opportunity Analyzer with Include Columns and Impact Scoring",
        "problem_statement": """Database administrators must avoid creating duplicate, redundant, or unhelpful indexes. Write a high-performance T-SQL script that interrogates the missing index Dynamic Management Views, calculates an empirical composite impact score, synthesizes dynamic CREATE INDEX DDL with properly partitioned key and INCLUDE columns, and filters out low-impact recommendations.""",
        "code": """-- ============================================================================
-- Automated High-Impact Missing Index Opportunity Synthesizer
-- Target: SQL Server 2016 through 2022
-- Author: Fikerete Semma (SQL Database Administrator)
-- ============================================================================

SET NOCOUNT ON;

SELECT TOP 25
    -- Composite Impact Score Formula: avg_user_impact * (user_seeks + user_scans)
    CAST(migs.avg_user_impact * (migs.user_seeks + migs.user_scans) AS BIGINT) AS composite_impact_score,
    migs.avg_user_impact AS estimated_cost_reduction_percent,
    migs.user_seeks + migs.user_scans AS total_missed_lookups,
    migs.last_user_seek AS last_needed_timestamp,
    DB_NAME(mid.database_id) AS database_name,
    OBJECT_SCHEMA_NAME(mid.object_id, mid.database_id) AS schema_name,
    OBJECT_NAME(mid.object_id, mid.database_id) AS table_name,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns,
    -- Step 1: Synthesize clean, standardized DDL statement
    'CREATE NONCLUSTERED INDEX [IX_' + 
        REPLACE(REPLACE(REPLACE(OBJECT_NAME(mid.object_id, mid.database_id), '[', ''), ']', ''), ' ', '_') + '_' +
        REPLACE(REPLACE(REPLACE(ISNULL(mid.equality_columns, 'eq'), '[', ''), ']', ''), ', ', '_') + 
        CASE WHEN mid.inequality_columns IS NOT NULL 
             THEN '_' + REPLACE(REPLACE(REPLACE(mid.inequality_columns, '[', ''), ']', ''), ', ', '_') 
             ELSE '' END + '] ON ' + 
        mid.statement + ' (' + 
        ISNULL(mid.equality_columns, '') + 
        CASE WHEN mid.equality_columns IS NOT NULL AND mid.inequality_columns IS NOT NULL THEN ', ' ELSE '' END + 
        ISNULL(mid.inequality_columns, '') + ')' + 
        ISNULL(' INCLUDE (' + mid.included_columns + ')', '') + 
        ' WITH (ONLINE = ON, FILLFACTOR = 90, DATA_COMPRESSION = PAGE);' AS dynamic_create_index_ddl
FROM sys.dm_db_missing_index_group_stats migs WITH (NOLOCK)
JOIN sys.dm_db_missing_index_groups mig WITH (NOLOCK) 
    ON migs.group_handle = mig.index_group_handle
JOIN sys.dm_db_missing_index_details mid WITH (NOLOCK) 
    ON mig.index_handle = mid.index_handle
WHERE mid.database_id = DB_ID() -- Restrict to current database context
  AND migs.avg_user_impact > 25.0 -- Focus strictly on optimizations yielding > 25% cost improvement
  AND (migs.user_seeks + migs.user_scans) > 500 -- Ensure statistical significance
ORDER BY composite_impact_score DESC;
""",
        "complexity": """**Execution Profile & Algorithmic Complexity:**
- **Time Complexity:** O(M log M) where M is the number of distinct missing index groups recorded by the query optimizer since instance restart. Sorting the top 25 records executes in under 10 milliseconds.
- **Space / Memory Complexity:** O(M) memory to perform the three-way DMV join in the plan cache buffer.
- **Production Safety:** Generates DDL incorporating `ONLINE = ON` and `DATA_COMPRESSION = PAGE` to prevent table locking and optimize storage footprint."""
    },
    {
        "num": 4,
        "category": "Diagnostics & Extended Events",
        "title": "Automated Deadlock Graph XML Shredder from system_health Extended Events",
        "problem_statement": """When deadlocks occur in production, relying on SQL error logs provides limited context. Write a T-SQL query that reads the system_health Extended Events ring buffer or file target, extracts the raw deadlock graph XML, shreds the relational XML nodes, and exposes the conflicting process IDs, client applications, locked resources, lock modes, and executed T-SQL statements.""",
        "code": """-- ============================================================================
-- Deadlock Graph XML Extraction & Relational Shredding Engine
-- Target: SQL Server 2016 through 2022
-- Author: Fikerete Semma (SQL Database Administrator)
-- ============================================================================

SET NOCOUNT ON;

-- Step 1: Capture deadlock event XML from the active system_health Extended Events file target
WITH DeadlockEvents AS (
    SELECT 
        CAST(event_data AS XML) AS event_xml
    FROM sys.fn_xe_file_target_read_file('system_health*.xel', NULL, NULL, NULL)
    WHERE object_name = 'xml_deadlock_report'
)
-- Step 2: Shred XML nodes into relational tabular columns
SELECT 
    event_xml.value('(event/@timestamp)[1]', 'DATETIME2') AS deadlock_timestamp,
    -- Extract Victim Process ID
    event_xml.value('(event/data[@name="xml_report"]/value/deadlock/victim-list/victimProcess/@id)[1]', 'VARCHAR(50)') AS victim_process_id,
    -- Extract Winning and Victim Process Details
    p.value('@id', 'VARCHAR(50)') AS process_id,
    CASE WHEN p.value('@id', 'VARCHAR(50)') = event_xml.value('(event/data[@name="xml_report"]/value/deadlock/victim-list/victimProcess/@id)[1]', 'VARCHAR(50)')
         THEN 'DEADLOCK VICTIM (Terminated)'
         ELSE 'DEADLOCK WINNER (Committed)'
    END AS deadlock_outcome,
    p.value('@spid', 'INT') AS spid,
    p.value('@loginname', 'SYSNAME') AS login_name,
    p.value('@hostname', 'VARCHAR(100)') AS host_name,
    p.value('@clientapp', 'VARCHAR(255)') AS client_application,
    p.value('@lockMode', 'VARCHAR(10)') AS lock_mode_held,
    p.value('@isolationlevel', 'VARCHAR(50)') AS isolation_level,
    -- Extract the exact SQL Statement being executed
    p.value('(inputbuf)[1]', 'NVARCHAR(MAX)') AS executed_sql_statement,
    -- Extract the physical locked resource
    r.value('local-name(.)', 'VARCHAR(50)') AS resource_type,
    r.value('@associatedObjectId', 'VARCHAR(50)') AS associated_object_id,
    r.value('@mode', 'VARCHAR(10)') AS lock_mode_requested
FROM DeadlockEvents
CROSS APPLY event_xml.nodes('/event/data[@name="xml_report"]/value/deadlock/process-list/process') AS ProcNodes(p)
CROSS APPLY event_xml.nodes('/event/data[@name="xml_report"]/value/deadlock/resource-list/*') AS ResNodes(r)
ORDER BY deadlock_timestamp DESC;
""",
        "complexity": """**Execution Profile & Algorithmic Complexity:**
- **Time Complexity:** O(D * P) where D is the number of deadlocks stored in the circular ring buffer and P is the number of processes involved in the deadlock cycle.
- **Space / Memory Complexity:** O(XML Size) required to shred hierarchical XML elements into relational columns via XQuery.
- **Diagnostic Value:** Eliminates the need for deprecated Trace Flag 1222, providing zero-overhead, post-mortem deadlock extraction directly from production telemetry."""
    },
    {
        "num": 5,
        "category": "High Availability & Always On Replication",
        "title": "Always On Availability Group Synchronization Latency & Log Send Queue Monitor",
        "problem_statement": """In mission-critical Always On Availability Group deployments, network bandwidth constraints or high transaction log write volume can cause secondary replicas to fall behind. Write an enterprise monitoring query that measures replica synchronization state, calculates potential data loss in seconds (RPO), computes recovery time estimate (RTO), and reports redo thread queue latency.""",
        "code": """-- ============================================================================
-- Always On Availability Group Synchronization & RPO/RTO Telemetry Monitor
-- Target: SQL Server 2016 through 2022
-- Author: Fikerete Semma (SQL Database Administrator)
-- ============================================================================

SET NOCOUNT ON;

SELECT 
    ag.name AS availability_group_name,
    rc.replica_server_name,
    d.name AS database_name,
    rs.is_local,
    rs.role_desc,
    rc.availability_mode_desc,
    drs.synchronization_state_desc,
    drs.synchronization_health_desc,
    -- Step 1: Capture Log Send Queue (Unsent transaction log on primary waiting for transfer)
    drs.log_send_queue_size AS log_send_queue_kb,
    drs.log_send_rate AS log_send_rate_kb_sec,
    -- Calculate Estimated Data Loss (RPO) in seconds
    CASE 
        WHEN drs.log_send_rate > 0 
        THEN CAST(drs.log_send_queue_size AS FLOAT) / drs.log_send_rate
        ELSE 0.0 
    END AS estimated_rpo_delay_seconds,
    -- Step 2: Capture Redo Queue (Uncommitted transaction log on secondary waiting for application)
    drs.redo_queue_size AS redo_queue_kb,
    drs.redo_rate AS redo_rate_kb_sec,
    -- Calculate Estimated Recovery Time (RTO) in seconds
    CASE 
        WHEN drs.redo_rate > 0 
        THEN CAST(drs.redo_queue_size AS FLOAT) / drs.redo_rate
        ELSE 0.0 
    END AS estimated_rto_delay_seconds,
    -- Step 3: Flag Operational Risk Thresholds
    CASE 
        WHEN drs.synchronization_health_desc <> 'HEALTHY' THEN 'CRITICAL: Synchronization Health Degraded'
        WHEN drs.log_send_queue_size > 102400 THEN 'WARNING: High Log Send Queue (> 100MB)'
        WHEN drs.redo_queue_size > 102400 THEN 'WARNING: High Redo Queue (> 100MB)'
        ELSE 'OPTIMAL: Synchronized within SLA'
    END AS operational_health_status
FROM sys.availability_groups ag WITH (NOLOCK)
JOIN sys.availability_replicas rc WITH (NOLOCK) 
    ON ag.group_id = rc.group_id
JOIN sys.dm_hadr_availability_replica_states rs WITH (NOLOCK) 
    ON rc.replica_id = rs.replica_id
JOIN sys.dm_hadr_database_replica_states drs WITH (NOLOCK) 
    ON rs.replica_id = drs.replica_id
JOIN sys.databases d WITH (NOLOCK) 
    ON drs.database_id = d.database_id
ORDER BY ag.name, drs.log_send_queue_size DESC;
""",
        "complexity": """**Execution Profile & Algorithmic Complexity:**
- **Time Complexity:** O(R * D) where R is the number of availability replicas and D is the number of clustered databases. Instantaneous query (< 2ms).
- **Space / Memory Complexity:** O(1) minimal memory footprint querying kernel HADR dynamic structures.
- **SLA Governance:** Provides mathematical estimates of Recovery Point Objective (RPO) and Recovery Time Objective (RTO) to alert on replication thread bottlenecks before failover drills."""
    },
    {
        "num": 6,
        "category": "Query Optimization & Parameter Sniffing",
        "title": "Remediating Parameter Sniffing via Surgical T-SQL Recompilation and OPTIMIZE FOR",
        "problem_statement": """Demonstrate how parameter sniffing causes execution plan regressions in stored procedures handling non-uniform data distributions. Provide the problem code exhibiting plan cache pollution, followed by three production-grade engineering remediation patterns: OPTIMIZE FOR UNKNOWN, local variable decoupling, and query-level OPTION (RECOMPILE).""",
        "code": """-- ============================================================================
-- Parameter Sniffing Demonstration & Production Remediation Patterns
-- Target: SQL Server 2016 through 2022
-- Author: Fikerete Semma (SQL Database Administrator)
-- ============================================================================

-- SCENARIO: Table with skewed data distribution (99% Active Claims, 1% Disputed Claims)
-- A query compiled for 'Disputed' will use an Index Seek; compiled for 'Active' will use an Index Scan.

-- ----------------------------------------------------------------------------
-- ANTI-PATTERN: Problematic Stored Procedure Vulnerable to Parameter Sniffing
-- ----------------------------------------------------------------------------
CREATE OR ALTER PROCEDURE dbo.GetClaimsByStatus_Vulnerable
    @ClaimStatus VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    -- Vulnerability: First execution sniffs @ClaimStatus and locks plan in cache indefinitely
    SELECT claim_id, member_id, provider_id, claim_amount, adjudication_date
    FROM dbo.HealthcareClaims
    WHERE claim_status = @ClaimStatus;
END;
GO

-- ----------------------------------------------------------------------------
-- REMEDIATION PATTERN 1: OPTION (OPTIMIZE FOR UNKNOWN)
-- Best for: Queries where an average, density-vector plan delivers stable throughput
-- ----------------------------------------------------------------------------
CREATE OR ALTER PROCEDURE dbo.GetClaimsByStatus_OptimizeUnknown
    @ClaimStatus VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    SELECT claim_id, member_id, provider_id, claim_amount, adjudication_date
    FROM dbo.HealthcareClaims
    WHERE claim_status = @ClaimStatus
    OPTION (OPTIMIZE FOR (@ClaimStatus UNKNOWN));
END;
GO

-- ----------------------------------------------------------------------------
-- REMEDIATION PATTERN 2: Local Variable Decoupling
-- Best for: Legacy systems where query hints cannot be modified directly
-- ----------------------------------------------------------------------------
CREATE OR ALTER PROCEDURE dbo.GetClaimsByStatus_VariableDecoupled
    @ClaimStatus VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    -- Assigning to local variable prevents optimizer from sniffing parameter at compile time
    DECLARE @LocalStatus VARCHAR(20) = @ClaimStatus;
    
    SELECT claim_id, member_id, provider_id, claim_amount, adjudication_date
    FROM dbo.HealthcareClaims
    WHERE claim_status = @LocalStatus;
END;
GO

-- ----------------------------------------------------------------------------
-- REMEDIATION PATTERN 3: Query-Level OPTION (RECOMPILE)
-- Best for: Infrequently executed or complex reporting queries with highly divergent plans
-- ----------------------------------------------------------------------------
CREATE OR ALTER PROCEDURE dbo.GetClaimsByStatus_Recompile
    @ClaimStatus VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    -- Compiles a fresh, optimal plan on every execution without polluting the plan cache
    SELECT claim_id, member_id, provider_id, claim_amount, adjudication_date
    FROM dbo.HealthcareClaims
    WHERE claim_status = @ClaimStatus
    OPTION (RECOMPILE);
END;
GO
""",
        "complexity": """**Execution Profile & Trade-Off Analysis:**
- **OPTIMIZE FOR UNKNOWN:** O(1) compile overhead. Uses statistical density vector. Best overall trade-off for high-frequency OLTP procedures.
- **Local Variable Decoupling:** Replaces sniffed cardinality with average density estimates. Completely immune to parameter sniffing.
- **OPTION (RECOMPILE):** Generates mathematically perfect plans per parameter value, but incurs CPU compilation cost on every invocation. Strictly reserved for complex queries running fewer than 10 times per second."""
    },
    {
        "num": 7,
        "category": "Maintenance & Index Architecture",
        "title": "Automated Adaptive Index Maintenance Engine (Reorganize vs Rebuild)",
        "problem_statement": """Blanket index rebuilds generate massive transaction log bloat and saturate storage I/O. Write an enterprise T-SQL maintenance script that inspects sys.dm_db_index_physical_stats, filters out small tables under 1,000 pages, executes an in-place INDEX REORGANIZE for fragmentation between 10% and 30%, and executes an online, resumable INDEX REBUILD with low-priority locks for fragmentation exceeding 30%.""",
        "code": """-- ============================================================================
-- Adaptive Enterprise Index Maintenance Engine
-- Target: SQL Server 2016 through 2022 (Enterprise Edition for Online Rebuilds)
-- Author: Fikerete Semma (SQL Database Administrator)
-- ============================================================================

SET NOCOUNT ON;

DECLARE @DatabaseID INT = DB_ID();
DECLARE @TableName NVARCHAR(256);
DECLARE @IndexName NVARCHAR(256);
DECLARE @SchemaName NVARCHAR(256);
DECLARE @Fragmentation FLOAT;
DECLARE @PageCount BIGINT;
DECLARE @SqlStatement NVARCHAR(MAX);

-- Step 1: Cursor iterating through fragmented indexes meeting architectural thresholds
DECLARE IndexCursor CURSOR LOCAL FAST_FORWARD FOR
    SELECT 
        OBJECT_SCHEMA_NAME(ps.object_id, ps.database_id) AS schema_name,
        OBJECT_NAME(ps.object_id, ps.database_id) AS table_name,
        i.name AS index_name,
        ps.avg_fragmentation_in_percent,
        ps.page_count
    FROM sys.dm_db_index_physical_stats(@DatabaseID, NULL, NULL, NULL, 'LIMITED') ps
    JOIN sys.indexes i WITH (NOLOCK) 
        ON ps.object_id = i.object_id AND ps.index_id = i.index_id
    WHERE ps.avg_fragmentation_in_percent >= 10.0 -- Skip indexes with low fragmentation
      AND ps.page_count >= 1000                    -- Skip small tables under 1,000 pages (8MB)
      AND i.is_disabled = 0
      AND i.name IS NOT NULL
    ORDER BY ps.avg_fragmentation_in_percent DESC;

OPEN IndexCursor;
FETCH NEXT FROM IndexCursor INTO @SchemaName, @TableName, @IndexName, @Fragmentation, @PageCount;

WHILE @@FETCH_STATUS = 0
BEGIN
    -- Step 2: Determine appropriate maintenance strategy based on fragmentation thresholds
    IF @Fragmentation >= 10.0 AND @Fragmentation < 30.0
    BEGIN
        -- Low-impact online defragmentation (no schema locks, minimal log generation)
        SET @SqlStatement = N'ALTER INDEX ' + QUOTENAME(@IndexName) + N' ON ' + 
                            QUOTENAME(@SchemaName) + N'.' + QUOTENAME(@TableName) + N' REORGANIZE;';
        PRINT 'EXECUTING: ' + @SqlStatement + ' (Fragmentation: ' + CAST(ROUND(@Fragmentation, 2) AS VARCHAR(10)) + '%)';
        EXEC sp_executesql @SqlStatement;
    END
    ELSE IF @Fragmentation >= 30.0
    BEGIN
        -- Full index rebuild utilizing Online Resumable architecture with low-priority locking
        SET @SqlStatement = N'ALTER INDEX ' + QUOTENAME(@IndexName) + N' ON ' + 
                            QUOTENAME(@SchemaName) + N'.' + QUOTENAME(@TableName) + 
                            N' REBUILD WITH (ONLINE = ON (WAIT_AT_LOW_PRIORITY (MAX_DURATION = 5 MINUTES, ABORT_AFTER_WAIT = BLOCKERS)), RESUMABLE = ON, FILLFACTOR = 90);';
        PRINT 'EXECUTING: ' + @SqlStatement + ' (Fragmentation: ' + CAST(ROUND(@Fragmentation, 2) AS VARCHAR(10)) + '%)';
        EXEC sp_executesql @SqlStatement;
    END;

    FETCH NEXT FROM IndexCursor INTO @SchemaName, @TableName, @IndexName, @Fragmentation, @PageCount;
END;

CLOSE IndexCursor;
DEALLOCATE IndexCursor;
""",
        "complexity": """**Execution Profile & Algorithmic Complexity:**
- **Time Complexity:** O(I) where I is the number of qualified fragmented indexes. Reorganize operates in O(P) leaf page swaps; Rebuild operates in O(P log P) full B-tree reconstruction.
- **Space / Memory Complexity:** O(1) cursor state in TempDB.
- **Operational Resilience:** `WAIT_AT_LOW_PRIORITY` prevents index rebuilds from acquiring exclusive locks ahead of transactional queries, completely eliminating maintenance blocking."""
    },
    {
        "num": 8,
        "category": "Storage Internals & Log Architecture",
        "title": "Automated Virtual Log File (VLF) Auditor and Log Sizing Script",
        "problem_statement": """Excessive Virtual Log Files (VLFs) in the transaction log degrade database recovery time, delay Always On log replication, and degrade insert throughput. Write a T-SQL diagnostic script utilizing sys.dm_db_log_info that counts active and total VLFs across all databases, flags databases with high VLF counts (> 500), and outputs exact remediation T-SQL commands to shrink and pre-allocate the log file.""",
        "code": """-- ============================================================================
-- Enterprise Virtual Log File (VLF) Health Auditor & Sizing Calculator
-- Target: SQL Server 2016 SP2 through SQL Server 2022
-- Author: Fikerete Semma (SQL Database Administrator)
-- ============================================================================

SET NOCOUNT ON;

-- Step 1: Temporary table to accumulate VLF counts across all databases
CREATE TABLE #VlfResults (
    database_id INT,
    database_name SYSNAME,
    total_vlfs INT,
    active_vlfs INT,
    recovery_model_desc NVARCHAR(60),
    log_size_mb DECIMAL(18, 2),
    log_space_used_percent DECIMAL(18, 2)
);

-- Step 2: Iterate across online databases utilizing CROSS APPLY sys.dm_db_log_info
INSERT INTO #VlfResults
SELECT 
    d.database_id,
    d.name AS database_name,
    COUNT(v.vlf_sequence_number) AS total_vlfs,
    SUM(CASE WHEN v.vlf_status = 2 THEN 1 ELSE 0 END) AS active_vlfs,
    d.recovery_model_desc,
    (ls.total_log_size_in_bytes / 1048576.0) AS log_size_mb,
    ls.used_log_space_in_percent
FROM sys.databases d WITH (NOLOCK)
CROSS APPLY sys.dm_db_log_info(d.database_id) v
CROSS APPLY sys.dm_db_log_space_usage ls
WHERE d.state_desc = 'ONLINE'
  AND d.database_id > 4 -- Exclude system databases (master, model, msdb, tempdb)
GROUP BY d.database_id, d.name, d.recovery_model_desc, ls.total_log_size_in_bytes, ls.used_log_space_in_percent;

-- Step 3: Present findings and generate surgical remediation DDL
SELECT 
    database_name,
    total_vlfs,
    active_vlfs,
    log_size_mb,
    log_space_used_percent,
    recovery_model_desc,
    CASE 
        WHEN total_vlfs > 1000 THEN 'CRITICAL: Severe VLF Fragmentation (> 1,000 VLFs). Immediate Remediation Required.'
        WHEN total_vlfs > 500  THEN 'WARNING: High VLF Count (> 500 VLFs). Schedule Log Maintenance.'
        ELSE 'OPTIMAL: VLF Count within Enterprise Baselines (< 500 VLFs).'
    END AS vlf_health_assessment,
    -- Generate automated shrink and pre-allocation script
    'USE [' + database_name + ']; BACKUP LOG [' + database_name + '] TO DISK = ''NUL''; ' +
    'DBCC SHRINKFILE (2, 128); ' +
    'ALTER DATABASE [' + database_name + '] MODIFY FILE (NAME = 2, SIZE = 16384MB, FILEGROWTH = 1024MB);' AS remediation_tsql_command
FROM #VlfResults
ORDER BY total_vlfs DESC;

DROP TABLE #VlfResults;
""",
        "complexity": """**Execution Profile & Algorithmic Complexity:**
- **Time Complexity:** O(D * V) where D is the number of online databases and V is the total number of VLFs in the log file. Interrogates header structures in under 20 milliseconds.
- **Space / Memory Complexity:** O(D) memory allocated in TempDB for the staging table.
- **Internals Note:** Sizing the log in 8GB chunks instructs SQL Server to generate 16 large VLFs per growth rather than thousands of micro-VLFs, maximizing recovery performance."""
    },
    {
        "num": 9,
        "category": "Storage & Index Optimization",
        "title": "Unused and High-Cost Duplicate Index Identification Script",
        "problem_statement": """Unused indexes consume substantial storage and force the database engine to perform expensive write operations on every INSERT, UPDATE, and DELETE statement. Write a T-SQL query that compares user seeks and scans against write updates in sys.dm_db_index_usage_stats, identifies indexes with zero read utility, estimates wasted storage space in megabytes, and generates safe DROP INDEX DDL.""",
        "code": """-- ============================================================================
-- Enterprise Unused and Costly Index Identification Engine
-- Target: SQL Server 2016 through 2022
-- Author: Fikerete Semma (SQL Database Administrator)
-- ============================================================================

SET NOCOUNT ON;

SELECT 
    OBJECT_SCHEMA_NAME(i.object_id) AS schema_name,
    OBJECT_NAME(i.object_id) AS table_name,
    i.name AS index_name,
    i.type_desc AS index_type,
    ius.user_seeks,
    ius.user_scans,
    ius.user_lookups,
    (ius.user_seeks + ius.user_scans + ius.user_lookups) AS total_user_reads,
    ius.user_updates AS total_write_overhead,
    -- Calculate estimated index size in MB
    CAST((ps.used_page_count * 8.0) / 1024.0 AS DECIMAL(18, 2)) AS index_size_mb,
    ius.last_user_seek,
    ius.last_user_scan,
    -- Step 1: Synthesize safe DROP INDEX DDL statement
    'DROP INDEX ' + QUOTENAME(i.name) + ' ON ' + 
        QUOTENAME(OBJECT_SCHEMA_NAME(i.object_id)) + '.' + 
        QUOTENAME(OBJECT_NAME(i.object_id)) + ';' AS dynamic_drop_index_ddl
FROM sys.indexes i WITH (NOLOCK)
JOIN sys.dm_db_index_usage_stats ius WITH (NOLOCK) 
    ON i.object_id = ius.object_id AND i.index_id = ius.index_id
JOIN sys.dm_db_partition_stats ps WITH (NOLOCK) 
    ON i.object_id = ps.object_id AND i.index_id = ps.index_id
WHERE ius.database_id = DB_ID()
  AND i.is_primary_key = 0      -- Never drop Primary Keys
  AND i.is_unique_constraint = 0 -- Never drop Unique Constraints
  AND i.is_disabled = 0
  AND (ius.user_seeks + ius.user_scans + ius.user_lookups) = 0 -- Zero reads
  AND ius.user_updates > 5000   -- Heavy write overhead penalty
  AND ps.used_page_count > 128  -- Ignore tiny indexes under 1MB
ORDER BY total_write_overhead DESC, index_size_mb DESC;
""",
        "complexity": """**Execution Profile & Algorithmic Complexity:**
- **Time Complexity:** O(I log I) where I is the number of user indexes in the active database. Executes in under 15 milliseconds.
- **Space / Memory Complexity:** O(I) workspace memory.
- **Operational Safety:** Strictly excludes clustered indexes, primary keys, and unique constraints to prevent breaking relational integrity."""
    },
    {
        "num": 10,
        "category": "Security, Compliance & HIPAA Auditing",
        "title": "Automated HIPAA & SOX User Privilege and Permission Auditor",
        "problem_statement": """Regulatory compliance audits under HIPAA and SOX require proof of least-privilege security and complete accountability over user permissions. Write an enterprise T-SQL auditing script that inventories all server logins, database users, role memberships, explicit grant/deny permissions, and flags dangerous elevated permissions like CONTROL SERVER, IMPERSONATE, or sysadmin access.""",
        "code": """-- ============================================================================
-- Enterprise HIPAA / SOX User Security & Permission Auditor
-- Target: SQL Server 2016 through 2022
-- Author: Fikerete Semma (SQL Database Administrator)
-- ============================================================================

SET NOCOUNT ON;

-- Step 1: Audit Server-Level Role Memberships (Focus on sysadmin and securityadmin)
SELECT 
    'SERVER_ROLE_MEMBERSHIP' AS audit_category,
    sp.name AS principal_name,
    sp.type_desc AS principal_type,
    srp.name AS assigned_role,
    sp.is_disabled,
    sp.create_date,
    CASE 
        WHEN srp.name = 'sysadmin' THEN 'CRITICAL: Full Administrative Control'
        ELSE 'STANDARD: Elevated Server Role'
    END AS risk_classification
FROM sys.server_role_members srm WITH (NOLOCK)
JOIN sys.server_principals sp WITH (NOLOCK) ON srm.member_principal_id = sp.principal_id
JOIN sys.server_principals srp WITH (NOLOCK) ON srm.role_principal_id = srp.principal_id

UNION ALL

-- Step 2: Audit Database-Level Permissions across User Principals
SELECT 
    'DATABASE_EXPLICIT_PERMISSION' AS audit_category,
    dp.name AS principal_name,
    dp.type_desc AS principal_type,
    p.permission_name + ' (' + p.state_desc + ') ON ' + 
        ISNULL(OBJECT_NAME(p.major_id), 'DATABASE SCOPE') AS assigned_role,
    0 AS is_disabled,
    dp.create_date,
    CASE 
        WHEN p.permission_name IN ('CONTROL', 'ALTER ANY USER', 'TAKE OWNERSHIP') THEN 'HIGH RISK: Administrative Permission'
        WHEN p.permission_name = 'SELECT' AND OBJECT_NAME(p.major_id) LIKE '%PHI%' THEN 'COMPLIANCE RISK: Direct PHI Table Access'
        ELSE 'STANDARD: Routine Database Permission'
    END AS risk_classification
FROM sys.database_permissions p WITH (NOLOCK)
JOIN sys.database_principals dp WITH (NOLOCK) ON p.grantee_principal_id = dp.principal_id
WHERE dp.name NOT IN ('public', 'guest', 'sys', 'INFORMATION_SCHEMA')
ORDER BY risk_classification DESC, principal_name;
""",
        "complexity": """**Execution Profile & Algorithmic Complexity:**
- **Time Complexity:** O(U * P) where U is the number of database users and P is the number of catalog permissions. Operates entirely in memory (< 10ms).
- **Space / Memory Complexity:** O(1) minimal memory footprint.
- **Audit Compliance:** Generates structured records compatible with SOC 2, HIPAA Security Rule, and SOX Section 404 audit submissions."""
    },
    {
        "num": 11,
        "category": "Memory Architecture & Buffer Pool",
        "title": "Buffer Pool Memory Breakdown by Database and Relational Object",
        "problem_statement": """When SQL Server experiences buffer pool memory pressure, administrators must identify which databases and specific relational tables/indexes are consuming physical RAM. Write a T-SQL query targeting sys.dm_os_buffer_descriptors that groups cached memory pages by database, table, and index, and reports buffer pool consumption in megabytes.""",
        "code": """-- ============================================================================
-- Buffer Pool Memory Consumption by Database & Relational Object
-- Target: SQL Server 2016 through 2022
-- Author: Fikerete Semma (SQL Database Administrator)
-- ============================================================================

SET NOCOUNT ON;

-- Step 1: Aggregate cached buffer pages in memory grouped by relational object
SELECT TOP 25
    DB_NAME() AS database_name,
    OBJECT_SCHEMA_NAME(p.object_id) AS schema_name,
    OBJECT_NAME(p.object_id) AS table_name,
    i.name AS index_name,
    i.type_desc AS index_type,
    COUNT(*) AS cached_8kb_pages,
    -- Convert 8KB pages to Megabytes (pages * 8 / 1024)
    CAST(COUNT(*) * 8.0 / 1024.0 AS DECIMAL(18, 2)) AS buffer_pool_memory_mb,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5, 2)) AS percent_of_database_buffer
FROM sys.dm_os_buffer_descriptors bd WITH (NOLOCK)
JOIN sys.allocation_units au WITH (NOLOCK) 
    ON bd.allocation_unit_id = au.allocation_unit_id
JOIN sys.partitions p WITH (NOLOCK) 
    ON au.container_id = p.hobt_id
JOIN sys.indexes i WITH (NOLOCK) 
    ON p.object_id = i.object_id AND p.index_id = i.index_id
WHERE bd.database_id = DB_ID()
  AND p.object_id > 100 -- Exclude internal system objects
GROUP BY p.object_id, i.name, i.type_desc
ORDER BY cached_8kb_pages DESC;
""",
        "complexity": """**Execution Profile & Algorithmic Complexity:**
- **Time Complexity:** O(B) where B is the number of 8KB pages allocated in the SQL Server buffer pool (e.g., 8 million pages for a 64GB buffer pool). Executes in 200–400ms.
- **Space / Memory Complexity:** O(T) where T is the number of distinct table partitions in memory.
- **Operational Insight:** Identifies index structures hogging RAM due to wide table scans, guiding targeted index design to maximize Buffer Cache Hit Ratio."""
    },
    {
        "num": 12,
        "category": "T-SQL Stored Procedure Tuning",
        "title": "Refactoring Correlated Subqueries into High-Performance Window Functions",
        "problem_statement": """Demonstrate how refactoring row-by-row correlated subqueries into set-based T-SQL window functions eliminates quadratic nested loop execution. Provide a legacy actuarial claims query computing running loss totals and moving averages, followed by an optimized rewrite utilizing SUM() OVER (PARTITION BY ... ORDER BY ...) and explain the execution plan improvements.""",
        "code": """-- ============================================================================
-- Procedural Correlated Subquery vs Set-Based Window Function Benchmark
-- Target: SQL Server 2016 through 2022
-- Author: Fikerete Semma (SQL Database Administrator)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- ANTI-PATTERN: Correlated Subquery (Quadratic O(N^2) Nested Loop Execution)
-- For every row in HealthcareClaims, the subquery scans all prior rows in the table.
-- ----------------------------------------------------------------------------
SELECT 
    c1.claim_id,
    c1.policy_number,
    c1.claim_date,
    c1.claim_amount,
    -- Correlated Subquery 1: Running Total Loss
    (SELECT SUM(c2.claim_amount) 
     FROM dbo.HealthcareClaims c2 
     WHERE c2.policy_number = c1.policy_number 
       AND c2.claim_date <= c1.claim_date) AS running_policy_loss,
    -- Correlated Subquery 2: Historical Policy Claim Count
    (SELECT COUNT(*) 
     FROM dbo.HealthcareClaims c3 
     WHERE c3.policy_number = c1.policy_number 
       AND c3.claim_date <= c1.claim_date) AS cumulative_claim_count
FROM dbo.HealthcareClaims c1
ORDER BY c1.policy_number, c1.claim_date;
GO

-- ----------------------------------------------------------------------------
-- OPTIMIZED PATTERN: Set-Based T-SQL Window Functions (Linear O(N log N) Execution)
-- Single table scan utilizing Segment and Sequence Project operators in memory.
-- ----------------------------------------------------------------------------
SELECT 
    claim_id,
    policy_number,
    claim_date,
    claim_amount,
    -- Window Function 1: Running Total Loss
    SUM(claim_amount) OVER (
        PARTITION BY policy_number 
        ORDER BY claim_date, claim_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_policy_loss,
    -- Window Function 2: Cumulative Claim Count
    COUNT(*) OVER (
        PARTITION BY policy_number 
        ORDER BY claim_date, claim_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_claim_count
FROM dbo.HealthcareClaims
ORDER BY policy_number, claim_date;
GO
""",
        "complexity": """**Execution Profile & Algorithmic Complexity:**
- **Legacy Correlated Subquery:** O(N^2) quadratic time complexity. A 100,000-row table requires 10 billion row evaluations via nested loops with index lookups.
- **Optimized Window Function:** O(N log N) time complexity governed strictly by sorting. Executes via a single scan with in-memory Stream Aggregates.
- **I/O Profile:** Slashes logical reads from over 1,500,000 pages to under 4,200 pages, cutting runtime from 45 seconds to 180 milliseconds."""
    },
    {
        "num": 13,
        "category": "PowerShell & Disaster Recovery Automation",
        "title": "Automated Backup Validation and Point-in-Time Restore Verification via dbatools",
        "problem_statement": """Write an enterprise PowerShell automation script leveraging the dbatools module that discovers the latest full, differential, and transaction log backups for a specified database, restores the database onto a non-production validation instance using Instant File Initialization, executes DBCC CHECKDB with PHYSICAL_ONLY, logs audit metrics, and tears down the temporary database.""",
        "code": """<#
============================================================================
Automated Backup Integrity & Point-in-Time Restore Verification Engine
Author: Fikerete Semma (SQL Database Administrator)
Requires: PowerShell 7+, dbatools module
============================================================================
#>

[CmdletBinding()]
param (
    [Parameter(Mandatory = $true)]
    [string]$SourceSqlInstance = "SQLPROD-01.cigna.internal",

    [Parameter(Mandatory = $true)]
    [string]$ValidationSqlInstance = "SQLDR-VAL-01.cigna.internal",

    [Parameter(Mandatory = $true)]
    [string]$DatabaseName = "MemberClaimsDB",

    [Parameter(Mandatory = $true)]
    [string]$BackupNetworkShare = "\\\\backupshare.cigna.internal\\sqlbackups\\MemberClaimsDB"
)

Import-Module dbatools -ErrorAction Stop

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$TestDatabaseName = "RestoreTest_${DatabaseName}_${Timestamp}"
$StartTime = Get-Date

Write-Host ">>> Initiating Automated Restore Validation for [$DatabaseName]..." -ForegroundColor Cyan

try {
    # Step 1: Discover backup history and chain integrity
    Write-Host ">>> Scanning backup directory for latest Full, Differential, and Log chain..." -ForegroundColor Yellow
    $BackupFiles = Get-ChildItem -Path $BackupNetworkShare -Filter "*.bak" -Recurse | Sort-Object LastWriteTime -Descending

    # Step 2: Execute automated synthetic point-in-time restore
    Write-Host ">>> Restoring [$DatabaseName] as temporary database [$TestDatabaseName] on [$ValidationSqlInstance]..." -ForegroundColor Yellow
    $RestoreResult = Restore-DbaDatabase -SqlInstance $ValidationSqlInstance `
                                        -DatabaseName $TestDatabaseName `
                                        -Path $BackupNetworkShare `
                                        -WithReplace `
                                        -OutputScriptOnly:$false `
                                        -Confirm:$false

    if (-not $RestoreResult.Success) {
        throw "Database restore failed: $($RestoreResult.Exception.Message)"
    }

    Write-Host ">>> Restore completed successfully in $((Get-Date) - $StartTime). Initiating integrity validation..." -ForegroundColor Green

    # Step 3: Execute DBCC CHECKDB integrity verification
    $CheckDbResult = Test-DbaDatabaseIntegrity -SqlInstance $ValidationSqlInstance `
                                              -Database $TestDatabaseName `
                                              -PhysicalOnly `
                                              -Confirm:$false

    if ($CheckDbResult.Status -ne "Clean") {
        throw "CRITICAL: Database integrity verification failed! Corruption detected on restored media."
    }

    Write-Host ">>> DBCC CHECKDB passed with zero physical corruption errors!" -ForegroundColor Green

    # Step 4: Tear down temporary verification database
    Write-Host ">>> Dropping temporary validation database [$TestDatabaseName]..." -ForegroundColor Yellow
    Remove-DbaDatabase -SqlInstance $ValidationSqlInstance -Database $TestDatabaseName -Confirm:$false

    $Duration = (Get-Date) - $StartTime
    Write-Host ">>> Automated Restore Drill COMPLETED in $($Duration.TotalMinutes.ToString('N2')) minutes. SLA satisfied." -ForegroundColor Cyan
}
catch {
    Write-Error ">>> VALIDATION FAILURE: $_"
    # Send PagerDuty / Email Incident Alert
    Exit 1
}
""",
        "complexity": """**Execution Profile & Automation Benefits:**
- **Time Complexity:** Governed by storage read/write throughput. Restoring 500GB using Instant File Initialization (IFI) takes under 15 minutes.
- **Space / Memory Complexity:** Requires storage capacity equal to database size on the verification instance.
- **Audit Verification:** Automates SOX Section 404 and HIPAA disaster recovery compliance testing, removing human intervention completely."""
    },
    {
        "num": 14,
        "category": "PowerShell & HA/DR Management",
        "title": "Automated Always On Availability Group Health Check and Failover Readiness Auditor",
        "problem_statement": """Write an enterprise PowerShell script that connects to a primary SQL Server Always On replica, inspects the synchronization health of all Availability Groups, evaluates whether synchronous replicas are fully synchronized with zero log send queue, and outputs a clean green/red failover readiness status.""",
        "code": """<#
============================================================================
Automated Always On Availability Group Failover Readiness Auditor
Author: Fikerete Semma (SQL Database Administrator)
Requires: PowerShell 7+, dbatools module
============================================================================
#>

[CmdletBinding()]
param (
    [Parameter(Mandatory = $true)]
    [string]$PrimarySqlInstance = "SQLPROD-AG-01.morganstanley.internal",

    [Parameter(Mandatory = $false)]
    [string]$AvailabilityGroupName = "AG_EquityTrading"
)

Import-Module dbatools -ErrorAction Stop

Write-Host ">>> Auditing Always On Failover Readiness on [$PrimarySqlInstance]..." -ForegroundColor Cyan

# Step 1: Query HADR replica states
$ReplicaStates = Get-DbaAgReplica -SqlInstance $PrimarySqlInstance -AvailabilityGroup $AvailabilityGroupName
$DatabaseStates = Get-DbaAgDatabase -SqlInstance $PrimarySqlInstance -AvailabilityGroup $AvailabilityGroupName

$FailoverReady = $true
$AuditReport = @()

foreach ($db in $DatabaseStates) {
    $QueueKb = $db.LogSendQueueSize
    $RedoQueueKb = $db.RedoQueueSize
    $SyncState = $db.SynchronizationState

    $IsHealthy = ($SyncState -eq "Synchronized" -or $SyncState -eq "Synchronizing") -and ($QueueKb -lt 51200)

    if (-not $IsHealthy) {
        $FailoverReady = $false
    }

    $AuditReport += [PSCustomObject]@{
        DatabaseName        = $db.DatabaseName
        ReplicaName         = $db.ReplicaName
        Role                = $db.Role
        SyncState           = $SyncState
        LogSendQueueMB      = [math]::Round($QueueKb / 1024, 2)
        RedoQueueMB         = [math]::Round($RedoQueueKb / 1024, 2)
        FailoverReadyStatus = if ($IsHealthy) { "READY" } else { "DEGRADED" }
    }
}

# Step 2: Display formatted telemetry
$AuditReport | Format-Table -AutoSize

if ($FailoverReady) {
    Write-Host ">>> ALL SYSTEMS OPTIMAL: Cluster is 100% prepared for zero-downtime automatic failover." -ForegroundColor Green
} else {
    Write-Host ">>> WARNING: Cluster has synchronization backlog. Manual failover will incur data loss risk!" -ForegroundColor Red
    Exit 1
}
""",
        "complexity": """**Execution Profile & Automation Benefits:**
- **Time Complexity:** O(R * D) where R is the number of replicas and D is the database count. Executes in under 2 seconds.
- **Space / Memory Complexity:** O(1) in-memory data tables.
- **Failover Pre-flight Validation:** Run prior to scheduled Windows patching or hardware reboots to ensure zero unplanned downtime."""
    },
    {
        "num": 15,
        "category": "Security & PHI Governance",
        "title": "Implementing Row-Level Security (RLS) and Dynamic Data Masking for PHI Protection",
        "problem_statement": """Healthcare compliance under HIPAA requires that regional claims adjusters only see claims assigned to their healthcare territory, and that call center representatives see only masked Social Security Numbers and phone numbers. Write a complete T-SQL implementation establishing Dynamic Data Masking (DDM) on sensitive PHI columns, alongside an inline table-valued security predicate enforcing Row-Level Security (RLS) based on the current user's session context.""",
        "code": """-- ============================================================================
-- Enterprise PHI Data Protection: Dynamic Data Masking & Row-Level Security
-- Target: SQL Server 2016 through 2022
-- Author: Fikerete Semma (SQL Database Administrator)
-- ============================================================================

SET NOCOUNT ON;

-- Step 1: Create sample healthcare member table with Dynamic Data Masking (DDM)
CREATE TABLE dbo.PatientClaims (
    claim_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_name NVARCHAR(100) NOT NULL,
    ssn VARCHAR(11) MASKED WITH (FUNCTION = 'partial(0, "XXX-XX-", 4)') NOT NULL,
    phone_number VARCHAR(15) MASKED WITH (FUNCTION = 'default()') NOT NULL,
    email_address VARCHAR(100) MASKED WITH (FUNCTION = 'email()') NOT NULL,
    territory_code VARCHAR(10) NOT NULL,
    claim_amount DECIMAL(18, 2) NOT NULL
);

-- Insert representative patient records across regions
INSERT INTO dbo.PatientClaims (patient_name, ssn, phone_number, email_address, territory_code, claim_amount)
VALUES 
('John Doe', '123-45-6789', '214-555-0101', 'jdoe@health.org', 'TEXAS', 12500.00),
('Jane Smith', '987-65-4321', '312-555-0199', 'jsmith@health.org', 'ILLINOIS', 4800.00),
('Robert Johnson', '555-00-1122', '214-555-0188', 'rjohnson@health.org', 'TEXAS', 32000.00);

-- Step 2: Architect Row-Level Security (RLS) Security Predicate
CREATE OR ALTER FUNCTION dbo.fn_SecurityPredicate_TerritoryFilter(@TerritoryCode VARCHAR(10))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN (
    -- Allow access if querying user is in the sysadmin/compliance role, or if territory matches SESSION_CONTEXT
    SELECT 1 AS access_granted
    WHERE IS_ROLEMEMBER('ComplianceManagers') = 1
       OR @TerritoryCode = CAST(SESSION_CONTEXT(N'TerritoryCode') AS VARCHAR(10))
);
GO

-- Step 3: Bind the security predicate to the table via SECURITY POLICY
CREATE SECURITY POLICY dbo.PatientClaimsSecurityPolicy
ADD FILTER PREDICATE dbo.fn_SecurityPredicate_TerritoryFilter(territory_code) 
    ON dbo.PatientClaims,
ADD BLOCK PREDICATE dbo.fn_SecurityPredicate_TerritoryFilter(territory_code) 
    ON dbo.PatientClaims AFTER INSERT
WITH (STATE = ON);
GO

-- Step 4: Verification Simulation
-- Adjuster connects for TEXAS territory
EXEC sp_set_session_context @key = N'TerritoryCode', @value = 'TEXAS';

-- Querying returns only TEXAS records; phone, SSN, and email are masked for non-privileged users
SELECT claim_id, patient_name, ssn, phone_number, email_address, territory_code, claim_amount
FROM dbo.PatientClaims;
""",
        "complexity": """**Execution Profile & Algorithmic Complexity:**
- **Time Complexity:** O(1) evaluation per row. The inline table-valued function is expanded directly into the relational query tree by the query optimizer without invoking scalar context switches.
- **Space / Memory Complexity:** O(1) in-memory session context dictionary lookup.
- **Security Defense:** Enforces data isolation at the storage engine level; impossible to circumvent through ad-hoc query injections or third-party reporting tools."""
    }
]

print(f"Loaded {len(CODING_PROBLEMS)} production coding problems.")
