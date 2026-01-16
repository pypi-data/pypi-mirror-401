from functools import cached_property
from typing import TYPE_CHECKING, Callable, Iterator, Type, TypeVar

import instructor
from pydantic import BaseModel

from ..logging import logger
from ..settings import settings
from ._base import BaseProvider
from ._base_tools import BaseTool

if TYPE_CHECKING:
    from ..models import Conversation, Message

T = TypeVar("T", bound=BaseModel)


class GeminiTool(BaseTool):
    def get_input_schema(self):
        """Return Gemini's function declaration format."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": self.get_properties_schema(),
                "required": self.required,
            },
        }

    def get_response_schema(self):
        """Return the function response for Gemini."""
        return {
            "role": "function",
            "parts": [
                {
                    "function_response": {
                        "name": self.name,
                        "response": {"result": self.function_result},
                    }
                }
            ],
        }

    @logger
    def handle(self, response, contents) -> None:
        """Handle tool execution from Gemini response."""
        part = response.candidates[0].content.parts[0]

        if hasattr(part, "function_call") and part.function_call:
            fn_call = part.function_call
            if fn_call.name == self.name:
                # Execute the function
                self.function_result = str(self.raw_func(**dict(fn_call.args)))

                # Add assistant's function call to contents
                contents.append(
                    {
                        "role": "model",
                        "parts": [
                            {
                                "function_call": {
                                    "name": fn_call.name,
                                    "args": dict(fn_call.args),
                                }
                            }
                        ],
                    }
                )

                # Add function response
                contents.append(self.get_response_schema())


class Gemini(BaseProvider):
    NAME = "gemini"
    DEFAULT_MODEL = "gemini-2.0-flash"
    supports_streaming = True

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.get_api_key(self.NAME)

    @cached_property
    def client(self):
        """The raw Gemini client."""
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        try:
            from google import genai
        except ImportError as exc:
            raise ImportError(
                "Please install the `google-genai` package: `pip install google-genai`"
            ) from exc
        return genai.Client(api_key=self.api_key)

    @cached_property
    def structured_client(self):
        """A Gemini client patched with Instructor."""
        return instructor.from_genai(self.client, use_async=False)

    @cached_property
    def tool(self) -> Type[BaseTool]:
        """The tool implementation for Gemini."""
        return GeminiTool

    @logger
    def generate_text(
        self, prompt: str, *, llm_model: str | None = None, **kwargs
    ) -> str:
        """Generate text using the Gemini API."""
        response = self.client.models.generate_content(
            model=llm_model or self.DEFAULT_MODEL,
            contents=prompt,
            **kwargs,
        )
        return response.text

    @logger
    def generate_stream_text(
        self, prompt: str, *, llm_model: str | None = None, **kwargs
    ) -> Iterator[str]:
        """Generate streaming text using the Gemini API."""
        for chunk in self.client.models.generate_content_stream(
            model=llm_model or self.DEFAULT_MODEL,
            contents=prompt,
            **kwargs,
        ):
            if chunk.text:
                yield chunk.text

    @logger
    def send_conversation(
        self,
        conversation: "Conversation",
        tools: list[Callable | BaseTool] | None = None,
        **kwargs,
    ) -> "Message":
        """Send a conversation to the Gemini API."""
        from ..models import Message

        # Convert messages to Gemini format (Gemini uses "model" instead of "assistant")
        contents = [
            {
                "role": "user" if msg.role == "user" else "model",
                "parts": [{"text": msg.text}],
            }
            for msg in conversation.messages
        ]

        # Set up tools if provided
        converted_tools = self.make_tools(tools)
        tool_config = (
            [t.get_input_schema() for t in converted_tools] if tools else None
        )

        request_kwargs = {
            "model": conversation.llm_model or self.DEFAULT_MODEL,
            "contents": contents,
            **kwargs,
        }
        if tool_config:
            request_kwargs["config"] = {
                "tools": [{"function_declarations": tool_config}]
            }

        response = self.client.models.generate_content(**request_kwargs)

        # Handle tool calls (loop until no more tool calls)
        while (
            response.candidates
            and response.candidates[0].content.parts
            and hasattr(response.candidates[0].content.parts[0], "function_call")
            and response.candidates[0].content.parts[0].function_call
        ):
            for tool in converted_tools:
                tool.handle(response, contents)
                if tool.is_executed():
                    response = self.client.models.generate_content(**request_kwargs)
                    tool.reset_result()

        return Message(
            role="assistant",
            text=response.text,
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
    ) -> Iterator[str]:
        """Stream a conversation response from the Gemini API."""
        # Convert messages to Gemini format
        contents = [
            {
                "role": "user" if msg.role == "user" else "model",
                "parts": [{"text": msg.text}],
            }
            for msg in conversation.messages
        ]

        # Set up tools if provided
        converted_tools = self.make_tools(tools)
        tool_config = (
            [t.get_input_schema() for t in converted_tools] if tools else None
        )

        request_kwargs = {
            "model": conversation.llm_model or self.DEFAULT_MODEL,
            "contents": contents,
            **kwargs,
        }
        if tool_config:
            request_kwargs["config"] = {
                "tools": [{"function_declarations": tool_config}]
            }

        for chunk in self.client.models.generate_content_stream(**request_kwargs):
            if chunk.text:
                yield chunk.text

    @logger
    def structured_response(
        self,
        prompt: str,
        response_model: Type[T],
        *,
        llm_model: str | None = None,
        **kwargs,
    ) -> T:
        """Get a structured response from the Gemini API."""
        response = self.structured_client.create(
            model=llm_model or self.DEFAULT_MODEL,
            contents=prompt,
            response_model=response_model,
            **kwargs,
        )
        return response
