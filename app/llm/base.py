from typing import Protocol

class LLMClient(Protocol):
    async def complete(self, system_prompt: str, user_prompt: str) -> str: ...
