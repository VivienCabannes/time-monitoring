"""Testing for basic command"""
from subprocess import PIPE, Popen

from time_monitor.config import BUFFER_FILE


def test_setup():
    """Setup environment"""
    with Popen(["setup_time_report"], stdout=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    assert err is None
    assert process.returncode == 0


def test_begin_no_argument():
    """Command `begin` without argument is not a correct behavior"""
    with Popen("begin", stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    tmp = err.splitlines()
    assert len(tmp) == 2
    assert tmp[1] == b"begin: error: the following arguments are required: activity"


def test_begin(activity):
    """Correct behavior of `begin` command"""
    with Popen(["begin", activity], stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    assert err == b""
    with open(BUFFER_FILE, "r", encoding="ascii") as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 2
    assert tmp[0] == activity


def test_begin_option(activity, message):
    """Command `begin` with one option"""
    with Popen(["begin", activity, "-m", message], stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    assert err == b""
    with open(BUFFER_FILE, "r", encoding="ascii") as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 3
    assert tmp[0] == activity
    assert tmp[2] == message


def test_begin_options(activity, message):
    """Command `begin` with many options"""
    cmd = ["begin", activity, "-m", message, message, message]
    with Popen(cmd, stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    assert err == b""
    with open(BUFFER_FILE, "r", encoding="ascii") as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 5
    assert tmp[0] == activity
    assert tmp[2] == message
    assert tmp[3] == message
    assert tmp[4] == message


def test_message_no_argument():
    """Command `message` without argument is not a correct behavior"""
    with Popen("message", stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    tmp = err.splitlines()
    assert len(tmp) == 2
    assert tmp[1] == b"message: error: the following arguments are required: message"


def test_message(activity, date, message):
    """Correct behavior of `message` command"""
    tmp = [activity + "\n", date + "\n"]
    with open(BUFFER_FILE, "w", encoding="ascii") as f:
        f.writelines(tmp)
    with Popen(["message", message], stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    assert err == b""
    with open(BUFFER_FILE, "r", encoding="ascii") as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 3
    assert tmp[0] == activity
    assert tmp[2] == message


def test_message_without_activity(message):
    """Command `message` when no activity are on-going"""
    with open(BUFFER_FILE, "w", encoding="ascii") as f:
        f.writelines([])
    with Popen(["message", message], stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b"No activity in progress\n"
    assert err == b""
    with open(BUFFER_FILE, "rb") as f:
        tmp = f.read()
    assert tmp == b""


def test_message_arguments(activity, date, message):
    """Command `message` with many arguments"""
    tmp = [activity + "\n", date + "\n"]
    with open(BUFFER_FILE, "w", encoding="ascii") as f:
        f.writelines(tmp)
    with Popen(["message", message, message, message], stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    assert err == b""
    with open(BUFFER_FILE, "r", encoding="ascii") as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 5
    assert tmp[0] == activity
    assert tmp[2] == message
    assert tmp[3] == message
    assert tmp[4] == message
