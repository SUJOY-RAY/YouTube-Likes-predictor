def convert_likes(column: str):
    try:
        # Remove any whitespace and ensure it's a string
        column = str(column).strip()
        
        # Check if it ends with K, M, or B
        if column.endswith(('K', 'M', 'B')):
            value = float(column[:-1])  # Extract number part
            if column.endswith('K'):
                return value * 1_000  # Thousands
            elif column.endswith('M'):
                return value * 1_000_000  # Millions
            elif column.endswith('B'):
                return value * 1_000_000_000  # Billions
        else:
            # If no suffix, try to convert directly to float
            return float(column)
    except (ValueError, TypeError, IndexError) as e:
        # Return 0 for any parsing errors
        return 0