## 4. Coding & Problem Solving: 21 LiveCode Questions

In Amazon’s **LiveCode** platform, candidates write code in real time without access to an IDE or code execution. The interviewer observes your thought process, algorithmic clarity, edge-case handling, and ability to derive machine learning math from first principles.

---

### Problem 1: [SQL / Redshift] Consecutive Event Gaps & Threshold Flagging

#### Problem Statement
In an **Amazon Fulfillment Center**, automated package scanners log barcode reading events. Given a table `scanner_events (event_id INT, category VARCHAR, scanned_at TIMESTAMP)`, write a **Redshift SQL** query to:
1. Calculate the time elapsed (in seconds) between consecutive scan events for each category.
2. Compute the average gap between consecutive events per category.
3. Flag any specific event where the gap between consecutive events exceeds 3× the category average gap (indicating a potential conveyor jam or scanner failure).

#### Thought Process
1. Use the **`LAG()`** window function partitioned by `category` and ordered by `scanned_at` to access the timestamp of the immediately preceding event.
2. In **Amazon Redshift**, subtract timestamps or use **`DATEDIFF('second', prev_time, curr_time)`** to obtain elapsed seconds.
3. Compute the per-category average gap across all consecutive transitions using an aggregate or window function **`AVG(gap_seconds) OVER (PARTITION BY category)`**.
4. In an outer query or CTE, evaluate the condition `gap_seconds > 3.0 * avg_category_gap` and produce the flagged record with its corresponding ratio.
5. Handle edge cases: the first event in any category has no preceding event (`LAG` is `NULL`), so it must be excluded from the gap evaluation.

#### Code (SQL - Amazon Redshift)
```sql
-- Step 1: Compute consecutive event gaps using LAG()
WITH EventGaps AS (
    SELECT
        event_id,
        category,
        scanned_at,
        LAG(scanned_at, 1) OVER (
            PARTITION BY category 
            ORDER BY scanned_at ASC
        ) AS prev_scanned_at,
        -- Calculate gap in seconds between consecutive events
        DATEDIFF('second', 
            LAG(scanned_at, 1) OVER (PARTITION BY category ORDER BY scanned_at ASC), 
            scanned_at
        ) AS gap_seconds
    FROM scanner_events
),
-- Step 2: Compute category-level average gap
CategoryAverages AS (
    SELECT
        event_id,
        category,
        scanned_at,
        gap_seconds,
        AVG(gap_seconds * 1.0) OVER (
            PARTITION BY category
        ) AS avg_category_gap
    FROM EventGaps
    WHERE gap_seconds IS NOT NULL -- Exclude first record of each category
)
-- Step 3: Flag events where gap exceeds 3x category average
SELECT
    event_id,
    category,
    scanned_at,
    gap_seconds,
    ROUND(avg_category_gap, 2) AS avg_category_gap,
    ROUND(gap_seconds / NULLIF(avg_category_gap, 0), 2) AS gap_to_avg_ratio,
    CASE 
        WHEN gap_seconds > (3.0 * avg_category_gap) THEN 1 
        ELSE 0 
    END AS is_anomaly_flag
FROM CategoryAverages
ORDER BY category, scanned_at;
```

#### Complexity Analysis
- **Time Complexity**: **O(N log N)**, where $N$ is the total number of scanner events. The bottleneck is sorting the dataset within the window partitions.
- **Space Complexity**: **O(N)** scratch space for sorting and computing window aggregations across partitions.

---

### Problem 2: [SQL / Redshift] Sorter Station Running Sum & Rolling 1-Hour Throughput

#### Problem Statement
Given a table `sorter_telemetry (station_id INT, reading_time TIMESTAMP, units_sorted INT)`, write a query to compute:
1. The **cumulative running total** of units sorted by each station since the start of the day.
2. The **rolling 1-hour throughput** (sum of units sorted in the preceding 60 minutes, inclusive of the current reading).
3. Identify the peak rolling 1-hour throughput recorded for each station.

#### Thought Process
1. Cumulative daily total uses **`SUM(units_sorted) OVER (PARTITION BY station_id, TRUNC(reading_time) ORDER BY reading_time ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`**.
2. For rolling time-based windows in Redshift, timestamp ranges can be represented either via **`RANGE BETWEEN INTERVAL '1 HOUR' PRECEDING AND CURRENT ROW`** (if supported by the dialect version) or via an explicit **self-join** on `reading_time BETWEEN t.reading_time - INTERVAL '1 HOUR' AND t.reading_time`. Using window functions with self-join or standardized range syntax guarantees high compatibility.
3. Compute the maximum of this rolling metric per station using **`DENSE_RANK()`** or windowed **`MAX()`**.

#### Code (SQL - Amazon Redshift)
```sql
-- Step 1: Base table with cumulative running total
WITH CumulativeMetrics AS (
    SELECT
        station_id,
        reading_time,
        units_sorted,
        -- Running sum from beginning of shift/day
        SUM(units_sorted) OVER (
            PARTITION BY station_id, TRUNC(reading_time)
            ORDER BY reading_time ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_daily_units
    FROM sorter_telemetry
),
-- Step 2: Rolling 1-hour throughput calculation via Self-Join
RollingHourlyThroughput AS (
    SELECT
        c1.station_id,
        c1.reading_time,
        c1.units_sorted,
        c1.cumulative_daily_units,
        SUM(c2.units_sorted) AS rolling_1h_units
    FROM CumulativeMetrics c1
    INNER JOIN CumulativeMetrics c2
        ON c1.station_id = c2.station_id
        AND c2.reading_time BETWEEN (c1.reading_time - INTERVAL '1 hour') AND c1.reading_time
    GROUP BY
        c1.station_id,
        c1.reading_time,
        c1.units_sorted,
        c1.cumulative_daily_units
),
-- Step 3: Rank stations to find peak rolling 1-hour window
RankedThroughput AS (
    SELECT
        station_id,
        reading_time AS peak_reading_time,
        rolling_1h_units AS max_rolling_1h_throughput,
        DENSE_RANK() OVER (
            PARTITION BY station_id 
            ORDER BY rolling_1h_units DESC, reading_time ASC
        ) AS rank_order
    FROM RankedThroughput
)
SELECT
    station_id,
    peak_reading_time,
    max_rolling_1h_throughput
FROM RankedThroughput
WHERE rank_order = 1
ORDER BY max_rolling_1h_throughput DESC;
```

