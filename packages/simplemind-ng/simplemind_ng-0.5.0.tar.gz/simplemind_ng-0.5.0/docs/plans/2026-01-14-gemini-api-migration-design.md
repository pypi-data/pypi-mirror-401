# Gemini API Migration: google-generativeai → google-genai

## Overview

Migrate the Gemini provider from the legacy `google-generativeai` package to the new `google-genai` SDK, which uses a centralized client architecture and improved APIs.

## Changes

### Package & Configuration

**pyproject.toml:**
```python
# Before
gemini = ["google-generativeai", "jsonref"]

# After
gemini = ["google-genai"]
```

**Environment Variable:**
- Rename `GEMINI_API_KEY` → `GOOGLE_API_KEY`
- Update `settings.py` to map "gemini" provider to "google" key
- Update README.md and CLAUDE.md documentation

### Default Model

- Before: `models/gemini-1.5-flash-latest`
- After: `gemini-2.0-flash`

### Client Architecture

**Before (legacy):**
```python
import google.generativeai as genai
genai.configure(api_key=self.api_key)
client = genai.GenerativeModel(model_name=self.model_name)
```

**After (new SDK):**
```python
from google import genai
client = genai.Client(api_key=self.api_key)
# Model specified per-request
client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
```

### Streaming

**Before:**
```python
response = client.generate_content(prompt, stream=True)
for chunk in response:
    yield chunk.text
```

**After:**
```python
for chunk in client.models.generate_content_stream(model=model, contents=prompt):
    yield chunk.text
```

### Conversation Format

Gemini uses `"model"` instead of `"assistant"` for role names:
```python
contents = [
    {"role": "user" if msg.role == "user" else "model", "parts": [{"text": msg.text}]}
    for msg in conversation.messages
]
```

### Instructor Integration

**Before:**
```python
instructor.from_gemini(model)  # Deprecated
```

**After:**
```python
instructor.from_genai(client, use_async=False)
```

### Tool/Function Calling

Add new `GeminiTool` class implementing:
- `get_input_schema()` - Gemini function declaration format
- `get_response_schema()` - Function response format
- `handle()` - Execute tool and update conversation contents

**Function declaration format:**
```python
{
    "name": self.name,
    "description": self.description,
    "parameters": {
        "type": "object",
        "properties": self.get_properties_schema(),
        "required": self.required,
    },
}
```

**Function response format:**
```python
{
    "role": "function",
    "parts": [{
        "function_response": {
            "name": self.name,
            "response": {"result": self.function_result},
        }
    }],
}
```

## Files to Modify

| File | Changes |
|------|---------|
| `pyproject.toml` | Update gemini dependency |
| `simplemind_ng/settings.py` | Rename GEMINI_API_KEY → GOOGLE_API_KEY |
| `simplemind_ng/providers/_base.py` | Fix `send_conversation_stream` return type to `Iterator[str]` |
| `simplemind_ng/providers/gemini.py` | Complete rewrite |
| `README.md` | Update env var documentation |
| `CLAUDE.md` | Update env var documentation |

## Breaking Changes

1. **Environment variable renamed:** `GEMINI_API_KEY` → `GOOGLE_API_KEY`
2. **Default model changed:** `models/gemini-1.5-flash-latest` → `gemini-2.0-flash`
3. **Dependency changed:** `google-generativeai` → `google-genai`

## Implementation Notes

- No backwards compatibility shims - clean migration
- Tool calling added (was not implemented before)
- Conversation streaming added (was not implemented before)
- Base class type hint fix for `send_conversation_stream`
