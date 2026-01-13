# Noodler Python SDK

## Example

```python
from noodler import setup, instrument_openai
from openai import OpenAI

# Configure OpenTelemetry tracing
setup(
    base_url="http://localhost:8000",
    api_key="noodler-api-key",
)

# Create and instrument OpenAI client
client = OpenAI()
wrapped_client = instrument_openai(client)

# Use the instrumented client - all API calls will be automatically traced
# Non-streaming
response = wrapped_client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "user", "content": "hi there!"}
    ],
)

# Streaming (also supported)
stream = wrapped_client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "user", "content": "hi there!"}
    ],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content, end="")
```

## Features

- ✅ Automatic tracing of `chat.completions.create()` calls
- ✅ Support for both streaming and non-streaming responses
- ✅ Full OpenTelemetry GenAI semantic convention compliance
- ✅ Token usage tracking
- ✅ Error tracking and span status reporting

## Limitations

Currently, only the `chat.completions.create()` endpoint is instrumented. Other OpenAI endpoints (embeddings, audio, fine-tuning, etc.) are not automatically traced. Calls to these endpoints will work normally but will not generate traces.