import json
from pathlib import Path
from typing import Dict, Any

def load_question_model(path: str = "config/questions.json") -> Dict[str, Any]:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data