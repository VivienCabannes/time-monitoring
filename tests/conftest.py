"""Variables for unit tests"""
from pathlib import Path
from shutil import rmtree
from subprocess import run

import pytest
from time_monitor.config import BUFFER_PATH


@pytest.fixture(scope="session", autouse=True)
def buffer_isolation():
    """Avoid overwritting the current buffer while testing"""

    # Move buffer to a temporary folder
    tmp_path = Path.home() / ".tmp-time-monitoring"
    if BUFFER_PATH.exists():
        run(["mv", str(BUFFER_PATH), str(tmp_path)], check=True)

    # instanciate a new buffer folder
    run(["setup_time_report"], check=True)

    # run unit test
    yield

    # remove the testing buffers
    rmtree(BUFFER_PATH)

    # move back the old buffer folder
    if tmp_path.exists():
        run(["mv", str(tmp_path), str(BUFFER_PATH)], check=True)


@pytest.fixture
def activity():
    """fake activity"""
    return "my activity"


@pytest.fixture
def act2():
    """fake activity"""
    return "second"


@pytest.fixture
def act3():
    """fake activity"""
    return "my third activity"


@pytest.fixture
def date():
    """fake date"""
    return "2021-01-01 10:00"


@pytest.fixture
def message():
    """fake message"""
    return "my message"


@pytest.fixture
def activity_report(activity, act2, act3, message):
    """Fake report table populating .current_report"""
    return [
        ["activity", "begin", "end", "length", "message"],
        [activity, "2021-09-01 07:52", "2021-09-01 08:07", "15", "monte carlo iteration"],
        [activity, "2021-09-01 09:02", "2021-09-01 09:07", "5", ""],
        [act2, "2021-09-01 09:15", "2021-09-01 09:20", "5", message],
        [act3, "2021-09-01 09:30", "2021-09-01 10:02", "32", ""],
        [act2, "2021-09-01 10:11", "2021-09-01 11:39", "88", message],
        [act3, "2021-09-01 11:41", "2021-09-01 11:49", "8", message],
        [activity, "2021-09-03 11:51", "2021-09-03 12:40", "49", ""],
        [activity, "2021-09-04 06:32", "2021-09-04 06:34", "2", message],
        [act3, "2021-09-04 06:41", "2021-09-04 06:41", "0", ""],
        [act3, "2021-09-04 06:41", "2021-09-04 08:37", "116", ""],
        [activity, "2021-09-04 09:19", "2021-09-04 09:21", "2", ""],
        [act2, "2021-09-04 09:23", "2021-09-04 09:23", "0", ""],
        [activity, "2021-09-04 09:23", "2021-09-04 09:42", "19", ""],
        [act2, "2021-09-05 09:06", "2021-09-05 09:39", "33", ""],
        [activity, "2021-09-05 15:25", "2021-09-05 17:07", "102", ""],
        [act2, "2021-09-05 17:08", "2021-09-05 17:16", "8", ""],
        [act2, "2021-09-06 16:00", "2021-09-06 16:35", "35", message],
        [act2, "2021-09-06 16:40", "2021-09-06 16:49", "9", ""],
        [act2, "2021-09-06 16:52", "2021-09-06 17:03", "11", ""],
        [activity, "2021-09-13 12:50", "2021-09-13 13:24", "34", ""],
        [activity, "2021-09-14 06:24", "2021-09-14 06:27", "3", ""],
        [activity, "2021-09-14 06:27", "2021-09-14 06:56", "29", ""],
        [activity, "2021-09-14 07:47", "2021-09-14 07:48", "1", ""],
        [act3, "2021-09-14 07:48", "2021-09-14 08:02", "14", ""],
        [act3, "2021-09-14 08:03", "2021-09-14 08:48", "45", ""],
        [act3, "2021-09-14 08:58", "2021-09-14 09:06", "8", ""],
        [act2, "2021-09-14 09:06", "2021-09-14 09:09", "3", ""],
        [activity, "2021-09-14 09:25", "2021-09-14 09:26", "1", message],
        [activity, "2021-09-14 09:26", "2021-09-14 09:27", "1", message],
        [activity, "2021-09-14 09:46", "2021-09-14 09:47", "1", message],
        [activity, "2021-09-14 10:02", "2021-09-14 10:20", "18", message],
        [activity, "2021-09-14 19:25", "2021-09-14 19:56", "31", message],
        [act3, "2021-09-15 07:33", "2021-09-15 08:55", "82", ""],
        [activity, "2021-09-15 09:00", "2021-09-15 09:35", "35", ""],
        [act2, "2021-09-15 13:53", "2021-09-15 18:23", "270", message],
    ]


@pytest.fixture
def act1_time():
    """time recorded as `act1` in `activity_report`"""
    return "5.8h (5h48m)"


@pytest.fixture
def act2_time():
    """time recorded as `act2` in `activity_report`"""
    return "7.7h (7h42m)"


@pytest.fixture
def act3_time():
    """time recorded as `act3` in `activity_report`"""
    return "5.083h (5h05m)"
