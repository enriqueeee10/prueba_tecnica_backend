from httpx import AsyncClient
import pytest
import pytest_asyncio


class TestUserAPI:
    @pytest.mark.asyncio
    async def test_create_user_success(self, test_client: AsyncClient):
        """Test successful user creation via API"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
        }

        response = await test_client.post("/api/v1/users/", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert "user_id" in data
        assert data["message"] == "User created successfully"

    @pytest.mark.asyncio
    async def test_create_user_invalid_email(self, test_client: AsyncClient):
        """Test user creation with invalid email"""
        user_data = {
            "name": "John Doe",
            "email": "invalid-email",
            "password": "password123",
        }

        response = await test_client.post("/api/v1/users/", json=user_data)

        assert response.status_code == 422  # FastAPI validation error

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, test_client: AsyncClient):
        """Test getting non-existent user"""
        user_id = "non-existent-id"

        response = await test_client.get(f"/api/v1/users/{user_id}")

        assert response.status_code == 404