#### Complexity Analysis
- **Time Complexity**: **O(N log N)** for the window function; **O(N · K)** for the self-join where K is the average number of readings per hour.
- **Space Complexity**: **O(N)** intermediate buffer storage in Redshift query memory.

---

### Problem 3: [SQL / Redshift] Sessionization of Warehouse Worker Scanning Activity

#### Problem Statement
Associate activity in a fulfillment center consists of item picks. Table `pick_logs (associate_id INT, scan_time TIMESTAMP, sku_id VARCHAR)`. An associate's continuous work period is interrupted if more than **15 minutes** elapse between consecutive scans. Write a query to assign a unique sequential `session_id` to each continuous working session per associate, and compute the total units picked and session duration.

#### Thought Process
1. This is a classic **Sessionization** problem.
2. Step 1: Use **`LAG(scan_time)`** partitioned by `associate_id` ordered by `scan_time`.
3. Step 2: Create an indicator variable `is_new_session = CASE WHEN DATEDIFF('minute', prev_scan_time, scan_time) > 15 OR prev_scan_time IS NULL THEN 1 ELSE 0 END`.
4. Step 3: Compute the cumulative sum of this flag: **`SUM(is_new_session) OVER (PARTITION BY associate_id ORDER BY scan_time ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`**. This cumulative sum creates a unique increasing `session_number` for each continuous work bout!
5. Step 4: Group by `associate_id` and `session_number` to calculate session duration and item count.

#### Code (SQL - Amazon Redshift)
```sql
WITH ScanGaps AS (
    SELECT
        associate_id,
        scan_time,
        sku_id,
        LAG(scan_time) OVER (
            PARTITION BY associate_id 
            ORDER BY scan_time ASC
        ) AS prev_scan_time
    FROM pick_logs
),
SessionFlags AS (
    SELECT
        associate_id,
        scan_time,
        sku_id,
        CASE 
            WHEN prev_scan_time IS NULL THEN 1
            WHEN DATEDIFF('minute', prev_scan_time, scan_time) > 15 THEN 1
            ELSE 0 
        END AS is_new_session
    FROM ScanGaps
),
SessionAssigned AS (
    SELECT
        associate_id,
        scan_time,
        sku_id,
        -- Running sum of session boundaries assigns sequential session IDs
        SUM(is_new_session) OVER (
            PARTITION BY associate_id 
            ORDER BY scan_time ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS session_idx
    FROM SessionFlags
)
SELECT
    associate_id,
    session_idx,
    MIN(scan_time) AS session_start,
    MAX(scan_time) AS session_end,
    DATEDIFF('minute', MIN(scan_time), MAX(scan_time)) AS session_duration_minutes,
    COUNT(sku_id) AS total_units_picked,
    ROUND(COUNT(sku_id) * 60.0 / NULLIF(DATEDIFF('minute', MIN(scan_time), MAX(scan_time)), 0), 1) AS picks_per_hour
FROM SessionAssigned
GROUP BY associate_id, session_idx
ORDER BY associate_id, session_start;
```

#### Complexity Analysis
- **Time Complexity**: **O(N log N)** driven by the window sort order.
- **Space Complexity**: **O(N)** for window state tracking.

---

### Problem 4: [SQL / Redshift] Markov Chain Transition Matrix of Equipment Error Codes

#### Problem Statement
Conveyor sorters generate fault codes during operation: `equipment_faults (conveyor_id INT, fault_time TIMESTAMP, fault_code VARCHAR)`. Amazon WWDE reliability engineers want to find the **top 3 most probable subsequent fault codes** that follow every given fault code, to determine if certain initial sensor warnings trigger catastrophic mechanical shutdowns.

#### Thought Process
1. Use **`LEAD(fault_code)`** partitioned by `conveyor_id` ordered by `fault_time` to find the immediate next fault.
2. Group by `(current_fault_code, next_fault_code)` to count the total transition frequency.
3. Compute the transition probability: `transition_count / SUM(transition_count) OVER (PARTITION BY current_fault_code)`.
4. Rank the subsequent transitions using **`DENSE_RANK()`** and filter for `rank <= 3`.

#### Code (SQL - Amazon Redshift)
```sql
WITH Transitions AS (
    SELECT
        conveyor_id,
        fault_code AS current_fault,
        LEAD(fault_code, 1) OVER (
            PARTITION BY conveyor_id 
            ORDER BY fault_time ASC
        ) AS next_fault
    FROM equipment_faults
),
ValidTransitions AS (
    SELECT
        current_fault,
        next_fault,
        COUNT(*) AS transition_frequency
    FROM Transitions
    WHERE next_fault IS NOT NULL
    GROUP BY current_fault, next_fault
),
TransitionProbabilities AS (
    SELECT
        current_fault,
        next_fault,
        transition_frequency,
        SUM(transition_frequency) OVER (PARTITION BY current_fault) AS total_initial_faults,
        ROUND(transition_frequency * 1.0 / SUM(transition_frequency) OVER (PARTITION BY current_fault), 4) AS transition_prob,
        DENSE_RANK() OVER (
            PARTITION BY current_fault 
            ORDER BY transition_frequency DESC
        ) AS prob_rank
    FROM ValidTransitions
)
SELECT
    current_fault,
    next_fault,
    transition_frequency,
    total_initial_faults,
    transition_prob
FROM TransitionProbabilities
WHERE prob_rank <= 3
ORDER BY current_fault, transition_prob DESC;
```

#### Complexity Analysis
- **Time Complexity**: **O(N log N)** for the window function plus **O(M log M)** where $M$ is the number of distinct transition pairs.
- **Space Complexity**: **O(N)** storage.

---

### Problem 5: [SQL / Redshift] Percentile and Median Package Dwell Time per Zone

#### Problem Statement
Given `package_tracking (package_id VARCHAR, zone_id VARCHAR, entry_time TIMESTAMP, exit_time TIMESTAMP)`, write a query to compute the **50th percentile (Median)**, **90th percentile ($P_{90}$)**, and **99th percentile ($P_{99}$)** dwell time (in minutes) for each warehouse zone, and flag zones where $P_{99} > 120$ minutes.

