from __future__ import annotations

import re

from .models import SearchHit


INJECTION_PATTERNS = {
    "ignore_previous": re.compile(r"ignora\s+(todas\s+)?las\s+instrucciones", re.I),
    "system_override": re.compile(r"(system|sistema)\s*:\s*", re.I),
    "reveal_secret": re.compile(r"(revela|muestra|imprime).*(secreto|clave|password|api[- ]?key)", re.I),
    "role_change": re.compile(r"\b(actua|actúa|ahora eres|you are now)\b", re.I),
}


def detect_prompt_injection(text: str) -> list[str]:
    return [name for name, pattern in INJECTION_PATTERNS.items() if pattern.search(text)]


def build_untrusted_context(hits: list[SearchHit]) -> tuple[str, list[str]]:
    flags: list[str] = []
    sections: list[str] = []
    for hit in hits:
        found = detect_prompt_injection(hit.content)
        flags.extend(f"{hit.source}:{flag}" for flag in found)
        sections.append(
            "\n".join(
                [
                    f"[INICIO DOCUMENTO NO CONFIABLE | fuente={hit.source} | chunk={hit.chunk_id}]",
                    hit.content,
                    "[FIN DOCUMENTO NO CONFIABLE]",
                ]
            )
        )
    return "\n\n".join(sections), sorted(set(flags))
