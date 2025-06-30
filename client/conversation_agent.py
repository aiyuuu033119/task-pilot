"""Conversation-aware agent that maintains chat history"""
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

class ConversationAgent:
    """Chatbot agent that maintains conversation history"""
    
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
        
        # MCP client for accessing MCP tools
        self.mcp_client = MCPClient(base_url=f"http://{config.MCP_SERVER_HOST}:{config.MCP_SERVER_PORT}")
        
        # Register all tools
        self._register_tools()
        
        # Storage for notes and conversation state
        self.notes_storage = {}
        self.conversation_state = {}
    
    def _register_tools(self):
        """Register all tools with the agent"""
        agent = self
        
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
        async def remember_fact(ctx: RunContext[None], fact: str, category: str = "general") -> Dict[str, Any]:
            """Remember a fact about the user or conversation."""
            # Use default session for now since deps might be None
            session_id = "default"
            
            if session_id not in agent.conversation_state:
                agent.conversation_state[session_id] = {"facts": {}}
            
            if category not in agent.conversation_state[session_id]["facts"]:
                agent.conversation_state[session_id]["facts"][category] = []
            
            agent.conversation_state[session_id]["facts"][category].append(fact)
            
            return {
                "success": True,
                "message": f"I'll remember that: {fact}",
                "category": category
            }
        
        @self.agent.tool
        async def recall_facts(ctx: RunContext[None], category: Optional[str] = None) -> Dict[str, Any]:
            """Recall facts from the conversation."""
            # Use default session for now since deps might be None
            session_id = "default"
            
            if session_id not in agent.conversation_state:
                return {"facts": {}, "message": "No facts remembered yet"}
            
            facts = agent.conversation_state[session_id].get("facts", {})
            
            if category:
                return {
                    "category": category,
                    "facts": facts.get(category, []),
                    "count": len(facts.get(category, []))
                }
            else:
                return {
                    "all_facts": facts,
                    "total_count": sum(len(f) for f in facts.values())
                }
        
        @self.agent.tool
        async def list_mcp_tools(ctx: RunContext[None]) -> Dict[str, Any]:
            """List all available tools from the MCP server."""
            try:
                tools = await agent.mcp_client.list_tools()
                return {
                    "success": True,
                    "tools": [
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.input_schema
                        }
                        for tool in tools
                    ],
                    "count": len(tools)
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to list MCP tools: {str(e)}",
                    "message": "MCP server may not be running"
                }
        
        @self.agent.tool
        async def call_mcp_tool(ctx: RunContext[None], tool_name: str, arguments: Dict[str, Any] = {}) -> Dict[str, Any]:
            """Call a tool from the MCP server.
            
            Args:
                tool_name: Name of the MCP tool to call
                arguments: Arguments to pass to the tool
            """
            try:
                result = await agent.mcp_client.call_tool(tool_name, arguments)
                return {
                    "success": True,
                    "tool_name": tool_name,
                    "result": result
                }
            except Exception as e:
                return {
                    "success": False,
                    "tool_name": tool_name,
                    "error": f"Failed to call MCP tool: {str(e)}"
                }
    
    def _build_context_prompt(self, message: str, context: Optional[ChatContext] = None) -> str:
        """Build a prompt that includes conversation context."""
        if not context or not context.message_history:
            return message
        
        # Get recent conversation summary
        recent_messages = context.message_history[-10:]  # Last 10 messages
        
        # Build context summary
        context_parts = []
        
        # Add conversation summary
        if recent_messages:
            context_parts.append("Recent conversation context:")
            for msg in recent_messages[-6:]:  # Show last 3 exchanges
                role = msg.get("role", "user")
                content = msg.get("content", "")[:100]  # Truncate long messages
                if len(msg.get("content", "")) > 100:
                    content += "..."
                context_parts.append(f"{role.capitalize()}: {content}")
        
        # Add current message
        context_parts.append(f"\nCurrent message: {message}")
        
        # Add instruction to maintain context
        context_parts.append("\nPlease respond to the current message while maintaining awareness of the conversation context.")
        
        return "\n".join(context_parts)
    
    async def __aenter__(self):
        """Enter async context"""
        # Initialize MCP client
        await self.mcp_client.__aenter__()
        
        # Check MCP server health
        try:
            if await self.mcp_client.health_check():
                print("MCP server is connected and healthy")
                tools = await self.mcp_client.list_tools()
                print(f"Available MCP tools: {[tool.name for tool in tools]}")
            else:
                print("MCP server is not available - MCP tools disabled")
        except Exception as e:
            print(f"MCP server connection error: {e}")
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context"""
        await self.http_client.aclose()
        await self.mcp_client.__aexit__(exc_type, exc_val, exc_tb)
    
    async def chat(self, message: str, context: Optional[ChatContext] = None) -> str:
        """Process a chat message and return the response."""
        try:
            # Build message with context
            contextualized_message = self._build_context_prompt(message, context)
            
            # Run the agent
            result = await self.agent.run(contextualized_message)
            return result.data
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    async def stream_chat(self, message: str, context: Optional[ChatContext] = None):
        """Stream a chat response."""
        try:
            # Build message with context
            contextualized_message = self._build_context_prompt(message, context)
            
            # Stream the response
            async with self.agent.run_stream(contextualized_message) as stream:
                # Use stream_text(delta=True) to get only new text chunks
                async for chunk in stream.stream_text(delta=True):
                    yield chunk
                    
        except Exception as e:
            yield f"I encountered an error: {str(e)}"

# Singleton instance
_conversation_agent_instance: Optional[ConversationAgent] = None

async def get_conversation_agent() -> ConversationAgent:
    """Get or create the singleton conversation agent instance"""
    global _conversation_agent_instance
    if _conversation_agent_instance is None:
        _conversation_agent_instance = ConversationAgent()
    return _conversation_agent_instance