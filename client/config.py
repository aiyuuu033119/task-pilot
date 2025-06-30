"""Configuration for the chatbot application"""
import os
from typing import Optional

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class Config:
    # AI Provider settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Default model selection - prioritize working API keys
    if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("your-"):
        DEFAULT_MODEL = "gpt-4o"
        MODEL_PROVIDER = "openai"
    elif ANTHROPIC_API_KEY and not ANTHROPIC_API_KEY.startswith("your-"):
        DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
        MODEL_PROVIDER = "anthropic"
    else:
        DEFAULT_MODEL = "gpt-4o"  # Will require API key at runtime
        MODEL_PROVIDER = "openai"
    
    # MCP Server settings
    MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
    MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", 8001))
    MCP_SERVER_URL = f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}/mcp"
    
    # FastAPI settings
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", 8000))
    
    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chat_history.db")
    
    # Chat settings
    MAX_CHAT_HISTORY = 50  # Maximum messages to keep in context
    SYSTEM_PROMPT = """You are a helpful AI assistant with access to various tools.

LOCAL TOOLS:
- calculator: Evaluate mathematical expressions
- get_current_time: Get current date and time
- get_weather: Get weather information (mock data)
- save_note/get_notes: Save and retrieve notes

MCP SERVER TOOLS:
- call_mcp_tool: Call tools from the MCP server (use tool_name parameter)
- list_mcp_tools: List all available MCP server tools

To use MCP tools, first call list_mcp_tools to see what's available, then use call_mcp_tool with the appropriate tool_name.

IMPORTANT: You are having a continuous conversation with the user. Remember what they told you earlier in the conversation.
The conversation history is provided in the format:
User: [their message]
Assistant: [your previous response]

Always maintain context from previous messages and refer back to earlier parts of the conversation when relevant.
Be concise but friendly in your responses."""

config = Config()