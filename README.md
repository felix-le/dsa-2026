# DSA & System Design — A Daily Training Log

**Started October 19, 2026 · Updated almost every day since · No days off — only light days**

I am Felix Le, a first-year Software Engineering student at York University (Lassonde School of Engineering, Toronto). My working background is full-stack development in JavaScript/TypeScript. This repository is where I rebuild my fundamentals from zero: data structures and algorithms in **Python** (a language I started from scratch for this), system design, and SQL — trained daily, in public, toward software engineering internships.

Everything here is my own work, written by hand, in the order I learned it. The commit history is the point: slow days, exam weeks, busy days — the log continues.

## The rules I train by

- **Think first.** Every problem gets up to 20 minutes of my own thinking before any discussion. No copied solutions.
- **Full workflow per problem:** analyze the requirements → think → pseudocode → JavaScript sketch (my working language) → final Python solution → I submit it on LeetCode myself.
- **Spaced repetition, no exceptions.** Every solved problem is re-solved from a blank page four more times (+1, +3, +7, +14 days), from memory, without looking at the old solution. Fail a round and it restarts from round 1.
- **Weekly tests.** Two interview-style written tests per week (Wednesday and Sunday), in English, only on material already learned. Anything failed comes back in the next test until it passes.
- **Progress is measured in finished work, not hours studied.**

## LeetCode progress — Easy first, all of them, before any Medium

Working through the Easy problems of *Top 100 Liked* and *Top Interview 150* first, in order, before touching Medium.

| # | Problem | Method | Solved |
|---|---------|--------|--------|
| 1 | Two Sum | Hash map | Oct 19, 2026 |
| 9 | Palindrome Number | Two pointers on digits | Oct 20, 2026 |
| 14 | Longest Common Prefix | Pairwise shrink | Oct 28, 2026 |
| 13 | Roman to Integer | Hash map + pair-checking with lookahead | Oct 31, 2026 |
| 20 | Valid Parentheses | Stack | Nov 1, 2026 |
| 26 | Remove Duplicates from Sorted Array | Two pointers | Nov 7, 2026 |
| 27 | Remove Element | Two pointers | Nov 9, 2026 |
| 28 | Find the Index of the First Occurrence in a String | Brute force | Nov 9, 2026 |
| 392 | Is Subsequence | Two pointers | Nov 9, 2026 |
| 21 | Merge Two Sorted Lists | Linked list + dummy node | Nov 10, 2026 |
| 35 | Search Insert Position | Binary search | Nov 11, 2026 |
| 58 | Length of Last Word | String split | Nov 11, 2026 |

## System design progress — System Design Primer order, one lesson at a time

1. Performance vs. Scalability
2. Availability, Consistency & the CAP Theorem
3. DNS
4. CDN
5. Load Balancer
6. Databases: SQL vs. NoSQL
7. Cache
8. Asynchronism
9. Communication (HTTP, TCP/UDP, RPC, REST)
10. Security
11. Estimation — in progress

## SQL

Top SQL 50, Easy first, learned from zero alongside DSA: `SELECT / FROM / WHERE`, `AND / OR`, and the `NULL` traps (`IS NULL`, three-valued logic) — LeetCode 1757 and 584 done.

## The roadmap

- **Oct – Dec 2026:** finish every Easy problem in both LeetCode lists; Python becomes fluent through the problems themselves
- **Jan – Apr 2027:** Medium, one per day; system design one lesson per week
- **May – Aug 2027:** full system designs (TinyURL first), mock interviews, online assessments
- **Sep 2027 target:** ~250 problems solved, Medium in under 30 minutes, interview-ready

## How this repo is organized

- One file per study day, named by date and topic (`dsa_nov_07_remove_dublicate.py`, `system_nov_11_security.md`, …)
- Each problem keeps the full trail: problem statement, my thinking, pseudocode, JavaScript, then Python
- `lectures/` — lesson notes · `weekly-test/` — my weekly test work

## Study materials

- [System Design Primer](https://github.com/donnemartin/system-design-primer) — backbone of the system design track; lessons follow its order, rewritten in my own words
- [LeetCode Top 100 Liked](https://leetcode.com/studyplan/top-100-liked/)
- [LeetCode Top Interview 150](https://leetcode.com/studyplan/top-interview-150/)
- [LeetCode Top SQL 50](https://leetcode.com/studyplan/top-sql-50/)

---

*Consistency beats intensity. This log is the proof of work.*
