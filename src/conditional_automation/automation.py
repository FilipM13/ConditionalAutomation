from typing import Any, Optional
import re
from datetime import datetime, timedelta

from .conditions import Condition
from .process import Process

class Automation:
    
    def __init__(
            self,
            process: Process,
            time_frame: str,
            pre_conditions: Optional[list[Condition]] = None,
            post_conditions: Optional[list[Condition]] = None,
            name: Optional[str] = None
        ) -> None:
        sr = re.fullmatch(r'(?:([\d]+)?w)?(?:([\d]+)?d)?(?:([\d]+)?h)?(?:([\d]+)?m)?(?:([\d]+)?s)?', time_frame)
        assert sr
        # weeks
        _v = sr.group(1) if sr.group(1) else None
        weeks = int(_v) if _v else 0
        # days
        _v = sr.group(2) if sr.group(2) else None
        days = int(_v) if _v else 0
        # hours
        _v = sr.group(3) if sr.group(3) else None
        hours = int(_v) if _v else 0
        # minutes
        _v = sr.group(4) if sr.group(4) else None
        minutes = int(_v) if _v else 0
        # seconds
        _v = sr.group(5) if sr.group(5) else None
        seconds = int(_v) if _v else 0
        self.process = process  # function to run
        self.time_frame = timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)  # how often process should succeed
        self.pre_conditions: Optional[list[Condition]] = pre_conditions  # check before running [optional]
        self.post_conditions: Optional[list[Condition]] = post_conditions  # check after running [optional]
        self.name = name if name else process.function.__name__
        # background values
        self.__ts__ = datetime.now()
        self.__success__ = False
        pass
    
    def check_pre(self):
        pre_checks = dict()
        for i, con in enumerate(self.pre_conditions):
            i = con.name if con.name else i
            pre_checks[i] = con()
        return all(pre_checks.values())
    
    def check_post(self):
        post_checks = dict()
        for i, con in enumerate(self.post_conditions):
            i = con.name if con.name else i
            post_checks[i] = con()
        return all(post_checks.values())
    
    def __call__(self) -> Any:
        __time_delta__ = datetime.now() - self.__ts__
        if __time_delta__ > self.time_frame:
            print(f'[{datetime.now()}] {self.name}: Time frame breached! Resetting...')
            self.__success__ = False
            self.__ts__ = datetime.now()
        if not self.__success__:
            pre = self.check_pre() if self.pre_conditions else True  # check pre conditions
            if pre:  # if passed
                process = self.process()  # run process
                if process:  # if successful
                    post = self.check_post() if self.post_conditions else True  # check post conditions
                    if post:  # if passed
                        print(f'[{datetime.now()}] {self.name}: Success!')
                        self.__success__ = True
                    else:
                        print(f'[{datetime.now()}] {self.name}: Fail at post!')
                else:
                    print(f'[{datetime.now()}] {self.name}: Fail at process!')
            else:
                print(f'[{datetime.now()}] {self.name}: Fail at pre!')
        else:
            print(f'[{datetime.now()}] {self.name}: not running (already successful in current time frame)')
