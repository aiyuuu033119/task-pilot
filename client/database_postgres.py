"""PostgreSQL database models and operations using SQLAlchemy"""
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional, AsyncGenerator
from contextlib import asynccontextmanager
import hashlib
import secrets

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, Text, ForeignKey, select, update, delete
from sqlalchemy.dialects.postgresql import UUID
import uuid

from config import config


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    display_name: Mapped[Optional[str]] = mapped_column(String(255))
    profile_picture: Mapped[Optional[str]] = mapped_column(String(500))
    job_title: Mapped[Optional[str]] = mapped_column(String(255))
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions: Mapped[List["UserSession"]] = relationship("UserSession", back_populates="user")
    chat_sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="user")


class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    session_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    refresh_token: Mapped[Optional[str]] = mapped_column(String(255), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_used_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="sessions")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class EmailVerificationToken(Base):
    __tablename__ = "email_verification_tokens"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="chat_sessions")
    messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="session")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(255), ForeignKey("chat_sessions.session_id"), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="messages")


class PostgreSQLDatabase:
    """PostgreSQL database operations using SQLAlchemy"""
    
    def __init__(self, database_url: str = None):
        self.database_url = database_url or config.DATABASE_URL
        # Convert SQLite URL to PostgreSQL if needed
        if self.database_url.startswith("sqlite"):
            self.database_url = "postgresql+asyncpg://user:password@localhost:5432/taskpilot"
        
        self.engine = create_async_engine(
            self.database_url,
            echo=False,  # Set to True for SQL debugging
            pool_pre_ping=True,
            pool_recycle=3600
        )
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)
    
    async def init_db(self):
        """Initialize database tables"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session context manager"""
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    # Chat Session Methods
    
    async def create_session(self, session_id: str, user_id: Optional[int] = None) -> None:
        """Create a new chat session"""
        async with self.get_session() as session:
            # Check if session already exists
            stmt = select(ChatSession).where(ChatSession.session_id == session_id)
            existing = await session.execute(stmt)
            if existing.scalar_one_or_none():
                return
                
            chat_session = ChatSession(session_id=session_id, user_id=user_id)
            session.add(chat_session)
    
    async def add_message(self, session_id: str, role: str, content: str) -> None:
        """Add a message to the chat history"""
        async with self.get_session() as session:
            # Ensure session exists
            stmt = select(ChatSession).where(ChatSession.session_id == session_id)
            chat_session = await session.execute(stmt)
            if not chat_session.scalar_one_or_none():
                await self.create_session(session_id)
            
            # Add message
            message = ChatMessage(session_id=session_id, role=role, content=content)
            session.add(message)
            
            # Update session timestamp
            stmt = (
                update(ChatSession)
                .where(ChatSession.session_id == session_id)
                .values(updated_at=datetime.utcnow())
            )
            await session.execute(stmt)
    
    async def get_session_messages(self, session_id: str, limit: int = 50) -> List[Dict[str, str]]:
        """Get messages for a session"""
        async with self.get_session() as session:
            stmt = (
                select(ChatMessage)
                .where(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.timestamp.desc())
                .limit(limit)
            )
            result = await session.execute(stmt)
            messages = result.scalars().all()
            
            # Return in chronological order
            return [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in reversed(messages)
            ]
    
    async def get_user_sessions(self, user_id: int) -> List[Dict[str, any]]:
        """Get all sessions for a user"""
        async with self.get_session() as session:
            stmt = (
                select(ChatSession)
                .where(ChatSession.user_id == user_id)
                .order_by(ChatSession.updated_at.desc())
            )
            result = await session.execute(stmt)
            sessions = result.scalars().all()
            
            return [
                {
                    "session_id": s.session_id,
                    "created_at": s.created_at.isoformat(),
                    "updated_at": s.updated_at.isoformat()
                }
                for s in sessions
            ]
    
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
        
        async with self.get_session() as session:
            try:
                user = User(
                    email=email,
                    password_hash=password_hash,
                    full_name=full_name,
                    display_name=display_name
                )
                session.add(user)
                await session.flush()  # Flush to get the ID
                return user.id
            except Exception:
                return None
    
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user with email and password"""
        async with self.get_session() as session:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if user and user.is_active and self._verify_password(password, user.password_hash):
                return {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "display_name": user.display_name,
                    "is_verified": user.is_verified
                }
            return None
    
    async def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        async with self.get_session() as session:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if user:
                return {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "display_name": user.display_name,
                    "profile_picture": user.profile_picture,
                    "job_title": user.job_title,
                    "timezone": user.timezone,
                    "is_active": user.is_active,
                    "is_verified": user.is_verified,
                    "created_at": user.created_at.isoformat(),
                    "updated_at": user.updated_at.isoformat()
                }
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        async with self.get_session() as session:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if user:
                return {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "display_name": user.display_name,
                    "profile_picture": user.profile_picture,
                    "job_title": user.job_title,
                    "timezone": user.timezone,
                    "is_active": user.is_active,
                    "is_verified": user.is_verified,
                    "created_at": user.created_at.isoformat(),
                    "updated_at": user.updated_at.isoformat()
                }
            return None
    
    async def update_user_profile(self, user_id: int, **kwargs) -> bool:
        """Update user profile information"""
        allowed_fields = {"full_name", "display_name", "profile_picture", "job_title", "timezone"}
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_fields:
            return False
        
        update_fields["updated_at"] = datetime.utcnow()
        
        async with self.get_session() as session:
            stmt = update(User).where(User.id == user_id).values(**update_fields)
            result = await session.execute(stmt)
            return result.rowcount > 0
    
    async def create_session_token(self, user_id: int, user_agent: str = None, ip_address: str = None) -> Dict[str, str]:
        """Create a new session token for user"""
        session_token = self._generate_token()
        refresh_token = self._generate_token()
        expires_at = datetime.utcnow() + timedelta(days=7)
        
        async with self.get_session() as session:
            user_session = UserSession(
                user_id=user_id,
                session_token=session_token,
                refresh_token=refresh_token,
                expires_at=expires_at,
                user_agent=user_agent,
                ip_address=ip_address
            )
            session.add(user_session)
        
        return {
            "session_token": session_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at.isoformat()
        }
    
    async def validate_session_token(self, session_token: str) -> Optional[int]:
        """Validate session token and return user_id if valid"""
        async with self.get_session() as session:
            stmt = (
                select(UserSession)
                .where(
                    UserSession.session_token == session_token,
                    UserSession.expires_at > datetime.utcnow(),
                    UserSession.is_active == True
                )
            )
            result = await session.execute(stmt)
            user_session = result.scalar_one_or_none()
            
            if user_session:
                # Update last_used_at
                stmt = (
                    update(UserSession)
                    .where(UserSession.session_token == session_token)
                    .values(last_used_at=datetime.utcnow())
                )
                await session.execute(stmt)
                return user_session.user_id
            return None
    
    async def invalidate_session(self, session_token: str) -> bool:
        """Invalidate a session token"""
        async with self.get_session() as session:
            stmt = (
                update(UserSession)
                .where(UserSession.session_token == session_token)
                .values(is_active=False)
            )
            result = await session.execute(stmt)
            return result.rowcount > 0
    
    async def create_password_reset_token(self, user_id: int) -> str:
        """Create password reset token"""
        token = self._generate_token()
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        async with self.get_session() as session:
            reset_token = PasswordResetToken(
                user_id=user_id,
                token=token,
                expires_at=expires_at
            )
            session.add(reset_token)
        
        return token
    
    async def validate_password_reset_token(self, token: str) -> Optional[int]:
        """Validate password reset token and return user_id if valid"""
        async with self.get_session() as session:
            stmt = (
                select(PasswordResetToken)
                .where(
                    PasswordResetToken.token == token,
                    PasswordResetToken.expires_at > datetime.utcnow(),
                    PasswordResetToken.used == False
                )
            )
            result = await session.execute(stmt)
            reset_token = result.scalar_one_or_none()
            
            if reset_token:
                # Mark token as used
                stmt = (
                    update(PasswordResetToken)
                    .where(PasswordResetToken.token == token)
                    .values(used=True)
                )
                await session.execute(stmt)
                return reset_token.user_id
            return None
    
    async def update_password(self, user_id: int, new_password: str) -> bool:
        """Update user password"""
        password_hash = self._hash_password(new_password)
        
        async with self.get_session() as session:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(password_hash=password_hash, updated_at=datetime.utcnow())
            )
            result = await session.execute(stmt)
            return result.rowcount > 0
    
    async def create_email_verification_token(self, user_id: int) -> str:
        """Create email verification token"""
        token = self._generate_token()
        expires_at = datetime.utcnow() + timedelta(days=7)
        
        async with self.get_session() as session:
            verification_token = EmailVerificationToken(
                user_id=user_id,
                token=token,
                expires_at=expires_at
            )
            session.add(verification_token)
        
        return token
    
    async def verify_email_token(self, token: str) -> bool:
        """Verify email verification token"""
        async with self.get_session() as session:
            stmt = (
                select(EmailVerificationToken)
                .where(
                    EmailVerificationToken.token == token,
                    EmailVerificationToken.expires_at > datetime.utcnow(),
                    EmailVerificationToken.used == False
                )
            )
            result = await session.execute(stmt)
            verification_token = result.scalar_one_or_none()
            
            if verification_token:
                user_id = verification_token.user_id
                # Mark token as used and user as verified
                stmt1 = (
                    update(EmailVerificationToken)
                    .where(EmailVerificationToken.token == token)
                    .values(used=True)
                )
                stmt2 = (
                    update(User)
                    .where(User.id == user_id)
                    .values(is_verified=True, updated_at=datetime.utcnow())
                )
                await session.execute(stmt1)
                await session.execute(stmt2)
                return True
            return False

    async def close(self):
        """Close database connection"""
        await self.engine.dispose()


# Create database instance
postgres_db = PostgreSQLDatabase()