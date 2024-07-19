def convert_into_date(date):
    try:
        converted_date = datetime.strptime(date, '%Y-%m-%d').date()
        return converted_date.strftime('%Y-%m-%d')
    except ValueError:
        return None