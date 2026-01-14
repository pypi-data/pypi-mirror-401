import re
from .parser import parse_single_date
from .language import parse_language_date
from .relative import parse_relative

def smart_date(t):
    return parse_single_date(t) or parse_language_date(t)

def parse_range(text, reference_date=None):
    # relative first
    r = parse_relative(text, reference_date)
    if r:
        return r

    # between / from-to
    m = re.search(
        r"(between|from)?\s*(\d{2}[-/.]\d{2}[-/.]\d{2,4})\s*(to|and)\s*(\d{2}[-/.]\d{2}[-/.]\d{2,4})",
        text, re.I
    )
    if m:
        return smart_date(m.group(2)), smart_date(m.group(4))

    # implicit range
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", text)
    if len(dates) == 2:
        return dates[0], dates[1]

    return None
