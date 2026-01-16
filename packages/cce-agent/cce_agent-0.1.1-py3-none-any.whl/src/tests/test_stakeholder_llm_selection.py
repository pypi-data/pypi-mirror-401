from src.stakeholder_generator import stakeholder_agents
from src.stakeholder_generator.stakeholder_agents import StakeholderAgent, StakeholderType


def test_stakeholder_llm_prefers_anthropic(monkeypatch):
    class FakeAnthropic:
        def __init__(self, model, temperature, api_key):
            self.model = model
            self.temperature = temperature
            self.api_key = api_key

    class FakeOpenAI:
        def __init__(self, model, temperature):
            self.model = model
            self.temperature = temperature

    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic-key")
    monkeypatch.setenv("OPENAI_API_KEY", "openai-key")
    monkeypatch.setattr(stakeholder_agents, "ChatAnthropic", FakeAnthropic)
    monkeypatch.setattr(stakeholder_agents, "ChatOpenAI", FakeOpenAI)

    agent = StakeholderAgent(StakeholderType.AIDER_INTEGRATION, prompt_manager=object())

    assert isinstance(agent.llm, FakeAnthropic)


def test_stakeholder_llm_falls_back_to_openai(monkeypatch):
    class FakeAnthropic:
        def __init__(self, model, temperature, api_key):
            self.model = model
            self.temperature = temperature
            self.api_key = api_key

    class FakeOpenAI:
        def __init__(self, model, temperature):
            self.model = model
            self.temperature = temperature

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "openai-key")
    monkeypatch.setattr(stakeholder_agents, "ChatAnthropic", FakeAnthropic)
    monkeypatch.setattr(stakeholder_agents, "ChatOpenAI", FakeOpenAI)

    agent = StakeholderAgent(StakeholderType.AIDER_INTEGRATION, prompt_manager=object())

    assert isinstance(agent.llm, FakeOpenAI)
