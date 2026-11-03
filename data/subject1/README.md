# Chinese Driver's License Test in English — Subject 1 (科目一) Practice Questions

**Free, complete English study guide for the China driving theory test (Subject 1 / 科目一).**
If you are a foreigner or expat trying to get or convert a driver's license in China and taking the
theory exam in English, this is the resource that did not exist: **2,545 real practice questions**
with **English translations, correct answers, explanations, and the original exam images** — in a
fixed, studyable order. No signup, no ads, no paywall. Free forever.

> Searching for: *China driving test in English*, *Chinese driver's license theory exam*,
> *科目一 English practice questions*, *how to get a driving license in China as a foreigner*,
> *convert foreign license to Chinese license test*, *China traffic rules exam questions*?
> **You are in the right place.**

---

## ⚠️ Important disclaimer — please read first

**This is an UNOFFICIAL, free, community-made educational resource.**

- **There is NO official, government-published question list.** The Chinese Ministry of Public
  Security (公安部) and the Vehicle Management Offices (车管所) run the exam from a centrally
  maintained pool but **do not publish it**. Anyone claiming to have "the official list" — including
  this project — is sharing an unofficial, community-compiled approximation.
- This repository is **not affiliated with, endorsed by, or verified by** the Ministry of Public
  Security, any 车管所, 驾考宝典, any driving school, or any government or commercial body.
- The content is provided **"AS IS", for educational and informational purposes only**, with
  **no warranty** of accuracy, completeness, or fitness for any purpose, and is **not legal advice**.
- The questions come from a **2022 open-source snapshot** and may be outdated. Rules, point values,
  fines, and speed limits change. **You are responsible for verifying everything against current,
  official sources before your exam and before driving.**
- To the maximum extent permitted by law, the author accepts **no liability** for any loss, exam
  result, penalty, or damage arising from use of this material. **By using it, you accept full
  responsibility for how you use it.**

*(This is a good-faith summary, not a substitute for professional legal advice.)*

---

## Who this is for

- **Foreigners / expatriates in China** taking the driver's license theory test in English.
- People **converting an overseas driver's license** to a Chinese one, who must pass the Subject 1
  theory exam (科目一).
- Anyone who wants a **free, offline, complete** study set instead of ad-heavy apps or websites that
  shuffle questions randomly so you can never be sure you have seen everything.

## What you get

- **2,545** unique Subject 1 questions (deduplicated), covering traffic law, road signs, signals,
  safe driving, and emergency handling.
- **787 original exam images** embedded (traffic signs, signals, and illustrated road scenes).
- Every question in **English + 中文**, with all options, the **correct answer**, a one-line
  **reason**, and the original Chinese legal explanation.
- Three formats: a **250+ page study PDF**, a structured **JSON** dataset, and a flat **CSV**.

### About the exam (Subject 1 / 科目一)

The Subject 1 theory test is the first stage of getting a Chinese driver's license. It is a
computer-based exam: **100 questions** drawn from the national pool, **45 minutes**, pass mark
**90/100**. The exam terminal supports several languages **including English**, so foreigners answer
the same questions, just translated. Studying this bank prepares you for that exam.

---

## Contents

```
.
├── pdf/
│   └── china-subject1-english-study-guide.pdf   # ← Start here to study (250+ pages)
├── data/
│   ├── questions_bilingual.json                 # Structured dataset (apps / flashcards / Anki)
│   └── questions.csv                            # Spreadsheet-friendly export
├── images/
│   └── <question_id>.jpg                         # 787 exam images, named by question id
├── build/
│   ├── assemble.py                              # Regenerates the LaTeX from the data
│   └── study-guide.tex                          # Generated LaTeX source (XeLaTeX)
├── LICENSE                                       # MIT (free to reuse with attribution)
├── SOURCES.md                                    # Full provenance & attribution
└── README.md
```

## Dataset at a glance

