import unittest
import os
from pathlib import Path

from scripts import local_rag


class FakeModel:
    max_seq_length = 512

    @staticmethod
    def tokenizer(text, **kwargs):
        # Character-level stand-in exercises actual-tokenizer limits and offsets.
        return {"input_ids": list(range(len(text) + 2))}


def chunk(kind="traffic_law", text="A condition. " * 100):
    return {"chunk_id": "test", "parent_id": "article-1", "text": text,
            "embedding_text": "Title\n" + text, "token_count": 50,
            "parent_char_start": 10, "parent_char_end": 10 + len(text),
            "metadata": {"kind": kind}}


class ModelWindowTests(unittest.TestCase):
    def test_download_and_temporary_paths_stay_in_project(self):
        for key in ["HF_HOME", "HF_HUB_CACHE", "HF_XET_CACHE", "TORCH_HOME", "PIP_CACHE_DIR", "TEMP", "TMP"]:
            self.assertTrue(Path(os.environ[key]).resolve().is_relative_to(local_rag.ROOT), key)

    def test_rechunking_is_lossless_and_preserves_parent_offsets(self):
        source = chunk()
        result = local_rag.fit_chunks(FakeModel(), [source])
        self.assertGreater(len(result), 1)
        self.assertEqual("".join(r["text"] for r in result), source["text"])
        for i, r in enumerate(result):
            a, b = r["parent_char_start"] - 10, r["parent_char_end"] - 10
            self.assertEqual(source["text"][a:b], r["text"])
            self.assertLessEqual(r["model_token_count"], 512)
            self.assertEqual(r["chunk_index"], i)
            self.assertNotIn("token_count", r)

    def test_question_is_never_silently_truncated_or_split(self):
        with self.assertRaisesRegex(ValueError, "Atomic question"):
            local_rag.fit_chunks(FakeModel(), [chunk(kind="exam_question")])

    def test_fitting_question_retains_whole_text_and_id(self):
        source = chunk(kind="exam_question", text="Question? A. Yes B. No Correct answer: B. No")
        result = local_rag.fit_chunks(FakeModel(), [source])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["text"], source["text"])
        self.assertEqual(result[0]["chunk_id"], source["chunk_id"])


if __name__ == "__main__":
    unittest.main()
