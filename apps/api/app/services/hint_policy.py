"""Hint policy heuristics for progressive disclosure."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(slots=True)
class HintState:
    """Tracks hint disclosure state for a learner."""

    hints_revealed: int = 0
    allow_solution: bool = False


class HintPolicy:
    """Simple keyword-based policy to prevent early solution leakage."""

    def __init__(self) -> None:
        self._solution_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in (
                r"jawaban akhir", r"kasih (?:tau|tahu) jawab", r"langsung jawaban", r"final answer"
            )
        ]

    def evaluate(self, message: str, state: HintState | None = None) -> HintState:
        state = state or HintState()
        if any(pattern.search(message) for pattern in self._solution_patterns):
            return HintState(hints_revealed=state.hints_revealed, allow_solution=False)
        return HintState(hints_revealed=state.hints_revealed + 1, allow_solution=state.allow_solution)


__all__ = ["HintPolicy", "HintState"]
