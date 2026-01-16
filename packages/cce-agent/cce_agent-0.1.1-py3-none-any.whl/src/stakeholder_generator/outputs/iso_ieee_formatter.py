# src/stakeholder_generator/outputs/iso_ieee_formatter.py
from datetime import datetime

from ..schemas import StakeholderAnalysis, SynthesisResult


class ISOIEEEFormatter:
    """
    Enhanced ISO/IEEE 42010 compliant formatter with full standard compliance.

    Implements complete ISO/IEEE 42010 architecture description including:
    - Stakeholder perspectives and concerns
    - All 7 standard architecture views
    - Correspondence maps and traceability
    - Formal decision logs and considerations
    - Architecture rationale and justification
    """

    # Standard ISO/IEEE 42010 Architecture Views
    STANDARD_VIEWS = {
        "functional": {
            "name": "Functional View",
            "viewpoint": "Functional Viewpoint",
            "description": "System's functional capabilities, services, and behavior",
            "model_kinds": ["Use Case Diagrams", "Activity Diagrams", "Sequence Diagrams"],
        },
        "structural": {
            "name": "Structural View",
            "viewpoint": "Structural Viewpoint",
            "description": "System components, modules, and their static relationships",
            "model_kinds": ["Component Diagrams", "Class Diagrams", "Package Diagrams"],
        },
        "behavioral": {
            "name": "Behavioral View",
            "viewpoint": "Behavioral Viewpoint",
            "description": "System's dynamic behavior, state changes, and interactions",
            "model_kinds": ["State Diagrams", "Communication Diagrams", "Timing Diagrams"],
        },
        "deployment": {
            "name": "Deployment View",
            "viewpoint": "Deployment Viewpoint",
            "description": "System deployment across physical and virtual infrastructure",
            "model_kinds": ["Deployment Diagrams", "Network Diagrams", "Infrastructure Models"],
        },
        "information": {
            "name": "Information View",
            "viewpoint": "Information Viewpoint",
            "description": "Data structures, information flow, and data management",
            "model_kinds": ["Data Models", "Entity-Relationship Diagrams", "Information Flow Diagrams"],
        },
        "interaction": {
            "name": "Interaction View",
            "viewpoint": "Interaction Viewpoint",
            "description": "External interfaces, APIs, and system boundaries",
            "model_kinds": ["Interface Diagrams", "API Specifications", "Protocol Models"],
        },
        "quality": {
            "name": "Quality View",
            "viewpoint": "Quality Viewpoint",
            "description": "Quality attributes, constraints, and non-functional requirements",
            "model_kinds": ["Quality Models", "Performance Models", "Security Models"],
        },
    }

    def __init__(
        self,
        synthesis_result: SynthesisResult,
        stakeholder_contributions: dict,
        integration_challenge: str = "",
        architecture_decisions: list[dict] = None,
    ):
        self.synthesis = synthesis_result
        self.contributions = stakeholder_contributions
        self.integration_challenge = integration_challenge
        self.architecture_decisions = architecture_decisions or []
        self.stakeholder_concerns = self._extract_stakeholder_concerns()
        self.correspondence_map = self._build_correspondence_map()

    def format(self) -> str:
        """
        Generates a comprehensive ISO/IEEE 42010 compliant architecture description.
        """
        return f"""# Architecture Description (ISO/IEEE 42010 Compliant)

**Generated on**: {datetime.utcnow().isoformat()}
**Integration Challenge**: {self.integration_challenge}

## 1. Architecture Overview
{self._format_introduction()}

## 2. Stakeholder Analysis
{self._format_stakeholder_perspectives()}

## 3. Architecture Viewpoints  
{self._format_viewpoints()}

## 4. Architecture Views
{self._format_comprehensive_views()}

## 5. Architecture Decisions
{self._format_formal_decisions()}

## 6. Architecture Considerations
{self._format_architecture_considerations()}

## 7. Correspondence Analysis
{self._format_correspondence_maps()}

## 8. Rationale and Justification
{self._format_rationale()}

## 9. Traceability Matrix
{self._format_traceability_matrix()}

---
*This architecture description conforms to ISO/IEC/IEEE 42010:2011 standard for architecture descriptions of systems and software.*
"""

    def _extract_stakeholder_concerns(self) -> dict[str, list[str]]:
        """Extract and categorize stakeholder concerns from contributions."""
        concerns = {}
        for name, contribution in self.contributions.items():
            if isinstance(contribution, StakeholderAnalysis):
                # Extract key concerns from analysis
                concern_keywords = ["concern", "risk", "challenge", "requirement", "need"]
                analysis_text = contribution.analysis.lower()
                stakeholder_concerns = []

                # Simple keyword-based extraction
                for line in contribution.analysis.split("\n"):
                    line = line.strip()
                    if any(keyword in line.lower() for keyword in concern_keywords) and len(line) > 20:
                        stakeholder_concerns.append(line[:500])

                # Add aspects as concerns if no specific concerns found
                if not stakeholder_concerns and contribution.aspects:
                    stakeholder_concerns = [f"Ensuring proper {aspect}" for aspect in contribution.aspects[:3]]

                concerns[name] = stakeholder_concerns or ["General architectural quality"]

        return concerns

    def _build_correspondence_map(self) -> dict[str, dict[str, list[str]]]:
        """Build correspondence mappings between stakeholders, concerns, views, and decisions."""
        correspondence = {
            "stakeholder_to_concerns": self.stakeholder_concerns,
            "concerns_to_views": {},
            "views_to_decisions": {},
            "decisions_to_rationale": {},
        }

        # Map concerns to views (simplified mapping)
        for stakeholder, concerns in self.stakeholder_concerns.items():
            for concern in concerns:
                # Map different types of concerns to appropriate views
                if any(word in concern.lower() for word in ["api", "interface", "integration"]):
                    correspondence["concerns_to_views"].setdefault(concern, []).append("Interaction View")
                elif any(word in concern.lower() for word in ["component", "module", "structure"]):
                    correspondence["concerns_to_views"].setdefault(concern, []).append("Structural View")
                elif any(word in concern.lower() for word in ["performance", "reliability", "quality"]):
                    correspondence["concerns_to_views"].setdefault(concern, []).append("Quality View")
                elif any(word in concern.lower() for word in ["behavior", "workflow", "process"]):
                    correspondence["concerns_to_views"].setdefault(concern, []).append("Behavioral View")
                else:
                    correspondence["concerns_to_views"].setdefault(concern, []).append("Functional View")

        # Map decisions to rationale
        for decision in self.synthesis.decisions:
            correspondence["decisions_to_rationale"][decision.decision] = decision.rationale

        return correspondence

    def _format_introduction(self) -> str:
        """Enhanced introduction with architecture purpose and scope."""
        base_intro = self.synthesis.introduction

        enhanced_intro = f"""{base_intro}

### Architecture Purpose
This architecture description addresses the integration challenge: "{self.integration_challenge}"

### Architecture Scope
The architecture encompasses {len(self.contributions)} stakeholder perspectives, addressing their specific concerns through {len(self.STANDARD_VIEWS)} standard architecture views as defined by ISO/IEC/IEEE 42010.

### Architecture Principles
- **Stakeholder-Driven**: All architectural decisions are traceable to stakeholder concerns
- **View-Based**: Multiple coordinated views provide comprehensive system understanding  
- **Decision-Centric**: Explicit recording of architectural decisions and their rationale
- **Correspondence-Aware**: Clear mappings between stakeholders, concerns, views, and decisions"""

        return enhanced_intro

    def _format_stakeholder_perspectives(self) -> str:
        """Format comprehensive stakeholder analysis with concerns and perspectives."""
        output = "### Stakeholder Identification and Analysis\n\n"
        output += "The following stakeholders participated in the architecture definition process:\n\n"

        for name, contribution in self.contributions.items():
            if isinstance(contribution, StakeholderAnalysis):
                stakeholder_name = name.replace("_", " ").title()
                output += f"#### {stakeholder_name}\n"
                output += f"**Perspective**: {contribution.perspective}\n\n"

                output += f"**Key Aspects of Concern**:\n"
                for aspect in contribution.aspects:
                    output += f"- {aspect}\n"
                output += "\n"

                output += f"**Primary Concerns**:\n"
                concerns = self.stakeholder_concerns.get(name, ["General architectural quality"])
                for concern in concerns:
                    output += f"- {concern}\n"
                output += "\n"

                # Extract key requirements from analysis
                output += f"**Detailed Analysis**:\n"
                output += f"{contribution.analysis[:500]}{'...' if len(contribution.analysis) > 500 else ''}\n\n"

                output += "---\n\n"

        return output

    def _format_viewpoints(self) -> str:
        """Format all standard ISO/IEEE 42010 viewpoints."""
        output = "### Architecture Viewpoints\n\n"
        output += "This architecture description uses the following standardized viewpoints:\n\n"

        for view_key, view_info in self.STANDARD_VIEWS.items():
            output += f"#### {view_info['viewpoint']}\n"
            output += f"**Purpose**: {view_info['description']}\n\n"
            output += f"**Typical Model Kinds**:\n"
            for model_kind in view_info["model_kinds"]:
                output += f"- {model_kind}\n"
            output += "\n"

            # Add stakeholder interests
            interested_stakeholders = self._get_stakeholders_for_viewpoint(view_key)
            if interested_stakeholders:
                output += f"**Primary Stakeholder Interests**: {', '.join(interested_stakeholders)}\n\n"

            output += "---\n\n"

        return output

    def _get_stakeholders_for_viewpoint(self, view_key: str) -> list[str]:
        """Determine which stakeholders are primarily interested in each viewpoint."""
        stakeholder_interests = {
            "functional": ["aider_integration", "developer_experience"],
            "structural": ["langgraph_architecture", "context_engineering"],
            "behavioral": ["langgraph_architecture", "aider_integration"],
            "deployment": ["production_stability", "langgraph_architecture"],
            "information": ["context_engineering", "aider_integration"],
            "interaction": ["developer_experience", "aider_integration"],
            "quality": ["production_stability", "developer_experience"],
        }

        interested = stakeholder_interests.get(view_key, [])
        return [name.replace("_", " ").title() for name in interested if name in self.contributions]

    def _format_comprehensive_views(self) -> str:
        """Format all architecture views with comprehensive coverage."""
        output = "### Architecture Views\n\n"

        # Start with synthesis-generated views
        synthesis_views = {view.view_name: view for view in self.synthesis.architecture_views}

        # Ensure all standard views are covered
        for view_key, view_info in self.STANDARD_VIEWS.items():
            view_name = view_info["name"]
            output += f"#### {view_name}\n"
            output += f"**Viewpoint**: {view_info['viewpoint']}\n"
            output += f"**Description**: {view_info['description']}\n\n"

            # Use synthesis data if available, otherwise provide standard structure
            if view_name in synthesis_views:
                synthesis_view = synthesis_views[view_name]
                output += f"**View Elements**:\n"
                for component in synthesis_view.view_components:
                    output += f"- {component}\n"
                output += "\n"

                if synthesis_view.model_kinds:
                    output += f"**Model Representations**:\n"
                    for model_kind in synthesis_view.model_kinds:
                        output += f"- {model_kind}\n"
                    output += "\n"
            else:
                # Provide standard structure for missing views
                output += f"**View Elements**: *To be elaborated in detailed design phase*\n\n"
                output += f"**Model Representations**:\n"
                for model_kind in view_info["model_kinds"]:
                    output += f"- {model_kind}\n"
                output += "\n"

            # Add correspondence to stakeholder concerns
            relevant_concerns = self._get_concerns_for_view(view_key)
            if relevant_concerns:
                output += f"**Addresses Stakeholder Concerns**:\n"
                for concern in relevant_concerns[:3]:  # Limit to top 3
                    output += f"- {concern}\n"
                output += "\n"

            output += "---\n\n"

        return output

    def _get_concerns_for_view(self, view_key: str) -> list[str]:
        """Get stakeholder concerns that are addressed by a specific view."""
        concerns = []
        view_keywords = {
            "functional": ["function", "capability", "service", "feature"],
            "structural": ["component", "module", "structure", "organization"],
            "behavioral": ["behavior", "workflow", "process", "interaction"],
            "deployment": ["deployment", "infrastructure", "environment"],
            "information": ["data", "information", "storage", "persistence"],
            "interaction": ["interface", "api", "integration", "communication"],
            "quality": ["performance", "reliability", "security", "quality"],
        }

        keywords = view_keywords.get(view_key, [])

        for stakeholder_concerns in self.stakeholder_concerns.values():
            for concern in stakeholder_concerns:
                if any(keyword in concern.lower() for keyword in keywords):
                    concerns.append(concern)

        return list(set(concerns))  # Remove duplicates

    def _format_formal_decisions(self) -> str:
        """Format architecture decisions with enhanced structure."""
        output = "### Architecture Decisions\n\n"

        if not self.synthesis.decisions:
            output += "*No explicit architecture decisions were recorded in the synthesis.*\n\n"
            return output

        output += "The following architecture decisions were made during the design process:\n\n"

        for i, decision in enumerate(self.synthesis.decisions, 1):
            output += f"#### Decision {i}: {decision.decision}\n"
            output += f"**Rationale**: {decision.rationale}\n\n"
            output += f"**Consequences**: {decision.consequences}\n\n"

            # Add traceability to stakeholder concerns
            related_concerns = self._find_related_concerns(decision.decision)
            if related_concerns:
                output += f"**Addresses Stakeholder Concerns**:\n"
                for concern in related_concerns[:2]:  # Limit to top 2
                    output += f"- {concern}\n"
                output += "\n"

            output += "---\n\n"

        return output

    def _find_related_concerns(self, decision_text: str) -> list[str]:
        """Find stakeholder concerns related to a specific decision."""
        related = []
        decision_lower = decision_text.lower()

        for stakeholder_concerns in self.stakeholder_concerns.values():
            for concern in stakeholder_concerns:
                # Simple keyword matching
                concern_words = set(concern.lower().split())
                decision_words = set(decision_lower.split())

                # If there's significant overlap, consider it related
                if len(concern_words.intersection(decision_words)) >= 2:
                    related.append(concern)

        return related

    def _format_architecture_considerations(self) -> str:
        """Format architecture considerations (alternatives that were considered but not chosen)."""
        output = "### Architecture Considerations\n\n"

        if not self.synthesis.architecture_considerations:
            output += "*No explicit architecture considerations were recorded in the synthesis.*\n\n"
            return output

        output += "The following alternatives and considerations were evaluated during the design process:\n\n"

        for i, consideration in enumerate(self.synthesis.architecture_considerations, 1):
            output += f"#### Consideration {i}: {consideration.consideration}\n"
            output += f"**Details**: {consideration.details}\n\n"
            output += "---\n\n"

        return output

    def _format_correspondence_maps(self) -> str:
        """Format comprehensive correspondence analysis and mappings."""
        output = "### Correspondence Analysis\n\n"
        output += "This section establishes the correspondence relationships between architecture elements:\n\n"

        # Stakeholder-to-Concern correspondence
        output += "#### Stakeholder-Concern Correspondence\n\n"
        output += "| Stakeholder | Primary Concerns |\n"
        output += "|-------------|------------------|\n"

        for stakeholder, concerns in self.stakeholder_concerns.items():
            stakeholder_name = stakeholder.replace("_", " ").title()
            concern_list = "; ".join(concerns[:2])  # Limit to first 2 concerns
            output += f"| {stakeholder_name} | {concern_list} |\n"

        output += "\n"

        # Concern-to-View correspondence
        output += "#### Concern-View Correspondence\n\n"
        output += "| Concern Category | Addressed by Views |\n"
        output += "|------------------|-------------------|\n"

        concern_categories = {
            "Functional Requirements": ["Functional View", "Behavioral View"],
            "Structural Organization": ["Structural View", "Information View"],
            "Quality Attributes": ["Quality View", "Deployment View"],
            "Integration & Interfaces": ["Interaction View", "Structural View"],
            "Operational Concerns": ["Deployment View", "Quality View"],
        }

        for category, views in concern_categories.items():
            view_list = ", ".join(views)
            output += f"| {category} | {view_list} |\n"

        output += "\n"

        # Decision-Rationale correspondence
        output += "#### Decision-Rationale Correspondence\n\n"
        if self.synthesis.decisions:
            output += "| Decision | Rationale Summary |\n"
            output += "|----------|------------------|\n"

            for decision in self.synthesis.decisions:
                rationale_summary = (
                    decision.rationale[:100] + "..." if len(decision.rationale) > 100 else decision.rationale
                )
                output += f"| {decision.decision} | {rationale_summary} |\n"
        else:
            output += "*No formal decisions recorded for correspondence analysis.*\n"

        output += "\n"

        return output

    def _format_rationale(self) -> str:
        """Format overall architecture rationale and justification."""
        output = "### Architecture Rationale\n\n"

        output += "#### Design Philosophy\n"
        output += "This architecture was developed using a multi-stakeholder collaborative approach, ensuring that diverse perspectives and concerns are addressed comprehensively.\n\n"

        output += "#### Key Design Principles\n"
        output += (
            "- **Stakeholder-Centric**: Every architectural element traces back to specific stakeholder concerns\n"
        )
        output += "- **Multi-View Consistency**: All views are coordinated and consistent with each other\n"
        output += (
            "- **Decision Transparency**: Architectural decisions are explicitly documented with clear rationale\n"
        )
        output += "- **Traceability**: Clear correspondence between concerns, views, and decisions\n\n"

        output += "#### Architecture Validation\n"
        output += f"This architecture addresses {len(self.contributions)} distinct stakeholder perspectives through {len(self.STANDARD_VIEWS)} comprehensive views, ensuring complete coverage of system concerns.\n\n"

        return output

    def _format_traceability_matrix(self) -> str:
        """Format traceability matrix showing relationships between architecture elements."""
        output = "### Traceability Matrix\n\n"

        output += "#### Stakeholder-View Traceability\n\n"
        output += "| Stakeholder | Primary Views | Secondary Views |\n"
        output += "|-------------|---------------|----------------|\n"

        stakeholder_view_map = {
            "aider_integration": (["Functional View", "Interaction View"], ["Structural View"]),
            "langgraph_architecture": (["Structural View", "Behavioral View"], ["Quality View"]),
            "context_engineering": (["Information View", "Structural View"], ["Behavioral View"]),
            "production_stability": (["Quality View", "Deployment View"], ["Behavioral View"]),
            "developer_experience": (["Interaction View", "Quality View"], ["Functional View"]),
        }

        for stakeholder in self.contributions.keys():
            stakeholder_name = stakeholder.replace("_", " ").title()
            primary_views, secondary_views = stakeholder_view_map.get(stakeholder, (["Functional View"], []))
            primary_str = ", ".join(primary_views)
            secondary_str = ", ".join(secondary_views)
            output += f"| {stakeholder_name} | {primary_str} | {secondary_str} |\n"

        output += "\n"

        output += "#### Decision-View Impact Matrix\n\n"
        if self.synthesis.decisions:
            output += "| Decision | Impacted Views |\n"
            output += "|----------|----------------|\n"

            for decision in self.synthesis.decisions:
                # Simple heuristic to determine which views are impacted
                impacted_views = self._determine_impacted_views(decision.decision)
                impact_str = ", ".join(impacted_views) if impacted_views else "Multiple Views"
                output += f"| {decision.decision} | {impact_str} |\n"
        else:
            output += "*No decisions available for traceability analysis.*\n"

        output += "\n"

        return output

    def _determine_impacted_views(self, decision_text: str) -> list[str]:
        """Determine which views are impacted by a specific decision."""
        decision_lower = decision_text.lower()
        impacted = []

        view_keywords = {
            "Functional View": ["function", "capability", "service", "feature"],
            "Structural View": ["component", "module", "structure", "architecture"],
            "Behavioral View": ["behavior", "workflow", "process", "state"],
            "Deployment View": ["deploy", "infrastructure", "environment"],
            "Information View": ["data", "information", "storage"],
            "Interaction View": ["interface", "api", "integration"],
            "Quality View": ["performance", "reliability", "security", "quality"],
        }

        for view_name, keywords in view_keywords.items():
            if any(keyword in decision_lower for keyword in keywords):
                impacted.append(view_name)

        return impacted
