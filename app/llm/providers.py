from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

class OpenAILLM:
    def __init__(self, model: str, api_key: str):
        self.client = ChatOpenAI(model=model, api_key=api_key, temperature=0)
    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        response = await self.client.ainvoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
        return str(response.content)

class AnthropicLLM:
    def __init__(self, model: str, api_key: str):
        self.client = ChatAnthropic(model=model, api_key=api_key, temperature=0)
    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        response = await self.client.ainvoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
        return str(response.content)

class MockLLM:
    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        return """SUMMARY:
Mock analysis completed successfully.

ANALYSIS:
The repository context was collected. Mock mode does not call an external LLM. Review the relevant files, reproduce the problem, make a focused change, and verify it with tests.

PROPOSED_CHANGES:
- Find the smallest code path related to the request.
- Add validation and clear error handling.
- Add or update automated tests.
- Update documentation when behavior changes.

PATCH:
```diff
# Mock mode does not generate a real patch.
# Select OpenAI or Anthropic for model-generated output.
```
"""
