"""MCP Server with basic tools for the chatbot"""
import os
import datetime
import json
import uuid
import hashlib
import random
import re
from typing import Any, Dict, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP
import httpx
import math

# Initialize FastAPI app
app = FastAPI(title="Chatbot MCP Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MCP server
mcp = FastMCP(name="chatbot-tools", version="1.0.0")

# Tool 1: Calculator
@mcp.tool()
async def calculator(expression: str) -> Dict[str, Any]:
    """
    Evaluate mathematical expressions safely.
    
    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 2", "sqrt(16)")
    
    Returns:
        Result of the calculation
    """
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

# Tool 2: Current datetime
@mcp.tool()
async def get_current_time(timezone: str = "UTC") -> Dict[str, str]:
    """
    Get the current date and time.
    
    Args:
        timezone: Timezone name (currently only supports UTC)
    
    Returns:
        Current date and time information
    """
    now = datetime.datetime.utcnow()
    
    return {
        "timezone": timezone,
        "datetime": now.isoformat(),
        "date": now.date().isoformat(),
        "time": now.time().isoformat(),
        "timestamp": now.timestamp()
    }

# Tool 3: Weather (mock implementation)
@mcp.tool()
async def get_weather(location: str) -> Dict[str, Any]:
    """
    Get weather information for a location (mock data for demo).
    
    Args:
        location: City name or location
    
    Returns:
        Weather information
    """
    # In a real implementation, this would call a weather API
    # For demo purposes, we'll return mock data
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

# Tool 4: Simple web search (using DuckDuckGo)
@mcp.tool()
async def web_search(query: str, max_results: int = 3) -> Dict[str, Any]:
    """
    Search the web for information.
    
    Args:
        query: Search query
        max_results: Maximum number of results to return
    
    Returns:
        Search results with titles and snippets
    """
    try:
        # Using DuckDuckGo HTML version for simplicity
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://html.duckduckgo.com/html/",
                params={"q": query},
                headers={"User-Agent": "Mozilla/5.0"}
            )
            
        # In a real implementation, parse the HTML properly
        # For demo, return mock results
        return {
            "success": True,
            "query": query,
            "results": [
                {
                    "title": f"Result 1 for {query}",
                    "snippet": f"This is a sample result about {query}...",
                    "url": "https://example.com/1"
                },
                {
                    "title": f"Result 2 for {query}",
                    "snippet": f"Another relevant result about {query}...",
                    "url": "https://example.com/2"
                }
            ][:max_results]
        }
    except Exception as e:
        return {
            "success": False,
            "query": query,
            "error": str(e)
        }

# Tool 5: Note taking
notes_storage = {}

# Storage for new project management tools
tasks_storage = {}
projects_storage = {}
reminders_storage = {}
templates_storage = {}
url_storage = {}
password_storage = {}

