def llm_analyze(features):
    if features.get("automation_pattern"):
        return "This session indicates automated scanning behavior, suggesting low-risk reconnaissance activity."
    elif features.get("contains_http"):
        return "This session shows protocol-specific interaction, indicating targeted probing behavior."
    else:
        return "This session lacks strong indicators and may represent benign or inconclusive activity."
