import re
from .parser import parse_single_date
from .relative import parse_relative

def parse_range(text):
    # relative range
    rel = parse_relative(text)
    if rel:
        return rel

    # between / from to
    m = re.search(r"(between|from)?\s*(.*?)\s*(to|-)\s*(.*)", text, re.I)
    if m:
        d1 = parse_single_date(m.group(2))
        d2 = parse_single_date(m.group(4))
        return d1, d2

    # two dates without keyword
    dates = re.findall(r"\d{2}[-/.]\d{2}[-/.]\d{2,4}", text)
    if len(dates) == 2:
        return parse_single_date(dates[0]), parse_single_date(dates[1])

    return None
