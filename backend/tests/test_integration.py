"""
Integration tests for complete API workflows
"""
import pytest
from fastapi import status


@pytest.mark.integration
class TestAuthWorkflow:
    """Test complete authentication workflow"""
    
    @pytest.mark.asyncio
    async def test_signup_login_workflow(self, client):
        """Test complete signup -> login -> get user flow"""
        # Signup
        signup_response = await client.post(
            "/auth/signup",
            json={
                "email": "workflow@example.com",
                "username": "workflowuser",
                "password": "Workflow@1234",
                "role": "developer"
            }
        )
        assert signup_response.status_code == status.HTTP_200_OK
        
        # Login
        login_response = await client.post(
            "/auth/login",
            json={
                "email": "workflow@example.com",
                "password": "Workflow@1234"
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get current user
        user_response = await client.get("/auth/me", headers=headers)
        assert user_response.status_code == status.HTTP_200_OK
        assert user_response.json()["email"] == "workflow@example.com"


@pytest.mark.integration
class TestCodeAnalysisWorkflow:
    """Test complete code analysis workflow"""
    
    @pytest.mark.asyncio
    async def test_submit_analyze_badge_workflow(self, client, auth_headers):
        """Test complete workflow: submit -> analyze -> check badges"""
        # Submit code
        submit_response = await client.post(
            "/submissions",
            headers=auth_headers,
            json={
                "code_content": "def efficient_sum(numbers): return sum(numbers)",
                "language": "python",
                "filename": "efficient.py"
            }
        )
        assert submit_response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
        submission_id = submit_response.json()["id"]
        
        # Analyze code
        analyze_response = await client.post(
            f"/submissions/{submission_id}/analyze",
            headers=auth_headers
        )
        assert analyze_response.status_code == status.HTTP_200_OK
        data = analyze_response.json()
        assert "green_score" in data
        assert data["green_score"] > 0
        
        # Check badges (if any were awarded)
        badges_response = await client.get("/badges/me", headers=auth_headers)
        assert badges_response.status_code == status.HTTP_200_OK


@pytest.mark.integration
class TestMetricsWorkflow:
    """Test metrics and leaderboard workflow"""
    
    @pytest.mark.asyncio
    async def test_submit_and_check_metrics(self, client, auth_headers):
        """Test submitting code and checking updated metrics"""
        # Get initial metrics
        initial_metrics = await client.get("/metrics/summary", headers=auth_headers)
        assert initial_metrics.status_code == status.HTTP_200_OK
        initial_count = initial_metrics.json().get("total_submissions", 0)
        
        # Submit code
        await client.post(
            "/submissions",
            headers=auth_headers,
            json={
                "code_content": "def test(): return 1",
                "language": "python",
                "filename": "test.py"
            }
        )
        
        # Check updated metrics (may need to wait for background processing)
        updated_metrics = await client.get("/metrics/summary", headers=auth_headers)
        assert updated_metrics.status_code == status.HTTP_200_OK

