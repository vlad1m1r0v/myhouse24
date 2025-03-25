from datetime import date, timedelta


def get_last_12_months():
    today = date.today().replace(day=1)
    months = [(today - timedelta(days=30 * i)) for i in range(12)]
    return list(reversed(months))
