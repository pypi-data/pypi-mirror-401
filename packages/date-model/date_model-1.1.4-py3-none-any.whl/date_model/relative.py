from datetime import date, timedelta
from calendar import monthrange
import re


def parse_relative(text, reference_date=None):
    t = text.lower()
    today = reference_date or date.today()

    # ---- single days ----
    if "day before yesterday" in t:
        d = today - timedelta(days=2)
        return d.strftime("%Y-%m-%d"), d.strftime("%Y-%m-%d")

    if "yesterday" in t:
        d = today - timedelta(days=1)
        return d.strftime("%Y-%m-%d"), d.strftime("%Y-%m-%d")

    if "today" in t:
        return today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

    if "tomorrow" in t:
        d = today + timedelta(days=1)
        return d.strftime("%Y-%m-%d"), d.strftime("%Y-%m-%d")

    # ---- rolling weeks ----
    if "last week" in t:
        s = today - timedelta(days=7)
        e = today - timedelta(days=1)
        return s.strftime("%Y-%m-%d"), e.strftime("%Y-%m-%d")

    if "this week" in t:
        s = today - timedelta(days=today.weekday())
        e = s + timedelta(days=6)
        return s.strftime("%Y-%m-%d"), e.strftime("%Y-%m-%d")

    # ---- weekday queries ----
    weekdays = {
        "monday": 0, "tuesday": 1, "wednesday": 2,
        "thursday": 3, "friday": 4,
        "saturday": 5, "sunday": 6
    }

    for w, idx in weekdays.items():
        if w in t and "week" in t:
            start = today - timedelta(days=today.weekday())
            d = start + timedelta(days=idx)
            return d.strftime("%Y-%m-%d"), d.strftime("%Y-%m-%d")

    # ---- N weeks before/after ----
    m = re.search(r"(\d+)\s+weeks?\s+(before|after)", t)
    if m:
        n, mode = int(m.group(1)), m.group(2)
        d = today - timedelta(weeks=n) if mode == "before" else today + timedelta(weeks=n)
        s = d.strftime("%Y-%m-%d")
        return s, s

    # ---- month relative ----
    if "this month" in t or "last month" in t or "next month" in t:
        y, m = today.year, today.month

        if "last month" in t:
            m -= 1
            if m == 0:
                m = 12
                y -= 1

        if "next month" in t:
            m += 1
            if m == 13:
                m = 1
                y += 1

        start = date(y, m, 1)
        end = date(y, m, monthrange(y, m)[1])
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

    return None
