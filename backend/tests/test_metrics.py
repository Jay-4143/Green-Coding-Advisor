"""
Unit tests for metrics endpoints
"""
import pytest
from fastapi import status


@pytest.mark.unit
class TestMetricsSummary:
    """Test metrics summary endpoint"""
    
    @pytest.mark.asyncio
    async def test_get_metrics_summary(self, client, auth_headers):
        """Test getting metrics summary"""
        response = await client.get("/metrics/summary", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_submissions" in data
        assert "average_green_score" in data
        assert "total_co2_saved" in data
        assert isinstance(data["total_submissions"], int)
        assert isinstance(data["average_green_score"], (int, float))


@pytest.mark.unit
class TestLeaderboard:
    """Test leaderboard endpoint"""
    
    @pytest.mark.asyncio
    async def test_get_leaderboard(self, client, auth_headers):
        """Test getting leaderboard"""
        response = await client.get("/metrics/leaderboard", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "entries" in data
        assert isinstance(data["entries"], list)
    
    @pytest.mark.asyncio
    async def test_get_leaderboard_timeframe(self, client, auth_headers):
        """Test leaderboard with different timeframes"""
        timeframes = ["week", "month", "all"]
        for timeframe in timeframes:
            response = await client.get(
                f"/metrics/leaderboard?timeframe={timeframe}",
                headers=auth_headers
            )
            assert response.status_code == status.HTTP_200_OK


@pytest.mark.unit
class TestLanguageStats:
    """Test language statistics endpoint"""
    
    @pytest.mark.asyncio
    async def test_get_language_stats(self, client, auth_headers):
        """Test getting language statistics"""
        response = await client.get("/metrics/language-stats", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "language_stats" in data
        assert isinstance(data["language_stats"], list)

