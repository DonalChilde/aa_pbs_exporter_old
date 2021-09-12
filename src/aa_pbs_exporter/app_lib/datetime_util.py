from datetime import date, datetime


def string_to_date(date_string: str, strf: str) -> date:
    new_date = datetime.strptime(date_string, strf)
    return new_date.date()
