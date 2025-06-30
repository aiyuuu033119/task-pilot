#!/usr/bin/env python3
"""
MCP Server with basic tools for Claude Desktop
Uses stdio transport for direct Claude Desktop integration
"""

import asyncio
import datetime
import json
import math
import os
import random
import re
import uuid
from typing import Any, Dict, List, Optional

from mcp.types import Tool, TextContent
from mcp.server import Server
from mcp import stdio_server
import httpx


# Initialize MCP server
server = Server("task-pilot-tools")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="calculator",
            description="Evaluate mathematical expressions safely",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 2', 'sqrt(16)')"
                    }
                },
                "required": ["expression"]
            }
        ),
        Tool(
            name="get_current_datetime",
            description="Get current date and time information",
            inputSchema={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone (optional, defaults to UTC)",
                        "default": "UTC"
                    },
                    "format": {
                        "type": "string", 
                        "description": "Date format (optional, defaults to ISO format)",
                        "default": "iso"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="generate_uuid",
            description="Generate a random UUID",
            inputSchema={
                "type": "object",
                "properties": {
                    "version": {
                        "type": "integer",
                        "description": "UUID version (1 or 4)",
                        "default": 4
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="hash_text",
            description="Generate hash of text using various algorithms",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to hash"
                    },
                    "algorithm": {
                        "type": "string",
                        "description": "Hash algorithm (md5, sha1, sha256, sha512)",
                        "default": "sha256"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="random_number",
            description="Generate random numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "min": {
                        "type": "number",
                        "description": "Minimum value",
                        "default": 0
                    },
                    "max": {
                        "type": "number", 
                        "description": "Maximum value",
                        "default": 100
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of random numbers to generate",
                        "default": 1
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="text_analysis",
            description="Analyze text for various metrics",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to analyze"
                    }
                },
                "required": ["text"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls"""
    
    if name == "calculator":
        expression = arguments.get("expression", "")
        try:
            # Define safe functions
            safe_dict = {
                'abs': abs, 'round': round, 'min': min, 'max': max,
                'sum': sum, 'pow': pow, 'sqrt': math.sqrt,
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'log': math.log, 'log10': math.log10, 'exp': math.exp,
                'pi': math.pi, 'e': math.e, 'ceil': math.ceil, 'floor': math.floor
            }
            
            # Clean expression - remove any potentially dangerous characters
            clean_expr = re.sub(r'[^0-9+\-*/().,\s\w]', '', expression)
            
            # Evaluate safely
            result = eval(clean_expr, {"__builtins__": {}}, safe_dict)
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "expression": expression,
                    "result": result,
                    "status": "success"
                }, indent=2)
            )]
        except Exception as e:
            return [TextContent(
                type="text", 
                text=json.dumps({
                    "expression": expression,
                    "error": str(e),
                    "status": "error"
                }, indent=2)
            )]
    
    elif name == "get_current_datetime":
        timezone = arguments.get("timezone", "UTC")
        format_type = arguments.get("format", "iso")
        
        try:
            now = datetime.datetime.now(datetime.timezone.utc)
            
            result = {
                "timestamp": now.isoformat(),
                "unix_timestamp": now.timestamp(),
                "timezone": timezone,
                "year": now.year,
                "month": now.month,
                "day": now.day,
                "hour": now.hour,
                "minute": now.minute,
                "second": now.second,
                "weekday": now.strftime("%A"),
                "formatted": {
                    "iso": now.isoformat(),
                    "human": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "date_only": now.strftime("%Y-%m-%d"),
                    "time_only": now.strftime("%H:%M:%S")
                }
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e), "status": "error"}, indent=2)
            )]
    
    elif name == "generate_uuid":
        version = arguments.get("version", 4)
        
        try:
            if version == 1:
                result_uuid = str(uuid.uuid1())
            elif version == 4:
                result_uuid = str(uuid.uuid4())
            else:
                raise ValueError("Only UUID versions 1 and 4 are supported")
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "uuid": result_uuid,
                    "version": version,
                    "status": "success"
                }, indent=2)
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e), "status": "error"}, indent=2)
            )]
    
    elif name == "hash_text":
        text = arguments.get("text", "")
        algorithm = arguments.get("algorithm", "sha256").lower()
        
        try:
            import hashlib
            
            # Encode text to bytes
            text_bytes = text.encode('utf-8')
            
            if algorithm == "md5":
                hash_obj = hashlib.md5(text_bytes)
            elif algorithm == "sha1":
                hash_obj = hashlib.sha1(text_bytes)
            elif algorithm == "sha256":
                hash_obj = hashlib.sha256(text_bytes)
            elif algorithm == "sha512":
                hash_obj = hashlib.sha512(text_bytes)
            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "text": text,
                    "algorithm": algorithm,
                    "hash": hash_obj.hexdigest(),
                    "status": "success"
                }, indent=2)
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e), "status": "error"}, indent=2)
            )]
    
    elif name == "random_number":
        min_val = arguments.get("min", 0)
        max_val = arguments.get("max", 100)
        count = arguments.get("count", 1)
        
        try:
            if count == 1:
                result = random.uniform(min_val, max_val)
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "number": result,
                        "min": min_val,
                        "max": max_val,
                        "status": "success"
                    }, indent=2)
                )]
            else:
                numbers = [random.uniform(min_val, max_val) for _ in range(count)]
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "numbers": numbers,
                        "count": count,
                        "min": min_val,
                        "max": max_val,
                        "status": "success"
                    }, indent=2)
                )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e), "status": "error"}, indent=2)
            )]
    
    elif name == "text_analysis":
        text = arguments.get("text", "")
        
        try:
            # Basic text analysis
            words = text.split()
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            result = {
                "text": text,
                "statistics": {
                    "character_count": len(text),
                    "character_count_no_spaces": len(text.replace(" ", "")),
                    "word_count": len(words),
                    "sentence_count": len(sentences),
                    "paragraph_count": len([p for p in text.split('\n\n') if p.strip()]),
                    "avg_words_per_sentence": len(words) / max(len(sentences), 1),
                    "avg_chars_per_word": sum(len(word) for word in words) / max(len(words), 1)
                },
                "readability": {
                    "longest_word": max(words, key=len) if words else "",
                    "shortest_word": min(words, key=len) if words else "",
                    "unique_words": len(set(word.lower() for word in words))
                },
                "status": "success"
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=json.dumps({"error": str(e), "status": "error"}, indent=2)
            )]
    
    else:
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown tool: {name}", "status": "error"}, indent=2)
        )]

async def main():
    """Main entry point"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())