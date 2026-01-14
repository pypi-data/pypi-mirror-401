# standard
# third party
# custom
from src.sunwaee_gen.logger import logger
from src.sunwaee_gen.agents.anthropic import *
from src.sunwaee_gen.agents.deepseek import *
from src.sunwaee_gen.agents.google import *
from src.sunwaee_gen.agents.openai import *
from src.sunwaee_gen.agents.xai import *

AGENTS = {
    a.name: a
    for a in ANTHROPIC_AGENTS
    + DEEPSEEK_AGENTS
    + GOOGLE_AGENTS
    + OPENAI_AGENTS
    + XAI_AGENTS
}

logger.debug(f"AVAILABLE AGENTS: {AGENTS.keys()}")
