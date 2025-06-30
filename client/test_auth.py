#!/usr/bin/env python3
"""Test script for authentication system"""

import asyncio
import aiosqlite
from database import ChatDatabase

async def test_auth_system():
    """Test the authentication system"""
    print("Testing Authentication System...")
    
    # Initialize database
    db = ChatDatabase()
    await db.init_db()
    
    # Test user creation
    print("\n1. Testing user creation...")
    user_id = await db.create_user(
        email="test@example.com",
        password="testpassword123",
        full_name="Test User",
        display_name="Tester"
    )
    print(f"Created user with ID: {user_id}")
    
    # Test duplicate email
    print("\n2. Testing duplicate email...")
    duplicate_user = await db.create_user(
        email="test@example.com",
        password="another_password"
    )
    print(f"Duplicate user creation result: {duplicate_user}")
    
    # Test authentication
    print("\n3. Testing authentication...")
    auth_result = await db.authenticate_user("test@example.com", "testpassword123")
    print(f"Authentication successful: {auth_result}")
    
    # Test wrong password
    print("\n4. Testing wrong password...")
    wrong_auth = await db.authenticate_user("test@example.com", "wrongpassword")
    print(f"Wrong password authentication: {wrong_auth}")
    
    # Test session token creation
    print("\n5. Testing session token creation...")
    if user_id:
        session_data = await db.create_session_token(user_id, "test-user-agent", "127.0.0.1")
        print(f"Session token created: {session_data['session_token'][:20]}...")
        
        # Test token validation
        print("\n6. Testing token validation...")
        validated_user_id = await db.validate_session_token(session_data['session_token'])
        print(f"Token validation result: {validated_user_id}")
        
        # Test token invalidation
        print("\n7. Testing token invalidation...")
        invalidated = await db.invalidate_session(session_data['session_token'])
        print(f"Token invalidated: {invalidated}")
        
        # Test invalidated token
        print("\n8. Testing invalidated token...")
        invalid_validation = await db.validate_session_token(session_data['session_token'])
        print(f"Invalidated token validation: {invalid_validation}")
    
    # Test password reset
    print("\n9. Testing password reset...")
    if user_id:
        reset_token = await db.create_password_reset_token(user_id)
        print(f"Password reset token created: {reset_token[:20]}...")
        
        # Test reset token validation
        print("\n10. Testing reset token validation...")
        reset_user_id = await db.validate_password_reset_token(reset_token)
        print(f"Reset token validation: {reset_user_id}")
        
        # Test password update
        print("\n11. Testing password update...")
        password_updated = await db.update_password(user_id, "newpassword123")
        print(f"Password updated: {password_updated}")
        
        # Test login with new password
        print("\n12. Testing login with new password...")
        new_auth = await db.authenticate_user("test@example.com", "newpassword123")
        print(f"New password authentication: {new_auth}")
    
    # Test user profile operations
    print("\n13. Testing profile operations...")
    if user_id:
        # Get user profile
        user_profile = await db.get_user_by_id(user_id)
        print(f"User profile: {user_profile}")
        
        # Update profile
        profile_updated = await db.update_user_profile(
            user_id,
            job_title="Software Engineer",
            timezone="America/New_York"
        )
        print(f"Profile updated: {profile_updated}")
        
        # Get updated profile
        updated_profile = await db.get_user_by_id(user_id)
        print(f"Updated profile: {updated_profile}")
    
    # Test email verification
    print("\n14. Testing email verification...")
    if user_id:
        verification_token = await db.create_email_verification_token(user_id)
        print(f"Verification token created: {verification_token[:20]}...")
        
        # Verify email
        verified = await db.verify_email_token(verification_token)
        print(f"Email verified: {verified}")
        
        # Check verification status
        verified_user = await db.get_user_by_id(user_id)
        print(f"User verification status: {verified_user['is_verified']}")
    
    print("\n✅ Authentication system test completed!")

if __name__ == "__main__":
    asyncio.run(test_auth_system())