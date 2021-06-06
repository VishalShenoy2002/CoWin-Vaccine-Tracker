# CoWin-Vaccine-Tracker
This Tracker is used to track slots from Cowin Website. It has a class called VaccineTracker which has all the required functions. This program is written in Python.

## Modules Used
The Modules used in this project are as Follows:
1. cowin_api
2. datetime
3. time
4. csv
5. plyer

## Setup
If there is an ImportError please do the following:
1. `pip install cowin`
2. `pip install plyer`

## Suggestion
Add the following to the code:
1. Create an Infinite Loop 
2. Inside the infinite loop add `time.sleep()` with number of seconds as the parameter for time interval so that the program runs once for each time interval.
3. *For Windows :* Create a task in task sheduler and make it trigger during Startup so that the program starts running automatically when your computer starts.
