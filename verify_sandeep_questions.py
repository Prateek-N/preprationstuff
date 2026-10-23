# verify_sandeep_questions.py
from sandeep_data_questions_part1 import QUESTIONS_PART1
from sandeep_data_questions_part2 import QUESTIONS_PART2

all_q = QUESTIONS_PART1 + QUESTIONS_PART2
print(f"Total Questions: {len(all_q)}")
short_count = 0
for q in all_q:
    words = len(q["answer"].split())
    if words < 300:
        print(f"SHORT: Q{q['num']:02d} has {words} words: {q['title']}")
        short_count += 1
    else:
        print(f"PASS: Q{q['num']:02d} - {words} words - {q['title'][:45]}")

print(f"\nFinal Result: {len(all_q) - short_count}/{len(all_q)} meet >= 300 words criteria.")
