#!/usr/bin/env python3
"""Test script to verify MCP tools integration"""
import asyncio
import sys
from conversation_agent import get_conversation_agent, ChatContext

async def test_mcp_tools():
    """Test MCP tool functionality"""
    print("Testing MCP Tools Integration")
    print("=" * 50)
    
    # Get the conversation agent
    agent = await get_conversation_agent()
    
    async with agent:
        print("\n1. Testing list_mcp_tools:")
        result = await agent.chat("Please list all available MCP tools")
        print(f"Response: {result}\n")
        
        print("2. Testing calculator through MCP:")
        result = await agent.chat("Use the MCP calculator tool to calculate 25 * 4")
        print(f"Response: {result}\n")
        
        print("3. Testing weather through MCP:")
        result = await agent.chat("What's the weather in London using the MCP weather tool?")
        print(f"Response: {result}\n")
        
        print("4. Testing web search through MCP:")
        result = await agent.chat("Search for 'Python programming' using the MCP web search tool")
        print(f"Response: {result}\n")
        
        print("5. Testing note-taking through MCP:")
        result = await agent.chat("Save a note titled 'Test Note' with content 'This is a test from MCP integration'")
        print(f"Response: {result}\n")
        
        print("6. Testing direct MCP tool call:")
        result = await agent.chat("Call the MCP tool named 'get_current_time' to get the current time")
        print(f"Response: {result}\n")

if __name__ == "__main__":
    print("Make sure the MCP server is running on port 8001!")
    print("Starting test in 3 seconds...\n")
    asyncio.run(test_mcp_tools())