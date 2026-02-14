from typing import List, Dict

DIMENSION_LEVELS = {
    (0, 1.5): "Initial",
    (1.5, 2.5): "Emerging",
    (2.5, 3.5): "Defined",
    (3.5, 4.5): "Managed",
    (4.5, 5.1): "Optimized",
}

def calculate_scores(answers: List[Dict]) -> Dict:
    # answers: [{dimension, question, answer(int 1–5)}]
    for a in answers:
        a["score"] = float(a["answer"])

    if not answers:
        return {"overall_score": 0.0, "maturity_level": "N/A"}

    overall = sum(a["score"] for a in answers) / len(answers)
    level = "N/A"
    for (low, high), name in DIMENSION_LEVELS.items():
        if low <= overall < high:
            level = name
            break

    return {
        "overall_score": round(overall, 2),
        "maturity_level": level,
    }