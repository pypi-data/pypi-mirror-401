"""
VY Organ SDK - Capabilities Module

Provides pre-configured clients for accessing other organs via CNS Bus.
All inter-organ communication goes through the CNS Bus - NEVER direct connections.

Available capabilities:
- CNSClient: Base client for dispatching intents via CNS Bus HTTP
- MemoryCapability: Access to Memory Guild (episodic, semantic, procedural, self, working)
- LLMCapability: Access to LLM Router (complete, chat)

Example usage:
    from vy_organ_sdk.capabilities import CNSClient, MemoryCapability, LLMCapability

    class MyOrgan(OrganHandler):
        def __init__(self):
            self.cns = CNSClient()
            self.memory = MemoryCapability(self.cns)
            self.llm = LLMCapability(self.cns)

        async def handle(self, request: HandlerRequest) -> HandlerResponse:
            # Use memory to get context
            context = await self.memory.build_context("my query")

            # Use LLM to generate response
            response = await self.llm.complete("Generate code for...")

            return HandlerResponse(ok=True, result={"response": response})
"""

from .cns_client import CNSClient, CNSDispatchError
from .memory import MemoryCapability
from .llm import LLMCapability

__all__ = [
    "CNSClient",
    "CNSDispatchError",
    "MemoryCapability",
    "LLMCapability",
]
