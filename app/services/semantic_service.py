def search_similar_test_cases(query_text, application_ids, top_k=10, min_similarity=0.3):
    """
    OWNER: Bhavesh.  CONTRACT (do not change without telling the team).
    Returns a list of dicts, best match first:
      {"test_case_id": "TC-CBS-003", "similarity": 0.82, "matched_fields": ["scenario"]}
    similarity is 0.0 to 1.0. Only IDs that exist in the test_case table.
    """
    return []


def reindex_all_test_cases():
    """OWNER: Bhavesh. Rebuilds the vector index. Returns {"indexed": N}."""
    return {"indexed": 0}