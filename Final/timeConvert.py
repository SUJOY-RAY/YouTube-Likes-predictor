import datetime
def date_convert(date_string, date_format="%b %d, %Y"):
    try:
        given_date = datetime.datetime.strptime(date_string, date_format)
        today = datetime.datetime.today()
        delta = today-given_date
        return delta.days
    except Exception as e:
        return f"Error: {e}"