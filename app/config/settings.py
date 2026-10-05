# Scoring weights (POC defaults from the spec). Change here, not in logic code.

TRACEABILITY_POINTS = 35

# key = dependency depth. 0 means the source module itself.
DEPENDENCY_POINTS = {0: 25, 1: 18, 2: 10}

SEMANTIC_MAX_POINTS = 20

CRITICALITY_POINTS = {"Critical": 10, "High": 7, "Medium": 4, "Low": 2}

# defect severity -> points (anything else = 0)
DEFECT_POINTS = {"High": 10, "Medium": 5}
