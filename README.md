# Chinese driving-test RAG

English question and traffic-law retrieval, prepared and embedded locally.
Project libraries, model downloads, caches, and indexes live under this project
directory on `E:`. No embedding API key or database service is required.

Double-click `Start-RAG.cmd`, or start it in PowerShell:

```powershell
Set-Location 'E:\Projects\RAG-pipeline'
.\.venv\Scripts\python.exe ask_rag.py "When should I use low beams?"
```

Startup asks whether to use an API service or a running local model server.
API options are OpenRouter (default model: Nemotron free), OpenAI, or another
Chat Completions-compatible API. Enter the provider's own key using hidden input;
keys are kept in memory for the session and never saved. Local mode asks for the
server URL, optionally its key, and a model ID (or a model from the server's list).
LM Studio and Ollama server addresses are shown as examples. Start the model server
yourself first. No Desktop key file is assumed and no alternate model is substituted.

Run `ask_rag.py` without a question for repeated independent questions; type
`exit` to quit. Local retrieval searches Q/A and supporting law passages, then
sends the question and selected excerpts to the chosen server. API services need
internet and may charge for the model you choose. All project files remain under
the project directory; the launcher uses its own folder rather than a fixed drive.

The model writes a concise answer with source references. Citation IDs are checked
against retrieved sources; this does not independently verify each claim. Free
provider capacity and rate limits can interrupt requests. Follow-up questions
should be self-contained; no conversation history is sent between questions.

To inspect retrieval without calling the answering model:

```powershell
Set-Location 'E:\Projects\RAG-pipeline'
.\.venv\Scripts\python.exe local_rag.py search "When should I switch to low beams at night?" --top 3
```

This command retrieves source passages only.
The default searches both questions and laws. Add `--kind exam_question` to search
only Q/A records, or `--kind traffic_law` to search only law documents.
Translations and legal validity still require review. Text embeddings do not
encode the linked exam images. Quarantined questions are excluded from the index.

- [Local setup, search, and rebuilding](LOCAL_RAG.md)
- [Chunk preparation and validation](RAG_PREPARATION.md)
- [Sources and review limitations](DATA_SOURCES.md)
