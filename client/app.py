"""FastAPI backend for the chatbot"""
import os
import uuid
from datetime import datetime
from typing import Optional, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr

from conversation_agent import get_conversation_agent as get_agent, ChatContext
from database import ChatDatabase
from config import config

# Initialize database
db = ChatDatabase()

# Security
security = HTTPBearer()

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.init_db()
    agent = await get_agent()
    async with agent:
        yield
    # Shutdown

# Initialize FastAPI app
app = FastAPI(
    title="Pydantic AI MCP Chatbot",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str

class SessionInfo(BaseModel):
    session_id: str
    created_at: str
    updated_at: str
    message_count: int

# Authentication models
class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    display_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    display_name: Optional[str]
    profile_picture: Optional[str]
    job_title: Optional[str]
    timezone: str
    is_verified: bool
    created_at: str
    updated_at: str

class AuthResponse(BaseModel):
    user: UserProfile
    session_token: str
    refresh_token: str
    expires_at: str

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    display_name: Optional[str] = None
    profile_picture: Optional[str] = None
    job_title: Optional[str] = None
    timezone: Optional[str] = None

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

# Authentication dependencies
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[dict]:
    """Get current authenticated user from session token"""
    try:
        session_token = credentials.credentials
        user_id = await db.validate_session_token(session_token)
        
        if user_id:
            user = await db.get_user_by_id(user_id)
            return user
        return None
    except Exception:
        return None

async def require_auth(user: dict = Depends(get_current_user)) -> dict:
    """Require authentication for protected endpoints"""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

# API Routes
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Pydantic AI Chat API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message"""
    try:
        # Generate IDs if not provided
        session_id = request.session_id or str(uuid.uuid4())
        user_id = request.user_id or "anonymous"
        
        # Create session if new
        await db.create_session(session_id, user_id)
        
        # Save user message
        await db.add_message(session_id, "user", request.message)
        
        # Get chat history
        history = await db.get_session_messages(session_id)
        
        # Debug: Print history length
        print(f"Debug: Retrieved {len(history)} messages for session {session_id}")
        
        # Create context
        context = ChatContext(
            user_id=user_id,
            session_id=session_id,
            message_history=history
        )
        
        # Get response from agent
        agent = await get_agent()
        response = await agent.chat(request.message, context)
        
        # Save assistant response
        await db.add_message(session_id, "assistant", response)
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for streaming chat"""
    await websocket.accept()
    print(f"WebSocket connected for session: {session_id}")
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            message = data.get("message", "")
            user_id = data.get("user_id", "anonymous")
            
            print(f"WebSocket received message: {message[:50]}...")
            
            # Create session if new
            await db.create_session(session_id, user_id)
            
            # Save user message
            await db.add_message(session_id, "user", message)
            
            # Get chat history
            history = await db.get_session_messages(session_id)
            print(f"WebSocket: Retrieved {len(history)} messages for context")
            
            # Create context
            context = ChatContext(
                user_id=user_id,
                session_id=session_id,
                message_history=history
            )
            
            # Send typing indicator
            await websocket.send_json({
                "type": "typing",
                "content": ""
            })
            
            # Stream response
            agent = await get_agent()
            full_response = ""
            
            async for chunk in agent.stream_chat(message, context):
                full_response += chunk
                await websocket.send_json({
                    "type": "stream",
                    "content": chunk
                })
            
            # Save complete response
            await db.add_message(session_id, "assistant", full_response)
            
            # Send completion signal
            await websocket.send_json({
                "type": "complete",
                "content": full_response
            })
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session: {session_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "content": str(e)
            })
        except:
            pass

@app.get("/api/sessions/{user_id}", response_model=List[SessionInfo])
async def get_user_sessions(user_id: str):
    """Get all chat sessions for a user"""
    try:
        sessions = await db.get_user_sessions(user_id)
        
        # Add message count for each session
        session_info = []
        for session in sessions:
            messages = await db.get_session_messages(session["session_id"])
            session_info.append(
                SessionInfo(
                    session_id=session["session_id"],
                    created_at=session["created_at"],
                    updated_at=session["updated_at"],
                    message_count=len(messages)
                )
            )
        
        return session_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/session/{session_id}/history")
