from app.config import settings


def get_label(score):
    if score >= 80:
        return "Critical"
    if score >= 60:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"


def get_recommendation(label, has_traceability):
    if label == "Critical":
        return "Mandatory review / include by default"
    if label == "High":
        return "Include by default"
    if label == "Medium":
        return "Reviewer decision"
    # Low
    if has_traceability:
        # spec rule: explicit traceability must stay visible even if score is low
        return "Reviewer decision (explicitly mapped, kept visible)"
    return "Exclude by default"


def calculate_score(has_traceability, dependency_depth, semantic_similarity,
                    criticality, defect_severity=None):
    """
    has_traceability     : True if TC is mapped to an impacted requirement
    dependency_depth     : 0 = source module, 1 = depth-1, 2 = depth-2, None = outside graph
    semantic_similarity  : number from 0.0 to 1.0 (use 0.0 if no semantic match)
    criticality          : "Critical" / "High" / "Medium" / "Low" (application criticality)
    defect_severity      : "High" / "Medium" / None
    """
    # 1. traceability
    if has_traceability:
        trace_points = settings.TRACEABILITY_POINTS
    else:
        trace_points = 0

    # 2. dependency proximity
    if dependency_depth is None:
        dep_points = 0
    else:
        dep_points = settings.DEPENDENCY_POINTS.get(dependency_depth, 0)

    # 3. semantic similarity (keep it between 0 and 1)
    similarity = max(0.0, min(1.0, semantic_similarity))
    semantic_points = similarity * settings.SEMANTIC_MAX_POINTS

    # 4. criticality
    crit_points = settings.CRITICALITY_POINTS.get(criticality, 0)

    # 5. defect history
    defect_points = settings.DEFECT_POINTS.get(defect_severity, 0)

    final_score = round(
        trace_points + dep_points + semantic_points + crit_points + defect_points, 1
    )
    label = get_label(final_score)

    return {
        "components": {
            "traceability": trace_points,
            "dependency": dep_points,
            "semantic": round(semantic_points, 1),
            "criticality": crit_points,
            "defect": defect_points,
        },
        "final_score": final_score,
        "label": label,
        "recommendation": get_recommendation(label, has_traceability),
        "default_included": label in ("Critical", "High"),
    }