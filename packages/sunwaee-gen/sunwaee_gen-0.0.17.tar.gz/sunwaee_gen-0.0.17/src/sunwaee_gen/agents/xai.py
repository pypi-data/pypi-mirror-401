# standard
# third party
# custom
from src.sunwaee_gen.agent import Agent, AgentCost, AgentFeatures, AgentSpecs
from src.sunwaee_gen.models.xai import *
from src.sunwaee_gen.providers.xai import *

GROK_4_1_FAST_AGENT = Agent(
    name="xai/grok-4-1-fast-reasoning",
    model=GROK_4_1_FAST,
    provider=XAI,
    cost=AgentCost(input_per_1m_token=0.2, output_per_1m_token=0.5),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=False,
    ),
    specs=AgentSpecs(max_input_tokens=2000000, max_output_tokens=30000),
)

GROK_CODE_FAST_1_AGENT = Agent(
    name="xai/grok-code-fast-1",
    model=GROK_CODE_FAST_1,
    provider=XAI,
    cost=AgentCost(input_per_1m_token=0.2, output_per_1m_token=1.5),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=True,
    ),
    specs=AgentSpecs(max_input_tokens=256000, max_output_tokens=256000),
)

GROK_4_AGENT = Agent(
    name="xai/grok-4",
    model=GROK_4,
    provider=XAI,
    cost=AgentCost(input_per_1m_token=3, output_per_1m_token=15),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=False,
    ),
    specs=AgentSpecs(max_input_tokens=256000, max_output_tokens=256000),
)

GROK_3_AGENT = Agent(
    name="xai/grok-3",
    model=GROK_3,
    provider=XAI,
    cost=AgentCost(input_per_1m_token=3, output_per_1m_token=15),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=False,
        reasoning_tokens_access=False,
    ),
    specs=AgentSpecs(max_input_tokens=131072, max_output_tokens=131072),
)

GROK_3_MINI_AGENT = Agent(
    name="xai/grok-3-mini",
    model=GROK_3_MINI,
    provider=XAI,
    cost=AgentCost(input_per_1m_token=0.3, output_per_1m_token=0.5),
    features=AgentFeatures(
        supports_tools=True,
        supports_reasoning=True,
        reasoning_tokens_access=False,
    ),
    specs=AgentSpecs(max_input_tokens=131072, max_output_tokens=131072),
)


XAI_AGENTS = [
    GROK_4_1_FAST_AGENT,
    GROK_CODE_FAST_1_AGENT,
    GROK_4_AGENT,
    GROK_3_AGENT,
    GROK_3_MINI_AGENT,
]
