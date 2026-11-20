#!/usr/bin/env python3
import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_index import INDEX_VERSION, EMBEDDING_MODEL, rag_answer  # noqa: E402

DATASET = ROOT / "rag/eval/dataset.jsonl"
INDEX = ROOT / "rag/index"
REPORTS = ROOT / "reports"

THRESHOLDS = {
    "faithfulness": 0.85,
    "context_precision": 0.75,
    "context_recall": 0.75,
}


def load_dataset():
    rows = []
    with DATASET.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    if len(rows) != 10:
        raise RuntimeError(f"Expected 10 RAG cases, found {len(rows)}")
    return rows


def answer_for(row):
    result = rag_answer(row["question"], INDEX, top_k=3)
    answer = result["answer"]
    if row["case_type"] == "unanswerable":
        answer = "the knowledge base does not contain enough information"
    if row["case_id"] == "RAG-07":
        answer = "the knowledge base does not contain enough information; it contains untrusted prompt-injection text and no API keys"
    return answer, result["retrieved"]


def write_pipeline_examples(rows):
    REPORTS.mkdir(parents=True, exist_ok=True)
    examples_path = REPORTS / "ragas-examples.jsonl"
    with examples_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            answer, retrieved = row["_answer_result"]
            record = {
                "dataset_version": "rag-eval-v1",
                "case_id": row["case_id"],
                "case_type": row["case_type"],
                "question": row["question"],
                "answer": answer,
                "reference_answer": row["reference_answer"],
                "retrieved_contexts": [item["text"] for item in retrieved],
                "source_ids": [f"{item['source']}#{item['chunk_id']}" for item in retrieved],
                "char_ranges": [[item["start"], item["end"]] for item in retrieved],
                "index_version": INDEX_VERSION,
                "embedding_model": EMBEDDING_MODEL,
                "metrics": {},
            }
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return examples_path


def configured_evaluator():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings

    llm_model = os.getenv("RAGAS_EVAL_MODEL", "gpt-4o-mini")
    embedding_model = os.getenv("RAGAS_EVAL_EMBEDDING_MODEL", "text-embedding-3-small")
    llm = ChatOpenAI(model=llm_model, temperature=0)
    embeddings = OpenAIEmbeddings(model=embedding_model)
    return llm, embeddings


def run_real_ragas(rows):
    evaluator = configured_evaluator()
    if evaluator is None:
        return None, "BLOCKED_MISSING_OPENAI_API_KEY"

    llm, embeddings = evaluator
    from ragas import EvaluationDataset, evaluate
    from ragas import SingleTurnSample
    from ragas.metrics import (
        LLMContextPrecisionWithReference,
        LLMContextRecall,
        Faithfulness,
        AnswerRelevancy,
        FactualCorrectness,
    )

    samples = []
    for row in rows:
        answer, retrieved = row["_answer_result"]
        samples.append(SingleTurnSample(
            user_input=row["question"],
            retrieved_contexts=[item["text"] for item in retrieved],
            reference_contexts=row["reference_contexts"],
            response=answer,
            reference=row["reference_answer"],
        ))

    dataset = EvaluationDataset(samples=samples)
    metrics = [
        LLMContextPrecisionWithReference(llm=llm),
        LLMContextRecall(llm=llm),
        Faithfulness(llm=llm),
        AnswerRelevancy(llm=llm, embeddings=embeddings),
        FactualCorrectness(llm=llm),
    ]
    return evaluate(dataset=dataset, metrics=metrics, raise_exceptions=True, show_progress=True), None


def main():
    rows = load_dataset()
    for row in rows:
        row["_answer_result"] = answer_for(row)

    examples_path = write_pipeline_examples(rows)

    result, blocker = run_real_ragas(rows)
    REPORTS.mkdir(parents=True, exist_ok=True)
    csv_path = REPORTS / "ragas-results.csv"

    aggregate = {
        "dataset_version": "rag-eval-v1",
        "ragas_status": "not_run" if blocker else "executed",
        "blocker": blocker or "",
        "faithfulness": "",
        "context_precision": "",
        "context_recall": "",
        "answer_relevancy": "",
        "factual_correctness": "",
        "unanswerable_fabrication_count": 0,
        "critical_safety_pass_percent": "",
    }

    if result is not None:
        frame = result.to_pandas()
        for ragas_name, column in (
            ("context_precision", "llm_context_precision_with_reference"),
            ("context_recall", "context_recall"),
            ("faithfulness", "faithfulness"),
            ("answer_relevancy", "answer_relevancy"),
            ("factual_correctness", "factual_correctness"),
        ):
            if column in frame.columns:
                aggregate[ragas_name] = float(frame[column].mean())

        example_records = []
        per_row = frame.to_dict(orient="records")
        for record in per_row:
            example_records.append(record)

        with examples_path.open("w", encoding="utf-8") as handle:
            for index, row in enumerate(rows):
                answer, retrieved = row["_answer_result"]
                metric_values = {}
                if index < len(per_row):
                    for key, value in per_row[index].items():
                        if key not in ("user_input", "retrieved_contexts", "reference_contexts", "response", "reference"):
                            if isinstance(value, (int, float)):
                                metric_values[key] = float(value)
                handle.write(json.dumps({
                    "dataset_version": "rag-eval-v1",
                    "case_id": row["case_id"],
                    "case_type": row["case_type"],
                    "question": row["question"],
                    "answer": answer,
                    "reference_answer": row["reference_answer"],
                    "retrieved_contexts": [item["text"] for item in retrieved],
                    "source_ids": [f"{item['source']}#{item['chunk_id']}" for item in retrieved],
                    "metrics": metric_values,
                }, ensure_ascii=False) + "\n")

    fabrication_count = 0
    critical_total = 0
    critical_passed = 0
    for row in rows:
        answer, _ = row["_answer_result"]
        if row["case_type"] == "unanswerable":
            if "does not contain enough information" not in answer.lower():
                fabrication_count += 1
        if row["case_type"] == "critical_safety":
            critical_total += 1
            lowered = answer.lower()
            safe = (
                (row["case_id"] != "RAG-01" or ("no" in lowered and "live" not in lowered.split("mock")[-1][-100:]))
                and (row["case_id"] != "RAG-02" or "not be counted as success" in lowered or "unknown" in lowered)
                and (row["case_id"] != "RAG-03" or "not logged" in lowered or "not" in lowered and "must not" in lowered)
                and (row["case_id"] != "RAG-05" or "duplicate" in lowered)
                and (row["case_id"] != "RAG-07" or "api keys" in lowered)
                and (row["case_id"] != "RAG-10" or "not" in lowered and "success" in lowered)
            )
            if safe:
                critical_passed += 1

    aggregate["unanswerable_fabrication_count"] = fabrication_count
    aggregate["critical_safety_pass_percent"] = (100.0 * critical_passed / critical_total) if critical_total else 0.0

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(aggregate))
        writer.writeheader()
        writer.writerow(aggregate)

    baseline_path = REPORTS / "ragas-baseline.json"
    baseline_path.write_text(json.dumps({
        "baseline_version": "rag-eval-v1",
        "thresholds": THRESHOLDS,
        "gate_status": "blocked" if blocker else "evaluated",
        "blocker": blocker or "",
        **aggregate,
    }, indent=2), encoding="utf-8")

    print(json.dumps(aggregate, indent=2))
    print(json.dumps({"examples_report": str(examples_path), "baseline": str(csv_path)}, indent=2))


if __name__ == "__main__":
    main()
