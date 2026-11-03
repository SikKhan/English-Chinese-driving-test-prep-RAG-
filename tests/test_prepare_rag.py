"""Checks source coverage and lossless retrieval preparation (no model calls)."""
import json
import unittest
from collections import defaultdict

from scripts import prepare_rag as prep


def records(name):
    return [json.loads(line) for line in (prep.OUT / name).read_text(encoding="utf-8").splitlines()]


class PreparationTests(unittest.TestCase):
    def test_split_preserves_every_character_and_bounds_full_embedding_input(self):
        text = ("(1) Do not proceed unless the crossing is clear.\n" * 150) + "Exception: emergency vehicles."
        prefix = "Traffic law | Article 4\n\n"
        spans = list(prep.split_spans(text, prefix))
        self.assertGreater(len(spans), 1)
        self.assertEqual("".join(text[a:b] for a, b in spans), text)
        self.assertTrue(all(prep.tokens(prefix + text[a:b]) <= prep.MAX_TOKENS for a, b in spans))

    def test_all_question_records_are_accounted_for_once(self):
        included = [p for p in records("parents.jsonl") if p["metadata"]["kind"] == "exam_question"]
        held = records("quarantine.jsonl")
        for subject, file in [(1, "data/subject1/data/questions_bilingual.json"), (4, "data/subject4/subject4_translations.json")]:
            source_ids = [r["id"] for r in prep.read(file)]
            output_ids = [r["metadata"]["record_id"] for r in included if r["metadata"]["subject"] == subject]
            output_ids += [r["record_id"] for r in held if r["source_file"] == file]
            self.assertCountEqual(source_ids, output_ids)
            self.assertEqual(len(output_ids), len(set(output_ids)))

    def test_every_chunk_resolves_to_parent_and_preserves_parent_text(self):
        parents = {p["parent_id"]: p for p in records("parents.jsonl")}
        grouped = defaultdict(list)
        for chunk in records("chunks.jsonl"):
            parent = parents[chunk["parent_id"]]
            a, b = chunk["parent_char_start"], chunk["parent_char_end"]
            self.assertEqual(parent["text"][a:b], chunk["text"])
            self.assertEqual(prep.tokens(chunk["embedding_text"]), chunk["token_count"])
            if chunk["metadata"]["kind"] == "traffic_law":
                self.assertLessEqual(chunk["token_count"], 512)
            grouped[chunk["parent_id"]].append(chunk)
        self.assertEqual(set(parents), set(grouped))
        for pid, children in grouped.items():
            self.assertEqual("".join(c["text"] for c in sorted(children, key=lambda c: c["chunk_index"])), parents[pid]["text"])
            if parents[pid]["metadata"]["kind"] == "exam_question":
                self.assertEqual(len(children), 1)

    def test_law_provenance_reconstructs_exact_translated_text(self):
        cache = {}
        counts = defaultdict(list)
        for parent in records("parents.jsonl"):
            meta = parent["metadata"]
            if meta["kind"] != "traffic_law":
                continue
            file = meta["source_file"]
            if file not in cache:
                cache[file] = {r["chunk"]: r["text_en"] for r in prep.read(file)}
            fragments = [cache[file][s["translation_chunk"]][s["text_en_char_start"]:s["text_en_char_end"]] for s in meta["translation_source_spans"]]
            self.assertEqual("\n".join(fragments), parent["text"])
            if meta["article_number"]:
                counts[meta["document_id"]].append(meta["article_number"])
        expected = {"accident-procedure-2017": 114, "compulsory-insurance-regulation-2019": 46,
                    "driving-licence-rules-2025": 111, "implementation-regulation-2017": 115,
                    "points-regulation-2022": 37, "road-traffic-safety-law-2021": 124,
                    "vehicle-registration-2022": 93, "violation-procedure-2020": 83}
        self.assertEqual(set(counts), set(expected))
        for name, count in expected.items():
            self.assertEqual(counts[name], list(range(1, count + 1)))

    def test_source_hashes_unchanged_and_image_references_resolve(self):
        manifest = prep.read("data/prepared/manifest.json")
        for source in manifest["input_files"]:
            self.assertEqual(prep.sha((prep.ROOT / source["path"]).read_bytes()), source["sha256"])
        for parent in records("parents.jsonl"):
            image = parent["metadata"].get("image_path")
            if image:
                self.assertTrue((prep.ROOT / image).is_file())


if __name__ == "__main__":
    unittest.main()
