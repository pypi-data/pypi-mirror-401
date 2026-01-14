import re
from datetime import datetime

MONTHS = {
    "jan": "January", "january": "January",
    "feb": "February", "february": "February",
}

def parse_language_date(text):
    text = text.lower()

    pattern = r"(\d{1,2})(st|nd|rd|th)?\s+(jan|january)\s+(\d{2,4})"
    m = re.search(pattern, text)
    if m:
        day, _, mon, year = m.groups()
        year = "20" + year if len(year) == 2 else year
        dt = datetime.strptime(f"{day} {MONTHS[mon]} {year}", "%d %B %Y")
        return dt.strftime(f"{day} %b {year}")
    return None
