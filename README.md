# Conditional Automation
Are you lazy programmer who wants to automate tasks but does not want to run them in specific time period if they succeed (yes, it's very specific)? Don't worry so am I. That's why I've spent couple of hours working on Conditional Automation, instead of running the code by myself (ugh) ad hoc.

### Basic Idea
1. Run the automation (check pre conditions [optional] -> run process -> check post conditions [optional]).
2. If succeeded, don't run it until specific time frame is breached.
3. If failed, try running it again after specific time period.
4. After time frame is breached go back to step 1.

## Building Blocks

### Automation
Setting up process, time frame and conditions. This is most important element. It will check if process was successful and if so, it will stop future execution in specified time frame. After that it will reset and run process (until success) again. Time from is specified by string containing number of weeks/days/hours/minutes/seconds, for example `1w2d3h4m8s`.

After initializing Automation, treat it as function in [schedule library](https://schedule.readthedocs.io/en/stable/).

### Process
Function executing main task.

Can use <b>Kwargs</b> (more on that later).

### Condition
Function returning True or False. It's supposed to check if everything for needed for process is in place (for example files in directory etc.) or if output if fine (for example check if output files were generated or not).

Can use <b>Kwargs</b> (more on that later).

### Kwargs in Process and Condition
Key word arguments can be used for functions is Process and Condition class. These can be specified as static values or dynamic values (additional functions running with no arguments). For example:
```python
# for this function:
def my_func(_now, some_text):
    pass
# kwargs can look like this:
kw = {
    "_now": datetime.now  # will execute this function each time automation is called
    "some_text": "this is text"  # this value will stay the same for each iteration
}
# combined into Process:
p = Process(
    function=my_func,
    kwargs=kw
)
# or into Condition: 
c = Condition(
    function=my_func,
    kwargs=kw
)
```

## Full Example
### Basic
Code:
```python
from conditional_automation import Automation, Process
import schedule

def my_process():
    # do stuff here
    pass

my_automation = Automation(
    process=Process(function=my_process),
    time_frame='2m',  # process should succeed once in every 2 minute window from starting time
)

schedule.every(20).seconds.do(my_automation)  # check Automation state every 2 seconds

while True:
    schedule.run_pending()
    time.sleep(1)  # check for pending jobs every second
```
Example print messages:
```
[2024-12-08 14:10:22.765113] my_process: Success!
[2024-12-08 14:10:42.882049] my_process: not running (already successful in current time frame)
[2024-12-08 14:11:02.970852] my_process: not running (already successful in current time frame)
[2024-12-08 14:11:23.091323] my_process: not running (already successful in current time frame)
[2024-12-08 14:11:43.195620] my_process: not running (already successful in current time frame)
[2024-12-08 14:12:03.265536] my_process: Time frame breached! Resetting...
[2024-12-08 14:12:03.265536] my_process: Success!
[2024-12-08 14:12:23.361370] my_process: not running (already successful in current time frame)
```

### Complex
code:
```python
from conditional_automation import Automation, Process, Condition
import schedule
from datetime import datetime
import random

def my_process(argument1):
    # do stuff here
    pass

def pre1(now_):
    return True

def post1():
    return random.choice([True, False])

my_automation = Automation(
    name="My Automation"
    process=Process(
        function=my_process, 
        kwargs={"argument1": "some text"}
    ),
    time_frame='1m20s',  # process should succeed once in every 2 minute window from starting time
    pre_conditions = [
        Condition(
            function=pre1,
            kwargs={"now_": datetime.now}
        )
    ],
    post_conditions = [
        Condition(
            function=post1,
        )
    ],
)

schedule.every(20).seconds.do(my_automation)  # check Automation state every 2 seconds

while True:
    schedule.run_pending()
    time.sleep(1)  # check for pending jobs every second
```
Example print messages:
```
[2024-12-08 14:46:30.519200] My Automation: Success!
[2024-12-08 14:46:50.620599] My Automation: not running (already successful in current time frame)
[2024-12-08 14:47:10.725353] My Automation: not running (already successful in current time frame)
[2024-12-08 14:47:30.857931] My Automation: not running (already successful in current time frame)
[2024-12-08 14:47:50.938669] My Automation: Time frame breached! Resetting...
[2024-12-08 14:47:50.938669] My Automation: Success!
[2024-12-08 14:48:11.056625] My Automation: not running (already successful in current time frame)
[2024-12-08 14:48:31.132945] My Automation: not running (already successful in current time frame)
[2024-12-08 14:48:51.252675] My Automation: not running (already successful in current time frame)
[2024-12-08 14:49:11.356413] My Automation: Time frame breached! Resetting...
[2024-12-08 14:49:11.356413] My Automation: Fail at post!
[2024-12-08 14:49:31.455280] My Automation: Success!
[2024-12-08 14:49:51.582683] My Automation: not running (already successful in current time frame)
```