| Metric | Count |
|---|---|
| Total questions | **2,545** |
| True / False (判断题) | 1,281 |
| Single choice (单选题) | 1,264 |
| Questions with an image | 787 |

### Questions by chapter

| Chapter | Topic | Questions |
|---|---|---|
| 1 | Traffic Safety Laws, Regulations & Rules / 道路交通安全法律法规 | 1,242 |
| 2 | Traffic Signals / 交通信号 | 547 |
| 3 | Safe & Civil Driving Basics / 安全行车、文明驾驶基础知识 | 184 |
| 4 | Vehicle Operation Basics / 机动车驾驶操作基础知识 | 41 |
| 5 | Incidents, Emergencies & Complex Conditions / 事故处理与应急 | 351 |
| 14 | Additional Questions A / 补充题库 A | 59 |
| 15 | Additional Questions B / 补充题库 B | 121 |

## How to use it

**Just studying?** Download and open
[`pdf/china-subject1-english-study-guide.pdf`](pdf/china-subject1-english-study-guide.pdf). It is
ordered by chapter with a table of contents. Read the English question, try to answer, then check
the green answer line. Focus on the one-line **reason** — the real exam rewords the same rule many
different ways, so learning the rule beats memorizing answers.

**Building an app, flashcards, or an Anki deck?** Use
[`data/questions_bilingual.json`](data/questions_bilingual.json). Schema:

```jsonc
{
  "id": "20191126...",             // stable unique id (also the image filename)
  "chapter_id": "1",
  "chapter": "Traffic Safety Laws, Regulations & Rules / 道路交通安全法律法规",
  "type": "judgement",             // "judgement" (T/F) or "single_choice"
  "question_en": "When the green light is on ...",
  "question_zh": "绿灯亮时 ...",
  "options": [
    { "label": "A", "text_en": "Correct", "text_zh": "正确" },
    { "label": "B", "text_en": "Wrong",   "text_zh": "错误" }
  ],
  "answer": "A",
  "why_en": "Turning vehicles must yield to through traffic.",
  "explanation_zh": "《道路交通安全法》第... 条 ...",
  "image": "images/20191126....jpg", // or null
  "difficulty": 1,
  "error_rate": "4.3"
}
```

## Rebuilding the PDF

Requirements: a TeX distribution with **XeLaTeX** and CJK fonts (`Songti SC`, `STHeiti` on macOS).

```bash
python3 build/assemble.py          # regenerates build/study-guide.tex from data + images
cd build && latexmk -xelatex study-guide.tex
```

## Sources & attribution

Full provenance in [SOURCES.md](SOURCES.md). In short: questions and answers are derived from the
open-source, MIT-licensed dataset
[`doupoa/DrivingTestSubjectOne`](https://github.com/doupoa/DrivingTestSubjectOne) (a July 2022
snapshot of the national 科目一 pool); the images are the original exam figures referenced by that
dataset; the English translations were produced for this project and are not the exam's official
English strings.

## Known limitations

- **2022 snapshot** — the pool is revised periodically; a minority of items may be outdated.
- **Machine-assisted translation** — faithful and consistent, but where an English item is ambiguous
  the Chinese `question_zh` is authoritative.
- **One known upstream data glitch** — a points question in Chapter 5 is internally inconsistent in
  the source data; flagged, not silently altered.

## Contributing

Found an outdated question, a translation that could be clearer, or a new rule? Open an issue or a
pull request. The goal is a genuinely useful, free resource for the expat community in China.

## License

**MIT** (see [LICENSE](LICENSE)) — free to use, share, and adapt with attribution. Consistent with
the upstream dataset's MIT license. Not affiliated with any government authority.

---

*Keywords: China driver's license test English, Chinese driving theory test, 科目一 practice questions
English, foreigner driving license China, expat driving test China, convert foreign license to
Chinese driving license, China traffic rules exam, Chinese road signs test, driving license China
Subject 1, free Chinese driving test questions with answers.*
