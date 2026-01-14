# standard
# third party
# custom
from src.sunwaee_gen.model import Model

GEMINI_3_PRO_PREVIEW = Model(
    name="gemini-3-pro-preview",
    display_name="Gemini 3 Pro Preview",
    origin="google",
)

GEMINI_3_FLASH_PREVIEW = Model(
    name="gemini-3-flash-preview",
    display_name="Gemini 3 Flash Preview",
    origin="google",
)

GEMINI_2_5_PRO = Model(
    name="gemini-2.5-pro",
    display_name="Gemini 2.5 Pro",
    origin="google",
)

GEMINI_2_5_FLASH = Model(
    name="gemini-2.5-flash",
    display_name="Gemini 2.5 Flash",
    origin="google",
)

GEMINI_2_5_FLASH_LITE = Model(
    name="gemini-2.5-flash-lite",
    display_name="Gemini 2.5 Flash Lite",
    origin="google",
)

GOOGLE_MODELS = [
    GEMINI_3_PRO_PREVIEW,
    GEMINI_3_FLASH_PREVIEW,
    GEMINI_2_5_PRO,
    GEMINI_2_5_FLASH,
    GEMINI_2_5_FLASH_LITE,
]
