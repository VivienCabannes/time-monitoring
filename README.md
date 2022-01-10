# Time monitoring

The `time-monitoring` package provides useful tools to monitor your time.
It can be used to improve productivity, or to generate invoice.

## Shell commands
This package provides the following shell executables.

#### Basic commands
- The `begin` command
```
$ begin <activity> -m --message "<optional message>"
```
This command indicates that you have begun a new activity specified by `<activity>`, *e.g.* `<activity>=work`.
You may add a message such as `"fixing issue 31"`.  
If you use this command while another activity was already declared, it will assume you just stop the precedent activity.

- The `message` command
```
$ message "<message>" "<first optional message>" [...] "<final optional message>"
```
This command allows you to add a message without modifying the activity you are currently pursuing.
For example, if you have already declare being in your spare time and decide to read the press and would like to monitor this, you can add the message `"reading the press"`.

- The `stop` command
```
$ stop
```
When you stop an activity and do not begin a new one, run this command.

- The `report` command
```
$ report
```
This command saves all activities recorded since last report in order to generate a new report.
This is useful to generate statistics or invoices.  
Reports are numbered according the the format `<YYYY><MM><NB>` where `<YYYY>` and `<MM>` denominates the current year and month and `<NB>` is counting the number of reports generated so far in the month.  
Past activity reports are kept in a `data` folder specified by the variable `DATA_PATH` of the `time_monitoring/config.py` file.

#### Advanced commands
- The `activity` command
```
$ activity
```
This command opens the buffer file that records your current activity.
It is useful to check make sure you have declared it correctly and eventually correct it.

- The `stats` command
```
$ stats
```
This command sums up current period activities.

- The `invoice` command
```
$ invoice -a --activity <activity> -o --output <output file> -p --partial -l --latex <main.tex>
```
This command is useful to generate invoices.

## Installation
**Requirements**:
The package is based on python and shell.  

We provide an installation through the `pipy` package repository, hence you can use pip to download it.
```
$ pip install time-monitoring
```
If you are working with `conda` environments, make sure that your pip command is linked to conda by typing `$ which pip` and making sure that the output displays conda installation path.
