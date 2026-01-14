# standard
# third party
# custom
from src.sunwaee_gen.agents._registry import AGENTS
from src.sunwaee_gen.agent import Agent
from src.sunwaee_gen.message import Message
from src.sunwaee_gen.tool import Tool


async def async_completion(
    agent: str | Agent,
    messages: list[dict],
    tools: list[dict] | None = None,
    streaming: bool = False,
    api_key: str | None = None,
):
    if isinstance(agent, str):
        if agent not in AGENTS:
            available_agents = list(AGENTS.keys())
            raise ValueError(
                f"Agent '{agent}' not found. Available agents: {available_agents}"
            )
        agent_obj = AGENTS[agent]
    else:
        agent_obj = agent

    # NOTE validate messages, including roles,
    # tool calls and tool results
    _ = Message.from_list(messages)

    # NOTE validate tools
    _ = Tool.from_list(tools) if tools else None

    async for block in agent_obj.async_completion(
        messages=messages,
        tools=tools,
        streaming=streaming,
        api_key=api_key,
    ):
        yield block
