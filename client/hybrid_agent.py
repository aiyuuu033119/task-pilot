"""Hybrid agent that uses both local and remote tools"""
import os
import httpx
import math
import datetime
from typing import Optional, List, Dict, Any
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from config import config

class ChatContext(BaseModel):
    """Context for chat conversations"""
    user_id: str
    session_id: str
    message_history: List[Dict[str, str]] = []

class HybridChatAgent:
    """Chatbot agent with both local tools and remote MCP tools"""
    
    def __init__(self):
        # Determine model string based on provider
        if config.MODEL_PROVIDER == "anthropic":
            model_string = f"anthropic:{config.DEFAULT_MODEL}"
        else:
            model_string = f"openai:{config.DEFAULT_MODEL}"
        
        # Initialize the agent
        self.agent = Agent(
            model_string,
            system_prompt=config.SYSTEM_PROMPT
        )
        
        # HTTP client for MCP server
        self.http_client = httpx.AsyncClient(
            base_url=f"http://{config.MCP_SERVER_HOST}:{config.MCP_SERVER_PORT}",
            timeout=30.0
        )
        
        # Register all tools
        self._register_tools()
        
        # Storage for notes
        self.notes_storage = {}
    
    def _register_tools(self):
        """Register all tools with the agent"""
        agent = self
        
        # Local calculator (as backup)
        @self.agent.tool
        async def calculator(ctx: RunContext[None], expression: str) -> Dict[str, Any]:
            """Evaluate mathematical expressions safely."""
            try:
                safe_dict = {
                    'abs': abs, 'round': round, 'min': min, 'max': max,
                    'sum': sum, 'pow': pow, 'sqrt': math.sqrt,
                    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                    'pi': math.pi, 'e': math.e
                }
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
            """Get weather information for a location."""
            # Try MCP server first
            try:
                # Direct HTTP call to MCP server endpoint
                response = await agent.http_client.get(
                    "/weather",
                    params={"location": location}
                )
                if response.status_code == 200:
                    return response.json()
            except:
                pass
            
            # Fallback to mock data
            return {
                "location": location,
                "temperature": 22,
                "unit": "celsius",
                "condition": "partly cloudy",
                "humidity": 65,
                "wind_speed": 10,
                "wind_unit": "km/h"
            }
        
        @self.agent.tool
        async def web_search(ctx: RunContext[None], query: str, max_results: int = 3) -> Dict[str, Any]:
            """Search the web for information."""
            # Try MCP server
            try:
                response = await agent.http_client.get(
                    "/search",
                    params={"query": query, "max_results": max_results}
                )
                if response.status_code == 200:
                    return response.json()
            except:
                pass
            
            # Fallback
            return {
                "success": True,
                "query": query,
                "results": [
                    {
                        "title": f"Result about {query}",
                        "snippet": f"Information related to {query}...",
                        "url": "https://example.com"
                    }
                ],
                "source": "fallback"
            }
        
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
        
        @self.agent.tool
        async def check_mcp_server(ctx: RunContext[None]) -> Dict[str, Any]:
            """Check if MCP server is available and list its capabilities."""
            try:
                response = await agent.http_client.get("/health")
                if response.status_code == 200:
                    return {
                        "success": True,
                        "status": "MCP server is running",
                        "health": response.json()
                    }
            except Exception as e:
                return {
                    "success": False,
                    "status": "MCP server is not available",
                    "error": str(e)
                }
    
    async def __aenter__(self):
        """Enter async context"""
        # Check MCP server
        try:
            response = await self.http_client.get("/health")
            if response.status_code == 200:
                print("MCP server is connected and healthy")
        except:
            print("MCP server is not available - using local tools only")
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context"""
        await self.http_client.aclose()
    
    async def chat(self, message: str, context: Optional[ChatContext] = None) -> str:
        """Process a chat message and return the response."""
        try:
            # For pydantic-ai, we need to pass the message with proper context
            # The agent will use the system prompt and tools to respond
            
            # Just pass the current message - pydantic-ai doesn't support conversation history directly
            # We'll need to include relevant context in the message itself if needed
            result = await self.agent.run(message)
            return result.data
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    async def stream_chat(self, message: str, context: Optional[ChatContext] = None):
        """Stream a chat response."""
        try:
            # Just pass the current message for streaming
            async with self.agent.run_stream(message) as stream:
                async for chunk in stream.stream():
                    yield chunk
                    
        except Exception as e:
            yield f"I encountered an error: {str(e)}"

# Singleton instance
_hybrid_agent_instance: Optional[HybridChatAgent] = None

async def get_hybrid_agent() -> HybridChatAgent:
    """Get or create the singleton hybrid agent instance"""
    global _hybrid_agent_instance
    if _hybrid_agent_instance is None:
        _hybrid_agent_instance = HybridChatAgent()
    return _hybrid_agent_instance