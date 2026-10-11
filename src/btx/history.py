import json
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path.home() / ".btx_history.json"


def save_engineering_snapshot(knowledge: dict):
    """
    Save an engineering snapshot.
    """

    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "project": knowledge.get("project_name", "Unknown"),
        "health_score": knowledge.get(
            "engineering_health_score",
            "Unknown",
        ),
        "maturity": knowledge.get(
            "engineering_maturity",
            "Unknown",
        ),
        "risk": knowledge.get(
            "risk_level",
            "Unknown",
        ),
    }

    history = []

    if HISTORY_FILE.exists():
        history = json.loads(HISTORY_FILE.read_text())

    history.append(snapshot)

    HISTORY_FILE.write_text(json.dumps(history, indent=4))
