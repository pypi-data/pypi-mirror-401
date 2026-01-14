# standard
# third party
# custom
from src.sunwaee_gen.logger import logger
from src.sunwaee_gen.providers.anthropic import *
from src.sunwaee_gen.providers.deepseek import *
from src.sunwaee_gen.providers.google import *
from src.sunwaee_gen.providers.openai import *
from src.sunwaee_gen.providers.xai import *

PROVIDERS = {
    p.name: p
    for p in [
        ANTHROPIC,
        DEEPSEEK,
        GOOGLE,
        OPENAI,
        XAI,
    ]
}

logger.debug(f"AVAILABLE PROVIDERS: {PROVIDERS.keys()}")
