from datetime import datetime

today = datetime.now()
current_year = today.year

start_date = datetime(current_year, 12, 15)
end_date = datetime(current_year, 12, 25)


def is_yalda():
    return start_date <= today <= end_date