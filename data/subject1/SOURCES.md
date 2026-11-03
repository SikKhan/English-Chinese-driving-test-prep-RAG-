# Sources & Attribution

This document records the full provenance of everything in this repository, in the interest of
transparency and proper credit.

## 1. Questions, answers, and Chinese explanations

The question text, option lists, correct answers, and the original Chinese legal/explanatory notes
are derived from the open-source dataset:

- **Repository:** [`doupoa/DrivingTestSubjectOne`](https://github.com/doupoa/DrivingTestSubjectOne)
- **License:** MIT
- **Description (original):** "2022年7月最新科目一题库带解析，带查询" — the July 2022 snapshot of the
  national Subject 1 (科目一) question pool, with explanations.
- **File used:** `q.json` (the full bank; this repo uses only the `subject == 1` records).

From that source we:
1. Filtered to Subject 1 questions only.
2. Deduplicated by question `id` (result: 2,545 unique questions).
3. Ordered them by chapter, then id, for a stable, studyable sequence.

## 2. Images

The dataset references each image question by a URL on its image CDN
(`app.static.public.chetailian.com`). The 787 Subject 1 images were retrieved from those URLs and
are stored here under `images/`, named by their question `id`. They are the original exam figures
(traffic signs, signal scenes, and illustrated road situations).

## 3. English translations

The English question text, English option text, and the one-line English reason (`why_en`) were
produced specifically for this repository using machine-assisted translation with consistency review.
They are **this project's own work** and are **not** the official English strings displayed on the
exam terminal. Where an English rendering is ambiguous, the original Chinese (`question_zh`) is the
authoritative text.

## 4. Background references (not redistributed here)

General facts about the exam format (100 questions, 45 minutes, 90/100 pass mark, multi-language
terminal support) were cross-checked against publicly available guides, including:

- Wikipedia: "Chinese driving test"
- chinesedrivingtest.com (an existing English practice site)

No content from those references is copied into this repository.

## 5. Official status

There is **no officially published government question bank**. The Ministry of Public Security
maintains the exam centrally but does not release the list. Consequently:

- No one, including this project, can authoritatively separate "currently active" questions from
  retired ones.
- This set should be treated as a **broad superset for study**, not as the exact live exam.

## 6. Disclaimer

This repository is an independent, unofficial, educational resource. It is not affiliated with,
endorsed by, or verified by the Ministry of Public Security (公安部), any Vehicle Management Office
(车管所), 驾考宝典, or any other authority or commercial entity. Use it to learn the rules; confirm
specifics against a current official-partnered source before your exam.