#### Thought Process
1. Dwell time in minutes is calculated as `DATEDIFF('minute', entry_time, exit_time)`.
2. Amazon Redshift supports **`PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY dwell_minutes)`** as an inverse distribution function.
3. Group by `zone_id` and aggregate percentiles.

#### Code (SQL - Amazon Redshift)
```sql
WITH PackageDwell AS (
    SELECT
        package_id,
        zone_id,
        DATEDIFF('minute', entry_time, exit_time) AS dwell_minutes
    FROM package_tracking
    WHERE exit_time >= entry_time
)
SELECT
    zone_id,
    COUNT(package_id) AS total_packages_processed,
    ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY dwell_minutes), 2) AS p50_median_dwell_mins,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY dwell_minutes), 2) AS p90_dwell_mins,
    ROUND(PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY dwell_minutes), 2) AS p99_dwell_mins,
    CASE 
        WHEN PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY dwell_minutes) > 120.0 THEN 'CRITICAL_BOTTLE_NECK'
        WHEN PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY dwell_minutes) > 60.0 THEN 'WARNING_CONGESTION'
        ELSE 'HEALTHY_FLOW'
    END AS operational_zone_status
FROM PackageDwell
GROUP BY zone_id
ORDER BY p99_dwell_mins DESC;
```

#### Complexity Analysis
- **Time Complexity**: **O(Z · K log K)**, where $Z$ is zones and $K$ is packages per zone (sorting required for exact continuous percentiles).
- **Space Complexity**: **O(N)** intermediate buffer memory.

---

### Problem 6: [Python / Scratch ML] Logistic Regression with L2 Regularization from Scratch

#### Problem Statement
Write a clean, production-grade Python implementation of **Logistic Regression** trained via **Batch Gradient Descent** from scratch using only **NumPy**. Implement the sigmoid activation, Binary Cross-Entropy loss with $L_2$ regularization (Ridge penalty), gradient computation, weight update, and prediction methods.

#### Thought Process
1. **Model Hypothesis**: `ŷ = σ(z) = 1 / (1 + e^-z)`, where `z = Xw + b`.
2. **Objective Function (Cost)**:
   > **J(w, b) = - (1/m) · Σ [ y⁽ⁱ⁾ · log(ŷ⁽ⁱ⁾) + (1 - y⁽ⁱ⁾) · log(1 - ŷ⁽ⁱ⁾) ] + (λ / 2m) · ||w||²**
3. **Gradients**:
   > **∂J/∂w = (1/m) · Xᵀ (ŷ - y) + (λ/m) · w**
> **∂J/∂b = (1/m) · Σ (ŷ⁽ⁱ⁾ - y⁽ⁱ⁾)**
4. Add numerical stability clipping to sigmoid/log inputs to prevent log(0) → -∞ or overflow.

#### Code (Python)
```python
import numpy as np

class ScratchLogisticRegression:
    def __init__(self, learning_rate: float = 0.01, num_iterations: int = 1000, 
                 l2_lambda: float = 0.1, fit_intercept: bool = True):
        self.lr = learning_rate
        self.num_iters = num_iterations
        self.l2_lambda = l2_lambda
        self.fit_intercept = fit_intercept
        self.weights = None
        self.bias = 0.0
        self.loss_history = []

    def _sigmoid(self, z: np.ndarray) -> np.ndarray:
        # Numerically stable sigmoid to prevent overflow
        z = np.clip(z, -500, 500)
        return 1.0 / (1.0 + np.exp(-z))

    def _compute_loss(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        m = y_true.shape[0]
        # Clip probabilities to avoid log(0)
        eps = 1e-15
        y_pred = np.clip(y_pred, eps, 1.0 - eps)
        # Binary Cross-Entropy Loss
        bce = - (1.0 / m) * np.sum(y_true * np.log(y_pred) + (1.0 - y_true) * np.log(1.0 - y_pred))
        # L2 Regularization penalty on weights (do not penalize bias)
        l2_cost = (self.l2_lambda / (2.0 * m)) * np.sum(self.weights ** 2)
        return float(bce + l2_cost)

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'ScratchLogisticRegression':
        m, n = X.shape
        # Initialize parameters
        self.weights = np.zeros(n, dtype=float)
        self.bias = 0.0
        self.loss_history = []

        for iteration in range(self.num_iters):
            # Forward pass: linear combination + activation
            linear_model = np.dot(X, self.weights) + self.bias
            y_pred = self._sigmoid(linear_model)

            # Compute gradients
            error = y_pred - y
            dw = (1.0 / m) * np.dot(X.T, error) + (self.l2_lambda / m) * self.weights
            db = (1.0 / m) * np.sum(error)

            # Gradient descent update
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

            # Track loss every 100 iterations
            if iteration % 100 == 0:
                current_loss = self._compute_loss(y, y_pred)
                self.loss_history.append(current_loss)

        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        linear_model = np.dot(X, self.weights) + self.bias
        return self._sigmoid(linear_model)

    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        probabilities = self.predict_proba(X)
        return (probabilities >= threshold).astype(int)
```

#### Complexity Analysis
- **Time Complexity**: **O(I · m · n)**, where $I$ is iterations, $m$ is number of samples, and $n$ is number of features.
- **Space Complexity**: **O(n)** to store weights and gradients.

---

### Problem 7: [Python / Scratch ML] Linear Regression with Ridge (L2) Regularization via Normal Equation

#### Problem Statement
Implement **Ridge Regression** from scratch using the closed-form **Normal Equation**. Provide an analytical solver that handles matrix inversion singularity checks, adds an intercept term, and fits optimal weights $\hat{w}$.

