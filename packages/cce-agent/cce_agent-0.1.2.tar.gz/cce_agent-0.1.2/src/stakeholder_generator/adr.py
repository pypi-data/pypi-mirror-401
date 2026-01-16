# src/stakeholder_generator/adr.py
import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ArchitectureConsideration:
    """Represents an architecture consideration."""

    consideration: str
    details: str


@dataclass
class ArchitectureDecision:
    """Represents an Architecture Decision Record (ADR)."""

    title: str
    status: str  # e.g., 'Proposed', 'Accepted', 'Rejected'
    context: str
    decision: str
    consequences: str
    considerations: list[ArchitectureConsideration] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class ADRManager:
    """Manages the creation and storage of ADRs."""

    def __init__(self, output_directory: str):
        self.output_directory = os.path.join(output_directory, "adrs")
        os.makedirs(self.output_directory, exist_ok=True)

    def create_adr(
        self,
        title: str,
        context: str,
        decision: str,
        consequences: str,
        considerations: list[dict] | None = None,
        status: str = "Accepted",
    ) -> ArchitectureDecision:
        """Creates and saves a new ADR."""

        parsed_considerations = []
        if considerations:
            for cons in considerations:
                parsed_considerations.append(
                    ArchitectureConsideration(
                        consideration=cons.get("consideration", ""), details=cons.get("details", "")
                    )
                )

        adr = ArchitectureDecision(
            title=title,
            status=status,
            context=context,
            decision=decision,
            consequences=consequences,
            considerations=parsed_considerations,
        )

        self.save_adr(adr)
        return adr

    def save_adr(self, adr: ArchitectureDecision):
        """Saves an ADR to a file."""
        # Sanitize title for safe filenames
        safe_title = adr.title.replace(" ", "_").replace("/", "_").replace("\\", "_")
        safe_title = "".join(ch for ch in safe_title if ch.isalnum() or ch in ("_", "-", "."))
        filename = f"adr_{adr.timestamp.replace(':', '-')}_{safe_title.lower()}.json"
        filepath = os.path.join(self.output_directory, filename)

        with open(filepath, "w") as f:
            json.dump(adr.__dict__, f, indent=4)

    def save_intermediate_decisions(self, decisions: list[dict[str, Any]], run_id: str):
        """Saves intermediate decisions to a file."""
        filename = f"intermediate_decisions_{run_id}.json"
        filepath = os.path.join(self.output_directory, filename)

        with open(filepath, "w") as f:
            json.dump(decisions, f, indent=4)

    def load_intermediate_decisions(self, run_id: str) -> list[dict[str, Any]]:
        """Loads intermediate decisions from a file."""
        filename = f"intermediate_decisions_{run_id}.json"
        filepath = os.path.join(self.output_directory, filename)

        if os.path.exists(filepath):
            with open(filepath) as f:
                return json.load(f)
        return []
