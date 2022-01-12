"""Testing for basic command"""
from subprocess import PIPE, Popen

from .fixtures import ACTIVITY, BUFFER_FILE, DATE, MESSAGE


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


def test_begin():
    """Correct behavior of `begin` command"""
    with Popen(["begin", ACTIVITY], stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    assert err == b""
    with open(BUFFER_FILE, "r", encoding="ascii") as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 2
    assert tmp[0] == ACTIVITY


def test_begin_option():
    """Command `begin` with one option"""
    with Popen(["begin", ACTIVITY, "-m", MESSAGE], stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    assert err == b""
    with open(BUFFER_FILE, "r", encoding="ascii") as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 3
    assert tmp[0] == ACTIVITY
    assert tmp[2] == MESSAGE


def test_begin_options():
    """Command `begin` with many options"""
    cmd = ["begin", ACTIVITY, "-m", MESSAGE, MESSAGE, MESSAGE]
    with Popen(cmd, stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    assert err == b""
    with open(BUFFER_FILE, "r", encoding="ascii") as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 5
    assert tmp[0] == ACTIVITY
    assert tmp[2] == MESSAGE
    assert tmp[3] == MESSAGE
    assert tmp[4] == MESSAGE


def test_message_no_argument():
    """Command `message` without argument is not a correct behavior"""
    with Popen("message", stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    tmp = err.splitlines()
    assert len(tmp) == 2
    assert tmp[1] == b"message: error: the following arguments are required: message"


def test_message():
    """Correct behavior of `message` command"""
    tmp = [ACTIVITY + "\n", DATE + "\n"]
    with open(BUFFER_FILE, "w", encoding="ascii") as f:
        f.writelines(tmp)
    with Popen(["message", MESSAGE], stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    assert err == b""
    with open(BUFFER_FILE, "r", encoding="ascii") as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 3
    assert tmp[0] == ACTIVITY
    assert tmp[2] == MESSAGE


def test_message_without_activity():
    """Command `message` when no activity are on-going"""
    with open(BUFFER_FILE, "w", encoding="ascii") as f:
        f.writelines([])
    with Popen(["message", MESSAGE], stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b"No activity in progress\n"
    assert err == b""
    with open(BUFFER_FILE, "rb") as f:
        tmp = f.read()
    assert tmp == b""


def test_message_arguments():
    """Command `message` with many arguments"""
    tmp = [ACTIVITY + "\n", DATE + "\n"]
    with open(BUFFER_FILE, "w", encoding="ascii") as f:
        f.writelines(tmp)
    with Popen(["message", MESSAGE, MESSAGE, MESSAGE], stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    assert err == b""
    with open(BUFFER_FILE, "r", encoding="ascii") as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 5
    assert tmp[0] == ACTIVITY
    assert tmp[2] == MESSAGE
    assert tmp[3] == MESSAGE
    assert tmp[4] == MESSAGE
