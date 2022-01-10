# Time monitoring

This package provides useful tools to monitor your time.
It can be used to improve productivity, or to generate invoice.

#### Basic commands

It provides the following shell executables.
- The `begin` command
```
$ begin <activity> -m --message "<optional message>"
```
This command indicates that you have begun a new activity specified by `<activity>`, *e.g.* `<activity>=work`.
You may add a message such as `"fixing issue 31"`.  
If you use this command while another activity was already declared, it will assume you just stop the precedent activity.

- The `stop` command
```
$ stop
```
When you stop an activity and do not begin a new one, run this command.

- The `geninv` command
```
$ geninv -a --activity <activity> -o --output <output file> -p --partial -l --latex <main.tex>
```
This command is useful to generate invoices.

#### Advance commands
- The `message` command
```
$ message "<message>" "<first optional message>" [...] "<final optional message>"
```
This command allows you to add a message without modifying the activity you are currently pursuing.
For example, if you have already declare being in your spare time and decide to read the press and would like to monitor this, you can add the message `"reading the press"`.

- The `check_activity` command
```
$ check_activity
```
This command opens the buffer file that records your current activity.
It is useful to check make sure you have declared it correctly and eventually correct it.
