from difflib import get_close_matches
from app.utils.synonyms import FEATURE_SYNONYMS
from app.utils.normalizer import normalize_column

def smart_match_columns(csv_columns, model_features):
    
    # normalize incoming CSV columns
    normalized_cols = {normalize_column(col): col for col in csv_columns}

    mapping = {}
    used_columns = set()

    for feature in model_features:
        best_match = None

        # STEP 1: synonym match
        synonyms = FEATURE_SYNONYMS.get(feature, [])

        for col_norm, original_col in normalized_cols.items():
            if col_norm in synonyms:
                best_match = original_col
                break

        # STEP 2: fuzzy match if no synonym match
        if not best_match:
            matches = get_close_matches(feature, normalized_cols.keys(), n=1, cutoff=0.6)
            if matches:
                best_match = normalized_cols[matches[0]]

        # STEP 3: assign mapping
        if best_match and best_match not in used_columns:
            mapping[feature] = best_match
            used_columns.add(best_match)
        else:
            mapping[feature] = None

    return mapping