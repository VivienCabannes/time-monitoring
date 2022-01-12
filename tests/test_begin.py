"""Testing for basic command"""
from subprocess import Popen, PIPE
from time_monitor.config import BUFFER_FILE
# try:
#     from time_monitor.config import BUFFER_FILE
# except ModuleNotFoundError as module_err:
#     print(module_err)
#     from pathlib import Path
#     BUFFER_PATH = Path.home() / '.time-monitoring'
#     BUFFER_FILE = BUFFER_PATH / '.activity'

ACTIVITY = 'my activity'
DATE = '2021-01-01 10:00'
MESSAGE = 'my message'


def test_setup():
    """Setup environment"""
    process = Popen(['setup_time_report'], stdout=PIPE)
    (out, err) = process.communicate()
    assert out == b''
    assert err is None
    assert process.returncode == 0


def test_begin_no_argument():
    """Command begin without argument is not a correct behavior"""
    process = Popen('begin', stdout=PIPE, stderr=PIPE)
    (out, err) = process.communicate()
    assert out == b''
    tmp = err.splitlines()
    assert len(tmp) == 2
    assert tmp[1] == b'begin: error: the following arguments are required: activity'


def test_begin():
    """Correct behavior of begin command"""
    process = Popen(['begin', ACTIVITY], stdout=PIPE, stderr=PIPE)
    (out, err) = process.communicate()
    assert out == b''
    assert err == b''
    with open(BUFFER_FILE, 'r') as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 2
    assert tmp[0] == ACTIVITY


def test_begin_option():
    """Command begin with one option"""
    process = Popen(['begin', ACTIVITY, '-m', MESSAGE], stdout=PIPE, stderr=PIPE)
    (out, err) = process.communicate()
    assert out == b''
    assert err == b''
    with open(BUFFER_FILE, 'r') as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 3
    assert tmp[0] == ACTIVITY
    assert tmp[2] == MESSAGE


def test_begin_options():
    """Command begin with many options"""
    process = Popen(['begin', ACTIVITY, '-m', MESSAGE, MESSAGE, MESSAGE],
                    stdout=PIPE, stderr=PIPE)
    (out, err) = process.communicate()
    assert out == b''
    assert err == b''
    with open(BUFFER_FILE, 'r') as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 5
    assert tmp[0] == ACTIVITY
    assert tmp[2] == MESSAGE
    assert tmp[3] == MESSAGE
    assert tmp[4] == MESSAGE


def test_message_no_argument():
    """Command message without argument is not a correct behavior"""
    process = Popen('message', stdout=PIPE, stderr=PIPE)
    (out, err) = process.communicate()
    assert out == b''
    tmp = err.splitlines()
    assert len(tmp) == 2
    assert tmp[1] == b'message: error: the following arguments are required: message'


def test_message():
    """Correct behavior of message command"""
    tmp = [ACTIVITY + '\n', DATE + '\n']
    with open(BUFFER_FILE, 'w') as f:
        f.writelines(tmp)
    process = Popen(['message', MESSAGE], stdout=PIPE, stderr=PIPE)
    (out, err) = process.communicate()
    assert out == b''
    assert err == b''
    with open(BUFFER_FILE, 'r') as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 3
    assert tmp[0] == ACTIVITY
    assert tmp[2] == MESSAGE


def test_message_without_activity():
    """Command message when no activity are on-going"""
    with open(BUFFER_FILE, 'w') as f:
        f.writelines([])
    process = Popen(['message', MESSAGE], stdout=PIPE, stderr=PIPE)
    (out, err) = process.communicate()
    assert out == b'No activity in progress\n'
    assert err == b''
    with open(BUFFER_FILE, 'rb') as f:
        tmp = f.read()
    assert tmp == b''


def test_message_arguments():
    """Command message with many arguments"""
    tmp = [ACTIVITY + '\n', DATE + '\n']
    with open(BUFFER_FILE, 'w') as f:
        f.writelines(tmp)
    process = Popen(['message', MESSAGE, MESSAGE, MESSAGE],
                    stdout=PIPE, stderr=PIPE)
    (out, err) = process.communicate()
    assert out == b''
    assert err == b''
    with open(BUFFER_FILE, 'r') as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 5
    assert tmp[0] == ACTIVITY
    assert tmp[2] == MESSAGE
    assert tmp[3] == MESSAGE
    assert tmp[4] == MESSAGE


if __name__ == '__main__':
    test_setup()
    test_begin_no_argument()
    test_begin()
    test_begin_option()
    test_begin_options()
    test_message_no_argument()
    test_message()
    test_message_without_activity()
    test_message_arguments()
