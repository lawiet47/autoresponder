# AutoResponder

## Carbon Black Response IR tool for hunting threats in an environment



![autoresponder](https://user-images.githubusercontent.com/27059441/69006416-ebb02280-093f-11ea-8654-88c19c4e95e9.PNG)


# What is it?

AutoResponder is a tool aimed to help people to carry out their Incident Response tasks WITH the help of Carbon Black Response's awesome capabilities and WITHOUT much bothering IT/System/Network Teams

# What can it do?


| Module  | :heavy_check_mark: / :x: |
| ------------- | ------------- |
| Delete Files  | :heavy_check_mark: |
| Delete Registry Values  | :heavy_check_mark:  |
| Delete Win32 Service Entries  | :heavy_check_mark:  |
| Delete Scheduled Task Entries  | :heavy_check_mark:  |
| Detailed Sensor List Export | :heavy_check_mark: |
| Find Files | :heavy_check_mark: |
| Find Registry Values | :heavy_check_mark: |
| Download Files | :heavy_check_mark: |
| Download A list of Win32 Service Entries | :heavy_check_mark: |
| Download A list of Scheduled Task Entries | :heavy_check_mark: |
| Download A list of WMI Entries | :heavy_check_mark: |
| Isolate/Unisolate Sensors | :heavy_check_mark: |
| Kill Running Processes | :heavy_check_mark: |
| Restart Sensors | :heavy_check_mark: |
| Restart Endpoints | :heavy_check_mark: |
| Generate CSV reports | :heavy_check_mark: |
| Delete WMI Entries  | :x:  |
| Solve the whole case and generate a nice report so we can all have a cold beer | :x: |

![2019-11-17_01-55-34](https://user-images.githubusercontent.com/27059441/69006239-590e8400-093d-11ea-8eb3-3aeb750fea99.gif)

# Who is it for?

| You are a  | :heavy_check_mark: / :x: |
| ------------- | ------------- |
| Government agency  | :heavy_check_mark: |
| State agency  | :heavy_check_mark:  |
| Bank  | :heavy_check_mark:  |
| Public/Private Institution  | :heavy_check_mark:  |
| Compant that has Carbon Black Response installed in the environment as an EDR product | :heavy_check_mark: |
| A company doing Incident Response | :heavy_check_mark: |
| Startup? (Doubt it) | :heavy_check_mark: |
| Person who has no idea what Carbon Black is | :x: |

# How?

For those who aren't familiar with Carbon Black Response, it is a quite amazing product that delivers a solution to Incident Response cases in its own unique and awesome way. Carbon Black Response has a python API integration which helps people automate their tasks - saving a lot of time. So all you see in this project is just python API magic - nothing more, nothing less.

# But why..?

For the past months there was a lot of Incident Response cases that our team had to deal with. Although we got through it like a champ, I've noticed that our team had been struggling to communicate with the customer's IT/System/Network Teams and when they did a single file search would result in weeks. Because we are Carbon Black's Incident Response partner and because we heavily use Carbon Black Response in most cases we're involved, I've decided to write a tool to help our team to get very BIG tasks done in a very short time with a minimum amount of help from others.


# What's the big deal? There are other tools and people for it

Fair enough, Now, Imagine a scenario where hundreds of the endpoints have been compromised, the attacker has established persistence on all of them and dropped a ton of files. And what a coincidence that is - whole IT team decided to go on a vacation leaving nobody back at the office to deal with the Incident and Domain Admin wants to file a paper for every key that's pressed on his keyboard - eleminating your ability to identify and eradicate threats on compromised systems. Good luck! (True story btw)



# How can I use it?

The code is written in python3 so any version above 3.4 will do fine

1. Download the zip archive or do a `git pull`
2. Install required modules with `pip3 install -r requirements.txt` 
3. Configure Carbon Black API => https://cbapi.readthedocs.io/en/latest/
4. Kick ass

## Special Thanks to

Big thanks to https://twitter.com/harunglec for helping out with the multi-threading module.

Many thanks to https://twitter.com/cyb3rops & https://twitter.com/thor_scanner for inspiring the CLI :) (I hope I don't get in any trouble for copying the UI)

# P.S

This is just a python code - which means feel free to modify it for your needs. Please report any issues to => https://github.com/lawiet47/autoresponder/issues 

Current modules all have been tested against sensors that have Windows as an OS environment. But you can give it a try on linux too.
