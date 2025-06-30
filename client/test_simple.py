#!/usr/bin/env python3
"""Simple test to check if tools are working"""
import asyncio
from conversation_agent import get_conversation_agent

async def main():
    """Test basic tool functionality"""
    print("Testing conversation agent tools...")
    
    agent = await get_conversation_agent()
    
    async with agent:
        # Test listing MCP tools
        print("\n1. Testing list_mcp_tools directly:")
        try:
            result = await agent.chat("Please list all available MCP tools using the list_mcp_tools function")
            print(f"Response: {result}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test a simple calculation
        print("\n2. Testing calculator:")
        try:
            result = await agent.chat("What is 10 + 15?")
            print(f"Response: {result}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test current time
        print("\n3. Testing get_current_time:")
        try:
            result = await agent.chat("What time is it?")
            print(f"Response: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())