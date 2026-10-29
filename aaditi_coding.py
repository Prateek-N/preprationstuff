# -*- coding: utf-8 -*-
"""
10 Production-Grade Coding Problems & Technical Analytical Solutions for Aaditi Roy.
Specialized for Business Analyst – Payment Model Evaluation at American Express (AMEX).
Covers SQL, Python (Pandas/Scikit-learn/Scipy), Power BI (DAX/M), and Financial Simulation.
Each solution includes:
1. Business Context & Problem Statement
2. Production-Grade Well-Documented Code/Query
3. Time & Space Complexity / Operational Performance Analysis
"""

CODING_PROBLEMS = [
    {
        "num": 1,
        "title": "SQL: Merchant Risk & Transaction Outlier Detection Pipeline",
        "category": "Advanced SQL & Risk Analytics",
        "problem": """American Express processes millions of daily transactions across global merchant networks. Under Global Merchant Acquisition policies, the Payment Model Evaluation team needs an automated SQL pipeline to identify merchants displaying anomalous transaction behavior—such as sudden volume surges, atypical average ticket sizes, or elevated refund ratios.

Write a production-grade SQL query that:
1. Computes rolling 30-day statistical baselines (mean ticket size, standard deviation, and daily volume) for each merchant.
2. Calculates the current day's Z-score for ticket size and volume relative to their 30-day baseline.
3. Flags merchants exceeding 3 standard deviations (Z-score > 3.0) or experiencing a refund ratio > 8% as 'High-Risk Policy Review'.""",
        "code": """-- Production SQL: Multi-Tier Windowed Outlier Detection for Merchant Monitoring
WITH DailyMerchantStats AS (
    SELECT 
        merchant_id,
        merchant_category_code,
        payment_model_type, -- e.g., 'BNPL', 'Direct', 'PayFac_Sub'
        CAST(transaction_timestamp AS DATE) AS transaction_date,
        COUNT(transaction_id) AS daily_tx_count,
        SUM(transaction_amount_usd) AS daily_volume_usd,
        AVG(transaction_amount_usd) AS avg_ticket_usd,
        SUM(CASE WHEN transaction_type = 'REFUND' THEN transaction_amount_usd ELSE 0 END) AS daily_refund_usd
    FROM gms_transactions_fact
    WHERE transaction_timestamp >= CURRENT_DATE - INTERVAL '60 DAY'
      AND status = 'SETTLED'
    GROUP BY 
        merchant_id, 
        merchant_category_code, 
        payment_model_type, 
        CAST(transaction_timestamp AS DATE)
),
RollingBaselines AS (
    SELECT 
        merchant_id,
        merchant_category_code,
        payment_model_type,
        transaction_date,
        daily_tx_count,
        daily_volume_usd,
        avg_ticket_usd,
        daily_refund_usd,
        -- Calculate 30-day rolling baseline excluding current day
        AVG(daily_volume_usd) OVER (
            PARTITION BY merchant_id 
            ORDER BY transaction_date 
            ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
        ) AS baseline_volume_mean,
        STDDEV(daily_volume_usd) OVER (
            PARTITION BY merchant_id 
            ORDER BY transaction_date 
            ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
        ) AS baseline_volume_std,
        AVG(avg_ticket_usd) OVER (
            PARTITION BY merchant_id 
            ORDER BY transaction_date 
            ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
        ) AS baseline_ticket_mean,
        STDDEV(avg_ticket_usd) OVER (
            PARTITION BY merchant_id 
            ORDER BY transaction_date 
            ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
        ) AS baseline_ticket_std
    FROM DailyMerchantStats
),
EvaluatedAnomalies AS (
    SELECT 
        merchant_id,
        merchant_category_code,
        payment_model_type,
        transaction_date,
        daily_volume_usd,
        baseline_volume_mean,
        -- Avoid division by zero with NULLIF
        ROUND((daily_volume_usd - baseline_volume_mean) / NULLIF(baseline_volume_std, 0), 2) AS volume_zscore,
        ROUND((avg_ticket_usd - baseline_ticket_mean) / NULLIF(baseline_ticket_std, 0), 2) AS ticket_zscore,
        ROUND((daily_refund_usd / NULLIF(daily_volume_usd, 0)) * 100, 2) AS refund_ratio_pct
    FROM RollingBaselines
    WHERE transaction_date = CURRENT_DATE - INTERVAL '1 DAY'
)
SELECT 
    merchant_id,
    merchant_category_code,
    payment_model_type,
    transaction_date,
    daily_volume_usd,
    volume_zscore,
    ticket_zscore,
    refund_ratio_pct,
    CASE 
        WHEN volume_zscore >= 3.0 AND refund_ratio_pct >= 8.0 THEN 'CRITICAL: Volumetric & Refund Anomaly'
        WHEN volume_zscore >= 3.0 THEN 'HIGH: Unprecedented Volume Surge'
        WHEN ticket_zscore >= 3.0 THEN 'MEDIUM: Atypical Ticket Size Deviation'
        WHEN refund_ratio_pct >= 8.0 THEN 'HIGH: Elevated Refund Threshold Breach'
        ELSE 'NORMAL: Policy Compliant'
    END AS risk_evaluation_tag
FROM EvaluatedAnomalies
WHERE volume_zscore >= 2.5 OR refund_ratio_pct >= 5.0
ORDER BY volume_zscore DESC, refund_ratio_pct DESC;""",
        "complexity": "Time Complexity: O(N log K) where N is total daily merchant records and K is the 30-day partition window. Space Complexity: O(N) temporary spool memory for analytical window frames. Highly optimized for Snowflake and PostgreSQL execution using clustered B-Tree indexes on (merchant_id, transaction_timestamp)."
    },
    {
        "num": 2,
        "title": "Python: Automated Payment Model Evaluation & Risk Tier Classifier",
        "category": "Python Data Engineering & Machine Learning",
        "problem": """Business Analysts evaluating emerging payment models at AMEX must categorize onboarding merchant applicants into risk tiers (Tier 1 Low Risk, Tier 2 Moderate Risk, Tier 3 Elevated Risk, Tier 4 Prohibited/Reject) based on credit scores, transaction fulfillment horizons, business model type, and regulatory completeness.

Write a modular, object-oriented Python class `PaymentModelEvaluator` using Pandas and Scikit-learn that:
1. Ingests raw merchant application data and cleanses missing values.
2. Applies rule-based policy filters (e.g., immediate rejection of prohibited MCCs or lack of AML/KYC certification).
3. Trains a Random Forest Classifier on historical merchant loss data to predict default probabilities.
4. Outputs an actionable evaluation report with recommended collateral reserve percentages.""",
        "code": """import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from typing import Dict, Tuple

class PaymentModelEvaluator:
    \"\"\"
    Automates merchant payment model evaluation under AMEX Global Policy Standards.
    Combines deterministic regulatory filters with ML-driven credit default scoring.
    \"\"\"
    PROHIBITED_MCCS = {'7995', '5993', '7273'} # Gambling, Adult, Certain Quasi-Cash

    def __init__(self, random_state: int = 42):
        self.model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=random_state)
        self.feature_cols = [
            'fulfillment_days', 'projected_monthly_vol_usd', 'avg_ticket_usd',
            'credit_bureau_score', 'has_aml_kyc_cert', 'is_intermediary_aggregator'
        ]
        self.is_fitted = False

    def preprocess_applications(self, df: pd.DataFrame) -> pd.DataFrame:
        clean_df = df.copy()
        clean_df['fulfillment_days'] = clean_df['fulfillment_days'].fillna(clean_df['fulfillment_days'].median())
        clean_df['credit_bureau_score'] = clean_df['credit_bureau_score'].fillna(600)
        clean_df['has_aml_kyc_cert'] = clean_df['has_aml_kyc_cert'].astype(int)
        clean_df['is_intermediary_aggregator'] = clean_df['payment_model'].apply(
            lambda x: 1 if x in ['PayFac', 'Marketplace', 'BNPL_Aggregator'] else 0
        )
        return clean_df

    def train_risk_model(self, historical_df: pd.DataFrame) -> Dict[str, float]:
        processed = self.preprocess_applications(historical_df)
        X = processed[self.feature_cols]
        y = processed['did_default_or_breach'] # Binary target (1 = default/chargeback loss)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        self.model.fit(X_train, y_train)
        self.is_fitted = True
        
        train_acc = self.model.score(X_train, y_train)
        test_acc = self.model.score(X_test, y_test)
        return {"train_accuracy": round(train_acc, 4), "test_accuracy": round(test_acc, 4)}

    def evaluate_merchant(self, applicant: Dict) -> Dict:
        # Rule 1: Immediate Prohibited Category Filter
        if str(applicant.get('mcc')) in self.PROHIBITED_MCCS:
            return {
                "merchant_id": applicant.get("merchant_id"),
                "policy_status": "REJECTED",
                "risk_tier": "Tier 4 - Prohibited Activity",
                "reserve_requirement_pct": 0.0,
                "reason": "Merchant Category Code violates AMEX Global Policy Standards."
            }
        
        # Rule 2: Mandatory KYC Verification
        if not applicant.get('has_aml_kyc_cert', False):
            return {
                "merchant_id": applicant.get("merchant_id"),
                "policy_status": "BLOCKED_PENDING_DOCS",
                "risk_tier": "Tier 3 - Non-Compliant Documentation",
                "reserve_requirement_pct": 0.0,
                "reason": "Missing mandatory AML/KYC certification."
            }

        if not self.is_fitted:
            raise RuntimeError("ML Risk Model must be trained before scoring applications.")

        # ML Scoring
        input_df = self.preprocess_applications(pd.DataFrame([applicant]))
        default_prob = self.model.predict_proba(input_df[self.feature_cols])[0][1]

        # Policy Tier Assignment & Rolling Reserve Sizing
        if default_prob < 0.10:
            tier = "Tier 1 - Low Risk"
            status = "APPROVED_STANDARD"
            reserve = 0.0
        elif default_prob < 0.25:
            tier = "Tier 2 - Moderate Risk"
            status = "APPROVED_CONDITIONAL"
            reserve = 5.0 # 5% rolling reserve
        else:
            tier = "Tier 3 - High Risk"
            status = "APPROVED_RESTRICTED"
            reserve = 15.0 # 15% rolling reserve with delayed settlement

        return {
            "merchant_id": applicant.get("merchant_id"),
            "policy_status": status,
            "risk_tier": tier,
            "predicted_default_prob": round(float(default_prob), 4),
            "reserve_requirement_pct": reserve,
            "reason": f"Evaluated under model. Default probability estimated at {round(default_prob*100, 2)}%."
        }""",
        "complexity": "Time Complexity: Preprocessing O(M), Training O(T * M * log M) where T is tree count (100) and M is historical record count. Inference is O(T * D) ~ O(1) instantaneous per merchant. Space Complexity: O(M) for feature matrix."
    },
    {
        "num": 3,
        "title": "SQL: Multi-Source Settlement Reconciliation & Three-Way Ledger Matching",
        "category": "Financial Reconciliation & Data Quality",
        "problem": """In payment operations, settlements must balance across three distinct ledgers:
1. Card Network Authorization Stream (`amex_auth_log`)
2. Payment Processor Settlement File (`processor_settlement_feed`)
3. Merchant Deposit Bank Confirmation (`merchant_bank_depository`)

Discrepancies indicate interchange leakage, uncollected discount fees, or processing drop-offs. Write an enterprise-grade SQL reconciliation query that performs a three-way outer match, isolates unbalanced batches, and outputs variance metrics categorized by variance type.""",
        "code": """-- Production SQL: Three-Way Ledger Reconciliation for Merchant Settlement
WITH AuthAggregations AS (
    SELECT 
        merchant_id,
        settlement_batch_id,
        CAST(auth_timestamp AS DATE) AS settlement_date,
        COUNT(transaction_id) AS auth_tx_count,
        SUM(gross_amount_usd) AS auth_gross_usd,
        SUM(interchange_fee_usd) AS expected_interchange_usd
    FROM amex_auth_log
    WHERE auth_timestamp >= CURRENT_DATE - INTERVAL '7 DAY'
    GROUP BY merchant_id, settlement_batch_id, CAST(auth_timestamp AS DATE)
),
ProcessorAggregations AS (
    SELECT 
        merchant_id,
        settlement_batch_id,
        settlement_date,
        COUNT(processor_ref_id) AS proc_tx_count,
        SUM(processed_gross_usd) AS proc_gross_usd,
        SUM(net_settlement_usd) AS proc_net_usd,
        SUM(withheld_discount_fee_usd) AS actual_discount_fee_usd
    FROM processor_settlement_feed
    WHERE settlement_date >= CURRENT_DATE - INTERVAL '7 DAY'
    GROUP BY merchant_id, settlement_batch_id, settlement_date
),
BankDepositoryAggregations AS (
    SELECT 
        merchant_id,
        batch_reference_number AS settlement_batch_id,
        deposit_date,
        SUM(deposited_amount_usd) AS bank_deposited_usd
    FROM merchant_bank_depository
    WHERE deposit_date >= CURRENT_DATE - INTERVAL '7 DAY'
    GROUP BY merchant_id, batch_reference_number, deposit_date
)
SELECT 
    COALESCE(a.merchant_id, p.merchant_id, b.merchant_id) AS merchant_id,
    COALESCE(a.settlement_batch_id, p.settlement_batch_id, b.settlement_batch_id) AS batch_id,
    COALESCE(a.settlement_date, p.settlement_date, b.deposit_date) AS recon_date,
    COALESCE(a.auth_gross_usd, 0) AS auth_gross_usd,
    COALESCE(p.proc_gross_usd, 0) AS proc_gross_usd,
    COALESCE(p.proc_net_usd, 0) AS proc_net_usd,
    COALESCE(b.bank_deposited_usd, 0) AS bank_deposited_usd,
    -- Variances
    ROUND(COALESCE(p.proc_gross_usd, 0) - COALESCE(a.auth_gross_usd, 0), 2) AS auth_to_proc_variance,
    ROUND(COALESCE(b.bank_deposited_usd, 0) - COALESCE(p.proc_net_usd, 0), 2) AS proc_to_bank_variance,
    CASE 
        WHEN a.settlement_batch_id IS NULL THEN 'UNMATCHED: Missing Card Network Authorization'
        WHEN p.settlement_batch_id IS NULL THEN 'CRITICAL: Settlement Dropped by Processor'
        WHEN b.settlement_batch_id IS NULL THEN 'PENDING: Funds Not Confirmed by Depository Bank'
        WHEN ABS(p.proc_gross_usd - a.auth_gross_usd) > 0.05 THEN 'VARIANCE: Gross Authorization Discrepancy'
        WHEN ABS(b.bank_deposited_usd - p.proc_net_usd) > 0.05 THEN 'VARIANCE: Net Deposit Discrepancy'
        ELSE 'BALANCED: Fully Reconciled'
    END AS reconciliation_status
FROM AuthAggregations a
FULL OUTER JOIN ProcessorAggregations p 
    ON a.merchant_id = p.merchant_id 
   AND a.settlement_batch_id = p.settlement_batch_id
FULL OUTER JOIN BankDepositoryAggregations b 
    ON COALESCE(a.merchant_id, p.merchant_id) = b.merchant_id 
   AND COALESCE(a.settlement_batch_id, p.settlement_batch_id) = b.settlement_batch_id
WHERE ABS(COALESCE(p.proc_gross_usd, 0) - COALESCE(a.auth_gross_usd, 0)) > 0.05
   OR ABS(COALESCE(b.bank_deposited_usd, 0) - COALESCE(p.proc_net_usd, 0)) > 0.05
   OR a.settlement_batch_id IS NULL 
   OR p.settlement_batch_id IS NULL 
   OR b.settlement_batch_id IS NULL
ORDER BY recon_date DESC, auth_gross_usd DESC;""",
        "complexity": "Time Complexity: O(A + P + B) with hash aggregation on indexed batch IDs. Space Complexity: O(A + P + B) for hash join tables. Guaranteed deterministic balance verification across multi-million-dollar settlement files."
    },
    {
        "num": 4,
        "title": "Python: Statistical Hypothesis Testing for Emerging Payment Model Default Rates",
        "category": "Hypothesis Testing & Statistical Inference",
        "problem": """AMEX Global Policy is evaluating whether a newly introduced Buy Now Pay Later (BNPL) payment aggregator model exhibits a statistically significant higher 90-day chargeback rate compared to traditional Direct Acquiring merchants across identical Merchant Category Codes.

Write a Python script using SciPy and Pandas that:
1. Performs a Two-Sample Independent T-Test and a Non-Parametric Mann-Whitney U Test on chargeback rate distributions.
2. Conducts a Chi-Square Test of Independence on loan default incidence.
3. Calculates Cohen's d effect size and outputs an executive summary detailing whether the policy committee should reject the null hypothesis at alpha = 0.01.""",
        "code": """import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict

def evaluate_payment_model_disparity(
    direct_chargeback_rates: np.ndarray,
    bnpl_chargeback_rates: np.ndarray,
    alpha: float = 0.01
) -> Dict[str, any]:
    \"\"\"
    Conducts rigorous parametric and non-parametric hypothesis testing
    comparing risk profiles between traditional vs emerging payment models.
    \"\"\"
    # 1. Summary Statistics
    n_direct = len(direct_chargeback_rates)
    n_bnpl = len(bnpl_chargeback_rates)
    mean_direct = np.mean(direct_chargeback_rates)
    mean_bnpl = np.mean(bnpl_chargeback_rates)
    
    # 2. Test for Normality (Shapiro-Wilk)
    _, p_norm_direct = stats.shapiro(direct_chargeback_rates[:100])
    _, p_norm_bnpl = stats.shapiro(bnpl_chargeback_rates[:100])
    is_normal = (p_norm_direct > 0.05) and (p_norm_bnpl > 0.05)

    # 3. Two-Sample T-Test (Welch's T-test, unequal variance assumed)
    t_stat, t_pval = stats.ttest_ind(bnpl_chargeback_rates, direct_chargeback_rates, equal_var=False)

    # 4. Non-Parametric Mann-Whitney U Test (Robust against outliers/skew)
    u_stat, u_pval = stats.mannwhitneyu(bnpl_chargeback_rates, direct_chargeback_rates, alternative='greater')

    # 5. Cohen's d Effect Size
    pooled_std = np.sqrt(
        ((n_bnpl - 1) * np.var(bnpl_chargeback_rates, ddof=1) + 
         (n_direct - 1) * np.var(direct_chargeback_rates, ddof=1)) / (n_bnpl + n_direct - 2)
    )
    cohens_d = (mean_bnpl - mean_direct) / pooled_std

    # Policy Recommendation Logic
    reject_null = (t_pval < alpha) or (u_pval < alpha)
    if reject_null and cohens_d > 0.5:
        recommendation = "REJECT H0: BNPL model exhibits statistically significant higher chargebacks with moderate-to-large effect size. Enforce enhanced reserve policy."
    elif reject_null:
        recommendation = "REJECT H0: Statistically significant difference detected, but small effect size. Implement standard monitoring."
    else:
        recommendation = "FAIL TO REJECT H0: No statistically significant difference in chargeback behavior. Approve standard onboarding."

    return {
        "sample_sizes": {"direct": n_direct, "bnpl": n_bnpl},
        "mean_chargeback_pct": {"direct": round(mean_direct * 100, 3), "bnpl": round(mean_bnpl * 100, 3)},
        "parametric_welch_t": {"t_statistic": round(float(t_stat), 4), "p_value": float(t_pval)},
        "non_parametric_mann_whitney": {"u_statistic": round(float(u_stat), 2), "p_value": float(u_pval)},
        "cohens_d_effect_size": round(float(cohens_d), 4),
        "significance_threshold_alpha": alpha,
        "policy_recommendation": recommendation
    }

# Unit Execution Demonstration
if __name__ == "__main__":
    np.random.seed(42)
    # Direct Acquiring: mean chargeback 0.8%, std 0.3%
    direct_sample = np.clip(np.random.normal(0.008, 0.003, 250), 0.0, 0.05)
    # BNPL Aggregator: mean chargeback 1.4%, std 0.5%
    bnpl_sample = np.clip(np.random.normal(0.014, 0.005, 200), 0.0, 0.08)

    results = evaluate_payment_model_disparity(direct_sample, bnpl_sample)
    for k, v in results.items():
        print(f"{k}: {v}")""",
        "complexity": "Time Complexity: O(N log N) dominated by rank sorting in Mann-Whitney U test, where N = n1 + n2. Space Complexity: O(N) array storage. Executes in < 15ms across hundreds of merchant samples."
    },
    {
        "num": 5,
        "title": "SQL: Churn & Revenue Exposure Cohort Analysis",
        "category": "Customer Analytics & SQL Cohorting",
        "problem": """At Akamai and Dell, cohort retention models protected millions in at-risk revenue. At AMEX, Business Analysts evaluate merchant tenure cohorts to track attrition, volume decay, and credit loss trajectories across merchant onboarding vintages.

Write an advanced SQL cohort analysis query that:
1. Groups merchants into quarterly acquisition cohorts based on their first processing date.
2. Tracks active processing volume and chargeback rates at 3, 6, 9, and 12 months of tenure.
3. Calculates cohort retention percentage and flags vintages with elevated early-tenure attrition.""",
        "code": """-- Production SQL: Merchant Onboarding Cohort Retention & Loss Trajectory
WITH MerchantOnboardingVintage AS (
    SELECT 
        merchant_id,
        payment_model_type,
        DATE_TRUNC('QUARTER', MIN(first_processing_date)) AS onboarding_cohort
    FROM gms_merchant_dimension
    GROUP BY merchant_id, payment_model_type
),
MonthlyMerchantActivity AS (
    SELECT 
        v.onboarding_cohort,
        v.payment_model_type,
        f.merchant_id,
        DATEDIFF('MONTH', v.onboarding_cohort, DATE_TRUNC('MONTH', f.transaction_timestamp)) AS tenure_months,
        SUM(f.transaction_amount_usd) AS monthly_vol_usd,
        SUM(CASE WHEN f.is_chargeback = 1 THEN f.transaction_amount_usd ELSE 0 END) AS monthly_cb_usd
    FROM gms_transactions_fact f
    JOIN MerchantOnboardingVintage v ON f.merchant_id = v.merchant_id
    WHERE f.transaction_timestamp >= '2024-01-01'
    GROUP BY 
        v.onboarding_cohort, 
        v.payment_model_type, 
        f.merchant_id, 
        DATEDIFF('MONTH', v.onboarding_cohort, DATE_TRUNC('MONTH', f.transaction_timestamp))
),
CohortAggregations AS (
    SELECT 
        onboarding_cohort,
        payment_model_type,
        tenure_months,
        COUNT(DISTINCT merchant_id) AS active_merchant_count,
        SUM(monthly_vol_usd) AS cohort_volume_usd,
        ROUND((SUM(monthly_cb_usd) / NULLIF(SUM(monthly_vol_usd), 0)) * 100, 3) AS cohort_cb_rate_pct
    FROM MonthlyMerchantActivity
    WHERE tenure_months IN (0, 3, 6, 9, 12)
    GROUP BY onboarding_cohort, payment_model_type, tenure_months
),
BaselineCohortSize AS (
    SELECT 
        onboarding_cohort,
        payment_model_type,
        active_merchant_count AS initial_cohort_size
    FROM CohortAggregations
    WHERE tenure_months = 0
)
SELECT 
    c.onboarding_cohort,
    c.payment_model_type,
    c.tenure_months,
    b.initial_cohort_size,
    c.active_merchant_count,
    ROUND((c.active_merchant_count::FLOAT / b.initial_cohort_size) * 100, 1) AS merchant_retention_pct,
    c.cohort_volume_usd,
    c.cohort_cb_rate_pct,
    CASE 
        WHEN c.tenure_months = 3 AND (c.active_merchant_count::FLOAT / b.initial_cohort_size) < 0.70 
            THEN 'WARNING: High Early Attrition Vintage'
        WHEN c.cohort_cb_rate_pct > 1.00 
            THEN 'ALERT: Excessive Portfolio Chargeback Rate'
        ELSE 'STABLE: Vintage Performing to Target'
    END AS vintage_health_assessment
FROM CohortAggregations c
JOIN BaselineCohortSize b 
    ON c.onboarding_cohort = b.onboarding_cohort 
   AND c.payment_model_type = b.payment_model_type
ORDER BY c.payment_model_type, c.onboarding_cohort DESC, c.tenure_months ASC;""",
        "complexity": "Time Complexity: O(M * T) where M is transaction count and T is tenure month bucket. Optimized with partition pruning on transaction_timestamp and foreign key clustering. Space Complexity: O(C * M_active) memory footprint."
    },
    {
        "num": 6,
        "title": "Python: Automated PII & Sensitive Entity Data Sanitization Script",
        "category": "Data Governance, Security & Compliance",
        "problem": """Under PCI-DSS and AMEX Data Protection Policies, business analysts extracting merchant underwriting dossiers and telemetry logs must sanitize all Personally Identifiable Information (PII), Taxpayer Identification Numbers (TIN/EIN), bank routing codes, and Primary Account Numbers (PAN) before analytical ingestion or sharing with AI tools (such as ChatGPT).

Write a production Python script that:
1. Detects and masks 15-digit and 16-digit credit card PANs using regex while preserving the last 4 digits for audit matching.
2. Identifies and redacts 9-digit SSN/EIN patterns.
3. Cryptographically hashes merchant bank account numbers using HMAC-SHA256 with a salt to preserve analytical joinability without leaking plaintext.""",
        "code": """import re
import hmac
import hashlib
from typing import Dict, Any, List

class PaymentDataSanitizer:
    \"\"\"
    Enforces PCI-DSS and AMEX Data Confidentiality standards by masking PAN,
    redacting federal tax identifiers, and hashing banking credentials.
    \"\"\"
    # AMEX (15 digits, starts with 34/37) and Visa/MC (16 digits)
    PAN_REGEX = re.compile(r'\\b(3[47]\\d{2})[- ]?(\\d{6})[- ]?(\\d{5})\\b|\\b(\\d{4})[- ]?(\\d{4})[- ]?(\\d{4})[- ]?(\\d{4})\\b')
    SSN_EIN_REGEX = re.compile(r'\\b\\d{3}-\\d{2}-\\d{4}\\b|\\b\\d{2}-\\d{7}\\b')
    EMAIL_REGEX = re.compile(r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b')

    def __init__(self, hmac_salt: str):
        if not hmac_salt or len(hmac_salt) < 16:
            raise ValueError("Cryptographic salt must be at least 16 characters for security.")
        self.salt = hmac_salt.encode('utf-8')

    def mask_pan(self, text: str) -> str:
        def repl(match):
            val = match.group(0).replace('-', '').replace(' ', '')
            last_four = val[-4:]
            return f"XXXX-XXXXXX-X{last_four}" if len(val) == 15 else f"XXXX-XXXX-XXXX-{last_four}"
        return self.PAN_REGEX.sub(repl, text)

    def redact_tax_id(self, text: str) -> str:
        return self.SSN_EIN_REGEX.sub("[REDACTED_TIN]", text)

    def redact_email(self, text: str) -> str:
        return self.EMAIL_REGEX.sub("[REDACTED_EMAIL]", text)

    def hash_bank_account(self, account_number: str) -> str:
        clean_acc = account_number.strip().replace('-', '')
        return hmac.new(self.salt, clean_acc.encode('utf-8'), hashlib.sha256).hexdigest()

    def sanitize_merchant_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        sanitized = record.copy()
        for k, v in sanitized.items():
            if isinstance(v, str):
                v_clean = self.mask_pan(v)
                v_clean = self.redact_tax_id(v_clean)
                v_clean = self.redact_email(v_clean)
                sanitized[k] = v_clean
        
        # Tokenize sensitive banking fields
        if 'bank_account_number' in sanitized:
            sanitized['bank_account_hash'] = self.hash_bank_account(sanitized.pop('bank_account_number'))
        if 'routing_number' in sanitized:
            sanitized['routing_number'] = "XXXX" + str(sanitized['routing_number'])[-4:]
            
        return sanitized

# Verification
if __name__ == "__main__":
    sanitizer = PaymentDataSanitizer(hmac_salt="amex_governance_salt_2026_secure")
    raw_record = {
        "merchant_name": "Apex Digital Labs LLC",
        "tax_identifier": "12-3456789",
        "contact_email": "compliance@apexdigital.com",
        "sample_customer_card": "3782-822456-91006",
        "bank_account_number": "987654321098",
        "routing_number": "122000496",
        "notes": "Merchant onboarding application under BNPL framework with EIN 12-3456789 and test card 378282245691006."
    }
    cleaned = sanitizer.sanitize_merchant_record(raw_record)
    for k, v in cleaned.items():
        print(f"  {k}: {v}")""",
        "complexity": "Time Complexity: O(L) linear in string length for compiled regex search and replace. HMAC-SHA256 is O(B) where B is account byte length (~12 bytes, instantaneous). Space Complexity: O(L) for sanitized copy."
    },
    {
        "num": 7,
        "title": "DAX / Power BI: Dynamic Risk-Weighted Merchant Exposure Calculation",
        "category": "Power BI & DAX Financial Modeling",
        "problem": """In Power BI executive dashboards at AMEX, leadership needs a dynamic DAX calculation that evaluates total Net Credit Exposure across thousands of merchants.

Write production-grade DAX measures that:
1. Calculate Total Gross Settled Volume over a selectable rolling period.
2. Dynamically apply Risk-Weighted Reserve Multipliers based on payment model tier (e.g., BNPL = 1.35x, PayFac = 1.20x, Direct = 1.00x).
3. Compute Net At-Risk Capital after deducting active merchant cash collateral reserves held on deposit.""",
        "code": """-- Production DAX: Dynamic Risk-Weighted Exposure & Reserve Cushion Measures

-- 1. Base Measure: Gross Processing Volume
GrossProcessingVolume = 
SUM ( 'Fact_MerchantSettlement'[settlement_amount_usd] )

-- 2. Base Measure: Active Cash Collateral Held in Reserve Escrow
CashCollateralHeld = 
SUM ( 'Fact_MerchantReserves'[collateral_reserve_usd] )

-- 3. Dynamic Measure: Payment Model Risk Weighting Factor
PaymentModelRiskFactor = 
VAR CurrentModel = SELECTEDVALUE ( 'Dim_Merchant'[payment_model_type], "Direct" )
RETURN
    SWITCH (
        CurrentModel,
        "BNPL_Aggregator", 1.35,
        "Payment_Facilitator", 1.20,
        "Crypto_Gateway", 1.50,
        "Marketplace", 1.15,
        "Direct_Acquiring", 1.00,
        1.10 -- Default fallback
    )

-- 4. Calculated Metric: 90-Day Rolling Chargeback Ratio
Rolling90DayChargebackPct = 
VAR LastDateSelected = MAX ( 'Dim_Date'[Date] )
VAR FirstDateInWindow = LastDateSelected - 90
VAR ChargebackVolume = 
    CALCULATE (
        SUM ( 'Fact_MerchantSettlement'[chargeback_amount_usd] ),
        DATESBETWEEN ( 'Dim_Date'[Date], FirstDateInWindow, LastDateSelected )
    )
VAR TotalVolume = 
    CALCULATE (
        [GrossProcessingVolume],
        DATESBETWEEN ( 'Dim_Date'[Date], FirstDateInWindow, LastDateSelected )
    )
RETURN
    DIVIDE ( ChargebackVolume, TotalVolume, 0 )

-- 5. Core Executive KPI: Net Risk-Weighted Exposure
NetRiskWeightedExposure = 
VAR GrossVol = [GrossProcessingVolume]
VAR RiskMultiplier = [PaymentModelRiskFactor]
VAR CbRate = [Rolling90DayChargebackPct]
VAR Collateral = [CashCollateralHeld]
-- Calculated gross potential loss liability
VAR ProjectedLiability = GrossVol * RiskMultiplier * ( CbRate * 1.5 )
RETURN
    MAX ( 0, ProjectedLiability - Collateral )

-- 6. Formatting KPI Card: Reserve Adequacy Status
ReserveAdequacyStatus = 
VAR NetExposure = [NetRiskWeightedExposure]
VAR Collateral = [CashCollateralHeld]
RETURN
    IF (
        Collateral >= ( NetExposure * 1.2 ),
        "OPTIMAL: Collateral Exceeds 120% of Exposure",
        IF (
            Collateral >= NetExposure,
            "ADEQUATE: Collateral Covers Current Exposure",
            "DEFICIT: Collateral Insufficient - Increase Reserve"
        )
    )""",
        "complexity": "Performance Analysis: Measures utilize storage engine vectorization in the VertiPaq in-memory engine. Uses DATESBETWEEN and CALCULATE filters without row-by-row iteration (avoids costly nested iterators like FILTER inside CALCULATE). Delivers sub-100ms dashboard KPI card rendering."
    },
    {
        "num": 8,
        "title": "Python: AI-Enabled Merchant Policy Compliance & Agreement Analyzer",
        "category": "NLP, Policy Governance & Text Analytics",
        "problem": """Business Analysts evaluating prospective merchant partners must audit their website Terms of Service and merchant agreements against AMEX Global Merchant Acquisition prohibited activity lists (e.g., unauthorized drug sales, counterfeit goods, pyramid marketing, unlicensed financial services).

Write a Python script that:
1. Ingests raw merchant terms text.
2. Scans for prohibited and high-risk activity keywords and contextual patterns using regular expressions.
3. Computes a Policy Risk Index score (0 to 100) and outputs a structured compliance report for Legal and Risk committees.""",
        "code": """import re
from typing import Dict, List, Tuple

class PolicyComplianceAuditor:
    \"\"\"
    Analyzes merchant operating agreements and terms of service against
    AMEX Global Merchant Acquisition Prohibited & Restricted Activities Policy.
    \"\"\"
    PROHIBITED_TAXONOMY = {
        "GAMBLING_UNAUTHORIZED": [
            r'\\bonline\\s+casino\\b', r'\\bsports\\s+wagering\\b', r'\\bi-gaming\\b', 
            r'\\blottery\\s+syndicate\\b', r'\\bbetting\\s+exchange\\b'
        ],
        "UNLICENSED_FINANCIAL": [
            r'\\bbinary\\s+options\\b', r'\\bpayday\\s+loan\\b', r'\\bcredit\\s+repair\\b', 
            r'\\bunregistered\\s+money\\s+transmitter\\b', r'\\bcrypto\\s+tumbler\\b'
        ],
        "DECEPTIVE_MARKETING": [
            r'\\bget\\s+rich\\s+quick\\b', r'\\bmulti-level\\s+marketing\\b', r'\\bpyramid\\s+scheme\\b',
            r'\\bguaranteed\\s+investment\\s+return\\b', r'\\bnegative\\s+option\\s+billing\\b'
        ],
        "CONTROLLED_SUBSTANCES": [
            r'\\bunregulated\\s+supplements\\b', r'\\brx\\s+without\\s+prescription\\b',
            r'\\bsynthetic\\s+cannabinoids\\b', r'\\bcounterfeit\\s+pharmaceuticals\\b'
        ]
    }

    SEVERITY_WEIGHTS = {
        "GAMBLING_UNAUTHORIZED": 30.0,
        "UNLICENSED_FINANCIAL": 35.0,
        "DECEPTIVE_MARKETING": 25.0,
        "CONTROLLED_SUBSTANCES": 40.0
    }

    def __init__(self):
        # Compile patterns for execution speed
        self.compiled_rules = {
            cat: [re.compile(p, re.IGNORECASE) for p in patterns]
            for cat, patterns in self.PROHIBITED_TAXONOMY.items()
        }

    def audit_agreement_text(self, merchant_id: str, agreement_text: str) -> Dict[str, any]:
        violations_found = []
        total_risk_score = 0.0

        for category, patterns in self.compiled_rules.items():
            category_hits = []
            for pattern in patterns:
                matches = pattern.findall(agreement_text)
                if matches:
                    category_hits.extend(list(set(matches)))
            
            if category_hits:
                weight = self.SEVERITY_WEIGHTS.get(category, 20.0)
                total_risk_score += weight
                violations_found.append({
                    "policy_category": category,
                    "matched_keywords": category_hits,
                    "severity_penalty": weight
                })

        # Bounded between 0 and 100
        normalized_risk_score = min(100.0, total_risk_score)

        if normalized_risk_score >= 35.0:
            compliance_verdict = "POLICY_VIOLATION_CRITICAL: Automatic Rejection Recommended"
        elif normalized_risk_score > 0.0:
            compliance_verdict = "ENHANCED_DUE_DILIGENCE: Requires Legal & Compliance Review"
        else:
            compliance_verdict = "COMPLIANT: No Prohibited Activity Detected"

        return {
            "merchant_id": merchant_id,
            "policy_risk_score": round(normalized_risk_score, 1),
            "compliance_verdict": compliance_verdict,
            "violations_detected_count": len(violations_found),
            "violation_details": violations_found
        }

# Verification
if __name__ == "__main__":
    auditor = PolicyComplianceAuditor()
    sample_tos = \"\"\"
    Welcome to QuickFin Services. By signing up, you agree that our platform provides automated
    credit repair assistance and access to high-yield binary options trading signals. Furthermore,
    we connect users to payday loan facilitators across selected partner networks.
    \"\"\"
    report = auditor.audit_agreement_text("M-884920", sample_tos)
    print(f"Merchant ID: {report['merchant_id']}")
    print(f"Policy Risk Score: {report['policy_risk_score']} / 100")
    print(f"Verdict: {report['compliance_verdict']}")
    for v in report['violation_details']:
        print(f"  Category: {v['policy_category']} | Matches: {v['matched_keywords']}")""",
        "complexity": "Time Complexity: O(R * N) where R is total compiled regex patterns (~15) and N is character length of the agreement. Space Complexity: O(K) where K is matched violation tokens."
    },
    {
        "num": 9,
        "title": "SQL: Recursive CTE for Multi-Tier Payment Facilitator & Sub-Merchant Aggregation",
        "category": "Hierarchical SQL & PayFac Topology",
        "problem": """In complex payment architectures, Payment Facilitators (PayFacs) and Independent Sales Organizations (ISOs) operate multi-level merchant hierarchies where Master PayFacs onboard intermediate sub-aggregators who in turn manage end-merchants. Risk governance requires evaluating cumulative exposure across the entire parent-child hierarchy tree.

Write a recursive Common Table Expression (CTE) query in SQL that:
1. Traverses the complete organizational tree from any master acquirer down to terminal sub-merchants.
2. Computes the hierarchical depth level.
3. Aggregates total downstream processing volume and total chargeback losses to evaluate parent-level concentration risk.""",
        "code": """-- Production SQL: Recursive Hierarchy Rollup for Payment Facilitators & Sub-Merchants
WITH RECURSIVE MerchantHierarchyCTE AS (
    -- Anchor Member: Root Master Payment Facilitators
    SELECT 
        merchant_id AS root_master_id,
        merchant_id,
        merchant_name,
        parent_merchant_id,
        payment_model_type,
        1 AS hierarchy_depth_level,
        CAST(merchant_name AS VARCHAR(1000)) AS hierarchy_path
    FROM gms_merchant_dimension
    WHERE parent_merchant_id IS NULL 
      AND payment_model_type IN ('Master_PayFac', 'ISO_Sponsor', 'Marketplace_Parent')

    UNION ALL

    -- Recursive Member: Sub-aggregators and Terminal Merchants
    SELECT 
        h.root_master_id,
        m.merchant_id,
        m.merchant_name,
        m.parent_merchant_id,
        m.payment_model_type,
        h.hierarchy_depth_level + 1 AS hierarchy_depth_level,
        CAST(h.hierarchy_path || ' -> ' || m.merchant_name AS VARCHAR(1000)) AS hierarchy_path
    FROM gms_merchant_dimension m
    JOIN MerchantHierarchyCTE h ON m.parent_merchant_id = h.merchant_id
    WHERE h.hierarchy_depth_level < 5 -- Guardrail against infinite loops
),
HierarchicalVolumeRollup AS (
    SELECT 
        h.root_master_id,
        h.merchant_id,
        h.hierarchy_depth_level,
        h.hierarchy_path,
        COALESCE(SUM(t.transaction_amount_usd), 0) AS total_settled_vol_usd,
        COALESCE(SUM(CASE WHEN t.is_chargeback = 1 THEN t.transaction_amount_usd ELSE 0 END), 0) AS total_cb_loss_usd
    FROM MerchantHierarchyCTE h
    LEFT JOIN gms_transactions_fact t 
        ON h.merchant_id = t.merchant_id 
       AND t.transaction_timestamp >= CURRENT_DATE - INTERVAL '30 DAY'
    GROUP BY 
        h.root_master_id, 
        h.merchant_id, 
        h.hierarchy_depth_level, 
        h.hierarchy_path
)
SELECT 
    root_master_id,
    COUNT(DISTINCT merchant_id) AS total_sub_entities,
    MAX(hierarchy_depth_level) AS max_tree_depth,
    SUM(total_settled_vol_usd) AS consolidated_root_volume_usd,
    SUM(total_cb_loss_usd) AS consolidated_root_loss_usd,
    ROUND((SUM(total_cb_loss_usd) / NULLIF(SUM(total_settled_vol_usd), 0)) * 100, 3) AS consolidated_cb_rate_pct,
    CASE 
        WHEN SUM(total_cb_loss_usd) > 250000 THEN 'CRITICAL: High Cumulative Network Exposure'
        WHEN (SUM(total_cb_loss_usd) / NULLIF(SUM(total_settled_vol_usd), 0)) * 100 > 0.90 THEN 'ELEVATED: Ratio Exceeds PayFac Governance Cap'
        ELSE 'NORMAL: Underwriting Limits Satisfied'
    END AS root_governance_tier
FROM HierarchicalVolumeRollup
GROUP BY root_master_id
ORDER BY consolidated_root_volume_usd DESC;""",
        "complexity": "Time Complexity: O(V + E) for tree traversal where V is merchant nodes and E is parent-child links. Grouped aggregation is O(T) over transaction fact partitions. Space Complexity: O(D) recursion stack where D is maximum tree depth."
    },
    {
        "num": 10,
        "title": "Python: Monte Carlo Simulation for Merchant Reserve & Portfolio Loss Sizing",
        "category": "Quantitative Finance & Risk Simulation",
        "problem": """When evaluating a new, unproven payment model (e.g., decentralized crypto merchant gateway or ultra-fast settlement PayFac), historical chargeback data is sparse. Business Analysts must simulate potential 90-day cumulative portfolio losses under macroeconomic stress scenarios to determine the appropriate collateral reserve escrow percentage.

Write an object-oriented Python class `MerchantReserveSimulator` that:
1. Executes a Monte Carlo simulation (10,000 trials) modeling daily transaction volume, chargeback incidence (Poisson process), and loss severity (Lognormal distribution).
2. Calculates Value at Risk (VaR at 95% and 99% confidence) and Conditional Value at Risk (CVaR / Expected Shortfall).
3. Recommends the exact dollar reserve and reserve percentage required to cover 99% of probable default losses.""",
        "code": """import numpy as np
from typing import Dict

class MerchantReserveSimulator:
    \"\"\"
    Monte Carlo loss simulation engine to determine required collateral
    reserves for emerging payment models under stressed risk scenarios.
    \"\"\"
    def __init__(self, random_seed: int = 42):
        np.random.seed(random_seed)

    def run_portfolio_stress_simulation(
        self,
        projected_daily_volume_usd: float,
        horizon_days: int = 90,
        baseline_cb_probability: float = 0.012, # 1.2% chargeback incidence
        stressed_loss_severity_mean: float = 120.0, # Mean ticket loss
        stressed_loss_severity_std: float = 45.0,
        n_trials: int = 10000
    ) -> Dict[str, float]:
        \"\"\"
        Simulates portfolio loss distributions over a multi-day horizon.
        \"\"\"
        # Convert lognormal parameters
        sigma2 = np.log(1 + (stressed_loss_severity_std / stressed_loss_severity_mean)**2)
        mu = np.log(stressed_loss_severity_mean) - (sigma2 / 2)
        sigma = np.sqrt(sigma2)

        total_simulated_losses = np.zeros(n_trials)
        avg_daily_transactions = int(projected_daily_volume_usd / stressed_loss_severity_mean)

        for _ in range(horizon_days):
            # Poisson process for number of disputed chargeback events per day
            daily_disputes = np.random.poisson(
                lam=avg_daily_transactions * baseline_cb_probability, 
                size=n_trials
            )
            # Lognormal severity for disputed amounts
            daily_loss_amounts = np.random.lognormal(mean=mu, sigma=sigma, size=n_trials)
            total_simulated_losses += (daily_disputes * daily_loss_amounts)

        # Quantitative Metrics: Value at Risk (VaR) and CVaR
        var_95 = np.percentile(total_simulated_losses, 95)
        var_99 = np.percentile(total_simulated_losses, 99)
        cvar_99 = total_simulated_losses[total_simulated_losses >= var_99].mean()
        expected_loss = np.mean(total_simulated_losses)

        total_projected_volume = projected_daily_volume_usd * horizon_days
        recommended_reserve_pct = (var_99 / total_projected_volume) * 100

        return {
            "simulation_trials": n_trials,
            "horizon_days": horizon_days,
            "total_projected_volume_usd": round(total_projected_volume, 2),
            "expected_portfolio_loss_usd": round(float(expected_loss), 2),
            "value_at_risk_95_pct_usd": round(float(var_95), 2),
            "value_at_risk_99_pct_usd": round(float(var_99), 2),
            "conditional_var_99_pct_cvar_usd": round(float(cvar_99), 2),
            "recommended_collateral_reserve_usd": round(float(var_99), 2),
            "recommended_reserve_rate_pct": round(float(recommended_reserve_pct), 3)
        }

# Execution Verification
if __name__ == "__main__":
    simulator = MerchantReserveSimulator()
    # Evaluating a $500K/day emerging payment facilitator over 90 days
    results = simulator.run_portfolio_stress_simulation(
        projected_daily_volume_usd=500000.0,
        horizon_days=90,
        baseline_cb_probability=0.015
    )
    print("=== AMEX PAYMENT MODEL STRESS SIMULATION (10,000 TRIALS) ===")
    for metric, val in results.items():
        print(f"  {metric}: {val}")""",
        "complexity": "Time Complexity: O(T * H) where T is simulation trials (10,000) and H is horizon days (90). Fully vectorized using NumPy C-extensions, executing in ~450ms. Space Complexity: O(T) array holding 10,000 trial outcomes."
    }
]
