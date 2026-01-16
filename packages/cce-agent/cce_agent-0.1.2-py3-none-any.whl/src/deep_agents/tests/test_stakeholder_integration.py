from src.deep_agents.stakeholder_integration import CCE_StakeholderIntegration, UnifiedStakeholderAgent


def test_load_deep_agents_subagents_accepts_dicts(monkeypatch):
    integration = CCE_StakeholderIntegration()
    monkeypatch.setattr("src.deep_agents.stakeholder_integration.SubAgent", object())
    monkeypatch.setattr(
        "src.deep_agents.stakeholder_integration.ALL_STAKEHOLDER_AGENTS",
        [{"name": "context-engineer", "tools": ["sync_to_disk"]}],
    )
    monkeypatch.setattr(
        "src.deep_agents.stakeholder_integration.context_engineering_agent",
        {"name": "context-engineer", "tools": ["sync_to_disk"]},
    )
    monkeypatch.setattr(
        "src.deep_agents.stakeholder_integration.general_purpose_agent",
        {"name": "general-purpose", "tools": ["create_plan"]},
    )
    monkeypatch.setattr(
        "src.deep_agents.stakeholder_integration.planning_agent",
        {"name": "planning-specialist", "tools": ["create_plan"]},
    )

    subagents = integration._load_deep_agents_subagents()

    assert "context-engineer" in subagents
    assert "general-purpose" in subagents
    assert "planning-specialist" in subagents


def test_execute_cce_stakeholder_uses_supervisor_graph():
    integration = CCE_StakeholderIntegration()

    class FakeSupervisor:
        def __init__(self):
            self.called = None

        def run(self, integration_challenge, stakeholder_charter, thread_id, output_directory=None):
            self.called = {
                "integration_challenge": integration_challenge,
                "stakeholder_charter": stakeholder_charter,
                "thread_id": thread_id,
                "output_directory": output_directory,
            }
            return {"status": "ok"}

    integration.supervisor_graph = FakeSupervisor()
    stakeholder = UnifiedStakeholderAgent(
        name="AIDER Specialist",
        description="",
        cce_agent=object(),
        deep_agents_subagent=None,
        capabilities=[],
        execution_mode="cce",
    )
    integration.unified_stakeholder_system = {"aider_specialist": stakeholder}

    result = integration.execute_stakeholder_task(
        "aider_specialist",
        {"integration_challenge": "challenge", "stakeholder_charter": "charter"},
        execution_mode="cce",
    )

    assert result["success"] is True
    assert integration.supervisor_graph.called["integration_challenge"] == "challenge"


def test_execute_deep_agents_stakeholder_uses_executor():
    integration = CCE_StakeholderIntegration()

    async def fake_executor(instruction, context):
        return {"success": True, "result": "ok", "instruction": instruction, "context": context}

    integration.deep_agents_executor = fake_executor
    stakeholder = UnifiedStakeholderAgent(
        name="context-engineer",
        description="",
        cce_agent=None,
        deep_agents_subagent={"name": "context-engineer"},
        capabilities=[],
        execution_mode="deep_agents",
    )
    integration.unified_stakeholder_system = {"context-engineer": stakeholder}

    result = integration.execute_stakeholder_task(
        "context-engineer",
        {"instruction": "analyze context"},
        execution_mode="deep_agents",
    )

    assert result["success"] is True
    assert result["execution_mode"] == "deep_agents"
    assert result["stakeholder"] == "context-engineer"
