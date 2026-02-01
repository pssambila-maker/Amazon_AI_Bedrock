"""
Simple test wrapper for Windows compatibility
"""
import sys
import io

# Set UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import asyncio
from cost_optimization_agent import process_request


async def test_query(query: str, description: str):
    """Test a single query and display results"""
    print(f"\n{'=' * 80}")
    print(f"TEST: {description}")
    print(f"{'=' * 80}")
    print(f"Query: {query}\n")
    print("Response:")
    print("-" * 80)

    payload = {"prompt": query}

    full_response = []
    async for chunk in process_request(payload):
        if chunk.get("type") == "chunk":
            data = chunk.get("data", "")
            print(data, end="", flush=True)
            full_response.append(data)
        elif chunk.get("error"):
            print(f"\nError: {chunk['error']}")
            return

    print("\n" + "=" * 80 + "\n")
    return "".join(full_response)


async def main():
    """Run a simple test"""
    print("\n" + "=" * 80)
    print("COST OPTIMIZATION AGENT - LOCAL TEST")
    print("=" * 80 + "\n")

    # Test 1: Simple cost query
    await test_query(
        "Are my costs higher than usual?",
        "Natural Language Understanding - Anomaly Detection"
    )

    print("\nTest completed!")


if __name__ == "__main__":
    asyncio.run(main())
