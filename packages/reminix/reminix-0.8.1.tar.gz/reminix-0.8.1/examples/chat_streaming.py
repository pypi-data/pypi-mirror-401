"""Streaming chat example.

This example demonstrates a streaming chat interaction with an agent.
Text is printed in real-time as the agent generates its response.

Usage:
    export REMINIX_API_KEY="your-api-key"
    python examples/chat_streaming.py
"""

import reminix

client = reminix.Reminix()

print("Assistant: ", end="", flush=True)

with client.agents.chat_stream(
    "my-agent",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a short story about a robot."},
    ],
) as stream:
    for chunk in stream:
        print(chunk.chunk, end="", flush=True)

print()  # Final newline
