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

### Authors and Contributors
Sachin Patney

### Support or Contact
Having trouble? Contact me.
