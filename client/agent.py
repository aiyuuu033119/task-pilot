"""Pydantic AI Agent with tools"""
import os
import httpx
import math
import datetime
from typing import Optional, List, Dict, Any
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from config import config
from mcp_client import MCPClient

class ChatContext(BaseModel):
    """Context for chat conversations"""
    user_id: str
    session_id: str
    message_history: List[Dict[str, str]] = []

class ChatAgent:
    """Chatbot agent using Pydantic AI with custom tools and MCP integration"""
    
    def __init__(self):
        # Determine model string based on provider
        if config.MODEL_PROVIDER == "anthropic":
            model_string = f"anthropic:{config.DEFAULT_MODEL}"
        else:
            model_string = f"openai:{config.DEFAULT_MODEL}"
        
        # Initialize the agent without MCP servers for now
        self.agent = Agent(
            model_string,
            system_prompt=config.SYSTEM_PROMPT
        )
        
        # Initialize MCP client
        self.mcp_client = MCPClient(f"http://{config.MCP_SERVER_HOST}:{config.MCP_SERVER_PORT}")
        
        # Register tools directly
        self._register_tools()
        
        # Register MCP tools
        self._register_mcp_tools()
        
        # Storage for notes
        self.notes_storage = {}
    
    def _register_tools(self):
        """Register tools with the agent"""
        
        @self.agent.tool
        async def calculator(ctx: RunContext[None], expression: str) -> Dict[str, Any]:
            """Evaluate mathematical expressions safely."""
            try:
                # Define safe functions
                safe_dict = {
                    'abs': abs, 'round': round, 'min': min, 'max': max,
                    'sum': sum, 'pow': pow, 'sqrt': math.sqrt,
                    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                    'pi': math.pi, 'e': math.e
                }
                
                # Evaluate expression safely
                result = eval(expression, {"__builtins__": {}}, safe_dict)
                
                return {
                    "success": True,
                    "expression": expression,
                    "result": result
                }
            except Exception as e:
                return {
                    "success": False,
                    "expression": expression,
                    "error": str(e)
                }
        
        @self.agent.tool
        async def get_current_time(ctx: RunContext[None], timezone: str = "UTC") -> Dict[str, str]:
            """Get the current date and time."""
            now = datetime.datetime.utcnow()
            
            return {
                "timezone": timezone,
                "datetime": now.isoformat(),
                "date": now.date().isoformat(),
                "time": now.time().isoformat(),
                "timestamp": now.timestamp()
            }
        
        @self.agent.tool
        async def get_weather(ctx: RunContext[None], location: str) -> Dict[str, Any]:
            """Get weather information for a location (mock data for demo)."""
            # Mock weather data
            mock_weather = {
                "location": location,
                "temperature": 22,
                "unit": "celsius",
                "condition": "partly cloudy",
                "humidity": 65,
                "wind_speed": 10,
                "wind_unit": "km/h"
            }
            
            return mock_weather
        
        # Create a closure to access self
        agent = self
        
        @self.agent.tool
        async def save_note(ctx: RunContext[None], title: str, content: str) -> Dict[str, Any]:
            """Save a note for later retrieval."""
            note_id = f"note_{len(agent.notes_storage) + 1}"
            agent.notes_storage[note_id] = {
                "id": note_id,
                "title": title,
                "content": content,
                "created_at": datetime.datetime.utcnow().isoformat()
            }
            
            return {
                "success": True,
                "note_id": note_id,
                "message": f"Note '{title}' saved successfully"
            }
        
        @self.agent.tool
        async def get_notes(ctx: RunContext[None]) -> Dict[str, Any]:
            """Retrieve all saved notes."""
            return {
                "success": True,
                "notes": list(agent.notes_storage.values()),
                "count": len(agent.notes_storage)
            }
    
    def _register_mcp_tools(self):
        """Register MCP server tools as dynamic tools"""
        agent = self
        
        @self.agent.tool
        async def call_mcp_tool(ctx: RunContext[None], tool_name: str, **kwargs) -> Dict[str, Any]:
            """Call a tool from the MCP server.
            Available MCP tools will be discovered dynamically."""
            try:
                async with agent.mcp_client as client:
                    result = await client.call_tool(tool_name, kwargs)
                    return result
            except Exception as e:
                return {"error": f"Failed to call MCP tool: {str(e)}"}
        
        # Also register a tool to list available MCP tools
        @self.agent.tool
        async def list_mcp_tools(ctx: RunContext[None]) -> Dict[str, Any]:
            """List all available tools from the MCP server."""
            try:
                async with agent.mcp_client as client:
                    tools = await client.list_tools()
                    return {
                        "success": True,
                        "tools": [
                            {
                                "name": tool.name,
                                "description": tool.description
                            }
                            for tool in tools
                        ],
                        "count": len(tools)
                    }
            except Exception as e:
                return {"error": f"Failed to list MCP tools: {str(e)}"}
    
    async def __aenter__(self):
        """Enter async context"""
        # Check MCP server health
        try:
            async with self.mcp_client as client:
                if await client.health_check():
                    print("MCP server is healthy")
                    # List available tools
                    tools = await client.list_tools()
                    if tools:
                        print(f"Found {len(tools)} MCP tools:")
                        for tool in tools:
                            print(f"  - {tool.name}: {tool.description}")
                else:
                    print("MCP server is not responding")
        except Exception as e:
            print(f"MCP server check failed: {e}")
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context"""
        pass
    
    async def chat(self, message: str, context: Optional[ChatContext] = None) -> str:
        """
        Process a chat message and return the response.
        
        Args:
            message: User's message
            context: Optional chat context with history
            
        Returns:
            AI assistant's response
        """
        try:
            # Build conversation history
            messages = []
            
            if context and context.message_history:
                # Include recent history (limited by MAX_CHAT_HISTORY)
                recent_history = context.message_history[-config.MAX_CHAT_HISTORY:]
                
                # Convert history to the format expected by pydantic-ai
                for msg in recent_history:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    
                    # Add messages in the format that maintains context
                    if role == "user":
                        messages.append(f"User: {content}")
                    elif role == "assistant":
                        messages.append(f"Assistant: {content}")
            
            # Add current message
            messages.append(f"User: {message}")
            
            # Join all messages into a conversation
            full_conversation = "\n\n".join(messages)
            
            # Run the agent with the full conversation context
            result = await self.agent.run(full_conversation)
            
            return result.output
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    async def stream_chat(self, message: str, context: Optional[ChatContext] = None):
        """
        Stream a chat response.
        
        Args:
            message: User's message
            context: Optional chat context with history
            
        Yields:
            Chunks of the response as they're generated
        """
        try:
            # Build conversation history
            messages = []
            
            if context and context.message_history:
                # Include recent history (limited by MAX_CHAT_HISTORY)
                recent_history = context.message_history[-config.MAX_CHAT_HISTORY:]
                
                # Convert history to the format expected by pydantic-ai
                for msg in recent_history:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    
                    # Add messages in the format that maintains context
                    if role == "user":
                        messages.append(f"User: {content}")
                    elif role == "assistant":
                        messages.append(f"Assistant: {content}")
            
            # Add current message
            messages.append(f"User: {message}")
            
            # Join all messages into a conversation
            full_conversation = "\n\n".join(messages)
            
            # Use run_stream for streaming response
            async with self.agent.run_stream(full_conversation) as stream:
                async for chunk in stream.stream():
                    yield chunk
                
        except Exception as e:
            yield f"I encountered an error: {str(e)}"

# Singleton instance
_agent_instance: Optional[ChatAgent] = None

async def get_agent() -> ChatAgent:
    """Get or create the singleton agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = ChatAgent()
    return _agent_instance