#!/usr/bin/env python3
"""Debug tool registration and execution"""
import asyncio
from pydantic_ai import Agent, RunContext
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

async def test_tools():
    """Test tool registration and execution"""
    
    # Create a simple agent
    model = "openai:gpt-4o" if os.getenv("OPENAI_API_KEY") else "anthropic:claude-3-5-sonnet-20241022"
    agent = Agent(model, system_prompt="You are a helpful assistant.")
    
    # Register a simple tool
    @agent.tool
    async def test_tool(ctx: RunContext[None], message: str) -> Dict[str, Any]:
        """A simple test tool"""
        print(f"Tool called with message: {message}")
        print(f"Context type: {type(ctx)}")
        print(f"Context dir: {dir(ctx)}")
        
        return {
            "success": True,
            "message": f"Received: {message}",
            "context_info": {
                "has_deps": hasattr(ctx, "deps"),
                "deps_value": getattr(ctx, "deps", None)
            }
        }
    
    # Test the agent
    try:
        result = await agent.run("Please use the test_tool with message 'Hello World'")
        print(f"\nAgent response: {result.data}")
    except Exception as e:
        print(f"Error running agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_tools())