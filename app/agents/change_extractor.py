def extract_change(title, description):
    """
    OWNER: Tanish.  CONTRACT.
    Returns a dict following the extraction contract (spec section 11),
    or None if the LLM is unavailable (the caller then uses the fallback).
    """
    return None 