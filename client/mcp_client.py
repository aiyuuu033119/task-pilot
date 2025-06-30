"""MCP Client for connecting to the FastMCP server"""
import httpx
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class MCPTool:
    """Represents an MCP tool"""
    name: str
    description: str
    input_schema: Dict[str, Any]

class MCPClient:
    """Client for interacting with FastMCP server"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def list_tools(self) -> List[MCPTool]:
        """List available tools from the MCP server"""
        try:
            # Try the standard MCP endpoint
            response = await self.client.post(
                f"{self.base_url}/mcp",
                json={
                    "jsonrpc": "2.0",
                    "method": "tools/list",
                    "id": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                tools = []
                
                if "result" in data and "tools" in data["result"]:
                    for tool_data in data["result"]["tools"]:
                        tools.append(MCPTool(
                            name=tool_data["name"],
                            description=tool_data.get("description", ""),
                            input_schema=tool_data.get("inputSchema", {})
                        ))
                
                return tools
            else:
                print(f"MCP tools/list failed: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error listing MCP tools: {e}")
            return []
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the MCP server"""
        try:
            response = await self.client.post(
                f"{self.base_url}/mcp",
                json={
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments
                    },
                    "id": 2
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    return data["result"]
                elif "error" in data:
                    return {"error": data["error"]["message"]}
                else:
                    return {"error": "Unknown response format"}
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
                
        except Exception as e:
            return {"error": f"Failed to call tool: {str(e)}"}
    
    async def health_check(self) -> bool:
        """Check if the MCP server is healthy"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False