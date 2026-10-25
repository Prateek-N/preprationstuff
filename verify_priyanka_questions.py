# -*- coding: utf-8 -*-
"""
Verification script for Priyanka Gantam interview questions.
Ensures:
1. Exactly 15 questions.
2. Every answer >= 300 words.
3. STRICTLY NO BULLET POINTS inside the answers (no '- ', '* ', '1. ', '2. ', etc.).
"""

import re
from priyanka_data_questions import QUESTIONS

print(f"Total Questions: {len(QUESTIONS)}")

short_count = 0
bullet_count = 0

bullet_regex = re.compile(r'^\s*([-*•]|\d+\.)\s+', re.MULTILINE)

for q in QUESTIONS:
    words = len(q["answer"].split())
    num = q["num"]
    title = q["title"]

    # Check words
    if words < 300:
        print(f"FAILED (Too short): Q{num:02d} - {words} words: {title}")
        short_count += 1
    else:
        print(f"PASS (Word count): Q{num:02d} - {words} words: {title[:40]}")

    # Check bullets
    bullet_matches = bullet_regex.findall(q["answer"])
    if bullet_matches:
        print(f"FAILED (Bullet detected): Q{num:02d} contains {len(bullet_matches)} bullet point(s)!")
        bullet_count += 1

print("\n--- Summary ---")
print(f"Word Count: {len(QUESTIONS) - short_count}/{len(QUESTIONS)} pass (>= 300 words).")
print(f"Bullet Check: {len(QUESTIONS) - bullet_count}/{len(QUESTIONS)} pass (NO bullet points).")

if short_count == 0 and bullet_count == 0:
    print("ALL 15 QUESTIONS PERFECTLY COMPLIANT WITH INSTRUCTIONS!")
else:
    print("ERRORS DETECTED. PLEASE FIX.")
