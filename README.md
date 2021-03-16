# Lyst

Here is a Cron test that simulates a typical crontab deamon in Linux.

It's been written in Python version 3 and runs as a command line interface.

In order to run the application use:

```
  python3 cli.py <HH:MM> < crons.txt
```
  
where *crons.txt* contains a series of crontab lines, eg:

``` 
  30 1 /bin/run_me_daily
  45 * /bin/run_me_hourly
  * * /bin/run_me_every_minute
  * 19 /bin/run_me_sixty_times
```

An example of its output is here:

```
  python3 cli.py 16:10 < crons.txt
  
  1:30 tomorrow - /bin/run_me_daily
  16:45 today - /bin/run_me_hourly
  16:10 today - /bin/run_me_every_minute
  19:00 today - /bin/run_me_sixty_times 
```

The application uses the 24-hour time format for HH:MM.

### Notes:

The code has assertions to ensure that the values for hours and minutes are within bounds although there are no attempts to recover from those errors. A better implementation would be to detect any input formatting errors and report exactly what the error is and on which line it was found.
