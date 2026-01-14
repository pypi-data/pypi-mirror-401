from .parser import parse_single_date
from .language import parse_language_date
from .ranges import parse_range

def parse_date(text, reference_date=None):
    return (
        parse_single_date(text)
        or parse_language_date(text)
    )

def parse_date_range(text, reference_date=None):
    return parse_range(text, reference_date)
