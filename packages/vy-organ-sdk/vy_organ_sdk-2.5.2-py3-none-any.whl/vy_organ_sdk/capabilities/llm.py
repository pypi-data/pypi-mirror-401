"""
LLM Capability - Access to LLM Router via CNS Bus.

Provides a typed interface to LLM Router intents:
- complete: Text completion
- chat: Multi-turn conversation
- list_models: Available models

All LLM calls go through CNS Bus to the LLM Router organ.
"""

from typing import Any, Dict, List, Optional
from .cns_client import CNSClient


class LLMCapability:
    """
    Interface to LLM Router via CNS Bus.

    Example:
        cns = CNSClient()
        llm = LLMCapability(cns)

        # Simple completion
        result = await llm.complete("Write a Python function that...")

        # Chat conversation
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is CNS?"}
        ]
        result = await llm.chat(messages)

        # List available models
        models = await llm.list_models()
    """

    # Default models for different use cases
    DEFAULT_MODEL = "qwen3-coder"
    FAST_MODEL = "qwen3-coder"
    SMART_MODEL = "claude-sonnet-4-20250514"

    def __init__(self, cns: CNSClient, default_model: Optional[str] = None):
        """
        Initialize LLM Capability.

        Args:
            cns: CNSClient instance for dispatching intents
            default_model: Default model to use (defaults to qwen3-coder)
        """
        self.cns = cns
        self.default_model = default_model or self.DEFAULT_MODEL

    async def complete(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        stop: Optional[List[str]] = None,
        system: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate text completion.

        Args:
            prompt: The prompt to complete
            model: Model to use (defaults to instance default)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            stop: Stop sequences
            system: System prompt

        Returns:
            Response with 'text' field containing completion
        """
        payload = {
            "prompt": prompt,
            "model": model or self.default_model,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        if stop:
            payload["stop"] = stop
        if system:
            payload["system"] = system

        return await self.cns.dispatch("vy.llm.complete.v1", payload)

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        system: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Multi-turn chat conversation.

        Args:
            messages: List of messages with 'role' and 'content'
                     Roles: 'system', 'user', 'assistant'
            model: Model to use
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system: System prompt (alternative to system message)

        Returns:
            Response with 'message' field containing assistant response
        """
        payload = {
            "messages": messages,
            "model": model or self.default_model,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        if system:
            payload["system"] = system

        return await self.cns.dispatch("vy.llm.chat.v1", payload)

    async def list_models(self) -> Dict[str, Any]:
        """
        List available models.

        Returns:
            Response with 'models' list containing model info
        """
        return await self.cns.dispatch("vy.llm.model.list.v1", {})

    async def get_model(self, model: str) -> Dict[str, Any]:
        """
        Get information about a specific model.

        Args:
            model: Model ID

        Returns:
            Model information
        """
        return await self.cns.dispatch(
            "vy.llm.model.get.v1",
            {"model": model},
        )

    # Convenience methods for common patterns

    async def generate_code(
        self,
        description: str,
        language: str = "python",
        context: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate code from description.

        Args:
            description: What the code should do
            language: Programming language
            context: Additional context (existing code, requirements)
            model: Model to use

        Returns:
            Response with generated code
        """
        prompt = f"""Generate {language} code for the following:

{description}
"""
        if context:
            prompt = f"""Context:
{context}

{prompt}"""

        prompt += f"\nProvide only the {language} code, no explanations."

        return await self.complete(
            prompt,
            model=model or self.FAST_MODEL,
            temperature=0.3,
        )

    async def analyze_code(
        self,
        code: str,
        question: str,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyze code and answer questions about it.

        Args:
            code: The code to analyze
            question: Question about the code
            model: Model to use

        Returns:
            Analysis response
        """
        prompt = f"""Analyze the following code:

```
{code}
```

Question: {question}

Provide a concise answer."""

        return await self.complete(
            prompt,
            model=model or self.SMART_MODEL,
            temperature=0.3,
        )

    async def fix_code(
        self,
        code: str,
        error: str,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fix code based on error message.

        Args:
            code: The broken code
            error: Error message
            model: Model to use

        Returns:
            Response with fixed code
        """
        prompt = f"""Fix the following code that has this error:

Error: {error}

Code:
```
{code}
```

Provide only the fixed code, no explanations."""

        return await self.complete(
            prompt,
            model=model or self.FAST_MODEL,
            temperature=0.2,
        )

    async def summarize(
        self,
        text: str,
        max_length: int = 200,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Summarize text.

        Args:
            text: Text to summarize
            max_length: Maximum summary length in words
            model: Model to use

        Returns:
            Summary response
        """
        prompt = f"""Summarize the following text in {max_length} words or less:

{text}

Summary:"""

        return await self.complete(
            prompt,
            model=model or self.FAST_MODEL,
            max_tokens=max_length * 2,
            temperature=0.3,
        )

    async def extract_json(
        self,
        text: str,
        schema_description: str,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Extract structured JSON from text.

        Args:
            text: Text to extract from
            schema_description: Description of expected JSON schema
            model: Model to use

        Returns:
            Response with extracted JSON
        """
        prompt = f"""Extract the following information as JSON:

Schema: {schema_description}

Text:
{text}

Return only valid JSON, no other text."""

        return await self.complete(
            prompt,
            model=model or self.SMART_MODEL,
            temperature=0.1,
        )
