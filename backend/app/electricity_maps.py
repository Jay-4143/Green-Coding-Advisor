"""
Electricity Maps API integration (lightweight helper).

Fetches live carbon intensity (gCO2eq/kWh) for a given zone. Falls back to a
static average when API key is missing or the request fails.
"""
from typing import Optional
import requests

from .config import settings
from .logger import green_logger

# Map broad regions to Electricity Maps zones
REGION_TO_ZONE = {
    "usa": "US",  # USA average
    "us": "US",
    "north_america": "US",
    "europe": "DE",  # Germany as a representative EU zone
    "asia": "IN-WB",  # West Bengal as a conservative, higher-intensity example
    "world": "US",
}


def get_live_emission_factor(region: str) -> Optional[float]:
    """
    Return live carbon intensity in gCO2/kWh for the given region using Electricity Maps.
    If unavailable, returns None (caller should fall back to defaults).
    """
    api_key = settings.electricity_maps_api_key
    if not api_key:
        return None

    zone = REGION_TO_ZONE.get(region.lower(), "US")
    url = f"https://api.electricitymap.org/v3/carbon-intensity/latest?zone={zone}"

    try:
        resp = requests.get(url, headers={"auth-token": api_key}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        value = data.get("carbonIntensity")
        if isinstance(value, (int, float)) and value > 0:
            return float(value)
    except Exception as exc:  # pragma: no cover - network variability
        if green_logger:
            green_logger.logger.warning(f"ElectricityMaps fetch failed for {zone}: {exc}")

    return None

