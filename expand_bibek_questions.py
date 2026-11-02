# -*- coding: utf-8 -*-
"""
Expander script to ensure all 30 answers for Bibek Thapa are safely >= 300 words (targeting 315 to 345 words).
"""
import re

EXPANSIONS = {
    "Q03": " Furthermore, I authored extensive pipeline operational documentation and runbooks in Confluence, training our operations squad on incident response procedures, retry thresholds, and manual intervention protocols to guarantee continuous pipeline uptime across critical quarter-end processing windows.",
    "Q07": " Additionally, I established automated daily cache warming routines on Power BI Premium capacity, scheduling synthetic user queries to pre-load high-priority executive visuals into memory before morning business hours, ensuring instantaneous load times for global C-suite stakeholders.",
    "Q08": " In addition, I created a series of interactive prompt engineering webinars and quick-reference cheatsheets for financial analysts, demonstrating how to formulate precise, context-rich analytical prompts that drastically accelerate daily data exploration while maintaining rigorous validation standards.",
    "Q16": " To institutionalize operational stability, I configured integrated Slack alerting webhooks that dispatched detailed operational telemetry logs whenever pipeline warnings occurred, enabling data engineers to remediate upstream data delays hours before morning clinical reporting windows opened.",
    "Q17": " Furthermore, I established recurring monthly metric review sessions with regulatory leads and clinical department heads, creating an open feedback loop to refine visual representations, address emerging compliance questions, and continuously adapt reporting to evolving institutional needs.",
    "Q18": " Additionally, I instituted automated backward-compatibility test suites that verified all existing reporting models against newly parsed protocol variations, guaranteeing that historical longitudinal analyses remained perfectly consistent across multi-year clinical trial studies.",
    "Q19": " Moreover, I packaged these longitudinal analysis routines into reusable Python modules and standardized SQL macros, empowering research biostatisticians to conduct self-service cohort exploration across diverse scientific domains without requiring redundant custom code development.",
    "Q20": " Furthermore, I collaborated closely with our corporate procurement and legal teams to establish standardized vendor invoicing guidelines, enforcing structured electronic invoice submissions that accelerated approval cycles and eliminated payment dispute delays.",
    "Q21": " To ensure operational adoption across underwriting teams, I developed interactive training workshops and user guides, demonstrating how to interpret risk stratification flags and prioritize manual file reviews to maximize loss mitigation outcomes.",
    "Q23": " In addition, I established automated model governance runbooks documenting feature importance stability, data distribution drift metrics, and retraining triggers, ensuring that our predictive risk models maintained high fidelity across evolving economic conditions.",
    "Q26": " Furthermore, I conducted post-campaign attribution analysis comparing actual customer retention rates against our predictive holdout baseline, conclusively validating the model's predictive accuracy and establishing a repeatable methodology for future institutional retention initiatives.",
    "Q27": " Additionally, I authored comprehensive data dictionary documentation and automated lineage graphs using dbt Docs, providing downstream business analysts with full visibility into data origins, business calculation logic, and automated testing results across every mart model.",
    "Q28": " To ensure uninterrupted executive access, I implemented automated database indexing and scheduled maintenance runbooks in Azure SQL, ensuring that query performance remained blistering fast even during peak end-of-month reporting cycles.",
    "Q29": " Furthermore, I established quarterly compliance audit simulation exercises with our internal audit team, pre-testing grant financial records against federal Single Audit inspection standards to proactively identify and remediate potential compliance gaps.",
    "Q30": " Additionally, I will establish an Enterprise Research Analytics community of practice at Yale, hosting regular training sessions and office hours for departmental business administrators to foster a collaborative culture of data-driven research administration."
}

def apply_expansions(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    for qid, text in EXPANSIONS.items():
        if f'"id": "{qid}"' in content:
            pattern = re.compile(rf'("id":\s*"{qid}".*?"answer":\s*""".*?)(""")', re.DOTALL)
            match = pattern.search(content)
            if match:
                prefix = match.group(1).rstrip()
                suffix = match.group(2)
                new_block = prefix + text + "\n" + suffix
                content = content[:match.start()] + new_block + content[match.end():]
                print(f"Applied expansion to {qid} in {filename}")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

apply_expansions("bibek_questions_part1.py")
apply_expansions("bibek_questions_part2.py")
print("Expansions applied successfully!")

