---
name: rag-evaluation
description: Evaluate RAG datasets and retrieval, grounding, and relevance behavior
---

# RAG Evaluation Workflow

- Validate that every dataset row contains a question, reference answer, and reference context.
- Include answerable, ambiguous, stale, conflicting, and unanswerable cases.
- Record retrieved contexts and generated answers for every evaluated row.
- Evaluate retrieval separately from faithfulness and answer relevance.
- Record the model, prompt, embedding model, chunking strategy, retriever, and dataset versions.
- Never use one metric as the only release decision.
- Compare results to a baseline and inspect individual examples.
- Save a machine-readable report and list its limitations.
