# Local embeddings and search

## Connected answering model

Double-click `Start-RAG.cmd` or run `scripts/ask_rag.py`. The script prompts for either an
API service (OpenRouter, OpenAI, or another Chat Completions-compatible service)
or a running local server. API mode asks for its key with hidden entry and the
model ID. No API answering model is preselected. Providers require their own
keys; an OpenRouter key is
not an OpenAI key. Local mode asks for a server URL and lists its models when
`GET /v1/models` is supported; otherwise enter the exact model ID manually.
Examples: LM Studio `http://localhost:1234/v1`, Ollama `http://localhost:11434/v1`.
The server must already be running with the desired model available. Local server
keys are optional. Keys are kept only in memory for the session, never saved or
automatically read from the Desktop.

Embeddings and retrieval remain local. Only the question and selected source text
are sent to the chosen server. Up to eight sources (four Q/A and four law parents)
are considered, with a 28,000-character evidence budget for APIs and a smaller
10,000-character default for local models. These are character budgets, not exact
answering-model token counts. Configure a sufficient context window on your server
(8K or more is a starting point), or lower `--evidence-chars` if it rejects a long
request. The embedding model and index remain unchanged when switching answerers.
No alternate model is substituted. API prices depend on the chosen model.

```powershell
.\.venv\Scripts\python.exe scripts/ask_rag.py "What is the penalty for drunk driving?"
.\.venv\Scripts\python.exe scripts/ask_rag.py
```

The second command keeps the embedding model loaded for repeated independent
questions. Type `exit` to quit; follow-ups must be self-contained. Optional
`--kind exam_question` / `--kind traffic_law` constrain sources. `--subject 1`
or `--subject 4` constrain the Q/A sources; common law sources remain available.
For unattended use, supply `--provider`, `--base-url` where needed, and `--model`.
Use `--key-file` for an explicitly chosen key file or `--api-key-env` for the name
of an environment variable. Without either, API mode checks only the selected
provider's `OPENROUTER_API_KEY` or `OPENAI_API_KEY`, then asks for hidden key entry.
Do not place a raw key on the command line. Supplying only `--key-file` retains
the explicit OpenRouter shortcut; a model is still prompted if not specified.

```powershell
.\.venv\Scripts\python.exe scripts/ask_rag.py --provider local --base-url http://localhost:1234/v1 --model YOUR_SERVED_MODEL_ID
```

Answers should cite supplied sources and abstain on unsupported questions. Local
validation rejects invented citation IDs, missing inline references, malformed
JSON, and truncated responses, retrying at most once. Citation validation and a
model's grounding label are not independent factual verification. Existing corpus
review flags remain in force. Images are not sent to the model; it is instructed
not to infer unseen image contents. Very long law parents use the retrieved excerpt
instead, explicitly marked as an excerpt. Free-model outages/rate limits produce
an error instead of switching to another model. Generic/local providers receive
ordinary Chat Completions parameters without OpenRouter-only reasoning options
or mandatory server-side JSON mode; JSON is requested in the prompt and checked
locally. Models must support instruction-following and the requested JSON format.

The launcher is self-configuring within this project, not a standalone executable:
keep the project folder structure, including `scripts/`, `data/`, `.venv/`,
`.models/`, and `local-index/`. Python environments generally need recreating if moved to
another machine. Setup and downloaded dependencies stay under the project folder.

The project uses `BAAI/bge-small-en-v1.5`, pinned to model revision
`5c38ec7c405ec4b44b94cc5a9bb96e735b38267a`. This is a lightweight English
retrieval baseline, not a claim that it is the best model for this corpus.
It generates normalized 384-dimensional vectors locally on the CPU. Model
files download into `.models/` initially; source text is not sent to a model API.
Project libraries live in `.venv/`, and download/temporary caches live in
`.cache/` and `.models/`, all under `E:\Projects\RAG-pipeline`. The environment
uses the existing Python installation; no new system Python is installed.
Search loads cached model files with `local_files_only=True` and works offline.

## Try a search

Open PowerShell in `E:\Projects\RAG-pipeline` and run:

```powershell
.\.venv\Scripts\python.exe scripts/local_rag.py search "When should I switch to low beams at night?"
```

To search just the law documents, add `--kind traffic_law`. To search questions,
add `--kind exam_question`; optionally add `--subject 1` or `--subject 4`.
Use `--top 3` to display three results. The output is retrieved source passages,
including complete parent articles and image paths where relevant. For a generated
answer use `scripts/ask_rag.py` above. Similarity scores are not confidence or legal verification.

The local vector index consists of `local-index/vectors.npy`, aligned
`records.jsonl`, and a hash-checked `manifest.json`. Exact cosine search is
sufficient to start with this small corpus, without a database server. The
vectors and record IDs can later be imported into a vector database. Images
remain linked assets; only English text is embedded. Existing review flags and
quarantined records from preparation remain in effect.

The completed build contains **4,186 vectors** from 4,184 prepared chunks. Two
extra splits were needed for the embedding model's tokenizer; no source text was
truncated. The maximum final input is 506 model tokens. The 210-chunk pilot found
all eight expected test articles in the top five; the full corpus found six of
eight. The full result is the relevant baseline: retrieval needs further tuning
and broader evaluation before connecting a trusted answering system. Results are
saved in `local-index/evaluation.json`.

## Installation and builds

The project environment is `.venv`. To recreate it:

```powershell
python -m venv .venv
$env:PIP_CACHE_DIR = "$PWD\.cache\pip"
$env:TEMP = "$PWD\.cache\tmp"
$env:TMP = $env:TEMP
New-Item -ItemType Directory -Force $env:TEMP | Out-Null
.\.venv\Scripts\python.exe -m pip install -r requirements/requirements-local.txt
.\.venv\Scripts\python.exe scripts/local_rag.py build --pilot
.\.venv\Scripts\python.exe scripts/local_rag.py evaluate --pilot
.\.venv\Scripts\python.exe scripts/local_rag.py build
.\.venv\Scripts\python.exe scripts/local_rag.py evaluate
```

Build refuses to overwrite an existing index. Keep an old index in another
folder before rebuilding. Initial installation/model downloads need internet;
local inference does not need an API key. Dependencies and model caches are
excluded from Git, as are the derived local indexes.

Every input is checked against the model's actual 512-token window, including
special tokens. Longer law chunks are split again without losing text or
parent offsets. Questions remain whole; any oversized question stops the build
instead of being truncated. Query text uses the model author's retrieval
instruction. Searches verify corpus hashes and the pinned model configuration
to avoid mixing incompatible vectors or stale parent text.

`evaluation.json` contains eight source-derived, law-filtered retrieval smoke
tests. These exercise the pipeline; they are not a held-out benchmark and do not
test answer correctness, abstention, image understanding, or hybrid retrieval.
Next work is a representative independent retrieval evaluation, adding keyword
search/reranking if needed, and connecting retrieved passages to an answering model.

Sources: [model card](https://huggingface.co/BAAI/bge-small-en-v1.5),
[Sentence Transformers usage](https://sbert.net/docs/sentence_transformer/usage/usage.html).

Translation scripts require an explicit `OPENROUTER_MODEL` environment variable.
The review script accepts `--model` or `OPENROUTER_MODEL`. No model is preselected
for these scripts. Historical model names removed from stored metadata are marked
`historical-model-name-removed`; translations and review findings are retained.
