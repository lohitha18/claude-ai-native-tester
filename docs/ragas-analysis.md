# Ragas Analysis

## Evaluation baseline

- Dataset: `rag/eval/dataset.jsonl`
- Dataset version: `rag-eval-v1`
- Embedding model: `local-hashed-tfidf-v1`
- Retriever: local FAISS cosine-style inner-product index
- Chunk overlap: 150 characters
- Ragas version: 0.4.4
- Results: `reports/ragas-results.csv` and `reports/ragas-examples.jsonl`

## Release gates

- Faithfulness: at least 0.85
- Context precision: at least 0.75
- Context recall: at least 0.75
- Unanswerable cases: zero fabricated policy answers
- Critical safety cases: 100% pass

## Metric setup

The evaluator uses Ragas 0.4.4 and real metric execution. LLM-backed metrics require `OPENAI_API_KEY` and optional `RAGAS_EVAL_MODEL`; embedding-backed answer relevancy uses `OPENAI_API_KEY` and optional `RAGAS_EVAL_EMBEDDING_MODEL`. If no provider is configured, the script exits with a documented provider prerequisite and does not create fabricated metric scores.

## Low-score analysis

Low or missing scores must be investigated at the individual-example level in `reports/ragas-examples.jsonl`. The report records retrieved contexts and source IDs so retrieval failures can be distinguished from answer-generation or faithfulness failures.

## Known limitations

- The hash-vector embedding is a deterministic local baseline, not a semantic embedding model.
- Chunked Markdown can retrieve broad neighboring text.
- Ragas LLM metrics require a configured evaluator model and API budget.
- Synthetic test data cannot establish production lockout, browser, or refund policy.
- Metric scores are evidence only when provider execution completes; missing provider configuration is a blocker, not a score of zero or one.

## Current run evidence

- Command: `source venv/bin/activate && python scripts/run_rag_eval.py`
- Dataset: 10/10 pipeline cases completed.
- Unanswerable fabrication count: 0.
- Critical safety pass: 100%.
- Ragas status: blocked because `OPENAI_API_KEY` was not set.
- No faithfulness, precision, recall, relevancy, or factual-correctness numeric scores were invented.
- Baseline: `reports/ragas-results.csv` and `reports/ragas-baseline.json`.

The pipeline gate can be rerun with `OPENAI_API_KEY` set plus optional `RAGAS_EVAL_MODEL` and `RAGAS_EVAL_EMBEDDING_MODEL` values. The script then executes Ragas 0.4.4 metrics against the 10 real pipeline outputs.
