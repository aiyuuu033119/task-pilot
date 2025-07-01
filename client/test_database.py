#!/usr/bin/env python3
"""Test script to verify database connection and basic operations"""
import asyncio
import sys
from pathlib import Path

# Add the client directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from database_factory import db
from config import config


async def test_database():
    """Test database connection and basic operations"""
    print(f"Testing database connection...")
    print(f"Database URL: {config.DATABASE_URL}")
    print(f"Database type: {'PostgreSQL' if config.DATABASE_URL.startswith('postgresql') else 'SQLite'}")
    
    try:
        # Initialize database
        print("\n1. Initializing database...")
        await db.init_db()
        print("✓ Database initialized successfully")
        
        # Test user creation
        print("\n2. Testing user creation...")
        user_id = await db.create_user(
            email="test@example.com",
            password="testpassword123",
            full_name="Test User",
            display_name="Tester"
        )
        
        if user_id:
            print(f"✓ User created successfully with ID: {user_id}")
        else:
            print("✗ Failed to create user")
            return False
        
        # Test user authentication
        print("\n3. Testing user authentication...")
        auth_result = await db.authenticate_user("test@example.com", "testpassword123")
        
        if auth_result:
            print(f"✓ User authenticated successfully: {auth_result['email']}")
        else:
            print("✗ User authentication failed")
            return False
        
        # Test session creation
        print("\n4. Testing chat session...")
        session_id = "test-session-123"
        await db.create_session(session_id, str(user_id))
        print(f"✓ Chat session created: {session_id}")
        
        # Test message storage
        print("\n5. Testing message storage...")
        await db.add_message(session_id, "user", "Hello, this is a test message!")
        await db.add_message(session_id, "assistant", "Hello! I received your test message.")
        print("✓ Messages stored successfully")
        
        # Test message retrieval
        print("\n6. Testing message retrieval...")
        messages = await db.get_session_messages(session_id)
        print(f"✓ Retrieved {len(messages)} messages:")
        for msg in messages:
            print(f"  - {msg['role']}: {msg['content'][:50]}...")
        
        # Test session token creation
        print("\n7. Testing session tokens...")
        session_data = await db.create_session_token(user_id)
        print(f"✓ Session token created (expires: {session_data['expires_at']})")
        
        # Test session token validation
        token = session_data['session_token']
        validated_user_id = await db.validate_session_token(token)
        
        if validated_user_id == user_id:
            print("✓ Session token validation successful")
        else:
            print("✗ Session token validation failed")
            return False
        
        print("\n🎉 All database tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Close database connection if it's PostgreSQL
        if hasattr(db, 'close'):
            await db.close()


async def main():
    """Main test function"""
    print("=== Database Connection Test ===")
    success = await test_database()
    
    if success:
        print("\n✅ Database is ready to use!")
        return 0
    else:
        print("\n❌ Database test failed!")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)