"""Streaming invoke example.

This example demonstrates a streaming task invocation with an agent.
Text is printed in real-time as the agent generates its response.

Usage:
    export REMINIX_API_KEY="your-api-key"
    python examples/invoke_streaming.py
"""

import reminix

client = reminix.Reminix()

print("Output: ", end="", flush=True)

with client.agents.invoke_stream(
    "my-agent",
    input={
        "task": "generate",
        "prompt": "Write a haiku about programming.",
    },
) as stream:
    for chunk in stream:
        print(chunk.chunk, end="", flush=True)

print()  # Final newline
