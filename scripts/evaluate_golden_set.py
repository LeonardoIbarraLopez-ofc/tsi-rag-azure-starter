from __future__ import annotations

import csv
import json
from pathlib import Path

from tsi_rag.config import Settings
from tsi_rag.service import RAGService


settings = Settings()
service = RAGService(settings)
cases = json.loads(Path("tests/golden_set.json").read_text(encoding="utf-8"))
rows = []
summary = []
MODES = ("keyword", "vector", "hybrid")

for case in cases:
    query = case["question"]
    expected_source = case.get("expected_source")
    expected_no_answer = case.get("expected_no_answer", False)
    for mode in MODES:
        hits = service.search(query, mode, settings.top_k)
        sources = [h.source for h in hits]
        hit = expected_source in sources if expected_source else None
        response = service.ask(query, mode, settings.top_k)
        no_answer_ok = (
            response.answer.startswith("No encuentro esa informacion") if expected_no_answer else None
        )
        rows.append(
            {
                "id": case["id"],
                "mode": mode,
                "question": query,
                "expected_source": expected_source or "",
                "retrieved_sources": "|".join(sources),
                "hit_at_k": hit,
                "expected_no_answer": expected_no_answer,
                "no_answer_ok": no_answer_ok,
                "latency_ms": response.total_ms,
            }
        )

report_dir = Path("reports")
report_dir.mkdir(exist_ok=True)
json_path = report_dir / "golden_set_results.json"
csv_path = report_dir / "golden_set_results.csv"
with csv_path.open("w", encoding="utf-8", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

for mode in MODES:
    retrieval_cases = [r for r in rows if r["hit_at_k"] is not None and r["mode"] == mode]
    hits = sum(1 for r in retrieval_cases if r["hit_at_k"] is True)
    no_answer_cases = [r for r in rows if r["expected_no_answer"] and r["mode"] == mode]
    abstentions = sum(1 for r in no_answer_cases if r["no_answer_ok"] is True)
    summary.append(
        {
            "mode": mode,
            "k": settings.top_k,
            "hit_at_k": round(hits / max(1, len(retrieval_cases)), 4),
            "correct_hits": hits,
            "answerable_cases": len(retrieval_cases),
            "abstention_rate": round(abstentions / max(1, len(no_answer_cases)), 4),
            "no_answer_cases": len(no_answer_cases),
        }
    )
    print(
        f"{mode}: Hit@{settings.top_k}={hits}/{len(retrieval_cases)} "
        f"({hits / max(1, len(retrieval_cases)):.1%}); "
        f"abstencion={abstentions}/{len(no_answer_cases)}"
    )
json_path.write_text(
    json.dumps({"rows": rows, "summary": summary}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"Reporte detallado: {csv_path}")
print(f"Reporte resumido: {json_path}")
