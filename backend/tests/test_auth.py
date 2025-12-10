"""
Unit tests for authentication endpoints
"""
import pytest
from fastapi import status


@pytest.mark.unit
class TestSignup:
    """Test user signup endpoint"""
    
    @pytest.mark.asyncio
    async def test_signup_success(self, client):
        """Test successful user signup"""
        response = await client.post(
            "/auth/signup",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "NewUser@1234",
                "role": "developer"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert "id" in data
    
    @pytest.mark.asyncio
    async def test_signup_duplicate_email(self, client, test_user):
        """Test signup with duplicate email"""
        response = await client.post(
            "/auth/signup",
            json={
                "email": test_user["email"],
                "username": "differentuser",
                "password": "Test@1234"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @pytest.mark.asyncio
    async def test_signup_weak_password(self, client):
        """Test signup with weak password"""
        response = await client.post(
            "/auth/signup",
            json={
                "email": "user@example.com",
                "username": "user",
                "password": "weak"
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.unit
class TestLogin:
    """Test user login endpoint"""
    
    @pytest.mark.asyncio
    async def test_login_success(self, client, test_user):
        """Test successful login"""
        response = await client.post(
            "/auth/login",
            json={
                "email": test_user["email"],
                "password": "Test@1234"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, client, test_user):
        """Test login with invalid password"""
        response = await client.post(
            "/auth/login",
            json={
                "email": test_user["email"],
                "password": "WrongPassword@123"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = await client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "Test@1234"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.unit
class TestGetCurrentUser:
    """Test get current user endpoint"""
    
    @pytest.mark.asyncio
    async def test_get_current_user_success(self, client, auth_headers):
        """Test getting current user info"""
        response = await client.get("/auth/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "email" in data
        assert "username" in data
        assert "id" in data
    
    @pytest.mark.asyncio
    async def test_get_current_user_unauthorized(self, client):
        """Test getting current user without authentication"""
        response = await client.get("/auth/me")
        # FastAPI returns 403 for missing auth, which is acceptable
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

