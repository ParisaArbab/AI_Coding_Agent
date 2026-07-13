from app.core.config import Settings
from app.llm.providers import AnthropicLLM, MockLLM, OpenAILLM

def build_llm(settings: Settings):
    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai.")
        return OpenAILLM(settings.openai_model, settings.openai_api_key)
    if settings.llm_provider == "anthropic":
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER=anthropic.")
        return AnthropicLLM(settings.anthropic_model, settings.anthropic_api_key)
    return MockLLM()
