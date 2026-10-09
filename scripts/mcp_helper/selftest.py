"""
selftest.py - checks helper_server.py WITHOUT Claude Desktop, so you can tell whether a problem
is in the server or in the Desktop connection.

Run it with the same Python as in claude_desktop_config.json, from anywhere:
    python scripts/mcp_helper/selftest.py

It starts the server as a child process, speaks MCP to it exactly like Claude Desktop does, runs
three tool calls and prints how long each took. A hang is reported as TIMEOUT, not left waiting.
"""
import asyncio
import sys
import time
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = Path(__file__).resolve().with_name("helper_server.py")
# A choice: every step should answer in seconds. The slowest measured call so far was 5.7 s
# (loading the SDK + listing files), so 60 s is generous, and still short enough to notice a hang.
STEP_TIMEOUT_SECONDS = 60


async def step(label, coroutine):
    """Run one step with a time limit; print the label, the time taken and the first line of the result."""
    started = time.perf_counter()
    try:
        result = await asyncio.wait_for(coroutine, STEP_TIMEOUT_SECONDS)
    except asyncio.TimeoutError:
        print(f"{label}: TIMEOUT after {STEP_TIMEOUT_SECONDS} s")
        return None
    seconds = time.perf_counter() - started
    text = result if isinstance(result, str) else str(result)
    print(f"{label}: OK in {seconds:.1f} s | {text.splitlines()[0][:110] if text else '(empty)'}")
    return result


async def call(session, name, **arguments):
    result = await session.call_tool(name, arguments)
    return "\n".join(part.text for part in result.content if hasattr(part, "text"))


async def main():
    print(f"Python: {sys.executable}")
    print(f"Server: {SERVER}")
    parameters = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            if await step("1 connect", session.initialize()) is None:
                return
            listing = await step("2 list tools", session.list_tools())
            if listing is not None:
                print("   tools:", [tool.name for tool in listing.tools])
            await step("3 search_code 'def watch' *.py", call(session, "search_code", query="def watch", glob="*.py"))
            await step("4 read_lines codemap.py 1-3", call(session, "read_lines", path="scripts/codemap/codemap.py", start=1, end=3))
            await step("5 read_lines ../AI-CONTEXT.md (must be refused)", call(session, "read_lines", path="../AI-CONTEXT.md", start=1, end=2))


if __name__ == "__main__":
    asyncio.run(main())
