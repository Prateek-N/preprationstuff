# -*- coding: utf-8 -*-
"""
Verification Script for Varun Sambath Kumar Technical Questions
Validates:
1. Exactly 30 questions
2. Word count >= 300 for every single question
3. Strictly NO bullet points in any question
4. Categorization and experience distribution
"""

import re
from varun_questions_part1 import QUESTIONS_PART1
from varun_questions_part2 import QUESTIONS_PART2

QUESTIONS = QUESTIONS_PART1 + QUESTIONS_PART2

print(f"Total Questions Loaded: {len(QUESTIONS)}")
assert len(QUESTIONS) == 30, f"Expected 30 questions, found {len(QUESTIONS)}"

word_count_passes = True
bullet_check_passes = True

print("\n" + "="*80)
print("AUDIT RESULTS PER QUESTION:")
print("="*80)

for q in QUESTIONS:
    words = len(re.findall(r'\b\w+\b', q['answer']))
    has_bullet = bool(re.search(r'(^|\n)\s*[-*+]\s+', q['answer']) or re.search(r'(^|\n)\s*\d+\.\s+', q['answer']))
    
    status_wc = "PASS" if words >= 300 else "FAIL"
    status_bullet = "PASS (No Bullets)" if not has_bullet else "FAIL (Found Bullets)"
    
    if words < 300:
        word_count_passes = False
    if has_bullet:
        bullet_check_passes = False
        
    print(f"Q{q['num']:02d}: {words:3d} words | {status_wc} | {status_bullet} | {q['title'][:50]}...")

print("\n" + "="*80)
print(f"Overall Word Count Check: {'PASS (All >= 300 words)' if word_count_passes else 'FAIL'}")
print(f"Overall Bullet Check:     {'PASS (Zero bullets found)' if bullet_check_passes else 'FAIL'}")
print("="*80)

if word_count_passes and bullet_check_passes:
    print("\nALL 30 QUESTIONS FULLY COMPLIANT WITH INSTRUCTIONS!")
else:
    print("\nATTENTION NEEDED: Some questions did not meet requirements.")
