# verify_questions.py
from pavan_data_questions_part1 import QUESTIONS_PART1
from pavan_data_questions_part2 import QUESTIONS_PART2

all_q = QUESTIONS_PART1 + QUESTIONS_PART2
print(f"Total questions: {len(all_q)}")
short_count = 0
for q in all_q:
    words = len(q["answer"].split())
    if words < 300:
        print(f"SHORT: Q{q['num']} has {words} words: {q['title']}")
        short_count += 1
    else:
        print(f"PASS: Q{q['num']:02d} - {words} words - {q['title'][:40]}")

print(f"\nSummary: {len(all_q) - short_count}/{len(all_q)} meet >= 300 words criteria.")

from pavan_data_coding_part1 import CODING_PROBLEMS_PART1
from pavan_data_coding_part2 import CODING_PROBLEMS_PART2
all_p = CODING_PROBLEMS_PART1 + CODING_PROBLEMS_PART2
print(f"\nTotal Coding Problems: {len(all_p)}")
for p in all_p:
    has_stmt = bool(p.get("problem_statement"))
    has_tp = bool(p.get("thought_process"))
    has_code = bool(p.get("code"))
    has_tc = bool(p.get("time_complexity"))
    has_sc = bool(p.get("space_complexity"))
    status = "OK" if all([has_stmt, has_tp, has_code, has_tc, has_sc]) else "INCOMPLETE"
    print(f"P{p['num']:02d} [{status}] - {p['title'][:40]} ({p['category']})")

