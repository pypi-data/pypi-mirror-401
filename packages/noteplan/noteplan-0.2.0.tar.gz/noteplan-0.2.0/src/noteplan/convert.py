from datetime import datetime


def day(dt: datetime) -> str:
    return f"{dt.year:4}{dt.month:02}{dt.day:02}"


def week(dt: datetime) -> str:
    return f"{dt.year:4}-W{dt.isocalendar().week:02}"
