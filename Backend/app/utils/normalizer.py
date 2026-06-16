import re

def normalize_column(col):
    col = col.lower().strip()
    col = re.sub(r"[^a-z0-9_ ]", "", col)
    col = col.replace(" ", "_")
    return col