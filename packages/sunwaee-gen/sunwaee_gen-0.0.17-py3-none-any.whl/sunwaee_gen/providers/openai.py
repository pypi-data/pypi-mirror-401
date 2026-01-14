# standard
# third party
# custom
from src.sunwaee_gen.provider import Provider


OPENAI = Provider(
    name="openai",
    url="https://api.openai.com/v1/chat/completions",
)
