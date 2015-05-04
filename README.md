### Welcome to 'Red' Alert

This is a notification system built for the Power BI Team @ Microsoft. The main contoller runs on the raspberry pi. Some parts of the system work in conjuntion with special hardware. An example is the NeoPixel class which uses an XBee to comunicate light sequences to arduinos connected with neopixel strips.

Setting this up on a raspberry pi is simple, just copy and run setup.py as follows :-

```
sudo python3 setup.py
```

This will enlist/install all the required libraries and folder structures. Depending on the hooks required, you might need to create options.csv in /var/www/tmp, and fill as shown

```
slack_token,your_token
vso_password,your_password
buildbroken,False
gmail_username,your_username
gmail_password,your_password
vso_username,your_username
weather_key,your_api_id
```

In addition, you will also need to create a cronjob to execute runner.py every minute.

### ITask
ITasks are extensible units of the system. It is a script that when run preforms a specific operation. An example is the weather task, which checks the weather in Redmond, and posts it to the timeline. The tasks's __run__(self, time) method takes in a time parameter which can be used to control when a task is run, since the runner will launch all tasks every minute. 

A sample implementation of a task looks like this :-

```
from common import ITask

class MyTask(ITask):
    def __init__(self):
        pass

    def __run__(self, time):
        if time['hour'] == '12' and time['min'] == '00':
            print('Wooo its 12pm!')
```

Once you create a new task, remember to add it to the runner.py, so the runner can launch it.

### Authors and Contributors
Sachin Patney

### Support
Part of the Power BI team? Having trouble? Contact me. If you are not part of the Power BI team, I will be unable to provide you with any support. Feel free to file issues if you think they are genuine bugs.
