"""Basic chat example (non-streaming).

This example demonstrates a simple chat interaction with an agent.

Usage:
    export REMINIX_API_KEY="your-api-key"
    python examples/chat.py
"""

import reminix

client = reminix.Reminix()

response = client.agents.chat(
    "my-agent",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
    ],
)

print(f"Assistant: {response.messages[-1].content}")
