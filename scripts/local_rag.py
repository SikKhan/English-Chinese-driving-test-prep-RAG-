"""Local CPU embeddings and exact cosine search; no database service or model API.

python scripts/local_rag.py build [--pilot]
python scripts/local_rag.py search "When should I use low beams?" [--kind traffic_law]
python scripts/local_rag.py evaluate [--pilot]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
# Set these before importing any model libraries. Keep project downloads off C:.
for key, relative in {
    "HF_HOME": ".models/hf-home", "HF_HUB_CACHE": ".models", "HF_XET_CACHE": ".models/xet",
    "SENTENCE_TRANSFORMERS_HOME": ".models", "TORCH_HOME": ".models/torch",
    "XDG_CACHE_HOME": ".cache", "PIP_CACHE_DIR": ".cache/pip", "TEMP": ".cache/tmp", "TMP": ".cache/tmp",
}.items():
    folder = ROOT / relative
    folder.mkdir(parents=True, exist_ok=True)
    os.environ[key] = str(folder)
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("DO_NOT_TRACK", "1")
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
MODEL = "BAAI/bge-small-en-v1.5"
REVISION = "5c38ec7c405ec4b44b94cc5a9bb96e735b38267a"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "
EVAL = [
    ("How long is a driver's penalty points cycle?", "points-regulation-2022:article-3"),
    ("What point deduction amounts can a single traffic violation carry?", "points-regulation-2022:article-7"),
    ("Can someone drive when excessively tired or after drinking alcohol?", "road-traffic-safety-law-2021:article-22"),
    ("Do a traffic officer's directions take priority over traffic lights?", "road-traffic-safety-law-2021:article-38"),
    ("Who must obtain compulsory motor vehicle accident liability insurance?", "compulsory-insurance-regulation-2019:article-2"),
    ("At what distance should I switch to low beams when meeting traffic at night?", "implementation-regulation-2017:article-48"),
    ("What age and physical conditions apply when requesting a driving licence?", "driving-licence-rules-2025:article-14"),
    ("What is the purpose and legal basis of motor vehicle registration rules?", "vehicle-registration-2022:article-1"),
]


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def load_model(offline):
    import torch
    from sentence_transformers import SentenceTransformer
    torch.set_num_threads(min(8, os.cpu_count() or 1))
    model = SentenceTransformer(MODEL, revision=REVISION, device="cpu", cache_folder=str(ROOT / ".models"),
                                trust_remote_code=False, local_files_only=offline)
    if model.get_embedding_dimension() != 384 or model.max_seq_length != 512:
        raise RuntimeError("Unexpected embedding model configuration")
    return model


def count_tokens(model, text):
    return len(model.tokenizer(text, add_special_tokens=True, truncation=False)["input_ids"])


def fit_chunks(model, source):
    """Re-split long law chunks with the actual model tokenizer, never truncate."""
    result = []
    for row in source:
        text = row["text"]
        assert row["embedding_text"].endswith(text)
        prefix = row["embedding_text"][:-len(text)]
        if count_tokens(model, row["embedding_text"]) <= model.max_seq_length:
            copy = dict(row)
            copy["preparation_token_count"] = copy.pop("token_count")
            copy["model_token_count"] = count_tokens(model, copy["embedding_text"])
            result.append(copy)
            continue
        if row["metadata"]["kind"] == "exam_question":
            raise ValueError(f"Atomic question exceeds this model's window: {row['chunk_id']}; use a longer-context model")
        start = 0
        pieces = []
        while start < len(text):
            lo, hi = start + 1, len(text)
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if count_tokens(model, prefix + text[start:mid]) <= model.max_seq_length:
                    lo = mid
                else:
                    hi = mid - 1
            end = lo
            if end < len(text):
                for pattern in [r"\n\s*\n", r"(?<=[.!?;])\s+", r"\s+"]:
                    breaks = [start + m.end() for m in re.finditer(pattern, text[start:end]) if m.end() > (end - start) // 2]
                    if breaks:
                        end = breaks[-1]
                        break
            fragment = text[start:end]
            copy = dict(row)
            copy["source_preparation_token_count"] = copy.pop("token_count")
            copy.update(chunk_id=row["chunk_id"] + f"-bge-{len(pieces)}", source_chunk_id=row["chunk_id"],
                        text=fragment, embedding_text=prefix + fragment,
                        parent_char_start=row["parent_char_start"] + start,
                        parent_char_end=row["parent_char_start"] + end,
                        model_token_count=count_tokens(model, prefix + fragment))
            if not fragment or copy["model_token_count"] > model.max_seq_length:
                raise ValueError("Unable to fit a chunk without truncation")
            pieces.append(copy)
            start = end
        assert "".join(p["text"] for p in pieces) == text
        result.extend(pieces)
    # Recompute indices after model-specific splitting.
    groups = {}
    for row in result:
        groups.setdefault(row["parent_id"], []).append(row)
    for group in groups.values():
        for i, row in enumerate(group):
            row.update(chunk_index=i, chunk_count=len(group))
    return result


def build(pilot):
    import numpy as np
    out = ROOT / ("local-index-pilot" if pilot else "local-index")
    if out.exists():
        raise FileExistsError(f"Index already exists: {out}. Choose a new output location before rebuilding.")
    inputs = rows(ROOT / "data/prepared/chunks.jsonl")
    model = load_model(offline=(ROOT / "local-index-pilot/manifest.json").is_file())
    if pilot:
        wanted = {pid for _, pid in EVAL}
        inputs = [r for r in inputs if r["parent_id"] in wanted] + inputs[:100] + [r for r in inputs if r["metadata"]["kind"] == "traffic_law"][:100]
        inputs = list({r["chunk_id"]: r for r in inputs}.values())
    records = fit_chunks(model, inputs)
    print(f"Embedding {len(records)} chunks locally on CPU; all inputs checked against the actual tokenizer.", flush=True)
    vectors = model.encode([r["embedding_text"] for r in records], batch_size=32, normalize_embeddings=True,
                           convert_to_numpy=True, show_progress_bar=True, prompt="").astype(np.float32)
    if vectors.shape != (len(records), 384) or not np.isfinite(vectors).all():
        raise ValueError("Invalid embeddings")
    if not np.allclose(np.linalg.norm(vectors, axis=1), 1, atol=1e-5):
        raise ValueError("Vectors are not normalized")
    out.mkdir()
    np.save(out / "vectors.npy", vectors, allow_pickle=False)
    (out / "records.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
    manifest = {"model": MODEL, "revision": REVISION, "device": "cpu", "dimensions": 384,
                "normalized": True, "distance": "cosine", "query_prefix": QUERY_PREFIX,
                "source_chunks_sha256": file_sha(ROOT / "data/prepared/chunks.jsonl"),
                "source_parents_sha256": file_sha(ROOT / "data/prepared/parents.jsonl"),
                "vectors_sha256": file_sha(out / "vectors.npy"), "records_sha256": file_sha(out / "records.jsonl"),
                "original_chunk_count": len(inputs), "vector_count": len(records), "pilot": pilot,
                "max_model_tokens": max(r["model_token_count"] for r in records),
                "packages": {p: importlib.metadata.version(p) for p in ["sentence-transformers", "transformers", "torch", "numpy"]}}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


def open_index(pilot):
    import numpy as np
    out = ROOT / ("local-index-pilot" if pilot else "local-index")
    manifest = json.loads((out / "manifest.json").read_text())
    if manifest["model"] != MODEL or manifest["revision"] != REVISION or manifest["query_prefix"] != QUERY_PREFIX:
        raise ValueError("Index/query model configuration mismatch")
    for name in ["vectors", "records"]:
        path = out / ("vectors.npy" if name == "vectors" else "records.jsonl")
        if file_sha(path) != manifest[name + "_sha256"]:
            raise ValueError("Index file hash mismatch")
    if file_sha(ROOT / "data/prepared/parents.jsonl") != manifest["source_parents_sha256"]:
        raise ValueError("Parent corpus changed; rebuild the index")
    if file_sha(ROOT / "data/prepared/chunks.jsonl") != manifest["source_chunks_sha256"]:
        raise ValueError("Chunk corpus changed; rebuild the index")
    records = rows(out / "records.jsonl")
    vectors = np.load(out / "vectors.npy", allow_pickle=False)
    if vectors.shape != (len(records), manifest["dimensions"]):
        raise ValueError("Vector/record alignment mismatch")
    return out, records, vectors


def rank(model, records, vectors, query, k=5, kind=None, subject=None):
    import numpy as np
    text = QUERY_PREFIX + query.strip()
    if not query.strip() or count_tokens(model, text) > model.max_seq_length:
        raise ValueError("Query is empty or exceeds the model window")
    vector = model.encode([text], normalize_embeddings=True, convert_to_numpy=True, prompt="")[0]
    scores = vectors @ vector
    ordered = np.argsort(-scores)
    seen, result = set(), []
    for index in ordered:
        row = records[int(index)]
        if kind and row["metadata"]["kind"] != kind:
            continue
        if subject and row["metadata"].get("subject") != subject:
            continue
        if row["parent_id"] in seen:
            continue
        seen.add(row["parent_id"])
        result.append({"parent_id": row["parent_id"], "score": float(scores[index]), "record": row})
        if len(result) == k:
            break
    return result


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build").add_argument("--pilot", action="store_true")
    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--pilot", action="store_true")
    search.add_argument("--kind", choices=["traffic_law", "exam_question"])
    search.add_argument("--subject", type=int, choices=[1, 4])
    search.add_argument("--top", type=int, default=5)
    sub.add_parser("evaluate").add_argument("--pilot", action="store_true")
    args = parser.parse_args()
    if args.command == "build":
        build(args.pilot)
        return
    out, records, vectors = open_index(args.pilot)
    model = load_model(offline=True)
    if args.command == "evaluate":
        results = []
        for query, expected in EVAL:
            matches = rank(model, records, vectors, query, kind="traffic_law")
            ids = [m["parent_id"] for m in matches]
            results.append({"query": query, "expected_parent_id": expected, "retrieved_parent_ids": ids,
                            "hit_at_5": expected in ids, "rank": ids.index(expected) + 1 if expected in ids else None})
        report = {"description": "Eight source-derived, law-filtered retrieval smoke tests; not a held-out quality benchmark.",
                  "hit_at_5": sum(r["hit_at_5"] for r in results), "queries": len(results), "results": results}
        (out / "evaluation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
    else:
        if not 1 <= args.top <= 50:
            raise ValueError("--top must be between 1 and 50")
        parents = {p["parent_id"]: p for p in rows(ROOT / "data/prepared/parents.jsonl")}
        for match in rank(model, records, vectors, args.query, args.top, args.kind, args.subject):
            parent = parents[match["parent_id"]]
            print(f"\nSimilarity {match['score']:.3f} | {parent['metadata']['citation']}")
            print(parent["text"])
            if parent["metadata"].get("image_path"):
                print("Image:", ROOT / parent["metadata"]["image_path"])
        print("\nRetrieved source passages only. Similarity is not confidence; review flags still apply.")


if __name__ == "__main__":
    main()
