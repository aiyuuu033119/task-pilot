"""Database models and operations for chat history and user authentication"""
import aiosqlite
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from config import config

class ChatDatabase:
    """Handle chat history storage"""
    
    def __init__(self, db_path: str = config.DATABASE_URL.replace("sqlite:///", "")):
        self.db_path = db_path
    
    async def init_db(self):
        """Initialize database tables"""
        async with aiosqlite.connect(self.db_path) as db:
            # User authentication tables
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT,
                    display_name TEXT,
                    profile_picture TEXT,
                    job_title TEXT,
                    timezone TEXT DEFAULT 'UTC',
                    is_active BOOLEAN DEFAULT 1,
                    is_verified BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token TEXT UNIQUE NOT NULL,
                    refresh_token TEXT UNIQUE,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_agent TEXT,
                    ip_address TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS password_reset_tokens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    token TEXT UNIQUE NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    used BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS email_verification_tokens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    token TEXT UNIQUE NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    used BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            # Chat history tables
            await db.execute("""
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    user_id TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id)
                )
            """)
            
            await db.commit()
    
    async def create_session(self, session_id: str, user_id: str) -> None:
        """Create a new chat session"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO chat_sessions (session_id, user_id) VALUES (?, ?)",
                (session_id, user_id)
            )
            await db.commit()
    
    async def add_message(self, session_id: str, role: str, content: str) -> None:
        """Add a message to the chat history"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO chat_messages (session_id, role, content) VALUES (?, ?, ?)",
                (session_id, role, content)
            )
            
            # Update session timestamp
            await db.execute(
                "UPDATE chat_sessions SET updated_at = CURRENT_TIMESTAMP WHERE session_id = ?",
                (session_id,)
            )
            
            await db.commit()
    
    async def get_session_messages(self, session_id: str, limit: int = 50) -> List[Dict[str, str]]:
        """Get messages for a session"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT role, content, timestamp 
                FROM chat_messages 
                WHERE session_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
                """,
                (session_id, limit)
            )
            
            rows = await cursor.fetchall()
            
            # Return in chronological order
            messages = [
                {
                    "role": row["role"],
                    "content": row["content"],
                    "timestamp": row["timestamp"]
                }
                for row in reversed(rows)
            ]
            
            return messages
    
    async def get_user_sessions(self, user_id: str) -> List[Dict[str, any]]:
        """Get all sessions for a user"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT session_id, created_at, updated_at
                FROM chat_sessions
                WHERE user_id = ?
                ORDER BY updated_at DESC
                """,
                (user_id,)
            )
            
            rows = await cursor.fetchall()
            
            sessions = [
                {
                    "session_id": row["session_id"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"]
                }
                for row in rows
            ]
            
            return sessions
    
    # User Authentication Methods
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"
    
    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password against stored hash"""
        try:
            salt, hash_value = stored_hash.split(":")
            password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return password_hash == hash_value
        except ValueError:
            return False
    
    def _generate_token(self) -> str:
        """Generate secure random token"""
        return secrets.token_urlsafe(32)
    
    async def create_user(self, email: str, password: str, full_name: str = None, display_name: str = None) -> Optional[int]:
        """Create a new user account"""
        password_hash = self._hash_password(password)
        
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute(
                    """
                    INSERT INTO users (email, password_hash, full_name, display_name)
                    VALUES (?, ?, ?, ?)
                    """,
                    (email, password_hash, full_name, display_name)
                )
                await db.commit()
                return cursor.lastrowid
            except aiosqlite.IntegrityError:
                # Email already exists
                return None
    
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user with email and password"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT id, email, password_hash, full_name, display_name, is_active, is_verified FROM users WHERE email = ?",
                (email,)
            )
            user = await cursor.fetchone()
            
            if user and user["is_active"] and self._verify_password(password, user["password_hash"]):
                return {
                    "id": user["id"],
                    "email": user["email"],
                    "full_name": user["full_name"],
                    "display_name": user["display_name"],
                    "is_verified": user["is_verified"]
                }
            return None
    
    async def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT id, email, full_name, display_name, profile_picture, 
                       job_title, timezone, is_active, is_verified, created_at, updated_at
                FROM users WHERE id = ?
                """,
                (user_id,)
            )
            user = await cursor.fetchone()
            
            if user:
                return dict(user)
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT id, email, full_name, display_name, profile_picture, 
                       job_title, timezone, is_active, is_verified, created_at, updated_at
                FROM users WHERE email = ?
                """,
                (email,)
            )
            user = await cursor.fetchone()
            
            if user:
                return dict(user)
            return None
    
    async def update_user_profile(self, user_id: int, **kwargs) -> bool:
        """Update user profile information"""
        allowed_fields = {"full_name", "display_name", "profile_picture", "job_title", "timezone"}
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_fields:
            return False
        
        set_clause = ", ".join([f"{field} = ?" for field in update_fields])
        values = list(update_fields.values()) + [user_id]
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                f"UPDATE users SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                values
            )
            await db.commit()
            return True
    
    async def create_session_token(self, user_id: int, user_agent: str = None, ip_address: str = None) -> Dict[str, str]:
        """Create a new session token for user"""
        session_token = self._generate_token()
        refresh_token = self._generate_token()
        expires_at = datetime.utcnow() + timedelta(days=7)  # Token valid for 7 days
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO user_sessions (user_id, session_token, refresh_token, expires_at, user_agent, ip_address)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, session_token, refresh_token, expires_at, user_agent, ip_address)
            )
            await db.commit()
        
        return {
            "session_token": session_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at.isoformat()
        }
    
    async def validate_session_token(self, session_token: str) -> Optional[int]:
        """Validate session token and return user_id if valid"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                SELECT user_id FROM user_sessions 
                WHERE session_token = ? AND expires_at > CURRENT_TIMESTAMP AND is_active = 1
                """,
                (session_token,)
            )
            result = await cursor.fetchone()
            
            if result:
                # Update last_used_at
                await db.execute(
                    "UPDATE user_sessions SET last_used_at = CURRENT_TIMESTAMP WHERE session_token = ?",
                    (session_token,)
                )
                await db.commit()
                return result[0]
            return None
    
    async def invalidate_session(self, session_token: str) -> bool:
        """Invalidate a session token"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "UPDATE user_sessions SET is_active = 0 WHERE session_token = ?",
                (session_token,)
            )
            await db.commit()
            return cursor.rowcount > 0
    
    async def create_password_reset_token(self, user_id: int) -> str:
        """Create password reset token"""
        token = self._generate_token()
        expires_at = datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (?, ?, ?)",
                (user_id, token, expires_at)
            )
            await db.commit()
        
        return token
    
    async def validate_password_reset_token(self, token: str) -> Optional[int]:
        """Validate password reset token and return user_id if valid"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                SELECT user_id FROM password_reset_tokens 
                WHERE token = ? AND expires_at > CURRENT_TIMESTAMP AND used = 0
                """,
                (token,)
            )
            result = await cursor.fetchone()
            
            if result:
                # Mark token as used
                await db.execute(
                    "UPDATE password_reset_tokens SET used = 1 WHERE token = ?",
                    (token,)
                )
                await db.commit()
                return result[0]
            return None
    
    async def update_password(self, user_id: int, new_password: str) -> bool:
        """Update user password"""
        password_hash = self._hash_password(new_password)
        
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (password_hash, user_id)
            )
            await db.commit()
            return cursor.rowcount > 0
    
    async def create_email_verification_token(self, user_id: int) -> str:
        """Create email verification token"""
        token = self._generate_token()
        expires_at = datetime.utcnow() + timedelta(days=7)  # Token valid for 7 days
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO email_verification_tokens (user_id, token, expires_at) VALUES (?, ?, ?)",
                (user_id, token, expires_at)
            )
            await db.commit()
        
        return token
    
    async def verify_email_token(self, token: str) -> bool:
        """Verify email verification token"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                SELECT user_id FROM email_verification_tokens 
                WHERE token = ? AND expires_at > CURRENT_TIMESTAMP AND used = 0
                """,
                (token,)
            )
            result = await cursor.fetchone()
            
            if result:
                user_id = result[0]
                # Mark token as used and user as verified
                await db.execute(
                    "UPDATE email_verification_tokens SET used = 1 WHERE token = ?",
                    (token,)
                )
                await db.execute(
                    "UPDATE users SET is_verified = 1, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (user_id,)
                )
                await db.commit()
                return True
            return False