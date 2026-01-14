from datetime import date, timedelta

def normalize_separator(text):
    return text.replace("/", "-").replace(".", "-")

def week_range(which="this"):
    today = date.today()
    start = today - timedelta(days=today.weekday())
    if which == "last":
        start -= timedelta(weeks=1)
    end = start + timedelta(days=6)
    return start, end
