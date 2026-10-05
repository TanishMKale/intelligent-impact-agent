from app.services.scoring_service import calculate_score


def test_source_module_mapped_critical_app():
    result = calculate_score(True, 0, 0.0, "Critical")   # 35 + 25 + 10
    assert result["final_score"] == 70
    assert result["label"] == "High"


def test_depth1_mapped_high_app():
    result = calculate_score(True, 1, 0.0, "High")       # 35 + 18 + 7
    assert result["final_score"] == 60
    assert result["label"] == "High"


def test_semantic_only_suggestion():
    result = calculate_score(False, 1, 0.8, "Critical")  # 0 + 18 + 16 + 10
    assert result["final_score"] == 44
    assert result["label"] == "Medium"
    assert result["default_included"] is False


def test_outside_graph_unmapped_is_low():
    result = calculate_score(False, None, 0.1, "Medium") # 0 + 0 + 2 + 4
    assert result["label"] == "Low"
    assert result["recommendation"] == "Exclude by default"


def test_mapped_low_score_stays_visible():
    result = calculate_score(True, None, 0.0, "Low")      # 35 + 0 + 0 + 2
    assert result["label"] == "Low"
    assert "kept visible" in result["recommendation"]


def test_similarity_is_clamped():
    result = calculate_score(False, 0, 5.0, "Low")
    assert result["components"]["semantic"] == 20