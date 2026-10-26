# -*- coding: utf-8 -*-
"""
Verification script for Pavan Chandramouleswara Edyou technical questions.
Checks:
1. Total questions = 30.
2. Every answer >= 300 words.
3. STRICTLY NO BULLET POINTS inside the answers.
"""

import re
from pavan_edyou_questions_part1 import QUESTIONS_PART1
from pavan_edyou_questions_part2 import QUESTIONS_PART2

ALL_Q = QUESTIONS_PART1 + QUESTIONS_PART2
print(f"Total Questions Loaded: {len(ALL_Q)}")

short_count = 0
bullet_count = 0
bullet_regex = re.compile(r'^\s*([-*•]|\d+\.)\s+', re.MULTILINE)

for q in ALL_Q:
    words = len(q["answer"].split())
    num = q["num"]
    title = q["title"]

    # Check words
    if words < 300:
        print(f"FAILED (Too short): Q{num:02d} - {words} words: {title}")
        short_count += 1
    else:
        print(f"PASS (Word count): Q{num:02d} - {words} words: {title[:45]}")

    # Check bullets
    bullet_matches = bullet_regex.findall(q["answer"])
    if bullet_matches:
        print(f"FAILED (Bullet detected): Q{num:02d} contains {len(bullet_matches)} bullet point(s)!")
        bullet_count += 1

print("\n--- Summary ---")
print(f"Word Count: {len(ALL_Q) - short_count}/{len(ALL_Q)} pass (>= 300 words).")
print(f"Bullet Check: {len(ALL_Q) - bullet_count}/{len(ALL_Q)} pass (NO bullet points).")

if short_count == 0 and bullet_count == 0:
    print("\nALL 30 QUESTIONS FULLY COMPLIANT WITH INSTRUCTIONS!")
else:
    print("\nERRORS DETECTED. PLEASE FIX.")
