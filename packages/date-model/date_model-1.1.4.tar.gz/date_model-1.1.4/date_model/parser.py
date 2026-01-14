import re
from datetime import datetime

def parse_single_date(text: str):
    text = text.strip()

    patterns = [
        "%d-%m-%Y", "%Y-%m-%d",
        "%d/%m/%Y", "%Y/%m/%d",
        "%d.%m.%Y", "%Y.%m.%d",
        "%d-%m-%y", "%d/%m/%y", "%d.%m.%y",
    ]

    for fmt in patterns:
        try:
            d = datetime.strptime(text, fmt)

            # ✅ FIX: convert 2-digit year → 4-digit
            if d.year < 100:
                d = d.replace(year=2000 + d.year)

            return d.strftime("%Y-%m-%d")
        except:
            continue

    return None
