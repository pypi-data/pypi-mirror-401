from .parser import parse_single_date
from .language import parse_language_date
from .ranges import parse_range
from datetime import datetime

def to_iso(d):
    if not d:
        return None
    try:
        return datetime.strptime(d, "%Y-%m-%d").strftime("%Y-%m-%d")
    except:
        try:
            return datetime.strptime(d, "%d-%m-%Y").strftime("%Y-%m-%d")
        except:
            try:
                return datetime.strptime(d, "%d %b %Y").strftime("%Y-%m-%d")
            except:
                try:
                    return datetime.strptime(d, "%d %B %Y").strftime("%Y-%m-%d")
                except:
                    return None


def parse_date(text, reference_date=None):
    d = parse_single_date(text) or parse_language_date(text)
    return to_iso(d)


def parse_date_range(text, reference_date=None):
    r = parse_range(text, reference_date)
    if not r:
        return None
    s, e = r
    return to_iso(s), to_iso(e)
