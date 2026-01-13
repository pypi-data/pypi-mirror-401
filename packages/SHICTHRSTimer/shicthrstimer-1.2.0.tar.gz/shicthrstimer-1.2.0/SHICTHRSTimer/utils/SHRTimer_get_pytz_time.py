
from datetime import datetime
import pytz

def get_pytz_time(time_zone : str) -> str:
    tz = pytz.timezone(time_zone)
    return datetime.now(tz)