@mcp.tool()
async def save_note(title: str, content: str) -> Dict[str, Any]:
    """
    Save a note for later retrieval.
    
    Args:
        title: Note title
        content: Note content
    
    Returns:
        Confirmation of saved note
    """
    note_id = f"note_{len(notes_storage) + 1}"
    notes_storage[note_id] = {
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

@mcp.tool()
async def get_notes() -> Dict[str, Any]:
    """
    Retrieve all saved notes.
    
    Returns:
        List of all notes
    """
    return {
        "success": True,
        "notes": list(notes_storage.values()),
        "count": len(notes_storage)
    }

# ==== NEW PROJECT MANAGEMENT TOOLS ====

@mcp.tool()
async def create_task(title: str, description: str = "", priority: str = "medium", due_date: str = None) -> Dict[str, Any]:
    """
    Create a new task with title, description, priority, and optional due date.
    
    Args:
        title: Task title (required)
        description: Task description (optional)
        priority: Task priority (low, medium, high, urgent)
        due_date: Due date in YYYY-MM-DD format (optional)
    
    Returns:
        Created task information
    """
    try:
        task_id = str(uuid.uuid4())
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "priority": priority.lower(),
            "status": "todo",
            "due_date": due_date,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "updated_at": datetime.datetime.utcnow().isoformat()
        }
        
        tasks_storage[task_id] = task
        
        return {
            "success": True,
            "task": task,
            "message": f"Task '{title}' created successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def update_task_status(task_id: str, status: str) -> Dict[str, Any]:
    """
    Update task status.
    
    Args:
        task_id: Task ID
        status: New status (todo, in_progress, review, done, blocked)
    
    Returns:
        Updated task information
    """
    try:
        if task_id not in tasks_storage:
            return {
                "success": False,
                "error": "Task not found"
            }
        
        valid_statuses = ["todo", "in_progress", "review", "done", "blocked"]
        if status.lower() not in valid_statuses:
            return {
                "success": False,
                "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            }
        
        tasks_storage[task_id]["status"] = status.lower()
        tasks_storage[task_id]["updated_at"] = datetime.datetime.utcnow().isoformat()
        
        return {
            "success": True,
            "task": tasks_storage[task_id],
            "message": f"Task status updated to '{status}'"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def list_tasks(status: str = None, priority: str = None) -> Dict[str, Any]:
    """
    List tasks with optional filtering by status or priority.
    
    Args:
        status: Filter by status (optional)
        priority: Filter by priority (optional)
    
    Returns:
        List of tasks matching filters
    """
    try:
        tasks = list(tasks_storage.values())
        
        if status:
            tasks = [t for t in tasks if t["status"] == status.lower()]
        
        if priority:
            tasks = [t for t in tasks if t["priority"] == priority.lower()]
        
        # Sort by created_at (newest first)
        tasks.sort(key=lambda x: x["created_at"], reverse=True)
        
        return {
            "success": True,
            "tasks": tasks,
            "count": len(tasks),
            "filters": {"status": status, "priority": priority}
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def generate_password(length: int = 12, include_symbols: bool = True) -> Dict[str, Any]:
    """
    Generate a secure random password.
    
    Args:
        length: Password length (default 12, min 6, max 64)
        include_symbols: Include special characters (default True)
    
    Returns:
        Generated password and strength info
    """
    try:
        if length < 6 or length > 64:
            return {
                "success": False,
                "error": "Password length must be between 6 and 64 characters"
            }
        
        # Define character sets
        lowercase = "abcdefghijklmnopqrstuvwxyz"
        uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        digits = "0123456789"
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Build character pool
        chars = lowercase + uppercase + digits
        if include_symbols:
            chars += symbols
        
        # Generate password ensuring at least one from each category
        password = []
        password.append(random.choice(lowercase))
        password.append(random.choice(uppercase))
        password.append(random.choice(digits))
        
        if include_symbols:
            password.append(random.choice(symbols))
        
        # Fill remaining length with random characters
        for _ in range(length - len(password)):
            password.append(random.choice(chars))
        
        # Shuffle the password
        random.shuffle(password)
        final_password = ''.join(password)
        
        # Calculate strength
        strength_score = 0
        if len(final_password) >= 8:
            strength_score += 1
        if any(c.islower() for c in final_password):
            strength_score += 1
        if any(c.isupper() for c in final_password):
            strength_score += 1
        if any(c.isdigit() for c in final_password):
            strength_score += 1
        if any(c in symbols for c in final_password):
            strength_score += 1
        
        strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
        strength = strength_levels[min(strength_score, 4)]
        
        return {
            "success": True,
            "password": final_password,
            "length": len(final_password),
            "strength": strength,
            "includes_symbols": include_symbols
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def create_reminder(title: str, message: str, remind_at: str) -> Dict[str, Any]:
    """
    Create a reminder for a specific date/time.
    
    Args:
        title: Reminder title
        message: Reminder message
        remind_at: When to remind (YYYY-MM-DD HH:MM format)
    
    Returns:
        Created reminder information
    """
    try:
        # Validate date format
        try:
            remind_datetime = datetime.datetime.strptime(remind_at, "%Y-%m-%d %H:%M")
        except ValueError:
            return {
                "success": False,
                "error": "Invalid date format. Use YYYY-MM-DD HH:MM"
            }
        
        reminder_id = str(uuid.uuid4())
        reminder = {
            "id": reminder_id,
            "title": title,
            "message": message,
            "remind_at": remind_at,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "status": "active"
        }
        
        reminders_storage[reminder_id] = reminder
        
        return {
            "success": True,
            "reminder": reminder,
            "message": f"Reminder '{title}' set for {remind_at}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def check_reminders() -> Dict[str, Any]:
    """
    Check for any active reminders that are due.
    
    Returns:
        List of due reminders
    """
    try:
        now = datetime.datetime.utcnow()
        due_reminders = []
        
        for reminder_id, reminder in reminders_storage.items():
            if reminder["status"] == "active":
                remind_time = datetime.datetime.strptime(reminder["remind_at"], "%Y-%m-%d %H:%M")
                if remind_time <= now:
                    due_reminders.append(reminder)
                    # Mark as triggered
                    reminder["status"] = "triggered"
        
        return {
            "success": True,
            "due_reminders": due_reminders,
            "count": len(due_reminders)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def url_shortener(long_url: str, custom_alias: str = None) -> Dict[str, Any]:
    """
    Create a shortened URL with optional custom alias.
    
    Args:
        long_url: The URL to shorten
        custom_alias: Optional custom alias (default: random)
    
    Returns:
        Shortened URL information
    """
    try:
        # Validate URL
        if not (long_url.startswith("http://") or long_url.startswith("https://")):
            return {
                "success": False,
                "error": "URL must start with http:// or https://"
            }
        
        if custom_alias:
            # Check if alias already exists
            if any(data["alias"] == custom_alias for data in url_storage.values()):
                return {
                    "success": False,
                    "error": "Custom alias already exists"
                }
            alias = custom_alias
        else:
            # Generate random alias
            alias = hashlib.md5(long_url.encode()).hexdigest()[:8]
        
        url_id = str(uuid.uuid4())
        url_data = {
            "id": url_id,
            "long_url": long_url,
            "alias": alias,
            "short_url": f"short.ly/{alias}",
            "created_at": datetime.datetime.utcnow().isoformat(),
            "clicks": 0
        }
        
        url_storage[url_id] = url_data
        
        return {
            "success": True,
            "url_data": url_data,
            "message": f"URL shortened successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def text_analyzer(text: str) -> Dict[str, Any]:
    """
    Analyze text for various metrics like word count, reading time, etc.
    
    Args:
        text: Text to analyze
    
    Returns:
        Text analysis results
    """
    try:
        # Basic metrics
        char_count = len(text)
        char_count_no_spaces = len(text.replace(" ", ""))
        word_count = len(text.split())
        sentence_count = len([s for s in re.split(r'[.!?]+', text) if s.strip()])
        paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
        
        # Reading time (average 200 words per minute)
        reading_time_minutes = round(word_count / 200, 1)
        
        # Average word length
        words = text.split()
        avg_word_length = round(sum(len(word) for word in words) / len(words), 1) if words else 0
        
        # Most common words (excluding very short words)
        long_words = [word.lower().strip('.,!?";()') for word in words if len(word) > 3]
        word_freq = {}
        for word in long_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        most_common = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "success": True,
            "analysis": {
                "character_count": char_count,
                "character_count_no_spaces": char_count_no_spaces,
                "word_count": word_count,
                "sentence_count": sentence_count,
                "paragraph_count": paragraph_count,
                "reading_time_minutes": reading_time_minutes,
                "average_word_length": avg_word_length,
                "most_common_words": most_common
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def unit_converter(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """
    Convert between different units (length, weight, temperature).
    
    Args:
        value: Value to convert
        from_unit: Source unit
        to_unit: Target unit
    
    Returns:
        Conversion result
    """
    try:
        # Length conversions (to meters)
        length_units = {
            "mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
            "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.34
        }
        
        # Weight conversions (to grams)
        weight_units = {
            "mg": 0.001, "g": 1, "kg": 1000, "t": 1000000,
            "oz": 28.3495, "lb": 453.592
        }
        
        # Temperature conversion
        def convert_temperature(temp, from_t, to_t):
            # Convert to Celsius first
            if from_t == "f":
                celsius = (temp - 32) * 5/9
            elif from_t == "k":
                celsius = temp - 273.15
            else:  # celsius
                celsius = temp
            
            # Convert from Celsius to target
            if to_t == "f":
                return celsius * 9/5 + 32
            elif to_t == "k":
                return celsius + 273.15
            else:  # celsius
                return celsius
        
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        # Check if it's temperature conversion
        temp_units = ["c", "f", "k", "celsius", "fahrenheit", "kelvin"]
        if from_unit in temp_units and to_unit in temp_units:
            # Normalize temperature unit names
            from_t = from_unit[0] if len(from_unit) == 1 else from_unit[0]
            to_t = to_unit[0] if len(to_unit) == 1 else to_unit[0]
            
            result = convert_temperature(value, from_t, to_t)
            
            return {
                "success": True,
                "conversion": {
                    "original_value": value,
                    "original_unit": from_unit,
                    "converted_value": round(result, 4),
                    "converted_unit": to_unit,
                    "type": "temperature"
                }
            }
        
        # Check if it's length conversion
        elif from_unit in length_units and to_unit in length_units:
            meters = value * length_units[from_unit]
            result = meters / length_units[to_unit]
            
            return {
                "success": True,
                "conversion": {
                    "original_value": value,
                    "original_unit": from_unit,
                    "converted_value": round(result, 6),
                    "converted_unit": to_unit,
                    "type": "length"
                }
            }
        
        # Check if it's weight conversion
        elif from_unit in weight_units and to_unit in weight_units:
            grams = value * weight_units[from_unit]
            result = grams / weight_units[to_unit]
            
            return {
                "success": True,
                "conversion": {
                    "original_value": value,
                    "original_unit": from_unit,
                    "converted_value": round(result, 6),
                    "converted_unit": to_unit,
                    "type": "weight"
                }
            }
        
        else:
            return {
                "success": False,
                "error": f"Unsupported unit conversion from '{from_unit}' to '{to_unit}'"
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def base64_encode_decode(text: str, operation: str = "encode") -> Dict[str, Any]:
    """
    Encode or decode base64 text.
    
    Args:
        text: Text to encode/decode
        operation: "encode" or "decode"
    
    Returns:
        Encoded/decoded result
    """
    try:
        import base64
        
        if operation.lower() == "encode":
            encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            return {
                "success": True,
                "operation": "encode",
                "input": text,
                "output": encoded
            }
        elif operation.lower() == "decode":
            decoded = base64.b64decode(text.encode('utf-8')).decode('utf-8')
            return {
                "success": True,
                "operation": "decode",
                "input": text,
                "output": decoded
            }
        else:
            return {
                "success": False,
                "error": "Operation must be 'encode' or 'decode'"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ==== END NEW TOOLS ====

# Mount MCP endpoints to FastAPI
# Use SSE for Pydantic AI compatibility
app.mount("/sse", mcp.sse_app())
app.mount("/mcp", mcp.http_app())

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "mcp-server"}

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("MCP_SERVER_PORT", 8001))
    host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    
    print(f"Starting MCP server on {host}:{port}")
    print(f"MCP endpoint: http://{host}:{port}/mcp")
    
    uvicorn.run(app, host=host, port=port)