"""Testing for reports"""
import csv
import os
from subprocess import PIPE, Popen, run

from .fixtures import ACT2, ACT3, ACTIVITY, BUFFER_FILE, DATA_PATH, MESSAGE, REPORT_FILE, ROWS


def test_report_header():
    """Test for report header"""
    # Setup environment
    if BUFFER_FILE.exists():
        os.remove(BUFFER_FILE)
    if REPORT_FILE.exists():
        os.remove(REPORT_FILE)
    run(["setup_time_report"], check=True)

    with open(REPORT_FILE, "r", encoding="ascii", newline="") as f:
        rows = list(csv.reader(f, delimiter=","))
    assert len(rows) == 1
    assert rows[0] == ["activity", "begin", "end", "length", "message"]


def test_pipeline_3b_1s():
    """Test pipeline with three begin commands and one stop"""
    if (
        run(["begin", ACTIVITY], check=True).returncode
        or run(["begin", ACT2], check=True).returncode
        or run(["message", MESSAGE], check=True).returncode
        or run(["begin", ACT3], check=True).returncode
    ):
        assert False
    with open(REPORT_FILE, "r", encoding="ascii", newline="") as f:
        rows = list(csv.reader(f, delimiter=","))
    assert len(rows) == 3
    assert rows[1][0] == ACTIVITY
    assert rows[2][0] == ACT2
    assert rows[1][-1] == ""
    assert rows[2][-1] == MESSAGE
    with open(BUFFER_FILE, "r", encoding="ascii") as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 2
    assert tmp[0] == ACT3

    assert not run(["stop"], check=True).returncode
    with open(REPORT_FILE, "r", encoding="ascii", newline="") as f:
        rows = list(csv.reader(f, delimiter=","))
    assert len(rows) == 4
    assert rows[1][0] == ACTIVITY
    assert rows[2][0] == ACT2
    assert rows[3][0] == ACT3
    assert rows[1][-1] == ""
    assert rows[2][-1] == MESSAGE
    assert rows[3][-1] == ""


def test_stats():
    """Correct behavior of `stats` command"""
    with open(REPORT_FILE, "w", encoding="ascii", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(ROWS)

    with Popen(["stats"], stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()

    assert (
        out
        == b"my activity: 5.8h (5h48m)\n"
        + b"second: 7.7h (7h42m)\n"
        + b"my third activity: 5.083h (5h05m)\n"
    )
    assert err == b""

    with Popen(["stats", "-a", ACT2, ACT3], stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()

    assert out == b"second: 7.7h (7h42m)\n" + b"my third activity: 5.083h (5h05m)\n"
    assert err == b""


def report():
    """Correct behavior of `report` command"""
    with Popen("ls", cwd=DATA_PATH, stdout=PIPE, text=True) as process:
        out_before = process.stdout.readlines()

    with Popen(["report"], stdout=PIPE, stderr=PIPE) as process:
        (out, err) = process.communicate()
    assert out == b""
    assert err == b""

    with Popen("ls", cwd=DATA_PATH, stdout=PIPE, text=True) as process:
        out_after = process.stdout.readlines()

    assert len(out_after) == len(out_before) + 1
    assert out_before == out_after[:-1]
    file_name = out_after[-1].strip()

    with open(DATA_PATH / file_name, "r", encoding="ascii", newline="") as f:
        rows = list(csv.reader(f, delimiter=","))

    assert rows == ROWS
