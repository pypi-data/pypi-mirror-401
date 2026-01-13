
import time

def get_system_time(format : str) -> str:
    current_time = time.localtime()
    formatted_time = time.strftime(format , current_time)
    return formatted_time