#### Thought Process
1. Analytical solution for Ridge Regression minimizing ||y - Xw||² + λ ||w||²:
   > **ŵ = (Xᵀ X + λ I')⁻¹ Xᵀ y**
2. Important detail: The bias/intercept term should **not** be regularized. The identity matrix I' must have a 0 at index (0, 0).
3. Check for matrix invertibility using `np.linalg.pinv` (Moore-Penrose pseudo-inverse) for robustness against collinear features.

#### Code (Python)
```python
import numpy as np

class ScratchRidgeRegression:
    def __init__(self, alpha: float = 1.0):
        self.alpha = float(alpha)
        self.weights = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'ScratchRidgeRegression':
        m, n = X.shape
        # Augment X with a column of ones for the intercept
        X_design = np.hstack([np.ones((m, 1)), X])
        
        # Construct regularization penalty matrix (n+1 x n+1)
        # Note: Do NOT regularize the bias term (index 0)
        I_reg = np.eye(n + 1)
        I_reg[0, 0] = 0.0

        # Normal equation with Ridge penalty: (X^T * X + alpha * I)^-1 * X^T * y
        XtX = np.dot(X_design.T, X_design)
        reg_term = self.alpha * I_reg
        XtY = np.dot(X_design.T, y)

        # Solve system of linear equations robustly
        self.weights = np.linalg.solve(XtX + reg_term, XtY)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        m = X.shape[0]
        X_design = np.hstack([np.ones((m, 1)), X])
        return np.dot(X_design, self.weights)

    @property
    def intercept_(self) -> float:
        return float(self.weights[0])

    @property
    def coef_(self) -> np.ndarray:
        return self.weights[1:]
```

#### Complexity Analysis
- **Time Complexity**: **O(n² · m + n³)** where n is feature count and m is sample count.
- **Space Complexity**: **O(n²)** for the (n + 1) × (n + 1) covariance matrix.

---

### Problem 8: [Python / Scratch ML] K-Means Clustering Algorithm from Scratch

#### Problem Statement
Implement the complete **K-Means Clustering** algorithm from scratch in NumPy, including random centroid initialization, Euclidean distance calculation, iterative assignment, centroid re-estimation, and convergence criteria based on tolerance $\epsilon$.

#### Thought Process
1. Initialize K centroids by randomly sampling K unique observation vectors from the dataset.
2. In each iteration:
   - Compute pairwise Euclidean distance between each point x_i and each centroid μ_k:
     > **dist(x_i, μ_k) = √[ Σ (x_ij - μ_kj)² ]**
   - Assign each point to the closest centroid: c_i = argmin_k dist(x_i, μ_k).
   - Update centroids to be the mean of all points assigned to that cluster: μ_k = (1 / |S_k|) · Σ x_i.
   - If a cluster becomes empty, reinitialize its centroid to a random data point.
3. Terminate when centroid movement is less than tolerance ε or max iterations reached.

#### Code (Python)
```python
import numpy as np

class ScratchKMeans:
    def __init__(self, k: int = 3, max_iter: int = 300, tol: float = 1e-4, random_state: int = 42):
        self.k = k
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.centroids = None
        self.inertia_ = 0.0

    def fit(self, X: np.ndarray) -> 'ScratchKMeans':
        np.random.seed(self.random_state)
        n_samples, n_features = X.shape

        # Randomly select k distinct initial data points as centroids
        random_indices = np.random.choice(n_samples, self.k, replace=False)
        self.centroids = X[random_indices].copy()

        for iteration in range(self.max_iter):
            # Compute distance matrix: Shape (n_samples, k)
            distances = np.linalg.norm(X[:, np.newaxis, :] - self.centroids[np.newaxis, :, :], axis=2)
            
            # Assign labels to nearest centroid
            labels = np.argmin(distances, axis=1)

            # Recompute centroids
            new_centroids = np.zeros_like(self.centroids)
            for cluster_idx in range(self.k):
                cluster_points = X[labels == cluster_idx]
                if len(cluster_points) > 0:
                    new_centroids[cluster_idx] = np.mean(cluster_points, axis=0)
                else:
                    new_centroids[cluster_idx] = X[np.random.choice(n_samples)]

            # Check convergence via centroid movement
            shift = np.linalg.norm(new_centroids - self.centroids)
            self.centroids = new_centroids
            if shift < self.tol:
                break

        # Compute final inertia (within-cluster sum of squares)
        final_distances = np.linalg.norm(X[:, np.newaxis, :] - self.centroids[np.newaxis, :, :], axis=2)
        min_dists = np.min(final_distances, axis=1)
        self.inertia_ = float(np.sum(min_dists ** 2))
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        distances = np.linalg.norm(X[:, np.newaxis, :] - self.centroids[np.newaxis, :, :], axis=2)
        return np.argmin(distances, axis=1)
```

#### Complexity Analysis
- **Time Complexity**: **O(T · m · K · d)**, where $T$ is iterations, $m$ is data points, $K$ is clusters, and $d$ is feature dimensions.
- **Space Complexity**: **O(m · K + K · d)** for pairwise distance matrices and centroid storage.

---

### Problem 9: [Python / Data Science] Rolling Z-Score Time-Series Anomaly Detection

#### Problem Statement
Given a pandas DataFrame of high-frequency conveyor motor current telemetry with timestamps `['timestamp', 'motor_current_amps']`, write a function that computes a **rolling Z-score** with a window size of W = 60 samples. Detect anomalies where the absolute Z-score exceeds a threshold (e.g., |Z| ≥ 3.0) and return the indices and timestamps of flagged anomalies, handling edge cases such as initial cold-start and zero standard deviation.

#### Thought Process
1. `Z_t = (x_t - μ_t) / σ_t`, where μ_t and σ_t are the rolling mean and rolling standard deviation over the prior W observations.
2. In production streaming/batch pipelines, using the current value in the mean calculation can bias the mean towards the anomaly. An anomaly-free calculation computes rolling statistics on **shifted** historical values `series.shift(1).rolling(window=W)`.
3. Handle numerical instability: if σ_t ≈ 0 (motor idle or perfectly steady), division by zero occurs. Add a small epsilon ε = 1e-6 to the denominator.
4. Filter out initial W - 1 rows where rolling window statistics are incomplete.

#### Code (Python)
```python
import pandas as pd
import numpy as np

def detect_rolling_zscore_anomalies(
    df: pd.DataFrame, 
    value_col: str = 'motor_current_amps', 
    window_size: int = 60, 
    threshold: float = 3.0,
    epsilon: float = 1e-6
) -> pd.DataFrame:
    # Detects time-series anomalies using an un-biased rolling Z-score
    data = df.copy()
    
    # Use shifted window so the tested point doesn't corrupt the baseline mean/std
    shifted_series = data[value_col].shift(1)
    
    # Compute rolling statistics
    rolling_mean = shifted_series.rolling(window=window_size, min_periods=window_size).mean()
    rolling_std = shifted_series.rolling(window=window_size, min_periods=window_size).std()
    
    # Compute Z-score with numerical stability guard
    data['rolling_mean'] = rolling_mean
    data['rolling_std'] = rolling_std
    data['z_score'] = (data[value_col] - rolling_mean) / (rolling_std + epsilon)
    
    # Flag anomalies
    data['is_anomaly'] = (data['z_score'].abs() >= threshold).fillna(False)
    
    # Extract only flagged records
    anomalies_df = data[data['is_anomaly']].copy()
    return anomalies_df[['timestamp', value_col, 'rolling_mean', 'rolling_std', 'z_score']]
```

#### Complexity Analysis
- **Time Complexity**: **O(N)** using Pandas/NumPy optimized vectorized sliding window algorithms.
- **Space Complexity**: **O(N)** for auxiliary feature columns.

---

### Problem 10: [Python / Data Science] Population Stability Index (PSI) Drift Calculation from Scratch

#### Problem Statement
In production ML at **Honeywell** and **Amazon**, models degrade over time due to feature drift. Implement a function in pure Python/NumPy to calculate the **Population Stability Index (PSI)** between a reference (expected/baseline) array and an inference (actual/current) array for a continuous feature.

#### Thought Process
1. Partition the reference distribution into B quantiles (typically deciles, B = 10).
2. Compute bucket boundaries from the expected distribution: [b_0, b_1, ..., b_10].
3. Bin both the expected and actual arrays into these exact same bucket boundaries.
4. Calculate the empirical proportion of samples falling in bucket k: P_exp(k) and P_act(k).
5. Apply smoothing (epsilon) to avoid division by zero or ln(0) if an actual bucket is empty.
6. Compute PSI:
   > **PSI = Σ [ (P_act(k) - P_exp(k)) × ln(P_act(k) / P_exp(k)) ]**

#### Code (Python)
```python
import numpy as np

def calculate_psi(expected: np.ndarray, actual: np.ndarray, num_buckets: int = 10, epsilon: float = 1e-4) -> float:
    # Computes Population Stability Index (PSI)
    # PSI < 0.1: Stable, 0.1 <= PSI < 0.2: Moderate drift, PSI >= 0.2: Significant drift
    expected = expected[~np.isnan(expected)]
    actual = actual[~np.isnan(actual)]
    
    # Define bucket boundaries using quantiles of the EXPECTED distribution
    percentiles = np.linspace(0, 100, num_buckets + 1)
    bucket_bounds = np.percentile(expected, percentiles)
    
    # Adjust outer bounds to avoid clipping out-of-range actual values
    bucket_bounds[0] = -np.inf
    bucket_bounds[-1] = np.inf
    
    # Calculate counts in each bucket
    expected_counts, _ = np.histogram(expected, bins=bucket_bounds)
    actual_counts, _ = np.histogram(actual, bins=bucket_bounds)
    
    # Calculate empirical probabilities
    expected_probs = expected_counts / len(expected)
    actual_probs = actual_counts / len(actual)
    
    # Add epsilon smoothing to prevent log(0) or division by zero
    expected_probs = np.where(expected_probs == 0, epsilon, expected_probs)
    actual_probs = np.where(actual_probs == 0, epsilon, actual_probs)
    
    # Renormalize probabilities after smoothing
    expected_probs /= np.sum(expected_probs)
    actual_probs /= np.sum(actual_probs)
    
    # Compute PSI sum
    psi_value = np.sum((actual_probs - expected_probs) * np.log(actual_probs / expected_probs))
    return float(psi_value)
```

#### Complexity Analysis
- **Time Complexity**: **O(N log N + M log B)**, where $N$ is size of expected array and $M$ is size of actual array.
- **Space Complexity**: **O(B)** where $B$ is the number of quantile buckets.

---

### Problem 11: [Python / Data Science] Area Under ROC Curve (AUC-ROC) from Scratch

#### Problem Statement
Write a function to compute the **AUC-ROC** given continuous prediction probabilities `y_pred` and true binary labels `y_true in {0, 1}` without importing `scikit-learn`.

#### Thought Process
1. **Mathematical Equivalence**: The Area Under the ROC Curve is mathematically identical to the **Wilcoxon-Mann-Whitney U-statistic**:
   > **AUC = P(ŷ_pos > ŷ_neg) + 0.5 × P(ŷ_pos == ŷ_neg)**
2. In other words, AUC represents the probability that a randomly chosen positive sample receives a higher predicted score than a randomly chosen negative sample!
3. Ranking Approach:
   - Rank all predictions in ascending order (assigning fractional ranks for ties).
   - Sum the ranks of all positive instances: R_pos.
   - Apply the Mann-Whitney $U$ formula:
     > **U = R_pos - [ n_pos · (n_pos + 1) ] / 2,     AUC = U / (n_pos × n_neg)**

#### Code (Python)
```python
import numpy as np

def compute_auc_roc_from_scratch(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    # Computes AUC-ROC using Wilcoxon-Mann-Whitney rank-sum formulation
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    
    pos_mask = (y_true == 1)
    neg_mask = (y_true == 0)
    
    n_pos = np.sum(pos_mask)
    n_neg = np.sum(neg_mask)
    
    if n_pos == 0 or n_neg == 0:
        raise ValueError("Both positive and negative classes must be present.")
        
    # Sort prediction indices ascending
    order = np.argsort(y_pred)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(y_pred) + 1)
    
    # Handle ties by assigning average rank for tied predictions
    sorted_pred = y_pred[order]
    unique_vals, inverse_indices, counts = np.unique(sorted_pred, return_inverse=True, return_counts=True)
    
    if len(unique_vals) < len(y_pred):
        sum_ranks = np.bincount(inverse_indices, weights=ranks[order])
        avg_ranks = sum_ranks / counts
        ranks[order] = avg_ranks[inverse_indices]
        
    # Sum ranks of positive samples
    sum_pos_ranks = np.sum(ranks[pos_mask])
    
    # Calculate U statistic
    u_statistic = sum_pos_ranks - (n_pos * (n_pos + 1)) / 2.0
    auc = u_statistic / (n_pos * n_neg)
    return float(auc)
```

#### Complexity Analysis
- **Time Complexity**: **O(N log N)** dominated by sorting the predictions.
- **Space Complexity**: **O(N)** for storing ranks.

---

### Problem 12: [Python / Data Manipulation] Asynchronous IoT Sensor Telemetry Resampling

#### Problem Statement
IoT vibration sensors ping asynchronously with variable millisecond timestamps and intermittent packet drops. Write a python function using **Pandas** that takes raw sensor logs `['timestamp', 'sensor_id', 'vibration_x', 'vibration_y', 'vibration_z']`, resamples each sensor to a clean **100ms fixed interval**, performs linear interpolation for gaps < 1 second, and flags any gap ≥ 1 second as `'SENSOR_OFFLINE'`.

#### Thought Process
1. Group by `sensor_id`.
2. Convert timestamp to datetime index and apply `.resample('100ms').mean()`.
3. Use `.interpolate(method='linear', limit=10)` (since 10 × 100ms = 1 second).
4. Identify missing values remaining after the limit and mark them as `'SENSOR_OFFLINE'`.

#### Code (Python)
```python
import pandas as pd
import numpy as np

def clean_and_resample_telemetry(df: pd.DataFrame) -> pd.DataFrame:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    resampled_list = []

    for sensor_id, group in df.groupby('sensor_id'):
        # Sort and set timestamp as index
        group = group.sort_values('timestamp').set_index('timestamp')
        
        # Resample to uniform 100ms grid
        resampled = group[['vibration_x', 'vibration_y', 'vibration_z']].resample('100ms').mean()
        
        # Linearly interpolate gaps up to 10 periods (10 * 100ms = 1 second)
        interpolated = resampled.interpolate(method='linear', limit=10)
        
        # Flag persistent outages
        interpolated['sensor_status'] = np.where(interpolated['vibration_x'].isna(), 'SENSOR_OFFLINE', 'HEALTHY')
        interpolated['sensor_id'] = sensor_id
        resampled_list.append(interpolated.reset_index())

    return pd.concat(resampled_list, ignore_index=True)
```

#### Complexity Analysis
- **Time Complexity**: **O(S · M log M)** where $S$ is number of sensors and $M$ is readings per sensor.
- **Space Complexity**: **O(M_resampled)** for the standardized time grid.

---

### Problem 13: [Python / Data Manipulation] Pivot & Flatten Hierarchical Inventory Flow

#### Problem Statement
Amazon fulfillment operations track inventory moves across zones: `['move_id', 'fc_id', 'source_zone', 'target_zone', 'units_moved', 'shift']`. Transform this table into a wide matrix where rows represent `(fc_id, shift)` and columns represent all pairwise flow volumes `units_from_<source>_to_<target>`, filling empty transitions with 0 and adding a total throughput column.

#### Thought Process
1. Construct a composite flow column: `flow_pair = 'units_from_' + df['source_zone'] + '_to_' + df['target_zone']`.
2. Pivot using `df.pivot_table(index=['fc_id', 'shift'], columns='flow_pair', values='units_moved', aggfunc='sum', fill_value=0)`.
3. Compute row-wise total sum and reset the index to flatten the DataFrame.

#### Code (Python)
```python
import pandas as pd

def pivot_fulfillment_flow(df: pd.DataFrame) -> pd.DataFrame:
    # Create descriptive flow column
    df['flow_key'] = 'units_from_' + df['source_zone'].astype(str) + '_to_' + df['target_zone'].astype(str)
    
    # Pivot table
    pivot_df = df.pivot_table(
        index=['fc_id', 'shift'],
        columns='flow_key',
        values='units_moved',
        aggfunc='sum',
        fill_value=0
    )
    
    # Add total row-level volume
    pivot_df['total_fc_units_moved'] = pivot_df.sum(axis=1)
    
    # Flatten MultiIndex and column names
    pivot_df = pivot_df.reset_index()
    pivot_df.columns.name = None
    return pivot_df
```

#### Complexity Analysis
- **Time Complexity**: **O(N)** where N is total number of movement records.
- **Space Complexity**: **O(U)** where U is unique `(fc_id, shift, flow_pair)` cells.

---

### Problem 14: [Python / Algorithms] Sliding Window Maximum Package Flow Rate (LeetCode 239)

#### Problem Statement
Amazon sorters record package counts inducted per second in an array `nums`. An optical sensor evaluates the maximum package surge over a sliding window of size k seconds. Return an array of the maximum surge rate for each sliding window of size $k$ across the shift.

#### Thought Process
1. Naive approach scans all $k$ elements in every window: **O(N · k)** (Too slow for high-frequency logs).
2. Optimal approach uses a **Monotonic Deque (Double-Ended Queue)** storing indices.
3. Invariant: Maintain elements in the deque in **strictly decreasing order** of value. The front of the deque `q[0]` always holds the index of the maximum element in the current window!
4. For each incoming element $nums[i]$:
   - Pop indices from the front if they fall outside the window (q[0] ≤ i - k).
   - Pop indices from the back if their corresponding values are smaller than nums[i] (nums[q[-1]] ≤ nums[i]).
   - Push $i$ to the back.
   - Once i ≥ k - 1, append $nums[q[0]]$ to output.

#### Code (Python)
```python
from collections import deque
from typing import List

class SolutionSlidingWindowMax:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        if not nums or k == 0:
            return []
            
        q = deque()  # Stores indices of candidate maximums
        result = []
        
        for i in range(len(nums)):
            # 1. Remove indices that are out of the current sliding window
            if q and q[0] <= i - k:
                q.popleft()
                
            # 2. Maintain monotonic decreasing order: pop smaller values from back
            while q and nums[q[-1]] <= nums[i]:
                q.pop()
                
            # 3. Add current index to deque
            q.append(i)
            
            # 4. Once the first window of size k is formed, record maximum
            if i >= k - 1:
                result.append(nums[q[0]])
                
        return result
```

#### Complexity Analysis
- **Time Complexity**: **O(N)** linear time. Every index is pushed and popped from the deque at most once.
- **Space Complexity**: **O(k)** auxiliary memory for the deque.

---

### Problem 15: [Python / Algorithms] Top K Most Frequent MHE Error Codes (LeetCode 347)

#### Problem Statement
Given an array of diagnostic error codes generated by robotic arms and sorters `error_codes`, return the **k most frequent error codes**. Must execute with time complexity strictly better than **O(N log N)**.

#### Thought Process
1. Step 1: Count error frequencies using a Hash Map: **O(N)**.
2. Step 2: Use a **Min-Heap** of fixed size k.
   - Iterate through each `(code, freq)` pair in the frequency map.
   - Push to min-heap ordered by frequency. If heap size exceeds k, pop the minimum element.
   - The heap retains the top k largest elements.

#### Code (Python)
```python
import heapq
from collections import Counter
from typing import List

def top_k_frequent_error_codes(error_codes: List[str], k: int) -> List[str]:
    # Step 1: Count frequency of each error code
    counts = Counter(error_codes)
    
    # Step 2: Min-Heap of size k storing (frequency, error_code)
    min_heap = []
    
    for code, freq in counts.items():
        heapq.heappush(min_heap, (freq, code))
        if len(min_heap) > k:
            heapq.heappop(min_heap)
            
    # Step 3: Extract codes in descending order of frequency
    top_k = [heapq.heappop(min_heap)[1] for _ in range(len(min_heap))]
    return top_k[::-1]
```

#### Complexity Analysis
- **Time Complexity**: **O(N + U log k)** where $N$ is array length and $U$ is unique error codes.
- **Space Complexity**: **O(U + k)** for the frequency map and min-heap.

---

### Problem 16: [Python / Algorithms] Merge Overlapping Equipment Maintenance Downtime Windows (LeetCode 56)

#### Problem Statement
Given an array of planned equipment maintenance intervals `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping maintenance windows, and return an array of non-overlapping intervals covering all downtime.

#### Thought Process
1. Sort intervals by their start time: start_i.
2. Initialize an empty merged list.
3. For each interval:
   - If `merged` is empty or the current interval's start is strictly greater than the end time of the previous interval in `merged` (start > merged[-1][1]), no overlap exists: append interval.
   - Otherwise, an overlap exists: update merged[-1][1] = max(merged[-1][1], end).

#### Code (Python)
```python
from typing import List

def merge_maintenance_windows(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
        
    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    
    for current_start, current_end in intervals[1:]:
        prev_start, prev_end = merged[-1]
        
        if current_start <= prev_end:
            # Overlapping window: extend end time
            merged[-1][1] = max(prev_end, current_end)
        else:
            # Non-overlapping window: append new interval
            merged.append([current_start, current_end])
            
    return merged
```

#### Complexity Analysis
- **Time Complexity**: **O(N log N)** driven by sorting the intervals.
- **Space Complexity**: **O(N)** to store the output merged intervals.

---

### Problem 17: [Python / Algorithms] Bottleneck Cycle & Topological Sort in Conveyor Network (LeetCode 207/210)

#### Problem Statement
A fulfillment center conveyor network consists of V transfer junctions numbered 0 to V - 1. Segments flow unidirectionally from junction u to junction v. If a cycle exists, totes loop infinitely, causing physical deadlocks. Given an adjacency list of conveyor transfers, write a function to detect whether a cycle exists and, if not, return a valid topological processing order of junctions using **Kahn's Algorithm (BFS)**.

#### Thought Process
1. **Kahn's Algorithm**:
   - Compute the in-degree of every node (number of incoming conveyor belts).
   - Enqueue all nodes with `in_degree == 0` (inbound induction stations).
   - While queue is not empty:
     - Dequeue node $u$, append to `topological_order`.
     - For each outgoing neighbor $v$ of $u$: decrement `in_degree[v]`.
     - If `in_degree[v] == 0`, enqueue $v$.
2. If `len(topological_order) == V`, no cycle exists; otherwise, a topological deadlock/cycle exists!

#### Code (Python)
```python
from collections import deque, defaultdict
from typing import List, Tuple

def analyze_conveyor_network(num_junctions: int, edges: List[Tuple[int, int]]) -> Tuple[bool, List[int]]:
    # Returns (has_cycle, valid_topological_order)
    adj = defaultdict(list)
    in_degree = [0] * num_junctions
    
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
        
    # Queue all junctions with 0 incoming conveyor segments
    queue = deque([i for i in range(num_junctions) if in_degree[i] == 0])
    topo_order = []
    
    while queue:
        curr = queue.popleft()
        topo_order.append(curr)
        
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    if len(topo_order) == num_junctions:
        return False, topo_order  # No cycle, clean DAG
    else:
        return True, []  # Cycle / deadlock detected
```

#### Complexity Analysis
- **Time Complexity**: **O(V + E)** where $V$ is junctions and $E$ is conveyor segments.
- **Space Complexity**: **O(V + E)** for adjacency list and in-degree tracking.

---

### Problem 18: [Python / Algorithms] Minimum AGVs Needed for Transport Schedule (LeetCode 253)

#### Problem Statement
Automated Guided Vehicles (AGVs) transport pallets across warehouse aisles. Given a list of transport missions with time intervals `intervals = [[start_time, end_time], ...]`, find the **minimum number of AGVs** required so that no mission is delayed.

#### Thought Process
1. This is equivalent to finding the maximum number of concurrent active missions at any point in time.
2. Sort intervals by `start_time`.
3. Use a **Min-Heap** to store the `end_time` of active AGVs.
4. For each new mission `[start, end]`:
   - If the earliest finishing AGV (`heap[0]`) finishes before or at `start`, that AGV is freed up: pop `heap[0]`.
   - Push the new mission's `end` time onto the heap.
5. The size of the heap represents the peak number of AGVs deployed concurrently.

#### Code (Python)
```python
import heapq
from typing import List

def min_agvs_required(intervals: List[List[int]]) -> int:
    if not intervals:
        return 0
        
    # Sort transport missions by start time
    intervals.sort(key=lambda x: x[0])
    
    # Min-Heap stores the completion time of in-use AGVs
    agv_heap = []
    
    for mission_start, mission_end in intervals:
        # If an AGV has completed its prior job, reuse it
        if agv_heap and agv_heap[0] <= mission_start:
            heapq.heappop(agv_heap)
            
        # Allocate AGV for current mission
        heapq.heappush(agv_heap, mission_end)
        
    # Peak AGVs active equals the maximum size reached by the heap
    return len(agv_heap)
```

#### Complexity Analysis
- **Time Complexity**: **O(N log N)** for sorting plus heap push/pop operations.
- **Space Complexity**: **O(N)** for heap storage.

---

### Problem 19: [Python / Algorithms] Binary Search for Optimal Conveyor Velocity

#### Problem Statement
Amazon engineers want to transport N packages of known weights across a fulfillment sorter within H hours. A conveyor motor running at variable speed V (speed capacity V weight units per hour) handles one batch per hour. If a package exceeds current speed, it must wait for the next hour. Find the minimum integer velocity V such that all packages are transported within $H$ hours.

#### Thought Process
1. Binary search on the answer space:
   - Minimum possible speed: max(weights) (the conveyor must be able to move the single heaviest package).
   - Maximum possible speed: sum(weights) (moving all packages in 1 hour).
2. Monotonicity: If speed $V$ can complete the workload in ≤ H hours, any speed V' > V can also do so. If speed $V$ takes > H hours, we need a faster speed.
3. Binary search boundaries: [max(weights), sum(weights)].

#### Code (Python)
```python
import math
from typing import List

def min_conveyor_velocity(weights: List[int], H: int) -> int:
    def can_complete_in_time(speed: int) -> bool:
        total_hours = 0
        for w in weights:
            total_hours += math.ceil(w / speed)
            if total_hours > H:
                return False
        return total_hours <= H

    low = max(weights)
    high = sum(weights)
    optimal_speed = high

    while low <= high:
        mid = (low + high) // 2
        if can_complete_in_time(mid):
            optimal_speed = mid
            high = mid - 1  # Try searching for a lower, more energy-efficient speed
        else:
            low = mid + 1   # Speed too slow, increase lower bound

    return optimal_speed
```

#### Complexity Analysis
- **Time Complexity**: **O(N log(Σ W - max W))**, extremely fast binary search across candidate speeds.
- **Space Complexity**: **O(1)** auxiliary memory.

---

### Problem 20: [Python / Algorithms] Dynamic Programming: 0/1 Outbound Trailer Packing

#### Problem Statement
An outbound Amazon trailer has a maximum payload weight capacity W. You are given N high-priority freight pallets, each with weight w_i and business value/urgency score v_i. Implement a space-optimized **Dynamic Programming** solution to determine the maximum value of freight that can be packed into the trailer without exceeding capacity.

#### Thought Process
1. Classic 0/1 Knapsack formulation:
   - State: $dp[w]$ represents the maximum urgency score achievable with trailer capacity w.
2. Space Optimization:
   - A naive 2D table requires **O(N · W)** space.
   - We can optimize to a **1D array** of size W + 1 by traversing backwards from W down to w_i.
   - Backward traversal ensures each pallet is chosen at most once!
3. Recurrence relation:
   > **dp[w] = max(dp[w], dp[w - w_i] + v_i)**

#### Code (Python)
```python
from typing import List

def optimize_trailer_packing(capacity: int, weights: List[int], values: List[int]) -> int:
    # Space-optimized 1D Dynamic Programming solution
    dp = [0] * (capacity + 1)
    
    for i in range(len(weights)):
        w_i = weights[i]
        v_i = values[i]
        
        # Traverse backwards to ensure each item is only counted once
        for w in range(capacity, w_i - 1, -1):
            dp[w] = max(dp[w], dp[w - w_i] + v_i)
            
    return dp[capacity]
```

#### Complexity Analysis
- **Time Complexity**: **O(N · W)** where $N$ is pallet count and $W$ is trailer capacity.
- **Space Complexity**: **O(W)** space-optimized 1D array.

---

### Problem 21: [Python / Scratch ML] Cosine Similarity & Vector Top-K Retrieval from Scratch

#### Problem Statement
For an AI-powered MHE technical manual retrieval system, write a pure **NumPy** function to compute cosine similarity between a 768-dimensional query embedding vector q and a matrix of document chunk embeddings D in R^(M × 768), and return the indices and scores of the **top K most similar document chunks** using a min-heap or partial sorting.

#### Thought Process
1. **Cosine Similarity**:
   > **Sim(q, d_i) = (q · d_i) / ( ||q||₂ · ||d_i||₂ )**
2. Vectorize the operation across all M documents:
   - Normalize query vector: q_norm = q / ( ||q||₂ + ε ).
   - Row-normalize document matrix: D_norm = D / ( ||D||₂ + ε ).
   - Matrix-vector dot product: S = D_norm · q_norm.
3. Top-$K$ selection: Use `np.argpartition` to find top K in **O(M)** linear time rather than sorting all M items in **O(M log M)**.

#### Code (Python)
```python
import numpy as np
from typing import List, Tuple

def retrieve_top_k_chunks(
    query_vector: np.ndarray, 
    document_matrix: np.ndarray, 
    k: int = 5, 
    eps: float = 1e-9
) -> List[Tuple[int, float]]:
    # Computes vector cosine similarity and returns top-k chunk indices and scores
    # Normalize query vector
    q_norm = np.linalg.norm(query_vector)
    q_unit = query_vector / (q_norm + eps)
    
    # Normalize document matrix rows
    d_norms = np.linalg.norm(document_matrix, axis=1, keepdims=True)
    d_unit = document_matrix / (d_norms + eps)
    
    # Compute cosine similarities via dot product: Shape (M,)
    similarity_scores = np.dot(d_unit, q_unit)
    
    # Fast top-k selection using argpartition
    if k >= len(similarity_scores):
        top_k_indices = np.argsort(similarity_scores)[::-1]
    else:
        # Partition top k elements to the end
        partitioned_indices = np.argpartition(similarity_scores, -k)[-k:]
        # Sort only those top k elements descending
        top_k_indices = partitioned_indices[np.argsort(similarity_scores[partitioned_indices])[::-1]]
        
    return [(int(idx), float(similarity_scores[idx])) for idx in top_k_indices]
```

#### Complexity Analysis
- **Time Complexity**: **O(M · d + M + k log k)** where M is chunk count, d is embedding dimension (768), and k is top chunks retrieved.
- **Space Complexity**: **O(M)** for normalized similarities.
