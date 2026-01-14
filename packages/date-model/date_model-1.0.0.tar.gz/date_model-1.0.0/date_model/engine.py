from .parser import parse_single_date
from .ranges import parse_range

def parse_date(text: str):
    """
    Input → single date
    Output → same format as input
    """
    return parse_single_date(text)

def parse_date_range(text: str):
    """
    Input → date range text
    Output → (start_date, end_date) in same input style
    """
    return parse_range(text)
