def convert_likes(column):
    if column.endswith('K'):
        return float(column[:-1]) * 1_000  
    elif column.endswith('M'):
        return float(column[:-1]) * 1_000_000  
    else:
        return float(column)  