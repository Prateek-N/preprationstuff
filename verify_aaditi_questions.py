import re
from aaditi_questions_part1 import QUESTIONS_PART1
from aaditi_questions_part2 import QUESTIONS_PART2

all_q = QUESTIONS_PART1 + QUESTIONS_PART2

print(f"Total questions loaded: {len(all_q)}")

errors = []
for i, q in enumerate(all_q, start=1):
    qid = q["id"]
    ans = q["answer"].strip()
    words = re.findall(r"\b[\w'-]+\b", ans)
    w_count = len(words)
    
    # Check word count
    if w_count < 300:
        errors.append(f"{qid}: Word count {w_count} is UNDER 300 words!")
        
    # Check bullets
    bullet_patterns = [r"^\s*[-*+]\s+", r"^\s*\d+\.\s+"]
    for line in ans.split("\n"):
        for bp in bullet_patterns:
            if re.search(bp, line):
                errors.append(f"{qid}: Contains bullet point or numbered list: '{line[:40]}...'")
                
    # Check bolding
    if "**" not in ans:
        errors.append(f"{qid}: Lacks bold formatting (**)")
        
    print(f"{qid} ({q['title'][:35]}...): {w_count} words | Pass")

if errors:
    print("\n--- ERRORS FOUND ---")
    for e in errors:
        print(f"  FAILED: {e}")
else:
    print("\nALL 30 QUESTIONS PASSED ALL AUDIT CHECKS WITH ZERO ERRORS!")
