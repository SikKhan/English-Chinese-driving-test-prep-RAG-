"""Prepare the local English driving-test corpus without embeddings or LLM calls.

Run: .venv/Scripts/python scripts/prepare_rag.py
The source allowlist deliberately excludes backups, reviews, and Chinese-only copies.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import tiktoken

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data/prepared"
ENC = tiktoken.get_encoding("cl100k_base")
VERSION = "1.0.0"
MAX_TOKENS = 512  # Applies to the entire embedding text, including its context.
LAW = {
    "accident-procedure-2017": ("Provisions on Procedures for Handling Road Traffic Accidents", r"(?m)^\(Promulgated by Order No\. 146", r"(?m)^National Regulations Database"),
    "compulsory-insurance-regulation-2019": ("Regulations on Compulsory Traffic Accident Liability Insurance for Motor Vehicles", r"\A", None),
    "driving-licence-rules-2025": ("Provisions on the Application and Use of Motor Vehicle Driving Licenses", r'(?m)^The "Decision of the Ministry', r"(?m)^Scan to open the current page"),
    "implementation-regulation-2017": ("Regulations on the Implementation of the Road Traffic Safety Law", r"(?m)^Adopted at the 49th", r"(?m)^Scan to open the current page"),
    "points-regulation-2022": ("Measures for the Administration of Points for Road Traffic Safety Violations", r"(?m)^Order No\. 163", r"(?m)^Scan to open the current page"),
    "road-traffic-safety-law-2021": ("Law of the People's Republic of China on Road Traffic Safety", r"(?m)^\(Adopted at the Fifth", r"(?m)^Share:"),
    "vehicle-registration-2022": ("Provisions on Motor Vehicle Registration", r'(?m)^Order No\. 164', r"(?m)^Scan to open the current page"),
    "violation-procedure-2020": ("Provisions on the Procedures for Handling Road Traffic Safety Violations", r"(?m)^Order of the Ministry", r"(?m)^Organizing Unit:"),
}


def read(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8-sig"))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def tokens(text):
    return len(ENC.encode(text, disallowed_special=()))


def write(name, rows):
    (OUT / name).write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in rows), encoding="utf-8")


def trim_span(text, start, end):
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return start, end


def split_spans(text, prefix):
    """Lossless, nonoverlapping spans; prefer paragraphs, clauses, then sentences.

    Parent expansion supplies neighboring context, so no arbitrary cross-article overlap.
    """
    start = 0
    while start < len(text):
        if tokens(prefix + text[start:]) <= MAX_TOKENS:
            yield start, len(text)
            return
        lo, hi = start + 1, len(text)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if tokens(prefix + text[start:mid]) <= MAX_TOKENS:
                lo = mid
            else:
                hi = mid - 1
        limit = lo
        lower = start + (limit - start) // 2
        candidates = []
        for pattern in [r"\n\s*\n", r"\n(?=\s*\(?\d+[).、])", r"(?<=[.!?;])\s+", r"\s+"]:
            candidates = [start + m.end() for m in re.finditer(pattern, text[start:limit]) if start + m.end() >= lower]
            if candidates:
                break
        end = candidates[-1] if candidates else limit
        if end <= start or tokens(prefix + text[start:end]) > MAX_TOKENS:
            raise ValueError("Unable to produce a bounded text span")
        yield start, end
        start = end


def main():
    OUT.mkdir(exist_ok=True)
    parents, chunks, quarantine, exclusions, inventory = [], [], [], [], []
    question_groups = defaultdict(list)
    law_counts = {}

    def source(path):
        item = {"path": path, "sha256": sha((ROOT / path).read_bytes())}
        if item not in inventory:
            inventory.append(item)
        return item

    def emit(parent, prefix, atomic=False):
        parent["text_sha256"] = sha(parent["text"].encode("utf-8"))
        parents.append(parent)
        spans = [(0, len(parent["text"]))] if atomic else list(split_spans(parent["text"], prefix))
        assert "".join(parent["text"][a:b] for a, b in spans) == parent["text"]
        for index, (a, b) in enumerate(spans):
            embedding_text = prefix + parent["text"][a:b]
            chunk_id = "chunk-" + sha((parent["parent_id"] + "\0" + str(index) + "\0" + embedding_text).encode())[:24]
            chunks.append({"chunk_id": chunk_id, "parent_id": parent["parent_id"], "chunk_index": index,
                           "chunk_count": len(spans), "text": parent["text"][a:b], "embedding_text": embedding_text,
                           "token_count": tokens(embedding_text), "parent_char_start": a, "parent_char_end": b,
                           "metadata": parent["metadata"]})

    for subject, path in [(1, "data/subject1/data/questions_bilingual.json"), (4, "data/subject4/subject4_translations.json")]:
        src = source(path)
        seen = set()
        for index, row in enumerate(read(path)):
            reasons = []
            rid = str(row.get("id", ""))
            if not rid or rid in seen:
                reasons.append("missing_or_duplicate_id")
            seen.add(rid)
            question = row.get("question_en", "").strip()
            if not question:
                reasons.append("missing_english_question")
            if subject == 1:
                options = [{"label": o["label"], "text": o.get("text_en", "").strip()} for o in row["options"]]
            else:
                raw_options = row.get("options_en", "").strip()
                matches = list(re.finditer(r"(?:^|\s)([A-D])[.、:：)．]\s*", raw_options))
                options = [{"label": m.group(1), "text": raw_options[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(raw_options)].strip()}
                           for i, m in enumerate(matches)]
                if not matches or raw_options[:matches[0].start()].strip():
                    reasons.append("unparsed_option_lines")
            labels = [o["label"] for o in options]
            if len(options) < 2 or len(set(labels)) != len(labels) or any(not o["text"] for o in options):
                reasons.append("invalid_options")
            answer = str(row.get("answer", ""))
            if not re.fullmatch(r"[ABCD]+", answer) or len(set(answer)) != len(answer) or any(x not in labels for x in answer):
                reasons.append("invalid_answer_key")
            image = row.get("image")
            image_path = "data/subject1/" + image if image else None
            if image_path and (not (ROOT / image_path).is_file() or not (ROOT / image_path).resolve().is_relative_to(ROOT)):
                reasons.append("missing_or_unsafe_image")
            missing_image = not image_path and bool(
                re.search(r"\b(?:as shown|this sign|this hand signal|in (?:the|this) (?:picture|image|diagram|figure))\b", question, re.I)
                or re.search(r"如图|图中|这个标志|这种手势", row.get("question_zh", "")))
            if missing_image:
                reasons.append("missing_referenced_image")
            if reasons:
                quarantine.append({"source_file": path, "source_record_index": index, "record_id": rid, "reasons": reasons, "record": row})
                continue
            chapter = row.get("chapter", "").split(" / ")[0]
            metadata = {"corpus": "driving-test", "kind": "exam_question", "subject": subject, "language": "en",
                        "record_id": rid, "source_file": path, "source_sha256": src["sha256"], "source_record_index": index,
                        "chapter": chapter, "question_type": row.get("type", "multiple_choice" if len(answer) > 1 else "single_choice"),
                        "answer_labels": list(answer), "image_path": image_path, "requires_image": bool(image_path),
                        "possible_missing_image": not image_path and bool(re.search(r"\b(image|picture|shown|diagram|figure)\b", question, re.I)),
                        "translation_review_required": row.get("translation_review_required", True),
                        "source_review_required": row.get("source_review_required", True),
                        "translation_model": row.get("translation_model", "upstream_machine_assisted"),
                        "official_exam_bank": False, "current_validity_verified": False,
                        "citation": f"Subject {subject}, question {rid}", "source": row.get("source", "china-drivers-license-subject1-en")}
            lines = ["Question: " + question] + [o["label"] + ". " + o["text"] for o in options]
            lines.append("Correct answer: " + "; ".join(o["label"] + ". " + o["text"] for o in options if o["label"] in answer))
            if row.get("why_en", "").strip():
                lines.append("Explanation: " + row["why_en"].strip())
            text = "\n".join(lines)
            prefix = f"Chinese driving test | Subject {subject}" + (" | " + chapter if chapter else "") + "\n\n"
            if tokens(prefix + text) > 2048:
                quarantine.append({"source_file": path, "record_id": rid, "reasons": ["oversized_atomic_question"], "record": row})
                continue
            emit({"parent_id": f"subject{subject}:{rid}", "text": text, "metadata": metadata}, prefix, atomic=True)
            key = re.sub(r"\s+", " ", question.casefold())
            question_groups[key].append({"parent_id": parents[-1]["parent_id"], "answer": answer,
                                         "options": options, "image_path": image_path})

    sources = {s["name"]: s for s in read("data/traffic-laws/sources.json")}
    source("data/traffic-laws/sources.json")
    for name, (title, start_pattern, footer_pattern) in LAW.items():
        path = f"data/traffic-laws/translations/{name}.json"
        src = source(path)
        rows = read(path)
        original = ROOT / f"data/traffic-laws/{name}.txt"
        source(original.relative_to(ROOT).as_posix())
        original_sha = sha(original.read_bytes())
        # Exact source coverage check; stale/incomplete translations must stop preparation.
        assert "".join(r["text_zh"] for r in rows) == original.read_text(encoding="utf-8"), name
        assert all(r["source_sha256"] == original_sha for r in rows), name
        assert [r["chunk"] for r in rows] == list(range(1, len(rows) + 1)), name
        assert all(r["text_en"].strip() for r in rows), name
        text, segments = "", []
        for row in rows:
            if text:
                text += "\n"  # Never guess how independently translated fragments should be rewritten.
            a = len(text)
            text += row["text_en"]
            segments.append((a, len(text), row["chunk"]))
        first = re.search(r"(?m)^Article\s+1\b", text)
        assert first, name
        footer = re.search(footer_pattern, text) if footer_pattern else None
        assert not footer_pattern or footer, name
        end = footer.start() if footer else len(text)
        start_match = re.search(start_pattern, text)
        assert start_match and start_match.start() < first.start(), name
        intro_start = start_match.start()
        toc = re.search(r"(?im)^Table of Contents", text[intro_start:first.start()])
        intro_end = intro_start + toc.start() if toc else first.start()
        # Omit only an introductory Chapter 1 heading if there is no contents list.
        heading = re.search(r"(?m)^Chapter\s+1\b", text[intro_start:intro_end])
        if heading:
            intro_end = intro_start + heading.start()
        for a, b, reason in [(0, intro_start, "website_header"), (intro_end, first.start(), "contents_and_repeated_headings"), (end, len(text), "website_footer")]:
            if b > a:
                exclusions.append({"source_file": path, "reason": reason, "assembled_char_start": a, "assembled_char_end": b, "text": text[a:b]})

        def law_parent(a, b, unit, context, number=None):
            a, b = trim_span(text, a, b)
            if a == b:
                return
            overlaps = [{"translation_chunk": i, "text_en_char_start": max(a, x) - x, "text_en_char_end": min(b, y) - x}
                        for x, y, i in segments if x < b and y > a]
            meta = {"corpus": "driving-test", "kind": "traffic_law", "language": "en", "document_id": name,
                    "title": title, "article_number": number, "unit": unit, "section_path": context,
                    "source_file": path, "source_sha256": src["sha256"], "original_text_sha256": original_sha,
                    "source_url": sources[name]["url"], "retrieved": sources[name]["retrieved"],
                    "translation_source_spans": overlaps, "translation_review_required": True,
                    "source_review_required": True, "current_validity_verified": False,
                    "translation_model": sorted({r["translation_model"] for r in rows}),
                    "crosses_translation_boundary": len(overlaps) > 1,
                    "citation": f"{title}, {unit}"}
            prefix = title + "\n" + " > ".join(context + [unit]) + "\n\n"
            emit({"parent_id": name + ":" + unit.lower().replace(" ", "-"), "text": text[a:b], "metadata": meta}, prefix)

        law_parent(intro_start, intro_end, "Promulgation and amendments", [])
        events = list(re.finditer(r"(?m)^(Article\s+(\d+)\b[^\n]*|Chapter\s+\d+[^\n]*|Section\s+\d+[^\n]*|Attachment[^\n]*)", text[first.start():end]))
        chapter = "Chapter 1 General Provisions"
        section = None
        numbers = []
        for i, match in enumerate(events):
            a = first.start() + match.start()
            b = first.start() + events[i + 1].start() if i + 1 < len(events) else end
            label = match.group(1)
            if label.startswith("Chapter"):
                chapter, section = label, None
                continue
            if label.startswith("Section"):
                section = label
                continue
            if label.startswith("Attachment"):
                law_parent(a, b, label.strip(), [chapter])
                continue
            number = int(match.group(2))
            numbers.append(number)
            law_parent(a, b, f"Article {number}", [x for x in [chapter, section] if x], number)
        assert numbers == list(range(1, max(numbers) + 1)), (name, numbers)
        law_counts[name] = {"articles": len(numbers), "translation_segments": len(rows),
                            "translation_boundary_articles": sum(p["metadata"].get("crosses_translation_boundary", False) for p in parents if p["metadata"].get("document_id") == name)}

    duplicates = [{"question": q, "records": rows, "conflicting_answers_for_identical_options_and_image":
                   len({json.dumps([r["options"], r["image_path"]], sort_keys=True) for r in rows}) == 1 and len({r["answer"] for r in rows}) > 1}
                  for q, rows in sorted(question_groups.items()) if len(rows) > 1]
    parent_ids = [p["parent_id"] for p in parents]
    assert len(parent_ids) == len(set(parent_ids)), "Duplicate parent IDs"
    assert len({c["chunk_id"] for c in chunks}) == len(chunks)
    for c in chunks:
        assert c["text"].strip() and c["embedding_text"].strip()
        if c["metadata"]["kind"] == "traffic_law":
            assert c["token_count"] <= MAX_TOKENS
    report = {"schema_version": VERSION, "tokenizer": "cl100k_base", "tokenizer_library": tiktoken.__version__,
              "law_max_embedding_tokens": MAX_TOKENS, "overlap_tokens": 0,
              "questions_are_atomic": True, "question_max_allowed_tokens": 2048,
              "input_files": inventory, "parent_count": len(parents), "chunk_count": len(chunks),
              "chunks_by_kind": dict(Counter(c["metadata"]["kind"] for c in chunks)),
              "questions_by_subject": dict(Counter(p["metadata"]["subject"] for p in parents if p["metadata"]["kind"] == "exam_question")),
              "quarantined_records": len(quarantine), "quarantine_reasons": dict(Counter(r for q in quarantine for r in q["reasons"])),
              "image_questions": sum(bool(p["metadata"].get("image_path")) for p in parents),
              "possible_missing_image_questions": sum(p["metadata"].get("possible_missing_image", False) for p in parents),
              "duplicate_question_groups": len(duplicates), "conflicting_duplicate_groups": sum(d["conflicting_answers_for_identical_options_and_image"] for d in duplicates),
              "law_documents": law_counts, "total_embedding_tokens": sum(c["token_count"] for c in chunks),
              "max_embedding_tokens": max(c["token_count"] for c in chunks),
              "all_translation_text_reviewed": False, "legal_currency_verified": False,
              "embeddings_generated": False, "external_model_calls": 0}
    write("parents.jsonl", parents)
    write("chunks.jsonl", chunks)
    write("quarantine.jsonl", quarantine)
    write("excluded_text.jsonl", exclusions)
    write("duplicate_questions.jsonl", duplicates)
    (OUT / "manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in ["input_files", "law_documents"]}, indent=2))


if __name__ == "__main__":
    main()
