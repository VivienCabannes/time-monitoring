"""Testing for reports"""
import csv
import os
from subprocess import PIPE, Popen, run

from time_monitor.config import BUFFER_FILE, DATA_PATH, REPORT_FILE


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


def test_pipeline_3b_1s(activity, act2, act3, message):
    """Test pipeline with three begin commands and one stop"""
    if (
        run(["begin", activity], check=True).returncode
        or run(["begin", act2], check=True).returncode
        or run(["message", message], check=True).returncode
        or run(["begin", act3], check=True).returncode
    ):
        assert False
    with open(REPORT_FILE, "r", encoding="ascii", newline="") as f:
        rows = list(csv.reader(f, delimiter=","))
    assert len(rows) == 3
    assert rows[1][0] == activity
    assert rows[2][0] == act2
    assert rows[1][-1] == ""
    assert rows[2][-1] == message
    with open(BUFFER_FILE, "r", encoding="ascii") as f:
        tmp = f.read().splitlines()
    assert len(tmp) == 2
    assert tmp[0] == act3

    assert not run(["stop"], check=True).returncode
    with open(REPORT_FILE, "r", encoding="ascii", newline="") as f:
        rows = list(csv.reader(f, delimiter=","))
    assert len(rows) == 4
    assert rows[1][0] == activity
    assert rows[2][0] == act2
    assert rows[3][0] == act3
    assert rows[1][-1] == ""
    assert rows[2][-1] == message
    assert rows[3][-1] == ""


def test_stats(activity_report, activity, act2, act3, act1_time, act2_time, act3_time):
    """Correct behavior of `stats` command"""
    with open(REPORT_FILE, "w", encoding="ascii", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(activity_report)

    with Popen(["stats"], stdout=PIPE, stderr=PIPE, text=True) as process:
        (out, err) = process.communicate()

    assert out == f"{activity}: {act1_time}\n{act2}: {act2_time}\n{act3}: {act3_time}\n"
    assert err == ""

    with Popen(["stats", "-a", act2, act3], stdout=PIPE, stderr=PIPE, text=True) as process:
        (out, err) = process.communicate()

    assert out == f"{act2}: {act2_time}\n{act3}: {act3_time}\n"
    assert err == ""


def report(activity_report):
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

    assert rows == activity_report
