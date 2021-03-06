# scooter_scrapper

The objective of this project is to scrap data of positions of scooters like Lime / Bird / Cird, etc.
Contrary to a lot of existing projects, the objective here is to get an overview of *all* the scooters of a city and to *store* this data, to be able to analyse it afterwards.

## Current Status
### Actual output
Running the main will 
* gather all the bikes of the cities from the spreadsheet (see below), 
* export all the data to a zipped csv (you can specify the folder in the argument of the main), 
* upload this CSV to a folder in google drive (you can specify the folder ID + auth stuff in the settings file)
* send a table with the result of the execution via Slack. This rely on a slack token and and a slack channel ID in the settings file.

In the utils.py file, you will find a method that is meant to run locally, `def import_new_data(settings):
`. It does the following: 
* Downloads any file from the Google Drive folder that has not been downloaded already
* Merge hourly CSVs into daily CSVs, removing the column "raw_data", making them half the size.
* Loads these daily files to a Postgres DB


### Pain points
#### Lime
Lime needs a lot of queries because the API responds only 50 bikes at a time, and Berlin has for example around 10k Lime scooters.You need to wait 5 seconds between each query, otherwise you get a 429 error (too many tries).
We could have a better strategy to query the bike in a smarter way, and use more than 1 account info to make more than 1 request each 5 seconds

But the real problem is that Lime Scooters have no identifying info, so you cannot see the history of a particular scooter. This forbids any life expectancy analysis, which is very problematic since this is one of the main objective of the project.

#### Bird 
For some reason, Bird is working only for Berlin. Even after generating another token from another device, I cannot get it to work. 

#### Circ
For some reason, Circ is working when ran locally, but not from my server. This could be due to Circ detecting from the IP that it is a server, but it's not so sure. 

## Tech Details
###Settings file
The Project needs a `settings.ini` file in the project folder that contains the necessary params, especially to make the request of each providers. This file should be as follow:

```
[PROVIDERS]
cities_providers_url = https://docs.google.com/spreadsheets/d/1-aa_2rgfnXMkhmxQQYVeFBfr1zJSFHfqqACV4LBELm0/export?format=csv&id=1-aa_2rgfnXMkhmxQQYVeFBfr1zJSFHfqqACV4LBELm0&gid=0
circ.access_token = 
circ.refresh_token = 
lime.token = 
bird.token = 
voi.authenticationtoken = 

[POSTGRES]
host = localhost
database = scooter_scrapper
user = 
password = 

[SLACK]
token = 
channel = 

[GOOGLE_DRIVE]
filename = 
folder_id = 
email_user = 
```

### cities and providers spreadsheet
See here: https://docs.google.com/spreadsheets/d/1-aa_2rgfnXMkhmxQQYVeFBfr1zJSFHfqqACV4LBELm0
a spreadsheet with cities and providers, as well was lat / lng info of each city. 

### Params for Provider requests
To see how to get the different token, the easiest is to refer to this list:
[https://github.com/ubahnverleih/WoBike](https://github.com/ubahnverleih/WoBike)
which explains in much details how to retrieve each of the token / necessary IDs. 

### CronJob
here is the Cron setup that you need to setup to run the main each hour: 

`0 * * * * <python path> <path to main.py> <working directory>`

so for me: 

`0 * * * * /usr/bin/python3 /root/scooter_scrapper/main.py /root/scooter_scrapper`

## Next Steps
* fix painpoint
* start the data analysis
