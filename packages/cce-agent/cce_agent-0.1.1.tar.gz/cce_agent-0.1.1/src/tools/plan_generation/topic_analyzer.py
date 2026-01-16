"""
Topic Analysis and Classification System

This module provides intelligent topic analysis using LangGraph to replace
hardcoded topic-specific logic in create_plan command.
"""

import logging
from dataclasses import dataclass
from typing import Any

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import TypedDict

# from langchain_core.output_parsers import PydanticOutputParser  # Replaced with with_structured_output

logger = logging.getLogger(__name__)


class TopicAnalysisOutput(BaseModel):
    """Structured output for topic analysis."""

    model_config = ConfigDict(strict=True, extra="forbid")

    domain_type: str = Field(description="Type of domain: feature, bugfix, refactor, infrastructure, performance")
    complexity_level: str = Field(description="Complexity level: simple, moderate, complex, enterprise")
    architectural_scope: list[str] = Field(description="List of architectural layers affected")
    technology_stack: list[str] = Field(description="List of relevant technologies")
    estimated_effort: str = Field(description="Estimated effort: small, medium, large, epic")
    risk_level: str = Field(description="Risk level: low, medium, high, critical")


class PhaseDefinition(BaseModel):
    """Structured output for a single implementation phase."""

    model_config = ConfigDict(strict=True, extra="forbid")

    phase_number: int = Field(description="Phase number")
    phase_name: str = Field(description="Phase name")
    description: str = Field(description="Detailed phase description")
    tasks: list[str] = Field(description="Phase tasks")
    deliverables: list[str] = Field(description="Phase deliverables")
    acceptance_criteria: list[str] = Field(description="Phase acceptance criteria")


class PhaseStructureOutput(BaseModel):
    """Structured output for phase structure generation."""

    model_config = ConfigDict(strict=True, extra="forbid")

    phases: list[PhaseDefinition] = Field(description="List of implementation phases")
    dependencies: list[str] = Field(description="List of dependencies between phases")
    risks: list[str] = Field(description="List of identified risks")
    estimated_duration: str = Field(description="Estimated total duration")
    success_criteria: list[str] = Field(description="List of success criteria")
    context_summary: list[str] = Field(
        description="3-5 bullet summary of key research findings and context", default=[]
    )


@dataclass
class PlanTopicAnalysis:
    """Structured analysis of a plan topic."""

    topic: str
    domain_type: str  # "feature", "bugfix", "refactor", "infrastructure", "performance"
    complexity_level: str  # "simple", "moderate", "complex", "enterprise"
    architectural_scope: list[str]  # ["frontend", "backend", "database", "api", "testing"]
    technology_stack: list[str]  # ["python", "javascript", "database", "ai_ml", "devops"]
    estimated_effort: str  # "small", "medium", "large", "epic"
    risk_level: str  # "low", "medium", "high", "critical"
    stakeholders_needed: list[str]  # ["architect", "frontend_dev", "qa", "pm", "devops"]


class TopicAnalysisState(TypedDict):
    """State for the topic analysis workflow."""

    plan_topic: str
    context: str
    semantic_analysis: str
    topic_analysis: PlanTopicAnalysis | None
    phase_structure: dict[str, Any] | None
    validation_results: dict[str, Any] | None
    error_message: str | None
    retry_count: int
    llm_available: bool


