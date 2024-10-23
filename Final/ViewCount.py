import numpy as np

def convert_views(views_str):
    if 'K' in views_str:
        return int(float(views_str.replace('K', '').replace(',', '')) * 1000)
    elif 'M' in views_str:
        return int(float(views_str.replace('M', '').replace(',', '')) * 1000000)
    elif 'B' in views_str:
        return int(float(views_str.replace('B', '').replace(',', '')) * 1000000000)
    else:
        return int(views_str.replace(',', ''))
def convert_date(date_str):
    if 'hours' in date_str:
        return 1
    elif 'days' in date_str:
        days=int(date_str.split()[0])
        return days
    elif 'weeks' in date_str:
        weeks=int(date_str.split()[0])
        return weeks*7
    elif 'month' in date_str:
        days=int(date_str.split()[0])
        return days*30
    elif 'year' in date_str:
        years=int(date_str.split()[0])
        return years*365
    else:
        return np.nan