"""
Plan Generation System

This module provides intelligent, dynamic plan generation capabilities
to replace hardcoded topic-specific logic in the create_plan command.

Key Components:
- TopicAnalysisGraph: LangGraph-based intelligent topic analysis
- PlanPhaseGenerator: Dynamic phase generation based on topic analysis
- PlanTemplateLibrary: Reusable templates for common scenarios
- Validation: Plan coherence and quality checking
"""

from .phase_generator import PlanPhaseGenerator
from .plan_templates import PlanTemplateLibrary
from .topic_analyzer import PlanTopicAnalysis, TopicAnalysisGraph
from .validation import PlanValidator

__all__ = ["TopicAnalysisGraph", "PlanTopicAnalysis", "PlanPhaseGenerator", "PlanTemplateLibrary", "PlanValidator"]
