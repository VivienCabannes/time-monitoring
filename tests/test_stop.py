"""Testing for reports"""
import csv
from datetime import datetime
from subprocess import Popen, PIPE
from time_monitor.config import (
    BUFFER_FILE,
    REPORT_FILE,
    DATE_FORMAT,
)
# try:
#     from time_monitor.config import BUFFER_FILE, REPORT_FILE, DATE_FORMAT
# except ModuleNotFoundError as module_err:
#     print(module_err)
#     from pathlib import Path
#     BUFFER_PATH = Path.home() / '.time-monitoring'
#     BUFFER_FILE = BUFFER_PATH / '.activity'
#     REPORT_FILE = BUFFER_PATH / '.current_report.csv'
#     DATE_FORMAT = '%Y-%m-%d %H:%M'

ACTIVITY = 'my activity'
DATE = '2021-01-01 10:00'
MESSAGE = 'my message'


# Setup environment
Popen(['setup_time_report'], stdout=PIPE).communicate()


def test_stop_without_activity():
    """Command message when no activity are on-going"""
    with open(BUFFER_FILE, 'w') as f:
        f.writelines([])
    process = Popen(['stop'], stdout=PIPE, stderr=PIPE)
    (out, err) = process.communicate()
    assert out == b'No activity in progress\n'
    assert err == b''
    with open(BUFFER_FILE, 'rb') as f:
        tmp = f.read()
    assert tmp == b''


def test_stop():
    """Correct behavior of stop command"""
    tmp = [ACTIVITY + '\n', DATE + '\n']
    with open(BUFFER_FILE, 'w') as f:
        f.writelines(tmp)
    process = Popen(['stop'], stdout=PIPE, stderr=PIPE)
    # record end time
    tf = datetime.utcnow()
    dt = tf - datetime.strptime(DATE, DATE_FORMAT)
    length = dt.days * 1440 + dt.seconds // 60
    tf = tf.strftime(DATE_FORMAT)
    # get process execution variable
    (out, err) = process.communicate()
    assert out == b''
    assert err == b''
    with open(REPORT_FILE, 'r', newline='') as f:
        rows = list(csv.reader(f, delimiter=','))
    assert abs(length - int(rows[-1][3])) < 1
    assert rows[-1] == [
        ACTIVITY, DATE, rows[-1][2], rows[-1][3], ''
    ]
    with open(BUFFER_FILE, 'rb') as f:
        tmp = f.read()
    assert tmp == b''


def test_stop_message():
    """Command stop when one message was posted"""
    tmp = [ACTIVITY + '\n', DATE + '\n', MESSAGE + '\n']
    with open(BUFFER_FILE, 'w') as f:
        f.writelines(tmp)
    process = Popen(['stop'], stdout=PIPE, stderr=PIPE)
    # record end time
    tf = datetime.utcnow()
    dt = tf - datetime.strptime(DATE, DATE_FORMAT)
    length = dt.days * 1440 + dt.seconds // 60
    tf = tf.strftime(DATE_FORMAT)
    # get process execution variable
    (out, err) = process.communicate()
    assert out == b''
    assert err == b''
    with open(REPORT_FILE, 'r', newline='') as f:
        rows = list(csv.reader(f, delimiter=','))
    assert abs(length - int(rows[-1][3])) < 1
    assert rows[-1] == [
        ACTIVITY, DATE, rows[-1][2], rows[-1][3], MESSAGE
    ]
    with open(BUFFER_FILE, 'rb') as f:
        tmp = f.read()
    assert tmp == b''


def test_stop_messages():
    """Command stop when several messages was posted"""
    tmp = [ACTIVITY + '\n', DATE + '\n', MESSAGE + '\n', MESSAGE + '\n', MESSAGE + '\n']
    with open(BUFFER_FILE, 'w') as f:
        f.writelines(tmp)
    process = Popen(['stop'], stdout=PIPE, stderr=PIPE)
    # record end time
    tf = datetime.utcnow()
    dt = tf - datetime.strptime(DATE, DATE_FORMAT)
    length = dt.days * 1440 + dt.seconds // 60
    tf = tf.strftime(DATE_FORMAT)
    # get process execution variable
    (out, err) = process.communicate()
    assert out == b''
    assert err == b''
    with open(REPORT_FILE, 'r', newline='') as f:
        rows = list(csv.reader(f, delimiter=','))
    assert abs(length - int(rows[-1][3])) < 1
    assert rows[-1] == [
        ACTIVITY, DATE, rows[-1][2], rows[-1][3], MESSAGE + ' - ' + MESSAGE + ' - ' + MESSAGE
    ]
    with open(BUFFER_FILE, 'rb') as f:
        tmp = f.read()
    assert tmp == b''


if __name__ == '__main__':
    test_stop_without_activity()
    test_stop()
    test_stop_message()
    test_stop_messages()
