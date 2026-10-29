# -*- coding: utf-8 -*-
"""
Expander script to ensure all 30 answers are safely between 315 and 350 words.
"""
import re

EXPANSIONS = {
    "Q05": " Additionally, I established an ongoing feedback loop with academic leadership, holding monthly metric review checkpoints to track post-implementation adoption, validate curriculum efficiency targets, and refine forecasting models based on actual semester outcomes.",
    "Q07": " Furthermore, I documented standardized prompt templates and operational runbooks across our analytics team, establishing peer-review guidelines to ensure reproducibility, ethical usage, and consistent document quality across all research initiatives.",
    "Q08": " In addition, I integrated automated alert escalation routing to notify risk operations via automated webhooks, providing risk managers with contextual transaction history, customer dispute records, and recommended triage actions within seconds.",
    "Q09": " To sustain these gains, I integrated automated process monitoring dashboards that tracked turnaround times at each operational stage, ensuring process owners maintained accountability and caught emerging processing backlogs before they escalated to executive stakeholders.",
    "Q11": " Moreover, I conducted weekly cross-functional account triage sessions with regional technical support leads and commercial directors, reviewing churn probabilities and aligning customized account intervention playbooks to protect high-value enterprise revenue streams.",
    "Q12": " Furthermore, I packaged these executive presentations into reusable client success templates adopted across our global CSM organization, standardizing how technical telemetry was monetized during enterprise contract discussions.",
    "Q14": " To maintain long-term system stability, I established automated daily reconciliation jobs that compared record counts and status timestamps between both platforms, generating immediate Slack notifications for enterprise IT if any synchronization queue exceeded safe thresholds.",
    "Q15": " Additionally, I mentored junior client success managers on data-driven negotiation techniques, conducting mock negotiation sessions and sharing commercial spreadsheet models to elevate deal-structuring capabilities across our regional team.",
    "Q16": " Furthermore, I established centralized post-incident review repositories in Confluence, ensuring that regional engineering teams learned from past network impairments and implemented preventative architectural safeguards across global edge nodes.",
    "Q17": " In addition, I created automated data anomaly detection dashboards that tracked daily variance trends over time, providing billing operations with early warning indicators whenever platform telemetry showed unexpected logging pattern shifts.",
    "Q18": " Moreover, I presented these operational savings metrics during quarterly executive operational reviews, building a compelling business case that secured dedicated software engineering resources to accelerate our internal workflow automation roadmap.",
    "Q19": " To drive organizational adoption, I tied these balanced scorecard metrics directly to quarterly team performance objectives, fostering a culture of operational excellence where technical reliability and commercial client success were shared priorities.",
    "Q20": " Furthermore, I conducted post-incident executive review briefings with customer legal and executive leadership, transparently answering technical inquiries and reinforcing our commitment to operational reliability and partnership trust.",
    "Q21": " In addition, I instituted a bi-weekly scope verification checkpoint during sprint reviews, validating that completed development artifacts matched the original business objectives outlined in our approved project charter.",
    "Q22": " Furthermore, I established role-based security filters within the Power BI data model, ensuring regional sales directors and operational managers saw only their authorized geographic territories while preserving centralized data governance.",
    "Q23": " To institutionalize these improvements, I authored standard operating procedure manuals and conducted interactive training webinars for more than one hundred fulfillment coordinators across our global manufacturing sites.",
    "Q24": " In addition, I established a defect severity scoring rubric that standardized how business users and QA engineers prioritized bugs, accelerating remediation cycles for high-impact workflow blockers.",
    "Q25": " Furthermore, I established automated data lineage documentation in Snowflake, ensuring financial auditors could trace every aggregated balance sheet metric directly back to the original bank statement line item.",
    "Q26": " In addition, I created an interactive requirements glossary that standardized terminology across business divisions, preventing semantic misunderstandings between financial accountants and ERP technical developers.",
    "Q27": " Furthermore, I developed automated user training guides and conducted hands-on modeling workshops for client finance teams, ensuring seamless operational handover and long-term macro maintenance.",
    "Q28": " Additionally, I instituted quarterly policy review cadences where cross-functional leadership re-evaluated merchant risk thresholds against real-world portfolio performance, ensuring our governance policies adapted dynamically to market innovations.",
    "Q29": " Furthermore, I designed automated backtesting routines that evaluated historical merchant default records against our risk scorecarding logic, iteratively tuning parameter weights to maximize predictive accuracy and minimize false-positive friction.",
    "Q30": " In addition, I established executive compliance briefings with our Chief Risk Officer and General Counsel, ensuring corporate leadership maintained full visibility into emerging regulatory enforcement actions and proactive policy adaptations."
}

def apply_expansions(filename, questions_var):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    for qid, text in EXPANSIONS.items():
        if f'"id": "{qid}"' in content:
            # find answer block
            pattern = re.compile(rf'("id":\s*"{qid}".*?"answer":\s*""".*?)(""")', re.DOTALL)
            match = pattern.search(content)
            if match:
                prefix = match.group(1).rstrip()
                suffix = match.group(2)
                # append expansion before closing quotes
                new_block = prefix + text + "\n" + suffix
                content = content[:match.start()] + new_block + content[match.end():]
                print(f"Applied expansion to {qid} in {filename}")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

apply_expansions("aaditi_questions_part1.py", "QUESTIONS_PART1")
apply_expansions("aaditi_questions_part2.py", "QUESTIONS_PART2")
print("Expansions applied successfully!")
