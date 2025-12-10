"""
Unit tests for code submission endpoints
"""
import pytest
from fastapi import status


@pytest.mark.unit
class TestCreateSubmission:
    """Test code submission creation"""
    
    @pytest.mark.asyncio
    async def test_create_submission_success(self, client, auth_headers):
        """Test successful code submission"""
        response = await client.post(
            "/submissions",
            headers=auth_headers,
            json={
                "code_content": "def hello(): return 'world'",
                "language": "python",
                "filename": "test.py"
            }
        )
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
        data = response.json()
        assert data["language"] == "python"
        assert data["filename"] == "test.py"
        assert "id" in data
    
    @pytest.mark.asyncio
    async def test_create_submission_unauthorized(self, client):
        """Test submission without authentication"""
        response = await client.post(
            "/submissions",
            json={
                "code_content": "def hello(): return 'world'",
                "language": "python"
            }
        )
        # FastAPI returns 403 for missing auth, which is acceptable
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


@pytest.mark.unit
class TestAnalyzeCode:
    """Test code analysis endpoint"""
    
    @pytest.mark.asyncio
    async def test_analyze_code_success(self, client, auth_headers):
        """Test successful code analysis"""
        response = await client.post(
            "/submissions/analyze",
            headers=auth_headers,
            json={
                "code": "def sum_numbers(numbers): return sum(numbers)",
                "language": "python"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "green_score" in data
        assert "energy_consumption_wh" in data
        assert "co2_emissions_g" in data
        assert "suggestions" in data
        assert isinstance(data["green_score"], (int, float))
        assert 0 <= data["green_score"] <= 100
    
    @pytest.mark.asyncio
    async def test_analyze_code_multiple_languages(self, client, auth_headers):
        """Test code analysis for different languages"""
        languages = ["python", "javascript", "java", "cpp"]
        
        for lang in languages:
            response = await client.post(
                "/submissions/analyze",
                headers=auth_headers,
                json={
                    "code": "function test() { return 1; }" if lang == "javascript" else "def test(): return 1",
                    "language": lang
                }
            )
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "green_score" in data


@pytest.mark.integration
class TestSubmissionWorkflow:
    """Test complete submission workflow"""
    
    @pytest.mark.asyncio
    async def test_submit_and_analyze_workflow(self, client, auth_headers):
        """Test complete workflow: create submission -> analyze"""
        # Create submission
        create_response = await client.post(
            "/submissions",
            headers=auth_headers,
            json={
                "code_content": "def efficient_sum(numbers): return sum(numbers)",
                "language": "python",
                "filename": "efficient.py"
            }
        )
        assert create_response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
        submission_id = create_response.json()["id"]
        
        # Analyze submission
        analyze_response = await client.post(
            f"/submissions/{submission_id}/analyze",
            headers=auth_headers
        )
        assert analyze_response.status_code == status.HTTP_200_OK
        data = analyze_response.json()
        assert "green_score" in data
        assert data["green_score"] > 0

