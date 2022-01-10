
import csv
from datetime import datetime
import os
from pathlib import Path

from .config import (
    REPORT_FILE,
    DATA_PATH,
)


def new_report():
    """Save current report file under report-friendly denomination"""
    # get report number
    date = datetime.utcnow().strftime('%Y-%m')
    year, month = date[:4], date[-2:]
    with open(DATA_PATH / '.report_numbers', 'r+', newline='') as f:
        rows = list(csv.reader(f))

        number = 1
        # look for similar year and month report
        if len(rows) > 1:
            # report are ordered, so only looked for last one
            row = rows[1]
            if row[0] == year and row[1] == month:
                number = int(row[2]) + 1

        # formatting
        if len(str(number)) < 2:
            number = '0' + str(number)
        else:
            number = str(number)
        rows.insert(1, [year, month, number])

    # report new report
    with open(DATA_PATH / '.report_numbers', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

    # save current report under report number
    file_name = year + month + number + '.csv'
    file_path = DATA_PATH / file_name
    os.rename(REPORT_FILE, file_path)

    # reset buffer file to report future work
    header = ['activity' , 'begin' , 'end' , 'length' , 'message',]
    with open(REPORT_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)


def get_last_report_number():
    """Get last report file path

    Read information in file .report_numbers.
    """
    with open(DATA_PATH / '.report_numbers', 'r+', newline='') as f:
        rows = list(csv.reader(f))
        if len(rows) > 1:
            # report are ordered, so only looked for last one
            row = rows[1]
            year = row[0]
            month = row[1]
            number = row[2]
        else:
            return ValueError('No report have been generated')
    return year + month + number


def read_report(report_path):
    """Extract precious information from report file

    Compute total number of hours per activity, clustered by days.
    """
    if isinstance(report_path, str):
        report_path = DATA_PATH / (report_path + '.csv')
    with open(report_path, 'r', newline='') as f:
        rows = list(csv.reader(f, delimiter=','))[1:]
        activities, messages, dates, lengths = [], [], [], []
        begin_date = None
        for row in rows:
            # retrieve informations
            activity, t0, tf, length, message = row
            message = message.replace(' - ', '\n')
            length = int(length)
            date = t0[:10]

            if begin_date is None:
                begin_date = date

            # if activity has already been define
            if activity in activities:
                index = activities.index(activity)
                messages[index] += message + '\n'

                # search if the same activity already took place this day
                if date in dates[index]:
                    ind = dates[index].index(date)
                    # add lengths to the current counter
                    lengths[index][ind] += length
                else:
                    dates[index].append(date)
                    lengths[index].append(length)

            else:
                activities.append(activity)
                messages.append(message + '\n')
                dates.append([date, ])
                lengths.append([length, ])
    try:
        end_date = date
    except UnboundLocalError:
        end_date = None

    # convert length to string
    outputs, totals = [], []
    for i in range(len(lengths)):
        output, total = '', 0
        for date, length in zip(dates[i], lengths[i]):
            total += length
            dt = str(length // 60) + 'h' + str(length % 60).zfill(2) + 'm'
            output += date + ' :& ' + dt + '\\\\'
        minute = str(total % 60)
        dt = str(total // 60) + 'h' + minute.zfill(2) + 'm'
        total = round(total / .06) / 1000
        dt = str(total) + 'h (' + dt + ')'
        outputs.append(output)
        totals.append([total, dt])

    return activities, outputs, totals, messages, (begin_date, end_date)
