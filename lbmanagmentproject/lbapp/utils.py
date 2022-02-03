from datetime import datetime, timedelta


def get_due_date():
    return datetime.today().date() + timedelta(days=30)