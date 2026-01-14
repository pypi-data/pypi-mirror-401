# standard
# third party
# custom
from src.sunwaee_gen.logger import logger
from src.sunwaee_gen.tools.execute_command import execute_command

TOOLS = {
    tool.function.name: tool
    for tool in [
        execute_command,
    ]
}

logger.debug(f"AVAILABLE TOOLS: {list(TOOLS.keys())}")
