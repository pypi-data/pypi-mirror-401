import re
from datetime import datetime
from .utils import normalize_separator

NUMERIC_PATTERNS = [
    r"\d{2}[-/.]\d{2}[-/.]\d{4}",
    r"\d{4}[-/.]\d{2}[-/.]\d{2}",
    r"\d{2}[-/.]\d{2}[-/.]\d{2}",
]

FORMATS = [
    "%d-%m-%Y", "%Y-%m-%d", "%d-%m-%y",
    "%d/%m/%Y", "%Y/%m/%d", "%d/%m/%y",
    "%d.%m.%Y", "%Y.%m.%d", "%d.%m.%y",
]

def parse_single_date(text: str):
    sep = normalize_separator(text)
    clean = re.search("|".join(NUMERIC_PATTERNS), sep)
    if clean:
        raw = clean.group()
        for fmt in FORMATS:
            try:
                dt = datetime.strptime(raw, fmt)
                return dt.strftime(fmt)   # OUTPUT SAME FORMAT
            except:
                pass
    return None
