# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Simplemind-ng is a Python library providing a unified, human-friendly interface for multiple LLM providers. It abstracts away provider-specific complexity, allowing identical API usage across Anthropic, OpenAI, Gemini, Groq, Ollama, xAI, Amazon Bedrock, and Deepseek.

## Commands

```bash
# Install with all providers
uv pip install 'simplemind-ng[full]'

# Install with specific provider only
uv pip install 'simplemind-ng[anthropic]'  # or openai, gemini, groq, ollama, xai, amazon, deepseek

# Run tests
uv run pytest

# Run a single test file
uv run pytest tests/test_generate_text.py

# Run a single test
uv run pytest tests/test_generate_text.py::test_generate_text -v
```

## Architecture

### Core Flow

```
Public API (simplemind_ng/__init__.py)
    ├── generate_text(prompt) → find_provider() → provider.generate_text() → str
    ├── generate_data(prompt, response_model) → provider.structured_response() → Pydantic model
    ├── create_conversation() → Conversation object
    └── Session(llm_provider, llm_model) → reusable config wrapper
```

### Provider System

All providers inherit from `BaseProvider` (`providers/_base.py`) and implement:
- `client` / `structured_client` - raw and instructor-wrapped LLM clients
- `send_conversation()` / `send_conversation_stream()` - conversation handling
- `structured_response()` - Pydantic model extraction via instructor
- `tool` - provider-specific function calling implementation

Provider lookup happens via `utils.find_provider(name)` which matches against `Provider.NAME`.

### Conversation & Plugin System

`Conversation` (`models.py`) manages message history with plugin hooks:
- `initialize_hook` / `cleanup_hook` - context manager lifecycle
- `pre_send_hook` / `post_send_hook` - intercept send operations
- `add_message_hook` - intercept message additions

Plugins extend `BasePlugin` and raise `NotImplementedError` for unused hooks.

### Tool/Function Calling

Each provider has its own tool class (e.g., `AnthropicTool`, `OpenAITool`) extending `BaseTool` (`providers/_base_tools.py`). Tools are created from Python functions via `Tool.from_function()`, using type hints and `Annotated[..., Field()]` for parameter schemas.

## Key Files

- `simplemind_ng/__init__.py` - Public API: `generate_text`, `generate_data`, `create_conversation`, `Session`, `tool` decorator
- `simplemind_ng/models.py` - `Message`, `Conversation`, `BasePlugin`
- `simplemind_ng/providers/_base.py` - `BaseProvider` abstract class
- `simplemind_ng/providers/_base_tools.py` - `BaseTool` for function calling
- `simplemind_ng/settings.py` - API key management via environment variables

## Environment Variables

```
OPENAI_API_KEY, ANTHROPIC_API_KEY, XAI_API_KEY, DEEPSEEK_API_KEY,
GROQ_API_KEY, GOOGLE_API_KEY
```

For Amazon Bedrock, use standard AWS credentials (AWS_ACCESS_KEY_ID, etc.)

## Adding a New Provider

1. Create `providers/newprovider.py` with a class extending `BaseProvider`
2. Set `NAME` (used for lookup) and `DEFAULT_MODEL`
3. Implement required abstract methods
4. Add tool class extending `BaseTool` if function calling is supported
5. Register in `providers/__init__.py`
6. Add optional dependency group in `pyproject.toml`
