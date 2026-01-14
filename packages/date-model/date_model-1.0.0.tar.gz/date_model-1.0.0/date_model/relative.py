from datetime import date, timedelta
import re

def parse_relative(text):
    today = date.today()
    t = text.lower()

    if "today" in t:
        return today, today

    if "yesterday" in t:
        d = today - timedelta(days=1)
        return d, d

    if "day before yesterday" in t:
        d = today - timedelta(days=2)
        return d, d

    m = re.search(r"(\d+)\s+weeks?\s+(before|after)", t)
    if m:
        n, mode = int(m.group(1)), m.group(2)
        delta = timedelta(weeks=n)
        d = today - delta if mode == "before" else today + delta
        return d, d

    m = re.search(r"(\d+)\s+months?\s+(before|after)", t)
    if m:
        n, mode = int(m.group(1)), m.group(2)
        d = today.replace(month=today.month - n if mode=="before" else today.month + n)
        return d, d

    return None