async def get_session_history(session_id: str):
    """Get chat history for a session"""
    try:
        messages = await db.get_session_messages(session_id)
        return {"session_id": session_id, "messages": messages}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Authentication endpoints
@app.post("/api/auth/register", response_model=AuthResponse)
async def register(user_data: UserRegistration):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = await db.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user
        user_id = await db.create_user(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            display_name=user_data.display_name
        )
        
        if not user_id:
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        # Get user data
        user = await db.get_user_by_id(user_id)
        
        # Create session token
        session_data = await db.create_session_token(user_id)
        
        # Create email verification token
        verification_token = await db.create_email_verification_token(user_id)
        
        return AuthResponse(
            user=UserProfile(**user),
            session_token=session_data["session_token"],
            refresh_token=session_data["refresh_token"],
            expires_at=session_data["expires_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/login", response_model=AuthResponse)
async def login(login_data: UserLogin):
    """Login user"""
    try:
        # Authenticate user
        user_data = await db.authenticate_user(login_data.email, login_data.password)
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create session token
        session_data = await db.create_session_token(user_data["id"])
        
        # Get full user profile
        user = await db.get_user_by_id(user_data["id"])
        
        return AuthResponse(
            user=UserProfile(**user),
            session_token=session_data["session_token"],
            refresh_token=session_data["refresh_token"],
            expires_at=session_data["expires_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/logout")
async def logout(user: dict = Depends(require_auth), credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout user by invalidating session token"""
    try:
        session_token = credentials.credentials
        success = await db.invalidate_session(session_token)
        
        return {"message": "Logged out successfully", "success": success}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/auth/me", response_model=UserProfile)
async def get_current_user_profile(user: dict = Depends(require_auth)):
    """Get current user profile"""
    return UserProfile(**user)

@app.put("/api/auth/profile", response_model=UserProfile)
async def update_profile(profile_data: ProfileUpdate, user: dict = Depends(require_auth)):
    """Update user profile"""
    try:
        update_data = {k: v for k, v in profile_data.dict().items() if v is not None}
        
        if update_data:
            success = await db.update_user_profile(user["id"], **update_data)
            if not success:
                raise HTTPException(status_code=400, detail="No fields to update")
        
        # Return updated user profile
        updated_user = await db.get_user_by_id(user["id"])
        return UserProfile(**updated_user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/password-reset")
async def request_password_reset(reset_data: PasswordReset):
    """Request password reset"""
    try:
        user = await db.get_user_by_email(reset_data.email)
        if not user:
            # Don't reveal if email exists for security
            return {"message": "If the email exists, a reset link has been sent"}
        
        # Create reset token
        reset_token = await db.create_password_reset_token(user["id"])
        
        # In a real app, you would send this token via email
        # For now, just return success message
        return {"message": "Password reset token created", "token": reset_token}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/password-reset/confirm")
async def confirm_password_reset(reset_data: PasswordResetConfirm):
    """Confirm password reset with token"""
    try:
        user_id = await db.validate_password_reset_token(reset_data.token)
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid or expired token")
        
        # Update password
        success = await db.update_password(user_id, reset_data.new_password)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update password")
        
        return {"message": "Password updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/verify-email")
async def verify_email(token: str):
    """Verify email with token"""
    try:
        success = await db.verify_email_token(token)
        if not success:
            raise HTTPException(status_code=400, detail="Invalid or expired token")
        
        return {"message": "Email verified successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "chatbot-backend"}

if __name__ == "__main__":
    import uvicorn
    
    print(f"Starting chatbot backend on {config.APP_HOST}:{config.APP_PORT}")
    uvicorn.run(
        "client.app:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True
    )