def extract_behavior_features(session):
    """
    Extract lightweight behavioral features from a session.
    No packet-level inspection is performed.
    """

    features = {}

    # Duration feature
    if session.get("start_time") and session.get("end_time"):
        features["static_duration"] = session["start_time"] == session["end_time"]

    # Protocol hint from filename
    features["contains_http"] = "http" in session.get("reference", "").lower()

    # Automation hint
    features["automation_pattern"] = "capture" in session.get("reference", "").lower()

    return features
