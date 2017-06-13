# website-tracker
Website tracking python script - notifies about changes with an email.

# Setup
Create config file:
```
{
    "sender" : {
        "address" : "someemail@gmail.com",
        "password" : "somepass",
        "smtp_server" : "smtp.gmail.com",
        "port" : "587",
        "enable_tls" : true
    },
    "trackers" : [
        {
            "alias" : "TRACKER #1",
            "to" : [
                "email1@email.com",
                "email2@email.com"
            ],
            "url" : "http://some-url-to-track.com"
            "subject" : "email notification subject",
            "content" : "email notification content"
        }
    ]
}
```

# Usage
Using cron is recommended, setup it to run _tracker.py_ every x minutes.

For example crontab configuration running the script every 30 minutes:
```
*/30 * * * * /path/to/tracker.py
```
By default _tracker.py_ searches for configuration file in your home directory (_~/.website-tracker-conf_). If it is located somewhere else or named something else you can explicitely tell the tracker to use it:
```
./tracker.py /path/to/config
```

# License
```
MIT License

Copyright (c) 2017 Maciej Grzeszczak

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
