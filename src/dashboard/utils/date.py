from datetime import date
from dateutil.relativedelta import relativedelta

def get_last_12_months():
    today = date.today().replace(day=1)
    months = [(today - relativedelta(months=i)) for i in range(12)]
    return list(reversed(months))