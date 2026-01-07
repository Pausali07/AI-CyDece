def assign_risk_score(features):
    """
    Assign a basic risk score based on extracted features.
    Returns a dictionary with level and reason.
    """

    if features.get("contains_http"):
        return {
            "risk_level": "medium",
            "reason": "HTTP-based interaction detected"
        }

    if features.get("automation_pattern"):
        return {
            "risk_level": "low",
            "reason": "Automated interaction pattern detected"
        }

    return {
        "risk_level": "unknown",
        "reason": "Insufficient indicators for classification"
    }
