# *-* coding: utf-8 *-*
# src\__init__.py
# SHICTHRS JSON LOADER
# AUTHOR : SHICTHRS-JNTMTMTM
# Copyright : © 2025-2026 SHICTHRS, Std. All rights reserved.
# lICENSE : GPL-3.0

from colorama import init
init()

from pytz import UnknownTimeZoneError
from .utils.SHRTimer_get_system_time import get_system_time
from .utils.SHRTimer_get_time_stamp import get_time_stamp
from .utils.SHRTimer_get_pytz_time import get_pytz_time
from .utils.SHRTimer_get_is_within_hours import get_is_within_hours

print('\033[1mWelcome to use SHRTimer - time process system\033[0m\n|  \033[1;34mGithub : https://github.com/JNTMTMTM/SHICTHRS_Timer\033[0m')
print('|  \033[1mAlgorithms = rule ; Questioning = approval\033[0m')
print('|  \033[1mCopyright : © 2025-2026 SHICTHRS, Std. All rights reserved.\033[0m\n')

class SHRTimerException(Exception):
    def __init__(self , message: str) -> None:
        self.message = message
    
    def __str__(self):
        return self.message

FORMAT_TYPE_CPT : dict = {'0' : '%Y-%m-%d %H:%M:%S' ,
                            '1' : '%Y-%m-%d-%H-%M-%S' ,
                            '2' : '%Y%m%d%H%M%S'}

__all__ = ['SHRTimer_get_system_time' , 'SHRTimer_get_time_stamp' , 'SHRTimer_get_pytz_time']

def SHRTimer_get_system_time(format_type : str) -> str:
    try:
        if format_type not in list(FORMAT_TYPE_CPT.keys()):
            raise SHRTimerException('SHRTimer [ERROR.8000] format type is not supported')
        return get_system_time(FORMAT_TYPE_CPT[format_type])
    except Exception as e:
        raise SHRTimerException(f'SHRTimer [ERROR.8001] unable to get system time | {''.join(e.args)}')
    
def SHRTimer_get_time_stamp() -> float:
    try:
        return get_time_stamp()
    except Exception as e:
        raise SHRTimerException(f'SHRTimer [ERROR.8002] unable to get system time stamp | {''.join(e.args)}')
    
def SHRTimer_get_pytz_time(time_zone : str) -> str:
    try:
        return get_pytz_time(time_zone)
    
    except UnknownTimeZoneError as e:
        raise SHRTimerException(f'SHRTimer [ERROR.8003] time zone is not supported | {''.join(e.args)}')

    except Exception as e:
        raise SHRTimerException(f'SHRTimer [ERROR.8004] unable to get pytz time | {''.join(e.args)}')

def SHRTimer_get_is_within_hours(time_0 : str , time_1 : str , hour : int) -> bool:
    try:
        return get_is_within_hours(time_0 , time_1 , hour)

    except Exception as e:
        raise SHRTimerException(f'SHRTimer [ERROR.8005] unable to determine whether the two times fall within the time period | {''.join(e.args)}')