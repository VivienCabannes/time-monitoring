"""Testing for time reports"""
import csv
from datetime import datetime
from subprocess import PIPE, Popen, run

from time_monitor.config import BUFFER_FILE, DATE_FORMAT, REPORT_FILE


def test_stop_without_activity():
    """Command `stop` when no activity are on-going"""
    # Setup environment
    run(["setup_time_report"], check=True)

    with open(BUFFER_FILE, "w", encoding="ascii") as f:
        f.writelines([])
    with Popen(["stop"], stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b"No activity in progress\n"
    assert err == b""
    with open(BUFFER_FILE, "rb") as f:
        tmp = f.read()
    assert tmp == b""


def test_stop(activity, date):
    """Correct behavior of `stop` command"""
    tmp = [activity + "\n", date + "\n"]
    with open(BUFFER_FILE, "w", encoding="ascii") as f:
        f.writelines(tmp)
    with Popen(["stop"], stdout=PIPE, stderr=PIPE) as process:
        # record end time
        tf = datetime.utcnow()
        dt = tf - datetime.strptime(date, DATE_FORMAT)
        length = dt.days * 1440 + dt.seconds // 60
        tf = tf.strftime(DATE_FORMAT)
        # get process execution variable
        (out, err) = process.communicate()
    assert out == b""
    assert err == b""
    with open(REPORT_FILE, "r", encoding="ascii", newline="") as f:
        rows = list(csv.reader(f, delimiter=","))
    assert abs(length - int(rows[-1][3])) < 1
    assert rows[-1] == [activity, date, rows[-1][2], rows[-1][3], ""]
    with open(BUFFER_FILE, "rb") as f:
        tmp = f.read()
    assert tmp == b""


def test_stop_message(activity, date, message):
    """Command `stop` when one message was posted"""
    tmp = [activity + "\n", date + "\n", message + "\n"]
    with open(BUFFER_FILE, "w", encoding="ascii") as f:
        f.writelines(tmp)
    with Popen(["stop"], stdout=PIPE, stderr=PIPE) as process:
        # record end time
        tf = datetime.utcnow()
        dt = tf - datetime.strptime(date, DATE_FORMAT)
        length = dt.days * 1440 + dt.seconds // 60
        tf = tf.strftime(DATE_FORMAT)
        # get process execution variable
        (out, err) = process.communicate()
    assert out == b""
    assert err == b""
    with open(REPORT_FILE, "r", encoding="ascii", newline="") as f:
        rows = list(csv.reader(f, delimiter=","))
    assert abs(length - int(rows[-1][3])) < 1
    assert rows[-1] == [activity, date, rows[-1][2], rows[-1][3], message]
    with open(BUFFER_FILE, "rb") as f:
        tmp = f.read()
    assert tmp == b""


def test_stop_messages(activity, date, message):
    """Command `stop` when several messages was posted"""
    tmp = [activity + "\n", date + "\n", message + "\n", message + "\n", message + "\n"]
    with open(BUFFER_FILE, "w", encoding="ascii") as f:
        f.writelines(tmp)
    with Popen(["stop"], stdout=PIPE, stderr=PIPE) as process:
        # record end time
        tf = datetime.utcnow()
        dt = tf - datetime.strptime(date, DATE_FORMAT)
        length = dt.days * 1440 + dt.seconds // 60
        tf = tf.strftime(DATE_FORMAT)
        # get process execution variable
        (out, err) = process.communicate()
    assert out == b""
    assert err == b""
    with open(REPORT_FILE, "r", encoding="ascii", newline="") as f:
        rows = list(csv.reader(f, delimiter=","))
    assert abs(length - int(rows[-1][3])) < 1
    assert rows[-1] == [
        activity,
        date,
        rows[-1][2],
        rows[-1][3],
        message + " - " + message + " - " + message,
    ]
    with open(BUFFER_FILE, "rb") as f:
        tmp = f.read()
    assert tmp == b""
