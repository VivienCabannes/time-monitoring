
import csv
from datetime import datetime
from pathlib import Path
import os

from .config import (
    BUFFER_FILE,
    REPORT_FILE,
    DATE_FORMAT
)


def declare_activity(str_activity):
    """Declare activity

    End last activity and generate a report of last activity in the report_file.
    Report activity and begin time in the buffer BUFFER_FILE.
    """
    end_activity()
    # begin time
    t = datetime.utcnow()
    str_t = t.strftime(DATE_FORMAT)
    with open(BUFFER_FILE, 'w') as f:
        f.write(str_activity + '\n' + str_t + '\n')


def add_message(str_message):
    """Specify activities

    Add a message relative to the current activity,
    writen in the buffer BUFFER_FILE.
    """
    # Assert an activity is in progress
    if os.stat(BUFFER_FILE).st_size == 0:
        print('No activity in progress')
        return

    with open(BUFFER_FILE, 'a') as f:
        # make sure to be at the end of file
        f.seek(0, 2)
        f.write(str_message + '\n')


def end_activity(verbose=False):
    """End activity script

    Report final time, recover begin time, activity and messages in the buffer BUFFER_FILE.
    Create a report if necessary in the REPORT_FILE.
    """
    if os.stat(BUFFER_FILE).st_size == 0:
        if verbose:
            print('No activity in progress')
        return

    with open(BUFFER_FILE, 'r+') as f:
        # make sure to be at the beginning of the file
        f.seek(0, 0)
        # retrive information
        activity = f.readline()[:-1]
        t0 = f.readline()[:-1]
        message = f.read()[:-1].replace('\n', ' - ')

    # clean file
    with open(BUFFER_FILE, 'w') as f:
        f.write('')

    # report final time
    tf = datetime.utcnow()
    dt = tf - datetime.strptime(t0, DATE_FORMAT)
    # get duration
    length = dt.days * 1440 + dt.seconds // 60
    tf = tf.strftime(DATE_FORMAT)

    # create a report
    report = [activity, t0, tf, length, message,]
    with open(REPORT_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(report)
