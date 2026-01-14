from datetime import date, timedelta
import re

def parse_relative(text, reference_date=None):
    t = text.lower()
    today = reference_date or date.today()

    # single day
    if "day before yesterday" in t:
        d = today - timedelta(days=2)
        return d.strftime("%Y-%m-%d"), d.strftime("%Y-%m-%d")

    if "yesterday" in t:
        d = today - timedelta(days=1)
        return d.strftime("%Y-%m-%d"), d.strftime("%Y-%m-%d")

    if "today" in t:
        return today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

    # weeks
    if "last week" in t:
        start = today - timedelta(days=7)
        end = today - timedelta(days=1)
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


    if "this week" in t:
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

    # N weeks before / after
    m = re.search(r"(\d+)\s+weeks?\s+(before|after)", t)
    if m:
        n, mode = int(m.group(1)), m.group(2)
        d = today - timedelta(weeks=n) if mode == "before" else today + timedelta(weeks=n)
        s = d.strftime("%Y-%m-%d")
        return s, s

    return None
