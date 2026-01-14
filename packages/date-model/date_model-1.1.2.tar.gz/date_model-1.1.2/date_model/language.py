import re
from datetime import datetime

MONTHS = {
    "jan": "January", "january": "January",
    "feb": "February", "february": "February",
    "mar": "March", "march": "March",
    "apr": "April", "april": "April",
    "may": "May",
    "jun": "June", "june": "June",
    "jul": "July", "july": "July",
    "aug": "August", "august": "August",
    "sep": "September", "september": "September",
    "oct": "October", "october": "October",
    "nov": "November", "november": "November",
    "dec": "December", "december": "December",
}

def parse_language_date(text):
    text = text.lower()

    # 2nd jan 2025 / 2 january 25
    m = re.search(r"(\d{1,2})(st|nd|rd|th)?\s+(jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october|nov|november|dec|december)\s+(\d{2,4})", text)
    if m:
        day, _, mon, year = m.groups()
        year = "20" + year if len(year) == 2 else year
        dt = datetime.strptime(f"{day} {MONTHS[mon]} {year}", "%d %B %Y")
        return dt.strftime(f"{day} %b {year}")

    # jan 2 2025
    m = re.search(r"(jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october|nov|november|dec|december)\s+(\d{1,2})\s+(\d{2,4})", text)
    if m:
        mon, day, year = m.groups()
        year = "20" + year if len(year) == 2 else year
        dt = datetime.strptime(f"{day} {MONTHS[mon]} {year}", "%d %B %Y")
        return dt.strftime(f"{day} %b {year}")

    return None
