"""Async streaming chat example.

This example demonstrates an async streaming chat interaction with an agent.
Text is printed in real-time as the agent generates its response.

Usage:
    export REMINIX_API_KEY="your-api-key"
    python examples/chat_streaming_async.py
"""

import asyncio

import reminix


async def main() -> None:
    client = reminix.AsyncReminix()

    print("Assistant: ", end="", flush=True)

    async with await client.agents.chat_stream(
        "my-agent",
        messages=[
            {"role": "user", "content": "Tell me a joke."},
        ],
    ) as stream:
        async for chunk in stream:
            print(chunk.chunk, end="", flush=True)

    print()  # Final newline


if __name__ == "__main__":
    asyncio.run(main())
