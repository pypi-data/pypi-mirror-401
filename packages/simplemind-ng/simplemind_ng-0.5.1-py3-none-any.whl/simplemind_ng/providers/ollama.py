from functools import cached_property
from typing import TYPE_CHECKING, Callable, Iterator, Type, TypeVar

import instructor
from pydantic import BaseModel

from ..logging import logger
from ..settings import settings
from ._base import BaseProvider
from ._base_tools import BaseTool
from .openai import OpenAITool

if TYPE_CHECKING:
    from ..models import Conversation, Message

T = TypeVar("T", bound=BaseModel)


class Ollama(BaseProvider):
    NAME = "ollama"
    DEFAULT_MODEL = "llama3.2"
    DEFAULT_TIMEOUT = 60
    DEFAULT_KWARGS = {}
    supports_streaming = True

    def __init__(self, host_url: str | None = None):
        self.host_url = host_url or settings.OLLAMA_HOST_URL

    @cached_property
    def client(self):
        """The raw Ollama client."""
        if not self.host_url:
            raise ValueError("No ollama host url provided")
        try:
            import openai
        except ImportError as exc:
            raise ImportError(
                "Please install the `openai` package: `pip install openai`"
            ) from exc
        return openai.OpenAI(base_url=f"{self.host_url}/v1", api_key="ollama")

    @cached_property
    def structured_client(self) -> instructor.Instructor:
        """A client patched with Instructor."""
        return instructor.from_openai(
            self.client,
            mode=instructor.Mode.JSON,
        )

    @cached_property
    def tool(self) -> Type[BaseTool]:
        """The tool implementation for Ollama (uses OpenAI-compatible format)."""
        return OpenAITool

    @logger
    def send_conversation(
        self,
        conversation: "Conversation",
        tools: list[Callable | BaseTool] | None = None,
        **kwargs,
    ) -> "Message":
        """Send a conversation to the Ollama API."""
        from ..models import Message

        messages = [
            {"role": msg.role, "content": msg.text}
            for msg in conversation.messages
        ]

        # Set up tools if provided
        converted_tools = self.make_tools(tools)
        tools_config = (
            [t.get_input_schema() for t in converted_tools] if tools else None
        )

        request_kwargs = {
            **self.DEFAULT_KWARGS,
            **kwargs,
            "model": conversation.llm_model or self.DEFAULT_MODEL,
            "messages": messages,
        }

        if tools_config:
            request_kwargs["tools"] = tools_config

        # Make initial API call
        response = self.client.chat.completions.create(**request_kwargs)

        # Handle tool responses if needed
        while response.choices[0].message.tool_calls:
            for tool in converted_tools:
                tool.handle(response, messages)
                if tool.is_executed():
                    response = self.client.chat.completions.create(**request_kwargs)
                    tool.reset_result()

        assistant_message = response.choices[0].message

        # Create and return a properly formatted Message instance
        return Message(
            role="assistant",
            text=assistant_message.content or "",
            raw=response,
            llm_model=conversation.llm_model or self.DEFAULT_MODEL,
            llm_provider=self.NAME,
        )

    @logger
    def send_conversation_stream(
        self,
        conversation: "Conversation",
        tools: list[Callable | BaseTool] | None = None,
        **kwargs,
    ):
        """Stream a conversation response from the Ollama API."""
        messages = [
            {"role": msg.role, "content": msg.text}
            for msg in conversation.messages
        ]

        # Set up tools if provided
        converted_tools = self.make_tools(tools)
        tools_config = (
            [t.get_input_schema() for t in converted_tools] if tools else None
        )

        request_kwargs = {
            **self.DEFAULT_KWARGS,
            **kwargs,
            "model": conversation.llm_model or self.DEFAULT_MODEL,
            "messages": messages,
            "stream": True,
        }

        if tools_config:
            request_kwargs["tools"] = tools_config

        response = self.client.chat.completions.create(**request_kwargs)

        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    @logger
    def structured_response(
        self,
        prompt: str,
        response_model: Type[T],
        *,
        llm_model: str | None = None,
        **kwargs,
    ) -> T:
        """Get a structured response from the Ollama API."""
        messages = [
            {"role": "user", "content": prompt},
        ]

        response = self.structured_client.chat.completions.create(
            messages=messages,
            model=llm_model or self.DEFAULT_MODEL,
            response_model=response_model,
            **{**self.DEFAULT_KWARGS, **kwargs},
        )
        return response_model.model_validate(response)

    @logger
    def generate_text(
        self, prompt: str, *, llm_model: str | None = None, **kwargs
    ) -> str:
        """Generate text using the Ollama API."""
        messages = [
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat.completions.create(
            messages=messages,
            model=llm_model or self.DEFAULT_MODEL,
            **{**self.DEFAULT_KWARGS, **kwargs},
        )

        return response.choices[0].message.content

    @logger
    def generate_stream_text(
        self, prompt: str, *, llm_model: str, **kwargs
    ) -> Iterator[str]:
        # Prepare the messages.
        messages = [
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat.completions.create(
            messages=messages,
            model=llm_model or self.DEFAULT_MODEL,
            stream=True,
            **{**self.DEFAULT_KWARGS, **kwargs},
        )

        # Iterate over the response and yield the content.
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
