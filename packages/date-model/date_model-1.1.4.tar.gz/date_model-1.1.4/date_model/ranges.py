import re
from datetime import date, timedelta
from calendar import monthrange

from .parser import parse_single_date
from .language import parse_language_date
from .relative import parse_relative


def smart_date(t):
    return parse_single_date(t) or parse_language_date(t)


def parse_year_only(text):
    m = re.fullmatch(r"\s*(\d{2}|\d{4})\s*", text)
    if not m:
        return None

    y = int(m.group(1))
    if y < 100:
        y = 2000 + y

    return f"{y}-01-01", f"{y}-12-31"


def parse_month_year(text):
    t = text.lower()
    month_map = {
        "jan": 1, "january": 1,
        "feb": 2, "february": 2,
        "mar": 3, "march": 3,
        "apr": 4, "april": 4,
        "may": 5,
        "jun": 6, "june": 6,
        "jul": 7, "july": 7,
        "aug": 8, "august": 8,
        "sep": 9, "september": 9,
        "oct": 10, "october": 10,
        "nov": 11, "november": 11,
        "dec": 12, "december": 12,
    }

    for k, m in month_map.items():
        if k in t:
            y = re.search(r"(20\d{2}|\d{2})", t)
            if not y:
                return None
            y = int(y.group())
            if y < 100:
                y = 2000 + y

            start = date(y, m, 1)
            end = date(y, m, monthrange(y, m)[1])
            return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

    return None


def parse_week_of_month(text, reference_date):
    t = text.lower()
    y, m = reference_date.year, reference_date.month

    first = date(y, m, 1)
    last = date(y, m, monthrange(y, m)[1])

    if "first week" in t:
        return first.strftime("%Y-%m-%d"), (first + timedelta(days=6)).strftime("%Y-%m-%d")

    if "second week" in t:
        s = first + timedelta(days=7)
        return s.strftime("%Y-%m-%d"), (s + timedelta(days=6)).strftime("%Y-%m-%d")

    if "mid week" in t:
        s = first + timedelta(days=14)
        return s.strftime("%Y-%m-%d"), (s + timedelta(days=6)).strftime("%Y-%m-%d")

    if "last week" in t and "this week" not in t:
        s = last - timedelta(days=6)
        return s.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d")

    return None


def parse_range(text, reference_date=None):
    reference_date = reference_date or date.today()

    # 1️⃣ relative (today, yesterday, last week, N weeks before/after)
    r = parse_relative(text, reference_date)
    if r:
        return r

    # 2️⃣ explicit between / from-to (all numeric formats)
    m = re.search(
        r"(between|from)?\s*([\w./-]+)\s*(to|and)\s*([\w./-]+)",
        text, re.I
    )
    if m:
        d1, d2 = smart_date(m.group(2)), smart_date(m.group(4))
        if d1 and d2:
            return d1, d2

    # 3️⃣ implicit two dates anywhere
    all_dates = re.findall(r"\d{1,4}[./-]\d{1,2}[./-]\d{2,4}", text)
    if len(all_dates) == 2:
        d1, d2 = smart_date(all_dates[0]), smart_date(all_dates[1])
        if d1 and d2:
            return d1, d2

    # 4️⃣ year-only
    y = parse_year_only(text.strip())
    if y:
        return y

    # 5️⃣ month + year
    m = parse_month_year(text)
    if m:
        return m

    # 6️⃣ week-of-month
    wom = parse_week_of_month(text, reference_date)
    if wom:
        return wom

    return None
