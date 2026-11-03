# English corpus preparation

Prepared on 2026-11-03. This is the stage before generating embeddings and indexing.
Original questions, translations, and images are unchanged.

## Output

`data/prepared/chunks.jsonl` is the embedding input: embed **only `embedding_text`**.
Use `chunk_id` as the index key. Store `text`, `parent_id`, and `metadata` with the
vector; index `embedding_text` for keyword retrieval as well. This is a neutral
JSONL exchange format, not a database-specific import file.

`data/prepared/parents.jsonl` holds complete questions and law articles. After retrieval,
resolve `parent_id` to recover a complete article when a rule spans several chunks.
Deduplicate retrieved chunks by parent before assembling the answer context.

`data/prepared/manifest.json` records counts, exact source hashes, tokenizer, and limits.
`data/prepared/quarantine.jsonl` holds excluded question records with repair reasons.
`data/prepared/excluded_text.jsonl` preserves removed website headers, footers, and
contents lists for inspection. `data/prepared/duplicate_questions.jsonl` reports repeated
question wording without deleting distinct records or diagrams.

## Decisions for this corpus

- Each question is one complete chunk, with its English options, answer labels and
  answer text, and existing English explanation. Chinese-only explanations are not
  invented or translated during this step. Single-line option lists are normalized.
- Law text is regrouped into articles, with document title, chapter, section, and
  article number attached. Promulgation notices, amendment decisions, and attachment
  references remain separately retrievable. Eight documents contain 723 articles.
- Long units split at paragraph, numbered clause, sentence, or whitespace boundaries,
  with a maximum of 512 tokens **including the contextual prefix**. Questions remain
  atomic, with a separate 2,048-token validation ceiling. Current questions also fit
  within 512 tokens. There is zero artificial overlap: complete article parents supply
  the surrounding context. No unrelated articles or questions are merged.
- Token counts use `cl100k_base`, a preparation baseline. Once the embedding model is
  selected, count its actual tokens, check its input limits, and apply its required
  query/document prefixes before embedding. Do not silently truncate.
- Paths, hashes, record IDs, source URLs, article numbers, and exact English translation
  segment offsets support citations, troubleshooting, and rebuilding. Chunk IDs depend
  on their content and parent. Rebuilds from the same inputs are deterministic.
- Image-based questions retain paths to all 787 existing images, relative to the project
  root. Images are not described or embedded here. Display the image with a retrieved
  question, or provide it to a vision-capable answering model. Text vectors alone do
  not represent the contents of these images.

## Current results and remaining review

4,184 chunks: 3,426 questions (2,545 Subject 1; 881 Subject 4), plus 758 law chunks.
There are 4,161 parent records and 417,695 embedding-input tokens in total.
23 Subject 4 questions are quarantined: six malformed answer keys and 17 questions
that explicitly reference unavailable images. No replacement answers were guessed.
Four additional included questions have a broad possible-image flag for inspection;
this heuristic is not an exhaustive image-dependency audit.

Review flags are retained. Preparation validates structure and coverage, not the
truth of answers, completeness of translations, legal accuracy, or current validity.
Previous machine review did not complete all suggestion adjudications. Some law
translations originally began or ended mid-sentence. Their English fragments are
joined with a newline without rewriting; `crosses_translation_boundary` flags affected
parents, and exact segment offsets let a reviewer check them. Splitting an article
can separate a condition from an exception, so expand its parent before answering.
Attachment references do not imply their missing tables or images are available.

## Rebuild and validate

From the project directory in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements/requirements-preparation.txt
.\.venv\Scripts\python.exe scripts/prepare_rag.py
.\.venv\Scripts\python.exe -m unittest tests.test_prepare_rag -v
```

The initial tokenizer setup may download its public vocabulary. Preparation makes
no embedding, translation, or other model calls and does not upload source material.
The source allowlist excludes backups, review reports, duplicate CSV/PDF editions,
and Chinese-only files from embedding inputs. Incomplete or stale law translations
stop the build. Rerunning overwrites only the named derived files in `data/prepared/`.

## Research and next step

Microsoft recommends choosing chunking by document structure and evaluating it for
the actual queries, rather than treating a single size as universally best:
https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase
Its chunking guidance discusses content-aware boundaries and contextual titles:
https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

Anthropic's experiments support supplying chunk context and combining semantic
retrieval with keyword retrieval (BM25), followed by reranking:
https://www.anthropic.com/research/contextual-retrieval
Here contextual prefixes come from existing titles and headings, with no generated
summaries that might introduce unsupported details. Those experimental results do
not establish an optimal configuration for this driving-test corpus.

Next: choose an embedding model, check its tokenizer and limits, embed `embedding_text`,
and persist the vectors with their text and metadata. Start with hybrid keyword/vector
retrieval, optional reranking, and parent expansion. Filter by subject/document when
appropriate and carry review flags and image requirements into the answering step.
Use a separate representative query set (including negations, exceptions, multi-answer
questions, image cases, and out-of-scope questions) to measure retrieval recall and
grounded answers. This build does not claim retrieval accuracy before that evaluation.
