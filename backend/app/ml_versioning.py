"""
Lightweight model versioning helper.
Stores metadata for trained models in backend/app/models/versions.json.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

MODELS_DIR = Path(__file__).resolve().parent / "models"
VERSIONS_FILE = MODELS_DIR / "versions.json"


def record_model_version(name: str, metrics: Dict[str, Any]) -> None:
    VERSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if VERSIONS_FILE.exists():
        try:
            existing = json.loads(VERSIONS_FILE.read_text())
        except Exception:
            existing = {}

    entry = {
        "name": name,
        "metrics": metrics,
        "recorded_at": datetime.utcnow().isoformat(),
    }
    existing[name] = entry
    VERSIONS_FILE.write_text(json.dumps(existing, indent=2))

