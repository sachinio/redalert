### Welcome to 'Red' Alert

This is a notification system built for the Power BI Team @ Microsoft. Some parts of the system work in conjuntion with special hardware and services. 

Setting this up on a raspberry pi is simple, just copy and run setup.py as follows :-

```
sudo python3 setup.py
```

This will enlist/install all the required libraries and folder structures. Depending on the hooks required, you might need to create options.csv in /var/www/tmp, and fill as shown

```
lack_token,your_token
vso_password,your_password
buildbroken,False
gmail_username,your_username
gmail_password,your_password
vso_username,your_username
weather_key,your_api_id
```

### ITask
An ITask is a script that when run preforms a specific operation. An example is the weather task, which checks the weather in Redmond, and posts it to the timeline. The tasks's __run__(self, time) method takes in a time parameter which can be used to control when a task is run, since the runner will launch all tasks every minute. 

An example of a task.

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

### Support or Contact
Having trouble? Contact me.
