
from datetime import datetime

def get_is_within_hours(time_str1 : str , time_str2 : str , hours_threshold : int):
    formats = [
        "%Y/%m/%d %H:%M:%S", 
        "%Y-%m-%d %H:%M:%S"
    ]
    
    dt1 = None
    for fmt in formats:
        try:
            dt1 = datetime.strptime(time_str1, fmt)
            break
        except ValueError:
            continue
    
    dt2 = None
    for fmt in formats:
        try:
            dt2 = datetime.strptime(time_str2, fmt)
            break
        except ValueError:
            continue
    
    time_difference = abs((dt1 - dt2).total_seconds())
    return (time_difference / 3600) <= hours_threshold