# Chinese driving prep. RAG.

English question and traffic-law retrieval, prepared and embedded locally.
Project libraries, model downloads, caches, and indexes live under this project
directory.

Startup script: `Start-RAG.cmd`.

Startup asks whether to use an API service or a running local model server.
API options are OpenRouter, OpenAI, or another
Chat Completions-compatible API. 
Start the model server yourself first. No Desktop key file is assumed and no alternate model is substituted.

All project files remain under the project directory; the launcher uses its own folder rather than a fixed drive.

The model writes a concise answer with source references. Citation IDs are checked
against retrieved sources.

To inspect retrieval without calling the answering model:

```powershell
Set-Location 'E:\Projects\RAG-pipeline'
.\.venv\Scripts\python.exe scripts/local_rag.py search "When should I switch to low beams at night?" --top 3
```

This command retrieves source passages only.
The default searches both questions and laws. Add `--kind exam_question` to search
only Q/A records, or `--kind traffic_law` to search only law documents.
Translations and legal validity still require review. 
Text embeddings do not
encode the linked exam images. Quarantined questions are excluded from the index.

- [Local setup, search, and rebuilding](docs/LOCAL_RAG.md)
- [Chunk preparation and validation](docs/RAG_PREPARATION.md)
- [Sources and review limitations](docs/DATA_SOURCES.md)

Run the checks with:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