class TopicAnalysisGraph:
    """LangGraph-based intelligent topic analysis system."""

    def __init__(self, llm=None, config: dict[str, Any] | None = None):
        """Initialize the topic analysis graph."""
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.TopicAnalysisGraph")

        # Initialize LLM with fallback strategies
        self.llm = llm or self._create_llm_with_fallbacks()

        # Create the workflow graph
        self.graph = self._create_workflow()

    def _create_llm_with_fallbacks(self):
        """Create LLM with fallback strategies using LangGraph patterns."""
        self.logger.info("🔧 Initializing LLM with fallback strategies...")

        # Try primary LLM first
        primary_llm = self._create_primary_llm()
        if primary_llm:
            self.logger.info("✅ Primary LLM initialized successfully")
            return primary_llm

        # Try fallback LLM
        self.logger.warning("⚠️ Primary LLM failed, trying fallback LLM...")
        fallback_llm = self._create_fallback_llm()
        if fallback_llm:
            self.logger.info("✅ Fallback LLM initialized successfully")
            return fallback_llm

        # All LLMs failed
        self.logger.error("❌ All LLM initialization attempts failed")
        return None

    def _create_primary_llm(self):
        """Create primary LLM configuration."""
        try:
            from langchain_openai import ChatOpenAI

            # Get configuration from config or use defaults
            model = self.config.get("primary_model", "gpt-4o")
            temperature = self.config.get("temperature", 0.1)
            max_tokens = self.config.get("max_tokens", 4096)
            timeout = self.config.get("timeout", 30)

            llm = ChatOpenAI(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                request_timeout=timeout,
                model_kwargs={"response_format": {"type": "json_object"}},
            )

            self.logger.info(f"✅ Primary LLM created: {model}")
            return llm

        except ImportError as e:
            self.logger.error(f"❌ LangChain OpenAI import failed: {e}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Primary LLM creation failed: {e}")
            return None

    def _create_fallback_llm(self):
        """Create fallback LLM configuration."""
        try:
            from langchain_openai import ChatOpenAI

            # Use simpler, more reliable model for fallback
            fallback_model = self.config.get("fallback_model", "gpt-3.5-turbo")
            temperature = self.config.get("temperature", 0.1)
            max_tokens = self.config.get("fallback_max_tokens", 2048)
            timeout = self.config.get("fallback_timeout", 60)

            llm = ChatOpenAI(
                model=fallback_model,
                temperature=temperature,
                max_tokens=max_tokens,
                request_timeout=timeout,
                # Don't force JSON for fallback to avoid compatibility issues
            )

            self.logger.info(f"✅ Fallback LLM created: {fallback_model}")
            return llm

        except ImportError as e:
            self.logger.error(f"❌ LangChain OpenAI import failed for fallback: {e}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Fallback LLM creation failed: {e}")
            return None

    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow for topic analysis with error handling."""
        workflow = StateGraph(TopicAnalysisState)

        # Add nodes
        workflow.add_node("analyze_topic_domain", self._analyze_topic_domain)
        workflow.add_node("retry_analysis", self._retry_analysis)
        workflow.add_node("fallback_analysis", self._fallback_analysis)
        workflow.add_node("assess_complexity", self._assess_complexity_and_scope)
        workflow.add_node("identify_stakeholders", self._identify_required_stakeholders)
        workflow.add_node("generate_phase_structure", self._generate_intelligent_phases)
        workflow.add_node("validate_plan_logic", self._validate_plan_logic)

        # Define workflow edges with error handling
        workflow.add_edge(START, "analyze_topic_domain")

        # Conditional edges for error handling and retry logic
        workflow.add_conditional_edges(
            "analyze_topic_domain",
            self._decide_analysis_path,
            {"success": "assess_complexity", "retry": "retry_analysis", "fallback": "fallback_analysis"},
        )

        workflow.add_conditional_edges(
            "retry_analysis", self._decide_retry_path, {"success": "assess_complexity", "fallback": "fallback_analysis"}
        )

        workflow.add_edge("fallback_analysis", "assess_complexity")
        workflow.add_edge("assess_complexity", "identify_stakeholders")
        workflow.add_edge("identify_stakeholders", "generate_phase_structure")
        workflow.add_edge("generate_phase_structure", "validate_plan_logic")
        workflow.add_edge("validate_plan_logic", END)

        return workflow.compile()

    def _decide_analysis_path(self, state: TopicAnalysisState) -> str:
        """Decide the next path based on analysis success/failure."""
        if state.get("error_message"):
            retry_count = state.get("retry_count", 0)
            if retry_count < 2:  # Max 2 retries
                return "retry"
            else:
                return "fallback"
        return "success"

    def _decide_retry_path(self, state: TopicAnalysisState) -> str:
        """Decide the next path after retry attempt."""
        if state.get("error_message"):
            return "fallback"
        return "success"

    async def _retry_analysis(self, state: TopicAnalysisState) -> TopicAnalysisState:
        """Retry analysis with exponential backoff using LangGraph patterns."""
        retry_count = state.get("retry_count", 0) + 1
        self.logger.info(f"🔄 Retrying analysis (attempt {retry_count})")

        # Update retry count
        state["retry_count"] = retry_count
        state["error_message"] = None

        # Add exponential backoff delay
        import asyncio

        delay = min(2**retry_count, 10)  # Max 10 seconds
        await asyncio.sleep(delay)

        # Retry the analysis
        try:
            return await self._analyze_topic_domain(state)
        except Exception as e:
            self.logger.warning(f"⚠️ Retry attempt {retry_count} failed: {e}")
            state["error_message"] = str(e)
            return state

    async def _fallback_analysis(self, state: TopicAnalysisState) -> TopicAnalysisState:
        """Fallback analysis when LLM is unavailable."""
        self.logger.info("🔍 Using intelligent fallback analysis")

        plan_topic = state["plan_topic"]
        context = state["context"]

        # Use intelligent fallback analysis
        topic_analysis = self._intelligent_fallback_analysis(plan_topic, context)
        state["topic_analysis"] = topic_analysis
        state["llm_available"] = False
        state["error_message"] = None

        return state

    async def analyze_and_structure_plan(
        self, plan_topic: str, context: str, semantic_analysis: str, discovered_files: list[str] | None = None
    ) -> dict[str, Any]:
        """Execute intelligent topic analysis and return structured plan."""
        self.logger.info(
            f"🚀 Starting intelligent plan analysis for: '{plan_topic}' with context length: {len(context)}"
        )
        self.logger.info(f"🔍 Context length: {len(context)} chars")
        self.logger.info(f"🔍 Semantic analysis length: {len(semantic_analysis)} chars")
        self.logger.info(f"🔍 LLM available: {self.llm is not None}")
        self.logger.info(f"🔍 Graph available: {self.graph is not None}")

        try:
            # Add discovered files to context if provided
            enhanced_context = context
            if discovered_files:
                files_context = f"\n\n## Discovered Files for Implementation:\n"
                for i, file_path in enumerate(discovered_files, 1):
                    files_context += f"{i}. `{file_path}`\n"
                files_context += "\nUse these files intelligently throughout the phases where relevant."
                enhanced_context = context + files_context

            state = {
                "plan_topic": plan_topic,
                "context": enhanced_context,
                "semantic_analysis": semantic_analysis,
                "topic_analysis": None,
                "phase_structure": None,
                "validation_results": None,
                "error_message": None,
                "retry_count": 0,
                "llm_available": self.llm is not None,
            }

            self.logger.info(f"🔍 Invoking LangGraph workflow...")
            self.logger.info(f"🔍 State keys: {list(state.keys())}")
            self.logger.info(f"🔍 State values types: {[(k, type(v)) for k, v in state.items()]}")

            try:
                result = await self.graph.ainvoke(state)
                self.logger.info(f"🔍 LangGraph workflow completed successfully")
                self.logger.info(f"🔍 Result type: {type(result)}")
                self.logger.info(f"🔍 Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                self.logger.info(f"🔍 Result value: {result}")
            except Exception as e:
                self.logger.error(f"🔍 [DEBUG] LangGraph workflow failed with exception")
                self.logger.error(f"🔍 [DEBUG] Exception type: {type(e)}")
                self.logger.error(f"🔍 [DEBUG] Exception value: {e}")
                self.logger.error(f"🔍 [DEBUG] Exception str: {str(e)}")
                import traceback

                self.logger.error(f"🔍 [DEBUG] Exception traceback: {traceback.format_exc()}")
                raise

            phase_structure = result.get("phase_structure", {})
            self.logger.info(f"🔍 Phase structure type: {type(phase_structure)}")
            self.logger.info(
                f"🔍 Phase structure keys: {list(phase_structure.keys()) if isinstance(phase_structure, dict) else 'Not a dict'}"
            )

            if isinstance(phase_structure, dict) and "phases" in phase_structure:
                self.logger.info(f"🔍 Number of phases: {len(phase_structure['phases'])}")
                if phase_structure["phases"]:
                    first_phase = phase_structure["phases"][0]
                    self.logger.info(f"🔍 First phase name: {first_phase.get('name', 'Unknown')}")

            self.logger.info(f"🔍 [DEBUG] About to return phase_structure")
            self.logger.info(f"🔍 [DEBUG] Return value type: {type(phase_structure)}")
            self.logger.info(f"🔍 [DEBUG] Return value: {phase_structure}")

            return phase_structure

        except Exception as e:
            self.logger.error(f"❌ Topic analysis failed: {e}")
            self.logger.error(f"❌ Error type: {type(e).__name__}")
            self.logger.error(f"🔍 [DEBUG] Exception value: {e}")
            self.logger.error(f"🔍 [DEBUG] Exception str: {str(e)}")
            import traceback

            self.logger.error(f"❌ Traceback: {traceback.format_exc()}")
            self.logger.warning("⚠️ Falling back to generic plan")
            fallback_plan = self._create_fallback_plan(plan_topic, context)
            self.logger.info(f"🔍 [DEBUG] Fallback plan type: {type(fallback_plan)}")
            self.logger.info(f"🔍 [DEBUG] Fallback plan value: {fallback_plan}")
            return fallback_plan

    async def _analyze_topic_domain(self, state: TopicAnalysisState) -> TopicAnalysisState:
        """Analyze topic to determine domain type and characteristics."""
        plan_topic = state["plan_topic"]
        context = state["context"]

        self.logger.info(f"🔍 Topic analysis - plan_topic: '{plan_topic}'")
        self.logger.info(f"🔍 Topic analysis - llm available: {self.llm is not None}")

        if not self.llm:
            self.logger.warning("⚠️ No LLM available for topic analysis, using fallback")
            state["error_message"] = "No LLM available"
            return state

        try:
            analysis_prompt = f"""
            You are a software architecture expert. Analyze this implementation topic and classify it.
            
            TOPIC: {plan_topic}
            
            DETAILED CONTEXT AND REQUIREMENTS:
            {context[:2000]}
            
            Based on the detailed context above, determine:
            1. Domain type: feature/bugfix/refactor/infrastructure/performance
            2. Complexity level: simple/moderate/complex/enterprise
            3. Architectural scope: which layers are affected (be specific based on the requirements)
            4. Technology stack: relevant technologies (be specific based on the context)
            5. Estimated effort: small/medium/large/epic
            6. Risk level: low/medium/high/critical
            
            IMPORTANT: Base your analysis on the specific requirements and context provided, not just the topic name.
            
            Return your analysis as a JSON object with the following structure:
            {{
                "domain_type": "feature|bugfix|refactor|infrastructure|performance",
                "complexity_level": "simple|moderate|complex|enterprise",
                "architectural_scope": ["layer1", "layer2", ...],
                "technology_stack": ["tech1", "tech2", ...],
                "estimated_effort": "small|medium|large|epic",
                "risk_level": "low|medium|high|critical"
            }}
            """

            # Use structured output with the LLM
            structured_llm = self.llm.with_structured_output(
                TopicAnalysisOutput, method="function_calling", strict=True
            )

            response = await structured_llm.ainvoke(analysis_prompt)
            # With structured output, response is the Pydantic object, not a response with .content
            if hasattr(response, "content"):
                self.logger.info(f"🔍 Topic analysis LLM response received: {len(response.content)} chars")
                self.logger.info(f"🔍 Topic analysis LLM response preview: {response.content[:200]}...")
                self.logger.info(f"🔍 FULL TOPIC ANALYSIS LLM RESPONSE:")
                self.logger.info(f"--- START TOPIC ANALYSIS RESPONSE ---")
                self.logger.info(response.content)
                self.logger.info(f"--- END TOPIC ANALYSIS RESPONSE ---")
            else:
                self.logger.info(f"🔍 Structured topic analysis response received: {type(response)}")
                self.logger.info(f"🔍 Response preview: {str(response)[:200]}...")

            # Parse using structured output
            try:
                parsed_output = response  # response is already a Pydantic object
                self.logger.info(f"✅ Successfully parsed structured topic analysis")
                self.logger.info(f"🔍 Domain type: {parsed_output.domain_type}")
                self.logger.info(f"🔍 Complexity: {parsed_output.complexity_level}")
                self.logger.info(f"🔍 Scope: {parsed_output.architectural_scope}")

                topic_analysis = PlanTopicAnalysis(
                    topic=plan_topic,
                    domain_type=parsed_output.domain_type,
                    complexity_level=parsed_output.complexity_level,
                    architectural_scope=parsed_output.architectural_scope,
                    technology_stack=parsed_output.technology_stack,
                    estimated_effort=parsed_output.estimated_effort,
                    risk_level=parsed_output.risk_level,
                    stakeholders_needed=["architect", "developer", "qa"],
                )

                self.logger.info(f"✅ Created PlanTopicAnalysis object")
                state["topic_analysis"] = topic_analysis

            except Exception as parse_error:
                self.logger.warning(f"⚠️ Structured parsing failed: {parse_error}")
                self.logger.warning("⚠️ Falling back to manual parsing")
                # With structured output, response is the Pydantic object, not a response with .content
                if hasattr(response, "content"):
                    topic_analysis = self._parse_topic_analysis(response.content, plan_topic)
                else:
                    # If response is already a Pydantic object, try to extract data
                    topic_analysis = self._parse_topic_analysis(str(response), plan_topic)
                state["topic_analysis"] = topic_analysis
            return state

        except Exception as e:
            self.logger.warning(f"LLM topic analysis failed: {e}")
            state["error_message"] = str(e)
            return state

    async def _assess_complexity_and_scope(self, state: TopicAnalysisState) -> TopicAnalysisState:
        """Assess complexity and architectural scope."""
        self.logger.info(f"🔍 Assessing complexity and scope...")
        self.logger.info(f"🔍 Topic analysis available: {state.get('topic_analysis') is not None}")
        # For now, pass through - complexity already assessed in domain analysis
        return state

    async def _identify_required_stakeholders(self, state: TopicAnalysisState) -> TopicAnalysisState:
        """Identify required stakeholders based on topic analysis."""
        self.logger.info(f"🔍 Identifying required stakeholders...")
        topic_analysis = state.get("topic_analysis")
        if not topic_analysis:
            self.logger.warning("⚠️ No topic analysis available for stakeholder identification")
            return state

        # Map domain types to stakeholders
        stakeholder_mapping = {
            "feature": ["architect", "pm", "developer", "qa"],
            "bugfix": ["developer", "qa", "pm"],
            "refactor": ["architect", "developer", "qa"],
            "infrastructure": ["architect", "devops", "qa"],
            "performance": ["architect", "developer", "qa"],
        }

        # Update stakeholders based on domain type
        base_stakeholders = stakeholder_mapping.get(topic_analysis.domain_type, ["architect", "developer", "qa"])
        topic_analysis.stakeholders_needed = base_stakeholders
        self.logger.info(f"🔍 Assigned stakeholders: {base_stakeholders}")

        return state

    async def _generate_intelligent_phases(self, state: TopicAnalysisState) -> TopicAnalysisState:
        """Generate implementation phases based on topic analysis."""
        topic_analysis = state.get("topic_analysis")
        semantic_analysis = state.get("semantic_analysis", "")

        self.logger.info(f"🔍 Phase generation - topic_analysis: {topic_analysis is not None}")
        self.logger.info(f"🔍 Phase generation - llm available: {self.llm is not None}")

        if topic_analysis:
            self.logger.info(f"🔍 Topic analysis details:")
            self.logger.info(f"   - Domain type: {topic_analysis.domain_type}")
            self.logger.info(f"   - Complexity: {topic_analysis.complexity_level}")
            self.logger.info(f"   - Scope: {topic_analysis.architectural_scope}")
            self.logger.info(f"   - Topic: {topic_analysis.topic}")

        if not topic_analysis:
            self.logger.warning("⚠️ No topic analysis available, using fallback")
            # Fallback phase generation
            phase_structure = self._create_fallback_plan(state["plan_topic"], state["context"])
            state["phase_structure"] = phase_structure
            return state

        try:
            if self.llm:
                phase_prompt = f"""
                You are a software architecture expert. Generate intelligent implementation phases for this topic.
                
                TOPIC: {topic_analysis.topic}
                
                TOPIC ANALYSIS: {topic_analysis}
                
                DETAILED CONTEXT AND REQUIREMENTS:
                {state.get("context", "")[:3000]}
                
                SEMANTIC CODEBASE ANALYSIS:
                {semantic_analysis[:1500]}
                
                INSTRUCTIONS:
                Create phases that are:
                1. SPECIFIC to this exact topic and requirements (not generic)
                2. Based on the detailed context and requirements provided above
                3. Appropriate for complexity level ({topic_analysis.complexity_level})
                4. Address the architectural scope ({topic_analysis.architectural_scope})
                5. Include specific tasks that directly implement the requirements
                6. Reference specific deliverables mentioned in the context
                7. Include realistic acceptance criteria based on the requirements
                8. **SUMMARIZE context in 3-5 bullets instead of embedding full research**
                
                Each phase should have: name, description, tasks, deliverables, acceptance_criteria
                
                CRITICAL: Make the phases SPECIFIC to the actual requirements in the context, not generic software development phases.
                - Avoid generic phases like "Research and Analysis", "Test Design", "Implementation"
                - Create phases that directly address the specific topic: {topic_analysis.topic}
                - Each phase should be actionable and specific to this exact topic
                - Phase names should reflect the specific work being done for this topic
                
                **CRITICAL: You MUST include a "context_summary" field in your JSON response with 3-5 bullet points summarizing the key research findings and context. Do NOT embed the full research text.**
                
                FILE INTERPOLATION GUIDANCE - CRITICAL REQUIREMENT:
                - **ABSOLUTELY MANDATORY**: Every phase description MUST start with specific file paths
                - **REQUIRED FORMAT**: "Modify src/tools/execution_config.py and src/agent.py to implement [specific changes]. This phase involves..."
                - **NEVER GENERIC**: NEVER write "Modify the core configuration files" - ALWAYS specify exact file paths
                - **DISTRIBUTION**: Phase 1 = core config files, Phase 2 = application logic files, Phase 3 = test files
                - **EXAMPLE REQUIRED**: "Modify src/tools/execution_config.py to add ExecutionMode enum with Demo/Guided/Expert values and update src/agent.py to integrate mode-aware behavior routing. This phase establishes..."
                - **FAILURE EXAMPLE**: "Modify the core configuration files to support the new run modes" (NO FILE PATHS = WRONG)
                - **SUCCESS EXAMPLE**: "Modify src/tools/execution_config.py to add ExecutionMode enum and src/config.py to support YAML configuration. This phase..."
                
                SUCCESS CRITERIA GUIDANCE:
                - Make success criteria SPECIFIC to this exact topic: {topic_analysis.topic}
                - Include measurable, actionable criteria that can be verified
                - Avoid generic criteria like "All tests pass" or "Documentation updated"
                - Focus on criteria that directly relate to the specific topic requirements
                
                Return your response as a JSON object with the following structure:
                {{
                    "phases": [
                        {{
                            "phase_number": 1,
                            "phase_name": "Phase Name",
                            "description": "Detailed description",
                            "tasks": ["task1", "task2", ...],
                            "deliverables": ["deliverable1", "deliverable2", ...],
                            "acceptance_criteria": ["criteria1", "criteria2", ...]
                        }}
                    ],
                    "dependencies": ["Phase 1 must complete before Phase 2", "Phase 2 depends on Phase 1"],
                    "risks": ["Risk 1: Description", "Risk 2: Description"],
                    "estimated_duration": "2-3 weeks",
                    "success_criteria": ["All phases completed", "All tests passing", "Documentation updated"],
                    "context_summary": ["Key finding 1", "Key finding 2", "Key finding 3"]
                }}
                
                **REMINDER: The context_summary field is REQUIRED and must contain 3-5 bullet points summarizing the key research findings and context.**
                """

                self.logger.info(f"🔍 Sending prompt to LLM (length: {len(phase_prompt)} chars)")
                self.logger.info(f"🔍 PROMPT PREVIEW:")
                self.logger.info(f"--- START PROMPT ---")
                prompt_preview = phase_prompt[:1000] + "..." if len(phase_prompt) > 1000 else phase_prompt
                self.logger.info(prompt_preview)
                self.logger.info(f"--- END PROMPT ---")

                # Use structured output with the LLM
                structured_llm = self.llm.with_structured_output(
                    PhaseStructureOutput, method="function_calling", strict=True
                )

                response = await structured_llm.ainvoke(phase_prompt)
                # With structured output, response is the Pydantic object, not a response with .content
                if hasattr(response, "content"):
                    self.logger.info(f"🔍 LLM response received: {len(response.content)} chars")
                    self.logger.info(f"🔍 LLM response preview: {response.content[:200]}...")
                    self.logger.info(f"🔍 FULL LLM RESPONSE:")
                    self.logger.info(f"--- START LLM RESPONSE ---")
                    self.logger.info(response.content)
                    self.logger.info(f"--- END LLM RESPONSE ---")
                else:
                    self.logger.info(f"🔍 Structured LLM response received: {type(response)}")
                    self.logger.info(f"🔍 Response preview: {str(response)[:200]}...")

                # Parse using structured output
                try:
                    parsed_output = response  # response is already a Pydantic object
                    self.logger.info(f"✅ Successfully parsed structured phase structure")
                    self.logger.info(f"🔍 Number of phases: {len(parsed_output.phases)}")
                    self.logger.info(f"🔍 Dependencies: {len(parsed_output.dependencies)}")
                    self.logger.info(f"🔍 Risks: {len(parsed_output.risks)}")
                    self.logger.info(f"🔍 Context summary: {len(parsed_output.context_summary)} items")
                    if parsed_output.context_summary:
                        self.logger.info(f"🔍 Context summary preview: {parsed_output.context_summary[0][:100]}...")

                    # Convert to the expected format
                    phase_structure = {
                        "phases": [phase.model_dump() for phase in parsed_output.phases],
                        "dependencies": parsed_output.dependencies,
                        "risks": parsed_output.risks,
                        "estimated_duration": parsed_output.estimated_duration,
                        "success_criteria": parsed_output.success_criteria,
                        "context_summary": parsed_output.context_summary,
                    }

                    self.logger.info(f"✅ Created phase structure with {len(phase_structure['phases'])} phases")

                except Exception as parse_error:
                    self.logger.warning(f"⚠️ Structured parsing failed: {parse_error}")
                    self.logger.warning("⚠️ Falling back to manual parsing")
                    # With structured output, response is the Pydantic object, not a response with .content
                    if hasattr(response, "content"):
                        phase_structure = self._parse_phase_structure(response.content, topic_analysis)
                    else:
                        # If response is already a Pydantic object, try to extract data
                        phase_structure = self._parse_phase_structure(str(response), topic_analysis)

                self.logger.info(f"🔍 Final phase structure: {phase_structure is not None}")
            else:
                self.logger.warning("⚠️ No LLM available, using fallback")
                # Fallback phase generation
                phase_structure = self._create_fallback_plan(state["plan_topic"], state["context"])

            state["phase_structure"] = phase_structure
            return state

        except Exception as e:
            self.logger.warning(f"Phase generation failed: {e}")
            state["error_message"] = str(e)
            return state

    async def _validate_plan_logic(self, state: TopicAnalysisState) -> TopicAnalysisState:
        """Validate plan coherence and quality."""
        self.logger.info(f"🔍 Validating plan logic...")
        phase_structure = state.get("phase_structure")
        self.logger.info(f"🔍 Phase structure available: {phase_structure is not None}")

        # For now, basic validation - can be enhanced later
        validation_results = {"coherent": True, "complete": True, "actionable": True}
        state["validation_results"] = validation_results
        self.logger.info(f"🔍 Validation completed: {validation_results}")
        return state

    def _parse_topic_analysis(self, response_content: str, plan_topic: str) -> PlanTopicAnalysis:
        """Parse LLM response into structured topic analysis."""
        try:
            import json

            self.logger.info(f"🔍 Parsing topic analysis response...")
            self.logger.info(f"🔍 Response length: {len(response_content)} chars")
            self.logger.info(f"🔍 Contains '{{': {'{' in response_content}")
            self.logger.info(f"🔍 Contains '}}': {'}' in response_content}")

            # Try to extract JSON from response
            if "{" in response_content and "}" in response_content:
                start = response_content.find("{")
                end = response_content.rfind("}") + 1
                json_str = response_content[start:end]
                self.logger.info(f"🔍 Extracted topic analysis JSON (length: {len(json_str)}):")
                self.logger.info(f"--- START TOPIC ANALYSIS JSON ---")
                self.logger.info(json_str)
                self.logger.info(f"--- END TOPIC ANALYSIS JSON ---")

                data = json.loads(json_str)
                self.logger.info(f"✅ Successfully parsed topic analysis JSON")
                self.logger.info(
                    f"🔍 Topic analysis data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}"
                )

                return PlanTopicAnalysis(
                    topic=plan_topic,
                    domain_type=data.get("domain_type", "feature"),
                    complexity_level=data.get("complexity_level", "moderate"),
                    architectural_scope=data.get("architectural_scope", ["backend"]),
                    technology_stack=data.get("technology_stack", ["python"]),
                    estimated_effort=data.get("estimated_effort", "medium"),
                    risk_level=data.get("risk_level", "medium"),
                    stakeholders_needed=data.get("stakeholders_needed", ["architect", "developer", "qa"]),
                )
        except Exception as e:
            self.logger.warning(f"Failed to parse topic analysis: {e}")

        # Fallback to intelligent analysis
        return self._intelligent_fallback_analysis(plan_topic, "")

    def _intelligent_fallback_analysis(self, plan_topic: str, context: str) -> PlanTopicAnalysis:
        """Intelligent fallback analysis using context and patterns."""
        self.logger.info(f"🔍 Using intelligent fallback analysis for: '{plan_topic}'")

        # Analyze from context first
        context_analysis = self._analyze_from_context(plan_topic, context)

        # Analyze from patterns
        pattern_analysis = self._analyze_from_patterns(plan_topic, context)

        # Combine analyses intelligently
        combined_analysis = self._combine_analyses(context_analysis, pattern_analysis, plan_topic)

        self.logger.info(
            f"🔍 Intelligent fallback result: {combined_analysis.domain_type}, {combined_analysis.complexity_level}"
        )
        return combined_analysis

    def _analyze_from_context(self, plan_topic: str, context: str) -> dict[str, Any]:
        """Analyze topic from available context."""
        context_lower = context.lower()
        topic_lower = plan_topic.lower()

        analysis = {
            "domain_type": "feature",
            "complexity_level": "moderate",
            "architectural_scope": [],
            "technology_stack": ["python"],
            "estimated_effort": "medium",
            "risk_level": "medium",
        }

        # Analyze domain type from context
        if any(word in context_lower for word in ["bug", "fix", "error", "issue", "problem", "broken"]):
            analysis["domain_type"] = "bugfix"
        elif any(word in context_lower for word in ["refactor", "clean", "improve", "optimize", "restructure"]):
            analysis["domain_type"] = "refactor"
        elif any(word in context_lower for word in ["infrastructure", "deploy", "ci", "cd", "pipeline", "devops"]):
            analysis["domain_type"] = "infrastructure"
        elif any(word in context_lower for word in ["performance", "speed", "memory", "optimize", "slow", "fast"]):
            analysis["domain_type"] = "performance"
        elif any(word in context_lower for word in ["feature", "new", "add", "implement", "create"]):
            analysis["domain_type"] = "feature"

        # Analyze complexity from context
        if any(word in context_lower for word in ["simple", "basic", "small", "minor", "quick"]):
            analysis["complexity_level"] = "simple"
        elif any(
            word in context_lower for word in ["complex", "enterprise", "large", "major", "comprehensive", "extensive"]
        ):
            analysis["complexity_level"] = "complex"
        elif any(word in context_lower for word in ["critical", "urgent", "important", "high priority"]):
            analysis["complexity_level"] = "enterprise"

        # Analyze architectural scope from context
        if any(word in context_lower for word in ["frontend", "ui", "user", "interface", "react", "vue", "angular"]):
            analysis["architectural_scope"].append("frontend")
        if any(word in context_lower for word in ["backend", "api", "server", "service", "endpoint", "controller"]):
            analysis["architectural_scope"].append("backend")
        if any(word in context_lower for word in ["database", "db", "data", "storage", "sql", "nosql"]):
            analysis["architectural_scope"].append("database")
        if any(word in context_lower for word in ["testing", "test", "qa", "quality", "validation"]):
            analysis["architectural_scope"].append("testing")
        if any(word in context_lower for word in ["security", "auth", "authentication", "authorization"]):
            analysis["architectural_scope"].append("security")

        # Default scope if none found
        if not analysis["architectural_scope"]:
            analysis["architectural_scope"] = ["backend"]

        # Analyze risk level from context
        if any(word in context_lower for word in ["critical", "urgent", "high risk", "dangerous", "breaking"]):
            analysis["risk_level"] = "critical"
        elif any(word in context_lower for word in ["high", "important", "significant", "major"]):
            analysis["risk_level"] = "high"
        elif any(word in context_lower for word in ["low", "minor", "simple", "safe"]):
            analysis["risk_level"] = "low"

        return analysis

    def _analyze_from_patterns(self, plan_topic: str, context: str) -> dict[str, Any]:
        """Analyze topic from codebase patterns and common structures."""
        topic_lower = plan_topic.lower()

        analysis = {
            "domain_type": "feature",
            "complexity_level": "moderate",
            "architectural_scope": [],
            "technology_stack": ["python"],
            "estimated_effort": "medium",
            "risk_level": "medium",
        }

        # Pattern-based domain analysis
        if any(word in topic_lower for word in ["fix", "bug", "error", "issue", "problem"]):
            analysis["domain_type"] = "bugfix"
        elif any(word in topic_lower for word in ["refactor", "clean", "improve", "optimize"]):
            analysis["domain_type"] = "refactor"
        elif any(word in topic_lower for word in ["infrastructure", "deploy", "ci", "cd", "pipeline"]):
            analysis["domain_type"] = "infrastructure"
        elif any(word in topic_lower for word in ["performance", "speed", "memory", "optimize"]):
            analysis["domain_type"] = "performance"

        # Pattern-based complexity analysis
        if any(word in topic_lower for word in ["simple", "basic", "small", "minor"]):
            analysis["complexity_level"] = "simple"
        elif any(word in topic_lower for word in ["complex", "enterprise", "large", "major"]):
            analysis["complexity_level"] = "complex"

        # Pattern-based scope analysis
        if any(word in topic_lower for word in ["frontend", "ui", "user", "interface"]):
            analysis["architectural_scope"].append("frontend")
        if any(word in topic_lower for word in ["backend", "api", "server", "service"]):
            analysis["architectural_scope"].append("backend")
        if any(word in topic_lower for word in ["database", "db", "data", "storage"]):
            analysis["architectural_scope"].append("database")

        # Default scope if none found
        if not analysis["architectural_scope"]:
            analysis["architectural_scope"] = ["backend"]

        return analysis

    def _combine_analyses(
        self, context_analysis: dict[str, Any], pattern_analysis: dict[str, Any], plan_topic: str
    ) -> PlanTopicAnalysis:
        """Combine context and pattern analyses intelligently."""
        # Prefer context analysis when available, fall back to pattern analysis
        final_analysis = context_analysis.copy()

        # Use pattern analysis for missing or weak context analysis
        if final_analysis["domain_type"] == "feature" and pattern_analysis["domain_type"] != "feature":
            final_analysis["domain_type"] = pattern_analysis["domain_type"]

        if final_analysis["complexity_level"] == "moderate" and pattern_analysis["complexity_level"] != "moderate":
            final_analysis["complexity_level"] = pattern_analysis["complexity_level"]

        # Combine architectural scopes
        combined_scope = list(set(final_analysis["architectural_scope"] + pattern_analysis["architectural_scope"]))
        final_analysis["architectural_scope"] = combined_scope if combined_scope else ["backend"]

        # Create final result
        return PlanTopicAnalysis(
            topic=plan_topic,
            domain_type=final_analysis["domain_type"],
            complexity_level=final_analysis["complexity_level"],
            architectural_scope=final_analysis["architectural_scope"],
            technology_stack=final_analysis["technology_stack"],
            estimated_effort=final_analysis["estimated_effort"],
            risk_level=final_analysis["risk_level"],
            stakeholders_needed=self._determine_stakeholders(final_analysis),
        )

    def _determine_stakeholders(self, analysis: dict[str, Any]) -> list[str]:
        """Determine required stakeholders based on analysis."""
        stakeholders = ["architect", "developer", "qa"]

        # Add stakeholders based on domain type
        if analysis["domain_type"] == "infrastructure":
            stakeholders.append("devops")
        elif analysis["domain_type"] == "feature":
            stakeholders.append("pm")

        # Add stakeholders based on architectural scope
        if "frontend" in analysis["architectural_scope"]:
            stakeholders.append("frontend_dev")
        if "database" in analysis["architectural_scope"]:
            stakeholders.append("dba")
        if "security" in analysis["architectural_scope"]:
            stakeholders.append("security")

        # Add stakeholders based on risk level
        if analysis["risk_level"] in ["high", "critical"]:
            stakeholders.append("tech_lead")

        return list(set(stakeholders))  # Remove duplicates

    def _fallback_topic_analysis(self, plan_topic: str, context: str) -> PlanTopicAnalysis:
        """Fallback topic analysis using keyword matching."""
        self.logger.info(f"🔍 Using fallback topic analysis for: '{plan_topic}'")
        topic_lower = plan_topic.lower()

        # Determine domain type
        if any(word in topic_lower for word in ["bug", "fix", "error", "issue"]):
            domain_type = "bugfix"
        elif any(word in topic_lower for word in ["refactor", "clean", "improve", "optimize"]):
            domain_type = "refactor"
        elif any(word in topic_lower for word in ["infrastructure", "deploy", "ci", "cd", "pipeline"]):
            domain_type = "infrastructure"
        elif any(word in topic_lower for word in ["performance", "speed", "memory", "optimize"]):
            domain_type = "performance"
        else:
            domain_type = "feature"

        # Determine complexity
        if any(word in topic_lower for word in ["simple", "basic", "small"]):
            complexity_level = "simple"
        elif any(word in topic_lower for word in ["complex", "enterprise", "large", "major"]):
            complexity_level = "complex"
        else:
            complexity_level = "moderate"

        # Determine architectural scope
        architectural_scope = []
        if any(word in topic_lower for word in ["frontend", "ui", "user", "interface"]):
            architectural_scope.append("frontend")
        if any(word in topic_lower for word in ["backend", "api", "server", "service"]):
            architectural_scope.append("backend")
        if any(word in topic_lower for word in ["database", "db", "data", "storage"]):
            architectural_scope.append("database")
        if not architectural_scope:
            architectural_scope = ["backend"]  # Default

        result = PlanTopicAnalysis(
            topic=plan_topic,
            domain_type=domain_type,
            complexity_level=complexity_level,
            architectural_scope=architectural_scope,
            technology_stack=["python"],  # Default for this project
            estimated_effort="medium",
            risk_level="medium",
            stakeholders_needed=["architect", "developer", "qa"],
        )

        self.logger.info(f"🔍 Fallback analysis result: {domain_type}, {complexity_level}, {architectural_scope}")
        return result

    def _parse_phase_structure(self, response_content: str, topic_analysis: PlanTopicAnalysis) -> dict[str, Any]:
        """Parse LLM response into structured phase structure."""
        try:
            import json
            import re

            self.logger.info(f"🔍 Parsing LLM response for JSON...")
            self.logger.info(f"🔍 Response length: {len(response_content)} chars")
            self.logger.info(f"🔍 Contains '{{': {'{' in response_content}")
            self.logger.info(f"🔍 Contains '}}': {'}' in response_content}")

            # Clean the response content
            cleaned_content = response_content.strip()

            # Try multiple JSON extraction strategies
            json_str = None

            # Strategy 1: Look for JSON between ```json and ```
            json_match = re.search(r"```json\s*(.*?)\s*```", cleaned_content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1).strip()
                self.logger.info(f"🔍 Found JSON in code block")

            # Strategy 2: Look for JSON between ``` and ```
            if not json_str:
                json_match = re.search(r"```\s*(.*?)\s*```", cleaned_content, re.DOTALL)
                if json_match:
                    potential_json = json_match.group(1).strip()
                    if potential_json.startswith("{") and potential_json.endswith("}"):
                        json_str = potential_json
                        self.logger.info(f"🔍 Found JSON in generic code block")

            # Strategy 3: Extract JSON from the response directly
            if not json_str and "{" in cleaned_content and "}" in cleaned_content:
                start = cleaned_content.find("{")
                end = cleaned_content.rfind("}") + 1
                json_str = cleaned_content[start:end]
                self.logger.info(f"🔍 Extracted JSON from response directly")

            if json_str:
                self.logger.info(f"🔍 Extracted JSON string (length: {len(json_str)}):")
                self.logger.info(f"--- START EXTRACTED JSON ---")
                self.logger.info(json_str)
                self.logger.info(f"--- END EXTRACTED JSON ---")

                parsed = json.loads(json_str)
                self.logger.info(f"✅ Successfully parsed JSON structure")
                self.logger.info(
                    f"🔍 Parsed structure keys: {list(parsed.keys()) if isinstance(parsed, dict) else 'Not a dict'}"
                )

                # Validate required fields
                if isinstance(parsed, dict) and "phases" in parsed:
                    self.logger.info(f"✅ JSON structure is valid with {len(parsed['phases'])} phases")
                    return parsed
                else:
                    self.logger.warning(f"⚠️ JSON structure missing required 'phases' field")
            else:
                self.logger.warning("⚠️ No JSON found in LLM response")
                self.logger.warning(f"🔍 Response content preview: {response_content[:500]}...")

        except json.JSONDecodeError as e:
            self.logger.warning(f"JSON decode error: {e}")
            self.logger.warning(f"Invalid JSON at line {e.lineno}, column {e.colno}")
        except Exception as e:
            self.logger.warning(f"Failed to parse phase structure: {e}")
            self.logger.warning(f"Error type: {type(e).__name__}")
            self.logger.warning(f"Response content: {response_content[:500]}...")

        # Fallback to template-based generation
        self.logger.warning("⚠️ Using fallback plan due to parsing failure")
        return self._create_fallback_plan(topic_analysis.topic, "")

    def _create_fallback_plan(self, plan_topic: str, context: str) -> dict[str, Any]:
        """Create fallback plan structure when intelligent analysis fails."""
        self.logger.warning(f"⚠️ Creating fallback plan for: '{plan_topic}'")
        return {
            "phases": [
                {
                    "name": "Analysis and Design",
                    "description": f"Analyze requirements for {plan_topic}",
                    "tasks": ["Requirement analysis", "Technical design", "Risk assessment"],
                    "deliverables": ["Requirements document", "Technical specification"],
                    "acceptance_criteria": ["Requirements validated", "Design approved"],
                },
                {
                    "name": "Implementation",
                    "description": f"Implement {plan_topic}",
                    "tasks": ["Core implementation", "Integration", "Unit testing"],
                    "deliverables": ["Working implementation", "Test coverage"],
                    "acceptance_criteria": ["Functionality complete", "Tests passing"],
                },
                {
                    "name": "Validation and Deployment",
                    "description": f"Validate and deploy {plan_topic}",
                    "tasks": ["Integration testing", "User acceptance", "Deployment"],
                    "deliverables": ["Validated system", "Deployment documentation"],
                    "acceptance_criteria": ["System validated", "Successfully deployed"],
                },
            ],
            "dependencies": ["Codebase analysis", "Stakeholder review"],
            "risks": ["Technical complexity", "Integration challenges"],
            "estimated_duration": "To be determined based on scope",
            "success_criteria": [
                "All functionality implemented as specified",
                "Tests pass with adequate coverage",
                "Documentation updated and accurate",
                "System validated and deployed successfully",
            ],
        }
