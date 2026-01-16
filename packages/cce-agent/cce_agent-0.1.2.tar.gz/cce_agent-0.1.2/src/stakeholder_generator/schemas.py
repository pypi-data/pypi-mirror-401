"""
Pydantic Schemas for Structured LLM Outputs
"""

from pydantic import BaseModel, Field


class ArchitectureView(BaseModel):
    """Defines a single architectural view."""

    view_name: str = Field(description="The name of the architecture view (e.g., 'Functional View').")
    view_components: list[str] = Field(description="A list of key components or elements within this view.")
    model_kinds: list[str] = Field(
        description="A list of model kinds used to represent this view (e.g., 'Use Case Diagram')."
    )


class ArchitectureConsideration(BaseModel):
    """An alternative or factor that was considered but not chosen."""

    consideration: str = Field(description="A brief description of the consideration.")
    details: str = Field(description="Details about why this consideration was explored and ultimately not selected.")


class ArchitectureDecision(BaseModel):
    """A significant architectural decision that was made."""

    decision: str = Field(description="The architectural decision.")
    rationale: str = Field(description="The reasoning and trade-offs behind the decision.")
    consequences: str = Field(description="The impact and outcomes of this decision.")


class SynthesisResult(BaseModel):
    """The structured output from the synthesis engine."""

    introduction: str = Field(description="A brief, high-level overview of the proposed architecture.")
    architecture_views: list[ArchitectureView] = Field(description="A list of the key architecture views.")
    decisions: list[ArchitectureDecision] = Field(description="A list of the significant architectural decisions made.")
    architecture_considerations: list[ArchitectureConsideration] = Field(
        default=[], description="A list of important considerations that were explored."
    )


class QualityAssessment(BaseModel):
    """The structured output from quality assessment evaluation."""

    implementation_readiness: float = Field(description="Score for implementation readiness (0.0-1.0)", ge=0.0, le=1.0)
    ticket_coverage: float = Field(description="Score for ticket coverage (0.0-1.0)", ge=0.0, le=1.0)
    stakeholder_balance: float = Field(description="Score for stakeholder balance (0.0-1.0)", ge=0.0, le=1.0)
    technical_feasibility: float = Field(description="Score for technical feasibility (0.0-1.0)", ge=0.0, le=1.0)
    clarity_completeness: float = Field(description="Score for clarity and completeness (0.0-1.0)", ge=0.0, le=1.0)
    overall_score: float = Field(description="Overall weighted score (0.0-1.0)", ge=0.0, le=1.0)
    details: str = Field(description="Detailed analysis and feedback")
    recommendations: list[str] = Field(description="List of specific improvement recommendations")
    pass_threshold: bool = Field(description="Whether the assessment passes the quality threshold")


class StakeholderAnalysis(BaseModel):
    """The structured output from a stakeholder agent's analysis."""

    perspective: str = Field(description="A brief, one-sentence summary of the stakeholder's primary viewpoint.")
    aspects: list[str] = Field(
        description="A list of the key aspects of the system this stakeholder is concerned with."
    )
    analysis: str = Field(
        default="",
        description="The full, detailed analysis, including concerns, recommendations, risks, and success criteria.",
    )
