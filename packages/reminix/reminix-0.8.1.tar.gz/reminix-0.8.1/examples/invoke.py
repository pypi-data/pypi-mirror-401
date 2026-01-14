"""Basic invoke example (non-streaming).

This example demonstrates a simple one-shot task invocation with an agent.

Usage:
    export REMINIX_API_KEY="your-api-key"
    python examples/invoke.py
"""

import reminix

client = reminix.Reminix()

response = client.agents.invoke(
    "my-agent",
    input={
        "task": "analyze",
        "data": {"values": [1, 2, 3, 4, 5]},
    },
)

print(f"Output: {response.output}")
